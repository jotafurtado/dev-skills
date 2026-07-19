# Advanced Filament features — decision and documentation router

Use this file to choose the correct Filament surface for features that do not belong in the day-to-day component inventories. Resolve the installed Filament and plugin versions first, then fetch the linked official page before writing API-specific code.

## Custom pages

Use a custom page when the workflow is panel-native but does not map cleanly to CRUD for one model. A custom page is a Livewire component and may use schemas, actions, widgets, and an optional Blade view. Prefer a Resource page when record routing, authorization, global search, and CRUD lifecycle already match the problem.

Before generating a page, inspect the target panel and existing page namespace. Confirm the exact generator options with `php artisan make:filament-page --help` for the installed version.

Official reference: [Custom pages](https://filamentphp.com/docs/5.x/navigation/custom-pages.md)

## Navigation groups, clusters, and record sub-navigation

Choose the smallest navigation structure that matches scope:

- navigation group: visual grouping in one panel menu;
- cluster: a domain-level group of Resources/pages with its own sub-navigation and route structure;
- record sub-navigation: pages that operate on the same Resource record;
- separate panel: a distinct audience, authentication boundary, path/domain, or operational product.

Do not introduce a cluster merely to reduce a long sidebar; confirm that the grouped pages form a durable domain. Preserve existing URLs or plan redirects when moving Resources into a cluster.

Official references: [Navigation](https://filamentphp.com/docs/5.x/navigation/overview.md) · [Clusters](https://filamentphp.com/docs/5.x/navigation/clusters.md) · [Resource sub-navigation](https://filamentphp.com/docs/5.x/resources/overview.md#resource-sub-navigation)

## Global search

Set a Resource record-title attribute before adding searchable attributes. Confirm that the Resource has a View or Edit destination, that result queries obey policy and tenant scope, and that relationship searches do not introduce avoidable query cost. Return safe display values and URLs.

Official reference: [Global search](https://filamentphp.com/docs/5.x/resources/global-search.md)

## Imports and exports

Use Filament's `ImportAction` / `ExportAction` family before building ad hoc CSV flows. Read `references/security.md`, then inspect the required generated classes, migrations, queue configuration, storage, authorization, retry/failure behavior, and notification channel for the installed version.

Treat imported files and cells as untrusted input. Imports do not automatically perform per-record policy checks, and exports do not automatically filter every record through a policy; add the documented lifecycle authorization or query scoping. Address sensitive failed-row logging and spreadsheet-formula injection. Test validation failures, download access, authorization, tenant isolation, and a representative queued run rather than only testing that a button renders.

Official references: [Import action](https://filamentphp.com/docs/5.x/actions/import.md) · [Export action](https://filamentphp.com/docs/5.x/actions/export.md)

## Multi-tenancy

Read `references/security.md` first. Decide whether the project needs Filament's many-to-many tenant switching or a simpler application-level one-to-many scope. Verify user tenant access, automatic Resource scoping, ownership relationships, creation association, validation scope, custom queries, jobs, middleware, and cross-tenant tests.

Official reference: [Multi-tenancy](https://filamentphp.com/docs/5.x/users/tenancy.md)

## Nested, related, and singular workflows

- Use a relation manager when related records need inline table/form management on an owner View/Edit page.
- Use `ManageRelatedRecords` when related management deserves a dedicated Resource page and record sub-navigation.
- Use nested Resources when the child lifecycle and URLs should remain explicitly under a parent; verify route and query scoping carefully.
- Use a singular custom-page form for one logical record such as site settings or a homepage. Check whether an official/profile or maintained settings plugin already solves the case.

Official references: [Managing relationships](https://filamentphp.com/docs/5.x/resources/managing-relationships.md) · [Nested resources](https://filamentphp.com/docs/5.x/resources/nesting.md) · [Singular resources](https://filamentphp.com/docs/5.x/resources/singular.md)

## Plugins

Treat each plugin as its own versioned dependency. Inspect `composer.lock`, the plugin's official documentation and compatibility table, its registered panel configuration, migrations/assets, and tests. Do not infer a plugin's v5 API from its v3/v4 examples. Prefer first-party Filament functionality when it already covers the requirement, but do not replace an established, working project plugin without a migration reason.

## Finish the workflow

For every advanced feature:

1. verify the installed API and generator options;
2. identify authorization, tenancy, queue, storage, and navigation effects;
3. preserve established project structure;
4. test the actual Livewire/queued/security behavior;
5. document any operational setup the user must complete.
