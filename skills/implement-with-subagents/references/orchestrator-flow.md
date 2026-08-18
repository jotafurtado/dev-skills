# Orchestrator flow

Edge cases for `/implement-with-subagents`. The Flow in `SKILL.md` is authoritative — this file does not restate those steps.

## Complete blocker

A blocker is **complete** only when its acceptance criteria are satisfied (local checkboxes checked, or the tracker marks the issue done/closed / `Status: resolved`). Losing `ready-for-agent` because the ticket was **claimed** mid-flight does **not** count as complete.

## Claim race

If removing `ready-for-agent` fails or another session already cleared it, drop that ticket from the wave and report it. Never spawn without a successful claim.

## Unit frontier warning

If the frontier has exactly one ticket and remaining open tickets are blocked behind it (a linear chain), tell the human at the gate: isolation still protects the orchestrator branch, but **no parallelism will occur**. Offer `/implement` serial as an alternative. Proceed with this skill only if they confirm.

## Resume handshake

On any session resume (compaction, new turn after a long gap, “continue the wave”), **before** claiming or spawning:

1. `git log --oneline -5` on the orchestrator branch
2. `git worktree list`
3. `git status --short` on the orchestrator branch and on every live ticket worktree
4. Re-read tracker `Status:` / labels and acceptance checkboxes for in-flight tickets

**Never cite a commit SHA from chat memory.** A SHA enters the report only after `git rev-parse HEAD` (or `git log -1 --format=%h`) on the orchestrator branch shows it.

Treat resume as a **mini-gate**: list remaining frontier + live worktrees and get confirmation before spawning again, unless the original first-wave confirmation is still in the same unbroken conversation and no compaction/handoff occurred.

## Await — do not integrate early

Do not copy a mid-flight worktree. Inspecting it is fine; dirty-tree integrate starts only after `outcome: success`.

## Post-worker extras

The numbered post-worker loop in `SKILL.md` is authoritative. Do not start a different order.

- Process successful workers in ascending ticket id/number order.
- On integrate conflict or incomplete copy: restore `ready-for-agent`, comment, leave the worktree, continue.
- `/code-review` uses the recorded fixed point as the diff base and the ticket as spec source.
- Tracker edits for “done” happen **after** the commit SHA is real — never in the same index as an uncommitted feature diff.
- Cleanup the worktree only after `git rev-parse HEAD` shows the new commit.

## Degraded `/code-review`

If `/code-review` cannot spawn its review axes (same class of host failure as a dead isolated runner):

1. The orchestrator performs both axes (Standards + Spec) **in-process** on the integrated diff.
2. Mark the wave report: `review: degraded`.
3. The gate still applies: P0 or Spec-fail → no commit.
4. Do not pretend the Matt skill ran; say it fell back.

## Next wave gate

Do not claim or spawn the next wave until every successful ticket from the current wave that you intended to commit has a SHA on `git log` (or was explicitly re-queued). Announcing “committed” without `rev-parse` is a skill violation.

## Tracker markdown hygiene

When editing issue files, follow write hygiene in [ticket-lifecycle.md](ticket-lifecycle.md): pure file contents only — no tool display wrappers.

## Final report

Follow **Verify** in `SKILL.md`. A SHA enters the report only after `git rev-parse` / `git log` shows it.
