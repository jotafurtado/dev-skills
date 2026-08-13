# Host adapters

Portable verbs this skill needs: **spawn**, **isolate**, **await**, **integrate**, **cleanup**. Map them on the current harness. Prefer the host's native isolation; do not invent a second worktree scheme when one exists.

## OMP (Oh My Pi)

Primary reference host.

| Verb | How |
| --- | --- |
| spawn | Use the `task` tool; one task per ticket; agent type suited to implementation (typically `task`). |
| isolate | Request an isolated git worktree for the task (`isolated: true` / host equivalent). Confirm the worker's cwd is the worktree. |
| await | Wait until every task in the wave settles; use the Agent Hub / task completion signals the host provides. Do not poll with ad-hoc sleeps when the host notifies on completion. |
| integrate | Apply or merge the task worktree into the orchestrator's current branch. Prefer the host's apply/merge controls when present; otherwise `git fetch`/`merge`/`rebase` from the worktree branch onto the current branch, resolving via `/resolving-merge-conflicts` only if already mid-conflict. |
| cleanup | Remove or keep worktrees with `omp worktree` as appropriate; keep failed/review-blocked trees until the user discards them. |

Workers should receive the same skills discovery the orchestrator has (`/implement`, `/tdd` visible). If the isolated session strips skills, pass an explicit instruction to load them.

## Cursor / other Task-capable hosts

| Verb | How |
| --- | --- |
| spawn | Host Task / subagent API — one subagent per ticket, in parallel. |
| isolate | Prefer a worktree-backed runner when the host offers one (e.g. isolated/best-of-n worktree). Otherwise create `git worktree add` on a branch named after the ticket and set the subagent cwd there. |
| await | Host parallel task completion. |
| integrate | Merge each ticket branch into the current branch sequentially in the post-worker phase. |
| cleanup | `git worktree remove` when done; keep on failure/review block. |

## Hosts without subagents

Do not fake parallelism inside one context window. Tell the user this skill needs a harness that can spawn isolated workers, and fall back to serial `/implement` per frontier ticket only if they explicitly ask for that degraded mode.

## Adapter choice

Detect the host from available tools (OMP `task` + `omp worktree`, Cursor Task, etc.). State which adapter you are using in the first-wave confirmation so the user can object before spawn.
