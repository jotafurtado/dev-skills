---
name: agent-native
description: "Build, extend, review, and debug Agent-Native apps using @agent-native/core and @agent-native/toolkit. Use for shared actions, SQL data, agent-visible application context, real-time or cross-tab synchronization, chat surfaces, or Toolkit component selection in a confirmed Agent-Native project, and when explicitly starting an app with this framework. Do not trigger for React Native; generic AI agents; unrelated React UI; or general discussions of agent-native architecture without this framework."
license: MIT
metadata:
  author: jotafurtado
  version: "1.0.0"
---

# Agent-Native

Build one capability that the person and the agent can both use. Keep its
validation, authorization, data, and effects on the same action path.

## 1. Establish the app and its version

For an existing app, read its instructions, package manifest, lockfile, relevant
source, and local skills. Resolve the installed Core and Toolkit versions;
workspace manifests may own dependencies instead of the current directory.
Distinguish package constraints from resolved versions.

For a new app, use the official Getting Started or template guide to choose a
starting point that fits the request. Verify its current prerequisites and CLI
options before scaffolding. Keep the generated dependency pins and conventions.

Completion: identify the app/template and resolved versions. If installation
evidence is missing, explicitly state in the answer that API compatibility is
unverified and name the installed docs/types needed before implementation.
Architecture planning can continue; present API names only as discovery leads.

## 2. Resolve only the knowledge this task needs

Read relevant project skills when present, especially `agent-native-docs`,
`actions`, `storing-data`, `real-time-sync`, `context-awareness`,
`agent-native-toolkit`, and `customizing-agent-native`. Their availability varies
by template. Use them as version-local guidance rather than installing duplicate
copies of them.

Read selected references fully before using their guidance:

- [Architecture](references/architecture.md): choosing Core, Toolkit, or a template; creating an app or mapping a feature across its layers.
- [Actions and data](references/actions-data.md): defining actions, querying SQL, mutations, authorization, and shared UI/agent operations.
- [UI and Toolkit](references/ui-toolkit.md): choosing chat components, controls, editors, collaboration, navigation, settings, and feedback; customizing existing UI.
- [Context and sync](references/context-sync.md): navigation, selection, agent handoffs, stale screens, background updates, and refetch jitter.
- [Documentation](references/documentation.md): finding version-matched APIs, checking imports, unavailable docs, or routing to advanced topics.

Use installed documentation and public types/source to verify every non-trivial
API used in the change. The local catalog is a discovery map, not proof that an
export exists in the target version. When sources conflict, use the installed
contract and identify the discrepancy. Do not replace missing evidence with a
guessed signature.

Completion: locate a matching definition/example for each API being introduced,
or name the unresolved API and stop only the dependent implementation.

## 3. Implement a shared feature

For each feature, account for the applicable areas:

| Area | Completion evidence |
| --- | --- |
| UI | The requested user flow uses existing app conventions and handles pending, empty, failure, and success states where applicable. |
| Action | UI and agent reach the same typed operation through supported invocation surfaces, with server-side access checks. |
| Instructions | New domain behavior is discoverable through the action description and, when a reusable workflow needs it, app instructions or a focused skill. |
| App context | The agent can resolve the relevant route, record, or selection and navigate to the result when the feature needs it. |

Mark an area inapplicable with a reason rather than inventing a screen or skill
for every operation. Retain app-owned domain models and workflows; adopt shared
Toolkit behavior where it fits. Configure, compose, or use a supported narrow
ejection before reimplementing runtime internals. Inspect package source as
read-only evidence and import supported public exports at runtime.

Use the agent chat bridge for work needing tools, context, steering, or multiple
steps. For a true text-in/text-out operation, consult the installed Component
API's server-side completion escape hatch and expose user-facing usage through
an action. Keep provider credentials on the server.

Completion: trace the requested operation from UI or agent entry through access
checks and data/effects to its visible result. Identify any missing area.

## 4. Verify the behavior

Separate observed symptoms, suspected causes, installed API evidence, and
executed behavior. Keep a cause hypothetical until a trace or test establishes
it. Handler tests with mocked context or transport do not verify framework
dispatch, session propagation, chat streaming, or browser synchronization.

Use the target app's scripts and tests, not assumed command names. For changed
operations, check valid/invalid inputs, allowed/denied callers, and relevant
ownership or organization boundaries. Verify UI calls and agent/tool calls reach
the same contract; report when the tool path cannot be exercised locally.

For UI or context changes, check route transitions, selection cleanup, agent
handoffs, and update visibility from every changed entry point. Test a second
tab or user only when remote updates are part of the requirement. Check keyboard
and focus behavior for changed interactive components.

Completion: report changes, API sources and version, checks actually run, and
remaining limitations. A documented example or proposed test is not an executed
integration test.
