# Testing Filament panels (Pest + Livewire)

Everything in a panel is tested through Livewire helpers — `livewire(PageClass::class)` in Pest, `Livewire::test()` in PHPUnit. ([testing overview](https://filamentphp.com/docs/5.x/testing/overview.md))

**What IS a Livewire component** (pass to `livewire()`): resource pages (`ListUsers`, `CreateUser`, `EditUser`…), relation managers, widgets, custom pages.
**What is NOT**: resource classes, schema components, actions — test those through the page that hosts them.

Snippets are focused Pest fragments. Add the shown model/page imports plus `use function Pest\Livewire\livewire;`; preserve the project's test setup and database traits.

## On this page

- Post-change minimum and setup
- List, create/edit, and view pages
- Actions and relation managers
- Authorization, tenant isolation, and official detailed guides

## Post-change minimum

After a Filament UI change, test each touched surface for which the official helpers apply:

1. Resource page: `assertOk()`, then its changed table, schema state, form, or action behavior.
2. Resource View page: pass `record`, call `assertOk()`, and assert the relevant infolist state with `assertSchemaStateSet()`.
3. Relation manager: assert the host page renders it with `assertSeeLivewire()`, then test the manager directly with `ownerRecord`, `pageClass`, `assertOk()`, and relevant records/actions.
4. Widget or custom page: load its Livewire class and assert the changed behavior.

Run only applicable tests, but do not treat a successful List/Edit page test as coverage for a changed View page or relation manager.

## Setup

```php
use App\Models\User;
use function Pest\Laravel\actingAs;

beforeEach(function () {
    actingAs(User::factory()->create());
});
```

Multi-panel: `Filament::setCurrentPanel('admin')`. For a multi-tenant Livewire test, set the tenant and current panel, then call `Filament::bootCurrentPanel()` when tenant scopes or model listeners need booting:

```php
Filament::setTenant($team);
Filament::setCurrentPanel('admin');
Filament::bootCurrentPanel();
```

## List page

```php
use App\Filament\Resources\Users\Pages\ListUsers;
use function Pest\Livewire\livewire;

it('can load the page', function () {
    $users = User::factory()->count(5)->create();

    livewire(ListUsers::class)
        ->assertOk()
        ->assertCanSeeTableRecords($users);
});
```

- **Search**: `->searchTable($users->first()->name)` then `assertCanSeeTableRecords(...)` / `assertCanNotSeeTableRecords(...)`.
- **Sort**: `->sortTable('name')` / `->sortTable('name', 'desc')` + `assertCanSeeTableRecords($users->sortBy('name'), inOrder: true)`.
- **Filter**: `->filterTable('locale', $value)`.

## Create / Edit pages

```php
use App\Filament\Resources\Users\Pages\CreateUser;
use App\Filament\Resources\Users\Pages\EditUser;

livewire(CreateUser::class)
    ->fillForm(['name' => 'Test', 'email' => 'test@example.com'])
    ->call('create')
    ->assertHasNoFormErrors()
    ->assertNotified();

livewire(EditUser::class, ['record' => $user])
    ->assertSchemaStateSet(['name' => $user->name])
    ->fillForm(['name' => 'Updated'])
    ->call('save')
    ->assertHasNoFormErrors();
```

Assert validation failures with `->assertHasFormErrors(['email' => 'required'])`.

## View pages

```php
use App\Filament\Resources\Users\Pages\ViewUser;
use App\Models\User;

it('can display a user', function () {
    $user = User::factory()->create();

    livewire(ViewUser::class, ['record' => $user->id])
        ->assertOk()
        ->assertSchemaStateSet([
            'name' => $user->name,
            'email' => $user->email,
        ]);
});
```

Use the same pattern for a custom `ViewRecord` page that defines its own instance `infolist()` method. For component-level checks, give schema components stable `->key(...)` values and use the documented schema assertions.

## Actions (including table and bulk)

Use `Filament\Actions\Testing\TestAction` to target where the action lives:

```php
use Filament\Actions\DeleteBulkAction;
use Filament\Actions\Testing\TestAction;

// row action
livewire(ListUsers::class)
    ->callAction(TestAction::make('send')->table($record));

// bulk action
livewire(ListUsers::class)
    ->selectTableRecords($users)
    ->callAction(TestAction::make(DeleteBulkAction::class)->table()->bulk())
    ->assertNotified()
    ->assertCanNotSeeTableRecords($users);
```

Actions with modal forms: `->callAction('send', data: ['reason' => '...'])->assertHasNoFormErrors()` — validation errors on an action's modal use the same `assertHasFormErrors()` / `assertHasNoFormErrors()` as any other form, not a separate action-specific assertion.

## Relation managers

```php
use App\Filament\Resources\Categories\Pages\EditCategory;
use App\Filament\Resources\Categories\RelationManagers\PostsRelationManager;

livewire(EditCategory::class, ['record' => $category->id])
    ->assertOk()
    ->assertSeeLivewire(PostsRelationManager::class);

livewire(PostsRelationManager::class, [
    'ownerRecord' => $category,
    'pageClass' => EditCategory::class,
])
    ->assertOk()
    ->assertCanSeeTableRecords($category->posts);
```

## Authorization and tenant isolation

For a protected mutation, test the allowed and denied actor through the actual Livewire host. Do not stop at asserting that an action is hidden: attempt the action or page access and assert that the record did not change. For tenancy, create records in at least two tenants and assert that the current actor cannot see, resolve, attach, update, or bulk-process the other tenant's records.

Include crafted identifiers where the boundary accepts a record key, relationship key, or stored file path. Read `references/security.md` for the minimum threat cases and use the exact action/schema assertion from the installed-version docs.

## Detailed guides

Per-surface docs: [testing-resources](https://filamentphp.com/docs/5.x/testing/testing-resources.md) · [testing-tables](https://filamentphp.com/docs/5.x/testing/testing-tables.md) · [testing-schemas](https://filamentphp.com/docs/5.x/testing/testing-schemas.md) · [testing-actions](https://filamentphp.com/docs/5.x/testing/testing-actions.md) · [testing-notifications](https://filamentphp.com/docs/5.x/testing/testing-notifications.md). Fetch the `.md` page before guessing an assertion name.
