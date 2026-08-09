# Ordinary form field compositions

Ready-to-adapt presentation for everyday Filament 5 form fields. Reach for this when deciding a field's geometry, labelling, guidance, or state.

Examples use a `Customer` / `Order` domain consistently across this library.

`laravel-filament-v5` owns field API signatures, validation rules, authorization, and tests. Page structure is owned by `form-layout.md`.

| Pattern | Use it for |
|---|---|
| [Ordinary field composition](#ordinary-field-composition) | Geometry, labels, guidance, and states of everyday fields |

---

## Ordinary field composition

**When**: ordinary fields need labels, expected-value guidance, and clear state feedback.

**Not when**: the problem is primarily page-level grouping, sequencing, or navigation.

**Alternatives**: responsive-columns (`form-layout.md`), fieldsets (`form-layout.md`), sections (`form-layout.md`), aside-sections (`form-layout.md`).

**Source**: [forms/overview](https://filamentphp.com/docs/5.x/forms/overview.md) · [forms/fields/simple](https://filamentphp.com/docs/images/5.x/light/forms/fields/simple.jpg)

```php
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            TextInput::make('name')
                ->label('Customer name')
                ->required()
                ->maxLength(255),
            TextInput::make('email')
                ->label('Email address')
                ->email()
                ->required(),
            TextInput::make('phone')
                ->label('Phone number'),
        ]);
}
```

**Responsive**: start with a readable one-column field flow, then let related short fields share rows at wider breakpoints.

**Accessibility**: labels identify fields and remain visible unless an accessible hidden-label treatment is necessary.

### Variant: Ordinary wrapper

**When**: the label, input, and any feedback need the familiar vertical reading order.

**Not when**: the form is a known dense, repetitive set whose short labels and values remain easy to scan inline.

**Source**: [forms/fields/simple](https://filamentphp.com/docs/images/5.x/light/forms/fields/simple.jpg)

Keep the default vertical label-above-input arrangement on each ordinary field:

```php
TextInput::make('name')
    ->label('Customer name')
    ->required()
    ->maxLength(255),
```

### Variant: Field-level guidance

**When**: a concise instruction, example, unit, or consequence directly qualifies one field.

**Not when**: the text merely repeats the label or explains a broader workflow, policy, or risk.

**Source**: [forms/fields/below-content/text](https://filamentphp.com/docs/images/5.x/light/forms/fields/below-content/text.jpg)

Add `belowContent()` beside the field it qualifies:

```php
TextInput::make('email')
    ->label('Email address')
    ->email()
    ->required()
    ->belowContent('Order receipts and shipping updates are sent to this address.'),
```

### Variant: Placeholder example

**When**: an empty input benefits from a short, realistic example of its expected value.

**Not when**: the text would replace the label, required state, instructions, or validation feedback.

**Source**: [forms/fields/placeholder](https://filamentphp.com/docs/images/5.x/light/forms/fields/placeholder.jpg)

Add `placeholder()` as an example value, not as a substitute for the label:

```php
TextInput::make('name')
    ->label('Customer name')
    ->placeholder('Jane Cooper')
    ->required()
    ->maxLength(255),
```

### Variant: Disabled and validation states

**When**: the field is unavailable or requires immediate correction and its reason or feedback can be made clear.

**Not when**: a disabled control hides the reason, removes needed recovery, or relies on color alone to communicate the state.

**Source**: [forms/validation](https://filamentphp.com/docs/images/5.x/light/forms/validation.jpg)

Mark required fields with `required()`, and pair `disabled()` with nearby guidance that states why the value cannot be edited:

```php
TextInput::make('email')
    ->label('Email address')
    ->email()
    ->required(),
TextInput::make('customer_number')
    ->label('Customer number')
    ->disabled()
    ->belowContent('Assigned when the customer is created and cannot be edited.'),
```

### Variant: Adjoined affix

**When**: a prefix or suffix is part of how the value is read, such as a URL scheme, currency, or unit.

**Not when**: the content is optional guidance, an unrelated action, or broad context rather than part of the value.

**Source**: [forms/fields/text-input/affix](https://filamentphp.com/docs/images/5.x/light/forms/fields/text-input/affix.jpg)

Replace a plain amount field with adjoined `prefix()` / `suffix()` text that belongs to the value:

```php
TextInput::make('order_total')
    ->label('Order total')
    ->numeric()
    ->prefix('$')
    ->suffix('USD')
    ->required(),
```

### Variant: Inline label

**When**: a dense, familiar form has short stable labels and vertical space is genuinely constrained.

**Not when**: labels, instructions, validation, or long values need the full line to remain scannable.

**Source**: [forms/fields/inline-label](https://filamentphp.com/docs/images/5.x/light/forms/fields/inline-label.jpg)

Add `inlineLabel()` on short, familiar fields:

```php
TextInput::make('name')
    ->label('Customer name')
    ->inlineLabel()
    ->required()
    ->maxLength(255),
TextInput::make('email')
    ->label('Email address')
    ->email()
    ->inlineLabel()
    ->required(),
TextInput::make('phone')
    ->label('Phone number')
    ->inlineLabel(),
```

### Variant: Auxiliary content

**When**: an immediate field-specific action or component helps complete, verify, or understand that field.

**Not when**: the action or information applies to multiple fields or the workflow and belongs in contextual guidance instead.

**Source**: [forms/fields/below-content/action](https://filamentphp.com/docs/images/5.x/light/forms/fields/below-content/action.jpg)

Add a field-scoped action through `belowContent()`:

```php
use Filament\Actions\Action;

TextInput::make('email')
    ->label('Email address')
    ->email()
    ->required()
    ->belowContent(
        Action::make('verifyEmail')
            ->label('Send verification'),
    ),
```

### Variant: Fused fields

**When**: two or more values form one compact concept, such as location or a measured value with a unit.

**Not when**: the controls are independently understood, require separate guidance or errors, or would become unreadable on narrow screens.

**Source**: [forms/fields/fused-label](https://filamentphp.com/docs/images/5.x/light/forms/fields/fused-label.jpg)

Replace separate city and country fields with a labelled `FusedGroup`:

```php
use Filament\Forms\Components\Select;
use Filament\Schemas\Components\FusedGroup;

FusedGroup::make([
    TextInput::make('city')
        ->placeholder('City'),
    Select::make('country')
        ->placeholder('Country')
        ->options([
            'us' => 'United States',
            'ca' => 'Canada',
            'gb' => 'United Kingdom',
        ]),
])
    ->label('Location'),
```

### Variant: Fused columns and spans

**When**: a fused concept contains parts with deliberately different expected widths at a wider breakpoint.

**Not when**: custom spans only make the row look balanced instead of reflecting value length or importance.

**Source**: [forms/fields/fused-columns-span](https://filamentphp.com/docs/images/5.x/light/forms/fields/fused-columns-span.jpg)

Give the longer city value more width inside the fused group:

```php
use Filament\Forms\Components\Select;
use Filament\Schemas\Components\FusedGroup;

FusedGroup::make([
    TextInput::make('city')
        ->placeholder('City')
        ->columnSpan(2),
    Select::make('country')
        ->placeholder('Country')
        ->options([
            'us' => 'United States',
            'ca' => 'Canada',
            'gb' => 'United Kingdom',
        ]),
])
    ->label('Location')
    ->columns(3),
```

### Variant: Contextual callout

**When**: important context, a warning, or a next step affects a group or workflow rather than one field.

**Not when**: a short field-specific instruction would be clearer as nearby field-level guidance.

**Source**: [schemas/layout/callout/simple](https://filamentphp.com/docs/images/5.x/light/schemas/layout/callout/simple.jpg)

Insert a `Callout` above the fields when the message applies to the workflow:

```php
use Filament\Schemas\Components\Callout;

Callout::make('Order confirmation emails the customer')
    ->description('Confirm the shipping city and contact email before changing OrderStatus.')
    ->warning(),
TextInput::make('email')
    ->label('Email address')
    ->email()
    ->required(),
```
