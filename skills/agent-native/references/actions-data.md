# Actions, data, and authorization

## Define an operation

The documented action entry point is `defineAction` from
`@agent-native/core/action`. An action file in `actions/` default-exports its
definition. The framework discovers action files; inspect the generated app
before introducing a registry or custom endpoint.

The definition combines an agent-facing description, an input schema, and a
`run` implementation. Describe intent and meaningful input fields so the agent
can select the operation. Reuse the app's supported schema library and database
helpers. Keep input and result types precise; validate at the action boundary
instead of trusting the caller.

For a read, a write, or an operation with external effects, verify the installed
HTTP/read-only contract. A read-only setting is not authorization. In the
current docs, GET enables query-hook calls; changing an action's HTTP path can
break standard action hooks that still address its file-derived name. Confirm
the target release before changing either option.

Invoke actions through the supported caller surface. Importing another action's
`run` directly skips the shared validation/access/audit seam. Extract app-owned
domain logic if internal code reuse is necessary, while retaining the action
boundary for externally initiated operations.

## Connect the UI

The documented client entry is `@agent-native/core/client/hooks`:

| API | Purpose | Detail to confirm in the installed types |
| --- | --- | --- |
| `useActionQuery` | Query an action and render its result | Action name, arguments, query options, loading/error state |
| `useActionMutation` | Run an operation after a user event | Hook configuration versus input passed to `mutate`/`mutateAsync` |
| `callAction` | Invoke an action outside a hook | Caller context, result and error types |

Read the action and its actual result before designing the UI. A mutation's
arguments belong to its invocation, not an assumed query-style hook argument.
Preserve structured action errors rather than replacing failures with success
notifications. Use the installed sync mechanism before adding manual cache
invalidation or polling.

## Enforce access at the server

Separate discoverability from authorization. Exposure options such as
`agentTool`, `mcpTool`, and `toolCallable` select calling surfaces; they do not
prove the caller may read or mutate a particular record.

Use the installed action context and access helpers to enforce actor, ownership,
organization, and sharing boundaries. Derive trusted identity server-side rather
than accepting an arbitrary owner ID from an input schema. Scope lists and
lookups as well as writes. Resolve referenced records under the same access
rules even when their IDs arrived from a selection or chat context.

Read the target version's authorization docs before choosing `access`,
`authorize`, `accessFilter`, or `assertAccess`; their roles and signatures are
not interchangeable. UI visibility complements these checks.

## Persist and verify

Keep domain data in the app's SQL schema and use its Drizzle/database conventions.
Inspect existing schema definitions, migration tooling, and transaction patterns.
Secrets belong in server-managed credential/configuration facilities, not in
browser state, action results, or agent-visible context.

For a changed operation, cover schema rejection, an allowed caller, a denied
caller, and cross-owner/organization access when applicable. Check both the UI
invocation and agent/tool path. Confirm the resulting record and UI refresh;
successful transport alone does not prove the product operation succeeded.

## Official sources

- [Actions Overview](https://www.agent-native.com/docs/actions-overview.md)
- [Defining Actions](https://www.agent-native.com/docs/actions-defining.md)
- [Run Context](https://www.agent-native.com/docs/actions-run-context.md)
- [Access and Authorization](https://www.agent-native.com/docs/actions-access-control.md)
- [Data and Sync](https://www.agent-native.com/docs/client-data.md)
- [Database](https://www.agent-native.com/docs/server-database.md)
- [Security](https://www.agent-native.com/docs/security.md)
