# Tables — columns, filters, empty states (`Filament\Tables\*`)

Used inside `public static function table(Table $table): Table`.

Signatures below are focused fragments. Add imports for the shown columns, filters, actions, icons, and `Filament\Tables\Table` in the target class.

This file is an **API inventory**: it states which official table components exist and what their signatures are. It names a composition decision where one exists, so the decision is not skipped in silence, and leaves every one of them — column order, filter choice, grouping, summaries, responsive record layout — to `laravel-filament-v5-ui-ux`, `references/table.md`, which publishes the reference compositions that resolve them.

## Columns (`Filament\Tables\Columns\*`)

| Component | For | Minimal signature | 5.x doc |
|---|---|---|---|
| `TextColumn` | Text, date, money, **badge** | `TextColumn::make('status')->badge()->sortable()->searchable()` · `->money('USD')` · `->dateTime()` | [columns/text](https://filamentphp.com/docs/5.x/tables/columns/text.md) |
| `IconColumn` | Icon/boolean | `IconColumn::make('is_active')->boolean()` | [columns/icon](https://filamentphp.com/docs/5.x/tables/columns/icon.md) |
| `ImageColumn` | Images/avatars | `ImageColumn::make('avatar')->circular()` | [columns/image](https://filamentphp.com/docs/5.x/tables/columns/image.md) |
| `ColorColumn` | Color swatch | `ColorColumn::make('color')` | [columns/color](https://filamentphp.com/docs/5.x/tables/columns/color.md) |
| `SelectColumn` / `ToggleColumn` / `TextInputColumn` / `CheckboxColumn` | Inline editing in the table | `ToggleColumn::make('is_featured')` | [columns/toggle](https://filamentphp.com/docs/5.x/tables/columns/toggle.md) |

Inline-editable columns do not automatically enforce the model's `update` policy. Add the documented `disabled()` authorization check and negative tests; see `references/security.md`.

## Filters (`Filament\Tables\Filters\*`)

| Component | For | Minimal signature | 5.x doc |
|---|---|---|---|
| `SelectFilter` | Filter by options/enum/relation | `SelectFilter::make('status')->options(OrderStatus::class)` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview.md) |
| `TernaryFilter` | Yes/no/all filter | `TernaryFilter::make('is_active')` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview.md) |
| `TrashedFilter` | Soft deletes | `TrashedFilter::make()` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview.md) |
| `Filter` | Custom query | `Filter::make('published')->query(fn ($query) => $query->whereNotNull('published_at'))` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview.md) |

## Empty state (`Table` API)

The table renders an empty state automatically; customize it on the `Table` object ([doc](https://filamentphp.com/docs/5.x/tables/empty-state.md)):

```php
use Filament\Actions\Action;
use Filament\Support\Icons\Heroicon;
use Filament\Tables\Table;

$table
    ->emptyStateHeading('No posts yet')
    ->emptyStateDescription('Once you write your first post, it will appear here.')
    ->emptyStateIcon(Heroicon::OutlinedBookmark)
    ->emptyStateActions([
        Action::make('create')->label('Create post')->button(),
    ])
```

`->emptyState(view('...'))` is a full-custom escape hatch. The mandatory component gate in `SKILL.md` governs when reaching for it is legitimate.

## Grouping rows

`->defaultGroup('status')` on the `Table` groups rows under headers. Group headers show the attribute value by default; customize with a `Group` object (`Filament\Tables\Grouping\Group`): `Group::make('status')->getTitleFromRecordUsing(fn ($record): string => ...)`, `->label('State')`, `->getDescriptionFromRecordUsing(...)`. ([grouping doc](https://filamentphp.com/docs/5.x/tables/grouping.md))

## Summaries

Summarizers attach to a column with `->summarize()` (`Filament\Tables\Columns\Summarizers\*`): `Average`, `Count`, `Range`, `Sum`. The first column in a table cannot carry a summarizer. ([summaries doc](https://filamentphp.com/docs/5.x/tables/summaries.md))

## Record layout components (`Filament\Tables\Columns\Layout\*`)

Columns can be composed into layout components ([layout doc](https://filamentphp.com/docs/5.x/tables/layout.md)):

| Component | Minimal signature |
|---|---|
| `Split` | `Split::make([...])->from('md')` — `->grow(false)` on inner columns prevents whitespace |
| `Stack` | `Stack::make([...])` — `->space(1)`, `->alignment(Alignment::End)`, `->visibleFrom('md')` |
| `Grid` | `Grid::make(['lg' => 2])->schema([...])` — CSS Grid, equal tracks; `->columnSpan([...])` per component |
| `Panel` | `Panel::make([...])->collapsible()` — `->collapsed(false)` expands by default |

Table-level: `->contentGrid(['md' => 2, 'xl' => 3])` renders records as cards; `->stackedOnMobile()` stacks cells on small screens without a layout component.

Which of these a record should use, and at which breakpoint, is a composition decision.

## Pagination

`->paginated([10, 25, 50, 100, 'all'])`, `->defaultPaginationPageOption(25)`, `->extremePaginationLinks()`, `->paginated(false)` to disable. ([overview doc](https://filamentphp.com/docs/5.x/tables/overview.md))

## Table-level conventions

- Actions go in `->recordActions([...])`, `->toolbarActions([...])`, and `->groupedBulkActions([...])` (see SKILL.md, "Filament v5 invariants"). Bulk actions wrap in `BulkActionGroup::make([...])`. Details in `references/actions.md`.
- `->defaultSort('created_at', direction: 'desc')` sets the table's default order. Whether the domain has a meaningful default order, and which column carries it, is a composition decision.
- `->searchable()` and `->sortable()` opt a column into search and ordering. Which columns receive them is a composition decision.
- `->toggleable(isToggledHiddenByDefault: true)` hides a column by default while keeping it reachable from the column toggle.
- For a reusable domain status shared across surfaces, see SKILL.md's enum invariant and `references/enums.md`. A documented `->color(fn (string $state) => ...)` callback remains valid for local or non-enum state; avoid duplicating the same mapping across surfaces.
