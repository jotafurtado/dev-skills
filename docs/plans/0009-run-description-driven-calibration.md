# 0009 - Run description-driven calibration

Status: Implemented
Depends on: [0008](./0008-add-pluggable-judges.md)
Unblocks: 0010
Source: [`0007-live-eval-and-trigger-calibration.md`](./0007-live-eval-and-trigger-calibration.md)

## Goal

Prove the three 2026-09-06 activation regressions against a judge that reads
`description`, three consecutive runs each, without losing validation
positives on Filament and Nova.

## Target seam

- Functional Filament API work without a composition decision loads
  `laravel-filament-v5`, not `laravel-filament-v5-ui-ux`.
- Visual-only Filament composition or review loads
  `laravel-filament-v5-ui-ux`.
- Confirmed Nova 4-to-Nova 4 work does not load `laravel-nova-5`; Nova 4→5
  migration does.

## Work

1. Run trigger evals with `--judge description` (three runs per query).
2. Score train first. If a regression fails, revise only `description`
   fields, generalizing from missed concepts.
3. Keep the validation winner.
4. Require validation positive pass_rate > 0.5 for the three skills.

## Completion

- Each regression is pass on all three runs.
- Validation positives for those three skills stay above 0.5.
- Chosen descriptions remain within 1–1024 characters.

## Out of scope

Live HTTP activator. Output-quality iteration (0010).
