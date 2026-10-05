# Skill Evaluation Hardening

Status: Implemented (residuals in live-eval-and-trigger-calibration)  
Recorded: 2026-09-06  
Closed: 2026-09-08

## Intent

Turn skill quality from a mostly structural claim into repeatable evidence. Keep the current skill behavior where it is already sound, correct the validation and activation gaps found in the 2026-09-06 evaluation, and establish a shared evaluation loop for every published skill.

## Current assessment

Overall maturity: **7.5/10**. The six published skills are structurally coherent and usable, but the repository does not yet prove that each skill improves agent output relative to a baseline.

### Evidence collected

- All six skill directories have a matching `name`, a non-empty `description` within the documented size limit, a `README.md`, a `SKILL.md` below 500 lines, and no broken local links.
- `node maintenance/validate_skill.mjs <skill>` reported all six published skills as valid.
- The repository test suite passed: 53 tests.
- Filament composition validation passed with 22 patterns and 76 variants, with no uncovered official patterns.
- Filament API verification passed against Filament 5.7.6: 64 classes and 13 enum cases.
- A 20-query cross-registry activation sample, run three times per query, passed 54 of 60 runs and 18 of 20 queries under the majority rule.
- Only two skills contain trigger-query datasets. Only `laravel-filament-v5` contains output-quality cases. No persisted grading, timing, or benchmark results were found.

### Skill maturity

| Skill | Assessment |
|---|---|
| `laravel-filament-v5` | Strongest evaluation assets and domain verification; activation overlaps with visual-only Filament work, and output cases have no executable fixtures or recorded benchmark. |
| `laravel-filament-v5-ui-ux` | Strong deterministic composition library and validation; activation is broad enough to load for functional Filament work, and no output-quality cases exist. |
| `prepare-commit` | Precise workflow and negative triggers; no trigger or output-quality suite exists. |
| `sdd-workflow` | Deep state, approval, invalidation, and resumption model; no evaluation suite exercises those transitions. |
| `laravel-nova-5` | Good version gate and progressive references; confirmed Nova 4 work still activates the Nova 5 skill, and no evaluation suite exists. |
| `implement-with-subagents` | Compact orchestration core with routed contracts; current tests largely pin source text instead of observable orchestration outcomes, and no evaluation suite exists. |

## Problems to solve

### 1. The local validator disagrees with the Agent Skills specification

[`maintenance/validate_skill.mjs`](../../maintenance/validate_skill.mjs) currently:

- accepts a `name` that does not match the parent directory;
- accepts empty `name` and `description` values;
- rejects the standard top-level `compatibility` field;
- treats the client-specific `disable-model-invocation` extension as part of the core schema without distinguishing portability from host support.

The validator can therefore return `Skill is valid!` for invalid skills and reject valid portable metadata.

### 2. Output quality is not measured

The repository contains definitions but no completed with-skill versus baseline runs. There are no persisted `grading.json`, `timing.json`, or `benchmark.json` results. A passing structural suite does not show that an agent follows the skill, produces a better result, or justifies its context cost.

The eight cases in [`laravel-filament-v5/evals/evals.json`](../../skills/laravel-filament-v5/evals/evals.json) have concrete assertions, but none supplies project fixtures. Cases that require a lockfile, policies, resources, or executable tests can currently pass through narrative compliance instead of real execution.

### 3. Activation boundaries overlap

Three reproducible boundaries need correction:

- `laravel-filament-v5-ui-ux` loaded in all three runs for a functional `OrderResource` request with a status filter and bulk action, although no composition decision was requested.
- `laravel-filament-v5` loaded in all observed valid runs for the visual-only query “Polish this Filament settings page while retaining our panel theme”, while its own trigger dataset marks that query as negative.
- `laravel-nova-5` loaded in all three runs for migration between two confirmed Nova 4 projects.

The intended seam is:

- Filament UI/UX selects or reviews composition, hierarchy, responsiveness, and presentation.
- Filament core owns installed-version APIs, implementation, security, migration, and tests.
- Nova 5 does not load for confirmed Nova 4-or-earlier work unless Nova 5 is the migration target.

### 4. Compatibility metadata is not portable

Several skills store operational requirements under `metadata.compatibility`. The Agent Skills specification defines `compatibility` as a top-level field. Host requirements that affect whether a skill can run should use the standard field after the local validator supports it.

