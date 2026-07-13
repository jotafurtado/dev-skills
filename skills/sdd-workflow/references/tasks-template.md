# Executable Tasks Template

Use for `tasks.md`. Tasks are an executable dependency graph, not a prose
summary. Order them by dependencies and deployable progress; prefer vertical
slices when they reduce integration risk. Do not impose a domain/services/UI
layer order on stacks that do not use it.

## Task schema

Every executable task has a stable ID and this shape:

```markdown
- [ ] T001 [required] [Short outcome-oriented title]
  - **Depends on:** none
  - **Traceability:** AC-001, NFR-001, DEC-001
  - **Outcome:** [Concrete repository or behavior state after completion.]
  - **Files/areas:** [Expected paths or components; update if discovery changes.]
  - **Verify:** [Exact targeted tests, checks, or observable evidence.]
  - **Evidence:** pending
```

Allowed execution classes:

- `[required]` — included in “run all”.
- `[optional]` — excluded unless the user requests it.

Use `Depends on: none` or a comma-separated list of task IDs. Dependencies must
form an acyclic graph.

## Recommended structure

```markdown
# Tasks: [Spec title]

## Execution policy

- **Mode:** [single task | all required]
- **Parallelism:** Independent tasks may run together only when files, state,
  migrations, and external effects cannot conflict.
- **Completion:** A checkbox changes to `[x]` only after verification passes.
- **Convergence:** T900 is the single final convergence run.

## Tasks

- [ ] T001 [required] [First independently verifiable outcome]
  - **Depends on:** none
  - **Traceability:** AC-001, DEC-001
  - **Outcome:** [Expected result.]
  - **Files/areas:** [Paths.]
  - **Verify:** [Targeted command/assertion.]
  - **Evidence:** pending

- [ ] T002 [required] [Dependent outcome]
  - **Depends on:** T001
  - **Traceability:** AC-002, PROP-001
  - **Outcome:** [Expected result.]
  - **Files/areas:** [Paths.]
  - **Verify:** [PBT only if PROP-001 is suitable and tooling exists; otherwise
    the selected unit/integration check.]
  - **Evidence:** pending

- [ ] T003 [optional] [Useful but non-required enhancement]
  - **Depends on:** T002
  - **Traceability:** [ID or "none — optional enhancement"]
  - **Outcome:** [Expected result.]
  - **Files/areas:** [Paths.]
  - **Verify:** [Check.]
  - **Evidence:** pending

- [ ] T900 [required] Converge implementation with approved acceptance criteria
  - **Depends on:** [All required implementation task IDs]
  - **Traceability:** [All AC/NFR or BUG-AC IDs]
  - **Outcome:** Every approved criterion maps to implementation and evidence;
    broader relevant checks pass; remaining risks and optional work are reported.
  - **Files/areas:** [Spec artifacts, tests, and affected code.]
  - **Verify:** [Relevant suite, static analysis, build, or documented manual checks.]
  - **Evidence:** pending
```

## Execution updates

When a task starts, record it in `spec.yaml` as the active task. Do not change
the checkbox yet.

When verification succeeds:

```markdown
- [x] T001 [required] [Title]
  ...
  - **Evidence:** `path/to/test` passed; relevant assertion verifies AC-001.
```

Increment the `tasks` revision and update its hash after the checkbox/evidence
change.

When blocked, leave it unchecked and replace `pending` with concise blocker
evidence. Increment the `tasks` revision, update its hash, and do not mark
dependent tasks ready.

## Generation and validation rules

- Every material AC, NFR, or BUG-AC must be covered by at least one required
  task; every required task must trace to approved behavior or a necessary
  design decision.
- Include exactly one required final convergence task (`T900` by convention).
  It depends on every required implementation task and is not repeated by a
  separate post-task convergence pass.
- Include boundary, failure, authorization, compatibility, and regression tests
  according to risk.
- Correctness properties remain linked even when verified with unit or
  integration tests. PBT is optional, not a universal task requirement.
- Expected outcomes must be observable; avoid tasks such as “implement service”
  without a behavior, file state, or verification target.
- Validate that referenced IDs exist, task IDs are unique, dependencies exist,
  and the graph has no cycle.
- Parallelize only tasks in the same dependency wave that cannot conflict.
- Never include optional tasks in “run all” without explicit user direction.
