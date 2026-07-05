# Filament v5 — Official Component First

AI agent skill that forces "official component first" behavior when building Filament v5 UIs. Instead of writing custom CSS/Blade for data presentation (JSON, key-value, colors, badges, images, icons, dates, money), the agent is anchored to enumerate Filament's official components — infolists, forms, tables, schemas, and actions — before reaching for markup.

## Install

```bash
npx skills add jotafurtado/dev-skills --skill filament-v5-official-first
```

Or with Laravel Boost:

```bash
php artisan boost:add-skill jotafurtado/dev-skills --skill filament-v5-official-first
```

## What's Covered

- Mandatory gate: classify the data primitive before writing custom markup
- Concrete anti-patterns (e.g. `<pre>` + CSS → `CodeEntry`, `<span>` + Tailwind → `badge()` + `HasColor` enum)
- Inventory of official v5 components: infolists, forms, table columns/filters, schema layouts, actions
- v5 API breaking changes vs v3/v4 (`Schema`, namespaces, `recordActions()`, `Filament\Actions\*`, etc.)
- Fetch protocol (llms.txt, docs 5.x, laravel-boost `search-docs`) as a freshness backup for anything outside the inventory

## Structure

```
filament-v5-official-first/
└── SKILL.md    # Single-file skill: rules, inventory, anti-patterns, v5 breaking changes, fetch protocol
```

## Requirements

- PHP 8.5+
- Laravel 12+
- Filament 5.x

## License

MIT
