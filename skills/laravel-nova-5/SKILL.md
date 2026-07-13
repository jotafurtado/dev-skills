---
name: laravel-nova-5
description: "Builds and reviews Laravel Nova 5 resources, fields, relationships, actions, filters, lenses, metrics, dashboards, policies, file fields, tools, cards, and menus. Use when the user explicitly mentions Laravel Nova or Nova APIs, or when the project is confirmed to require laravel/nova 5.x. Do not trigger from 'admin panel' or 'back-office' alone; Filament requests belong to a Filament-specific skill."
license: MIT
compatible_agents:
  - Claude Code
  - Cursor
  - Windsurf
  - Copilot
tags:
  - laravel
  - php
  - nova
  - backend
metadata:
  author: community
  version: "2.0.0"
  domain: backend
  nova_version: "5.x"
  laravel_version: "10.x-13.x"
  triggers: Laravel Nova, laravel/nova, Nova resource, Nova field, Nova action, Nova metric, Nova lens, Nova filter, Nova dashboard, Nova tool, Nova card
  role: specialist
  scope: implementation
  output-format: code
---

# Laravel Nova 5

Use official, version-matched Nova and Laravel APIs to implement or review Nova
features without inventing framework signatures.

## Gate: confirm the stack first

Before generating or changing Nova code:

1. Read the application's `composer.json`.
2. Read `composer.lock`, locate the `laravel/nova` package, and record its exact
   installed version.
3. Confirm the resolved package is Nova `5.x`; also record the installed Laravel
   and PHP constraints because supported syntax and framework APIs vary.
4. Inspect nearby Nova resources, the base `App\Nova\Resource`,
   `NovaServiceProvider`, policies, tests, and generated component scaffolds
   relevant to the task.

If either Composer file is unavailable, `laravel/nova` is absent, or the lockfile
does not resolve Nova 5, stop before producing Nova-specific code. Report the
evidence and ask whether to proceed with a different stack or first update the
dependencies.

An isolated request for an “admin panel”, “back-office”, generic CRUD, or a
Laravel authorization policy is not enough to activate this skill. If the code
uses `filament/filament`, Filament namespaces, Resources, schemas, or panels,
route the task to the Filament skill instead. If both products exist, scope work
to files and namespaces explicitly tied to Nova.

## Official documentation protocol

Treat documentation lookup as part of implementation, not an optional follow-up:

1. Fetch Nova's official index:
   <https://nova.laravel.com/docs/llms.txt>.
2. Select the relevant versioned page from that index and fetch its `/docs/v5/`
   Markdown URL before writing an API call.
3. For Laravel behavior, use the official Laravel documentation matching the
   installed framework major.
4. For skill authoring behavior, use the official Cursor Agent Skills guide:
   <https://cursor.com/docs/skills>.
5. Prefer the project's generated Nova stub and installed official package
   signature when it is more specific than prose documentation.

Never guess a class, namespace, method name, argument order, return type, policy
hook, Artisan command, or frontend scaffold. If the official v5 page and
installed package do not confirm it, omit it, label the uncertainty, or ask for
the missing evidence. Do not silently transpose APIs from Nova 4, Filament, or a
community package.

## Core constraints

- Preserve project conventions unless they conflict with confirmed Nova 5 APIs.
- Add imports to complete snippets. If context intentionally omits imports,
  label the snippet `// Fragment: imports and enclosing class omitted`.
- Match method signatures to the installed Nova 5 version. Do not force return
  types or modern PHP syntax when the inherited signature or project version
  makes them incompatible.
- Keep authorization server-side. UI visibility such as `canSee` complements,
  but does not replace, policies, gates, or route middleware.
- Define all policy methods relevant to the feature. Nova's undefined-method
  defaults are not uniformly permissive or restrictive.
- Match relationship labels, Eloquent method names, and related Nova resource
  classes deliberately; do not apply pluralization as an unconditional rule.
- Add eager loading only when a displayed title, subtitle, field, or query
  actually benefits from it; avoid creating unnecessary joins or memory use.
- Chain `->asBigInt()` on an `ID` field only for identifiers too large for safe
  client-side rendering.
- Queue actions when workload and delivery semantics justify it. Confirm queue
  workers and remember that queued actions cannot contain `File` fields.
- Run `storage:link` only for a local `public` disk that needs the conventional
  `public/storage` link.
- Start custom fields, cards, filters, and tools from Nova's generated scaffold.
  Keep its build stack unless the installed scaffold and v5 docs support a
  migration.
- Avoid broad polling, eager loading, custom assets, or expensive metric queries
  without considering page cost and the application's scale.
- Do not edit vendor code or expose Nova source in public distributions.

## Route to one-level references

Read only the references needed for the current task, but read each selected file
fully before implementing:

- [Resources](references/resources.md): resource definition, display,
  panels/tabs, validation, polling, soft deletes.
- [Fields](references/fields.md): built-in, computed, dependent, and repeater
  fields.
- [Relationships](references/relationships.md): relationship fields, pivot
  fields/actions, inline creation, relatable queries.
- [Authorization](references/authorization.md): access gate, policy defaults,
  Nova-specific policies, relationships, fields, queries.
- [Files](references/files.md): disks, metadata, storage/deletion callbacks,
  previews, downloads, validation.
- [Actions, filters, and lenses](references/actions-and-filters.md): execution,
  responses, queues, registration, query contracts.
- [Metrics and dashboards](references/metrics-and-dashboards.md): metric result
  types, registration, dashboard naming and authorization.
- [Customization](references/customization.md): tools, cards, custom fields,
  menus, notifications, localization, assets.
- [Testing](references/testing.md): proportional tests and official Laravel
  runners without fabricated Nova testing helpers.

## Implementation workflow

1. Confirm the stack gate and existing local conventions.
2. Fetch the exact official v5 pages for the requested topic.
3. Read the matching references above.
4. Make the smallest compatible change, including imports and authorization.
5. Format with the project's existing formatter.
6. Run the narrowest relevant tests first, then expand based on risk.
7. Re-read changed code for undocumented Nova APIs and report any behavior that
   still requires browser or integration verification.

## Verification expectations

At minimum, verify PHP syntax and the project's targeted test or static-analysis
command when available. For authorization, exercise allowed and denied paths.
For persistence, cover create/update validation and model effects. For actions,
filters, metrics, files, or custom frontend packages, add deeper integration or
browser checks only when the change's risk warrants them. See
[Testing](references/testing.md).
