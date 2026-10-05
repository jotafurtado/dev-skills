import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from maintenance.eval_judges import (
    DescriptionJudge,
    LiveJudge,
    extract_completion,
    http_infrastructure_kind,
    interpret_grade,
)
from maintenance.eval_skills import (
    CaseResult,
    InfrastructureError,
    MockJudge,
    OutputEval,
    SkillDatasets,
    TriggerQuery,
    aggregate_benchmark,
    evaluate_gates,
    run_output_case,
    run_trigger_case,
)


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "maintenance" / "eval_skills.py"


def run_harness(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(HARNESS), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )






class EvalSkillsRunTests(unittest.TestCase):
    def test_mock_run_writes_grading_and_benchmark(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "eval-run"
            result = run_harness(
                [
                    "run",
                    "--out",
                    str(out_dir),
                    "--judge",
                    "mock",
                    "--skill",
                    "laravel-filament-v5",
                ]
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            benchmark_path = out_dir / "benchmark.json"
            self.assertTrue(benchmark_path.is_file())
            benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
            self.assertIn("laravel-filament-v5", benchmark["skills"])

            trigger_grading = (
                out_dir / "laravel-filament-v5" / "trigger-000-run-1" / "grading.json"
            )
            output_grading = (
                out_dir / "laravel-filament-v5" / "output-001-with_skill" / "grading.json"
            )
            self.assertTrue(trigger_grading.is_file())
            self.assertTrue(output_grading.is_file())

            trigger_payload = json.loads(trigger_grading.read_text(encoding="utf-8"))
            output_payload = json.loads(output_grading.read_text(encoding="utf-8"))
            self.assertIn("passed", trigger_payload)
            self.assertIn("summary", output_payload)
            self.assertTrue(
                (out_dir / "laravel-filament-v5" / "trigger-000-run-1" / "timing.json").is_file()
            )
            self.assertTrue(
                (out_dir / "laravel-filament-v5" / "output-001-with_skill" / "outputs").is_dir()
            )

    def test_rate_limit_is_infrastructure_skip_not_skill_fail(self):
        judge = MockJudge()
        skill = SkillDatasets(
            name="laravel-filament-v5",
            skill_dir=ROOT / "skills" / "laravel-filament-v5",
            trigger_queries=[
                TriggerQuery(
                    index=0,
                    query=f"Build OrderResource {MockJudge.RATE_LIMIT_MARKER}",
                    should_trigger=True,
                )
            ],
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir)
            result = run_trigger_case(
                skill,
                skill.trigger_queries[0],
                0,
                judge,
                out_dir,
                ["laravel-filament-v5"],
            )

            self.assertEqual(result.infrastructure, "rate_limit")
            self.assertIsNone(result.passed)

            benchmark = aggregate_benchmark([result], "mock")
            trigger = benchmark["skills"]["laravel-filament-v5"]["trigger"]
            self.assertEqual(trigger["infrastructure_skipped"], 1)
            self.assertEqual(trigger["failed"], 0)
            self.assertEqual(trigger["pass_rate"], 0.0)
            self.assertEqual(len(benchmark["infrastructure_failures"]), 1)



class EvalSkillsJudgeTests(unittest.TestCase):

    def test_output_rate_limit_skips_graded_failure(self):
        judge = MockJudge()
        skill = SkillDatasets(
            name="laravel-filament-v5",
            skill_dir=ROOT / "skills" / "laravel-filament-v5",
            output_evals=[],
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_eval = OutputEval(
                id=99,
                prompt=f"Do work {MockJudge.RATE_LIMIT_MARKER}",
                expected_output="done",
                assertions=["The response is complete"],
            )
            result = run_output_case(skill, output_eval, "with_skill", judge, Path(tmp_dir))
            self.assertEqual(result.infrastructure, "rate_limit")
            self.assertIsNone(result.passed)



class DescriptionAndLiveJudgeTests(unittest.TestCase):

    def test_live_judge_missing_credentials_is_infrastructure(self):
        judge = LiveJudge(ROOT / "skills", env={})
        with self.assertRaises(InfrastructureError) as ctx:
            judge.select_skills("Build a Nova resource", ["laravel-nova-5"])
        self.assertEqual(ctx.exception.kind, "missing_credentials")

        skill = SkillDatasets(
            name="laravel-nova-5",
            skill_dir=ROOT / "skills" / "laravel-nova-5",
            trigger_queries=[TriggerQuery(0, "Build a Nova resource", True)],
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_trigger_case(
                skill,
                skill.trigger_queries[0],
                0,
                judge,
                Path(tmp_dir),
                ["laravel-nova-5"],
            )
            self.assertEqual(result.infrastructure, "missing_credentials")
            self.assertIsNone(result.passed)
            benchmark = aggregate_benchmark([result], "live")
            self.assertEqual(benchmark["skills"]["laravel-nova-5"]["trigger"]["failed"], 0)
            self.assertEqual(benchmark["infrastructure_failures"][0]["infrastructure"], "missing_credentials")

    def test_description_judge_hits_activation_regressions(self):
        judge = DescriptionJudge(ROOT / "skills")
        available = [
            "laravel-filament-v5",
            "laravel-filament-v5-ui-ux",
            "laravel-nova-5",
        ]
        cases = [
            (
                "Build a Filament 5 OrderResource with a status filter and bulk approve action.",
                {"laravel-filament-v5"},
                {"laravel-filament-v5-ui-ux"},
            ),
            (
                "Polish this Filament settings page while retaining our panel theme.",
                {"laravel-filament-v5-ui-ux"},
                {"laravel-filament-v5"},
            ),
            (
                "Migrate custom Nova tools between two confirmed Nova 4 projects.",
                set(),
                {"laravel-nova-5"},
            ),
        ]
        for query, required, forbidden in cases:
            for _ in range(3):
                selected = set(judge.select_skills(query, available))
                self.assertTrue(required <= selected, (query, selected))
                self.assertTrue(selected.isdisjoint(forbidden), (query, selected))

    def test_description_output_is_offline_not_agent_evidence(self):
        judge = DescriptionJudge(ROOT / "skills")
        skill = SkillDatasets(
            name="laravel-nova-5",
            skill_dir=ROOT / "skills" / "laravel-nova-5",
            output_evals=[],
        )
        output_eval = OutputEval(
            id=1,
            prompt="Migrate the attached Nova 4 Invoice resource to Nova 5.",
            expected_output="version-matched migration",
            assertions=["Confirm the installed Nova major before generating code."],
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_output_case(skill, output_eval, "with_skill", judge, Path(tmp_dir))
            grading = json.loads(result.grading_path.read_text(encoding="utf-8"))
            self.assertEqual(grading["evidence_mode"], "offline")
            self.assertIsNone(result.passed)
            benchmark = aggregate_benchmark([result], "description")
            bucket = benchmark["skills"]["laravel-nova-5"]["output"]["with_skill"]
            self.assertEqual(benchmark["evidence_mode"], "offline")
            self.assertEqual(bucket["failed"], 0)
            self.assertEqual(bucket["ungraded"], 1)
            self.assertEqual(bucket["pass_rate"], 0.0)


class LiveRequestAndProtocolTests(unittest.TestCase):



    def test_missing_fixture_is_protocol_error(self):
        judge = LiveJudge(ROOT / "skills", env={})
        with self.assertRaises(InfrastructureError) as ctx:
            judge.build_completion_request("hi", None, ["../etc/passwd"])
        self.assertEqual(ctx.exception.kind, "protocol")

    def test_malformed_selection_does_not_match_names_in_prose(self):
        judge = LiveJudge(ROOT / "skills", env={"OPENAI_API_KEY": "test"})
        judge._chat = lambda messages, **_kwargs: ("Please load laravel-nova-5 for this query.", 2)
        with self.assertRaises(InfrastructureError) as ctx:
            judge.select_skills("Build a Nova resource", ["laravel-nova-5"])
        self.assertEqual(ctx.exception.kind, "protocol")
        self.assertIn("laravel-nova-5", ctx.exception.raw or "")

        skill = SkillDatasets(
            name="laravel-nova-5",
            skill_dir=ROOT / "skills" / "laravel-nova-5",
            trigger_queries=[TriggerQuery(0, "Build a Nova resource", True)],
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_trigger_case(
                skill,
                skill.trigger_queries[0],
                0,
                judge,
                Path(tmp_dir),
                ["laravel-nova-5"],
            )
            grading = json.loads(result.grading_path.read_text(encoding="utf-8"))
            self.assertEqual(result.infrastructure, "protocol")
            self.assertIsNone(result.passed)
            self.assertEqual(grading["selected_skills"], [])
            self.assertIn("laravel-nova-5", grading["raw_reply"])
            timing = json.loads(result.timing_path.read_text(encoding="utf-8"))
            self.assertEqual(timing["total_tokens"], 2)
            self.assertEqual(timing["token_usage"], "available")
            benchmark = aggregate_benchmark([result], "live")
            self.assertEqual(benchmark["skills"]["laravel-nova-5"]["trigger"]["failed"], 0)
            self.assertEqual(benchmark["infrastructure_failures"][0]["infrastructure"], "protocol")

    def test_grade_indexes_cite_source_lines_and_keep_assertion_order(self):
        output = "First fact.\r\nSecond fact.\r\nThird fact."
        assertions = ["First condition.", "Second condition."]
        raw = json.dumps({"results": [
            {"assertion_id": 2, "passed": False, "evidence_start_line": 2, "evidence_end_line": 3},
            {"assertion_id": 1, "passed": True, "evidence_start_line": 1, "evidence_end_line": 1},
        ]})
        graded = interpret_grade(raw, assertions, output)
        self.assertEqual([item["text"] for item in graded["assertion_results"]], assertions)
        self.assertEqual(graded["assertion_results"][0]["evidence"], "First fact.\r\n")
        self.assertEqual(graded["assertion_results"][1]["evidence"], "Second fact.\r\nThird fact.")
        self.assertEqual(graded["summary"]["passed"], 1)
        self.assertEqual(graded["summary"]["failed"], 1)

    def test_bool_strings_and_bad_grades_are_protocol_errors(self):
        output = "The plan uses CodeEntry for the JSON payload."
        assertion = "Select CodeEntry."
        valid = {"assertion_id": 1, "passed": False, "evidence_start_line": 1, "evidence_end_line": 1}
        for passed in ("false", 1):
            with self.subTest(passed=passed), self.assertRaises(InfrastructureError) as ctx:
                interpret_grade(json.dumps({"results": [{**valid, "passed": passed}]}), [assertion], output)
            self.assertEqual(ctx.exception.kind, "protocol")
        for start, end in ((0, 1), (2, 1), (1, 2), (True, 1)):
            with self.subTest(start=start, end=end), self.assertRaises(InfrastructureError):
                interpret_grade(json.dumps({"results": [{**valid, "evidence_start_line": start,
                                                        "evidence_end_line": end}]}), [assertion], output)
        for assertion_id in (0, 2, True, 1.0):
            with self.subTest(assertion_id=assertion_id), self.assertRaises(InfrastructureError):
                interpret_grade(json.dumps({"results": [{**valid, "assertion_id": assertion_id}]}), [assertion], output)
        for raw in ("not json at all", '{"results": []}', json.dumps({"results": [valid, valid]})):
            with self.subTest(raw=raw), self.assertRaises(InfrastructureError):
                interpret_grade(raw, [assertion], output)
        with self.assertRaises(InfrastructureError):
            interpret_grade(json.dumps({"results": [valid]}), [assertion, "Another condition."], output)
        with self.assertRaises(InfrastructureError):
            interpret_grade(json.dumps({"results": [{"text": assertion, "passed": True,
                                                    "evidence": 'Invented claim plus "CodeEntry"'}]}), [assertion], output)
        accepted = interpret_grade(json.dumps({"results": [valid]}), [assertion], output)
        self.assertFalse(accepted["assertion_results"][0]["passed"])
        self.assertEqual(accepted["summary"]["failed"], 1)

        judge = LiveJudge(ROOT / "skills", env={"OPENAI_API_KEY": "test"})
        called = {"count": 0}
        def explode(messages, **_kwargs):
            called["count"] += 1
            return "unused", 1
        judge._chat = explode
        with self.assertRaises(InfrastructureError) as missing:
            judge.grade_output("prompt", [], None, [], output)
        self.assertEqual(missing.exception.kind, "protocol")
        self.assertEqual(called["count"], 0)

    def test_truncated_and_empty_completions_stay_ungraded(self):
        with self.assertRaises(InfrastructureError) as empty:
            extract_completion(
                {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"content": "", "reasoning": "hidden chain"},
                        }
                    ],
                    "usage": {"total_tokens": 3},
                }
            )
        self.assertEqual(empty.exception.kind, "protocol")
        self.assertFalse(empty.exception.preserve_output)
        self.assertIn("hidden chain", empty.exception.raw or "")

        with self.assertRaises(InfrastructureError) as truncated:
            extract_completion(
                {
                    "choices": [
                        {"finish_reason": "length", "message": {"content": "partial answer"}}
                    ],
                    "usage": {"total_tokens": 9},
                }
            )
        self.assertEqual(truncated.exception.finish_reason, "length")
        self.assertTrue(truncated.exception.preserve_output)
        self.assertEqual(truncated.exception.raw, "partial answer")
        self.assertEqual(truncated.exception.total_tokens, 9)

        with self.assertRaises(InfrastructureError) as reasoning_only:
            extract_completion(
                {
                    "choices": [
                        {
                            "finish_reason": "length",
                            "message": {"content": "", "reasoning": "hidden chain only"},
                        }
                    ],
                    "usage": {"total_tokens": 4},
                }
            )
        self.assertEqual(reasoning_only.exception.finish_reason, "length")
        self.assertFalse(reasoning_only.exception.preserve_output)
        self.assertIn("hidden chain only", reasoning_only.exception.raw or "")

        with self.assertRaises(InfrastructureError) as provider:
            extract_completion({"choices": []})
        self.assertEqual(provider.exception.kind, "provider")

        self.assertEqual(http_infrastructure_kind(500), "provider")
        self.assertEqual(http_infrastructure_kind(429), "rate_limit")
        self.assertEqual(http_infrastructure_kind(403), "missing_credentials")
        self.assertEqual(http_infrastructure_kind(504), "timeout")
        self.assertNotEqual(http_infrastructure_kind(500), "timeout")

    def test_grading_failure_preserves_generation_output(self):
        class GradeBreaks(MockJudge):
            def complete(self, prompt, skill_name, files):
                self.usage_tokens = 9
                return {
                    "text": "KEEP THIS OUTPUT",
                    "model": "mock",
                    "total_tokens": 9,
                    "evidence_mode": "simulated",
                }

            def grade_output(self, prompt, assertions, skill_name, files, output_text):
                self.usage_tokens = None
                raise InfrastructureError("protocol", "bad grade", raw="NOT-JSON")

        skill = SkillDatasets(name="demo", skill_dir=ROOT, output_evals=[])
        output_eval = OutputEval(id=7, prompt="do it", expected_output="", assertions=["Done"])
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_output_case(skill, output_eval, "with_skill", GradeBreaks(), Path(tmp_dir))
            response = (result.outputs_dir / "response.txt").read_text(encoding="utf-8")
            self.assertIn("KEEP THIS OUTPUT", response)
            self.assertEqual((result.outputs_dir / "raw_reply.txt").read_text(encoding="utf-8"), "NOT-JSON")
            grading = json.loads(result.grading_path.read_text(encoding="utf-8"))
            self.assertEqual(grading["raw_reply"], "NOT-JSON")
            self.assertEqual(grading["infrastructure"], "protocol")
            self.assertIsNone(grading["passed"])
            self.assertNotIn("summary", grading)
            timing = json.loads(result.timing_path.read_text(encoding="utf-8"))
            self.assertEqual(timing["total_tokens"], 9)
            self.assertEqual(timing["token_usage"], "partial")
            benchmark = aggregate_benchmark([result], "mock")
            self.assertEqual(benchmark["skills"]["demo"]["output"]["with_skill"]["failed"], 0)

    def test_mock_evidence_is_simulated_and_tokens_unavailable(self):
        judge = MockJudge()
        skill = SkillDatasets(name="demo", skill_dir=ROOT, output_evals=[])
        output_eval = OutputEval(id=1, prompt="commit this", expected_output="", assertions=["Ship it"])
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_output_case(skill, output_eval, "with_skill", judge, Path(tmp_dir))
            grading = json.loads(result.grading_path.read_text(encoding="utf-8"))
            timing = json.loads(result.timing_path.read_text(encoding="utf-8"))
            self.assertEqual(grading["evidence_mode"], "simulated")
            self.assertIsNone(timing["total_tokens"])
            self.assertEqual(timing["token_usage"], "unavailable")
            self.assertEqual(grading["execution"], "isolated_prompt")

    def test_output_only_skips_trigger_runs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "eval-run"
            result = run_harness(
                [
                    "run",
                    "--out",
                    str(out_dir),
                    "--judge",
                    "mock",
                    "--skill",
                    "prepare-commit",
                    "--output-only",
                ]
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(list((out_dir / "prepare-commit").glob("trigger-*")), [])
            self.assertTrue(
                (out_dir / "prepare-commit" / "output-001-with_skill" / "grading.json").is_file()
            )

    def test_quality_gates_skip_baseline_and_fail_all_skipped(self):
        skipped = CaseResult(
            skill="demo",
            case_id="trigger-000-run-1",
            variant=None,
            run_index=1,
            passed=None,
            infrastructure="missing_credentials",
            kind="trigger",
        )
        skipped_benchmark = aggregate_benchmark([skipped], "live")
        self.assertTrue(any("all skipped" in item for item in evaluate_gates(skipped_benchmark, 0.8)))

        compared = aggregate_benchmark(
            [
                CaseResult(
                    skill="demo",
                    case_id="output-001-with_skill",
                    variant="with_skill",
                    run_index=None,
                    passed=True,
                    kind="output",
                ),
                CaseResult(
                    skill="demo",
                    case_id="output-001-no_skill",
                    variant="no_skill",
                    run_index=None,
                    passed=False,
                    kind="output",
                ),
            ],
            "live",
        )
        self.assertEqual(evaluate_gates(compared, 0.8), [])

        failed_candidate = aggregate_benchmark(
            [
                CaseResult(
                    skill="demo",
                    case_id="output-001-with_skill",
                    variant="with_skill",
                    run_index=None,
                    passed=False,
                    kind="output",
                )
            ],
            "live",
        )
        self.assertTrue(any("with_skill" in item for item in evaluate_gates(failed_candidate, 0.8)))

        simulated_baseline = aggregate_benchmark(
            [
                CaseResult(
                    skill="demo",
                    case_id="output-001-no_skill",
                    variant="no_skill",
                    run_index=None,
                    passed=False,
                    kind="output",
                )
            ],
            "mock",
        )
        self.assertEqual(evaluate_gates(simulated_baseline, 0.8), [])



if __name__ == "__main__":
    unittest.main()
