#!/usr/bin/env python3
"""Repository-level skill evaluation harness."""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

try:
    from maintenance.eval_judges import (
        DescriptionJudge,
        InfrastructureError,
        Judge,
        LiveJudge,
        MockJudge,
        load_judge,
    )
except ModuleNotFoundError:  # python3 maintenance/eval_skills.py
    from eval_judges import (
        DescriptionJudge,
        InfrastructureError,
        Judge,
        LiveJudge,
        MockJudge,
        load_judge,
    )

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
TRIGGER_RUNS = 3
SPLITS = frozenset({"train", "validation"})
CASE_VARIANTS = ("with_skill", "no_skill")


@dataclass
class TriggerQuery:
    index: int
    query: str
    should_trigger: bool
    split: str | None = None

    @classmethod
    def from_dict(cls, index: int, raw: dict[str, Any]) -> TriggerQuery:
        split = raw.get("split")
        if split is not None and split not in SPLITS:
            raise ValueError(f"query {index}: split must be one of {sorted(SPLITS)}")
        return cls(
            index=index,
            query=str(raw["query"]),
            should_trigger=bool(raw["should_trigger"]),
            split=split,
        )


@dataclass
class OutputEval:
    id: int
    prompt: str
    expected_output: str
    assertions: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    limits: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> OutputEval:
        limits = raw.get("limits", [])
        if not isinstance(limits, list) or not all(isinstance(item, str) and item.strip() for item in limits):
            raise ValueError(f"output eval {raw.get('id')}: limits must be an array of non-empty strings")
        return cls(
            id=int(raw["id"]),
            prompt=str(raw["prompt"]),
            expected_output=str(raw.get("expected_output", "")),
            assertions=[str(item) for item in raw.get("assertions", [])],
            files=[str(item) for item in raw.get("files", [])],
            limits=[item.strip() for item in limits],
        )


@dataclass
class SkillDatasets:
    name: str
    skill_dir: Path
    trigger_queries: list[TriggerQuery] = field(default_factory=list)
    output_evals: list[OutputEval] = field(default_factory=list)


@dataclass
class CaseResult:
    skill: str
    case_id: str
    variant: str | None
    run_index: int | None
    passed: bool | None
    infrastructure: str | None = None
    grading_path: Path | None = None
    timing_path: Path | None = None
    outputs_dir: Path | None = None
    split: str | None = None
    kind: Literal["trigger", "output"] = "trigger"
    counts_as_grade: bool = True


def discover_skills(skills_dir: Path = SKILLS_DIR) -> list[SkillDatasets]:
    discovered: list[SkillDatasets] = []
    if not skills_dir.is_dir():
        return discovered

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        evals_dir = skill_dir / "evals"
        if not evals_dir.is_dir():
            continue

        trigger_path = evals_dir / "eval_queries.json"
        output_path = evals_dir / "evals.json"
        if not trigger_path.is_file() and not output_path.is_file():
            continue

        datasets = SkillDatasets(name=skill_dir.name, skill_dir=skill_dir)
        if trigger_path.is_file():
            raw_queries = json.loads(trigger_path.read_text(encoding="utf-8"))
            if not isinstance(raw_queries, list):
                raise ValueError(f"{trigger_path}: expected a JSON array")
            datasets.trigger_queries = [
                TriggerQuery.from_dict(index, item) for index, item in enumerate(raw_queries)
            ]

        if output_path.is_file():
            raw_output = json.loads(output_path.read_text(encoding="utf-8"))
            if not isinstance(raw_output, dict):
                raise ValueError(f"{output_path}: expected a JSON object")
            skill_name = raw_output.get("skill_name", skill_dir.name)
            if skill_name != skill_dir.name:
                raise ValueError(
                    f"{output_path}: skill_name '{skill_name}' does not match directory '{skill_dir.name}'"
                )
            eval_items = raw_output.get("evals", [])
            if not isinstance(eval_items, list):
                raise ValueError(f"{output_path}: evals must be an array")
            datasets.output_evals = [OutputEval.from_dict(item) for item in eval_items]

        discovered.append(datasets)
    return discovered


