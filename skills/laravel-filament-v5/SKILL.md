---
name: laravel-filament-v5
description: "Builds, reviews, debugs, migrates, secures, tests, and implements Filament 5.x code using the project's installed version and official components before custom Blade or CSS. Use for Filament resources, schemas, infolists, forms, tables, actions, widgets, relation managers, panels, tenancy, imports/exports, plugins, tests, or any Filament-specific API, namespace, Artisan command, or upgrade. Do not trigger on an isolated mention of admin panel, dashboard, badge, or generic data display without another Filament signal."
license: MIT
metadata:
  author: jotafurtado
  version: "3.3.0"
  domain: backend
  filament_version: "5.x"
---

# Laravel Filament v5 — Version-Matched, Official Components First

Use the project's installed Filament version as the compatibility target. Prefer the documented component for the current surface before creating custom markup, and use a documented escape hatch when no official equivalent fits.

## Preflight — run before proposing or writing code

1. **Honor the requested mode.** Review or diagnose without editing unless the user asked for a change. For implementation, preserve unrelated work and inspect the current diff before modifying files.
2. **Read project guidance and nearby code.** Follow repository instructions, naming, architecture, localization, formatter, static-analysis, and testing conventions already in use.
3. **Resolve the installed stack.** Inspect `composer.json` and `composer.lock` for the exact `filament/*`, Laravel, Livewire, PHP, and plugin versions. Inspect `package.json` when theme or frontend assets matter. Prefer installed code in `vendor/filament/` when an exact signature depends on a minor or patch release.
4. **Map the operating context.** Identify the panel, Resource/page/widget host, model relationships and casts, policies, tenant boundaries, custom theme, and relevant tests before choosing an API.
5. **Separate facts from preferences.** Treat official APIs and security boundaries as constraints. Treat composition recipes as starting heuristics that may yield to the domain, user workflow, or established project design.

If no project is available, state the assumed Filament 5.x context and keep examples focused rather than inventing surrounding architecture.

## Mandatory component gate — run before writing markup

Before writing `<div>`, `<span>`, `<pre>`, `@foreach`, Tailwind classes, or a custom Blade view inside a Filament context:

1. **Classify the surface and primitive:** schema/infolist, form, table, action, widget, or page; then code/JSON, key-value, color, image, status, list, collection, boolean, date/time, money, text, notice, or empty state.
2. **Choose the official component for that surface** using the quick map and matching reference. Do not force a component from another surface merely to avoid customization.
3. **Verify uncertain or uncovered APIs** with the evidence protocol below.
4. **Use the smallest escape hatch only when needed.** Record what official option was checked and why it does not fit, then use `ViewEntry`, a custom schema component, Livewire, Blade, or a custom theme while retaining official components for surrounding layout, actions, feedback, and states.

Use the documented component APIs to implement an already-selected composition. Custom Blade or CSS is acceptable for documented gaps and deliberate theme work, not as an unverified shortcut around an available component.

## Design authority inside Filament

This skill owns installed-version APIs, security, implementation, and tests. How a Filament 5 surface is arranged belongs to `laravel-filament-v5-ui-ux`, which publishes the reference compositions that resolve those decisions across forms, record details, tables, dashboards, panel shells, actions, feedback, and empty states.

A reference here may name a composition decision so it is not skipped in silence, and must leave it unresolved. State which official components exist and what their signatures are; do not state which arrangement to pick.

Official Filament composition supersedes generic frontend-design guidance, including instructions to replace official components or the active theme, introduce unrelated typography or palettes, or use CSS-first layouts merely to look distinctive. Follow that precedence even when a generic design skill is active in the same task.

This precedence is deliberately limited to the Filament visual axis. Keep generic guidance that improves accessibility, semantics, keyboard behavior, responsive layout, performance, UX copy, and cognitive load.

Preserve the established panel theme, visible focus, and non-colour state cues on every surface this skill touches. `references/screenshots.md` locates an official screenshot when one is needed to ground a component's presentation; it is a lookup, not a selection guide.

