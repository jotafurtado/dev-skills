# Record detail compositions

Ready-to-adapt read-oriented record detail compositions for Filament 5. Pick the one whose `When` matches the task, paste it, and rename the model, entries, and relations to the target domain.

Examples use a `Customer` / `Order` domain consistently across this library.

`laravel-filament-v5` owns field API signatures, authorization, and tests. This file owns how the components are arranged.

| Pattern | Use it for |
|---|---|
| [Record detail infolist](#record-detail-infolist) | Recognising one Order and its current state before scanning supporting facts and history |

---

## Record detail infolist

**When**: a person needs to recognise one record and its current state before scanning its supporting facts, while compact primary facts stay ahead of history, repeated data, or supporting media.

**Not when**: staff must compare the same facts across many peer records, which requires a table, or the surface is an edit workflow rather than a read-oriented record detail.

**Alternatives**: simple-detail-page, two-zone-detail-page, tabbed-secondary-detail.

**Source**: [infolists/overview](https://filamentphp.com/docs/5.x/infolists/overview.md) · [resources/viewing-records](https://filamentphp.com/docs/5.x/resources/viewing-records.md) · [infolists/overview](https://filamentphp.com/docs/images/5.x/light/infolists/overview.jpg)

Put identity and current state first, then the primary facts people use most often, then secondary fulfilment detail and history:

```php
use Filament\Infolists\Components\IconEntry;
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Components\Flex;
use Filament\Schemas\Components\Section;
use Filament\Schemas\Schema;

public static function infolist(Schema $schema): Schema
{
    return $schema
        ->components([
            Flex::make([
                Section::make([
                    TextEntry::make('number')
                        ->label('Order'),
                    TextEntry::make('status')
                        ->badge(),
                    TextEntry::make('customer.name')
                        ->label('Customer'),
                ]),
                Section::make([
                    TextEntry::make('total')
                        ->money('USD'),
                    TextEntry::make('placed_at')
                        ->dateTime(),
                    TextEntry::make('payment_method')
                        ->label('Payment'),
                ])->grow(false),
            ])->from('md'),
            Section::make('Fulfilment')
                ->schema([
                    TextEntry::make('shipping_method')
                        ->label('Shipping'),
                    TextEntry::make('tracking_number')
                        ->label('Tracking')
                        ->placeholder('Not provided'),
                    IconEntry::make('is_paid')
                        ->label('Paid')
                        ->boolean(),
                ]),
            Section::make('History')
                ->schema([
                    TextEntry::make('last_status_change_at')
                        ->label('Last status change')
                        ->since()
                        ->dateTimeTooltip(),
                    TextEntry::make('notes')
                        ->placeholder('No notes'),
                ]),
        ]);
}
```

**Responsive**: keep identity, current status, and the primary facts before secondary metadata when the layout stacks.

**Accessibility**: pair status badges and icons with readable text so state is not communicated by colour alone, and retain visible labels or an equivalent accessible name for every fact, including placeholders for absent values.

### Variant: Two-zone identity and facts

**When**: identity and current state need to stay prominent while compact facts form a scannable adjacent or following block.

**Not when**: the record is too small to justify a second zone or its facts require a larger navigable secondary surface.

**Source**: [infolists/entries/simple](https://filamentphp.com/docs/images/5.x/light/infolists/entries/simple.jpg)

Keep the `Flex` two-zone block at the top of the skeleton — identity and status in the growing section, compact money and timing facts in the non-growing section:

```php
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Components\Flex;
use Filament\Schemas\Components\Section;

Flex::make([
    Section::make([
        TextEntry::make('number')
            ->label('Order'),
        TextEntry::make('status')
            ->badge(),
        TextEntry::make('customer.name')
            ->label('Customer'),
    ]),
    Section::make([
        TextEntry::make('total')
            ->money('USD'),
        TextEntry::make('placed_at')
            ->dateTime(),
        TextEntry::make('payment_method')
            ->label('Payment'),
    ])->grow(false),
])->from('md'),
```

### Variant: Status badge and icon

**When**: a current status or conventional boolean changes the next decision and needs a compact semantic cue.

**Not when**: colour or an unlabelled icon would be the only explanation of state.

**Source**: [infolists/entries/text/badge](https://filamentphp.com/docs/images/5.x/light/infolists/entries/text/badge.jpg)

Keep the labelled status badge and paid icon in the skeleton — reinforce state with colour only after the text label is present:

```php
use Filament\Infolists\Components\IconEntry;
use Filament\Infolists\Components\TextEntry;

TextEntry::make('status')
    ->badge()
    ->color(fn (string $state): string => match ($state) {
        'pending' => 'gray',
        'processing' => 'warning',
        'shipped' => 'info',
        'completed' => 'success',
        'cancelled' => 'danger',
        default => 'gray',
    }),
IconEntry::make('is_paid')
    ->label('Paid')
    ->boolean(),
```

### Variant: Inline label facts

**When**: many short, stable fact labels and values need to conserve vertical space without losing their association.

**Not when**: values are long, labels are ambiguous, or the stacked narrow layout is more readable.

**Source**: [infolists/entries/inline-label/section](https://filamentphp.com/docs/images/5.x/light/infolists/entries/inline-label/section.jpg)

Replace the Fulfilment section with an inline-label block for short stable pairs:

```php
use Filament\Infolists\Components\IconEntry;
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Components\Section;

Section::make('Fulfilment')
    ->inlineLabel()
    ->schema([
        TextEntry::make('shipping_method')
            ->label('Shipping'),
        TextEntry::make('tracking_number')
            ->label('Tracking')
            ->placeholder('Not provided'),
        IconEntry::make('is_paid')
            ->label('Paid')
            ->boolean(),
    ]),
```

### Variant: Simple detail page

**When**: a record has a short, self-explanatory set of facts that can be read in one flow.

**Not when**: identity, current state, and a larger set of supporting metadata need separate visual priority.

**Source**: [infolists/overview](https://filamentphp.com/docs/images/5.x/light/infolists/overview.jpg)

Replace the whole `components([...])` body with one short vertical flow when a second zone would add no hierarchy:

```php
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Schema;

public static function infolist(Schema $schema): Schema
{
    return $schema
        ->components([
            TextEntry::make('number')
                ->label('Order'),
            TextEntry::make('status')
                ->badge(),
            TextEntry::make('customer.name')
                ->label('Customer'),
            TextEntry::make('total')
                ->money('USD'),
            TextEntry::make('placed_at')
                ->dateTime(),
            TextEntry::make('notes')
                ->placeholder('No notes')
                ->columnSpanFull(),
        ]);
}
```

### Variant: Placeholder for absent fact

**When**: an absent expected value must remain distinguishable from an omitted or loading fact.

**Not when**: a placeholder would add noise to optional information with no user consequence.

**Source**: [infolists/entries/placeholder](https://filamentphp.com/docs/images/5.x/light/infolists/entries/placeholder.jpg)

Keep `placeholder()` only on expected absences that change the next decision, such as tracking or notes:

```php
use Filament\Infolists\Components\TextEntry;

TextEntry::make('tracking_number')
    ->label('Tracking')
    ->placeholder('Not provided'),
TextEntry::make('notes')
    ->placeholder('No notes'),
```

### Variant: Media and copyable identity

**When**: recognition media or a high-value identifier helps users verify, share, or act on the record.

**Not when**: decorative media competes with identity or copying is not a meaningful user task.

**Source**: [infolists/entries/text/copyable](https://filamentphp.com/docs/images/5.x/light/infolists/entries/text/copyable.jpg)

Add recognition media with a visible limit, and make the order number copyable for escalation:

```php
use Filament\Infolists\Components\ImageEntry;
use Filament\Infolists\Components\TextEntry;

ImageEntry::make('customer.avatar')
    ->label('Customer')
    ->circular()
    ->imageSize(40),
ImageEntry::make('attachments')
    ->label('Attachments')
    ->square()
    ->limit(3)
    ->limitedRemainingText(),
TextEntry::make('number')
    ->label('Order')
    ->copyable()
    ->copyMessage('Order number copied'),
```

### Variant: Repeatable secondary detail

**When**: a record contains structured repeated facts, media, or history that users need to inspect as units.

**Not when**: a compact summary is enough or a large history needs a dedicated related-record surface.

**Source**: [infolists/entries/repeatable/table](https://filamentphp.com/docs/images/5.x/light/infolists/entries/repeatable/table.jpg)

Replace the History section with a table-layout repeatable for order items after identity and primary facts:

```php
use Filament\Infolists\Components\RepeatableEntry;
use Filament\Infolists\Components\RepeatableEntry\TableColumn;
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Components\Section;

Section::make('Items')
    ->schema([
        RepeatableEntry::make('items')
            ->table([
                TableColumn::make('Item'),
                TableColumn::make('Quantity'),
                TableColumn::make('Total'),
            ])
            ->schema([
                TextEntry::make('name'),
                TextEntry::make('quantity'),
                TextEntry::make('total')
                    ->money('USD'),
            ]),
    ]),
```

### Variant: Tabbed secondary detail

**When**: several sizeable secondary groups such as history, related records, or media would obscure primary identity and facts in one long page.

**Not when**: only a few short groups remain easy to scan in a single detail flow.

**Source**: [schemas/layout/tabs/simple](https://filamentphp.com/docs/images/5.x/light/schemas/layout/tabs/simple.jpg)

Keep the identity `Flex` first, then move Fulfilment and History into tabs so secondary groups stay reachable without burying current state:

```php
use Filament\Infolists\Components\IconEntry;
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;

Tabs::make('Order details')
    ->tabs([
        Tab::make('Fulfilment')
            ->schema([
                TextEntry::make('shipping_method')
                    ->label('Shipping'),
                TextEntry::make('tracking_number')
                    ->label('Tracking')
                    ->placeholder('Not provided'),
                IconEntry::make('is_paid')
                    ->label('Paid')
                    ->boolean(),
            ]),
        Tab::make('History')
            ->schema([
                TextEntry::make('last_status_change_at')
                    ->label('Last status change')
                    ->since()
                    ->dateTimeTooltip(),
                TextEntry::make('notes')
                    ->placeholder('No notes'),
            ]),
    ]),
```

### Variant: Collapsed long-tail detail

**When**: long-tail information has a meaningful summary and is not needed for the recurring decision.

**Not when**: the hidden information contains current status, primary identity, error recovery, or a common action.

**Source**: [infolists/entries/text/expandable-limited-list](https://filamentphp.com/docs/images/5.x/light/infolists/entries/text/expandable-limited-list.jpg)

Add an expandable limited list only after identity and current state remain visible — never collapse status or the order number into it:

```php
use Filament\Infolists\Components\TextEntry;

TextEntry::make('status_events')
    ->label('Earlier status events')
    ->listWithLineBreaks()
    ->limitList(3)
    ->expandableLimitedList(),
```
