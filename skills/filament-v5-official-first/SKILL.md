---
name: filament-v5-official-first
description: "Builds Filament v5 interfaces using ALWAYS official components before any custom markup/CSS. Activates when creating or editing anything Filament: resources, infolists, forms, tables, actions, schemas, panels, widgets, relation managers, custom pages, filters, columns, entries, fields, modals, wizards, or panel tests. Also triggers when the user mentions 'Filament', 'admin panel', 'infolist', 'view page', 'form schema', 'table column', 'display payload', 'show JSON', 'status badge', or asks to render/display/format data inside a Filament page."
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
  author: community
  version: "1.0.0"
  domain: backend
  filament_version: "5.x"
  laravel_version: ">=12.x"
  php_version: ">=8.5"
  triggers: Filament, infolist, form schema, table column, action, panel, widget, resource, relation manager, custom page, badge, CodeEntry, KeyValueEntry
  role: specialist
  scope: implementation
  output-format: code
---

# Filament v5 — Official Component First

The mistake this skill prevents isn't a knowledge gap — it's overconfidence. You know how to render JSON with a styled `<pre>`, so you write the `<pre>`. But Filament v5 already ships `CodeEntry` with syntax highlighting, a copy button, and dark mode support, ready to use. The official component never made it into your list of options because you never stopped to consider it might exist. This skill exists to force that pause.

## The mandatory gate (run BEFORE writing markup)

Before writing `<div>`, `<span>`, `<pre>`, `@foreach`, Tailwind classes, or any custom Blade view inside a Filament context, **stop and run these 3 steps**:

1. **Classify the data** into a presentation primitive: code/JSON, key-value, color, image, badge/status, list, repeatable collection, icon/boolean, date/time, money, formatted text.
2. **Every primitive on that list HAS an official component.** Find it in the inventory below and use it. There's no "too simple a case for a component" — the component IS the simple case.
3. **If it's not in the inventory**, run the fetch protocol (last section) BEFORE concluding it doesn't exist. "I don't recall this component" is not evidence that it doesn't exist.

**Custom CSS/Blade is allowed only for layout fine-tuning** (spacing, alignment, width) — **never** to render data. If you catch yourself writing a styled `<pre>`, a colored `<span>`, or a Blade loop inside a resource, that's the signal you skipped the gate. Go back to step 1.

Confidence is not verification: the mistake happens exactly at the moment you "know" how to render something by hand. The more obvious a custom solution seems, the more likely an official component exists for it.

## Anti-patterns: don't do X, do Y

**❌ JSON/code with `<pre>` + custom CSS → ✅ `CodeEntry`**

```php
// ❌ NEVER
ViewEntry::make('payload')->view('filament.custom-json-pre') // <pre> with CSS

// ✅ ALWAYS — highlighting via Phiki, dark mode, all built in
use Filament\Infolists\Components\CodeEntry;
use Phiki\Grammar\Grammar;

CodeEntry::make('payload')
    ->grammar(Grammar::Json)
    ->copyable()
```

**❌ Colored status with `<span>` + Tailwind → ✅ `badge()` + `HasColor` enum**

```php
// ❌ NEVER
// <span class="rounded bg-green-100 px-2 text-green-800">{{ $status }}</span>

// ✅ ALWAYS — same API in an infolist (TextEntry) or a table (TextColumn)
TextEntry::make('status')->badge() // color/label/icon come from the enum

// The enum carries the semantics:
use Filament\Support\Contracts\{HasColor, HasIcon, HasLabel};

enum OrderStatus: string implements HasLabel, HasColor, HasIcon
{
    case Pending = 'pending';
    case Shipped = 'shipped';

    public function getLabel(): string { /* ... */ }
    public function getColor(): string { /* 'warning', 'success'... */ }
    public function getIcon(): \Filament\Support\Icons\Heroicon { /* ... */ }
}
```

**More of the same family:**

