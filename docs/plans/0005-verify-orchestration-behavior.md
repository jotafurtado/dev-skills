# 0005 — Verify orchestration behavior

Status: Implemented  
Depends on: [0003](./0003-author-eval-coverage.md)  
Unblocks: 0006  
Source: [`0000-skill-evaluation-hardening.md`](./0000-skill-evaluation-hardening.md)

## Goal

Replace wording assertions in the implement-with-subagents tests with
controlled scenarios that observe orchestration outcomes.

## Observable properties

1. Only unblocked `ready-for-agent` tickets enter a wave.
2. One worker failure does not abort successful siblings.
3. Unsuccessful workers are not integrated.
4. Dirty-tree integrate copies tracked and untracked non-junk paths and
   refuses a no-op merge of an uncommitted ticket branch.
5. Review failure prevents commit and restores `ready-for-agent`.
6. Ticket completion is recorded only after a real commit SHA exists on
   `git log`.

## Work

1. Extract the checkable procedures from
   `skills/implement-with-subagents/references/` into testable helpers or a
   narrow seam that tests can drive with a fake tracker and fake host adapter.
2. Replace `tests/test_implement_with_subagents.py` phrase checks with
   scenarios for the six properties above.
3. Keep payload constraints that are still structural (for example: the
   installed skill must not depend on source-repo ADR paths) as file-existence
   or path assertions, not as required prose.
4. If a helper would change runtime skill behavior, keep the helper in
   `maintenance/` or tests unless the skill already needs it at install time.

## Completion

- The six properties fail a planted counterexample and pass a correct run.
- Phrase-pinning tests for orchestration Markdown are gone.
- `python3 -m unittest tests.test_implement_with_subagents` is green.

## Out of scope

Live multi-host worker runs. Description calibration (0004). Full
candidate-versus-baseline agent eval of the skill (covered by 0003 datasets
and recorded in 0006).
