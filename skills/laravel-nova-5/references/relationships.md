# Relationships

Use this reference for Nova relationship fields and relationship query behavior.
Read:

- [Relationships](https://nova.laravel.com/docs/v5/resources/relationships.md)
- [Authorization](https://nova.laravel.com/docs/v5/resources/authorization.md)

## Field definitions

Nova provides fields for Eloquent relationship types including `HasOne`,
`HasMany`, `BelongsTo`, `BelongsToMany`, through relationships, and polymorphic
relationships. Match the field to the actual Eloquent relation.

```php
use App\Nova\Post;
use App\Nova\User;
use Laravel\Nova\Fields\BelongsTo;
use Laravel\Nova\Fields\BelongsToMany;
use Laravel\Nova\Fields\HasMany;
use Laravel\Nova\Fields\Text;

// Fragment: returned from a resource's fields() method.
BelongsTo::make('Author', 'author', User::class)
    ->searchable()
    ->withoutTrashed()
    ->showCreateRelationButton()
    ->modalSize('5xl'),

HasMany::make('Posts', 'posts', Post::class),

BelongsToMany::make('Roles')
    ->fields(fn ($request, $relatedModel) => [
        Text::make('Notes'),
    ]),
```

Import the related **Nova resource** class, not its Eloquent model, for the third
argument. The first argument is a display label; the second is the Eloquent
relationship method. Use explicit arguments when convention is ambiguous.
Plural labels often read naturally for to-many relationships, but correctness
depends on those three meanings rather than an unconditional pluralization rule.

## Searching and inline creation

Use `searchable()` for large associatable sets instead of loading every option.
Use `withSubtitles()` only when related resources provide useful subtitles.
Avoid `preload()` for unbounded datasets.

`showCreateRelationButton()` is documented for `BelongsTo` and `MorphTo`, and
for creating related models from `BelongsToMany` / `MorphToMany` attach flows.
It may receive a closure for conditional availability. The create button does
not replace `create`, `add{Model}`, or `attach{Model}` policy checks.

## Pivot fields and actions

```php
use App\Nova\Actions\MarkAsActive;
use Laravel\Nova\Fields\BelongsToMany;
use Laravel\Nova\Fields\Text;

// Fragment: returned from a resource's fields() method.
BelongsToMany::make('Roles')
    ->fields(fn ($request, $relatedModel) => [
        Text::make('Notes'),
    ])
    ->actions(fn () => [
        new MarkAsActive,
    ]),
```

Use a pivot field class when the field list is reused. If duplicate relations
are allowed, follow the official `allowDuplicateRelations()` requirements,
including a pivot `id`; do not enable duplicates solely in the UI.

## Relatable queries

Customize which models appear in relationship selectors with the resource's
documented `relatableQuery` or dynamic `relatable{Models}` methods. A field can
also use `relatableQueryUsing` where documented.

```php
use Illuminate\Contracts\Database\Eloquent\Builder;
use Laravel\Nova\Http\Requests\NovaRequest;

// Fragment: method on the related Nova resource.
public static function relatableTags(
    NovaRequest $request,
    Builder $query
): Builder {
    return $query->where('type', 'posts');
}
```

If one resource has multiple relationships to the same related resource, the
dynamic method may receive the `Field` so code can distinguish attributes and
field types. Copy that signature from the current v5 docs or installed package;
do not guess it.

Relatable filtering limits selectable relationship records. It is not a
substitute for relationship policy methods, database constraints, or tenant
scoping elsewhere in the application.

## Performance

- Prefer searchable associatables for high-cardinality relations.
- Use explicit eager loading only where rendered data repeatedly accesses a
  relationship.
- Avoid pivot callbacks that execute a query per row.
- Verify relationship indexes and tenant scopes at the database/query layer.
- Test attach, detach, and inline-create authorization in both allowed and
  denied cases when those operations change.
