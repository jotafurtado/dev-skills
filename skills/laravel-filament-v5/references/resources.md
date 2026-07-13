# Resources — CRUD interfaces for Eloquent models

A resource is a static class describing how a model is managed in the panel. This file covers the resource's own anatomy; the form/table content it delegates to is `references/forms.md` / `references/tables.md`. ([overview](https://filamentphp.com/docs/5.x/resources/overview.md))

Snippets are focused fragments unless a full class is shown; preserve the surrounding namespace/class and add the displayed imports.

## Generating a resource

```bash
php artisan make:filament-resource Customer
php artisan make:filament-resource Customer --generate      # infer form/table from DB columns
php artisan make:filament-resource Customer --view           # also generate a View page
php artisan make:filament-resource Customer --soft-deletes   # restore/force-delete/trashed filter
php artisan make:filament-resource Customer --simple         # single page, modals for create/edit/delete
php artisan make:filament-resource Customer --model --migration --factory
```

The default v5 scaffold **already delegates** form and table to dedicated classes — this is not an optional convention, it's what `make:filament-resource` generates:

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

Keep this delegation for any resource with more than a handful of fields/columns — it's what keeps the resource class readable as the form/table grow. Inlining `form()`/`table()` directly in the resource is only for genuinely trivial resources.

**Simple (modal) resources** (`--simple`) get one "Manage" page (List + create/edit/delete modals) and have no `getRelations()` — relation managers only attach to Edit/View pages, which simple resources don't have.

## Resource infolist vs custom View page infolist

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

Prefer `hiddenOn()` / `visibleOn()` over a custom callback when those methods express the condition.

Hierarchy:

1. Prefer dedicated `hiddenOn()` / `visibleOn()` / `disabledOn()` methods.
2. In Resource configuration, use `Operation` enum cases where accepted, as in the official Resource overview.
3. In utility callbacks, inject `string $operation` and compare against the documented values `'create'`, `'edit'`, or `'view'`.

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
