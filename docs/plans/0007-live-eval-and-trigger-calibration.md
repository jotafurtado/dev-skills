# 0007 - Live eval and trigger calibration

Status: Implemented
Source: [`docs/intents/live-eval-and-trigger-calibration.md`](../intents/live-eval-and-trigger-calibration.md)
Recorded: 2026-09-08

## Purpose

Close the residuals left by `--judge mock`: a judge that reads skill
`description` fields, a live judge that skips on missing credentials, three
consecutive description-driven passes on the Filament and Nova activation
regressions, and output grading that quotes generated text.

This file is the index. Later files in this sequence are the phases.

## Sequence

```text
0008-add-pluggable-judges
        │
        ▼
0009-run-description-driven-calibration
        │
        ▼
0010-record-quoted-output-benchmark
```

## Phases

| ID | File | Outcome |
|---|---|---|
| 0008 | [add-pluggable-judges](./0008-add-pluggable-judges.md) | `--judge` accepts `description` and `live`; missing live credentials are `missing_credentials`. |
| 0009 | [run-description-driven-calibration](./0009-run-description-driven-calibration.md) | The three activation regressions pass three consecutive description-driven runs; validation positives stay above 0.5. |
| 0010 | [record-quoted-output-benchmark](./0010-record-quoted-output-benchmark.md) | Persisted with-skill vs baseline grading quotes output; README names mock and live commands. |

## Shared constraints

- Keep `mock` as the default for unit tests and offline CI.
- Do not rewrite skill bodies unless a description-driven trigger eval
  proves the `description` cannot carry the boundary.
- Do not bundle `maintenance/evals-out/` into git.
- Infrastructure failures stay out of pass_rate.

## Program done when

Every acceptance criterion in the live-eval intent is met, and each phase
file can be marked complete with the evidence it names.

## Later live evidence

The remaining paid-execution gap was closed on 2026-10-04. Required activation
boundaries passed, and all six skills have paired output artifacts. Semantic
grades remain fallible and are not a quality certificate. See
[`release-closure-2026-10-04.md`](../research/release-closure-2026-10-04.md).

