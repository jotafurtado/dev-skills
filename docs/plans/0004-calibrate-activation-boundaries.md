# 0004 — Calibrate activation boundaries

Status: Implemented (required live regressions verified 2026-10-04)  
Depends on: [0003](./0003-author-eval-coverage.md)  
Unblocks: 0006  
Source: [`0000-skill-evaluation-hardening.md`](./0000-skill-evaluation-hardening.md)

## Goal

Change skill `description` fields so the three reproduced activation failures
pass three consecutive runs, without losing existing positive triggers.

## Target seam

- `laravel-filament-v5-ui-ux` loads when the task selects or reviews
  composition, hierarchy, responsiveness, or presentation.
- `laravel-filament-v5` loads for installed-version APIs, implementation,
  security, migration, and tests. It does not own visual-only polish.
- `laravel-nova-5` does not load for confirmed Nova 4-or-earlier work unless
  Nova 5 is the requested migration target.

## Work

1. Treat trigger queries as a train/validation split. Revise descriptions
   using the train set only.
2. For each revision, run the trigger harness three times per query.
3. A query passes when trigger rate is greater than 0.5 for positives and
   less than 0.5 for negatives. The three intent regressions must pass all
   three runs, not just the majority rule.
4. Generalize from missed concepts. Do not paste failed-query keywords into
   the description.
5. After the train set is green, score the validation set. Keep the
   description with the best validation pass rate, even if an earlier
   iteration looked stronger on train.
6. Confirm remaining positive Filament and Nova queries still load the
   intended skill.

## Completion

- Functional Filament API work without a composition decision loads
  `laravel-filament-v5` and not `laravel-filament-v5-ui-ux`.
- Visual-only Filament composition or review loads
  `laravel-filament-v5-ui-ux`, adding the core skill only when API,
  implementation, security, migration, or tests are required.
- Confirmed Nova 4 work does not load `laravel-nova-5` unless the target is
  Nova 5.
- Each of those three cases passes three consecutive runs.
- Existing positive cases for the three skills continue to load.
- The chosen descriptions are the validation winners, not necessarily the
  last edit.

## Out of scope

Body-instruction rewrites unless a trigger eval proves the description cannot
carry the boundary. Output-quality iteration belongs in 0006.

## Recorded evidence

The required boundaries passed all three live repetitions; validation positives
for Filament core, UI/UX, and Nova stay above 0.5. Five other trigger misses are
retained rather than hidden. See
[`release-closure-2026-10-04.md`](../research/release-closure-2026-10-04.md).

