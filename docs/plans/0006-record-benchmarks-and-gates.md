# 0006 — Record benchmarks and gates

Status: Implemented (live artifacts recorded 2026-10-04; semantic scores not certified)  
Depends on: [0004](./0004-calibrate-activation-boundaries.md), [0005](./0005-verify-orchestration-behavior.md)  
Source: [`0000-skill-evaluation-hardening.md`](./0000-skill-evaluation-hardening.md)

## Goal

Produce the first complete candidate-versus-baseline record and publish the
exact maintainer commands.

## Work

1. Run the harness from 0002 against every skill dataset from 0003, using the
   descriptions from 0004.
2. For each output case, keep with-skill and baseline artifacts, grading with
   quoted evidence, timing, and token counts.
3. Write aggregate `benchmark.json` per skill and one repository summary.
4. Treat infrastructure failures as skipped, not as skill fails. Re-run only
   the skipped cases if a rate limit or host outage interrupted the batch.
5. Update skill README maintenance sections and, where a human would look
   first, `README.md` so they name:
   - `node maintenance/validate_skill.mjs <skill_directory>`;
   - the evaluation command from 0002;
   - existing Filament composition/API commands that remain in force.
6. Confirm a clean evaluation run produces persisted per-case grading and the
   aggregate benchmark on disk.

## Completion

- Every skill has at least one recorded candidate-versus-baseline output
  benchmark.
- Grading files cite output evidence for pass and fail.
- Infrastructure failures are listed separately and omitted from pass-rate.
- README maintenance instructions name the exact validation and evaluation
  commands.
- All intent acceptance criteria are checked off against this run.

## Out of scope

Starting a second improvement loop. If the benchmark is weak, record the
gaps in the results; a later intent owns the next skill rewrite.

## Recorded evidence

Each of the six skills has a paired live output grade, a per-skill benchmark,
and a repository summary. Source responses, raw replies, protocol failures,
timing, and available token usage are preserved. The model's output quality
gates are not all green; this phase records the failures rather than starting
the improvement loop excluded above. See
[`release-closure-2026-10-04.md`](../research/release-closure-2026-10-04.md).

