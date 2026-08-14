# Orchestrator flow

Edge cases and completion criteria for `/implement-with-subagents`. The Flow in `SKILL.md` is authoritative — this file does not restate those steps.

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

Do not start dirty-tree integrate for a ticket until that worker has settled with `outcome: success`. Mid-flight files in the worktree are not a deliverable. Inspecting them for curiosity is fine; copying them is not.

## Post-worker order

Process successful workers in ascending ticket id/number order.

1. Record `fixed-point` = current orchestrator `HEAD` (`git rev-parse HEAD`).
2. **Integrate** via dirty-tree rules in [host-adapters.md](host-adapters.md). On conflict or incomplete copy: restore `ready-for-agent`, comment, leave worktree, continue.
3. Run project tests on the orchestrator branch after integrate.
4. Run `/code-review` against the fixed point with the ticket as spec source.
5. **Review gate**: P0 or Spec-fail → do not commit; restore `ready-for-agent`; comment; leave worktree; continue.
6. Commit only after a clean (or explicitly degraded-but-passing) review gate.
7. Only after `git rev-parse HEAD` shows the new commit: mark acceptance criteria done / tracker done comment; then cleanup worktree.

Never mark the ticket done in the same staging area *before* the feature commit exists on the log. Tracker edits for “done” happen **after** the commit SHA is real.

## Degraded `/code-review`

If `/code-review` cannot spawn its review axes (same class of host failure as a dead isolated runner):

1. The orchestrator performs both axes (Standards + Spec) **in-process** on the integrated diff.
2. Mark the wave report: `review: degraded`.
3. The gate still applies: P0 or Spec-fail → no commit.
4. Do not pretend the Matt skill ran; say it fell back.

## Next wave gate

Do not claim or spawn the next wave until every successful ticket from the current wave that you intended to commit has a SHA on `git log` (or was explicitly re-queued). Announcing “committed” without `rev-parse` is a skill violation.

## Tracker markdown hygiene

When editing issue files, write **pure file contents** only. Never write tool display wrappers (`[path#hash]` headers or `N:` line-number prefixes) back into the ticket. After claim/done, the file must remain valid markdown.

## Final report

Always end with:

- Committed (ticket → commit sha from `git log`)
- Re-queued (`ready-for-agent` restored): worker failure / review gate / integrate conflict
- Still blocked (waiting on incomplete blockers)
- Worktrees left for inspection (paths)
- `review: ok` or `review: degraded` per ticket when relevant
