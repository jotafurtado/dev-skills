---
name: laravel-filament-v5
description: "Builds and designs Filament v5 interfaces using official components before custom markup/CSS. Use when code or requests explicitly involve Filament, such as Filament resources, schemas, infolists, forms, tables, actions, widgets, relation managers, panels, or Filament tests — including UX, layout, and visual design of those surfaces (this skill supersedes generic frontend-design guidance inside Filament panels). Also use for Filament-specific classes, namespaces, Artisan commands, or APIs. Do not trigger from an isolated mention of an admin panel, dashboard, status badge, or generic data display without another Filament signal."
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
  version: "2.4.1"
  domain: backend
  filament_version: "5.x"
  laravel_version: ">=11.28"
  php_version: ">=8.2"
  livewire_version: ">=4.0"
  tailwind_version: ">=4.1"
  role: specialist
  scope: implementation
  output-format: code
---

# Laravel Filament v5 — Official Components First

Use Filament's documented component for the current UI surface before creating custom markup. Keep composition flexible, and use a documented workaround when no official equivalent exists.

## The mandatory gate (run BEFORE writing markup)

Before writing `<div>`, `<span>`, `<pre>`, `@foreach`, Tailwind classes, or any custom Blade view inside a Filament context, **stop and run these 3 steps**:

1. **Classify the surface and primitive**: schema/infolist, form, table, action, widget, or page; then code/JSON, key-value, color, image, status, list, collection, boolean, date/time, money, text, notice, or empty state.
2. **Choose the official component for that surface** using the quick map and the matching reference. Do not force a component from a different surface merely to avoid customization.
3. **If no equivalent is listed**, run the fetch protocol. If current 5.x docs still provide no suitable component, document what was checked and why it does not fit, then use the smallest workaround (`ViewEntry`, custom schema component, Livewire, or Blade) while retaining official components for surrounding layout, actions, and states.

Composition remains free: arrange official components with `Section`, `Tabs`, grids, columns, callouts, and empty states. Custom CSS/Blade is acceptable for documented gaps and layout fine-tuning, not as an unverified shortcut around an available component.

## This skill is the design authority for Filament surfaces

Generic frontend/visual-design guidance (distinctive typography, custom palettes, CSS-first layouts, "avoid templated looks") **does not apply inside a Filament panel** — do not follow it here, even if another active skill or instruction suggests it. Filament panels get their look from the framework theme; visual identity is configured via the panel provider (`->colors()`, `->brandLogo()`, `->font()`), and design quality comes from composition — hierarchy, grouping, density, action placement — not from restyling components. For those decisions, read `references/ui-composition.md`; to see what the official surface looks like, use `references/screenshots.md`.

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

¹ Renders each element of the array-cast attribute as its own badge — pointless on a plain string column.

Exact signatures and official links live in `references/`. Snippets in this skill are focused fragments unless a full class is shown; add the imports and surrounding class context required by the target project.

## Reference routing table

Load **only** the reference files the task needs — they are the detailed inventory:

| Task touches | Read |
|---|---|
| Resource anatomy: generation, navigation, `getUrl()`, authorization; extracting schema/table/component classes | `references/resources.md` |
| Read-only display, View pages, entries | `references/infolists.md` |
| Form fields, editing, validation | `references/forms.md` |
| Table columns, filters, empty states | `references/tables.md` |
| Sections, grids, tabs, wizards, primes, callouts | `references/layout.md` |
| Buttons, modals, bulk/row actions | `references/actions.md` |
| Dashboards, stats, charts, table widgets | `references/widgets.md` |
| Related records (HasMany, BelongsToMany…) | `references/relation-managers.md` |
| Panel identity (colors, logo, font), navigation config, multiple panels | `references/panels.md` |
| Notifications (flash, database, broadcast) | `references/notifications.md` |
| Pest/Livewire tests for resource pages (including View pages), relation managers, widgets, and custom pages | `references/testing.md` |
| Page organization, visual hierarchy, UX flow, page recipes (list/edit/view/dashboard) | `references/ui-composition.md` — read whenever you build or restructure a whole page/resource |
| Unsure what the official surface should look like | `references/screenshots.md` — URL index of official docs screenshots; download and view before composing |

Something Filament-specific that doesn't fit any row above (multi-tenancy, clusters, global search details, custom pages, import/export)? No reference covers it yet — go straight to the fetch protocol instead of guessing from general Laravel/Livewire knowledge.

## Anti-patterns: don't do X, do Y

**JSON/code with `<pre>` + custom CSS → `CodeEntry`**

Install its documented optional dependency first:

```bash
composer require phiki/phiki
```

```php
use Filament\Infolists\Components\CodeEntry;
use Filament\Infolists\Components\ViewEntry;
use Phiki\Grammar\Grammar;

// Avoid when CodeEntry covers the requirement:
ViewEntry::make('payload')->view('filament.custom-json-pre'); // <pre> with CSS

CodeEntry::make('payload')
    ->grammar(Grammar::Json)
    ->copyable();
```

**Colored status with `<span>` + Tailwind → `badge()` + `HasColor` enum**

