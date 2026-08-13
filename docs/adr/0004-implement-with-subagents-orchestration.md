# Parallel implement via orchestrator-owned review and commit

Status: Accepted

## Context

`/implement` (Matt Pocock) is a single-ticket, single-session skill: TDD, verify, `/code-review`, then commit on the current branch. Running that whole loop in parallel subagents collides on the working tree and on commit ownership. Patching Matt's skill in place is off the table — his pack updates independently and we must not edit it.

## Decision

Publish a separate skill, `implement-with-subagents`, that owns **orchestration only**.

- Workers run the **miolo** of `/implement` (TDD + ticket verification) inside an isolated worktree/branch and must not review or commit.
- The orchestrator integrates each successful worktree into the current branch, runs `/code-review`, and only then commits — sequentially per ticket inside a wave.
- Parallelism is gated solely by **blocking edges** (the frontier). A failed or review-blocked ticket does not abort the wave; it restores `ready-for-agent` and keeps dependents blocked.
- Claim/done/failed are expressed with the existing triage vocabulary only: claim and done clear `ready-for-agent`; failure puts `ready-for-agent` back.

The skill is harness-agnostic at the contract layer and documents host adapters (starting with OMP) for spawn/isolate/integrate.

## Consequences

- Requires Matt's `/implement`, `/tdd`, and `/code-review` installed at runtime; we cite them and do not vendor their text.
- Review findings that fail the gate leave the ticket uncommitted and re-queueable, so the trunk stays review-clean.
- File-overlap inside a frontier is accepted as a risk of blocker-only parallelism; integration conflicts surface at integrate time and follow the failure policy.
