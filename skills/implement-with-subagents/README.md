# Implement with subagents

Orchestrates **parallel** implementation of `ready-for-agent` tickets whose blockers are done. Extends the Matt Pocock [`/implement`](https://github.com/mattpocock/skills) contract with an orchestrator that spawns isolated workers, then reviews and commits sequentially.

Current version: **1.2.2**

## Install

```bash
npx skills add jotafurtado/dev-skills --skill implement-with-subagents
```

Also install Matt Pocock's skills so `/implement`, `/tdd`, and `/code-review` resolve on the host (for example via `/setup-matt-pocock-skills`).

## What's covered

- Frontier detection from the tracker configured in `docs/agents/issue-tracker.md`
- Human confirmation of the first wave (and mini-gate on session resume)
- Warning when the frontier is a single ticket in a linear chain (isolation ≠ parallelism)
- Claim by removing `ready-for-agent` (no new triage labels)
- One isolated worktree worker per frontier ticket (miolo of `/implement`: TDD + verify, no review, no commit)
- Cursor/OMP isolate fallbacks when the native runner fails to start
- **Dirty-tree integrate** (copy every non-junk path from worktree `git status`, tracked and untracked; completeness check before tests; do not merge an uncommitted ticket branch)
- Worker prompt template in `references/worker-contract.md` (ticket, absolute Matt skill paths, exclusions, JSON result)
- Failure isolation — one red worker does not abort the wave
- Sequential integrate → test → `/code-review` (or degraded in-process) → commit
- Automatic follow-up waves only after real commit SHAs exist on `git log`

## Invocation

User-invoked (`disable-model-invocation: true`): `/implement-with-subagents`, optionally with a feature slug. Hosts that honor the flag keep the description out of always-on context load.

Not for a single ticket — use `/implement`. Not for triaging or labeling issues — use `/triage`. Not for writing specs, committing existing work, or a generic "use subagents" request without a `ready-for-agent` frontier.

## Requirements

- Git repository
- Matt Pocock `/implement`, `/tdd`, `/code-review`
- `docs/agents/issue-tracker.md` from setup
- A host that can spawn isolated subagents (OMP recommended; Cursor with manual worktree fallback supported — see `references/host-adapters.md`)

## License

MIT