def validate_datasets(skills_dir: Path = SKILLS_DIR) -> list[str]:
    errors: list[str] = []
    try:
        skills = discover_skills(skills_dir)
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        return [str(exc)]

    if not skills:
        errors.append(f"no skill eval datasets found under {skills_dir}")

    for skill in skills:
        if not skill.trigger_queries and not skill.output_evals:
            errors.append(f"{skill.name}: evals directory exists but has no datasets")

        for query in skill.trigger_queries:
            if not query.query.strip():
                errors.append(f"{skill.name}: trigger query {query.index} is empty")

        for output_eval in skill.output_evals:
            if not output_eval.prompt.strip():
                errors.append(f"{skill.name}: output eval {output_eval.id} has empty prompt")
            if not output_eval.assertions:
                errors.append(
                    f"{skill.name}: output eval {output_eval.id} has no assertions"
                )
            root = skills_dir.parent.resolve()
            for relative in output_eval.files:
                path = (skills_dir.parent / relative).resolve()
                if not path.is_relative_to(root) or not path.is_file():
                    errors.append(
                        f"{skill.name}: output eval {output_eval.id} fixture missing: {relative}"
                    )
                elif path.stat().st_size == 0:
                    errors.append(
                        f"{skill.name}: output eval {output_eval.id} fixture empty: {relative}"
                    )

    return errors


def available_skill_names(skills_dir: Path = SKILLS_DIR) -> list[str]:
    return sorted(
        path.name for path in skills_dir.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    )


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _judge_model(judge: Judge) -> str | None:
    if isinstance(judge, MockJudge):
        return "mock"
    if isinstance(judge, DescriptionJudge):
        return "description"
    if isinstance(judge, LiveJudge):
        return judge.model
    return None


def evidence_mode_for(judge_name: str) -> str:
    return {"mock": "simulated", "description": "offline", "live": "model"}.get(judge_name, "model")


def combine_token_usage(*groups: int | None) -> tuple[int | None, str]:
    known = [value for value in groups if type(value) is int]
    if not known:
        return None, "unavailable"
    if len(known) != len(groups):
        return sum(known), "partial"
    return sum(known), "available"


def _write_raw(outputs_dir: Path, raw: str | None) -> None:
    if raw:
        (outputs_dir / "raw_reply.txt").write_text(raw, encoding="utf-8")


def run_trigger_case(
    skill: SkillDatasets,
    query: TriggerQuery,
    run_index: int,
    judge: Judge,
    out_dir: Path,
    available_skills: list[str],
) -> CaseResult:
    case_id = f"trigger-{query.index:03d}-run-{run_index + 1}"
    case_dir = out_dir / skill.name / case_id
    outputs_dir = case_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    started = time.perf_counter()
    infrastructure: str | None = None
    selected: list[str] = []
    passed: bool | None = None
    raw_reply: str | None = None
    finish_reason: str | None = None
    judge.usage_tokens = None

    try:
        selected = judge.select_skills(query.query, available_skills)
        triggered = skill.name in selected
        passed = triggered == query.should_trigger
    except InfrastructureError as exc:
        infrastructure = exc.kind
        passed = None
        raw_reply = exc.raw
        finish_reason = exc.finish_reason
        if type(exc.total_tokens) is int:
            judge.usage_tokens = exc.total_tokens
        _write_raw(outputs_dir, raw_reply)

    duration_ms = int((time.perf_counter() - started) * 1000)
    total_tokens, token_usage = combine_token_usage(judge.usage_tokens)
    timing = {
        "duration_ms": duration_ms,
        "total_tokens": total_tokens,
        "token_usage": token_usage,
        "model": _judge_model(judge),
    }
    grading = {
        "kind": "trigger",
        "skill": skill.name,
        "case_id": case_id,
        "run_index": run_index + 1,
        "split": query.split,
        "query": query.query,
        "expected_should_trigger": query.should_trigger,
        "selected_skills": selected,
        "triggered": None if infrastructure else skill.name in selected,
        "passed": passed,
        "infrastructure": infrastructure,
        "finish_reason": finish_reason,
        "raw_reply": raw_reply,
    }

    write_json(case_dir / "timing.json", timing)
    write_json(case_dir / "grading.json", grading)
    (outputs_dir / "selection.json").write_text(
        json.dumps({"selected_skills": selected}, indent=2) + "\n",
        encoding="utf-8",
    )

    return CaseResult(
        skill=skill.name,
        case_id=case_id,
        variant=None,
        run_index=run_index + 1,
        passed=passed,
        infrastructure=infrastructure,
        grading_path=case_dir / "grading.json",
        timing_path=case_dir / "timing.json",
        outputs_dir=outputs_dir,
        split=query.split,
        kind="trigger",
    )


