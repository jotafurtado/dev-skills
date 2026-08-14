# Ticket lifecycle

State is expressed with the triage roles in `docs/agents/triage-labels.md`. This skill never invents labels such as `claimed`, `done`, or `failed` for its own sake.

## Roles this skill touches

| Event | Label / Status change | Comment |
| --- | --- | --- |
| Claim | Remove `ready-for-agent` | `claimed by implement-with-subagents` |
| Done (committed) | Leave `ready-for-agent` off; check acceptance boxes; only then apply project “resolved/closed” if the tracker uses it | completion + **real** commit SHA |
| Worker / integrate / review failure | Restore `ready-for-agent` | failure reason + pointer to worktree if kept |
| Still blocked | unchanged | n/a — not on frontier |

Do not apply `ready-for-human`, `needs-info`, `needs-triage`, or `wontfix` from this skill unless the user explicitly redirects a ticket.

## Coexistence with Wayfinder vocabulary

Some repos' `docs/agents/issue-tracker.md` also document Wayfinder statuses: `Status: claimed` | `resolved`.

For **this** skill:

- **Do not write** `Status: claimed` on claim. Clear `ready-for-agent` and comment instead (or leave Status blank / omit the triage role).
- Treat `Status: resolved` **or** all acceptance boxes checked as a **complete** blocker when scanning the frontier.
- On done, after the feature commit exists on `git log`: check every acceptance `- [x]`; append the done comment with the SHA; if the project's tracker already uses Wayfinder `resolved` for finished implementation tickets, set `Status: resolved` **after** that commit — never in the same index as an uncommitted feature diff.

Frontier scan must not rely on a single magic Status string alone when tickets mix vocabularies: combine `ready-for-agent`, checkboxes, `Blocked by`, and comments.

## Local markdown tracker

Per `docs/agents/issue-tracker.md`:

- Tickets live at `.scratch/<feature>/issues/<NN>-<slug>.md`.
- Triage role sits on the `Status:` line when used.
- On claim: clear `ready-for-agent` from `Status:` and append under `## Comments`.
- On done: mark every acceptance `- [x]`; append a done comment with SHA from `git rev-parse`; keep `ready-for-agent` off.
- On failure: set `Status: ready-for-agent` again; append the failure comment.
- **Blocked by** lines name other ticket numbers; a blocker is complete when its acceptance criteria are all checked (or `Status: resolved`).

### Write hygiene

Issue files are product markdown. After any edit, the file must open as normal markdown: **no** `[path#hash]` tool headers and **no** `N:` line-number prefixes written back into the file.

## Remote trackers (GitHub, Linear, …)

- Claim: remove the `ready-for-agent` label; add a comment.
- Done: ensure acceptance criteria in the body are checked; comment with commit SHA from `git rev-parse`; do not re-add `ready-for-agent`. Close the issue only if the project's tracker conventions say agents should close — otherwise leave that to the human.
- Failure: re-add `ready-for-agent`; comment.
- Blocking edges: use the tracker's native blocks/blocked-by when present; otherwise parse the ticket body's Blocked by section.

## Frontier scan checklist

1. List issues with `ready-for-agent` (and any the user filter includes).
2. Parse blockers.
3. Exclude any whose blockers are incomplete (unchecked boxes and not `resolved`/closed).
4. Optional user filter (feature slug, path prefix, explicit ids).
5. That set is the frontier for the next wave.
6. If `|frontier| == 1` and the rest of the feature is a linear chain, apply the unit-frontier warning in [orchestrator-flow.md](orchestrator-flow.md).
