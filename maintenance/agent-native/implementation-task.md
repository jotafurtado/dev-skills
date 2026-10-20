# Independent implementation task

The control and candidate start from identical official Chat standalone source
and the same resolved dependency lock. Read the app's AGENTS.md and its official
local skills. Only the candidate additionally reads the local agent-native skill
and its relevant references. Work only in the assigned app; do not inspect the
other variant or parent repository skill sources.

Implement `/tasks` list creation/completion using SQL/Drizzle and shared
actions, server-derived authenticated identity, owner-only reads/writes, and
anonymous rejection. Include loading, empty, error, and success UI states using
existing components, keyboard focus, and narrow-screen usability. Publish the
opened task and selection in agent context, and clear obsolete context on route
transitions. The agent must navigate to the correct task exactly once. Preserve
the chat runtime. UI/agent writes refresh the screen and a same-owner second
session receives changes through supported sync. Extend authorized view-screen,
navigate, and tool discovery. Verify every introduced API against installed
docs/types. Keep pins; do not install or build until the parent prepares the
baseline. No secrets in files/output, no commit/deploy. Code English, new UI
pt-BR, Title Case controls, no new any types. Provide API evidence, meaningful
tests, changed files, and limitations.

## Execution notes

Two initial workers were interrupted immediately because they inherited parent
history, which already contained the candidate skill. The measured pair used
`fork_turns=none`, the same default host model, no model override, separate app
folders, and the task above. No implementation from those interrupted workers
was used. Both measured workers stopped after implementation and their own
checks. Parent-owned HTTP/browser tests use identical semantics and documented
adapters for the two valid action/route shapes.

This is one implementation pair, not a statistical superiority experiment.
Workers can access the shared filesystem; isolation is instruction-based, not a
filesystem sandbox. Their responses and produced deltas are preserved. Parent
changes, if any, are reported separately from initial output.
