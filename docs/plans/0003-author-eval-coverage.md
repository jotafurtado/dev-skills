# 0003 — Author eval coverage

Status: Implemented  
Depends on: [0002](./0002-build-evaluation-harness.md)  
Unblocks: 0004, 0005, 0006  
Source: [`0000-skill-evaluation-hardening.md`](./0000-skill-evaluation-hardening.md)

## Goal

Give every published skill the eval definitions the harness can run, including
fixtures whenever a prompt requires project state.

## Coverage bar

For each of:

- `laravel-filament-v5`
- `laravel-filament-v5-ui-ux`
- `laravel-nova-5`
- `prepare-commit`
- `sdd-workflow`
- `implement-with-subagents`

ship:

- about 20 realistic trigger queries: positives, negatives, and near misses;
- a documented train/validation split (~60/40);
- two or three output-quality cases, one of them a boundary or failure case;
- assertions on consumer-visible outcomes, not required source wording;
- executable fixtures when the prompt needs files, lockfiles, policies, a
  git tree, a tracker, or other runtime state.

## Work

1. Keep and extend existing Filament trigger files; do not drop known
   regressions from the intent:
   - functional `OrderResource` work must not load UI/UX alone as a visual
     task;
   - “Polish this Filament settings page…” must stay a visual-only query;
   - Nova 4-to-Nova 4 migration must remain a negative for `laravel-nova-5`.
2. Add `evals/eval_queries.json` to skills that lack it.
3. Add `evals/evals.json` to skills that lack output cases. For
   `laravel-filament-v5`, attach fixtures so the existing eight assertions can
   be graded from artifacts instead of narrative compliance. If eight cases
   remain too expensive to fixture in this phase, keep them, but ensure at
   least two or three have executable fixtures and are the ones 0006 runs
   first.
4. Put large or generated trees outside the install payload; reference them
   from the eval case `files` list.
5. Assertions inspect outputs, exit status, created files, commit messages,
   spec artifacts, or tracker comments — not whether `SKILL.md` still contains
   a phrase.

## Completion

- All six skills meet the coverage bar above.
- Every output case that requires project state names a fixture that exists.
- Train/validation splits are recorded next to each trigger dataset.
- The harness from 0002 can discover every new dataset without code changes
  beyond configuration.

## Out of scope

Rewriting skill descriptions (0004), replacing orchestration unit tests
(0005), and recording the first live benchmark (0006).
