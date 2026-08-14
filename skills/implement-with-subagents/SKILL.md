---
name: implement-with-subagents
description: "Orchestrates parallel implementation of ready-for-agent frontier tickets with isolated workers and orchestrator-owned review and commit. User-invoked via /implement-with-subagents."
license: MIT
metadata:
  compatibility: "Requires Matt Pocock /implement, /tdd, and /code-review installed. Harness-agnostic contract; see references/host-adapters.md."
  author: jotafurtado
  version: "1.2.0"
  domain: workflow
  role: orchestrator
  scope: implementation
  tags: "implement, subagents, parallel, tickets, worktree, orchestration"
disable-model-invocation: true
---

# Implement with subagents

Orchestrate **waves** of **workers** over the issue-tracker **frontier**. This skill extends the Matt Pocock [`/implement`](https://github.com/mattpocock/skills) contract with parallel subagents — it does not patch or vendor that skill.

Read glossary terms in [`CONTEXT.md`](CONTEXT.md). Decisions: [`docs/adr/0004-implement-with-subagents-orchestration.md`](../../docs/adr/0004-implement-with-subagents-orchestration.md), [`docs/adr/0005-allow-disable-model-invocation.md`](../../docs/adr/0005-allow-disable-model-invocation.md), [`docs/adr/0006-dirty-tree-integrate.md`](../../docs/adr/0006-dirty-tree-integrate.md).

## Provenance and dependencies

| Piece | Owner |
| --- | --- |
| TDD loop, typecheck/tests cadence, single-ticket shape | Installed `/implement` + `/tdd` |
| Two-axis review before commit | Installed `/code-review` (or degraded in-process fallback) |
| Frontier, waves, claim, isolate, dirty-tree integrate, failure policy | This skill |

If `/implement`, `/tdd`, or `/code-review` is missing, stop and tell the user to install Matt Pocock's skills (e.g. via `/setup-matt-pocock-skills`). Do not paste a private fork of those skills into the worker prompt.

## Preconditions

1. Working directory is a git repo on the branch that should receive integrated commits.
2. `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md` exist (run `/setup-matt-pocock-skills` if not).
3. Dependencies above are installed.
4. Optional argument: a feature slug or tracker filter. Without it, discover all `ready-for-agent` tickets the configured tracker exposes for this repo.
5. If this session is a **resume**, run the resume handshake in [references/orchestrator-flow.md](references/orchestrator-flow.md) before anything else.

## Flow

### 1. Discover and compute the frontier

Follow the tracker in `docs/agents/issue-tracker.md`. The **frontier** is every `ready-for-agent` ticket whose blockers are complete — scan checklist in [references/ticket-lifecycle.md](references/ticket-lifecycle.md); complete-blocker rule in [references/orchestrator-flow.md](references/orchestrator-flow.md).

If the frontier is empty, report why (none ready, or all ready tickets still blocked) and stop.

If `|frontier| == 1` and the rest is a linear blocked chain, warn that isolation will not buy parallelism — see unit-frontier warning in [references/orchestrator-flow.md](references/orchestrator-flow.md).

### 2. Human gate (first wave, and every resume mini-gate)

List the frontier: title, id/path, blockers (none), adapter name. Ask the user to confirm before spawning.

Later waves in the **same unbroken conversation** recompute the frontier and spawn without asking, unless the user asked to pause between waves. After resume/compaction, always mini-gate again.

### 3. Claim, then spawn the wave

For each frontier ticket, **claim**: remove `ready-for-agent` and append a short tracker comment that this skill claimed it (pure markdown — see ticket-lifecycle). Then spawn one **worker** per ticket, in parallel, each in an isolated worktree/branch.

Worker prompt contract: [references/worker-contract.md](references/worker-contract.md).  
How to spawn/isolate/integrate on this host: [references/host-adapters.md](references/host-adapters.md).

### 4. Await workers; do not abort the wave on one failure

When a worker fails (red tests, crash, timeout, empty diff when work was required), restore `ready-for-agent`, comment the failure, leave or clean its worktree per the host adapter, and continue with the others. Dependents of a failed ticket stay blocked.

Do **not** integrate until that worker reports `outcome: success`.

### 5. Post-worker phase — sequential per successful ticket

For each successful worker, in stable ticket order:

1. **Dirty-tree integrate** into the current branch ([host-adapters](references/host-adapters.md)) — trust `git status` in the worktree, not `filesTouched` alone; never no-op `git merge` of an uncommitted ticket branch.
2. Run the project tests on the orchestrator branch.
3. Run `/code-review` against the fixed point from before this ticket's integration (degraded in-process fallback if spawn fails — [orchestrator-flow](references/orchestrator-flow.md)).
4. **Review gate**: P0 or Spec-fail → do not commit; restore `ready-for-agent`; comment findings; leave the worktree for inspection; continue to the next ticket.
5. On clean (or degraded-but-passing) review: **commit** on the current branch; only then, after `git rev-parse HEAD` shows the new SHA, mark acceptance criteria done and comment completion; do **not** put `ready-for-agent` back.

Detail: [references/orchestrator-flow.md](references/orchestrator-flow.md).

### 6. Next wave or stop

Do not start the next wave until every intended commit from this wave has a SHA on `git log`. Recompute the frontier. If non-empty, go to step 3 (no human gate only inside an unbroken conversation). If empty, summarize: committed tickets, failed/re-queued, still blocked, leftover worktrees, review ok/degraded.

## Hard rules

- Workers never commit and never run `/code-review`.
- Only the orchestrator commits, and only after a passing review gate.
- SHAs in reports come from `git rev-parse` / `git log`, never from chat memory.
- Parallelism follows blocking edges only — do not invent file-overlap scheduling in v1.
- Use triage roles for claim/re-queue; map Wayfinder `resolved` only as documented in ticket-lifecycle.
- Prefer Continue inside a wave; do not `/clear` between tickets of the same wave.
