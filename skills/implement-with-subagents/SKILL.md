---
name: implement-with-subagents
description: "Orchestrates parallel implementation of ready-for-agent tickets whose blockers are done, using isolated workers and orchestrator-owned review and commit. Use only when the user explicitly invokes /implement-with-subagents or asks to implement open tickets in parallel with subagents. Do not use for a single ticket (use /implement), triage, wayfinding, or editing Matt Pocock skills."
license: MIT
metadata:
  compatibility: "Requires Matt Pocock /implement, /tdd, and /code-review installed. Harness-agnostic contract; see references/host-adapters.md."
  author: jotafurtado
  version: "1.0.0"
  domain: workflow
  role: orchestrator
  scope: implementation
  tags: "implement, subagents, parallel, tickets, worktree, orchestration"
---

# Implement with subagents

Orchestrate **waves** of **workers** over the issue-tracker **frontier**. This skill extends the Matt Pocock [`/implement`](https://github.com/mattpocock/skills) contract with parallel subagents — it does not patch or vendor that skill.

Read glossary terms in [`CONTEXT.md`](CONTEXT.md). Architecture decision: [`docs/adr/0004-implement-with-subagents-orchestration.md`](../../docs/adr/0004-implement-with-subagents-orchestration.md).

## Provenance and dependencies

| Piece | Owner |
| --- | --- |
| TDD loop, typecheck/tests cadence, single-ticket shape | Installed `/implement` + `/tdd` |
| Two-axis review before commit | Installed `/code-review` |
| Frontier, waves, claim, isolate, integrate, failure policy | This skill |

If `/implement`, `/tdd`, or `/code-review` is missing, stop and tell the user to install Matt Pocock's skills (e.g. via `/setup-matt-pocock-skills`). Do not paste a private fork of those skills into the worker prompt.

## Preconditions

1. Working directory is a git repo on the branch that should receive integrated commits.
2. `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md` exist (run `/setup-matt-pocock-skills` if not).
3. Dependencies above are installed.
4. Optional argument: a feature slug or tracker filter. Without it, discover all `ready-for-agent` tickets the configured tracker exposes for this repo.

## Flow

### 1. Discover and compute the frontier

Follow the tracker in `docs/agents/issue-tracker.md`. Load every candidate that still carries `ready-for-agent`.

A ticket is on the **frontier** when:

- it has `ready-for-agent`, and
- every ticket listed in its blocking edges is complete (acceptance criteria done / issue closed — whatever the tracker uses for "done"; absence of `ready-for-agent` alone is not enough if acceptance boxes remain open after a failed claim).

If the frontier is empty, report why (none ready, or all ready tickets still blocked) and stop.

Detail: [references/ticket-lifecycle.md](references/ticket-lifecycle.md).

### 2. Human gate (first wave only)

List the frontier: title, id/path, blockers (none). Ask the user to confirm before spawning.

Later waves recompute the frontier and spawn without asking, unless the user asked to pause between waves.

### 3. Claim, then spawn the wave

For each frontier ticket, **claim**: remove `ready-for-agent` and append a short tracker comment that this skill claimed it. Then spawn one **worker** per ticket, in parallel, each in an isolated worktree/branch.

Worker prompt contract: [references/worker-contract.md](references/worker-contract.md).  
How to spawn/isolate on this host: [references/host-adapters.md](references/host-adapters.md).

### 4. Await workers; do not abort the wave on one failure

When a worker fails (red tests, crash, timeout, empty diff when work was required), restore `ready-for-agent`, comment the failure, leave or clean its worktree per the host adapter, and continue with the others. Dependents of a failed ticket stay blocked.

### 5. Post-worker phase — sequential per successful ticket

For each successful worker, in stable ticket order:

1. **Integrate** the worktree into the current branch (host adapter).
2. Run `/code-review` against the fixed point from before this ticket's integration.
3. **Review gate**: P0 or Spec-fail → do not commit; restore `ready-for-agent`; comment findings; leave the worktree for inspection; continue to the next ticket.
4. On clean review: **commit** on the current branch (follow project commit conventions / `/prepare-commit` if that is the repo habit); mark acceptance criteria done; comment completion; do **not** put `ready-for-agent` back.

Detail: [references/orchestrator-flow.md](references/orchestrator-flow.md).

### 6. Next wave or stop

Recompute the frontier. If non-empty, go to step 3 (no human gate). If empty, summarize: committed tickets, failed/re-queued, still blocked, leftover worktrees.

## Hard rules

- Workers never commit and never run `/code-review`.
- Only the orchestrator commits, and only after a passing review gate.
- Parallelism follows blocking edges only — do not invent file-overlap scheduling in v1.
- Use only the triage roles in `docs/agents/triage-labels.md` for ticket state. Claim and done clear `ready-for-agent`; failure restores it.
- Prefer Continue inside a wave; do not `/clear` between tickets of the same wave.
