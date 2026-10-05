# Live eval and trigger calibration

Status: Implemented (live artifacts recorded; semantic scores not certified)  
Recorded: 2026-09-08  
Closed: 2026-10-04  
Source: [`docs/research/skill-eval-mock-benchmark-2026-09-08.md`](../research/skill-eval-mock-benchmark-2026-09-08.md)  
Prior: [`docs/intents/skill-evaluation-hardening.md`](./skill-evaluation-hardening.md)

## Intent

Close the two acceptance criteria the hardening program could not meet with
`--judge mock`: live three-run trigger calibration, and a candidate-versus-baseline
output benchmark graded from real agent artifacts. Keep skill instruction
bodies unless a live trigger eval proves the `description` cannot carry the
boundary.

## Assessment at recording (2026-09-08)

The repository now has a shared harness, datasets for all six skills,
portable `compatibility`, orchestration behavior tests, and README commands.
A mock run wrote `maintenance/evals-out/benchmark.json`. That run does not
measure activation or output quality.

- Trigger selection is a keyword map in `MockJudge`.
- Output grading assumes with-skill passes and no-skill fails.
- `load_judge` accepts only `mock`.
- Trigger pass rates under that map: Filament core 1.00, SDD 0.90,
  prepare-commit 0.80, Nova 0.70, implement-with-subagents 0.60,
  Filament UI/UX 0.50.
- The three 2026-09-06 activation regressions are labeled in the datasets
  but have not been re-scored by a live activator.

## Problems to solve

### 1. The harness cannot talk to a real activator or grader

`python3 maintenance/eval_skills.py run --judge mock` is the only supported
path. There is no judge that:

- reads each skill `description` and decides trigger given a user query;
- runs an agent (or equivalent isolated prompt) with and without `SKILL.md`;
- records model id, duration, and token usage when the host provides them.

Until that exists, quality gates on `--gate` score the mock, not the skills.

### 2. Trigger calibration is unfinished

Phase 0004 updated Filament and Nova descriptions. The required loop is
still missing: three runs per query, train-only description edits,
validation winner, and three consecutive passes on:

- functional Filament API work without a composition decision →
  `laravel-filament-v5`, not `laravel-filament-v5-ui-ux`;
- visual-only Filament composition or review → `laravel-filament-v5-ui-ux`;
- confirmed Nova 4-to-Nova 4 work → do not load `laravel-nova-5`.

Mock keyword misses also show that UI/UX visual queries without
polish/layout keywords, Nova 4→5 migrations, and implement-with-subagents
frontier wording are not exercised by the mock map.

### 3. Output delta is not evidence

A 0.85 with-skill versus 0.00 baseline delta is produced by the mock
always failing `no_skill`. Assertions that contain “without” also fail
with-skill. Graders must quote consumer-visible output, not
`skill_name is not None`.

## Desired outcomes

- A pluggable live (or host-backed) judge registered beside `mock`.
- Trigger runs still execute three times per query and keep
  train/validation splits.
- Description changes for Filament, Nova, and any skill whose live
  trigger rate is below the majority rule, using train data only and
  keeping the validation winner.
- One recorded with-skill versus baseline output run per published skill,
  with `grading.json` quoting output evidence.
- Infrastructure failures still excluded from pass_rate.
- Mock judge remains the default for unit tests and offline CI.

## Non-goals

- Rewriting skill workflows without a failing live eval.
- Bundling `maintenance/evals-out/` into git or into installed payloads.
- Requiring identical scores across models or hosts.
- Replacing Filament composition/API verification commands.

## Acceptance criteria

- `eval_skills.py run --judge` accepts a non-mock judge that is skipped
  cleanly when credentials are missing (`missing_credentials`
  infrastructure, not a skill fail).
- The three activation regressions pass three consecutive live (or
  description-driven activator) runs each.
- Existing positive trigger cases for those three skills stay above 0.5
  on the validation split.
- Each skill has at least one persisted with-skill versus baseline output
  grading whose evidence quotes the agent output, not the mock heuristic.
- README still documents the mock command for CI; live command and
  required environment are documented next to it.

## References

- [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/best-practices)
- [Mock benchmark 2026-09-08](../research/skill-eval-mock-benchmark-2026-09-08.md)

## Residual

The paid live run and candidate-versus-baseline artifacts are now recorded in
[`release-closure-2026-10-04.md`](../research/release-closure-2026-10-04.md).
The three required regressions passed all live repetitions, and validation
positives remain above 0.5. Every published skill has a protocol-valid paired
output grade with literal source quotes.

This closes the missing-execution residual, not model fallibility. Five trigger
misses and disputed semantic output grades remain in the evidence. Raw output
scores are not certified quality metrics; the output quality gates are not all
green. No further paid iteration or score-driven skill rewrite was performed.
