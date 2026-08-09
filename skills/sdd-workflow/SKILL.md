---
name: sdd-workflow
description: "Runs a Kiro-inspired Spec-Driven Development workflow with Requirements-First, Design-First, Quick Plan, and Bugfix modes before implementation. Creates numbered, versioned artifacts under sdd-specs/ and executes approved tasks with traceability and verification. Use only when the user explicitly asks for SDD, a Kiro-style spec, spec-driven development, avoiding vibe coding, writing a spec, or planning before implementation. Do not auto-apply to ordinary feature, refactor, or bug requests that do not ask for a spec workflow."
license: MIT
metadata:
  compatibility: "Designed for Claude Code, Cursor, Windsurf, and Copilot."
  tags: "spec-driven-development, sdd, kiro, planning, requirements, design, bugfix, workflow"
  author: jotafurtado
  version: "2.0.0"
  domain: workflow
  role: specialist
  scope: planning-and-implementation
  output-format: markdown+code
---

# SDD Workflow — Kiro-Inspired Spec-Driven Development

## Purpose and official basis

Turn an explicitly requested spec workflow into durable artifacts, then execute
only from the resulting task plan. The semantic model follows the official Kiro
documentation:

- [Specs](https://kiro.dev/docs/specs/)
- [Feature Specs](https://kiro.dev/docs/specs/feature-specs/)
- [Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs/)
- [Quick Plan](https://kiro.dev/docs/specs/quick-plan/)
- [Analyze Requirements](https://kiro.dev/docs/specs/analyze-requirements/)
- [Correctness](https://kiro.dev/docs/specs/correctness/)

This is a portable Agent Skill, not an implementation of Kiro's UI. Kiro-specific
features such as `.kiro/specs/`, `#spec`, Sync Files, and UI approval state are
adapted to files under `sdd-specs/`.

## Host precedence and invocation

Current user instructions and the host agent's modes, permissions, safety rules,
and approval requirements always take precedence. This skill does not authorize
source edits, commands, commits, pushes, or destructive operations.

Apply automatically only when the request explicitly mentions SDD, Kiro specs,
spec-driven development, avoiding vibe coding, writing a spec, or planning
before implementation. Otherwise, do not impose this workflow on an ordinary
feature, refactor, or bug request.

Manual invocation with `/sdd-workflow` is always explicit opt-in.

Use the user's language for artifacts and approval prompts unless the project
documents another language.

## Spec location and mandatory numbering

Every spec lives in:

```text
sdd-specs/{sequence}-{slug}/
```

Example:

```text
sdd-specs/001-user-authentication/
├── spec.yaml
├── requirements.md   # Feature modes and Quick Plan; absent for Bugfix
├── bugfix.md          # Bugfix only; absent for Feature and Quick Plan
├── design.md
└── tasks.md
```

Before creating a new spec:

1. Create the `sdd-specs/` root if it does not exist, then inspect only its
   immediate child directories whose names match
   `^[0-9]+-`.
2. Parse each numeric prefix as base 10. The next sequence is the maximum plus
   one, or `1` if no matching directory exists.
3. Format with at least three digits: `001` through `999`; `1000` remains
   `1000`.
4. Create a kebab-case slug and combine it with the sequence, for example
   `007-payment-reconciliation`.
5. Re-scan immediately before creating the directory. If the identifier now
   exists, calculate again.

Never reuse, rename, or close a numbering gap. Ignore non-matching directories.
Persist the immutable `sequence`, `slug`, and full `spec_id` in `spec.yaml`.

Before allocating a new number, check whether the user intends to resume an
existing spec. Resume by full `spec_id`; if only a slug is supplied and more
than one spec matches, ask which one. If a same-purpose spec exists, ask whether
to resume it or create a new numbered spec.

Immediately after creating the directory, instantiate `spec.yaml` from
`references/spec-state-template.yaml` before writing another artifact. Fill the
immutable identifiers, type, mode, ISO 8601 timestamps, initial phase, and this
mode-specific graph:

- `requirements-first`: requirements → design → tasks; initial phase
  `requirements`.
- `design-first-hld` or `design-first-lld`: design → requirements → tasks;
  initial phase `design`.
- `quick-plan`: requirements → design → tasks; initial phase `requirements`;
  requirements/design approval is not required.
- `bugfix`: bugfix → design → tasks; initial phase `bugfix`; requirements is not
  applicable.

Do not leave the Requirements-First defaults in place for another mode.

## Select one workflow mode

If the user has not made the mode clear, ask one focused question. Persist the
selected mode. If the user later changes it, reconcile artifact dependencies and
approvals; create a new spec only when the goal itself is a separate body of
work.

### Feature — Requirements-First

Use when desired behavior is known but architecture remains open:

1. `requirements.md` — generate, review, and obtain explicit approval.
2. `design.md` — generate from approved requirements, review, and obtain
   explicit approval.
3. `tasks.md` — generate executable tasks and wait for an explicit command to
   run one task or all required tasks, unless implementation was already
   authorized in the current request.

### Feature — Design-First

Use when architecture, stack, constraints, or algorithms are the starting point:

1. Ask whether the design level is HLD or LLD.
2. `design.md` — generate, review, and obtain explicit approval.
3. `requirements.md` — derive feasible requirements from the approved design,
   review, and obtain explicit approval.
4. `tasks.md` — generate executable tasks, then follow the same execution
   authorization rule as Requirements-First.

### Quick Plan

Use only for well-understood, low-ambiguity work:

1. Ask all blocking clarification questions up front.
2. Generate `requirements.md`, `design.md`, and `tasks.md` continuously without
   intermediate approval gates.
3. Present the complete plan. Do not edit source code unless the current request
   already authorizes implementation; otherwise wait for a run command.

For complex, regulated, security-sensitive, or highly ambiguous work, recommend
a gated Feature mode instead. Offer an optional requirements analysis before
design when it can expose ambiguity, conflicts, assumptions, or missing cases.

### Bugfix Spec

Use for a defect requiring structured diagnosis:

1. `bugfix.md` — capture reproduction, current behavior, expected behavior,
   behavior that must remain unchanged, evidence, and root-cause status; obtain
   explicit approval.
2. Before and during `design.md`, inspect the affected code paths and reproduce
   or trace the defect where possible. Confirm or refine the root cause, then
   define the smallest safe correction and regression strategy; obtain explicit
   approval.
3. `tasks.md` — generate fix and regression tasks, then wait for execution
   authorization unless it was already granted.

Do not force a bug into the feature `requirements.md` template.

## Persistent state, approval, and resumption

Read `references/spec-state-template.yaml` before creating or resuming a spec.
`spec.yaml` is a portable extension of this skill; it stores workflow state that
Kiro normally manages in its product UI.

For each applicable artifact, persist:

- path, revision, status, and dependencies;
- whether approval is required;
- approver and approval timestamp;
- deterministic whole-file content hash when it becomes approved, generated, or
  ready for the next phase.

Prefer `git hash-object <path>` in a Git repository. Record the hash algorithm.
If no deterministic hash tool is available, set the hash to `null` and require
explicit reapproval when external edits cannot be ruled out.

Increment an artifact's revision for every accepted content change. Update its
hash after each agent-controlled change, including task checkbox/evidence
updates, so later resumption can distinguish known progress from external edits.

Use these transitions consistently:

1. On first creation, set the artifact revision to `1` and status to `draft`.
   Missing artifacts remain revision `0`.
2. When a gated artifact is ready for review, set its status and the spec status
   to `awaiting-approval`.
3. On explicit approval, set artifact status to `approved`, approval status to
   `approved`, `approved_by` to `user`, `approved_at` to the current timestamp,
   and store its hash. Advance `current_phase` to the next artifact and set the
   spec status to `draft`.
4. In Quick Plan, store hashes and mark requirements/design as `generated`.
   After any mode generates tasks, mark tasks `ready`, store its hash, set
   `current_phase: tasks`, and set spec status to `ready`.
5. Update `updated_at` on every transition. Set `created_at` only once.

Before any phase or execution:

1. Read `spec.yaml` and every existing artifact.
2. Recompute every non-null artifact hash.
3. If content differs from persisted state, mark it `draft`; clear approval when
   required and reconcile the change before proceeding.
4. Apply downstream invalidation rules.
5. Inspect `tasks.md` and relevant code/tests. Never mark an existing task
   complete without concrete evidence.
6. Resume at the first applicable artifact that is missing, draft, stale, or
   awaiting approval. If upstream artifacts are `approved` or `generated` and
   tasks is `ready`, offer execution. If tasks is `in-progress` or the spec is
   `blocked`, reconcile recorded evidence and resume the eligible task.

Artifact existence is not approval. Never overwrite an approved artifact
silently.

## Invalidation and synchronization

Use a living-spec model during active work and follow the selected mode's
dependency direction:

- Requirements-First and Quick Plan:
  `requirements.md → design.md → tasks.md`.
- Design-First: `design.md → requirements.md → tasks.md`. A requirements change
  invalidates tasks; it invalidates design too only when it contradicts or
  materially expands the approved design.
- Bugfix: `bugfix.md → design.md → tasks.md`.
- Changing any artifact invalidates all of its descendants in that graph.
- Changing `tasks.md` requires reconciliation with execution progress but does
  not invalidate upstream artifacts.
- A material implementation discovery updates the appropriate upstream
  artifact, clears its approval, invalidates descendants, and stops execution
  until the required gate is passed again.

Persist invalidation rather than merely reporting it. Mark each descendant
artifact `stale`, reset any required approval to `pending`, and clear its
approver/timestamp. Preserve its file, revision, and previous hash until
reconciliation. When reconciled content is accepted, increment its revision,
store the new hash, and pass its gate again when required.

Material changes include behavior, public contracts, data models, security or
privacy assumptions, external dependencies, architecture, or acceptance
criteria. Minor in-scope implementation details may proceed when they do not
change approved behavior or design; record them as task evidence or a design
note.

Never regenerate stale files by erasing human edits. Reconcile deliberately and
summarize what changed.

## Task execution

Read `references/tasks-template.md` before generating or running tasks.

The user may request one task by ID or all required incomplete tasks. Before
running a task, confirm:

- upstream artifacts are approved or valid for Quick Plan;
- the task is incomplete and all dependencies are complete;
- the task is authorized by the current user request;
- no host safety rule or unrelated work blocks it.

When execution is authorized, persist `execution.authorization: granted`,
`authorized_at`, `current_phase: execution`, tasks status `in-progress`, and
spec status `in-progress`.
Authorization remains subject to the current host and user instructions; set it
to `revoked` if the user withdraws permission.

For each task:

1. Add its ID to `execution.active_tasks`.
2. Implement only its approved scope.
3. Run the narrowest relevant tests, linters, static analysis, or manual checks
   that the host and project support.
4. Compare the result with the task outcome and linked acceptance criteria.
5. Record concise evidence in `tasks.md`.
6. Mark `- [x]` only after verification passes, remove it from `active_tasks`,
   increment the tasks revision, update its hash, and update `updated_at`. On
   failure, leave it incomplete, record the blocker, increment the tasks
   revision, clear it from `active_tasks`, update its hash, set spec status to
   `blocked`, and stop or retry within the authorized scope.

For “run all”, build dependency waves from required incomplete tasks. Execute
independent tasks in parallel only when the host supports it and their files,
state, migrations, or external effects cannot conflict. Run waves sequentially.
Optional tasks are never included unless explicitly requested.

Generate exactly one required final convergence task, conventionally `T900`,
which depends on all required implementation tasks. It is the sole convergence
run and appears as the last dependency wave in “run all”. When it starts, set
`current_phase: convergence`. That task must:

1. Map every acceptance criterion or bugfix expected/unchanged behavior to
   implementation and verification evidence.
2. Run broader relevant checks.
3. Reconcile code and artifacts without hiding deviations.
4. On success, mark T900 checked, tasks status `complete`,
   `current_phase: complete`, and spec status `complete`. On failure, leave T900
   unchecked and set spec status `blocked`.
5. Store `last_convergence_at`, set `last_convergence_result` to `passed` or
   `failed`, clear active tasks, increment the tasks revision, update its hash,
   and report completed work, evidence, optional tasks left, and remaining
   risks.

## Reference routing

Load only what the current phase needs:

- `requirements.md` → `references/requirements-template.md`
- `bugfix.md` → `references/bugfix-template.md`
- `design.md` → `references/design-template.md`
- `tasks.md` → `references/tasks-template.md`
- `spec.yaml`, resume, approval, invalidation → `references/spec-state-template.yaml`

The templates define this skill's portable file schema. Do not present their
exact headings, IDs, metadata, or directory path as requirements of Kiro itself.
