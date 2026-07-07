---
name: laravel-filament-v5
description: "Builds Filament v5 interfaces using official components before any custom markup/CSS. Use when creating or editing anything Filament: resources, infolists, forms, tables, actions, widgets, relation managers, panels, or panel tests. Triggers on mentions of Filament, admin panel, infolist, form schema, table column, status badge, dashboard, or requests to render/display data inside a Filament page."
license: MIT
compatible_agents:
  - Claude Code
  - Cursor
  - Windsurf
  - Copilot
tags:
  - laravel
  - php
  - filament
  - admin-panel
  - backend
metadata:
  author: jotafurtado
  version: "2.0.0"
  domain: backend
  filament_version: "5.x"
  laravel_version: ">=12.x"
  php_version: ">=8.3"
  role: specialist
  scope: implementation
  output-format: code
---

# Laravel Filament v5 — Official Components, Free Composition

The mistake this skill prevents isn't a knowledge gap — it's overconfidence. You know how to render JSON with a styled `<pre>`, so you write the `<pre>`. But Filament v5 already ships `CodeEntry` with syntax highlighting, a copy button, and dark mode support, ready to use. The official component never made it into your list of options because you never stopped to consider it might exist. This skill exists to force that pause.

## The mandatory gate (run BEFORE writing markup)

Before writing `<div>`, `<span>`, `<pre>`, `@foreach`, Tailwind classes, or any custom Blade view inside a Filament context, **stop and run these 3 steps**:

1. **Classify the data** into a presentation primitive using the quick map below: code/JSON, key-value, color, image, badge/status, list, repeatable collection, icon/boolean, date/time, money, formatted text, static text/notice, empty state.
2. **Every primitive on that list HAS an official component.** Find it in the quick map, then load the matching reference file for the exact signature. There's no "too simple a case for a component" — the component IS the simple case.
3. **If it's not in the map**, run the fetch protocol (last section) BEFORE concluding it doesn't exist. "I don't recall this component" is not evidence that it doesn't exist.

Two clarifications so the gate doesn't over-restrict:

- **Data rendering is locked to official components. Composition is free.** How you arrange sections, tabs, columns, callouts, and empty states is a design decision — `references/ui-composition.md` gives you the patterns to make those pages fluid and scannable. Use it actively; a page built only from correct components can still be a bad page.
- **Custom CSS/Blade is allowed only for layout fine-tuning** (spacing, alignment, width) — **never** to render data. If you catch yourself writing a styled `<pre>`, a colored `<span>`, or a Blade loop inside a resource, that's the signal you skipped the gate. Go back to step 1.

Confidence is not verification: the mistake happens exactly at the moment you "know" how to render something by hand. The more obvious a custom solution seems, the more likely an official component exists for it.

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
| List of strings | `TextEntry->listWithLineBreaks()` | `TagsInput` | `TextColumn->badge()` |
| Static text / notice | `Text` / `Callout` | `Text` / `Callout` | — |
| "Nothing here yet" | `EmptyState` (schema) | — | `->emptyStateHeading()` |

Exact signatures, extra methods, and doc links live in `references/` — load the file for the surface you're touching.

## Reference routing table

Load **only** the reference files the task needs — they are the detailed inventory:

| Task touches | Read |
|---|---|
| Resource anatomy: generation, navigation, `getUrl()`, authorization | `references/resources.md` |
| Read-only display, View pages, entries | `references/infolists.md` |
| Form fields, editing, validation | `references/forms.md` |
| Table columns, filters, empty states | `references/tables.md` |
| Sections, grids, tabs, wizards, primes, callouts | `references/layout.md` |
| Buttons, modals, bulk/row actions | `references/actions.md` |
| Dashboards, stats, charts, table widgets | `references/widgets.md` |
| Related records (HasMany, BelongsToMany…) | `references/relation-managers.md` |
| Pest/Livewire tests for panels | `references/testing.md` |
| Page organization, visual hierarchy, UX flow | `references/ui-composition.md` — read whenever you build or restructure a whole page/resource |

Something Filament-specific that doesn't fit any row above (multi-tenancy, clusters, global search, custom pages, import/export, notifications)? No reference covers it yet — go straight to the fetch protocol instead of guessing from general Laravel/Livewire knowledge.

## Anti-patterns: don't do X, do Y

**JSON/code with `<pre>` + custom CSS → `CodeEntry`**

```php
// NEVER
ViewEntry::make('payload')->view('filament.custom-json-pre') // <pre> with CSS

// ALWAYS — highlighting via Phiki, dark mode, all built in
use Filament\Infolists\Components\CodeEntry;
use Phiki\Grammar\Grammar;

CodeEntry::make('payload')
    ->grammar(Grammar::Json)
    ->copyable()
```

**Colored status with `<span>` + Tailwind → `badge()` + `HasColor` enum**

