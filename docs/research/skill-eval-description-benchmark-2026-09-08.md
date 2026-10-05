# Description-driven skill-eval benchmark (2026-09-08)

Recorded after `docs/plans/0007-live-eval-and-trigger-calibration.md`.
Command:

```bash
python3 maintenance/eval_skills.py run --judge description --out maintenance/evals-out
```

Judge: `description` (`maintenance/eval_judges.py`). Trigger selection
reads each skill `SKILL.md` `description` (use-when vs do-not, including
`unless`). Output text is excerpted from the skill body (with-skill) or a
generic baseline (no-skill); grading quotes `outputs/response.txt`.

`--judge live` with empty credentials exits 0 and records
`missing_credentials` infrastructure skips.

## Activation regressions (3/3 runs)

| Query | Expected | Result |
|---|---|---|
| Filament 5 OrderResource with status filter and bulk approve | `laravel-filament-v5` yes, UI/UX no | pass |
| Polish Filament settings page retaining panel theme | UI/UX yes, core no | pass |
| Migrate custom Nova tools between two confirmed Nova 4 projects | `laravel-nova-5` no | pass |
| Migrate this Nova 4 Invoice resource to Nova 5 | `laravel-nova-5` yes | pass |

Validation positive pass_rate: Filament core 0.89, UI/UX 0.67, Nova 0.67
(all above 0.5).

## Per-skill trigger

| Skill | pass_rate | train | validation |
|---|---|---|---|
| sdd-workflow | 0.90 | 0.91 | 0.89 |
| laravel-filament-v5 | 0.76 | 0.67 | 0.89 |
| laravel-filament-v5-ui-ux | 0.75 | 0.82 | 0.67 |
| laravel-nova-5 | 0.75 | 0.82 | 0.67 |
| implement-with-subagents | 0.60 | 0.55 | 0.67 |
| prepare-commit | 0.45 | 0.45 | 0.44 |

`prepare-commit` remains below majority under this activator; a later
description loop can own it. This run did not call a paid model.

## Output grading

Every published skill has with-skill and no-skill `grading.json` files
whose assertion evidence starts with `output:` and quotes
`outputs/response.txt`. This is still a description-driven stand-in, not a
hosted agent transcript.