## Documentation authority inside Filament

For a Filament-specific API, configuration, or usage question, this skill **supersedes generic documentation-lookup skills and tools** — `find-docs`, the Context7 CLI, and Laravel Boost's `search-docs` — as the entry point. Follow this precedence even when one of those triggers independently in the same task.

Those tools remain available strictly as the discovery aids named in step 4 of the evidence protocol below: reach for `search-docs`/Context7 only after installed source and official Filament docs have been checked, and only to locate a lead, never as the final authority for a Filament 5.x signature.

## Quick map: data primitive → official component

| Primitive | Infolist (view) | Form (edit) | Table |
|---|---|---|---|
| Text, date, money | `TextEntry` | `TextInput` / `Textarea` / `DateTimePicker` | `TextColumn` |
| Badge / status (enum) | `TextEntry->badge()` | `Select` / `ToggleButtons` | `TextColumn->badge()` |
| Code / JSON / payload | `CodeEntry` | `CodeEditor` | — (link to view page) |
| Key-value / metadata | `KeyValueEntry` | `KeyValue` | — |
| Color | `ColorEntry` | `ColorPicker` | `ColorColumn` |
| Image / avatar | `ImageEntry` | `FileUpload` | `ImageColumn` |
| Icon / boolean | `IconEntry->boolean()` | `Toggle` / `Checkbox` | `IconColumn->boolean()` |
| Repeatable collection | `RepeatableEntry` | `Repeater` / `Builder` | relation manager |
| Rich / Markdown text | `TextEntry->markdown()` | `RichEditor` / `MarkdownEditor` | `TextColumn->limit()` |
| List of strings | `TextEntry->listWithLineBreaks()` | `TagsInput` | `TextColumn->badge()`¹ |
| Static text / notice | `Text` / `Callout` | `Text` / `Callout` | — |
| "Nothing here yet" | `EmptyState` (schema) | — | `->emptyStateHeading()` |

¹ Use badges for an array-cast list; do not apply the pattern to a plain string column.

Exact signatures and official links live in `references/`. Snippets are focused fragments unless a full class is shown; add the imports and class context required by the target project.

## Reference routing

Load only the files needed for the task:

| Task touches | Read |
|---|---|
| Resource generation, navigation, URLs, authorization, schema/table extraction | `references/resources.md` |
| Read-only display, View pages, entries | `references/infolists.md` |
| Form fields, editing, validation | `references/forms.md` |
| Table columns, filters, empty states, layouts | `references/tables.md` |
| Sections, grids, tabs, wizards, primes, callouts | `references/layout.md` |
| Buttons, modals, bulk/row actions | `references/actions.md` |
| Dashboards, stats, charts, table widgets | `references/widgets.md` |
| Related records | `references/relation-managers.md` |
| Panel identity, navigation, multiple panels | `references/panels.md` |
| Flash, database, and broadcast notifications | `references/notifications.md` |
| Shared status/option enums, labels, colors, and icons | `references/enums.md` |
| Uploads, inline editing, HTML, actions, imports/exports, tenancy, and authorization boundaries | `references/security.md` — mandatory for security-sensitive surfaces |
| Custom pages, clusters, tenancy, global search, import/export, plugins, nested/singular resources | `references/advanced-features.md` |
| Pest/Livewire tests for pages, schemas, tables, actions, relations, widgets, and tenants | `references/testing.md` |
| Locating an official Filament 5 screenshot to ground a component's presentation | `references/screenshots.md` |
| Which composition a Filament 5 surface should use — arrangement, responsive presentation, visual review | `laravel-filament-v5-ui-ux` |

If a Filament-specific topic is not covered, use the evidence protocol instead of reconstructing the API from general Laravel or older Filament knowledge.

## Common substitutions