This is most important for `implement-with-subagents`, which requires Git, tracker documentation, external Matt Pocock skills, and a host capable of isolated workers.

### 5. Some tests pin wording instead of behavior

[`tests/test_implement_with_subagents.py`](../../tests/test_implement_with_subagents.py) checks for literal phrases in Markdown. These checks can pass while frontier calculation, failure isolation, dirty-tree integration, review gating, or SHA-backed completion is behaviorally wrong.

## Desired outcomes

### Validator conformance

- Accept every field defined by the current Agent Skills specification.
- Reject empty required values.
- Reject a `name` that differs from the parent directory.
- Validate standard field types and length limits.
- Handle client extensions through an explicit compatibility policy instead of silently treating them as core fields.
- Keep deterministic fixtures for both valid and invalid skill directories.

### Evaluation harness

Provide one repository-level command that:

1. discovers published skills and their eval datasets;
2. runs each trigger query three times in isolated context;
3. supports train and validation partitions;
4. runs output cases with the candidate skill and a declared baseline;
5. records model, duration, token usage, outputs, assertion evidence, and failures;
6. aggregates per-skill and repository-level benchmark results;
7. distinguishes infrastructure failures such as rate limiting from skill failures;
8. exits non-zero only for defined quality gates, not for missing optional telemetry.

Persist outputs outside the installed skill payload unless a compact, stable fixture belongs to the skill itself.

### Evaluation coverage

Every published skill has:

- approximately 20 realistic trigger queries with positive cases, negative cases, and near misses;
- a documented train/validation split;
- two or three output-quality cases, including one meaningful boundary or failure case;
- executable fixtures whenever the prompt requires repository files or runtime behavior;
- assertions that inspect consumer-visible outcomes rather than source wording;
- at least one completed candidate-versus-baseline benchmark.

### Trigger calibration

Update descriptions so these regression cases pass in all three runs:

- functional Filament API work without a composition decision loads `laravel-filament-v5`, not `laravel-filament-v5-ui-ux`;
- visual-only Filament composition or review loads `laravel-filament-v5-ui-ux`, adding the core skill only when API, implementation, security, migration, or tests are required;
- confirmed Nova 4 work does not load `laravel-nova-5` unless the requested target is Nova 5;
- existing positive cases for all three skills continue to load correctly.

Select description changes using validation performance rather than the final training iteration.

### Behavioral orchestration checks

Replace wording assertions with controlled scenarios that prove:

- only unblocked `ready-for-agent` tickets enter a wave;
- one worker failure does not abort successful siblings;
- unsuccessful workers are not integrated;
- dirty-tree integration accounts for tracked and untracked non-junk paths;
- review failure prevents commit and restores eligibility;
- ticket completion is recorded only after a real commit SHA exists.

## Non-goals

- Rewriting otherwise sound skill workflows without evaluation evidence.
- Revalidating every Filament, Nova, Kiro, Git, or host API as part of the shared harness.
- Making benchmark results identical across models or hosts.
- Bundling large generated benchmark workspaces into installed skill payloads.
- Publishing, committing, or releasing skills as part of evaluation itself.

## Acceptance criteria

- The local validator passes specification-valid fixtures and rejects directory mismatch, empty required fields, invalid types, and over-limit values.
- All six current skills pass the corrected validator.
- Standard `compatibility` metadata is used where execution requirements exist.
- Every skill has trigger and output-quality eval definitions meeting the coverage above.
- Every output case that requires project state includes executable fixtures.
- A clean evaluation run produces persisted per-case grading and an aggregate benchmark.
- Infrastructure failures are reported separately and excluded from skill pass-rate calculations.
- The three activation regressions pass three consecutive runs each.
- Repository tests verify observable orchestration and validation behavior rather than required prose.
- README maintenance instructions name the exact validation and evaluation commands.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)
- [Previous repository skill audit](../research/skills-audit.md)

## Residual resolution

The later live run, validator type corrections, real fixture loading, protocol
handling, and controlled orchestration evidence are recorded in
[`release-closure-2026-10-04.md`](../research/release-closure-2026-10-04.md).
The mock benchmark remains historical, synthetic evidence. Live output grades
are model assessments of isolated prompts, not proof of executed consumer code.
