# Laravel Filament v5

AI agent skill for building, reviewing, debugging, migrating, securing, testing, and designing Filament 5.x code. It resolves the project's installed version first, checks the official component for the current surface before custom Blade/CSS, and treats authorization and tenant isolation as server-side boundaries.

## Install

```bash
npx skills add jotafurtado/dev-skills --skill laravel-filament-v5
```

Or with Laravel Boost:

```bash
php artisan boost:add-skill jotafurtado/dev-skills --skill laravel-filament-v5
```

## What's Covered

- Mandatory gate: classify the data primitive before writing custom markup
- Preflight: inspect project guidance, lockfiles, installed source, panel/tenant context, policies, theme, and tests before choosing an API
- Quick map from data primitive → official component across infolist / form / table
- Documented escape hatch when no component exists on the correct surface
- Concrete substitutions (e.g. `<pre>` + CSS → `CodeEntry`, `<span>` + Tailwind → `badge()` + `HasColor` enum)
- v5 API breaking changes vs v3/v4 (`Schema`, namespaces, `recordActions()`, `Filament\Actions\*`, etc.)
- On-demand reference library for resources, infolists, forms, tables, layouts, actions, widgets, relation managers, panels, notifications, enums, advanced features, security, and testing
- Security guardrails for custom actions, inline editing, relationship selection, uploads, HTML/URLs, imports/exports, sensitive Livewire state, tenancy, and cross-tenant tests
- UI composition guide: adaptable page recipes, Filament-aligned defaults, visual hierarchy, Sections vs Tabs vs Wizard, column widths, scannable tables, empty states, modals, and feedback
- Official screenshot index: URL formula + curated map of docs screenshots so vision-capable agents view the real surface before composing
- Filament-specific visual authority that supersedes generic CSS-first guidance while retaining accessibility, responsive, performance, and UX requirements
- Evidence protocol: installed lock/vendor source first, official versioned docs second, exact upstream tags third, and aggregators only as source-checked discovery aids
- Behavioral output evals plus trigger/non-trigger queries for regression testing

## Structure

```
laravel-filament-v5/
├── SKILL.md                        # Entry point: preflight, gate, routing, v5 invariants, evidence protocol
├── agents/
│   └── openai.yaml                 # Codex discovery metadata and default invocation prompt
├── evals/
│   ├── evals.json                  # Behavioral quality cases and assertions
│   └── eval_queries.json           # Trigger and non-trigger coverage
└── references/                     # Loaded on demand per task
    ├── resources.md                # Resource anatomy: generation, navigation, getUrl(), authorization, extracting classes
    ├── infolists.md                # Read-only display entries
    ├── forms.md                    # Form fields + recurring patterns
    ├── tables.md                   # Columns, filters, empty states, grouping, record layouts (Split/Stack/Panel)
    ├── layout.md                   # Sections, grids, tabs, wizards, primes, callouts, EmptyState
    ├── actions.md                  # Actions, modals, table action placement
    ├── widgets.md                  # Stats, charts, table widgets, dashboards
    ├── relation-managers.md        # Choosing the right relationship tool + relation managers
    ├── panels.md                   # Panel provider: identity (colors/logo/font), navigation, multiple panels
    ├── notifications.md            # Flash, database, and broadcast notifications
    ├── enums.md                    # Shared labels, colors, icons, casts, fields, entries, and filters
    ├── security.md                 # Authorization, tenancy, uploads, HTML, import/export, sensitive state
    ├── advanced-features.md        # Pages, clusters, search, tenancy, import/export, nesting, plugins
    ├── testing.md                  # Pest + Livewire behavior, authorization, and tenant testing
    ├── ui-composition.md           # Filament-aligned defaults, page recipes, hierarchy, composition patterns
    └── screenshots.md              # Index of official docs screenshots for on-demand visual reference
```

## Requirements

- A Filament 5.x project. The agent verifies the exact installed Filament, Laravel, Livewire, PHP, Tailwind, and plugin versions instead of assuming rolling documentation matches the lockfile.

Baseline sources: [Filament 5 installation](https://filamentphp.com/docs/5.x/introduction/installation.md) and [upgrade guide](https://filamentphp.com/docs/5.x/upgrade-guide.md).

## Maintenance and evaluation

- Run `skills-ref validate skills/laravel-filament-v5` when the Agent Skills reference CLI is available.
- Run every case in `evals/evals.json` against the candidate skill and a clean previous-version baseline, then grade the listed assertions with concrete evidence.
- Use `evals/eval_queries.json` to regression-test implicit activation separately from output quality.
- Before publishing API changes, compare every versioned documentation link with `https://filamentphp.com/docs/llms.txt` and verify minor/patch-sensitive signatures against installed source or the matching upstream tag.

## License

MIT
