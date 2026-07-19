# Tables — columns, filters, empty states (`Filament\Tables\*`)

Used inside `public static function table(Table $table): Table`.

Signatures below are focused fragments. Add imports for the shown columns, filters, actions, icons, and `Filament\Tables\Table` in the target class.

## Columns (`Filament\Tables\Columns\*`)

| Component | For | Minimal signature | 5.x doc |
|---|---|---|---|
| `TextColumn` | Text, date, money, **badge** | `TextColumn::make('status')->badge()->sortable()->searchable()` · `->money('USD')` · `->dateTime()` | [columns/text](https://filamentphp.com/docs/5.x/tables/columns/text.md) |
| `IconColumn` | Icon/boolean | `IconColumn::make('is_active')->boolean()` | [columns/icon](https://filamentphp.com/docs/5.x/tables/columns/icon.md) |
| `ImageColumn` | Images/avatars | `ImageColumn::make('avatar')->circular()` | [columns/image](https://filamentphp.com/docs/5.x/tables/columns/image.md) |
| `ColorColumn` | Color swatch | `ColorColumn::make('color')` | [columns/color](https://filamentphp.com/docs/5.x/tables/columns/color.md) |
| `SelectColumn` / `ToggleColumn` / `TextInputColumn` / `CheckboxColumn` | Inline editing in the table | `ToggleColumn::make('is_featured')` | [columns/toggle](https://filamentphp.com/docs/5.x/tables/columns/toggle.md) |

## Filters (`Filament\Tables\Filters\*`)

| Component | For | Minimal signature | 5.x doc |
|---|---|---|---|
| `SelectFilter` | Filter by options/enum/relation | `SelectFilter::make('status')->options(OrderStatus::class)` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview.md) |
| `TernaryFilter` | Yes/no/all filter | `TernaryFilter::make('is_active')` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview.md) |
| `TrashedFilter` | Soft deletes | `TrashedFilter::make()` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview.md) |
| `Filter` | Custom query | `Filter::make('published')->query(fn ($query) => $query->whereNotNull('published_at'))` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview.md) |

## Empty state — use the table API first

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

`->emptyState(view('...'))` exists as a full-custom escape hatch — use only when the heading/description/icon/actions API genuinely can't express the design.

## Grouping rows

`->defaultGroup('status')` on the `Table` groups rows under headers — a deliberate alternative to a redundant status column when users scan by state. Group headers show the attribute value by default; customize with a `Group` object (`Filament\Tables\Grouping\Group`): `Group::make('status')->getTitleFromRecordUsing(fn ($record): string => ...)`, `->label('State')`, `->getDescriptionFromRecordUsing(...)`. ([grouping doc](https://filamentphp.com/docs/5.x/tables/grouping.md))

## Record layouts — Split, Stack, Panel, grid

For records where a photo/identity block matters more than comparable facts (people, products, cards), columns compose into layouts from `Filament\Tables\Columns\Layout\*` ([layout doc](https://filamentphp.com/docs/5.x/tables/layout.md)):

| Component | For | Minimal signature |
|---|---|---|
| `Split` | Side-by-side blocks that stack below a breakpoint | `Split::make([ImageColumn::make('avatar')->grow(false), Stack::make([...])])->from('md')` — `->grow(false)` on inner columns prevents whitespace |
| `Stack` | Vertical stack inside a row or Split | `Stack::make([TextColumn::make('name'), TextColumn::make('email')])` |
| `Panel` | Pre-styled collapsible container for the long tail | `Panel::make([...])->collapsible()` — `->collapsed(false)` expands by default |

- Card grid: `$table->contentGrid(['md' => 2, 'xl' => 3])` renders records as cards instead of rows.
- `->stackedOnMobile()` on the table stacks columns on small screens without a layout component.
- Regular columns beat card grids for compare-and-scan work — see `references/ui-composition.md` for when each fits, and `references/screenshots.md` (`tables/layout/*`) for the official look.

## Table-level conventions

- Actions go in `->recordActions([...])`, `->groupedBulkActions([...])`, `->toolbarActions([...])` — the v3 `->actions()` / `->bulkActions()` no longer exist. Details in `references/actions.md`.
- `->defaultSort('created_at', direction: 'desc')` — every list should have a deliberate default order.
- `->searchable()` on key text columns; `->sortable()` where ordering is meaningful.
- `->toggleable(isToggledHiddenByDefault: true)` for secondary columns — keeps the default view scannable (see `ui-composition.md`).
- For a reusable domain status, prefer a model-cast enum implementing `HasColor` / `HasLabel` / `HasIcon`, so tables, infolists, and forms share semantics. A documented `->color(fn (string $state) => ...)` callback remains valid for local or non-enum state; avoid duplicating the same mapping across surfaces.
