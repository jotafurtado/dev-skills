# Architecture and feature boundaries

## Mental model

Agent-Native is the BuilderIO TypeScript framework, not a generic architecture
label. An agent and a human-facing UI operate on the same capabilities, SQL
records, and application context.

| Layer | Responsibility | Choose it when |
| --- | --- | --- |
| Core (`@agent-native/core`) | Runtime contracts: actions, data helpers, access, application state, agent runtime, sync | Every Agent-Native app needs the foundation; inspect the installed package for its exact seams. |
| Toolkit (`@agent-native/toolkit`) | Optional reusable UI and product capabilities wired to Core | The product needs shared chat, settings, editors, sharing, or other standard surfaces. |
| Templates | Optional app starting points built on Core, potentially using Toolkit | An existing domain app or the minimal Chat template matches the requested starting point. |

Toolkit and templates are independently optional. A template is app source to
adapt; Toolkit runtime implementation remains package-owned until deliberately
transferred through a supported customization seam.

## Shared operations

An action defines an operation once. Supported surfaces can expose it to the UI,
agent, HTTP, CLI, MCP, or A2A, subject to that version's exposure and access
configuration. Adding separate browser and agent implementations introduces
different validation, access checks, and effects. Prefer the shared action path
for app operations; protocol-specific routes still have legitimate uses.

Domain records use the app's PostgreSQL/Drizzle model. PGlite supports local
development; hosted PostgreSQL is the production path documented by the
framework. Inspect the app's database setup before changing schemas or migration
behavior. Reuse its existing migration mechanism.

Application context describes what the user is doing: current view, stable
record IDs, and semantic selection. Publish the context the agent needs through
framework application state. Local component state remains useful for purely
presentational interactions; it is insufficient as the only home of context the
agent must read.

## Find the feature's code

Inspect the generated app rather than imposing another React stack's layout.
Common template boundaries are `app/` for browser UI, `actions/` for shared
operations, `server/` for server infrastructure, and `.agents/skills/` for
workflow knowledge. Browser routes under `app/routes/` and Nitro server routes
under `server/routes/` are different systems. Confirm the template's React Router
configuration and route conventions before adding a page or treating a server
endpoint as a screen.

## Feature design

Start with one user operation, its typed action, and its access boundary. Add UI,
domain workflow instructions, and application context where the operation needs
them. An action-only automation does not require a browse screen. Conversely,
adding a screen without an agent-callable operation leaves an incomplete shared
workflow.

Instructions, skills, and actions solve different problems:

- App instructions carry stable identity, invariants, and navigation pointers.
- Skills teach reusable workflows and load when relevant.
- Actions implement callable operations, with input validation and effects.

For AI-assisted product operations needing tools or durable context, hand work
to the agent rather than adding an unrelated client-side model call. Use the
documented server-side text-completion escape hatch only when its narrower
contract actually fits.

## Official sources

- [What is Agent-Native?](https://www.agent-native.com/docs/what-is-agent-native.md)
- [Key Concepts](https://www.agent-native.com/docs/key-concepts.md)
- [Toolkit](https://www.agent-native.com/docs/agent-native-toolkit.md)
- [Getting Started](https://www.agent-native.com/docs/getting-started.md)
- [Templates](https://www.agent-native.com/docs/cloneable-saas.md)
- [Client Routing](https://www.agent-native.com/docs/client-routing.md)

Use the documentation lookup procedure in the main skill to confirm these
concepts against the target installation before adopting implementation details.
