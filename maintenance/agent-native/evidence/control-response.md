# Control implementation evidence

Implementation is confined to `control/`. No other variant or parent skill was read. Local app AGENTS.md and official local guides were consulted, followed by installed Core/Toolkit docs and declarations at version 0.209.2. Dependencies and pins were not changed.

## Delivered

- `/tasks` creates private SQL tasks, opens a selected task via `?taskId=`, and sets explicit completion state through shared actions.
- PostgreSQL Drizzle schema, owner/creation index, lazy database client, and named additive framework migration.
- `list-tasks`, `create-task`, `complete-task`, `view-screen` and `navigate` derive identity solely from the trusted action execution context. Missing identity returns 401; owner predicates protect every task read/update. Unknown/foreign task IDs return the same 404.
- UI uses existing local Button/Input/Label controls, loading/empty/error/retry/pending/success feedback, wrapping narrow layout, keyboard controls, visible focus and focused opened task.
- Navigation is semantic and tab scoped; open task ID is published. Selection publishes only id/title and is deleted on close/unmount. Fresh screen reads validate both open and selected task ownership and omit obsolete task state off the tasks route.
- Navigation emits one `_writeId` command and uses the existing `useAgentRouteState` consumer, which deduplicates and deletes it. No second navigation transport was introduced. Existing root chat layout/runtime preserved.
- Action queries/mutations provide local and agent refresh. Supported `useDbSync` opts in solely on private `/tasks` for same-owner second-session updates. Default actor-scoped action event delivery is appropriate because tasks have no collaborators.
- Primary tools registered in existing `INITIAL_TOOL_NAMES`; task workflow/action table added to app instructions.

## API evidence inspected

- Core `dist/action.d.ts`: `ActionRunContext.userEmail`, `caller`, `run` context, `fail` status/errorCode, `retrySafe`, receipts and pure navigable result `urlPath` contract; app local actions guides.
- Core `docs/content/server-database.mdx`, `dist/db/create-get-db.d.ts`, `dist/db/migrations.d.ts`: `createGetDb(schema)` and `runMigrations(entries, { table })`, stable migration name.
- Core `dist/application-state/script-helpers.d.ts`: current-tab reads with `fallbackToGlobal: false`, current-tab command writes.
- Core `dist/client/route-state.d.ts`: route-state generics, `navigateOptions`, `agentChatViewTransition`.
- Core `dist/client/use-action.d.ts`: inferred action hooks, mutation invalidation and actionErrorMessage.
- Core `dist/client/application-state.d.ts` and `dist/client/use-db-sync.d.ts`: tab selection cleanup including keepalive; route-gated realtime reason.
- Existing app component shims and design-system registration; installed Toolkit UI contracts are checked through TypeScript.

## Verification completed

- `NODE_ENV=development pnpm typecheck`: passed after implementation.
- `NODE_ENV=development pnpm agent-native:doctor`: clean, all guards including ownership/identity/migrations.
- `NODE_ENV=development pnpm test`: 4 tests passed against a real temporary PGlite database using Drizzle and shared actions. Tests cover anonymous list/create/update denial, input validation, owner list isolation, foreign completion/read/navigation denial, exactly one command emitted for authorized task navigation, explicit completion/reopening, and subsequent same-owner action reads.
- `git diff --check`: clean (fixture is ignored by enclosing repo, so changed files were also inspected directly).

## Limits

Browser/runtime checks, actual one-shot command consumption, active chat continuity and transport delivery to a second browser session remain for parent verification. Automated tests verify the SQL/action boundary and command emission, not a browser or the production hosted sync transport. Server migrations follow the starter's boot/release contract; first-request startup race was not exercised. UI copy is intentionally pt-BR; existing app locale catalogs and unrelated copy were preserved. No production build, commit or deploy was performed by this agent.

## Changed files

`AGENTS.md`; `actions/{list-tasks,create-task,complete-task,navigate,view-screen}.ts`; `server/db/{schema,index,tasks}.ts`; `server/plugins/{db,agent-chat}.ts`; `app/routes/tasks.tsx`; `app/hooks/use-navigation-state.ts`; `app/root.tsx`; `app/components/layout/Sidebar.tsx`; `tests/tasks.test.ts`.
