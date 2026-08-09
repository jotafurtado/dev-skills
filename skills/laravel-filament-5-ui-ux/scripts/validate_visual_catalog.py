#!/usr/bin/env python3
"""Reject incomplete, stale, or invalid Filament 5 visual catalog data."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = SKILL_ROOT / "references" / "visual-catalog.json"
INVENTORY_PATH = SKILL_ROOT / "references" / "screenshot-inventory.json"
INDEX_PATH = SKILL_ROOT / "references" / "visual-catalog-index.md"
BUILD_INDEX_SCRIPT = Path(__file__).with_name("build_catalog_index.py")
DOC_PREFIX = "https://filamentphp.com/docs/5.x/"
IMAGE_PREFIX = "https://filamentphp.com/docs/images/5.x/"


def _load_build_index_module() -> Any:
    spec = importlib.util.spec_from_file_location("build_catalog_index", BUILD_INDEX_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def validate_inventory(catalog: dict[str, Any], inventory: dict[str, Any]) -> list[str]:
    """Return deterministic validation errors for inventory contracts."""
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
        actual_manifest: dict[str, list[str]] = {page: [] for page in crawl_pages}
        for screenshot in inventory.get("screenshots", []):
            documentation_pages = screenshot.get("documentation_pages", [screenshot.get("documentation", "")])
            if not isinstance(documentation_pages, list) or not documentation_pages:
                errors.append(f"{screenshot.get('name', '<unnamed>')} is missing documentation_pages")
                continue
            for page in documentation_pages:
                actual_manifest.setdefault(page, []).append(screenshot.get("name", ""))
        actual_manifest = {page: sorted(names) for page, names in actual_manifest.items()}
        expected_manifest = {page: sorted(names) for page, names in manifest.items()}
        if actual_manifest != expected_manifest:
            errors.append("inventory does not match its crawl manifest")
    patterns = {pattern.get("id") for pattern in catalog.get("patterns", [])}
    names: set[str] = set()
    for screenshot in inventory.get("screenshots", []):
        name = screenshot.get("name", "<unnamed>")
        if name in names:
            errors.append(f"duplicate screenshot {name}")
        names.add(name)
        for field in ("name", "documentation", "light_image", "dark_image", "status"):
            if not screenshot.get(field):
                errors.append(f"{name} is missing {field}")
        if not screenshot.get("decision_relevance"):
            errors.append(f"{name} is missing decision_relevance")
        if screenshot.get("status") != "reviewed":
            errors.append(f"{name} is unreviewed")
        if not str(screenshot.get("documentation", "")).startswith(DOC_PREFIX):
            errors.append(f"{name} has an invalid documentation source")
        for field in ("light_image", "dark_image"):
            if not str(screenshot.get(field, "")).startswith(IMAGE_PREFIX):
                errors.append(f"{name} has an invalid {field} source")
        decision_relevance = screenshot.get("decision_relevance")
        if decision_relevance not in {"decision-changing", "non-decision-changing"}:
            errors.append(f"{name} has an invalid decision_relevance")
            continue
        family = screenshot.get("family")
        if decision_relevance == "decision-changing":
            if family not in patterns:
                errors.append(f"{name} references unknown family {family}")
            if not screenshot.get("variant"):
                errors.append(f"{name} needs a variant for a decision-changing screenshot")
        elif family is not None and family not in patterns:
            errors.append(f"{name} references unknown family {family}")
    return errors


def validate_index(
    catalog: dict[str, Any],
    *,
    skill_root: Path = SKILL_ROOT,
    index_path: Path = INDEX_PATH,
) -> list[str]:
    """Return errors for missing routes or index drift against the catalog."""
    errors: list[str] = []
    for pattern in catalog.get("patterns", []):
        pattern_id = pattern.get("id", "<unnamed>")
        routed = pattern.get("routed_reference")
        if not routed:
            errors.append(f"{pattern_id} is missing routed_reference")
            continue
        target = skill_root / routed
        if not target.is_file():
            errors.append(f"{pattern_id} routed_reference does not exist: {routed}")

    build_index = _load_build_index_module()
    expected = build_index.render_index(catalog)
    if not index_path.is_file():
        errors.append(
            "visual-catalog-index.md is missing; regenerate with "
            "scripts/build_catalog_index.py"
        )
    else:
        actual = index_path.read_text()
        if actual != expected:
            errors.append(
                "visual-catalog-index.md drifts from the catalog; regenerate with "
                "python3 skills/laravel-filament-5-ui-ux/scripts/build_catalog_index.py "
                "--output skills/laravel-filament-5-ui-ux/references/visual-catalog-index.md"
            )
    return errors


def validate(catalog: dict[str, Any], inventory: dict[str, Any]) -> list[str]:
    """Return deterministic validation errors for inventory contracts."""
    return sorted(validate_inventory(catalog, inventory))


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the Filament 5 visual catalog.")
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--index", type=Path, default=INDEX_PATH)
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text())
    inventory = json.loads(args.inventory.read_text())
    errors = validate_inventory(catalog, inventory)
    errors.extend(validate_index(catalog, index_path=args.index))
    errors = sorted(errors)
    if errors:
        raise SystemExit("Visual catalog validation failed:\n- " + "\n- ".join(errors))
    print("Visual catalog validation passed.")


if __name__ == "__main__":
    main()
