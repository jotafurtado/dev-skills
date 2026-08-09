<!--
Sync Impact Report
- Version change: (none, template) → 1.0.0
- Rationale: Initial ratification. The template was entirely unfilled placeholders;
  this is the first concrete constitution for this repository, so it is seeded as
  MAJOR version 1.0.0 rather than an incremental bump.
- Modified principles: none (initial set)
- Added sections:
  - Core Principles I–VI (Evidence-Grounded Accuracy, English-Authored Skills /
    Localized Human Language, Deep Modules & Progressive Disclosure, Verified
    Before Shipped, Earned Absolutes, Licensing Integrity)
  - Repository Conventions (issue tracking, triage labels, domain docs)
  - Skill Lifecycle & Verification (adding a skill, pre-ship checks, delegation
    contracts between skills)
  - Governance (amendment procedure, versioning policy, compliance review)
- Removed sections: none
- Templates requiring follow-up: none — plan/spec/tasks templates in
  .specify/templates/ contain no hard-coded principle references that
  contradict this version.
- Deferred placeholders: none. RATIFICATION_DATE is set to the date of this
  initial ratification since no earlier adoption date exists for this repo.
- Deferred non-governance intent: none from this invocation.
-->

# Dev Skills Constitution

Dev Skills is a personal collection of [Agent Skills](https://skills.sh) —
`SKILL.md`-format packages that encode the author's own agentic-coding
dev flow for specific, recurring jobs (framework-version-matched
implementation, UI/UX pattern selection, commit hygiene, spec-driven
workflows, and similar tasks) — distributed by installing directly from
this repository.

## Core Principles

### I. Evidence-Grounded Accuracy (NON-NEGOTIABLE)

Every API signature, configuration option, CLI flag, or version-specific
behavior documented in a skill MUST be grounded in official documentation
or installed source — never reconstructed from training-data memory. A
skill MUST have its consuming agent resolve the installed version from the
project's manifest or lockfile before citing a signature, rather than
pinning versions in the skill's own text. When evidence conflicts between
installed source and general framework documentation, the installed
version-matched source takes precedence, and the conflict MUST be
disclosed rather than silently resolved. If a signature cannot be
confirmed, the skill MUST say so instead of guessing.

Rationale: these skills exist specifically to prevent hallucinated APIs in
domains — Filament, Nova, and similar fast-moving frameworks — where a
wrong signature compiles or parses but fails at runtime. Trust in the
whole collection depends on this discipline holding without exception.

### II. English-Authored Skills, Localized Human Language

All skill content — `SKILL.md`, `references/`, and other agent-facing
files — MUST be written in English, regardless of the author's working
language elsewhere. A skill MAY still produce output in another language
when that is its documented, deliberate behavior (for example,
`prepare-commit` writing pt-BR commit messages). This is a project-level
exception to any personal or global language convention that would
otherwise apply to code versus documentation.

Rationale: skills here are published for reuse across multiple agent
tools and, where shared, a wider audience; English content maximizes
reach and reviewability, while an explicit exception list keeps
intentional localized behavior from being "corrected" by mistake.

### III. Deep Modules, Progressive Disclosure

Each skill MUST ship exactly two entry points: `SKILL.md` (loaded by the
agent, holding the decision flow, gates, and routing) and `README.md`
(for humans browsing the repository or skills.sh). `references/` MUST
stay one level deep and MUST be loaded only on demand — `SKILL.md` routes
to a reference file only when the task needs it, and reference-level
detail MUST NOT be inlined into `SKILL.md`. The YAML frontmatter
`description` MUST be specific enough to trigger correctly with few false
positives, stating both when to use and when not to use the skill.

Rationale: an agent pays a context cost for every loaded file; a shallow,
routed structure keeps the always-loaded core small while still letting
deep, detailed guidance exist and stay reachable when the task needs it.

### IV. Verified Before Shipped

A skill's tooling, decision flows, or gates described as "mandatory" or
"required" MUST be exercised by at least one recorded execution before
being trusted — prose review alone is not sufficient evidence that a step
is actually followed. Deterministic helpers (query scripts, validators)
MUST fail closed on invalid or unrecognized input rather than silently
substituting an unrelated result. Any eval or forward-run recorded as
supporting evidence MUST have its assertions scored against the real
transcript before being counted as a pass; an exit code alone is not a
verdict.

Rationale: direct testing of this repository's own skills has already
found cases where a step documented as mandatory was never invoked by a
real agent run, and where a query tool failed open on bad input instead
of erroring — both produce false confidence that is worse than no
tooling at all.

### V. Earned Absolutes

Skill guidance MUST reserve unconditional language ("Never", "Always",
hard-fail gates) for genuine, source-backed constraints — security
boundaries, breaking API removals, or license terms. Where the underlying
framework or tool admits more than one valid solution, guidance MUST be
expressed as a conditional recommendation (prefer/avoid with stated
conditions) instead of an absolute rule.

Rationale: false absolutes erode trust in the true ones and push agents
toward brittle, one-size-fits-all output in domains that legitimately
support multiple valid designs.

### VI. Licensing Integrity

Skill content MUST be built only from officially-licensed sources —
official documentation, source code under a compatible license, or the
author's original analysis. Text or structure MUST NOT be copied from a
project that has no license or an incompatible one; such a project may
inform architecture or approach but never verbatim content. The
repository and every skill in it remain MIT-licensed.

Rationale: this repository is installed directly into other people's
projects; a licensing mistake here propagates downstream silently and is
hard to unwind after the fact.

## Repository Conventions

Issues and PRDs for this repository live as GitHub issues, operated
through the `gh` CLI (see `docs/agents/issue-tracker.md` for the exact
commands). Pull requests are not used as a triage surface unless that is
explicitly reconfigured in that doc. Triage uses exactly five canonical
labels, applied without aliases: `needs-triage`, `needs-info`,
`ready-for-agent`, `ready-for-human`, `wontfix` (see
`docs/agents/triage-labels.md`).

This is a single-context repository. `CONTEXT.md` at the root is the
project glossary; architectural decisions live under `docs/adr/`. Work
MUST use terminology already defined in `CONTEXT.md` and MUST NOT
introduce a synonym the glossary explicitly rejects. If a proposal
contradicts an existing ADR, that conflict MUST be surfaced explicitly
rather than silently overridden.

## Skill Lifecycle & Verification

Adding a skill: create `skills/<skill-name>/SKILL.md` with required
frontmatter (`name`, `description`), add a companion
`skills/<skill-name>/README.md`, and add a row to the table in the root
`README.md`.

Before a skill change ships — any material edit to a `SKILL.md`, a
`references/` file, or a script — the author MUST run that skill's
existing automated tests and validators, and, where an eval suite exists,
MUST review its assertions against a real transcript rather than trusting
a green exit code alone (Principle IV).

Skills that delegate authority to one another (for example,
version-sensitive implementation versus visual pattern composition) MUST
keep that delegation contract mutual and explicit in both skills'
`SKILL.md` files: the delegating skill states what it hands off, and the
receiving skill states what it owns plus its fallback behavior when the
other skill is unavailable.

## Governance

This constitution governs how skills in this repository are authored,
structured, and verified, and takes precedence over any conflicting
guidance recorded elsewhere in the repository (including `AGENTS.md` and
files under `docs/agents/`). Where such a file conflicts with this
constitution, the conflict MUST be reconciled in the same change that
introduces or reveals it — either by updating the file or by amending
this constitution.

Amendments are proposed through the `/speckit-constitution` workflow or
an equivalent direct edit followed by a Sync Impact Report. The version
MUST be bumped according to semantic versioning: MAJOR for a backward
incompatible principle removal or redefinition, MINOR for a new principle
or materially expanded guidance, PATCH for wording clarifications or
typo fixes with no semantic change.

Before merging a new or materially changed skill, verify it against the
Core Principles above (evidence grounding, language, structure,
verification, earned absolutes, licensing). Any deliberate exception to a
principle MUST be justified in the PR or commit description rather than
left unexplained.

**Version**: 1.0.0 | **Ratified**: 2026-08-03 | **Last Amended**: 2026-08-03
