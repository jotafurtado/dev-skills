# Application context and synchronization

## Publish semantic context

Use application state for context the agent needs to share with the UI. Describe
meaning with stable IDs and structured fields rather than dumping the DOM,
entire records, or credentials into a prompt.

| Context | Purpose | Responsibility |
| --- | --- | --- |
| `navigation` | Current view, record, tab, and relevant filters | UI publishes semantic route state. |
| `selection` | Selected rows, blocks, assets, or other domain objects | UI updates and clears selection when its scope changes. |
| `view-screen` action | Resolve context IDs into authorized records or a useful screen summary | App action performs scoped reads. |
| `navigate` command | Ask the UI to move or focus an object | App navigation integration interprets and consumes it. |
| `sendToAgentChat` | Hand a user operation and its relevant context to chat | UI chooses explicit send versus draft for review. |

The framework also tracks URL and one-shot context keys. Check the installed
guide before manipulating reserved keys directly.

## Navigation is a two-way bridge

`useNavigationState` is a template/app hook, commonly located at
`app/hooks/use-navigation-state.ts`; it is not an assumed Core export. Inspect
and extend that hook first. The documented Core primitive is `useAgentRouteState`
from `@agent-native/core/client/navigation`. A non-router UI may instead need
the documented semantic-navigation primitive.

Keep outbound route-to-context mapping and inbound command-to-route mapping
consistent. Reuse the app's browser-tab identity so navigation and selection
target the intended tab. Retain command consumption, duplicate protection, and
source tagging supplied by the framework instead of adding a second loop.

When handing work to chat, distinguish visible prompt text from attached
model-visible context. Confirm the installed handoff options. Source access must
still be checked when the action resolves IDs from that context. On navigation,
clear selections that no longer belong to the active record/view.

## Choose an update path

Prefer action query/mutation hooks for ordinary CRUD. They participate in the
framework's action refresh path. Investigate stale UI by tracing the write,
action completion, change/version signal, query key, invalidation, and refetch.
A successful mutation with an unchanged screen is not proof of a database bug.

The current Data and Sync guide distinguishes local chat-run refreshes from
background changes originating in other tabs, users, jobs, or webhooks.
Background sync is opt-in and should have a concrete product reason. Consult
the installed `useDbSync` contract for that release's transport, scope, and
options rather than copying an interval or assuming perpetual SSE.

For a raw React Query query, inspect the documented change-version integration
before inventing manual timers. Keep query keys aligned with the actual view
and data scope. Add invalidation only when the existing action path does not
cover the write.

## Avoid refetch and navigation jitter

Reuse the existing tab/request-source tagging and ignore-source convention when
the installed version supports it. Self-originated selection or layout writes
should not continually refetch their own screen. Remote writes still need to
reach opted-in views. Avoid recreating framework polling or command consumers
inside individual components.

## Verification scenarios

- Change a route and selection; confirm the agent sees the correct stable IDs.
- Resolve those IDs through `view-screen`; verify unauthorized records stay out.
- Navigate through the agent; confirm the command runs once and targets the right tab.
- Mutate from UI and agent paths; confirm each produces the visible result.
- For remote-sync requirements, change data from a second tab/user and verify
  delivery, cleanup on unmount, and absence of recurring self-refetches.

## Official sources

- [Context Awareness](https://www.agent-native.com/docs/context-awareness.md)
- [Data and Sync](https://www.agent-native.com/docs/client-data.md)
- [Sync Internals](https://www.agent-native.com/docs/client-sync-internals.md)
- [Agent Chat](https://www.agent-native.com/docs/client-agent-chat.md)
- [Advanced Client APIs](https://www.agent-native.com/docs/client-advanced.md)
