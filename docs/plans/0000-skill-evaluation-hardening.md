# 0000 — Skill evaluation hardening

Status: Implemented  
Source: [`docs/intents/skill-evaluation-hardening.md`](../intents/skill-evaluation-hardening.md)  
Recorded: 2026-09-07

## Purpose

Execute the intent in independent, ordered phases. Each later file in this
directory is one phase. Finish a phase only when its acceptance criteria pass;
do not start the next phase until then.

This file is the index. It does not authorize implementation by itself.

## Sequence

```text
0001-align-skill-validator
        │
        ▼
0002-build-evaluation-harness
        │
        ▼
0003-author-eval-coverage
        │
        ├──────────────► 0004-calibrate-activation-boundaries
        │
        └──────────────► 0005-verify-orchestration-behavior
                              │
                              ▼
                    0006-record-benchmarks-and-gates
```

`0004` and `0005` may run in parallel after `0003`. `0006` waits for both.

## Phases

| ID | File | Outcome |
|---|---|---|
| 0001 | [align-skill-validator](./0001-align-skill-validator.md) | Local validator matches the Agent Skills specification; published skills use portable `compatibility` where they have runtime requirements. |
| 0002 | [build-evaluation-harness](./0002-build-evaluation-harness.md) | One repository command discovers evals, runs isolated trials, and persists grading without mixing infrastructure failures into skill scores. |
| 0003 | [author-eval-coverage](./0003-author-eval-coverage.md) | Every published skill has trigger queries, output cases, train/validation splits, and executable fixtures where the prompt requires project state. |
| 0004 | [calibrate-activation-boundaries](./0004-calibrate-activation-boundaries.md) | Filament visual/functional and Nova 4/5 regressions pass three consecutive runs without losing existing positive triggers. |
| 0005 | [verify-orchestration-behavior](./0005-verify-orchestration-behavior.md) | Orchestration tests prove frontier, failure isolation, dirty-tree integrate, review gate, and SHA-backed completion. |
| 0006 | [record-benchmarks-and-gates](./0006-record-benchmarks-and-gates.md) | Candidate-versus-baseline results exist on disk; README commands name the exact validation and evaluation entry points. |

## Shared constraints

Taken from the intent; do not reopen them in a phase:

- Keep skill workflows that already work. Change descriptions, validators,
  tests, evals, and fixtures first.
- Do not revalidate Filament, Nova, Kiro, Git, or host APIs inside the shared
  harness.
- Do not require identical scores across models or hosts.
- Do not ship large generated workspaces inside installed skill payloads.
- Evaluation does not publish, commit, or release skills.

## Program done when

Every acceptance criterion in the intent is met, and each phase file can be
marked complete with the evidence it names.
