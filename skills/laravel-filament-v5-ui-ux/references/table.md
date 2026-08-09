# Table compositions

Ready-to-adapt table compositions for Filament 5. Pick the one whose `When` matches the task, paste it, and rename the model, columns, and relations to the target domain.

Examples use a `Customer` / `Order` domain consistently across this library.

`laravel-filament-v5` owns field API signatures, authorization, and tests. This file owns how the components are arranged.

| Pattern | Use it for |
|---|---|
| [Standard compare-and-scan table](#standard-compare-and-scan-table) | Comparing the same facts across many peer records |
| [Responsive identity-centred table](#responsive-identity-centred-table) | Records whose identity matters more than column comparison |

---

## Standard compare-and-scan table

**When**: people need to compare the same decision-relevant facts across many records, and identity, state, facts, dates, and actions have a stable scanning order.

**Not when**: each record needs materially different rich content that cannot stay comparable in a row, or a detail-first layout is required by the task rather than by visual preference.

**Alternatives**: [Responsive identity-centred table](#responsive-identity-centred-table).

**Source**: [tables/overview](https://filamentphp.com/docs/5.x/tables/overview.md) · [overview/columns](https://filamentphp.com/docs/images/5.x/light/tables/overview/columns.jpg)

```php
use Filament\Actions\ActionGroup;
use Filament\Actions\DeleteAction;
use Filament\Actions\EditAction;
use Filament\Actions\ViewAction;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;

public static function table(Table $table): Table
{
    return $table
        ->columns([
            TextColumn::make('name')
                ->searchable()
                ->sortable(),
            TextColumn::make('status')
                ->badge()
                ->sortable(),
            TextColumn::make('total_spent')
                ->money('USD')
                ->sortable(),
            TextColumn::make('email')
                ->searchable()
                ->toggleable(isToggledHiddenByDefault: true),
            TextColumn::make('created_at')
                ->dateTime()
                ->sortable()
                ->toggleable(isToggledHiddenByDefault: true),
        ])
        ->defaultSort('created_at', direction: 'desc')
        ->recordActions([
            ActionGroup::make([
                ViewAction::make(),
                EditAction::make(),
                DeleteAction::make(),
            ]),
        ]);
}
```

**Responsive**: keep identity and the state that drives the decision before collapsing secondary information; do not turn every row into a card merely because the viewport narrows.

**Accessibility**: associate headers with their values, name icon-only controls, and keep sorting, filtering, pagination, selection, and empty-state meaning perceivable without colour alone.

### Variant: purposeful filters

**When**: users repeatedly need a named subset such as a status, owner, date range, or exception.

**Not when**: the filter substitutes for an obvious column or a simple search, or hides results without explanation.

**Source**: [overview/filters](https://filamentphp.com/docs/images/5.x/light/tables/overview/filters.jpg)

Add `filters()` to the table:

```php
use Filament\Tables\Filters\Filter;
use Filament\Tables\Filters\SelectFilter;
use Illuminate\Database\Eloquent\Builder;

->filters([
    SelectFilter::make('status')
        ->options([
            'active' => 'Active',
            'suspended' => 'Suspended',
            'closed' => 'Closed',
        ]),
    Filter::make('has_orders')
        ->query(fn (Builder $query) => $query->has('orders')),
])
```

### Variant: keep the common action direct

**When**: one frequent row action should stay one click away while secondary or destructive actions would crowd the row.

**Not when**: the only common next step ends up hidden inside an ambiguous menu.

**Source**: [actions/group](https://filamentphp.com/docs/images/5.x/light/tables/actions/group.jpg)

Replace the single `ActionGroup` in `recordActions()`:

```php
->recordActions([
    EditAction::make(),
    ActionGroup::make([
        ViewAction::make(),
        DeleteAction::make(),
    ]),
])
```

### Variant: state that reads without colour

**When**: state changes the user's decision and needs a concise, scannable label or conventional icon.

**Not when**: colour alone — including red versus green — is the only way to understand the value.

**Source**: [overview/columns](https://filamentphp.com/docs/images/5.x/light/tables/overview/columns.jpg)

Use a badge with a label for domain state, and a boolean icon only for true/false facts:

```php
use Filament\Tables\Columns\IconColumn;

TextColumn::make('status')
    ->badge()
    ->sortable(),
IconColumn::make('is_verified')
    ->boolean()
    ->label('Verified'),
```

### Variant: bulk selection

**When**: users operate on several records at once and the scope, consequences, confirmation, and recovery are clear.

**Not when**: mixed records make the operation unsafe, or the interface implies selection spans pages without explicit support.

**Source**: [actions/bulk](https://filamentphp.com/docs/images/5.x/light/tables/actions/bulk.jpg)

Add `toolbarActions()` to the table. A domain bulk action states its scope through per-record authorization and reports what actually happened — the user cannot see which records were skipped:

```php
use Filament\Actions\BulkAction;
use Filament\Actions\BulkActionGroup;
use Filament\Actions\DeleteBulkAction;
use Illuminate\Database\Eloquent\Collection;

->toolbarActions([
    BulkActionGroup::make([
        BulkAction::make('markShipped')
            ->label('Mark as shipped')
            ->requiresConfirmation()
            ->authorizeIndividualRecords('update')
            ->successNotificationTitle('Orders marked as shipped')
            ->failureNotificationTitle(
                fn (int $successCount, int $failureCount): string => "{$successCount} marked, {$failureCount} skipped",
            )
            ->action(fn (Collection $records) => $records->each->markShipped()),
        DeleteBulkAction::make(),
    ]),
])
```

### Variant: distinguish empty from filtered-empty

**When**: the table must separate an initial absence of records from a filter that matched nothing.

**Not when**: a filtered empty result invites duplicate creation instead of surfacing the active filters and a reset.

**Source**: [empty-state](https://filamentphp.com/docs/images/5.x/light/tables/empty-state.jpg)

Customize the empty state on the table:

```php
use Filament\Actions\Action;
use Filament\Support\Icons\Heroicon;

->emptyStateHeading('No customers yet')
->emptyStateDescription('Once your first customer signs up, they will appear here.')
->emptyStateIcon(Heroicon::OutlinedUsers)
->emptyStateActions([
    Action::make('create')
        ->label('Add customer')
        ->button(),
])
```

### Variant: group rows by a shared attribute

**When**: a shared attribute such as workflow state or a date bucket is a useful scan boundary.

**Not when**: cross-group comparison matters more than the boundary, or collapsed groups would hide discoverable records.

**Source**: [grouping](https://filamentphp.com/docs/images/5.x/light/tables/grouping.jpg)

Add a default group to the table — a deliberate alternative to a redundant status column:

```php
use Filament\Tables\Grouping\Group;

->defaultGroup(
    Group::make('status')
        ->label('State'),
)
```

### Variant: aggregate that changes a decision

**When**: a total, count, or average changes a table-level decision.

**Not when**: the aggregate is decorative, competes with row data, or its filter and pagination scope is unclear.

**Source**: [summaries](https://filamentphp.com/docs/images/5.x/light/tables/summaries.jpg)

Add a summarizer to the column it belongs to. The first column cannot carry one:

```php
use Filament\Tables\Columns\Summarizers\Sum;

TextColumn::make('total_spent')
    ->money('USD')
    ->sortable()
    ->summarize(
        Sum::make()
            ->label('Total, current results'),
    ),
```

Name the scope in the label. A bare total reads as "all records" even when filters are active.

### Variant: pagination that preserves position

**When**: a large result set needs a visible range and page navigation that keeps comparison context.

**Not when**: simpler pagination would stop users from reaching distant pages or understanding where they are.

**Source**: [pagination/default](https://filamentphp.com/docs/images/5.x/light/tables/pagination/default.jpg)

Tune pagination on the table:

```php
->paginated([10, 25, 50, 100, 'all'])
->defaultPaginationPageOption(25)
->extremePaginationLinks()
```

---

## Responsive identity-centred table

**When**: one record's identity and grouped details matter more than comparing the same facts across rows; a desktop row should express an identity-first hierarchy before becoming a mobile stack.

**Not when**: people must compare the same facts across many peer records, or a card-like layout is proposed only for visual novelty.

**Alternatives**: [Standard compare-and-scan table](#standard-compare-and-scan-table).

**Source**: [tables/layout](https://filamentphp.com/docs/5.x/tables/layout.md) · [split-desktop](https://filamentphp.com/docs/images/5.x/light/tables/layout/split-desktop.jpg) · [split-desktop/mobile](https://filamentphp.com/docs/images/5.x/light/tables/layout/split-desktop/mobile.jpg)

```php
use Filament\Actions\ActionGroup;
use Filament\Actions\EditAction;
use Filament\Actions\ViewAction;
use Filament\Support\Enums\FontWeight;
use Filament\Tables\Columns\ImageColumn;
use Filament\Tables\Columns\Layout\Split;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;

public static function table(Table $table): Table
{
    return $table
        ->columns([
            Split::make([
                ImageColumn::make('avatar')
                    ->circular(),
                TextColumn::make('name')
                    ->weight(FontWeight::Bold)
                    ->searchable()
                    ->sortable(),
                TextColumn::make('email')
                    ->icon('heroicon-m-envelope'),
                TextColumn::make('status')
                    ->badge(),
            ])->from('md'),
        ])
        ->recordActions([
            ActionGroup::make([
                ViewAction::make(),
                EditAction::make(),
            ]),
        ]);
}
```

**Responsive**: reorganize identity, state, details, and actions at the breakpoint instead of shrinking desktop columns. Keep the primary action discoverable when content stacks or collapses.

**Accessibility**: preserve reading order across `Split`, `Stack`, and `Grid` transforms; keep visible focus for selection, expand/collapse, and row actions; never let colour or position be the only carrier of state.

### Variant: stack related details

**When**: contact, status, or metadata details read better as one vertical unit inside the record.

**Not when**: those facts are independent and need peer comparison across rows.

**Source**: [stack](https://filamentphp.com/docs/images/5.x/light/tables/layout/stack.jpg)

Replace the flat `email` column inside the `Split`:

```php
use Filament\Tables\Columns\Layout\Stack;

Stack::make([
    TextColumn::make('email')
        ->icon('heroicon-m-envelope'),
    TextColumn::make('phone')
        ->icon('heroicon-m-phone'),
])->space(1),
```

### Variant: fixed-width identity

**When**: a short identity or fixed-width fact should keep its natural width while the rest of the line absorbs the free space.

**Not when**: disabling growth truncates decision-critical content or displaces the row action.

**Source**: [grow-disabled](https://filamentphp.com/docs/images/5.x/light/tables/layout/grow-disabled.jpg)

Add `grow(false)` to the columns that should not stretch:

```php
ImageColumn::make('avatar')
    ->circular()
    ->grow(false),
```

### Variant: hide secondary details on mobile

**When**: a secondary detail can disappear at a narrow breakpoint because an equivalent identity, state, or action cue remains.

**Not when**: the hidden content is the only way to understand state or discover an action.

**Source**: [stack-hidden-on-mobile](https://filamentphp.com/docs/images/5.x/light/tables/layout/stack-hidden-on-mobile.jpg)

Add `visibleFrom()` to the stacked details:

```php
Stack::make([
    TextColumn::make('email')
        ->icon('heroicon-m-envelope'),
    TextColumn::make('phone')
        ->icon('heroicon-m-phone'),
])->visibleFrom('md'),
```

### Variant: collapsible secondary details

**When**: secondary details have a meaningful summary, and identity, state, and the recurring action stay visible while collapsed.

**Not when**: the collapsed content is needed for the recurring task, selection, or error recovery.

**Source**: [collapsible](https://filamentphp.com/docs/images/5.x/light/tables/layout/collapsible.jpg) · [collapsible/mobile](https://filamentphp.com/docs/images/5.x/light/tables/layout/collapsible/mobile.jpg)

Add a `Panel` as a second entry in `columns()`, after the `Split`:

```php
use Filament\Tables\Columns\Layout\Panel;
use Filament\Tables\Columns\Layout\Stack;

Panel::make([
    Stack::make([
        TextColumn::make('phone')
            ->icon('heroicon-m-phone'),
        TextColumn::make('address')
            ->icon('heroicon-m-map-pin'),
    ]),
])->collapsible(),
```

### Variant: grid-grouped details

**When**: grouped peer details deserve equal tracks while the record stays identity-centred. Use this when `Split` produces inconsistent widths because some rows carry much more content.

**Not when**: equal tracks flatten the hierarchy, or the task actually needs an aligned standard table.

**Source**: [column-grid](https://filamentphp.com/docs/images/5.x/light/tables/layout/column-grid.jpg)

Replace the detail columns with a `Grid`:

```php
use Filament\Tables\Columns\Layout\Grid;

Grid::make([
    'lg' => 2,
])
    ->schema([
        TextColumn::make('email')
            ->icon('heroicon-m-envelope'),
        TextColumn::make('phone')
            ->icon('heroicon-m-phone'),
    ]),
```

### Variant: records as a content grid

**When**: independent identity units stay scannable as responsive cards at wider breakpoints.

**Not when**: cross-record comparison needs persistent column alignment.

**Source**: [grid](https://filamentphp.com/docs/images/5.x/light/tables/layout/grid.jpg) · [grid/mobile](https://filamentphp.com/docs/images/5.x/light/tables/layout/grid/mobile.jpg)

Wrap the columns in a single `Stack` and add `contentGrid()` to the table:

```php
use Filament\Tables\Columns\Layout\Stack;

return $table
    ->columns([
        Stack::make([
            ImageColumn::make('avatar')
                ->circular(),
            TextColumn::make('name')
                ->weight(FontWeight::Bold)
                ->searchable(),
            TextColumn::make('email')
                ->icon('heroicon-m-envelope'),
        ]),
    ])
    ->contentGrid([
        'md' => 2,
        'xl' => 3,
    ]);
```
