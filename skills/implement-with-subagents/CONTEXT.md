# Implement with subagents

Orchestrating parallel implementation of agent-ready tickets whose blockers are done, without editing Matt Pocock's `/implement` skill.

## Language

**Frontier**:
The set of open tickets that currently carry `ready-for-agent` and whose declared blockers are all complete. Only frontier tickets may start in a wave.
_Avoid_: Backlog, queue, open issues (unfiltered)

**Wave**:
One parallel execution of the entire current frontier. When the wave finishes its post-worker phase, the frontier is recomputed for the next wave.
_Avoid_: Batch, sprint, job group

**Worker**:
A subagent that implements exactly one ticket in an isolated worktree by following the installed `/implement` contract except review and commit.
_Avoid_: Implementer, child agent, task agent (as synonyms for this role)

**Orchestrator**:
The session that discovers the frontier, claims tickets, spawns workers, integrates worktrees, runs `/code-review`, and commits.
_Avoid_: Parent agent, conductor, main agent (as the role name)

**Miolo**:
The `/implement` work a worker is allowed to do: TDD at agreed seams, typecheck, and the ticket's tests — explicitly excluding `/code-review` and commit.
_Avoid_: Full implement, partial implement, implement-without-commit (as the glossary term)

**Claim**:
Removing `ready-for-agent` from a frontier ticket (plus a tracker comment) so no other orchestrator grabs it before this wave finishes with it.
_Avoid_: Assign, lock, checkout

**Host adapter**:
The harness-specific way to realize the portable orchestration contract (spawn, isolate, await, integrate). OMP's `task` + isolated worktree is one adapter; others map the same verbs.
_Avoid_: Runtime plugin, backend
