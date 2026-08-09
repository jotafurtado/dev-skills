#!/usr/bin/env python3
"""Query reviewed Filament 5 visual patterns without network access."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CATALOG_PATH = Path(__file__).resolve().parents[1] / "references" / "visual-catalog.json"


def load_catalog() -> dict[str, Any]:
    """Load the local reviewed catalog."""
    return json.loads(CATALOG_PATH.read_text())


def _score_pattern(
    pattern: dict[str, Any],
    *,
    surface: str,
    goal: str,
    workflow: str,
    available_width: str,
    information_shape: str | None,
    relationship: str | None,
    responsive_context: str | None,
) -> int:
    score = 0
    score += 8 if surface in pattern["surface"] else -100
    score += 4 if goal in pattern["goals"] else 0
    score += 3 if workflow in pattern["workflows"] else -100
    score += 3 if available_width in pattern["available_width"] else -100
    if information_shape:
        score += 2 if information_shape in pattern.get("information_shapes", []) else -100
    if relationship:
        score += 2 if relationship in pattern.get("relationships", []) else -100
    if responsive_context:
        score += 2 if responsive_context in pattern.get("responsive_contexts", []) else -100
    score += pattern.get("selection_weight", 0)
    return score


def query_catalog(
    *,
    surface: str,
    goal: str,
    workflow: str,
    available_width: str,
    information_shape: str | None = None,
    relationship: str | None = None,
    responsive_context: str | None = None,
) -> dict[str, Any]:
    """Return reviewed candidates and a deterministic selected pattern."""
    patterns = load_catalog()["patterns"]
    ranked = [
        (pattern, _score_pattern(
            pattern,
            surface=surface,
            goal=goal,
            workflow=workflow,
            available_width=available_width,
            information_shape=information_shape,
            relationship=relationship,
            responsive_context=responsive_context,
        ))
        for pattern in patterns
        if surface in pattern["surface"] and pattern["status"] == "reviewed"
    ]
    ranked = [item for item in ranked if item[1] >= 0]
    ranked.sort(key=lambda item: (-item[1], item[0]["id"]))

    if not ranked:
        raise ValueError(
            "No reviewed visual pattern matches the requested surface. "
            "Use official Filament 5 evidence and record the catalog gap."
        )

    candidates = [pattern for pattern, _score in ranked if goal in pattern["goals"]]
    if not candidates:
        candidates = [pattern for pattern, _score in ranked]

    selected_pattern = candidates[0]
    return {
        "query": {
            "surface": surface,
            "goal": goal,
            "workflow": workflow,
            "available_width": available_width,
            "information_shape": information_shape,
            "relationship": relationship,
            "responsive_context": responsive_context,
        },
        "candidates": candidates,
        "selected_pattern": selected_pattern,
        "decision_trace": {
            "surface": surface,
            "goal": goal,
            "official_candidates": [candidate["id"] for candidate in candidates],
            "visual_evidence": selected_pattern["visual_evidence"],
            "selected_pattern": selected_pattern["id"],
            "requires_direct_inspection": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Query reviewed Filament 5 visual patterns."
    )
    parser.add_argument("--surface", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--available-width", required=True)
    parser.add_argument("--information-shape")
    parser.add_argument("--relationship")
    parser.add_argument("--responsive-context")
    args = parser.parse_args()

    result = query_catalog(
        surface=args.surface,
        goal=args.goal,
        workflow=args.workflow,
        available_width=args.available_width,
        information_shape=args.information_shape,
        relationship=args.relationship,
        responsive_context=args.responsive_context,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
