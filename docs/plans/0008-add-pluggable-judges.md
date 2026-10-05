# 0008 - Add pluggable judges

Status: Implemented
Depends on: none
Unblocks: 0009, 0010
Source: [`0007-live-eval-and-trigger-calibration.md`](./0007-live-eval-and-trigger-calibration.md)

## Goal

Register two judges beside `mock` so the harness can score activation from
skill descriptions and call a live model when credentials exist.

## Work

1. Keep `Judge` as the protocol. Add `complete()` (or equivalent) so output
   cases persist the text that grading quotes.
2. Add `description`: load each available skill's `SKILL.md` `description`
   and decide trigger from those clauses (use-when vs do-not, including
   `unless`). Do not use the mock keyword map.
3. Add `live`: require `EVAL_SKILLS_API_KEY` or `OPENAI_API_KEY`. If absent,
   raise `InfrastructureError("missing_credentials")`. If present, POST to
   an OpenAI-compatible chat endpoint (`EVAL_SKILLS_BASE_URL`,
   `EVAL_SKILLS_MODEL`).
4. `--judge` choices: `mock`, `description`, `live`. Default remains `mock`.
5. Unit tests: live with empty env is infrastructure skip, not a skill fail;
   description judge is constructible without network.

## Completion

- `eval_skills.py run --judge live` with no key writes infrastructure skips
  and exit 0 (unless `--gate` demands graded cases).
- `eval_skills.py run --judge description` runs offline.
- Mock tests stay green.

## Out of scope

Description rewrites. Live paid evals in CI.
