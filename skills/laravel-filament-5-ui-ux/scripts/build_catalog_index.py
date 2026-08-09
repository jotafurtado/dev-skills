#!/usr/bin/env python3
"""Generate the compact visual-catalog index from the reviewed catalog."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = SKILL_ROOT / "references" / "visual-catalog.json"
DEFAULT_OUTPUT = SKILL_ROOT / "references" / "visual-catalog-index.md"

VOCABULARY_DIMENSIONS: tuple[tuple[str, str, str], ...] = (
    ("Surfaces", "surface", "surface"),
    ("Goals", "goals", "goals"),
    ("Workflows", "workflows", "workflows"),
    ("Information shapes", "information_shapes", "information_shapes"),
    ("Relationships", "relationships", "relationships"),
    ("Responsive contexts", "responsive_contexts", "responsive_contexts"),
)


def load_catalog(path: Path = CATALOG_PATH) -> dict[str, Any]:
    """Load the local reviewed catalog."""
    return json.loads(path.read_text())


def _join(values: list[str]) -> str:
    return ", ".join(sorted(values))


def vocabulary_terms(patterns: list[dict[str, Any]], field: str) -> list[str]:
    """Return sorted unique vocabulary terms for one catalog field."""
    terms: set[str] = set()
    for pattern in patterns:
        for term in pattern.get(field, []):
            terms.add(term)
    return sorted(terms)


def render_index(catalog: dict[str, Any]) -> str:
    """Project the catalog into the compact Markdown index."""
    patterns = [
        pattern
        for pattern in catalog.get("patterns", [])
        if pattern.get("status") == "reviewed"
    ]
    patterns = sorted(patterns, key=lambda item: item["id"])

    lines = [
        "# Filament 5 visual pattern index",
        "",
        "Generated from references/visual-catalog.json. Do not edit by hand.",
        "",
        "## Patterns",
        "",
        "| Pattern | Surfaces | Goals | Responsive contexts | Reference | Evidence |",
        "|---|---|---|---|---|---|",
    ]
    for pattern in patterns:
        lines.append(
            "| {id} | {surfaces} | {goals} | {responsive} | {reference} | {evidence} |".format(
                id=pattern["id"],
                surfaces=_join(pattern.get("surface", [])),
                goals=_join(pattern.get("goals", [])),
                responsive=_join(pattern.get("responsive_contexts", [])),
                reference=pattern["routed_reference"],
                evidence=len(pattern.get("visual_evidence", [])),
            )
        )

    lines.extend(["", "## Vocabulary", ""])
    for label, _dimension, field in VOCABULARY_DIMENSIONS:
        terms = vocabulary_terms(patterns, field)
        lines.append(f"**{label}** ({len(terms)}): {_join(terms)}")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the compact visual catalog index.")
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    catalog = load_catalog(args.catalog)
    content = render_index(catalog)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(content)


if __name__ == "__main__":
    main()
