# Host adapters

**Principle:** invariants are fixed; mechanism is chosen by the agent. This skill prescribes *what* must hold (isolate, dirty-tree, no-commit), the host prescribes *how* to get subagents.

## Invariants (all hosts)

- **Isolation**: one worktree/branch per worker. No concurrent writes to the same tree.
- **No commit by worker**: workers leave a dirty tree only.
- **Integrate = dirty tree** (see below), not `git merge` of an uncommitted ticket branch.
- **Await = settlement**: do not integrate until `outcome: success`.

## Integrate — dirty tree is the default

Workers **must not commit**, so `git merge ticket/...` is usually a no-op: the ticket branch stays at the orchestrator SHA and the real diff lives in the worktree filesystem. After `outcome: success`, transfer that dirty tree onto the orchestrator branch.

Prefer a host apply/merge **only** when it actually copies those filesystem paths. Never declare success on `Already up to date` or an empty merge of an uncommitted ticket branch.

### Procedure

Run 1–5 in the worker worktree, then 6–8 on the orchestrator branch.

1. Confirm `outcome: success`. Do not copy a mid-flight tree.
2. Record `git rev-parse HEAD` in the worktree. It must equal the SHA the worker started from. If the worker committed, that is a contract violation: restore `ready-for-agent`, comment, leave the tree, continue.
3. Capture `git status --short` in the worktree. This list is authoritative. `filesTouched` is an index for comparison only — copy **status**, not just the list. If status is empty when the ticket required work, fail the integrate the same way as a red worker.
4. Classify each status path (include untracked `??`):
   - **Skip** local junk even if it appears: `node_modules/`, caches, `.env` / `.env.*` except a tracked `.env.example`, OS junk (`.DS_Store`, `Thumbs.db`), editor metadata. Ignored build artifacts are absent from status by design — do not go looking for them.
   - **Tracked modifications**: copy the worktree file bytes onto the same relative path in the orchestrator tree (`mkdir -p` parents as needed). Do **not** `git checkout` the ticket branch — there is no commit to check out.
   - **Untracked files (`??`)**: copy file contents the same way; there is no blob.
   - **Deletions**: delete the corresponding path on the orchestrator tree.
   - **Renames (`R`)**: delete the old path and copy the new path.
   - Never copy the worktree's `.git`.
5. **Completeness check** before tests: every non-junk path from step 3 must be represented on the orchestrator tree (present with matching content, or absent if it was a deletion). Diff the filtered worktree status against orchestrator paths. If any ticket path is missing or content differs, fail: restore `ready-for-agent`, comment the missing paths, leave the worktree, continue to the next ticket.
6. Run focused tests on the orchestrator branch.
7. Review and commit per `SKILL.md`.
8. Only after `git rev-parse HEAD` shows the new commit, mark the ticket done and clean the worktree.

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
