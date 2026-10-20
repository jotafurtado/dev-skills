# UI and Toolkit discovery map

## Choose the smallest suitable layer

Start with the existing app's composition. Use a complete shared surface when
it fits; move down to panel, runtime-backed chat, or composer/transcript pieces
only when the requested product behavior requires more control. Preserve thread
state, streaming, tool results, attachments, and context when changing chrome.

The catalog below is a discovery snapshot, checked on 2026-10-17. Names and
package subpaths come from the official Component API and Toolkit guides. Verify
exports, props, providers, and CSS requirements in the installed release before
importing them. Availability can differ between Core and Toolkit versions.

## Catalog by purpose

Paths are public entry-point candidates, not instructions to replace app-local
adapters. Each row links to the page that owns its usage contract.

| Need | Principal building blocks | Owner / documented entry | Source |
| --- | --- | --- | --- |
| Complete agent sidebar | `AgentSidebar`, `AgentToggleButton` | Toolkit: `@agent-native/toolkit/app/chat` | [Component API](https://www.agent-native.com/docs/components.md#agent-chat-ui) |
| Chat in an app-owned layout or route | `AgentPanel`, `AgentChatSurface` | Toolkit: `@agent-native/toolkit/app/chat` | [Agent Surfaces](https://www.agent-native.com/docs/agent-surfaces.md) |
| Custom chat chrome and thread tabs | `AssistantChat`, `MultiTabAssistantChat` | Toolkit: `@agent-native/toolkit/app/chat` | [Component API](https://www.agent-native.com/docs/components.md#agent-chat-ui) |
| Prompt entry, attachments, mentions | `PromptComposer` | Toolkit: `@agent-native/toolkit/app/chat/composer` | [Composer](https://www.agent-native.com/docs/components.md#composer) |
| Conversation/transcript rendering | `AgentConversation` | Toolkit: `@agent-native/toolkit/app/chat/conversation` | [Conversation](https://www.agent-native.com/docs/components.md#conversation) |
| Threads, handoffs, runtime adapters | `useChatThreads`, `sendToAgentChat`, `createHttpAgentChatRuntime` | Core: `@agent-native/core/client/agent-chat` | [Component API](https://www.agent-native.com/docs/components.md#agent-chat-ui) |
| Prompt landing and template browsing | `PromptHome`, `PromptHomeLibrary`, `TemplateLibraryGrid`, `TemplatePreviewDialog` | Toolkit: `@agent-native/toolkit/app-shell` | [Prompt Home](https://www.agent-native.com/docs/components.md#prompt-home) |
| Controls and overlays | Button, dialog, menu, input and related primitives | Toolkit primitives behind app-local adapters; semantic adapters through `ToolkitProvider` | [UI Primitives](https://www.agent-native.com/docs/toolkit-ui.md) |
| Header actions and responsive feedback | `useSetHeaderActions`, mobile/toast hooks | Toolkit: `@agent-native/toolkit/app-shell`, documented hook subpaths | [Shell Hooks](https://www.agent-native.com/docs/toolkit-ui.md#shell-hooks) |
| Settings and workspace navigation | Shared settings pages, command/navigation kits | Toolkit surfaces; inspect each kit's public exports | [Settings](https://www.agent-native.com/docs/toolkit-settings.md), [Navigation](https://www.agent-native.com/docs/toolkit-command-navigation.md) |
| Tabular editing and dashboards | `DataGrid`, `DataTable`, `MetricCard`, `GenericChartPanel` | Toolkit: `@agent-native/toolkit/data-grid`, `@agent-native/toolkit/dashboard` | [Grid](https://www.agent-native.com/docs/toolkit-ui.md#data-grid), [Public UI](https://www.agent-native.com/docs/components.md#other-ui) |
| Rich content and structured blocks | `SharedRichEditor`, `BlockView`, `SchemaBlockEditor`, `BlockRegistryProvider` | Toolkit: `@agent-native/toolkit/editor`, `@agent-native/toolkit/app/blocks` | [Editors and Canvases](https://www.agent-native.com/docs/toolkit-editors-canvases.md) |
| Canvas annotations | `DrawOverlay`, `CanvasCommentPins` | Toolkit: `@agent-native/toolkit/canvas-annotations` | [Editors and Canvases](https://www.agent-native.com/docs/toolkit-editors-canvases.md) |
| Sharing and presence | `ShareButton`, `ShareDialog`, `VisibilityBadge`; `usePresence` | Toolkit: `@agent-native/toolkit/app/sharing`, `@agent-native/toolkit/sharing`; Core: `@agent-native/core/client/collab` | [Collaboration](https://www.agent-native.com/docs/toolkit-collaboration.md), [Component API](https://www.agent-native.com/docs/components.md) |
| Review, comments, history | Shared comments/review and history kits | Toolkit UI with Core-backed contracts; inspect kit ownership | [Comments](https://www.agent-native.com/docs/toolkit-comments-review.md), [History](https://www.agent-native.com/docs/toolkit-history.md) |
| Chat history | `ChatHistoryList`, `ChatHistoryRail` | Toolkit: `@agent-native/toolkit/chat-history` | [Agent UX](https://www.agent-native.com/docs/toolkit-agent-ux.md) |
| Agent and knowledge resources | `AgentTabsPage`, `ResourcesPanel`, `ResourceTree`, `ResourceEditor` | Toolkit: `@agent-native/toolkit/app/agent-page`, `@agent-native/toolkit/app/resources`; resource hooks in Core | [Resources](https://www.agent-native.com/docs/toolkit-resources.md), [Public UI](https://www.agent-native.com/docs/components.md#other-ui) |
| Background-work feedback | `NotificationsBell`, `RunsTray` | Toolkit: `@agent-native/toolkit/app/notifications`, `@agent-native/toolkit/app/progress`; run registry in Core | [Public UI](https://www.agent-native.com/docs/components.md#other-ui) |
| Setup and team surfaces | Setup/connections and organization kits | Shared Toolkit surfaces and Core services | [Setup](https://www.agent-native.com/docs/toolkit-setup-connections.md), [Organization](https://www.agent-native.com/docs/toolkit-org-team.md) |

For the remaining capability modules or operational UI, follow the
[Toolkit catalog](https://www.agent-native.com/docs/agent-native-toolkit.md).
These are optional capabilities, not dependencies every app must install.

## Ownership and customization

Apps own domain records, actions, routes, and product-specific workflows. Shared
workspace behavior should use its existing Toolkit surface when available.

For ordinary app controls, follow the app-local adapter convention, commonly
`@/components/ui/*`, instead of importing Toolkit primitives throughout domain
pages. Inspect the existing `ToolkitProvider` and design-system registration
before introducing a second provider or styling system. Reusable package code
can use public Toolkit primitives directly where its contract calls for them.

Prefer supported configuration, slots, and composition. If the feature needs
ownership of shared implementation, consult the installed customization guide
and supported ejection units. Keep package internals read-only and use public
exports instead of deep-importing private source.

Framework-wired composer and chat wrappers provide runtime services. Bare UI
requires explicit adapters/providers; confirm those obligations before swapping
layers. Context-picker selection and component visibility do not grant data
access; authenticated actions must recheck it.

## UI acceptance

Check pending, empty, failed, and successful outcomes using real action results.
Preserve accessible names, keyboard activation, overlay dismissal, and focus
restoration. Verify narrow screens and scrolling for changed shells. Keep app
branding and existing adapter seams rather than rebuilding shared behavior to
change appearance.
