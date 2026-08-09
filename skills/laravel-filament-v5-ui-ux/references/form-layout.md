# Form and schema layout compositions

Ready-to-adapt page structure for Filament 5 forms and schemas. Reach for this when deciding how a form page is grouped, columned, or sequenced.

Examples use a `Customer` / `Order` domain consistently across this library.

`laravel-filament-v5` owns field API signatures, validation rules, authorization, and tests. This file owns page structure for the form surface. Field treatment — geometry, labels, guidance, states — comes from `form-fields.md`. Collection, upload, relationship, and rich-content controls come from `form-inputs.md`; compose them inside the page structure chosen here.

| Pattern | Use it for |
|---|---|
| [Flat content](#flat-content) | A small related set that needs no grouping |
| [Responsive columns](#responsive-columns) | Using horizontal space deliberately |
| [Sections](#sections) | Organizing stable groups scanned top to bottom |
| [Aside sections](#aside-sections) | Separating explanatory context from controls |
| [Fieldsets](#fieldsets) | Making a semantic subgroup explicit |
| [Vertical tabs](#vertical-tabs) | Stable groups on a wide panel |
| [Horizontal tabs](#horizontal-tabs) | Stable groups with a short label set |
| [Wizard](#wizard) | A required sequence of dependent steps |
| [Dense layout](#dense-layout) | Increasing information density deliberately |

---

## Flat content

**When**: one short, self-explanatory group would gain no clarity from a container that only adds visual weight.

**Not when**: groups need names, descriptions, or separate actions, or field order or width needs stronger structure.

**Alternatives**: responsive-columns, sections, fieldsets.

**Source**: [schemas/layouts](https://filamentphp.com/docs/5.x/schemas/layouts.md) · [schemas/layout/flex/simple](https://filamentphp.com/docs/images/5.x/light/schemas/layout/flex/simple.jpg)

```php
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Toggle;
use Filament\Schemas\Components\Flex;
use Filament\Schemas\Components\Group;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            Flex::make([
                Group::make([
                    TextInput::make('name')
                        ->required(),
                    TextInput::make('email')
                        ->email()
                        ->required(),
                ]),
                Group::make([
                    Select::make('status')
                        ->options(OrderStatus::class)
                        ->required(),
                    Toggle::make('is_active')
                        ->label('Active customer'),
                ])->grow(false),
            ])->from('md'),
        ]);
}
```

**Responsive**: keep a readable single-column default, and add structure before controls become visually ambiguous.

**Accessibility**: retain visible labels and programmatic grouping when controls form one concept, and do not use visual proximity as the only relationship cue.

---

---

## Responsive columns

**When**: ordinary short related fields can share a row, long fields need space for their expected value, and short high-importance fields need a deliberately prominent span.

**Not when**: a narrow viewport makes multiple columns unreadable, or equal widths obscure information hierarchy.

**Alternatives**: flat-content, sections, dense-layout.

**Source**: [schemas/layouts](https://filamentphp.com/docs/5.x/schemas/layouts.md) · [schemas/layout/grid/column-span](https://filamentphp.com/docs/images/5.x/light/schemas/layout/grid/column-span.jpg)

```php
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Textarea;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            Grid::make([
                'default' => 1,
                'md' => 2,
                'xl' => 3,
            ])
                ->schema([
                    TextInput::make('name')
                        ->required(),
                    TextInput::make('email')
                        ->email()
                        ->required(),
                    Select::make('status')
                        ->options(OrderStatus::class)
                        ->required(),
                    TextInput::make('reference')
                        ->columnSpan([
                            'md' => 1,
                            'xl' => 2,
                        ]),
                    Textarea::make('notes')
                        ->rows(4)
                        ->columnSpanFull(),
                ]),
        ]);
}
```

**Responsive**: define one column before larger breakpoints, and give long, high-importance fields a deliberate full or wider span.

**Accessibility**: preserve a logical DOM and keyboard order when changing visual spans, and never rely on column position to communicate requiredness or sequence.

---

---

## Sections

**When**: two to four named groups scan top to bottom, and descriptions clarify hierarchy.

**Not when**: grouping adds no hierarchy, or users usually work in one of several large groups.

**Alternatives**: [Aside sections](#aside-sections), horizontal-tabs, vertical-tabs, wizard.

**Source**: [schemas/sections](https://filamentphp.com/docs/5.x/schemas/sections.md) · [schemas/layout/section/simple](https://filamentphp.com/docs/images/5.x/light/schemas/layout/section/simple.jpg)

```php
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Textarea;
use Filament\Schemas\Components\Section;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            Section::make('Customer')
                ->description('Who places and receives this order')
                ->columns(2)
                ->schema([
                    TextInput::make('name')
                        ->required(),
                    TextInput::make('email')
                        ->email()
                        ->required(),
                ]),
            Section::make('Order')
                ->description('Status and totals for the current order')
                ->columns(2)
                ->schema([
                    Select::make('status')
                        ->options(OrderStatus::class)
                        ->required(),
                    TextInput::make('total')
                        ->numeric()
                        ->prefix('$')
                        ->required(),
                ]),
            Section::make('Order notes')
                ->description('Internal context that is not required to complete the order')
                ->schema([
                    Textarea::make('notes')
                        ->rows(3),
                ])
                ->collapsible(),
        ]);
}
```

**Responsive**: collapse columns before reducing field readability, and use compact or secondary treatment only when hierarchy remains clear.

**Accessibility**: use headings and descriptions that identify each group, and do not collapse essential content by default.

### Variant: contained

**When**: a named group needs a visible boundary.

**Not when**: the surrounding composition already provides the boundary.

**Source**: [schemas/layout/section/simple](https://filamentphp.com/docs/images/5.x/light/schemas/layout/section/simple.jpg)

Keep the default section card boundary on each named group:

```php
Section::make('Customer')
    ->description('Who places and receives this order')
    ->columns(2)
    ->schema([
        TextInput::make('name')
            ->required(),
        TextInput::make('email')
            ->email()
            ->required(),
    ]),
```

### Variant: compact

**When**: a familiar, low-risk group needs modest density without removing its hierarchy.

**Not when**: help, errors, or touch targets need the default breathing room.

**Source**: [schemas/layout/section/compact](https://filamentphp.com/docs/images/5.x/light/schemas/layout/section/compact.jpg)

Add `compact()` to a familiar supporting group:

```php
Section::make('Order notes')
    ->description('Internal context that is not required to complete the order')
    ->schema([
        Textarea::make('notes')
            ->rows(3),
    ])
    ->compact()
    ->collapsible(),
```

### Variant: secondary

**When**: a supporting group is intentionally lower in the information hierarchy.

**Not when**: the group carries primary task completion.

**Source**: [schemas/layout/section/secondary](https://filamentphp.com/docs/images/5.x/light/schemas/layout/section/secondary.jpg)

Replace the notes section with secondary styling (optionally combined with `compact()`):

```php
Section::make('Order notes')
    ->schema([
        Textarea::make('notes')
            ->rows(3),
    ])
    ->secondary()
    ->compact(),
```

---

---

## Aside sections

**When**: a group heading and description deserve a separate scan lane, and the panel has enough width for context beside controls.

**Not when**: the description is too short to earn a separate lane, or narrow layouts would crowd labels and inputs.

**Alternatives**: [Sections](#sections), vertical-tabs.

**Source**: [schemas/sections](https://filamentphp.com/docs/5.x/schemas/sections.md) · [schemas/layout/section/aside](https://filamentphp.com/docs/images/5.x/light/schemas/layout/section/aside.jpg)

```php
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Textarea;
use Filament\Schemas\Components\Section;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            Section::make('Customer profile')
                ->description('Identity used on invoices, shipping labels, and customer replies')
                ->aside()
                ->schema([
                    TextInput::make('name')
                        ->required(),
                    TextInput::make('email')
                        ->email()
                        ->required(),
                    TextInput::make('phone')
                        ->tel(),
                ]),
            Section::make('Order preferences')
                ->description('Defaults applied when staff create a new order for this customer')
                ->aside()
                ->schema([
                    Select::make('default_status')
                        ->options(OrderStatus::class)
                        ->required(),
                    Textarea::make('fulfillment_notes')
                        ->rows(3),
                ]),
        ]);
}
```

**Responsive**: return heading and controls to a readable vertical flow on narrow screens.

**Accessibility**: associate descriptions with their group rather than encoding meaning only in side-by-side placement, and keep heading order logical when the layout stacks.

---

---

## Fieldsets

**When**: a small subgroup has a shared label, and a visible boundary clarifies a semantic relationship.

**Not when**: the border is purely decorative, or larger groups need descriptions, actions, or stronger hierarchy.

**Alternatives**: flat-content, [Sections](#sections), responsive-columns.

**Source**: [schemas/layouts](https://filamentphp.com/docs/5.x/schemas/layouts.md) · [schemas/layout/fieldset/simple](https://filamentphp.com/docs/images/5.x/light/schemas/layout/fieldset/simple.jpg)

```php
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Fieldset;
use Filament\Schemas\Components\Section;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            Section::make('Customer')
                ->description('Contact details for this customer')
                ->schema([
                    TextInput::make('name')
                        ->required(),
                    Fieldset::make('Shipping address')
                        ->columns([
                            'default' => 1,
                            'md' => 2,
                        ])
                        ->schema([
                            TextInput::make('shipping_line1')
                                ->label('Address line 1')
                                ->required(),
                            TextInput::make('shipping_line2')
                                ->label('Address line 2'),
                            TextInput::make('shipping_city')
                                ->label('City')
                                ->required(),
                            TextInput::make('shipping_postal_code')
                                ->label('Postal code')
                                ->required(),
                        ]),
                ]),
        ]);
}
```

**Responsive**: keep the group readable at one column before adding internal columns.

**Accessibility**: use the fieldset legend as the group name, and ensure the visible boundary reinforces rather than replaces the programmatic group.

### Variant: contained

**When**: a visible border helps separate the subgroup from surrounding controls.

**Not when**: the boundary would duplicate a containing section.

**Source**: [schemas/layout/fieldset/simple](https://filamentphp.com/docs/images/5.x/light/schemas/layout/fieldset/simple.jpg)

Keep the default fieldset border and legend:

```php
Fieldset::make('Shipping address')
    ->columns([
        'default' => 1,
        'md' => 2,
    ])
    ->schema([
        TextInput::make('shipping_line1')
            ->label('Address line 1')
            ->required(),
        TextInput::make('shipping_line2')
            ->label('Address line 2'),
        TextInput::make('shipping_city')
            ->label('City')
            ->required(),
        TextInput::make('shipping_postal_code')
            ->label('Postal code')
            ->required(),
    ]),
```

### Variant: uncontained

**When**: a parent section already makes the subgroup boundary clear.

**Not when**: the subgroup would otherwise blend with unrelated controls.

**Source**: [schemas/layout/fieldset/not-contained](https://filamentphp.com/docs/images/5.x/light/schemas/layout/fieldset/not-contained.jpg)

Add `contained(false)` to drop the fieldset border while keeping the legend:

```php
Fieldset::make('Shipping address')
    ->contained(false)
    ->columns([
        'default' => 1,
        'md' => 2,
    ])
    ->schema([
        TextInput::make('shipping_line1')
            ->label('Address line 1')
            ->required(),
        TextInput::make('shipping_line2')
            ->label('Address line 2'),
        TextInput::make('shipping_city')
            ->label('City')
            ->required(),
        TextInput::make('shipping_postal_code')
            ->label('Postal code')
            ->required(),
    ]),
```

---

## Vertical tabs

**When**: several stable groups, sufficient horizontal space, and navigation labels benefit from persistent scanning.

**Not when**: input is a required sequence, or available width is too narrow for a useful navigation rail.

**Alternatives**: [Horizontal tabs](#horizontal-tabs), sections, [Wizard](#wizard).

**Source**: [schemas/tabs](https://filamentphp.com/docs/5.x/schemas/tabs.md) · [schemas/layout/tabs/vertical](https://filamentphp.com/docs/images/5.x/light/schemas/layout/tabs/vertical.jpg)

```php
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Textarea;
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            Tabs::make('Customer order')
                ->tabs([
                    Tab::make('Customer')
                        ->schema([
                            TextInput::make('name')
                                ->required(),
                            TextInput::make('email')
                                ->email()
                                ->required(),
                        ])
                        ->columns(2),
                    Tab::make('Order')
                        ->schema([
                            Select::make('status')
                                ->options(OrderStatus::class)
                                ->required(),
                            TextInput::make('total')
                                ->numeric()
                                ->prefix('$')
                                ->required(),
                        ])
                        ->columns(2),
                    Tab::make('Billing')
                        ->schema([
                            TextInput::make('billing_name')
                                ->required(),
                            TextInput::make('billing_email')
                                ->email()
                                ->required(),
                        ])
                        ->columns(2),
                    Tab::make('Notes')
                        ->schema([
                            Textarea::make('notes')
                                ->rows(3),
                        ]),
                ])
                ->vertical(),
        ]);
}
```

**Responsive**: verify navigation labels remain usable at narrow widths, and keep fields within each tab responsive through columns and spans.

**Accessibility**: preserve keyboard navigation between the tab list and panels, and do not make the navigation rail the only cue for the active group.

---

---

## Horizontal tabs

**When**: a small number of short group labels and frequent switching between parallel groups.

**Not when**: content must be compared together, labels overflow available width, or input is sequential.

**Alternatives**: [Vertical tabs](#vertical-tabs), sections, [Wizard](#wizard).

**Source**: [schemas/tabs](https://filamentphp.com/docs/5.x/schemas/tabs.md) · [schemas/layout/tabs/simple](https://filamentphp.com/docs/images/5.x/light/schemas/layout/tabs/simple.jpg)

```php
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Textarea;
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            Tabs::make('Customer order')
                ->tabs([
                    Tab::make('Customer')
                        ->schema([
                            TextInput::make('name')
                                ->required(),
                            TextInput::make('email')
                                ->email()
                                ->required(),
                        ])
                        ->columns(2),
                    Tab::make('Order')
                        ->schema([
                            Select::make('status')
                                ->options(OrderStatus::class)
                                ->required(),
                            TextInput::make('total')
                                ->numeric()
                                ->prefix('$')
                                ->required(),
                        ])
                        ->columns(2),
                    Tab::make('Notes')
                        ->schema([
                            Textarea::make('notes')
                                ->rows(3),
                        ]),
                ])
                ->persistTabInQueryString(),
        ]);
}
```

**Responsive**: test label overflow and the overflow menu on narrow screens, and do not hide always-needed content behind a non-default tab.

**Accessibility**: keep keyboard tab navigation and focus management intact, and make the active panel and tab relationship perceivable.

### Variant: contained

**When**: the tab set needs a distinct boundary from surrounding content.

**Not when**: a surrounding section already provides that boundary.

**Source**: [schemas/layout/tabs/simple](https://filamentphp.com/docs/images/5.x/light/schemas/layout/tabs/simple.jpg)

Keep the default card container around the tabs (do not call `contained(false)`):

```php
Tabs::make('Customer order')
    ->tabs([
        Tab::make('Customer')
            ->schema([
                TextInput::make('name')
                    ->required(),
                TextInput::make('email')
                    ->email()
                    ->required(),
            ])
            ->columns(2),
        Tab::make('Order')
            ->schema([
                Select::make('status')
                    ->options(OrderStatus::class)
                    ->required(),
                TextInput::make('total')
                    ->numeric()
                    ->prefix('$')
                    ->required(),
            ])
            ->columns(2),
        Tab::make('Notes')
            ->schema([
                Textarea::make('notes')
                    ->rows(3),
            ]),
    ])
    ->persistTabInQueryString(),
```

### Variant: uncontained

**When**: the parent composition supplies the needed hierarchy and container chrome would be redundant.

**Not when**: the active panel would lose a clear visual relationship to its tabs.

**Source**: [schemas/layout/tabs/not-contained](https://filamentphp.com/docs/images/5.x/light/schemas/layout/tabs/not-contained.jpg)

Add `contained(false)` after `tabs([...])`:

```php
->contained(false)
```

### Variant: overflow menu

**When**: parallel groups remain valid but labels exceed the available horizontal space.

**Not when**: hidden labels would make essential groups hard to discover.

**Source**: [schemas/layout/tabs/not-scrollable](https://filamentphp.com/docs/images/5.x/light/schemas/layout/tabs/not-scrollable.jpg)

Add `scrollable(false)` so overflowing tabs move into the dropdown instead of scrolling:

```php
->scrollable(false)
```

---

---

## Wizard

**When**: later input depends on earlier choices, and completion benefits from an explicit ordered path.

**Not when**: users need to complete groups in any order, or the steps only partition parallel content.

**Alternatives**: sections, [Horizontal tabs](#horizontal-tabs), [Vertical tabs](#vertical-tabs).

**Source**: [schemas/wizards](https://filamentphp.com/docs/5.x/schemas/wizards.md) · [schemas/layout/wizard/simple](https://filamentphp.com/docs/images/5.x/light/schemas/layout/wizard/simple.jpg)

```php
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Wizard;
use Filament\Schemas\Components\Wizard\Step;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            Wizard::make([
                Step::make('Customer')
                    ->description('Who places this order')
                    ->schema([
                        TextInput::make('name')
                            ->required(),
                        TextInput::make('email')
                            ->email()
                            ->required(),
                    ])
                    ->columns(2),
                Step::make('Order')
                    ->description('Status and total for the order')
                    ->schema([
                        Select::make('status')
                            ->options(OrderStatus::class)
                            ->required(),
                        TextInput::make('total')
                            ->numeric()
                            ->prefix('$')
                            ->required(),
                    ])
                    ->columns(2),
                Step::make('Billing')
                    ->description('Where the invoice is sent')
                    ->schema([
                        TextInput::make('billing_name')
                            ->required(),
                        TextInput::make('billing_email')
                            ->email()
                            ->required(),
                    ])
                    ->columns(2),
            ])
                ->skippable(),
        ]);
}
```

**Responsive**: keep step labels concise and ensure navigation controls remain reachable on narrow screens.

**Accessibility**: communicate current step and completion state programmatically, and do not prevent correction of earlier steps without a clear recovery path.

---

## Dense layout

**When**: repetition makes default spacing unnecessarily slow to scan, and adjacent controls remain clearly distinguishable.

**Not when**: new or error-prone input needs breathing room, or reduced gaps would blur labels, errors, or touch targets.

**Alternatives**: responsive-columns, sections, flat-content.

**Source**: [schemas/layouts](https://filamentphp.com/docs/5.x/schemas/layouts.md) · [schemas/layout/dense](https://filamentphp.com/docs/images/5.x/light/schemas/layout/dense.jpg)

```php
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Toggle;
use Filament\Schemas\Components\Fieldset;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            Fieldset::make('Order flags')
                ->dense()
                ->columns([
                    'default' => 1,
                    'md' => 2,
                ])
                ->schema([
                    Toggle::make('is_priority')
                        ->label('Priority order'),
                    Toggle::make('requires_signature')
                        ->label('Requires signature'),
                    Toggle::make('is_gift')
                        ->label('Gift wrap'),
                    Select::make('status')
                        ->options(OrderStatus::class)
                        ->required(),
                    TextInput::make('internal_code'),
                    TextInput::make('warehouse_bin'),
                ]),
        ]);
}
```

**Responsive**: restore spacing before labels, errors, or touch targets become crowded on smaller screens.

**Accessibility**: preserve readable error separation and pointer target size, and do not use dense spacing to conceal required instructions.

### Variant: dense

**When**: repeated low-risk controls remain individually scannable with reduced spacing.

**Not when**: the task is new, error-prone, or instruction-heavy.

**Source**: [schemas/layout/dense](https://filamentphp.com/docs/images/5.x/light/schemas/layout/dense.jpg)

Keep `dense()` on the `Fieldset` skeleton:

```php
use Filament\Schemas\Components\Fieldset;

Fieldset::make('Order flags')
    ->dense()
    ->columns([
        'default' => 1,
        'md' => 2,
    ])
    ->schema([
        // ...
    ]),
```

### Variant: compact section

**When**: the group needs its own hierarchy but less vertical padding.

**Not when**: secondary density would weaken the group heading or description.

**Source**: [schemas/layout/section/compact](https://filamentphp.com/docs/images/5.x/light/schemas/layout/section/compact.jpg)

Replace the `Fieldset` with a compact `Section`:

```php
use Filament\Schemas\Components\Section;

Section::make('Order flags')
    ->description('Low-risk toggles and codes scanned together during fulfillment')
    ->schema([
        // ...
    ])
    ->compact(),
```

### Variant: no gap

**When**: adjacent controls are perceived as one tightly related unit.

**Not when**: reduced spacing would blur labels, errors, instructions, or touch targets.

**Source**: [schemas/layout/no-gap](https://filamentphp.com/docs/images/5.x/light/schemas/layout/no-gap.jpg)

Replace `dense()` with `gap(false)` on the `Fieldset`:

```php
use Filament\Schemas\Components\Fieldset;

Fieldset::make('Order flags')
    ->gap(false)
    ->columns([
        'default' => 1,
        'md' => 2,
    ])
    ->schema([
        // ...
    ]),
```