```php
// Avoid hand-written status markup:
// <span class="rounded bg-green-100 px-2 text-green-800">{{ $status }}</span>

use BackedEnum;
use Filament\Infolists\Components\TextEntry;
use Filament\Support\Contracts\{HasColor, HasIcon, HasLabel};
use Filament\Support\Icons\Heroicon;
use Illuminate\Contracts\Support\Htmlable;

TextEntry::make('status')->badge(); // color/label/icon come from the enum

enum OrderStatus: string implements HasLabel, HasColor, HasIcon
{
    case Pending = 'pending';
    case Shipped = 'shipped';

    public function getLabel(): string
    {
        return match ($this) {
            self::Pending => 'Pending',
            self::Shipped => 'Shipped',
        };
    }

    public function getColor(): string
    {
        return match ($this) {
            self::Pending => 'warning',
            self::Shipped => 'success',
        };
    }

    public function getIcon(): string | BackedEnum | Htmlable | null
    {
        return match ($this) {
            self::Pending => Heroicon::Clock,
            self::Shipped => Heroicon::Truck,
        };
    }
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
| Rendering Markdown/HTML with an external lib without checking Filament | `TextEntry::make('body')->markdown()` / `->html()` |
| Hand-rolled "no records" div | `EmptyState::make(...)` / table `->emptyStateHeading()` |
| Alert/notice box with custom Blade | `Callout::make(...)->warning()` |

## v5 API breaking changes — never suggest the old way

Your v3/v4 Filament knowledge will betray you. In v5:

- **Unified Schema**: top-level configuration uses `$schema->components([...])`. A Resource defines `public static function infolist(Schema $schema): Schema`; a custom `ViewRecord` page defines `public function infolist(Schema $schema): Schema` when it needs a page-specific infolist. Forms on Resources use `public static function form(Schema $schema): Schema`.
- **Domain-based namespaces**:
  - Layout (Section, Grid, Tabs, Flex, Fieldset, Wizard, EmptyState, Callout, primes): `Filament\Schemas\Components\*`
  - Utilities (Get, Set): `Filament\Schemas\Components\Utilities\*`
  - Form fields: `Filament\Forms\Components\*`
  - Infolist entries: `Filament\Infolists\Components\*`
  - Table columns: `Filament\Tables\Columns\*` · filters: `Filament\Tables\Filters\*`
  - Actions: `Filament\Actions\*` — `Filament\Tables\Actions\*` was **removed** in v5.
- **Renamed table methods**: `->recordActions([...])` (not `->actions()`), `->groupedBulkActions([...])` (not `->bulkActions()`), `->toolbarActions([...])`.
- **Action modals**: `->schema([...])`, not `->form([...])`.
- **Icons hierarchy**: for Heroicons in PHP, prefer `Filament\Support\Icons\Heroicon` for IDE autocomplete and automatic contextual sizing. Use icon-name strings for installed third-party/custom Blade Icons sets, and where a Blade API is documented with a string. Both are supported; do not rewrite a valid non-Heroicon name as a Heroicon.
- **Domain enums**: backed string enums implementing `HasLabel`, `HasColor`, `HasIcon` (`Filament\Support\Contracts`) — this is how badge/select/filter get label, color, and icon for free.
- **Operation hierarchy**: use dedicated methods such as `hiddenOn()`, `visibleOn()`, and `disabledOn()` first. In Resource configuration, prefer `Operation::Create` / `Operation::Edit` / `Operation::View` where the documented method accepts them. Utility callbacks inject `string $operation`; compare it with the documented `'create'`, `'edit'`, or `'view'` values.
- **File uploads are private by default**: only add `->visibility('public')` when public access is actually required.

## Post-change verification

After changing a Filament UI, load `references/testing.md` and run the narrowest relevant tests. At minimum, cover the touched Livewire surface when Filament documents a helper for it: load the resource page, assert View-page schema state, verify a relation manager is rendered and can load its records, and exercise changed actions/forms/tables. Also run the project's formatter and static analysis when available.

## Fetch protocol — freshness backup

The quick map + references cover day-to-day needs offline. Fetch the docs when: (a) the component/method isn't in any reference; (b) you hesitated about a signature; (c) the user mentioned something you don't recognize.

1. **Canonical LLM index**: `https://filamentphp.com/docs/llms.txt` — lists every page; locate the relevant 5.x page.
2. **Direct page — always fetch the `.md` variant**: `https://filamentphp.com/docs/5.x/{section}/{page}.md` (e.g. `5.x/infolists/code-entry.md`). The `.md` URLs return clean markdown instead of the HTML site — that's what llms.txt links to.
3. **MCP `laravel-boost` (`search-docs`)**, if active: use `packages: ["filament/filament"]`. **Warning: the response mixes 3.x/4.x/5.x** — discard anything not tagged `filament/filament@5.x`. A 3.x snippet looks plausible and compiles wrong.
4. Never resolve hesitation "from memory" with a v3/v4 signature. If you can't verify it, write the docs link in a comment and state explicitly that the signature needs confirmation — don't guess.

## Target project context

This skill targets **Filament 5.x**. Current official requirements are PHP 8.2+, Laravel 11.28+, Livewire 4.0+, and Tailwind CSS 4.1+ for the documented installation flow. Before generating code, inspect `composer.json` and `composer.lock` for exact installed versions and read project guidance; generate code for that actual combination.