def run_output_case(
    skill: SkillDatasets,
    output_eval: OutputEval,
    variant: str,
    judge: Judge,
    out_dir: Path,
) -> CaseResult:
    case_id = f"output-{output_eval.id:03d}-{variant}"
    case_dir = out_dir / skill.name / case_id
    outputs_dir = case_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    skill_name = skill.name if variant == "with_skill" else None
    started = time.perf_counter()
    infrastructure: str | None = None
    grading_payload: dict[str, Any] | None = None
    passed: bool | None = None
    completion: dict[str, Any] | None = None
    raw_reply: str | None = None
    finish_reason: str | None = None
    counts_as_grade = True
    generation_tokens: int | None = None
    grade_tokens: int | None = None
    graded = False

    try:
        judge.usage_tokens = None
        completion = judge.complete(output_eval.prompt, skill_name, output_eval.files)
        generation_tokens = judge.usage_tokens
        if generation_tokens is None and type(completion.get("total_tokens")) is int:
            generation_tokens = completion["total_tokens"]
        output_text = str(completion.get("text") or "")
        (outputs_dir / "response.txt").write_text(
            output_text + ("\n" if output_text else ""),
            encoding="utf-8",
        )
        judge.usage_tokens = None
        grading_payload = judge.grade_output(
            output_eval.prompt,
            output_eval.assertions,
            skill_name,
            output_eval.files,
            output_text,
        )
        raw_reply = grading_payload.get("raw_reply")
        _write_raw(outputs_dir, raw_reply)
        grade_tokens = judge.usage_tokens
        graded = True
        counts_as_grade = bool(grading_payload.get("counts_as_skill_grade", True))
        rate = grading_payload.get("summary", {}).get("pass_rate")
        if counts_as_grade and type(rate) in {int, float}:
            passed = rate >= 1.0
        else:
            passed = None
            counts_as_grade = False
    except InfrastructureError as exc:
        infrastructure = exc.kind
        passed = None
        counts_as_grade = True
        raw_reply = exc.raw
        finish_reason = exc.finish_reason
        _write_raw(outputs_dir, raw_reply)
        if type(exc.total_tokens) is int:
            judge.usage_tokens = exc.total_tokens
        if completion is None:
            generation_tokens = judge.usage_tokens
            preserved = exc.raw if exc.preserve_output and exc.raw else ""
            (outputs_dir / "response.txt").write_text(
                preserved + ("\n" if preserved else ""),
                encoding="utf-8",
            )
        elif judge.usage_tokens is not None:
            grade_tokens = judge.usage_tokens

    duration_ms = int((time.perf_counter() - started) * 1000)
    if graded:
        total_tokens, token_usage = combine_token_usage(generation_tokens, grade_tokens)
    elif generation_tokens is not None or grade_tokens is not None:
        total_tokens = sum(
            value for value in (generation_tokens, grade_tokens) if type(value) is int
        )
        token_usage = "partial"
    else:
        total_tokens, token_usage = None, "unavailable"
    timing = {
        "duration_ms": duration_ms,
        "total_tokens": total_tokens,
        "token_usage": token_usage,
        "model": (None if completion is None else completion.get("model")) or _judge_model(judge),
    }

    evidence_mode = evidence_mode_for("live")
    if completion is not None and isinstance(completion.get("evidence_mode"), str):
        evidence_mode = completion["evidence_mode"]
    elif isinstance(judge, MockJudge):
        evidence_mode = "simulated"
    elif isinstance(judge, DescriptionJudge):
        evidence_mode = "offline"
    elif isinstance(judge, LiveJudge):
        evidence_mode = "model"

    grading = {
        "kind": "output",
        "skill": skill.name,
        "case_id": case_id,
        "variant": variant,
        "prompt": output_eval.prompt,
        "expected_output": output_eval.expected_output,
        "files": output_eval.files,
        "limits": output_eval.limits,
        "execution": "isolated_prompt",
        "evidence_mode": evidence_mode,
        "passed": passed,
        "infrastructure": infrastructure,
        "finish_reason": finish_reason,
        "raw_reply": raw_reply,
    }
    if grading_payload is not None:
        grading.update(grading_payload)
        grading["evidence_mode"] = grading_payload.get("evidence_mode") or evidence_mode
        grading["limits"] = output_eval.limits
        grading["execution"] = "isolated_prompt"
        grading["finish_reason"] = finish_reason
        grading["raw_reply"] = raw_reply

    write_json(case_dir / "timing.json", timing)
    write_json(case_dir / "grading.json", grading)

    return CaseResult(
        skill=skill.name,
        case_id=case_id,
        variant=variant,
        run_index=None,
        passed=passed,
        infrastructure=infrastructure,
        grading_path=case_dir / "grading.json",
        timing_path=case_dir / "timing.json",
        outputs_dir=outputs_dir,
        kind="output",
        counts_as_grade=counts_as_grade and infrastructure is None,
    )


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _stddev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    avg = _mean(values)
    variance = sum((value - avg) ** 2 for value in values) / len(values)
    return math.sqrt(variance)


