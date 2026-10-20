# Candidate implementation

Implemented in `candidate` only. No dependency pins changed, no production build, commit, or deployment performed.

## Result

- `/tasks` offers private task listing, creation, completion, an opened-task detail, loading/empty/error/success feedback, keyboard links and controls, focus on opened details and restoration to the creation field, and wrapping mobile layouts.
- `list-tasks`, `create-task`, and `complete-task` share the action contract between UI and agent. SQL/Drizzle persistence includes a named additive migration and owner/creation index.
- Identity comes only from server-resolved `ActionRunContext.userEmail`; missing identity fails 401. Lists, lookups, and updates filter `owner_email`; unavailable IDs fail uniformly with 404. Creation rejects injected ownership fields. Task sharing is intentionally absent because the requirement is owner-only.
- Existing persistent layout/chat runtime retained. The existing `useAgentRouteState` consumes one navigation channel, with framework duplicate protection and consumption. Task URL IDs populate semantic navigation and tab-scoped selection. Route changes delete obsolete selection. `view-screen` resolves IDs through owner-scoped reads and excludes task selection outside the tasks view.
- `navigate` checks task ownership before emitting a task command, rejects non-local paths, and uses a single `_writeId` command. Task actions are in the plugin's starter tool set and AGENTS action table.
- Action hooks supply local UI/agent write refresh. Tasks opt into supported shared `useDbSync` for changes originating from a second session of the same owner, with hidden-tab pause and no custom event stream/polling.
- Existing local Button/Input adapters and i18n catalogs reused. New domain UI text remains pt-BR across configured catalogs as requested.

## API evidence

Installed Core and Toolkit versions inspected: **0.209.2**. Manifest Core constraint is exact; Toolkit resolved version verified separately.

- `defineAction`, optional `ActionRunContext.userEmail`, `fail`, strict schema dispatch: Core `dist/action.d.ts`, `dist/action.js`, and installed `docs/content/actions-run-context.mdx`, `actions-access-control.mdx`.
- `createGetDb`, `runMigrations`, named migration entries: Core public `db` export, `dist/db/create-get-db.d.ts`, `dist/db/migrations.d.ts`, and `docs/content/server-database.mdx`.
- PostgreSQL table/column/index DSL, `select/insert/update/returning`, `and/eq/desc`: installed Drizzle package types and existing installed framework Database examples. Queries are Drizzle; only migration DDL is SQL text.
- `useActionQuery`, invocation arguments for `useActionMutation`, `actionErrorMessage`: Core public `client/hooks` export; `dist/client/use-action.d.ts`. Local invalidation checked in `use-action.js` (`['action']` invalidation on mutation).
- `useDbSync` opt-in `{ realtime: { reason }, ignoreSource, pauseWhenHidden }`: `dist/client/use-db-sync.d.ts`, installed local real-time-sync skill, and client Data & Sync docs. Default action change events reach the actor, which covers another session of that same owner.
- `useAgentRouteState`, callback locations and `navigateOptions`, `agentChatViewTransition`: public `client/navigation` export and `dist/client/route-state.d.ts/js`. Kept the existing TAB_ID.
- `writeClientAppState`/`deleteClientAppState` options and tab-suffixed keys: public hooks export and `dist/client/application-state.d.ts`; `readAppStateForCurrentTab`/`writeAppStateForCurrentTab` verified in public application-state exports.
- Action `link` metadata and `buildDeepLink`: `dist/action.d.ts`, public server export, `dist/server/deep-link.d.ts/js`. Links carry an explicit `to` task route.
- React Router route discovery, search params, Link and route layout follow the existing scaffold and installed types. Existing app-local Button/Input exports forward the installed Toolkit contracts. `useT` and configured catalog structure follow the existing app.

## Verification performed

- Initial `NODE_ENV=development pnpm typecheck`: exit 0. Repeated after links/i18n integration: exit 0.
- `NODE_ENV=development pnpm agent-native:doctor`: clean, no findings.
- Initial three PGlite-backed Vitest tests passed: anonymous list/create/complete rejection; real schema title bounds and owner-field injection rejection; frontend/tool action persistence, cross-owner list/update denial, and idempotent completion.
- Added a fourth test for authorized navigation, authorized opened-task/selection resolution, anonymous context rejection, and suppressing stale selection outside tasks. Its run was interrupted by the parent replacing the dependency symlink: `vitest: command not found`. This is unexecuted, not a passing check. Parent must rerun the final tests after installation.
- No production build or browser smoke performed by this worker, per parent assignment. Parent owns authenticated HTTP/tool dispatch, UI interactions, narrow-screen rendering, shell continuity, command once-only behavior, route selection cleanup, and same-owner second-session delivery verification. Handler tests use real PGlite and mocked app-state storage; they do not prove the framework dispatcher or transport.

## Changed files

`AGENTS.md`; `actions/{list-tasks,create-task,complete-task,navigate,view-screen}.ts`; `server/db/{schema,index,task-store}.ts`; `server/plugins/{db,agent-chat}.ts`; `app/routes/tasks.tsx`; `app/hooks/use-navigation-state.ts`; `app/components/layout/Sidebar.tsx`; all existing locale message catalogs under `app/i18n/` (tasks namespace); `tests/tasks.test.ts`.

No further implementation edits after this evidence file; parent can snapshot candidate.