```php
// NEVER
// <span class="rounded bg-green-100 px-2 text-green-800">{{ $status }}</span>

// ALWAYS — same API in an infolist (TextEntry) or a table (TextColumn)
TextEntry::make('status')->badge() // color/label/icon come from the enum

// The enum carries the semantics:
use Filament\Support\Contracts\{HasColor, HasIcon, HasLabel};
use Filament\Support\Icons\Heroicon;

enum OrderStatus: string implements HasLabel, HasColor, HasIcon
{
    case Pending = 'pending';
    case Shipped = 'shipped';

    public function getLabel(): string { /* ... */ }
    public function getColor(): string { /* 'warning', 'success'... */ }
    public function getIcon(): Heroicon { /* ... */ }
}
```

**More of the same family:**

| Don't | Do |
|---|---|
| `@foreach` in Blade over an associative array | `KeyValueEntry::make('meta')` |
| `@foreach` over a list of related items | `RepeatableEntry::make('items')->schema([...])` |
| `<div style="background: {{ $color }}">` | `ColorEntry::make('color')` |
| `<img>` with avatar classes | `ImageEntry::make('avatar')->circular()` |
| Inline SVG / icon string for a boolean | `IconEntry::make('is_active')->boolean()` |
| Formatting date/money by hand in Blade | `TextEntry::make('...')->dateTime()` / `->money('USD')` |
| Custom JS "copy to clipboard" | `->copyable()` (available on several entries) |
| Rendering Markdown/HTML with an external lib | `TextEntry::make('body')->markdown()` / `->html()` |
| Hand-rolled "no records" div | `EmptyState::make(...)` / table `->emptyStateHeading()` |
| Alert/notice box with custom Blade | `Callout::make(...)->warning()` |

## v5 API breaking changes — never suggest the old way

Your v3/v4 Filament knowledge will betray you. In v5:

- **Unified Schema**: `public function infolist(Schema $schema): Schema` and `public static function form(Schema $schema): Schema`. Top-level is `$schema->components([...])`. Never `$infolist->schema([...])` — that is v3 and no longer exists.
- **Domain-based namespaces**:
  - Layout (Section, Grid, Tabs, Flex, Fieldset, Wizard, EmptyState, Callout, primes): `Filament\Schemas\Components\*`
  - Utilities (Get, Set): `Filament\Schemas\Components\Utilities\*`
  - Form fields: `Filament\Forms\Components\*`
  - Infolist entries: `Filament\Infolists\Components\*`
  - Table columns: `Filament\Tables\Columns\*` · filters: `Filament\Tables\Filters\*`
  - Actions: `Filament\Actions\*` — `Filament\Tables\Actions\*` was **removed** in v5.
- **Renamed table methods**: `->recordActions([...])` (not `->actions()`), `->groupedBulkActions([...])` (not `->bulkActions()`), `->toolbarActions([...])`.
- **Action modals**: `->schema([...])`, not `->form([...])`.
- **Icons**: for any Heroicon, use the `Filament\Support\Icons\Heroicon` enum (e.g. `Heroicon::PencilSquare`), not the string form `'heroicon-o-pencil'` — the icon property type is `string|BackedEnum|null`, so the string still works, but the enum gives IDE autocomplete and is what v5's own examples favor. String names remain necessary for icon sets other than Heroicons. For navigation, use the `Outlined*` variants.
- **Domain enums**: backed string enums implementing `HasLabel`, `HasColor`, `HasIcon` (`Filament\Support\Contracts`) — this is how badge/select/filter get label, color, and icon for free.
- **Conditional operation**: compare against `Operation::Create` / `Operation::Edit` / `Operation::View` — never the strings `'create'`/`'edit'`.
- **File uploads are private by default**: only add `->visibility('public')` when public access is actually required.

## Fetch protocol — freshness backup

The quick map + references cover day-to-day needs offline. Fetch the docs when: (a) the component/method isn't in any reference; (b) you hesitated about a signature; (c) the user mentioned something you don't recognize.

1. **Canonical LLM index**: `https://filamentphp.com/docs/llms.txt` — lists every page; locate the relevant 5.x page.
2. **Direct page — always fetch the `.md` variant**: `https://filamentphp.com/docs/5.x/{section}/{page}.md` (e.g. `5.x/infolists/code-entry.md`). The `.md` URLs return clean markdown instead of the HTML site — that's what llms.txt links to.
3. **MCP `laravel-boost` (`search-docs`)**, if active: use `packages: ["filament/filament"]`. **Warning: the response mixes 3.x/4.x/5.x** — discard anything not tagged `filament/filament@5.x`. A 3.x snippet looks plausible and compiles wrong.
4. Never resolve hesitation "from memory" with a v3/v4 signature. If you can't verify it, write the docs link in a comment and state explicitly that the signature needs confirmation — don't guess.

## Target project context

This skill targets **Filament 5.x** on Laravel 12+ / PHP 8.3+ / Livewire 4 / Tailwind v4. Before generating code, read the project's `composer.json` (and `composer.lock` for exact versions) to confirm the installed `filament/filament`, `laravel/framework`, and PHP versions — all generated code must be valid for that specific combination, and project conventions (steering/CLAUDE.md files) override this skill's defaults where they conflict.
