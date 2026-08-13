# Orchestrator flow

Edge cases and completion criteria for `/implement-with-subagents`. The Flow in `SKILL.md` is authoritative — this file does not restate those steps.

## Complete blocker

A blocker is **complete** only when its acceptance criteria are satisfied (local checkboxes checked, or the tracker marks the issue done/closed). Losing `ready-for-agent` because the ticket was **claimed** mid-flight does **not** count as complete.

## Claim race

If removing `ready-for-agent` fails or another session already cleared it, drop that ticket from the wave and report it. Never spawn without a successful claim.

## Post-worker fixed point and integrate conflict

Process successful workers in ascending ticket id/number order.

Before integrating each ticket, record `fixed-point` = current `HEAD` (or the merge-base `/code-review` expects). After integrate, run `/code-review` against that fixed point with the ticket as the spec source.

On merge/rebase conflict during integrate: treat as failure for that ticket — restore `ready-for-agent`, comment, leave the worktree, continue to the next success.

## Final report

Always end with:

- Committed (ticket → commit sha)
- Re-queued (`ready-for-agent` restored): worker failure / review gate / integrate conflict
- Still blocked (waiting on incomplete blockers)
- Worktrees left for inspection (paths)
