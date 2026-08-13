# Orchestrator flow

Ordered detail for the session that runs `/implement-with-subagents`. The SKILL.md steps are authoritative; this file expands completion criteria and edge cases.

## Discovery

1. Read `docs/agents/issue-tracker.md` and apply its fetch conventions.
2. If the user passed a feature slug (e.g. `checkout`), restrict to that feature's tickets.
3. Build a graph: ticket id → blockers, status/labels, acceptance checklist.
4. Frontier = `ready-for-agent` ∧ all blockers complete.

**Complete blocker** means the blocking ticket's acceptance criteria are satisfied (checkboxes checked locally, or the tracker marks the issue done/closed). A ticket that lost `ready-for-agent` because it was claimed mid-flight is not "complete".

## First-wave confirmation

Present a compact table:

- id / path
- title
- blocked by (should be none for frontier members)

Wait for explicit OK. On rejection, stop without claims.

## Claiming

For each confirmed frontier ticket, before spawn:

1. Remove `ready-for-agent` (local `Status:` line or remote label).
2. Append under `## Comments` (or the tracker's comment API): `claimed by implement-with-subagents` plus timestamp / session hint.
3. Only then spawn the worker.

If claim fails (race), drop that ticket from the wave and report it.

## Spawning

Spawn the whole frontier in one parallel fan-out. One worker ↔ one ticket ↔ one isolated worktree. Pass each worker the ticket body, acceptance criteria, and the [worker-contract](worker-contract.md) constraints.

Do not start the post-worker phase until every worker in the wave has settled (success or failure).

## Failure isolation

Per failed worker:

- Restore `ready-for-agent`.
- Comment with the failure summary the worker returned (or "timeout/no report").
- Do not integrate that worktree into the trunk.
- Continue post-worker work for successes.

Never cancel in-flight siblings because one peer failed.

## Integrate → review → commit

Process successes in ascending ticket id / number order so logs stay predictable.

1. **Integrate** via the [host adapter](host-adapters.md) into the orchestrator's current branch. On merge/rebase conflict: treat as failure for that ticket (restore `ready-for-agent`, comment, leave worktree), continue.
2. Record `fixed-point` = `HEAD` before this ticket's commit (the commit before integration, or the merge-base the review skill expects — pin explicitly for `/code-review`).
3. Run `/code-review` with that fixed point and the ticket as the spec source.
4. **Gate**: any P0 finding or Spec-axis failure blocks commit. Restore `ready-for-agent`, paste findings into the ticket comment, skip commit, move on.
5. **Commit** only the integrated diff for this ticket. Prefer the repo's usual commit skill if present. Message should reference the ticket id.
6. Mark acceptance criteria complete; comment done; leave `ready-for-agent` off.

## Wave boundary

After every ticket in the wave is either committed, re-queued, or left blocked on review/integration failure:

1. Recompute frontier (fresh tracker read).
2. If empty → final report.
3. If non-empty → claim + spawn immediately (no human gate unless the user asked for gates every wave).

## Final report

Always end with:

- Committed (ticket → commit sha)
- Re-queued (`ready-for-agent` restored): worker failure / review gate / integrate conflict
- Still blocked (waiting on incomplete blockers)
- Worktrees left for inspection (paths)
