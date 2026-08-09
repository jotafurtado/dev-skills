#!/usr/bin/env python3
"""Verify every Filament symbol used by a reference composition exists in a real install.

``validate_compositions.py`` proves the compositions parse. It cannot prove the
APIs are real: a class renamed or moved between Filament versions still parses.
This script resolves a Composer fixture and checks each imported Filament class
and each enum case the compositions reference against the installed source.

The fixture is reused between runs. Delete it to force a fresh resolution.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]
REFERENCES = SKILL_ROOT / "references"
DEFAULT_FIXTURE = REPO_ROOT / ".filament-fixture"
DEFAULT_CONSTRAINT = "^5.0"

COMPOSITION_FILES = (
    "table.md",
    "form-layout.md",
    "form-fields.md",
    "form-inputs.md",
    "record-detail.md",
    "dashboard.md",
    "panel-shell.md",
    "action-feedback.md",
)

PHP_BLOCK = re.compile(r"```php\n(.*?)```", re.S)
IMPORT = re.compile(r"^use\s+(Filament\\[A-Za-z0-9_\\]+);", re.M)
STATIC_MEMBER = re.compile(r"\b([A-Z][A-Za-z0-9_]*)::([A-Za-z_][A-Za-z0-9_]*)")


def collect_symbols(references: Path) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Return ``(classes, enum_cases)`` referenced by the compositions.

    ``classes`` maps a fully qualified Filament class to the files using it.
    ``enum_cases`` maps ``FQCN::Case`` to the files using it. Method calls are
    not collected: resolving the receiver of a fluent chain needs real type
    inference, which the Composer fixture cannot cheaply provide.
    """
    classes: dict[str, set[str]] = {}
    enum_cases: dict[str, set[str]] = {}

    for name in COMPOSITION_FILES:
        path = references / name
        if not path.is_file():
            continue
        text = path.read_text()
        aliases: dict[str, str] = {}
        for block in PHP_BLOCK.findall(text):
            for fqcn in IMPORT.findall(block):
                aliases[fqcn.rsplit("\\", 1)[-1]] = fqcn
                classes.setdefault(fqcn, set()).add(name)
        for block in PHP_BLOCK.findall(text):
            for short, member in STATIC_MEMBER.findall(block):
                fqcn = aliases.get(short)
                if fqcn is None or member in {"make", "class"}:
                    continue
                if member[:1].isupper():
                    enum_cases.setdefault(f"{fqcn}::{member}", set()).add(name)

    return classes, enum_cases


def ensure_fixture(fixture: Path, constraint: str, *, refresh: bool) -> str:
    """Resolve ``filament/filament`` into ``fixture`` and return the version."""
    if refresh and fixture.exists():
        shutil.rmtree(fixture)
    fixture.mkdir(parents=True, exist_ok=True)

    manifest = fixture / "composer.json"
    desired = {
        "name": "dev-skills/filament-fixture",
        "description": "Resolves Filament so composition APIs can be verified.",
        "require": {"filament/filament": constraint},
        "minimum-stability": "stable",
        "config": {"allow-plugins": {"*": True}},
    }
    if not manifest.is_file() or json.loads(manifest.read_text()) != desired:
        manifest.write_text(json.dumps(desired, indent=2) + "\n")
        if (fixture / "composer.lock").exists():
            (fixture / "composer.lock").unlink()

    if not (fixture / "vendor" / "autoload.php").is_file():
        completed = subprocess.run(
            ["composer", "install", "--no-interaction", "--no-progress", "--quiet"],
            cwd=fixture,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            raise SystemExit(
                "composer install failed in the fixture:\n"
                + (completed.stderr.strip() or completed.stdout.strip())
            )

    installed = json.loads((fixture / "vendor" / "composer" / "installed.json").read_text())
    packages = installed.get("packages", installed)
    for package in packages:
        if package.get("name") == "filament/filament":
            return package.get("version", "unknown")
    return "unknown"


def check_symbols(
    fixture: Path, classes: dict[str, set[str]], enum_cases: dict[str, set[str]]
) -> list[str]:
    """Return one error per symbol missing from the installed Filament."""
    probe = {
        "classes": sorted(classes),
        "enum_cases": sorted(enum_cases),
    }
    script = fixture / "probe.php"
    script.write_text(
        "<?php\n"
        "require __DIR__ . '/vendor/autoload.php';\n"
        "$probe = json_decode(file_get_contents($argv[1]), true);\n"
        "$missing = ['classes' => [], 'enum_cases' => []];\n"
        "foreach ($probe['classes'] as $fqcn) {\n"
        "    if (!class_exists($fqcn) && !interface_exists($fqcn)"
        " && !trait_exists($fqcn) && !enum_exists($fqcn)) {\n"
        "        $missing['classes'][] = $fqcn;\n"
        "    }\n"
        "}\n"
        "foreach ($probe['enum_cases'] as $case) {\n"
        "    [$fqcn, $name] = explode('::', $case, 2);\n"
        "    if (!defined($case) && !(enum_exists($fqcn) && in_array($name,"
        " array_column($fqcn::cases(), 'name'), true))) {\n"
        "        $missing['enum_cases'][] = $case;\n"
        "    }\n"
        "}\n"
        "echo json_encode($missing);\n"
    )
    payload = fixture / "probe.json"
    payload.write_text(json.dumps(probe))

    completed = subprocess.run(
        ["php", str(script), str(payload)], capture_output=True, text=True
    )
    if completed.returncode != 0:
        raise SystemExit(
            "probe failed:\n" + (completed.stderr.strip() or completed.stdout.strip())
        )

    missing = json.loads(completed.stdout)
    errors: list[str] = []
    for fqcn in missing["classes"]:
        where = ", ".join(sorted(classes[fqcn]))
        errors.append(f"class {fqcn} does not exist in the installed Filament ({where})")
    for case in missing["enum_cases"]:
        where = ", ".join(sorted(enum_cases[case]))
        errors.append(f"enum case {case} does not exist in the installed Filament ({where})")
    return sorted(errors)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--references", type=Path, default=REFERENCES)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--constraint", default=DEFAULT_CONSTRAINT)
    parser.add_argument("--refresh", action="store_true", help="discard and re-resolve the fixture")
    args = parser.parse_args()

    for binary in ("php", "composer"):
        if shutil.which(binary) is None:
            raise SystemExit(f"{binary} was not found on PATH")

    classes, enum_cases = collect_symbols(args.references)
    if not classes:
        raise SystemExit("no Filament imports found in the compositions")

    version = ensure_fixture(args.fixture, args.constraint, refresh=args.refresh)
    errors = check_symbols(args.fixture, classes, enum_cases)

    print(f"Filament {version} · {len(classes)} classes · {len(enum_cases)} enum cases")
    if errors:
        print("\nAPI verification failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print("API verification passed.")


if __name__ == "__main__":
    main()