| ❌ Don't | ✅ Do |
|---|---|
| `@foreach` in Blade over an associative array | `KeyValueEntry::make('meta')` |
| `@foreach` over a list of related items | `RepeatableEntry::make('items')->schema([...])` |
| `<div style="background: {{ $color }}">` | `ColorEntry::make('color')` |
| `<img>` with avatar classes | `ImageEntry::make('avatar')->circular()` |
| Inline SVG / icon string for a boolean | `IconEntry::make('is_active')->boolean()` |
| Formatting date/money by hand in Blade | `TextEntry::make('...')->dateTime()` / `->money('USD')` |
| Custom JS "copy to clipboard" | `->copyable()` (available on several entries) |
| Rendering Markdown/HTML with an external lib | `TextEntry::make('body')->markdown()` / `->html()` |

## Official v5 component inventory

This is memory, not documentation: minimal signature + link. If in doubt about a specific method, open the link — don't guess.

### Infolists — read-only display (`Filament\Infolists\Components\*`)

Used inside `public function infolist(Schema $schema): Schema` in View pages.

| Component | For | Minimal signature | 5.x doc |
|---|---|---|---|
| `TextEntry` | Text, date, money, badge, lists | `TextEntry::make('title')->badge()` · `->dateTime()` · `->money('USD')` · `->markdown()` · `->listWithLineBreaks()` | [text-entry](https://filamentphp.com/docs/5.x/infolists/text-entry) |
| `CodeEntry` | Code, JSON, payloads, logs | `CodeEntry::make('payload')->grammar(Grammar::Json)->copyable()` | [code-entry](https://filamentphp.com/docs/5.x/infolists/code-entry) |
| `KeyValueEntry` | Associative array / metadata | `KeyValueEntry::make('meta')` | [key-value-entry](https://filamentphp.com/docs/5.x/infolists/key-value-entry) |
| `ColorEntry` | Color swatch | `ColorEntry::make('color')` | [color-entry](https://filamentphp.com/docs/5.x/infolists/color-entry) |
| `ImageEntry` | Images, avatars | `ImageEntry::make('avatar')->circular()` · `->stacked()` | [image-entry](https://filamentphp.com/docs/5.x/infolists/image-entry) |
| `IconEntry` | Icon, visual boolean | `IconEntry::make('is_active')->boolean()` | [icon-entry](https://filamentphp.com/docs/5.x/infolists/icon-entry) |
| `RepeatableEntry` | Repeated collections/relations | `RepeatableEntry::make('comments')->schema([...])` | [repeatable-entry](https://filamentphp.com/docs/5.x/infolists/repeatable-entry) |

### Forms — editing (`Filament\Forms\Components\*`)

Used inside `public static function form(Schema $schema): Schema`.

| Component | For | Minimal signature | 5.x doc |
|---|---|---|---|
| `TextInput` | Text, email, number, password | `TextInput::make('email')->email()->required()` | [text-input](https://filamentphp.com/docs/5.x/forms/text-input) |
| `Textarea` | Plain long text | `Textarea::make('notes')->rows(4)` | [textarea](https://filamentphp.com/docs/5.x/forms/textarea) |
| `Select` | Options, relationships | `Select::make('author_id')->relationship('author', 'name')->searchable()->preload()` | [select](https://filamentphp.com/docs/5.x/forms/select) |
| `Checkbox` / `Toggle` | Boolean | `Toggle::make('is_active')` | [toggle](https://filamentphp.com/docs/5.x/forms/toggle) |
| `ToggleButtons` | Few visible options (status!) | `ToggleButtons::make('status')->options(OrderStatus::class)->inline()` | [toggle-buttons](https://filamentphp.com/docs/5.x/forms/toggle-buttons) |
| `Radio` / `CheckboxList` | Options in a list | `CheckboxList::make('tags')->options([...])` | [checkbox-list](https://filamentphp.com/docs/5.x/forms/checkbox-list) |
| `DateTimePicker` | Date/time (also `DatePicker`, `TimePicker`) | `DateTimePicker::make('published_at')` | [date-time-picker](https://filamentphp.com/docs/5.x/forms/date-time-picker) |
| `FileUpload` | Files, images | `FileUpload::make('attachment')->image()` — default is **private**; `->visibility('public')` only if needed | [file-upload](https://filamentphp.com/docs/5.x/forms/file-upload) |
| `RichEditor` / `MarkdownEditor` | Rich text | `RichEditor::make('body')` | [rich-editor](https://filamentphp.com/docs/5.x/forms/rich-editor) |
| `Repeater` | Repeated rows / relations | `Repeater::make('items')->schema([...])` — doesn't take full width by default | [repeater](https://filamentphp.com/docs/5.x/forms/repeater) |
| `Builder` | Flexible content blocks | `Builder::make('content')->blocks([...])` | [builder](https://filamentphp.com/docs/5.x/forms/builder) |
| `TagsInput` | List of strings | `TagsInput::make('tags')` | [tags-input](https://filamentphp.com/docs/5.x/forms/tags-input) |
| `KeyValue` | Edit associative array | `KeyValue::make('meta')` | [key-value](https://filamentphp.com/docs/5.x/forms/key-value) |
| `ColorPicker` | Pick a color | `ColorPicker::make('color')` | [color-picker](https://filamentphp.com/docs/5.x/forms/color-picker) |
| `CodeEditor` | Edit code/JSON | `CodeEditor::make('config')` — verify the exact signature in the 5.x docs | [code-editor](https://filamentphp.com/docs/5.x/forms/code-editor) |
| `Hidden` | Hidden value | `Hidden::make('user_id')` | [hidden](https://filamentphp.com/docs/5.x/forms/hidden) |

### Tables — columns and filters (`Filament\Tables\Columns\*`, `Filament\Tables\Filters\*`)

| Component | For | Minimal signature | 5.x doc |
|---|---|---|---|
| `TextColumn` | Text, date, money, **badge** | `TextColumn::make('status')->badge()->sortable()->searchable()` · `->money('USD')` · `->dateTime()` | [columns/text](https://filamentphp.com/docs/5.x/tables/columns/text) |
| `IconColumn` | Icon/boolean | `IconColumn::make('is_active')->boolean()` | [columns/icon](https://filamentphp.com/docs/5.x/tables/columns/icon) |
| `ImageColumn` | Images/avatars | `ImageColumn::make('avatar')->circular()` | [columns/image](https://filamentphp.com/docs/5.x/tables/columns/image) |
| `ColorColumn` | Color swatch | `ColorColumn::make('color')` | [columns/color](https://filamentphp.com/docs/5.x/tables/columns/color) |
| `SelectColumn` / `ToggleColumn` / `TextInputColumn` / `CheckboxColumn` | Inline editing in the table | `ToggleColumn::make('is_featured')` | [columns/toggle](https://filamentphp.com/docs/5.x/tables/columns/toggle) |
| `SelectFilter` | Filter by options/enum/relation | `SelectFilter::make('status')->options(OrderStatus::class)` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview) |
| `TernaryFilter` | Yes/no/all filter | `TernaryFilter::make('is_active')` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview) |
| `TrashedFilter` | Soft deletes | `TrashedFilter::make()` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview) |

### Layout — schemas (`Filament\Schemas\Components\*`)

Apply to both forms AND infolists (same Schema system in v5).

| Component | Minimal signature | 5.x doc |
|---|---|---|
| `Section` | `Section::make('Details')->columns(2)->collapsible()->schema([...])` | [sections](https://filamentphp.com/docs/5.x/schemas/sections) |
| `Grid` | `Grid::make(3)->schema([...])` | [layouts](https://filamentphp.com/docs/5.x/schemas/layouts) |
| `Tabs` | `Tabs::make()->tabs([Tabs\Tab::make('General')->schema([...])])` | [tabs](https://filamentphp.com/docs/5.x/schemas/tabs) |
| `Wizard` | `Wizard::make([Wizard\Step::make('Order')->schema([...])])` | [wizards](https://filamentphp.com/docs/5.x/schemas/wizards) |
| `Fieldset` / `Flex` / `Group` | grouping and distribution — verify the exact signature in the 5.x docs | [layouts](https://filamentphp.com/docs/5.x/schemas/layouts) |
| `Text` / `Icon` / `Image` (primes) | arbitrary static content inside a schema — use BEFORE reaching for custom Blade; verify in the docs | [primes](https://filamentphp.com/docs/5.x/schemas/primes) |

⚠️ `Grid`, `Section`, and `Repeater` **don't take full width by default** — use `->columnSpan(...)` or `->columnSpanFull()`.

### Actions (`Filament\Actions\*` — ALWAYS this namespace)

| Component | Minimal signature | 5.x doc |
|---|---|---|
| `Action` | `Action::make('approve')->requiresConfirmation()->action(fn ($record) => ...)` | [overview](https://filamentphp.com/docs/5.x/actions/overview) |
| Action with modal/form | `Action::make('edit')->schema([TextInput::make('reason')])` — modals use `->schema()`, **not** `->form()` | [modals](https://filamentphp.com/docs/5.x/actions/modals) |
| `CreateAction`, `EditAction`, `ViewAction`, `DeleteAction`, `ActionGroup`, `BulkAction`, `DeleteBulkAction`, `ImportAction`, `ExportAction` | `DeleteAction::make()` | [overview](https://filamentphp.com/docs/5.x/actions/overview) |

## v5 API breaking changes — never suggest the old way

Your v3/v4 Filament knowledge will betray you. In v5:

- **Unified Schema**: `public function infolist(Schema $schema): Schema` and `public static function form(Schema $schema): Schema`. Top-level is `$schema->components([...])`. ❌ `$infolist->schema([...])` is v3 — no longer exists.
- **Domain-based namespaces**:
  - Layout (Section, Grid, Tabs, Flex, Fieldset, Wizard): `Filament\Schemas\Components\*`
  - Utilities (Get, Set): `Filament\Schemas\Components\Utilities\*`
  - Form fields: `Filament\Forms\Components\*`
  - Infolist entries: `Filament\Infolists\Components\*`
  - Table columns: `Filament\Tables\Columns\*` · filters: `Filament\Tables\Filters\*`
  - Actions: `Filament\Actions\*` — ❌ `Filament\Tables\Actions\*` was **removed** in v5.
- **Renamed table methods**: `->recordActions([...])` (not `->actions()`), `->groupedBulkActions([...])` (not `->bulkActions()`), `->toolbarActions([...])`.
- **Action modals**: `->schema([...])`, ❌ not `->form([...])`.
- **Icons**: enum `Filament\Support\Icons\Heroicon` (e.g. `Heroicon::PencilSquare`). ❌ Never strings like `'heroicon-o-pencil'`. For navigation, use the `Outlined*` variants.
- **Domain enums**: backed string enums implementing `HasLabel`, `HasColor`, `HasIcon` (`Filament\Support\Contracts`) — this is how badge/select/filter get label, color, and icon for free.
- **Conditional operation**: compare against `Operation::Create` / `Operation::Edit` / `Operation::View` — ❌ don't compare strings `'create'`/`'edit'`.
- **File uploads are private by default**: only add `->visibility('public')` when public access is actually required.

## Fetch protocol — freshness backup

The inventory above works offline and covers day-to-day needs. Fetch the docs when: (a) the component/method isn't in the inventory; (b) you hesitated about a signature; (c) the user mentioned something you don't recognize.

1. **Canonical LLM index**: `https://filamentphp.com/docs/llms.txt` — lists every page; locate the relevant 5.x page.
2. **Direct page**: `https://filamentphp.com/docs/5.x/{section}/{page}` (e.g. `5.x/infolists/code-entry`).
3. **MCP `laravel-boost` (`search-docs`)**, if active: use `packages: ["filament/filament"]`. ⚠️ **The response mixes 3.x/4.x/5.x** — discard anything not tagged `filament/filament@5.x`. A 3.x snippet looks plausible and compiles wrong.
4. Never resolve hesitation "from memory" with a v3/v4 signature. If you can't verify it, write the docs link in a comment and state explicitly that the signature needs confirmation — don't guess.

## Target project context

`filament/filament` **v5.6.0** · PHP 8.5 · Laravel 12 · Livewire 4 · Tailwind v4. All generated code must be valid for this combination.
