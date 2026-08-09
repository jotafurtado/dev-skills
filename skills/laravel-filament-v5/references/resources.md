# Resources — CRUD interfaces for Eloquent models

A resource is a static class describing how a model is managed in the panel. This file covers the resource's own anatomy; the form/table content it delegates to is `references/forms.md` / `references/tables.md`. ([overview](https://filamentphp.com/docs/5.x/resources/overview.md))

Snippets are focused fragments unless a full class is shown; preserve the surrounding namespace/class and add the displayed imports.

## On this page

- Generation, generated structure, and extracted component classes
- Resource versus page-specific infolists
- Record identity, navigation, and URL generation
- Operation-aware fields, authorization, and query scoping

## Generating a resource

```bash
php artisan make:filament-resource Customer
php artisan make:filament-resource Customer --generate      # infer form/table from DB columns
php artisan make:filament-resource Customer --view           # also generate a View page
php artisan make:filament-resource Customer --soft-deletes   # restore/force-delete/trashed filter
php artisan make:filament-resource Customer --simple         # single page, modals for create/edit/delete
php artisan make:filament-resource Customer --model --migration --factory
```

The default v5 scaffold **already delegates** form and table to dedicated classes — this is not an optional convention, it's what `make:filament-resource` generates ([code quality tips](https://filamentphp.com/docs/5.x/resources/code-quality-tips.md)):

```
Resources/Customers/
├── CustomerResource.php
├── Pages/
│   ├── ListCustomers.php
│   ├── CreateCustomer.php
│   └── EditCustomer.php
├── Schemas/
│   └── CustomerForm.php
└── Tables/
    └── CustomersTable.php
```

```php
// CustomerResource.php
use App\Filament\Resources\Customers\Schemas\CustomerForm;
use App\Filament\Resources\Customers\Tables\CustomersTable;
use Filament\Schemas\Schema;
use Filament\Tables\Table;

public static function form(Schema $schema): Schema
{
    return CustomerForm::configure($schema);
}

public static function table(Table $table): Table
{
    return CustomersTable::configure($table);
}
```

The same pattern applies to `infolist()` — write the class yourself and delegate to it exactly as above:

```php
use App\Filament\Resources\Customers\Schemas\CustomerInfolist;
use Filament\Schemas\Schema;

public static function infolist(Schema $schema): Schema
{
    return CustomerInfolist::configure($schema);
}
```

Keep this delegation for any resource with more than a handful of fields/columns — it's what keeps the resource class readable as the form/table grow. Inlining `form()`/`table()` directly in the resource is only for genuinely trivial resources.

These classes deliberately have **no parent class and no interface**. That's the design: an enforced `configure()` signature would stop you passing your own configuration variables, which is what lets one class serve several places with slight tweaks.

```php
namespace App\Filament\Resources\Customers\Schemas;

use Filament\Forms\Components\TextInput;
use Filament\Schemas\Schema;

class CustomerForm
{
    public static function configure(Schema $schema, bool $withBillingFields = true): Schema
    {
        return $schema->components([
            TextInput::make('name'),
            ...($withBillingFields ? [TextInput::make('vat_number')] : []),
        ]);
    }
}
```

The Resource then calls `CustomerForm::configure($schema)`, while a modal action that only collects a name calls `CustomerForm::configure($schema, withBillingFields: false)`.

**Simple (modal) resources** (`--simple`) get one "Manage" page (List + create/edit/delete modals) and have no `getRelations()` — relation managers only attach to Edit/View pages, which simple resources don't have.

## Component classes — when `configure()` itself gets long

Delegating to `CustomerForm` doesn't help once `configure()` grows to hundreds of lines. Extract a heavily-configured component into its own class exposing a static `make()` that returns the configured official component:

```php
namespace App\Filament\Resources\Customers\Schemas\Components;

use Filament\Forms\Components\TextInput;

class CustomerNameInput
{
    public static function make(): TextInput
    {
        return TextInput::make('name')
            ->label('Full name')
            ->required()
            ->maxLength(255)
            ->placeholder('Enter your full name')
            ->belowContent('This is the name that will be displayed on your profile.');
    }
}
```

It then reads as a component anywhere a component is accepted — the call site doesn't change shape:

```php
use App\Filament\Resources\Customers\Schemas\Components\CustomerNameInput;

return $schema->components([
    CustomerNameInput::make(),
]);
```

The return type is the real Filament component, so the caller can still chain onto it (`CustomerNameInput::make()->disabled()`) when one call site needs a variation.

Filament enforces no naming or location rules here; the documented suggestions, relative to the resource directory:

| Kind | Directory | Naming |
|---|---|---|
| Schema components | `Schemas/Components/` | `CustomerNameInput`, `CustomerCountrySelect` |
| Table columns | `Tables/Columns/` | `CustomerNameColumn` |
| Table filters | `Tables/Filters/` | `CustomerCountryFilter` |
| Actions | `Actions/` | `EmailCustomerAction`, `UpdateCustomerCountryBulkAction` |

Actions pay off most, because the same class serves a page header and a table row:

