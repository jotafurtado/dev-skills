# Host adapters

Portable verbs: **spawn**, **isolate**, **await**, **integrate**, **cleanup**. This file tells *what* must hold; *how* is up to the agent using the host's native capabilities.

> In OMP, saying **"orchestrate"** triggers native multi-phase + parallel subagent orchestration — prefer that when available. Let the agent pick the concrete mechanism (isolated worktree, task tool, etc.) that best satisfies the invariants below.

## Invariants (all hosts)

- **Isolation**: each worker gets its own worktree/branch. No two workers write the same working tree concurrently.
- **No commit by worker**: workers leave dirty tree only.
- **Integrate = dirty tree** (see below), not `git merge` of an uncommitted ticket branch.
- **Await = settlement**: do not integrate until `outcome: success`.

## Integrate — dirty tree is the default

Workers **must not commit**, so `git merge ticket/...` is usually a no-op.

1. Only after `outcome: success`.
2. `git status --short` in the worktree is authoritative (include untracked).
3. `filesTouched` is index only — copy **status**, not just the list.
4. Copy every path from status into orchestrator tree (skip `node_modules`, caches, `.env*`). Use `git checkout` only if the path was committed; otherwise copy file contents.
5. Run focused tests on orchestrator branch, then review/commit per SKILL.md.

## How to choose a mechanism

Let the agent decide using the host's native tools:

- If the host offers isolated worktrees / `task --isolated` / `orchestrate`, use it.
- If native isolation fails, fallback is always `git worktree add -b ticket/<id>-<slug> .worktrees/<slug>` and spawn subagents with cwd = that worktree. Ensure `.worktrees/` is gitignored.
- State the chosen adapter in the first-wave confirmation (`adapter: <name>`); if you fall back mid-wave, note it in the report.

## Hosts without subagents

Do not fake parallelism in one window. Tell the user this host needs isolated workers; fall back to serial `/implement` only if explicitly requested.
