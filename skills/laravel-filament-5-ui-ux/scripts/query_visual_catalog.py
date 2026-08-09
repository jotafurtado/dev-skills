#!/usr/bin/env python3
"""Query reviewed Filament 5 visual patterns without network access."""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path
from typing import Any


CATALOG_PATH = Path(__file__).resolve().parents[1] / "references" / "visual-catalog.json"

DIMENSION_FIELDS: dict[str, str] = {
    "surface": "surface",
    "goal": "goals",
    "workflow": "workflows",
    "responsive_context": "responsive_contexts",
    "information_shape": "information_shapes",
    "relationship": "relationships",
}

DIMENSION_WEIGHTS: dict[str, int] = {
    "goal": 4,
    "workflow": 3,
    "responsive_context": 2,
    "information_shape": 2,
    "relationship": 2,
}


def load_catalog() -> dict[str, Any]:
    """Load the local reviewed catalog."""
    return json.loads(CATALOG_PATH.read_text())


def vocabulary_from_catalog(catalog: dict[str, Any] | None = None) -> dict[str, list[str]]:
    """Extract sorted controlled vocabulary per query dimension."""
    patterns = (catalog or load_catalog())["patterns"]
    vocabulary: dict[str, list[str]] = {}
    for dimension, field in DIMENSION_FIELDS.items():
        terms: set[str] = set()
        for pattern in patterns:
            for term in pattern.get(field, []):
                terms.add(term)
        vocabulary[dimension] = sorted(terms)
    return vocabulary


def _format_invalid_term(dimension: str, value: str, valid_terms: list[str]) -> str:
    suggestions = difflib.get_close_matches(value, valid_terms, n=5, cutoff=0.6)
    if suggestions:
        suggestion_text = ", ".join(suggestions)
        return (
            f"Invalid {dimension} '{value}'. Did you mean: {suggestion_text}? "
            f"Valid terms: {', '.join(valid_terms)}"
        )
    return (
        f"Invalid {dimension} '{value}'. "
        f"Valid terms: {', '.join(valid_terms)}"
    )


def _validate_term(dimension: str, value: str | None, vocabulary: dict[str, list[str]]) -> None:
    if value is None:
        return
    valid_terms = vocabulary[dimension]
    if value not in valid_terms:
        raise ValueError(_format_invalid_term(dimension, value, valid_terms))


def _score_pattern(
    pattern: dict[str, Any],
    *,
    goal: str,
    workflow: str | None,
    information_shape: str | None,
    relationship: str | None,
    responsive_context: str | None,
) -> int:
    score = pattern.get("selection_weight", 0)
    if goal in pattern["goals"]:
        score += DIMENSION_WEIGHTS["goal"]
    if workflow and workflow in pattern["workflows"]:
        score += DIMENSION_WEIGHTS["workflow"]
    if information_shape and information_shape in pattern.get("information_shapes", []):
        score += DIMENSION_WEIGHTS["information_shape"]
    if relationship and relationship in pattern.get("relationships", []):
        score += DIMENSION_WEIGHTS["relationship"]
    if responsive_context and responsive_context in pattern.get("responsive_contexts", []):
        score += DIMENSION_WEIGHTS["responsive_context"]
    return score


def query_catalog(
    *,
    surface: str,
    goal: str,
    workflow: str | None = None,
    information_shape: str | None = None,
    relationship: str | None = None,
    responsive_context: str | None = None,
) -> dict[str, Any]:
    """Return reviewed candidates and a deterministic selected pattern."""
    catalog = load_catalog()
    vocabulary = vocabulary_from_catalog(catalog)

    _validate_term("surface", surface, vocabulary)
    _validate_term("goal", goal, vocabulary)
    _validate_term("workflow", workflow, vocabulary)
    _validate_term("information_shape", information_shape, vocabulary)
    _validate_term("relationship", relationship, vocabulary)
    _validate_term("responsive_context", responsive_context, vocabulary)

    patterns = catalog["patterns"]
    ranked = [
        (
            pattern,
            _score_pattern(
                pattern,
                goal=goal,
                workflow=workflow,
                information_shape=information_shape,
                relationship=relationship,
                responsive_context=responsive_context,
            ),
        )
        for pattern in patterns
        if surface in pattern["surface"] and pattern["status"] == "reviewed"
    ]
    ranked.sort(key=lambda item: (-item[1], item[0]["id"]))

    goal_matches = [pattern for pattern, _score in ranked if goal in pattern["goals"]]
    candidates = goal_matches if goal_matches else [pattern for pattern, _score in ranked]
    selected_pattern = candidates[0]
    return {
        "query": {
            "surface": surface,
            "goal": goal,
            "workflow": workflow,
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


def _print_vocabulary(vocabulary: dict[str, list[str]]) -> None:
    labels = {
        "surface": "Surfaces",
        "goal": "Goals",
        "workflow": "Workflows",
        "information_shape": "Information shapes",
        "relationship": "Relationships",
        "responsive_context": "Responsive contexts",
    }
    for dimension, label in labels.items():
        terms = vocabulary[dimension]
        print(f"{label} ({len(terms)}): {', '.join(terms)}")


def main() -> None:
    catalog = load_catalog()
    vocabulary = vocabulary_from_catalog(catalog)

    parser = argparse.ArgumentParser(
        description="Query reviewed Filament 5 visual patterns."
    )
    parser.add_argument("--list-vocabulary", action="store_true")
    parser.add_argument("--surface", choices=vocabulary["surface"])
    parser.add_argument("--goal", choices=vocabulary["goal"])
    parser.add_argument("--workflow", choices=vocabulary["workflow"])
    parser.add_argument("--information-shape", choices=vocabulary["information_shape"])
    parser.add_argument("--relationship", choices=vocabulary["relationship"])
    parser.add_argument("--responsive-context", choices=vocabulary["responsive_context"])
    args = parser.parse_args()

    if args.list_vocabulary:
        _print_vocabulary(vocabulary)
        return

    if not args.surface or not args.goal:
        parser.error("--surface and --goal are required unless --list-vocabulary is set")

    try:
        result = query_catalog(
            surface=args.surface,
            goal=args.goal,
            workflow=args.workflow,
            information_shape=args.information_shape,
            relationship=args.relationship,
            responsive_context=args.responsive_context,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc

    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