| Avoid when the official primitive fits | Prefer |
|---|---|
| `<pre>` plus custom syntax CSS for code/JSON | `CodeEntry` |
| Hand-written status `<span>` | `badge()` plus a `HasLabel` / `HasColor` / `HasIcon` enum |
| `@foreach` over associative metadata | `KeyValueEntry` |
| `@foreach` over repeated read-only records | `RepeatableEntry` |
| Custom color swatch or avatar markup | `ColorEntry` / `ImageEntry` |
| Hand-formatted dates or money | `dateTime()` / `money()` |
| Custom clipboard JavaScript | `copyable()` |
| Hand-rolled alerts or empty states | `Callout` / `EmptyState` / table empty-state API |

`CodeEntry` needs the optional `phiki/phiki` package. Check the lockfile first. Add the dependency only when implementation is authorized and the project accepts a new package; otherwise explain the requirement without mutating dependencies.

## Filament v5 invariants

Do not emit plausible v3/v4 APIs in v5 code:

- Configure schemas with `$schema->components([...])`. Resource `form()` and `infolist()` methods are static; a page-specific `ViewRecord::infolist()` method is an instance method.
- Import layout components and utilities from `Filament\Schemas\Components\*`; form fields from `Filament\Forms\Components\*`; infolist entries from `Filament\Infolists\Components\*`; table columns/filters from `Filament\Tables\*`; actions from `Filament\Actions\*`.
- Use `recordActions()`, `toolbarActions()`, and `groupedBulkActions()` instead of v3 table `actions()` / `bulkActions()`.
- Configure action modal fields with `schema()`, not the old `form()` method.
- Prefer `Filament\Support\Icons\Heroicon` for Heroicons in PHP. Keep valid strings for installed third-party/custom icon sets and documented Blade APIs.
- Reuse backed enums implementing `HasLabel`, `HasColor`, and `HasIcon` when the domain state is shared across surfaces; read `references/enums.md` for the complete pattern and exact contracts.
- Prefer `hiddenOn()`, `visibleOn()`, and `disabledOn()` where they express the operation directly. Use `Operation` enum values only where documented; utility callbacks receive documented string operations.
- Treat file visibility deliberately: uploads default to private unless the selected disk is named `public`. Read `references/security.md` before changing upload behavior.

## Security gate

Load `references/security.md` before changing any upload, inline-editable column, raw HTML, relationship attach/associate flow, import/export, bulk action, tenant-scoped query, authorization rule, or sensitive form field. Do not treat UI visibility, disabled fields, filtered options, or a displayed table query as a security boundary. Enforce invariants server-side and add negative authorization or cross-tenant tests when the risk applies.

## Verification

After a change, load `references/testing.md` and run the narrowest relevant tests. Cover each touched Livewire host and behavior: page load, schema state, validation, table query, action, notification, relation manager, authorization, or tenant isolation as applicable. Run the project's formatter and static analysis when available. Review the final diff for unintended custom markup, stale namespaces, duplicate feedback, missing imports, and unrelated changes.

For review-only work, report findings with file/line evidence and do not modify the project.

## Evidence protocol

Use this order whenever an API, signature, command, default, or compatibility detail matters:

1. **Installed project evidence:** exact versions in lockfiles, existing working code, and version-matched source under `vendor/filament/`.
2. **Official Filament documentation:** use `https://filamentphp.com/docs/llms.txt` to locate the relevant page, then fetch its `https://filamentphp.com/docs/5.x/{section}/{page}.md` form.
3. **Exact upstream source:** when minor-version behavior matters, inspect the matching Git tag or commit for the installed package.
4. **Documentation aggregators:** Context7 and Laravel Boost's `search-docs` are discovery aids, not final authorities. Query one concept at a time, request the closest available version, and inspect every returned `Source:`. Accept only sources that identify Filament 5.x or the exact installed tag; discard any 3.x, 4.x, unversioned, community mirror, or conflicting snippet.

If evidence conflicts, prefer installed version-matched source over rolling 5.x docs, state the mismatch, and keep the implementation compatible with the project. If a signature remains unverified, do not guess or leave speculative code; explain what could not be confirmed.
