# Laravel Filament v5

AI agent skill that forces "official component first" behavior when building Filament v5 UIs. Instead of writing custom CSS/Blade for data presentation (JSON, key-value, colors, badges, images, icons, dates, money), the agent is anchored to enumerate Filament's official components — infolists, forms, tables, schemas, and actions — before reaching for markup. Data rendering is locked to official components; page composition stays free, guided by dedicated UI-composition patterns.

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
- Concrete anti-patterns (e.g. `<pre>` + CSS → `CodeEntry`, `<span>` + Tailwind → `badge()` + `HasColor` enum)
- v5 API breaking changes vs v3/v4 (`Schema`, namespaces, `recordActions()`, `Filament\Actions\*`, etc.)
- On-demand reference library: resources, infolists, forms, tables, layout/primes/callouts/empty states, actions, widgets & dashboards, relation managers, panel testing
- UI composition guide: visual hierarchy, Sections vs Tabs vs Wizard, column widths, scannable tables, empty states, feedback
- Fetch protocol (llms.txt, `.md` doc pages, laravel-boost `search-docs`) as a freshness backup for anything outside the references

## Structure

```
laravel-filament-v5/
├── SKILL.md                        # Always loaded: gate, quick map, anti-patterns, v5 breaking changes, routing, fetch protocol
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

- PHP 8.3+
- Laravel 12+
- Filament 5.x

## License

MIT
