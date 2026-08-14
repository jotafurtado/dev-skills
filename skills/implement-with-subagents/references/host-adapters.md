# Host adapters

**Principle:** invariants are fixed; mechanism is chosen by the agent. This skill prescribes *what* must hold (isolate, dirty-tree, no-commit), the host prescribes *how* to get subagents.

## Invariants (all hosts)

- **Isolation**: one worktree/branch per worker. No concurrent writes to the same tree.
- **No commit by worker**: workers leave a dirty tree only.
- **Integrate = dirty tree** (see below), not `git merge` of an uncommitted ticket branch.
- **Await = settlement**: do not integrate until `outcome: success`.

## Integrate — dirty tree is the default

Workers **must not commit**, so `git merge ticket/...` is usually a no-op.

1. Only after `outcome: success`.
2. `git status --short` in the worktree is authoritative (include untracked).
3. `filesTouched` is index only — copy **status**, not just the list.
4. Copy every path from status into orchestrator tree (skip `node_modules`, caches, `.env*`). Use `git checkout` only if the path was committed; otherwise copy file contents.
5. Run focused tests on orchestrator branch, then review/commit per SKILL.md.

## Trigger words by host (hints, not requirements)

Use the host's native trigger when you want to *force* parallelism. Otherwise let automatic delegation decide.

| Host | How to nudge subagents | Where roles live |
|---|---|---|
| **OMP** | Type **`orchestrate`** — glows and forces multi-phase + parallel orchestration. Otherwise auto-delegates when task looks complex. Agent `task` role + `.omp/agents/*.md` (description) drives routing. | `task` tool (`isolated: true`), Agent Hub `Alt+A` |
| **Claude Code** | Say **`use subagents`** / **`in parallel`** / **`Task: ...`** in the prompt. Or `/agents`. Custom agents routed by **description** in `.claude/agents/`. | `Explore` (Haiku, read-only), `Plan`, `General-purpose` |
| **Cursor** | **`/orchestrate`** skill or `/create-subagent`. Foreground vs background controls sequencing. Auto-delegation on complex tasks. | `.cursor/agents/` + `.cursor/rules/` + `SKILL.md` |
| **Codex** | **`Delegate` / `Split` / `Break into sub-tasks`** in prompt, or `AGENTS.md` in repo. “Ultra” mode may auto-parallelize. | `AGENTS.md` |
| **OpenCode** | Manual **`@explore`** / **`@<name>`** mention. Auto via Build/Plan based on **description** (`mode: subagent`). | `opencode.json` / `.opencode/agent/` |

> No host requires a magic word — descriptive intent is enough. The table just makes “force it now” reliable.

## How the agent should choose

1. Prefer the host's native isolated mechanism if available (OMP `isolated: true`, Claude Code subagents, Cursor orchestrate, OpenCode `@`).
2. If native isolation fails to start, **fallback is always portable**: `git worktree add -b ticket/<id>-<slug> .worktrees/<slug>` and spawn subagents with `cwd = that worktree`. Ensure `.worktrees/` is gitignored.
3. Announce the chosen adapter in the first-wave confirmation (`adapter: <name>`); note any mid-wave fallback in the wave report.

## Hosts without subagents

Do not fake parallelism in one window. Tell the user this host needs isolated workers; fall back to serial `/implement` only if explicitly requested.
