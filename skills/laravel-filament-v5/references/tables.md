# Tables — columns, filters, empty states (`Filament\Tables\*`)

Used inside `public static function table(Table $table): Table`.

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

## Empty state — never a custom "no records" div

The table renders an empty state automatically; customize it on the `Table` object ([doc](https://filamentphp.com/docs/5.x/tables/empty-state.md)):

```php
$table
    ->emptyStateHeading('No posts yet')
    ->emptyStateDescription('Once you write your first post, it will appear here.')
    ->emptyStateIcon(Heroicon::OutlinedBookmark)
    ->emptyStateActions([
        Action::make('create')->label('Create post')->button(),
    ])
```

`->emptyState(view('...'))` exists as a full-custom escape hatch — use only when the heading/description/icon/actions API genuinely can't express the design.

## Table-level conventions

- Actions go in `->recordActions([...])`, `->groupedBulkActions([...])`, `->toolbarActions([...])` — the v3 `->actions()` / `->bulkActions()` no longer exist. Details in `references/actions.md`.
- `->defaultSort('created_at', direction: 'desc')` — every list should have a deliberate default order.
- `->searchable()` on key text columns; `->sortable()` where ordering is meaningful.
- `->toggleable(isToggledHiddenByDefault: true)` for secondary columns — keeps the default view scannable (see `ui-composition.md`).
- Enum-backed badge columns get color/label/icon from the enum's `HasColor`/`HasLabel`/`HasIcon` — never `->color(fn ...)` matching on raw strings.
