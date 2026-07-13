# Authorization

Use this reference for Nova access, model/resource policies, relationship
authorization, field visibility, and query filtering. Read:

- [Nova Authorization](https://nova.laravel.com/docs/v5/resources/authorization.md)
- [Nova Installation: access gate](https://nova.laravel.com/docs/v5/installation.md#authorizing-access-to-nova)
- The official Laravel authorization page matching the installed Laravel major.

## Layer 1: access to Nova

The `viewNova` gate in `App\Providers\NovaServiceProvider` controls access in
non-local environments:

```php
use Illuminate\Support\Facades\Gate;

// Fragment: method on App\Providers\NovaServiceProvider.
protected function gate(): void
{
    Gate::define('viewNova', function ($user) {
        return $user->hasRole('administrator');
    });
}
```

Keep the application's existing identity and permission conventions. Do not
copy an email allowlist into production unless that is the intended access
model.

## Layer 2: resource operations

Nova automatically checks a registered model policy for `viewAny`, `view`,
`create`, `update`, `replicate`, `delete`, `restore`, and `forceDelete`.
Register or discover policies using the installed Laravel version's documented
mechanism.

### Undefined Nova policy methods

When a policy exists but a method is absent, Nova 5 documents these defaults:

- `viewAny`: allowed.
- `view`, `create`, `update`, `delete`, `forceDelete`, `restore`: forbidden.
- `replicate`: falls back to `create` and `update`.
- `add{Model}`, `attach{Model}`, `attachAny{Model}`, `detach{Model}`: allowed.
- `runAction`: falls back to `update`.
- `runDestructiveAction`: falls back to `delete`.

These defaults are intentionally not summarized as “deny by default” or “allow
by default”. Define every method relevant to the feature so behavior is
explicit, especially `viewAny` and relationship methods whose defaults allow.
If no policy exists, do not claim Nova applies the table above; first determine
the application's actual gate and policy setup.

## Nova-specific authorization

Use only the two Nova-specific mechanisms documented for v5:

1. `Nova::whenServing()` inside a shared application policy when only selected
   decisions differ for Nova requests.
2. A resource-specific policy generated with
   `php artisan nova:policy PostPolicy --resource=Post`, assigned through the
   Nova resource's static `$policy` property.

```php
use App\Models\User;
use Illuminate\Http\Request;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Nova;

// Fragment: method on an application model policy.
public function viewAny(User $user)
{
    return Nova::whenServing(
        fn (NovaRequest $request) => $user->can('nova:view-posts'),
        fn (Request $request) => $user->can('view-posts'),
    );
}
```

```php
namespace App\Nova;

use App\Nova\Policies\PostPolicy;

class Post extends Resource
{
    /** @var class-string */
    public static $policy = PostPolicy::class;
}
```

Follow generated signatures from the installed version. Do not invent
Nova-only policy methods beyond those listed in the official v5 authorization
or action documentation.

## Relationship methods

Nova's documented naming conventions are:

- `addComment(User $user, Podcast $podcast)` for adding a related model.
- `attachTag(User $user, Podcast $podcast, Tag $tag)` for attaching an existing
  many-to-many model.
- `attachAnyTag(User $user, Podcast $podcast)` to control whether the attach UI
  is available at all.
- `detachTag(User $user, Podcast $podcast, Tag $tag)` for detaching.

Define corresponding methods on both related policies where inverse operations
are exposed. Use the actual related model's singular class name in the method
suffix.

## Actions, fields, metrics, dashboards, and tools

Apply `canSee` when registering fields, actions, metrics, dashboards, cards, or
tools as documented for that type. Use the `canSeeWhen` policy proxy only where
the relevant v5 page documents it, including fields, lenses, metrics, and
dashboards. Actions additionally support `canRun`. These methods control Nova UI
visibility or execution, but backend operations still need policy, gate, and
route authorization.

## Query visibility is separate

A policy `view` denial does not remove a row from a resource index. Scope index
records with the documented `indexQuery()` method, and scope relationship
selectors with `relatableQuery()` / dynamic relatable methods. When Scout is
used, apply the documented `scoutQuery()` hook.

Keep tenant and ownership boundaries in server-side queries as well as policies.
Test both authorized and unauthorized users; include index visibility,
individual record access, mutation, relationship operations, and action
execution according to the changed behavior.