def aggregate_benchmark(results: list[CaseResult], judge_name: str) -> dict[str, Any]:
    by_skill: dict[str, dict[str, Any]] = {}
    infrastructure_failures: list[dict[str, Any]] = []

    for result in results:
        skill_entry = by_skill.setdefault(
            result.skill,
            {
                "trigger": {
                    "cases": 0,
                    "passed": 0,
                    "failed": 0,
                    "infrastructure_skipped": 0,
                    "ungraded": 0,
                    "pass_rate": 0.0,
                    "by_split": {},
                },
                "output": {
                    variant: {
                        "cases": 0,
                        "passed": 0,
                        "failed": 0,
                        "infrastructure_skipped": 0,
                        "ungraded": 0,
                        "pass_rate": 0.0,
                    }
                    for variant in CASE_VARIANTS
                },
            },
        )

        if result.infrastructure:
            infrastructure_failures.append(
                {
                    "skill": result.skill,
                    "case_id": result.case_id,
                    "kind": result.kind,
                    "infrastructure": result.infrastructure,
                }
            )

        if result.kind == "trigger":
            bucket = skill_entry["trigger"]
            bucket["cases"] += 1
            if result.infrastructure:
                bucket["infrastructure_skipped"] += 1
            elif not result.counts_as_grade:
                bucket["ungraded"] += 1
            elif result.passed:
                bucket["passed"] += 1
            else:
                bucket["failed"] += 1

            if result.split:
                split_bucket = bucket["by_split"].setdefault(
                    result.split,
                    {"cases": 0, "passed": 0, "failed": 0, "infrastructure_skipped": 0},
                )
                split_bucket["cases"] += 1
                if result.infrastructure:
                    split_bucket["infrastructure_skipped"] += 1
                elif result.passed:
                    split_bucket["passed"] += 1
                else:
                    split_bucket["failed"] += 1
        else:
            assert result.variant is not None
            bucket = skill_entry["output"][result.variant]
            bucket["cases"] += 1
            if result.infrastructure:
                bucket["infrastructure_skipped"] += 1
            elif not result.counts_as_grade:
                bucket["ungraded"] += 1
            elif result.passed:
                bucket["passed"] += 1
            else:
                bucket["failed"] += 1

    timing_values: dict[str, list[float]] = {"trigger": [], "output": []}
    for result in results:
        if result.timing_path and result.timing_path.is_file():
            timing = json.loads(result.timing_path.read_text(encoding="utf-8"))
            duration = timing.get("duration_ms")
            if isinstance(duration, (int, float)):
                timing_values[result.kind].append(float(duration))

    for skill_entry in by_skill.values():
        trigger = skill_entry["trigger"]
        graded = trigger["passed"] + trigger["failed"]
        trigger["pass_rate"] = (trigger["passed"] / graded) if graded else 0.0
        for split_bucket in trigger["by_split"].values():
            split_graded = split_bucket["passed"] + split_bucket["failed"]
            split_bucket["pass_rate"] = (
                (split_bucket["passed"] / split_graded) if split_graded else 0.0
            )

        for variant in CASE_VARIANTS:
            bucket = skill_entry["output"][variant]
            graded = bucket["passed"] + bucket["failed"]
            bucket["pass_rate"] = (bucket["passed"] / graded) if graded else 0.0

    with_skill_rates = [
        entry["output"]["with_skill"]["pass_rate"]
        for entry in by_skill.values()
        if entry["output"]["with_skill"]["passed"] + entry["output"]["with_skill"]["failed"]
    ]
    no_skill_rates = [
        entry["output"]["no_skill"]["pass_rate"]
        for entry in by_skill.values()
        if entry["output"]["no_skill"]["passed"] + entry["output"]["no_skill"]["failed"]
    ]

    return {
        "judge": judge_name,
        "evidence_mode": evidence_mode_for(judge_name),
        "skills": by_skill,
        "infrastructure_failures": infrastructure_failures,
        "run_summary": {
            "trigger": {
                "duration_ms": {
                    "mean": _mean(timing_values["trigger"]),
                    "stddev": _stddev(timing_values["trigger"]),
                }
            },
            "output": {
                "duration_ms": {
                    "mean": _mean(timing_values["output"]),
                    "stddev": _stddev(timing_values["output"]),
                }
            },
            "with_skill": {
                "pass_rate": {"mean": _mean(with_skill_rates), "stddev": _stddev(with_skill_rates)}
            },
            "no_skill": {
                "pass_rate": {"mean": _mean(no_skill_rates), "stddev": _stddev(no_skill_rates)}
            },
            "delta": {
                "pass_rate": _mean(with_skill_rates) - _mean(no_skill_rates),
            },
        },
    }


