# Ticket lifecycle

State is expressed only with the triage roles in `docs/agents/triage-labels.md`. This skill never invents labels such as `claimed`, `done`, or `failed`.

## Roles this skill touches

| Event | Label / Status change | Comment |
| --- | --- | --- |
| Claim | Remove `ready-for-agent` | `claimed by implement-with-subagents` |
| Done (committed) | Leave `ready-for-agent` off; check acceptance boxes | completion + commit reference |
| Worker / integrate / review failure | Restore `ready-for-agent` | failure reason + pointer to worktree if kept |
| Still blocked | unchanged | n/a — not on frontier |

Do not apply `ready-for-human`, `needs-info`, `needs-triage`, or `wontfix` from this skill unless the user explicitly redirects a ticket.

## Local markdown tracker

Per `docs/agents/issue-tracker.md`:

- Tickets live at `.scratch/<feature>/issues/<NN>-<slug>.md`.
- Triage role sits on the `Status:` line.
- On claim: clear `ready-for-agent` from `Status:` (blank the role or remove the line's role token) and append under `## Comments`.
- On done: mark every acceptance `- [x]`; append a done comment; keep `ready-for-agent` off.
- On failure: set `Status: ready-for-agent` again; append the failure comment.
- **Blocked by** lines name other ticket numbers; a blocker is complete when its acceptance criteria are all checked.

## Remote trackers (GitHub, Linear, …)

- Claim: remove the `ready-for-agent` label; add a comment.
- Done: ensure acceptance criteria in the body are checked; comment with commit; do not re-add `ready-for-agent`. Close the issue only if the project's tracker conventions say agents should close — otherwise leave that to the human.
- Failure: re-add `ready-for-agent`; comment.
- Blocking edges: use the tracker's native blocks/blocked-by when present; otherwise parse the ticket body's Blocked by section.

## Frontier scan checklist

1. List issues with `ready-for-agent`.
2. Parse blockers.
3. Exclude any whose blockers are incomplete.
4. Optional user filter (feature slug, path prefix, explicit ids).
5. That set is the frontier for the next wave.
