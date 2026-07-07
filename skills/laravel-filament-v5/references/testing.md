# Testing Filament panels (Pest + Livewire)

Everything in a panel is tested through Livewire helpers — `livewire(PageClass::class)` in Pest, `Livewire::test()` in PHPUnit. ([testing overview](https://filamentphp.com/docs/5.x/testing/overview.md))

**What IS a Livewire component** (pass to `livewire()`): resource pages (`ListUsers`, `CreateUser`, `EditUser`…), relation managers, widgets, custom pages.
**What is NOT**: resource classes, schema components, actions — test those through the page that hosts them.

## Setup

```php
use App\Models\User;

beforeEach(function () {
    actingAs(User::factory()->create());
});
```

Multi-panel: `Filament::setCurrentPanel('admin')`. Multi-tenant: `Filament::setTenant($team)`.

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

## Actions (including table and bulk)

Use `Filament\Actions\Testing\TestAction` to target where the action lives:

```php
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
livewire(PostsRelationManager::class, [
    'ownerRecord' => $category,
    'pageClass' => EditCategory::class,
])->assertCanSeeTableRecords($category->posts);
```

## Detailed guides

Per-surface docs: [testing-resources](https://filamentphp.com/docs/5.x/testing/testing-resources.md) · [testing-tables](https://filamentphp.com/docs/5.x/testing/testing-tables.md) · [testing-schemas](https://filamentphp.com/docs/5.x/testing/testing-schemas.md) · [testing-actions](https://filamentphp.com/docs/5.x/testing/testing-actions.md) · [testing-notifications](https://filamentphp.com/docs/5.x/testing/testing-notifications.md). Fetch the `.md` page before guessing an assertion name.