def evaluate_gates(benchmark: dict[str, Any], min_trigger_pass_rate: float) -> list[str]:
    failures: list[str] = []
    evidence_mode = benchmark.get("evidence_mode")
    for skill_name, skill_entry in benchmark.get("skills", {}).items():
        trigger = skill_entry.get("trigger", {})
        trigger_cases = trigger.get("cases", 0)
        trigger_graded = trigger.get("passed", 0) + trigger.get("failed", 0)
        if trigger_cases and trigger_graded == 0 and trigger.get("ungraded", 0) == 0:
            failures.append(f"{skill_name}: trigger run has no graded cases (all skipped)")
        elif trigger_graded and trigger.get("pass_rate", 0.0) < min_trigger_pass_rate:
            failures.append(
                f"{skill_name}: trigger pass_rate {trigger['pass_rate']:.2f} "
                f"below gate {min_trigger_pass_rate:.2f}"
            )

        if evidence_mode != "model":
            continue
        with_skill = skill_entry.get("output", {}).get("with_skill", {})
        output_cases = with_skill.get("cases", 0)
        output_graded = with_skill.get("passed", 0) + with_skill.get("failed", 0)
        if output_cases and output_graded == 0 and with_skill.get("ungraded", 0) == 0:
            failures.append(f"{skill_name}: with_skill output run has no graded cases (all skipped)")
        elif with_skill.get("failed", 0) > 0:
            failures.append(
                f"{skill_name}: output with_skill has {with_skill['failed']} assertion failures"
            )
    return failures


