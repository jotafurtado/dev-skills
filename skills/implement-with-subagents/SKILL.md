---
name: implement-with-subagents
description: "Orchestrates parallel waves of isolated workers over ready-for-agent frontier tickets; the orchestrator reviews and commits. User-invoked via /implement-with-subagents (optional feature slug). Use when the user asks to implement multiple ready-for-agent tickets in parallel. Do not trigger for a single ticket (use /implement), triaging or labeling (use /triage), writing specs, committing existing work, or a generic request to use subagents without a ready-for-agent frontier."
license: MIT
metadata:
  compatibility: "Requires Matt Pocock /implement, /tdd, and /code-review installed. Harness-agnostic contract; spawn/isolate/integrate in references/host-adapters.md."
  author: jotafurtado
  version: "1.2.2"
  domain: workflow
  role: orchestrator
  scope: implementation
  tags: "implement, subagents, parallel, tickets, worktree, orchestration"
disable-model-invocation: true
---

# Implement with subagents

Orchestrate **waves** of **workers** over the issue-tracker **frontier**. This skill extends the Matt Pocock [`/implement`](https://github.com/mattpocock/skills) contract with parallel subagents — it does not patch or vendor that skill.

## Preflight

Read [`CONTEXT.md`](CONTEXT.md) for leading-word definitions and forbidden synonyms (**frontier**, **wave**, **worker**, **orchestrator**, **miolo**, **claim**, **dirty-tree integrate**, **degraded review**, **resume handshake**, **host adapter**).

1. Working directory is a git repo on the branch that should receive integrated commits.
2. `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md` exist (run `/setup-matt-pocock-skills` if not).
3. Installed `/implement`, `/tdd`, and `/code-review` resolve on the host. If any is missing, stop and tell the user to install Matt Pocock's skills (e.g. via `/setup-matt-pocock-skills`). Do not paste a private fork of those skills into the worker prompt.
4. Optional argument: a feature slug or tracker filter. Without it, discover all `ready-for-agent` tickets the configured tracker exposes for this repo.
5. If this session is a **resume**, run the resume handshake in `references/orchestrator-flow.md` before anything else.

| Piece | Owner |
| --- | --- |
| TDD loop, typecheck/tests cadence, single-ticket shape | Installed `/implement` + `/tdd` |
| Two-axis review before commit | Installed `/code-review` (or degraded in-process fallback) |
| Frontier, waves, claim, isolate, dirty-tree integrate, failure policy | This skill |

## Gates

- Workers never commit and never run `/code-review`.
- Only the orchestrator commits, and only after a passing review gate.
- SHAs in reports come from `git rev-parse` / `git log`, never from chat memory.
- Parallelism follows blocking edges only — do not invent file-overlap scheduling in v1.
- Use triage roles for claim/re-queue; map Wayfinder `resolved` only as documented in `references/ticket-lifecycle.md`.
- Prefer Continue inside a wave; do not `/clear` between tickets of the same wave.
- Do not open source-repo ADRs at runtime — the installer does not copy them.

## Reference routing

| Task touches | Read |
| --- | --- |
| Frontier scan, claim/done/failure labels, Wayfinder `Status` | `references/ticket-lifecycle.md` |
| Worker prompt, exclusions, result JSON | `references/worker-contract.md` |
| Spawn, isolate, dirty-tree integrate, host fallback | `references/host-adapters.md` |
| Resume handshake, unit-frontier warning, claim race, degraded review, next-wave SHA | `references/orchestrator-flow.md` |

## Flow

### 1. Discover and compute the frontier

Follow the tracker in `docs/agents/issue-tracker.md`. The **frontier** is every `ready-for-agent` ticket whose blockers are complete — scan checklist in `references/ticket-lifecycle.md`. A blocker is complete only per the complete-blocker rule in `references/orchestrator-flow.md`.

If the frontier is empty, report why (none ready, or all ready tickets still blocked) and stop.

If `|frontier| == 1` and the rest is a linear blocked chain, warn that isolation will not buy parallelism — unit-frontier warning in `references/orchestrator-flow.md`.

### 2. Human gate (first wave, and every resume mini-gate)

List the frontier: title, id/path, blockers (none), adapter name. Ask the user to confirm before spawning.

Later waves in the **same unbroken conversation** recompute the frontier and spawn without asking, unless the user asked to pause between waves. After resume/compaction, always mini-gate again.

### 3. Claim, then spawn the wave

For each frontier ticket, **claim**: remove `ready-for-agent` and append a short tracker comment that this skill claimed it (pure markdown — `references/ticket-lifecycle.md`). If the claim fails, drop that ticket from the wave — claim race in `references/orchestrator-flow.md`. Then spawn one **worker** per ticket, in parallel, each in an isolated worktree/branch.

When spawning, read `references/worker-contract.md` for the prompt. When isolating or integrating, read `references/host-adapters.md`.

### 4. Await workers; do not abort the wave on one failure

When a worker fails (red tests, crash, timeout, empty diff when work was required), restore `ready-for-agent`, comment the failure, leave or clean its worktree per the host adapter, and continue with the others. Dependents of a failed ticket stay blocked.

Do **not** integrate until that worker reports `outcome: success`.

### 5. Post-worker phase — sequential per successful ticket

For each successful worker, in stable ticket order:

1. Record `fixed-point` = current orchestrator `HEAD` (`git rev-parse HEAD`).
2. **Dirty-tree integrate** into the current branch — read `references/host-adapters.md`. Trust `git status` in the worktree, not `filesTouched` alone; never no-op `git merge` of an uncommitted ticket branch.
3. Run the project tests on the orchestrator branch.
4. Run `/code-review` against that fixed point. If `/code-review` cannot spawn, use the degraded in-process fallback in `references/orchestrator-flow.md`.
5. **Review gate**: P0 or Spec-fail → do not commit; restore `ready-for-agent`; comment findings; leave the worktree for inspection; continue to the next ticket.
6. On clean (or degraded-but-passing) review: **commit** on the current branch; only then, after `git rev-parse HEAD` shows the new SHA, mark acceptance criteria done and comment completion; do **not** put `ready-for-agent` back.

If integrate conflicts or the copy is incomplete, restore `ready-for-agent`, comment, leave the worktree, and continue. Never mark the ticket done before the feature commit exists on `git log`.

### 6. Next wave or stop

Do not start the next wave until every intended commit from this wave has a SHA on `git log`. Recompute the frontier. If non-empty, go to step 3 (no human gate only inside an unbroken conversation). If empty, stop and Verify.

## Verify

Always end with:

- Committed (ticket → commit sha from `git log`)
- Re-queued (`ready-for-agent` restored): worker failure / review gate / integrate conflict
- Still blocked (waiting on incomplete blockers)
- Worktrees left for inspection (paths)
- `review: ok` or `review: degraded` per ticket when relevant
