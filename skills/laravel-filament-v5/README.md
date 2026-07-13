# Laravel Filament v5

AI agent skill that enforces "official component first" behavior when building Filament v5 UIs. Before writing custom CSS/Blade, the agent checks the documented component for the current surface—schema/infolist, form, table, action, widget, or page. When no official equivalent fits, it records the documentation checked and uses the smallest workaround while keeping page composition flexible.

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
- Quick map from data primitive → official component across infolist / form / table
- Documented escape hatch when no component exists on the correct surface
- Concrete anti-patterns (e.g. `<pre>` + CSS → `CodeEntry`, `<span>` + Tailwind → `badge()` + `HasColor` enum)
- v5 API breaking changes vs v3/v4 (`Schema`, namespaces, `recordActions()`, `Filament\Actions\*`, etc.)
- On-demand reference library: resources, infolists, forms, tables, layout/primes/callouts/empty states, actions, widgets & dashboards, relation managers, panel testing
- UI composition guide: visual hierarchy, Sections vs Tabs vs Wizard, column widths, scannable tables, empty states, feedback
- Fetch protocol (llms.txt, `.md` doc pages, laravel-boost `search-docs`) as a freshness backup for anything outside the references

## Structure

```
laravel-filament-v5/
├── SKILL.md                        # Entry point: gate, quick map, v5 changes, routing, fetch protocol
└── references/                     # Loaded on demand per task
    ├── resources.md                # Resource anatomy: generation, navigation, getUrl(), authorization
    ├── infolists.md                # Read-only display entries
    ├── forms.md                    # Form fields + recurring patterns
    ├── tables.md                   # Columns, filters, empty states
    ├── layout.md                   # Sections, grids, tabs, wizards, primes, callouts, EmptyState
    ├── actions.md                  # Actions, modals, table action placement
    ├── widgets.md                  # Stats, charts, table widgets, dashboards
    ├── relation-managers.md        # Choosing the right relationship tool + relation managers
    ├── testing.md                  # Pest + Livewire panel testing
    └── ui-composition.md           # Visual hierarchy and page organization patterns
```

## Requirements

- Filament 5.x
- PHP 8.2+
- Laravel 11.28+
- Livewire 4.0+
- Tailwind CSS 4.1+ for the current documented installation flow

Sources: [Filament 5 installation](https://filamentphp.com/docs/5.x/introduction/installation.md) and [upgrade guide](https://filamentphp.com/docs/5.x/upgrade-guide.md).

## License

MIT