def cmd_discover(args: argparse.Namespace) -> int:
    skills = discover_skills(Path(args.skills_dir))
    payload = {
        "skills_dir": str(Path(args.skills_dir)),
        "count": len(skills),
        "skills": [
            {
                "name": skill.name,
                "trigger_queries": len(skill.trigger_queries),
                "output_evals": len(skill.output_evals),
                "trigger_splits": sorted(
                    {query.split for query in skill.trigger_queries if query.split}
                ),
            }
            for skill in skills
        ],
    }
    print(json.dumps(payload, indent=2))
    return 0


def cmd_validate_datasets(args: argparse.Namespace) -> int:
    errors = validate_datasets(Path(args.skills_dir))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("All skill eval datasets are valid.")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    skills_dir = Path(args.skills_dir)
    judge = load_judge(args.judge, skills_dir)
    skills = discover_skills(skills_dir)
    available_skills = available_skill_names(skills_dir)

    if args.skill:
        skills = [skill for skill in skills if skill.name == args.skill]
        if not skills:
            print(f"skill not found: {args.skill}", file=sys.stderr)
            return 1

    results: list[CaseResult] = []
    for skill in skills:
        queries = skill.trigger_queries
        if args.split:
            queries = [query for query in queries if query.split == args.split]

        if not args.output_only:
            for query in queries:
                for run_index in range(TRIGGER_RUNS):
                    results.append(
                        run_trigger_case(
                            skill,
                            query,
                            run_index,
                            judge,
                            out_dir,
                            available_skills,
                        )
                    )

        for output_eval in skill.output_evals:
            for variant in CASE_VARIANTS:
                results.append(
                    run_output_case(skill, output_eval, variant, judge, out_dir)
                )

    benchmark = aggregate_benchmark(results, args.judge)
    write_json(out_dir / "benchmark.json", benchmark)
    for skill in skills:
        skill_results = [result for result in results if result.skill == skill.name]
        write_json(out_dir / skill.name / "benchmark.json", aggregate_benchmark(skill_results, args.judge))

    if args.gate:
        gate_failures = evaluate_gates(benchmark, args.min_trigger_pass_rate)
        if gate_failures:
            for failure in gate_failures:
                print(failure, file=sys.stderr)
            return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Discover and run skill evaluation datasets for this repository.",
    )
    parser.add_argument(
        "--skills-dir",
        default=str(SKILLS_DIR),
        help="Directory containing skill folders (default: skills/)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    discover_parser = subparsers.add_parser("discover", help="List skills with eval datasets")
    discover_parser.set_defaults(func=cmd_discover)

    validate_parser = subparsers.add_parser(
        "validate-datasets",
        help="Validate eval_queries.json and evals.json files",
    )
    validate_parser.set_defaults(func=cmd_validate_datasets)

    run_parser = subparsers.add_parser("run", help="Execute trigger and output eval cases")
    run_parser.add_argument(
        "--out",
        required=True,
        help="Output directory for per-case artifacts and benchmark.json",
    )
    run_parser.add_argument(
        "--judge",
        default="mock",
        choices=["mock", "description", "live"],
        help="Judge implementation (default: mock)",
    )
    run_parser.add_argument(
        "--skill",
        help="Run evals for a single skill name",
    )
    run_parser.add_argument(
        "--split",
        choices=sorted(SPLITS),
        help="Run only trigger queries tagged with this split",
    )
    run_parser.add_argument(
        "--output-only",
        action="store_true",
        help="Run output cases only, without repeating trigger runs",
    )
    run_parser.add_argument(
        "--gate",
        action="store_true",
        help="Exit non-zero when quality gates fail",
    )
    run_parser.add_argument(
        "--min-trigger-pass-rate",
        type=float,
        default=0.8,
        help="Minimum graded trigger pass rate when --gate is set (default: 0.8)",
    )
    run_parser.set_defaults(func=cmd_run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
