#!/usr/bin/env python3
"""Reject incomplete, stale, or invalid Filament 5 visual catalog data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = SKILL_ROOT / "references" / "visual-catalog.json"
INVENTORY_PATH = SKILL_ROOT / "references" / "screenshot-inventory.json"
DOC_PREFIX = "https://filamentphp.com/docs/5.x/"
IMAGE_PREFIX = "https://filamentphp.com/docs/images/5.x/"


def validate(catalog: dict[str, Any], inventory: dict[str, Any]) -> list[str]:
    """Return deterministic validation errors for catalog and inventory contracts."""
    errors: list[str] = []
    crawl = inventory.get("crawl", {})
    crawl_pages = crawl.get("pages")
    if crawl.get("status") != "complete" or not isinstance(crawl_pages, list) or not crawl_pages:
        errors.append("inventory is missing a complete crawl contract")
    elif crawl_pages != sorted(set(crawl_pages)):
        errors.append("inventory crawl pages are not stably ordered")
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
        family = screenshot.get("family")
        if family not in patterns:
            errors.append(f"{name} references unknown family {family}")
        if screenshot.get("decision_relevance") == "decision-changing" and not screenshot.get("variant"):
            errors.append(f"{name} needs a variant for a decision-changing screenshot")
    return sorted(errors)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the Filament 5 visual catalog.")
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    args = parser.parse_args()
    errors = validate(json.loads(args.catalog.read_text()), json.loads(args.inventory.read_text()))
    if errors:
        raise SystemExit("Visual catalog validation failed:\n- " + "\n- ".join(errors))
    print("Visual catalog validation passed.")


if __name__ == "__main__":
    main()
