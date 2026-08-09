#!/usr/bin/env python3
"""Reject invalid reference compositions and stale screenshot inventory data.

Two gates:

* Every ``php`` block in a composition file must parse. Blocks are fragments, so
  each is wrapped in the smallest context that makes it a valid file before
  ``php -l`` runs. See :func:`wrap_fragment` for the six recognised shapes.
* Every pattern must carry ``When``, ``Not when``, and ``Source`` with official
  Filament URLs, use no placeholder identifiers, and avoid namespaces removed in
  Filament 5.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_ROOT / "references"
INVENTORY_PATH = REFERENCES / "screenshot-inventory.json"
DOC_PREFIX = "https://filamentphp.com/docs/5.x/"
IMAGE_PREFIX = "https://filamentphp.com/docs/images/5.x/"

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
PATTERN_HEADING = re.compile(r"^## (.+)$", re.M)
PLACEHOLDER = re.compile(r"\b(YourModel|YourResource|your_[a-z_]+|FooBar)\b")
REMOVED_NAMESPACE = "Filament\\Tables\\Actions\\"
REQUIRED_FIELDS = ("**When**", "**Not when**", "**Source**")


def wrap_fragment(code: str) -> str:
    """Wrap a composition fragment in the smallest valid PHP file.

    Compositions are fragments meant to be pasted into an existing class, schema
    array, or chain, so none of them parse on their own. Six shapes are handled;
    anything else is treated as an array element list.
    """
    uses = [line for line in code.splitlines() if line.startswith("use ")]
    body = [line for line in code.splitlines() if not line.startswith("use ")]
    src = "\n".join(body).strip()
    head = "<?php\n" + "\n".join(uses) + "\n"

    if src.startswith("namespace ") or re.match(
        r"(final|abstract|readonly)?\s*\b(class|enum|interface|trait)\b", src
    ):
        return head + src + "\n"
    if re.match(r"(public|protected|private|static|function)\b", src):
        return head + "class __Probe {\n" + src + "\n}\n"
    if src.startswith("return "):
        return head + "class __Probe { public function __p($table) {\n" + src + "\n} }\n"
    if src.startswith("->"):
        return head + "$__p = $table\n" + src.rstrip(";") + ";\n"
    if src.endswith(";"):
        return head + src + "\n"
    return head + "$__p = [\n" + src.rstrip(",") + ",\n];\n"


def lint_php(code: str, *, php: str = "php") -> str | None:
    """Return a parse error for ``code``, or ``None`` when it parses."""
    with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False) as handle:
        handle.write(wrap_fragment(code))
        path = handle.name
    try:
        completed = subprocess.run([php, "-l", path], capture_output=True, text=True)
    finally:
        Path(path).unlink(missing_ok=True)
    if completed.returncode == 0:
        return None
    output = completed.stdout.strip() or completed.stderr.strip()
    return output.splitlines()[0] if output else "unknown parse failure"


def validate_composition(name: str, text: str, *, php: str | None = "php") -> list[str]:
    """Return deterministic errors for one composition file."""
    errors: list[str] = []

    headings = PATTERN_HEADING.findall(text)
    if not headings:
        errors.append(f"{name} declares no pattern")

    for section in re.split(r"^## ", text, flags=re.M)[1:]:
        title = section.splitlines()[0].strip()
        preamble = section.split("\n### ")[0]
        for field in REQUIRED_FIELDS:
            if field not in preamble:
                errors.append(f"{name}: pattern {title!r} is missing {field}")
        if "**Source**" in preamble and not (
            DOC_PREFIX in preamble or IMAGE_PREFIX in preamble
        ):
            errors.append(f"{name}: pattern {title!r} has no official Source URL")

    for placeholder in sorted(set(PLACEHOLDER.findall(text))):
        errors.append(f"{name}: uses placeholder identifier {placeholder!r}")

    if REMOVED_NAMESPACE in text:
        errors.append(f"{name}: uses {REMOVED_NAMESPACE}, removed in Filament 5")

    blocks = PHP_BLOCK.findall(text)
    if not blocks:
        errors.append(f"{name} ships no php composition")
    if php is not None:
        for index, block in enumerate(blocks, start=1):
            failure = lint_php(block, php=php)
            if failure:
                errors.append(f"{name}: php block {index} does not parse: {failure}")

    return errors


def validate_compositions(
    *, references: Path = REFERENCES, php: str | None = "php"
) -> list[str]:
    """Return errors across every composition file the skill ships."""
    errors: list[str] = []
    for name in COMPOSITION_FILES:
        path = references / name
        if not path.is_file():
            errors.append(f"{name} is missing")
            continue
        errors.extend(validate_composition(name, path.read_text(), php=php))
    return errors


def validate_inventory(inventory: dict[str, Any]) -> list[str]:
    """Return errors for the screenshot inventory's own contracts.

    The inventory is the discovery asset: it records which official screenshots
    exist and which ones change a composition decision. Patterns without a
    reference composition are expansion work, not errors.
    """
    errors: list[str] = []

    crawl = inventory.get("crawl", {})
    crawl_pages = crawl.get("pages")
    if crawl.get("status") != "complete" or not isinstance(crawl_pages, list) or not crawl_pages:
        errors.append("inventory is missing a complete crawl contract")
    elif crawl_pages != sorted(set(crawl_pages)):
        errors.append("inventory crawl pages are not stably ordered")

    manifest = crawl.get("manifest")
    if not isinstance(manifest, dict) or set(manifest) != set(crawl_pages or []):
        errors.append("inventory is missing a complete crawl manifest")
    else:
        actual: dict[str, list[str]] = {page: [] for page in crawl_pages}
        for screenshot in inventory.get("screenshots", []):
            pages = screenshot.get("documentation_pages", [screenshot.get("documentation", "")])
            if not isinstance(pages, list) or not pages:
                errors.append(f"{screenshot.get('name', '<unnamed>')} is missing documentation_pages")
                continue
            for page in pages:
                actual.setdefault(page, []).append(screenshot.get("name", ""))
        if {p: sorted(n) for p, n in actual.items()} != {p: sorted(n) for p, n in manifest.items()}:
            errors.append("inventory does not match its crawl manifest")

    names: set[str] = set()
    for screenshot in inventory.get("screenshots", []):
        name = screenshot.get("name", "<unnamed>")
        if name in names:
            errors.append(f"duplicate screenshot {name}")
        names.add(name)
        for field in ("name", "documentation", "light_image", "dark_image", "status"):
            if not screenshot.get(field):
                errors.append(f"{name} is missing {field}")
        if screenshot.get("status") != "reviewed":
            errors.append(f"{name} is unreviewed")
        if not str(screenshot.get("documentation", "")).startswith(DOC_PREFIX):
            errors.append(f"{name} has an invalid documentation source")
        for field in ("light_image", "dark_image"):
            if not str(screenshot.get(field, "")).startswith(IMAGE_PREFIX):
                errors.append(f"{name} has an invalid {field} source")
        relevance = screenshot.get("decision_relevance")
        if relevance not in {"decision-changing", "non-decision-changing"}:
            errors.append(f"{name} has an invalid decision_relevance")
            continue
        if relevance == "decision-changing":
            if not screenshot.get("family"):
                errors.append(f"{name} needs a family for a decision-changing screenshot")
            if not screenshot.get("variant"):
                errors.append(f"{name} needs a variant for a decision-changing screenshot")

    return errors


def coverage(*, references: Path = REFERENCES) -> tuple[int, int]:
    """Return ``(patterns, variants)`` shipped as reference compositions."""
    patterns = variants = 0
    for name in COMPOSITION_FILES:
        path = references / name
        if not path.is_file():
            continue
        text = path.read_text()
        patterns += len(PATTERN_HEADING.findall(text))
        variants += len(re.findall(r"^### Variant: ", text, re.M))
    return patterns, variants


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Filament 5 reference compositions.")
    parser.add_argument("--references", type=Path, default=REFERENCES)
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument(
        "--skip-php",
        action="store_true",
        help="skip php -l parsing (use only where no php binary is available)",
    )
    args = parser.parse_args()

    php: str | None = None if args.skip_php else shutil.which("php")
    if not args.skip_php and php is None:
        raise SystemExit("php was not found on PATH; install php or pass --skip-php")

    errors = validate_compositions(references=args.references, php=php)
    errors.extend(validate_inventory(json.loads(args.inventory.read_text())))
    errors = sorted(errors)
    if errors:
        raise SystemExit("Composition validation failed:\n- " + "\n- ".join(errors))

    patterns, variants = coverage(references=args.references)
    print(f"Composition validation passed: {patterns} patterns, {variants} variants.")


if __name__ == "__main__":
    main()
