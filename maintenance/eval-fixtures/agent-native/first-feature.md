# First shared feature: task completion

Synthetic project evidence for a read-only design evaluation. This is not a
runnable app or an authoritative framework API declaration.

The existing Chat-template app has Core and Toolkit dependencies, a SQL tasks
table, app-local controls, an action directory, and an app navigation hook.
The manifest and lockfile contents have not been supplied. No installed package
docs, exports, or declarations are available in this fixture.

The product request is to list my tasks and complete one using either the UI or
the in-app agent. The agent should understand which task the user has open.

Proposed implementation:

- Add a browser-only POST route that updates SQL directly.
- Add a separate agent tool with its own SQL update logic.
- Both implementations accept taskId and ownerId from the caller; neither
  verifies the authenticated actor against that ownerId.
- Fetch the task list through another route without ownership filtering.
- Put the open task ID only in React component state.
- Display a success toast as soon as the completion button is clicked.
- Skip action descriptions, input validation, and pending/error behavior until later.

No tests or browser/agent runs have been performed. The evaluator expects an
implementation approach and verification plan, not a fabricated working patch.
