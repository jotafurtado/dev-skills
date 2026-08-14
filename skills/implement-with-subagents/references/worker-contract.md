# Worker contract

Each worker implements **one** ticket. It follows the installed Matt Pocock `/implement` skill for the miolo only.

## Required preamble (pass verbatim intent)

Give the worker:

1. Full ticket text (what to build, acceptance criteria, blockers already satisfied).
2. Path or id of the ticket on the tracker.
3. Instruction to load and follow `/implement` and `/tdd` as installed on the host. If the isolated session may not discover skills, pass absolute paths to those `SKILL.md` files.
4. The hard exclusions below.
5. The required result shape below.

## Hard exclusions

The worker MUST:

- Stay inside its isolated worktree/branch.
- Use `/tdd` at pre-agreed seams (confirm seams briefly if the ticket does not already pin them; prefer seams named in the ticket/spec).
- Run typechecking and the ticket-relevant tests regularly; run the focused suite that proves the acceptance criteria.
- Leave changes **uncommitted** in the worktree.

The worker MUST NOT:

- Run `/code-review`.
- Create a git commit, amend, rebase onto trunk, or push.
- Modify tracker labels/status (the orchestrator owns claim/done/failure).
- Start work on any other ticket.
- Edit files outside the worktree root.

## Required result shape

Return a concise structured result (JSON is fine):

| Field | Meaning |
| --- | --- |
| `outcome` | `success` \| `failure` |
| `filesTouched` | Paths the worker believes it changed — **index only**; orchestrator validates via `git status` in the worktree |
| `testsRun` | What was run |
| `criteriaMet` | Which acceptance criteria are met |
| `skillsLoaded` | e.g. `["implement","tdd"]`, or `[]` if the worker followed the prompt only because skills were missing |
| `orchestratorBlockers` | Anything the orchestrator must handle |

If `skillsLoaded` is empty, the orchestrator treats the run as **prompt-only** and may re-queue or re-prompt when fidelity to `/implement` matters.

## Success vs failure

- **success**: acceptance criteria are demonstrably met in this worktree; tests proving them are green; no commit was made.
- **failure**: cannot meet criteria, tests stay red, or an unrecoverable error — return why; leave the tree as-is for orchestrator inspection when useful.

## Provenance note for the worker prompt

You may include one line: "Execution contract from Matt Pocock `/implement` (TDD + verify); review and commit are intentionally withheld for the orchestrator (`implement-with-subagents`)." Do not paste the full text of Matt's skill into the prompt — instruct the worker to invoke the installed skill (or open the absolute `SKILL.md` paths you passed).