```php
namespace App\Filament\Resources\Customers\Actions;

use App\Models\Customer;
use Filament\Actions\Action;
use Filament\Forms\Components\Textarea;
use Filament\Forms\Components\TextInput;
use Filament\Support\Icons\Heroicon;

class EmailCustomerAction
{
    public static function make(): Action
    {
        return Action::make('email')
            ->label('Send email')
            ->icon(Heroicon::Envelope)
            ->schema([
                TextInput::make('subject')->required()->maxLength(255),
                Textarea::make('body')->autosize()->required(),
            ])
            ->action(function (Customer $customer, array $data) {
                // ...
            });
    }
}
```

```php
// Pages/ViewCustomer.php
protected function getHeaderActions(): array
{
    return [EmailCustomerAction::make()];
}

// Tables/CustomersTable.php
return $table
    ->columns([/* ... */])
    ->recordActions([EmailCustomerAction::make()]);
```

Extract when a component is long enough to hide the shape of its `configure()`, or when it's used in more than one place. A three-line `TextInput` in one schema stays inline — a wrapper class per field is its own kind of noise.

## Resource infolist vs custom View page infolist

This is about *where the method lives*, independent of delegation — either body below can hand off to a `CustomerInfolist::configure($schema)` class once it outgrows a few entries.

Define the shared View-page infolist as a **static method on the Resource**:

```php
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Schema;

public static function infolist(Schema $schema): Schema
{
    return $schema->components([
        TextEntry::make('name'),
    ]);
}
```

Define a page-specific infolist as an **instance method on the custom `ViewRecord` page**:

```php
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Schema;

public function infolist(Schema $schema): Schema
{
    return $schema->components([
        TextEntry::make('name'),
    ]);
}
```

The official [Viewing records](https://filamentphp.com/docs/5.x/resources/viewing-records.md) page documents both contexts.

## Record identity

```php
protected static ?string $recordTitleAttribute = 'name'; // required for global search
protected static ?string $modelLabel = 'customer';        // singular label, auto-derived if omitted
protected static ?string $pluralModelLabel = 'customers';
```

`$recordTitleAttribute` can also name an Eloquent accessor when one column isn't enough to identify a record.

## Navigation

```php
use BackedEnum;
use Filament\Support\Icons\Heroicon;
use UnitEnum;

protected static string|BackedEnum|null $navigationIcon = Heroicon::OutlinedUserGroup; // Heroicon enum, per SKILL.md
protected static ?string $navigationLabel = 'Customers';   // auto-derived from plural label if omitted
protected static string|UnitEnum|null $navigationGroup = 'Shop';
protected static ?string $navigationParentItem = 'Products'; // nests under another item; that item's group must also be set
protected static ?int $navigationSort = 2;
```

Dynamic equivalents exist for every property above: `getNavigationIcon()`, `getNavigationLabel()`, `getNavigationGroup()`, `getNavigationSort()`. A resource missing from the nav menu despite no `$navigationIcon` issue is usually a policy problem — see Authorization below (`viewAny()` must return `true`).

## Generating URLs — never hand-build resource routes

```php
CustomerResource::getUrl();                                  // list page
CustomerResource::getUrl('create');
CustomerResource::getUrl('edit', ['record' => $customer]);   // model or ID
CustomerResource::getUrl(panel: 'marketing');                 // cross-panel
```

Never `route('filament.admin.resources.customers.index')` — the slug/route-naming convention is exactly what `getUrl()` exists to hide. For simple/modal resources, generate a URL that opens an action directly: `CustomerResource::getUrl(parameters: ['tableAction' => EditAction::getDefaultName(), 'tableActionRecord' => $customer])`.

## Conditional form fields by operation

```php
use Filament\Forms\Components\TextInput;
use Filament\Support\Enums\Operation;

TextInput::make('password')->password()->required()->hiddenOn(Operation::Edit);
TextInput::make('password')->password()->required()->visibleOn(Operation::Create);
```

See SKILL.md, "Filament v5 invariants", for when to prefer `hiddenOn()` / `visibleOn()` / `disabledOn()` over a custom callback and for the operation hierarchy (dedicated methods → `Operation` enum → `string $operation` values).

## Authorization

Filament observes standard Laravel model policies automatically — no extra wiring needed once a policy is registered:

| Policy method | Controls |
|---|---|
| `viewAny()` | Whether the resource appears in navigation and is accessible at all |
| `create()` | The Create page / action |
| `update()` | The Edit page / action |
| `view()` | The View page / action |
| `delete()` / `deleteAny()` | Single delete / bulk `DeleteBulkAction` (bulk uses `deleteAny()` for performance; add `->authorizeIndividualRecords()` to check `delete()` per record instead) |
| `forceDelete()` / `forceDeleteAny()` | Same pattern for permanent deletion of soft-deleted records |
| `restore()` / `restoreAny()` | Same pattern for restoring soft-deleted records |
| `reorder()` | Drag-to-reorder in tables |

```php
protected static bool $shouldSkipAuthorization = true; // opt out entirely — rare, justify it in a comment
```

Custom actions/pages and inline-editable columns have separate authorization responsibilities. Read `references/security.md`; visibility and navigation checks are not substitutes for server-side authorization.

## Query scoping

```php
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\SoftDeletingScope;

public static function getEloquentQuery(): Builder
{
    return parent::getEloquentQuery()
        ->withoutGlobalScopes([SoftDeletingScope::class]); // only if you deliberately need scoped-out records
}
```

In a tenant-aware panel, do not remove global scopes indiscriminately: `withoutGlobalScopes()` can also remove tenancy protection. Prefer naming only the scope that must be removed and add cross-tenant tests; see `references/security.md`.
