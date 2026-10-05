# Mock skill-eval benchmark (2026-09-08)

Recorded after `docs/plans/0000-skill-evaluation-hardening.md` shipped the
validator, harness, datasets, description seams, orchestration tests, and
README commands. This note is evidence for a later intent; it is not a
second rewrite of skill bodies.

Command:

```bash
python3 maintenance/eval_skills.py run --judge mock --out maintenance/evals-out
```

Judge: `mock` only (`maintenance/eval_skills.py` has no live-model judge).
Trigger selection is a hardcoded keyword map. Output grading treats
`with_skill` as passing most assertions and `no_skill` as failing them.
Token counts are null; durations are ~0 ms.

## Aggregate

| Metric | Value |
|---|---|
| with-skill output pass_rate mean | 0.847 |
| no-skill output pass_rate mean | 0.000 |
| delta (pass_rate) | 0.847 |
| infrastructure failures | none |

The delta is an artifact of the mock, not proof that an agent follows the
skill.

## Per-skill trigger (3 runs × each query)

| Skill | pass_rate | train | validation | Notes |
|---|---|---|---|---|
| laravel-filament-v5 | 1.00 | 1.00 | 1.00 | Keyword map covers the dataset. |
| sdd-workflow | 0.90 | 1.00 | 0.78 | False trigger on “plan this feature”; miss on “Kiro-inspired design-first”. |
| prepare-commit | 0.80 | 0.82 | 0.78 | False triggers on `git log`, Conventional Commits definition, cherry-pick, changelog-only. |
| laravel-nova-5 | 0.70 | 0.82 | 0.56 | Misses Nova 4→5 migrations; false triggers on Nova CSS polish, git commit, SDD, Laravel-only upgrade. |
| implement-with-subagents | 0.60 | 0.55 | 0.67 | Map keys on “subagent”/“workpool”; misses “ready-for-agent” / “frontier” / “worktree”. |
| laravel-filament-v5-ui-ux | 0.50 | 0.36 | 0.67 | Visual queries without “polish/layout/composition/responsive” go to core Filament. |

The three description regressions from the 2026-09-06 evaluation are
encoded in the datasets and pass under the mock map. They have **not**
been re-run against a live activator three times.

## Output grading (mock)

| Skill | with_skill | no_skill |
|---|---|---|
| laravel-filament-v5 | 6/8 (0.75) | 0/8 |
| laravel-filament-v5-ui-ux | 3/3 | 0/3 |
| laravel-nova-5 | 3/3 | 0/3 |
| sdd-workflow | 3/3 | 0/3 |
| prepare-commit | 2/3 | 0/3 |
| implement-with-subagents | 2/3 | 0/3 |

Failed with-skill mock cases are assertion-wording artifacts (the mock
fails assertions containing “without”), not agent transcripts.

## What this does not close

- Intent criterion: three activation regressions, three consecutive live runs.
- Intent criterion: candidate-versus-baseline with quoted output evidence from a real agent.
- Description calibration using train/validation on a judge that reads `description`, not a keyword table.
- Token usage and wall-clock cost of loading a skill.

## Follow-on

[`docs/intents/live-eval-and-trigger-calibration.md`](../intents/live-eval-and-trigger-calibration.md)
