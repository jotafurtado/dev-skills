# Implement with subagents

Orchestrates **parallel** implementation of `ready-for-agent` tickets whose blockers are done. Extends the Matt Pocock [`/implement`](https://github.com/mattpocock/skills) contract with an orchestrator that spawns isolated workers, then reviews and commits sequentially.

Current version: **1.1.0**

## Install

```bash
npx skills add jotafurtado/dev-skills --skill implement-with-subagents
```

Also install Matt Pocock's skills so `/implement`, `/tdd`, and `/code-review` resolve on the host (for example via `/setup-matt-pocock-skills`).

## What's covered

- Frontier detection from the tracker configured in `docs/agents/issue-tracker.md`
- Human confirmation of the first wave only
- Claim by removing `ready-for-agent` (no new triage labels)
- One isolated worktree worker per frontier ticket (miolo of `/implement`: TDD + verify, no review, no commit)
- Failure isolation — one red worker does not abort the wave
- Sequential integrate → `/code-review` → commit on the current branch
- Automatic follow-up waves until the frontier is empty

## Invocation

User-invoked (`disable-model-invocation: true`): `/implement-with-subagents`, optionally with a feature slug. Hosts that honor the flag keep the description out of always-on context load.

Not for a single ticket — use `/implement`. Not for triaging raw issues — use `/triage`.

## Requirements

- Git repository
- Matt Pocock `/implement`, `/tdd`, `/code-review`
- `docs/agents/issue-tracker.md` from setup
- A host that can spawn isolated subagents (OMP recommended; see `references/host-adapters.md`)

## License

MIT
