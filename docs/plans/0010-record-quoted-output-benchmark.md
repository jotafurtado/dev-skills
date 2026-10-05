# 0010 - Record quoted output benchmark

Status: Implemented
Depends on: [0009](./0009-run-description-driven-calibration.md)
Source: [`0007-live-eval-and-trigger-calibration.md`](./0007-live-eval-and-trigger-calibration.md)

## Goal

Persist at least one with-skill versus baseline output grading per skill
whose evidence quotes generated output, and document mock vs live commands.

## Work

1. Run `python3 maintenance/eval_skills.py run --judge live --out maintenance/evals-out/live-run` with maintainer credentials. `--judge description` is an offline activator and cannot produce agent-output evidence.
2. Confirm each skill has `output-*-with_skill` and `output-*-no_skill`
   `grading.json` files whose assertion evidence quotes `outputs/response.txt`.
3. Write a short research note for this run (not a second skill rewrite).
4. Update root README Maintenance: keep the mock CI command; add
   `--judge description` and `--judge live` plus required env vars.

## Completion

- Quoted evidence exists for every published skill.
- README names mock, description, and live entry points.
- Intent acceptance criteria can be checked against this run.

## Out of scope

Requiring a paid live model in CI. Starting another description loop.

## Recorded evidence

The 2026-10-04 paid run produced 46 responses. Regrading those same responses
with assertion IDs and output-line ranges produced 45 protocol-valid grades and
one baseline protocol skip, with at least one paired grade per published skill.
Quotes are copied verbatim from saved output; this does not certify the model's
semantic verdicts. The disputed grades and isolated-prompt limits are recorded
in [`release-closure-2026-10-04.md`](../research/release-closure-2026-10-04.md).

