# Fields

Use this reference for built-in, computed, dependent, and repeater fields. Read:

- [Fields](https://nova.laravel.com/docs/v5/resources/fields.md)
- [Dependent Fields](https://nova.laravel.com/docs/v5/resources/dependent-fields.md)
- [Repeater Fields](https://nova.laravel.com/docs/v5/resources/repeater-fields.md)
- [Validation](https://nova.laravel.com/docs/v5/resources/validation.md)

## Define and map fields

The first `make()` argument is the display name. Nova normally derives the
attribute in snake case; pass the attribute explicitly when it differs:

```php
use Laravel\Nova\Fields\ID;
use Laravel\Nova\Fields\Text;

// Fragment: returned from a resource's fields() method.
ID::make()->sortable(),
Text::make('Full Name'),
Text::make('Email', 'email_address'),
```

Use documented visibility methods for the intended context:
`showOnIndex`, `showOnDetail`, `showOnCreating`, `showOnUpdating`,
`hideFromIndex`, `hideFromDetail`, `hideWhenCreating`, `hideWhenUpdating`,
`onlyOnIndex`, `onlyOnDetail`, `onlyOnForms`, and `exceptOnForms`.

`required()` controls the visual required indicator; it does not add a Laravel
validation rule. Pair it with `rules('required')` when input is actually
required. `nullable()` controls conversion of empty values to `null`.

Use `ID::make()->asBigInt()` only when large integer identifiers cannot be
represented safely by the client. Computed fields created from a callable are
not sortable because they do not map directly to a database column.

## Authorization and field visibility

```php
use Laravel\Nova\Fields\Text;

// Fragment: $this is the current Nova resource.
Text::make('Name')
    ->canSee(fn ($request) => $request->user()->can('viewProfile', $this)),

Text::make('Internal Note')
    ->canSeeWhen('viewInternalNote', $this),
```

Visibility is presentation-level authorization. Protect the underlying model
operation or endpoint with a policy, gate, or middleware as well.

## Dependent fields

The field receiving `dependsOn` must be in Nova's supported dependent-field
list. Separately, the field being observed must live-report changes. The
official list of fields that **cannot be depended upon** includes `Audio`,
`Code`, `File`, `Image`, `KeyValue`, `Status`, `Tag`, `Trix`, `VaporAudio`,
`VaporFile`, and `VaporImage`.

```php
use Laravel\Nova\Fields\FormData;
use Laravel\Nova\Fields\Select;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// Fragment: returned from a resource's fields() method.
Select::make('Purchase Type', 'type')->options([
    'personal' => 'Personal',
    'gift' => 'Gift',
]),

Text::make('Recipient')
    ->readonly()
    ->dependsOn(
        ['type'],
        function (Text $field, NovaRequest $request, FormData $formData) {
            if ($formData->type === 'gift') {
                $field->readonly(false)->rules(['required', 'email']);
            }
        }
    ),
```

Use `dependsOnCreating` or `dependsOnUpdating` for mode-specific behavior.
Use `FormData::resource()` exactly as documented when resolving a selected
related resource ID. Do not infer IDs from display labels.

## Repeaters

Generate a repeatable with `php artisan nova:repeatable LineItem`. Nova supports
JSON and `HasMany` storage presets:

```php
use App\Nova\Repeaters\LineItem;
use Laravel\Nova\Fields\Repeater;

// Fragment: returned from a resource's fields() method.
Repeater::make('Line Items', 'line_items')
    ->repeatables([
        LineItem::make(),
    ])
    ->asJson(),
```

For `asJson()`, cast the model attribute to `array` (or an equivalent supported
cast). For `asHasMany()`, each repeatable declares its Eloquent `$model`.
Understand deletion/recreation behavior before choosing the preset; use the
documented `uniqueField()` workflow when upsert semantics are required.

Repeatable constraints from the v5 docs:

- Fields inside a repeatable do not support `dependsOn`.
- `creationRules` and `updateRules` are not supported there; use `rules`.
- Relationship fields are unsupported inside repeatables.
- `File`, `Audio`, and `Image` require a `uniqueField`.
- Markdown and Trix attachments are not supported inside repeatables.

Do not collapse these constraints into “no files” or “only MorphToMany is
unsupported”; both statements are inaccurate.
