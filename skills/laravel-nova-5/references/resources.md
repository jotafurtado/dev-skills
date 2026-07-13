# Resources

Use this reference for resource classes, display behavior, panels, validation,
polling, pagination, and soft deletes. Read the official pages first:

- [The Basics](https://nova.laravel.com/docs/v5/resources/the-basics.md)
- [Fields](https://nova.laravel.com/docs/v5/resources/fields.md)
- [Field Panels](https://nova.laravel.com/docs/v5/resources/panels.md)
- [Validation](https://nova.laravel.com/docs/v5/resources/validation.md)

## Define a resource

Generate resources with `php artisan nova:resource Post`. A complete minimal
resource includes the local base resource and all field imports:

```php
<?php

namespace App\Nova;

use App\Models\Post as PostModel;
use Laravel\Nova\Fields\ID;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

class Post extends Resource
{
    /** @var class-string<PostModel> */
    public static $model = PostModel::class;

    public static $title = 'title';

    public static $search = ['id', 'title'];

    /**
     * @return array<int, \Laravel\Nova\Fields\Field>
     */
    public function fields(NovaRequest $request): array
    {
        return [
            ID::make()->sortable(),
            Text::make('Title')
                ->sortable()
                ->rules('required', 'max:255'),
        ];
    }
}
```

Follow the generated resource signature from the installed Nova version if it
differs. Keep the resource class singular. Customize display text through
documented `label()` and `singularLabel()` methods rather than assuming English
pluralization.

## Titles, search, and query cost

- `$title` identifies the model attribute shown as the resource title.
- Override `title()` only when the display value is computed.
- `subtitle()` can add global-search context.
- `$search` defines searchable columns; consult Scout documentation before
  enabling Scout-specific behavior.
- Add relationships to `$with` only when resource rendering repeatedly accesses
  them and eager loading is beneficial. Confirm query and memory impact.

## Panels and tabs

```php
use Laravel\Nova\Fields\Date;
use Laravel\Nova\Fields\HasMany;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Panel;
use Laravel\Nova\Tabs\Tab;

// Fragment: returned from a resource's fields() method.
Panel::make('Profile', [
    Text::make('Full Name'),
    Date::make('Date of Birth'),
])->collapsible()->collapsedByDefault()->limit(1),

Tab::group('Relations', [
    HasMany::make('Orders'),
]),
```

`Panel::limit()` controls initially displayed fields. `collapsible()` allows the
user to toggle a panel; `collapsedByDefault()` starts it collapsed. For an
untitled tab group, the official API uses the named argument form
`Tab::group(fields: [...])`.

## Validation

Nova field validation uses Laravel validation rules:

```php
use Laravel\Nova\Fields\Text;

// Fragment: returned from a resource's fields() method.
Text::make('Email')
    ->rules('required', 'email', 'max:255')
    ->creationRules('unique:users,email')
    ->updateRules('unique:users,email,{{resourceId}}'),
```

Use rule objects or closures when appropriate. For cross-field validation, use
the documented resource hooks `afterValidation`, `afterCreationValidation`, and
`afterUpdateValidation`. Keep database constraints as the final integrity
boundary.

## Pagination, debounce, and polling

These options are opt-in tuning controls, not defaults to add everywhere:

```php
// Fragment: resource properties.
public static $perPageOptions = [25, 50, 100];
public static $debounce = 0.5;
public static $polling = true;
public static $pollingInterval = 5;
public static $showPollingToggle = true;
```

The first `perPageOptions` value becomes the default page size. Enable polling
only where freshness justifies repeated requests, and choose an interval that
fits query cost and expected concurrency.

## Soft deletes and replication

When the Eloquent model uses Laravel's `SoftDeletes` trait, Nova exposes the
corresponding restore, force-delete, and trashed behavior. Authorize `restore`
and `forceDelete` explicitly when a policy exists.

If overriding resource replication, begin with `parent::replicate()` and mutate
the cloned model deliberately. Review file fields and relationship semantics
before allowing replication; not every attachment workflow should be copied.
