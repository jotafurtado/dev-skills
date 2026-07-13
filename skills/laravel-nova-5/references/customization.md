# Customization

Use this reference for custom components, menus, notifications, localization,
assets, stubs, search, and impersonation. Authorization and resource
replication live in their dedicated references.

Official pages:

- [Tools](https://nova.laravel.com/docs/v5/customization/tools.md)
- [Resource Tools](https://nova.laravel.com/docs/v5/customization/resource-tools.md)
- [Cards](https://nova.laravel.com/docs/v5/customization/cards.md)
- [Custom Fields](https://nova.laravel.com/docs/v5/customization/fields.md)
- [Custom Filters](https://nova.laravel.com/docs/v5/customization/filters.md)
- [Menus](https://nova.laravel.com/docs/v5/customization/menus.md)
- [Notifications](https://nova.laravel.com/docs/v5/customization/notifications.md)
- [Localization](https://nova.laravel.com/docs/v5/customization/localization.md)
- [Assets](https://nova.laravel.com/docs/v5/customization/assets.md)
- [CSS / JavaScript](https://nova.laravel.com/docs/v5/customization/frontend.md)
- [Stubs](https://nova.laravel.com/docs/v5/customization/stubs.md)
- [Impersonation](https://nova.laravel.com/docs/v5/customization/impersonation.md)

## Generate from Nova scaffolds

Use the command matching the component:

```shell
php artisan nova:tool acme/analytics-dashboard
php artisan nova:resource-tool acme/stripe-inspector
php artisan nova:card acme/weather-widget
php artisan nova:field acme/color-picker
php artisan nova:custom-filter acme/date-range-filter
php artisan nova:asset acme/analytics
```

`nova:filter` generates a PHP resource filter; `nova:custom-filter` generates a
custom frontend filter package. Do not interchange them.

Generated components live under `nova-components`, contain their own Composer
package and build setup, and may be registered as Composer path repositories.
Use the generated installed scaffold as the source of truth for Vue, Inertia,
Laravel Mix, Node, NPM, and CSS conventions. Do not rewrite it from remembered
Nova or Tailwind versions.

### Register tools and resource tools

```php
use Acme\AnalyticsDashboard\AnalyticsDashboard;

// Fragment: method on App\Providers\NovaServiceProvider.
public function tools(): array
{
    return [
        (new AnalyticsDashboard)
            ->canSee(fn ($request) => $request->user()->can('viewAnalytics')),
    ];
}
```

```php
use Acme\StripeInspector\StripeInspector;
use Laravel\Nova\Fields\ID;
use Laravel\Nova\Http\Requests\NovaRequest;

// Fragment: method on a Nova resource.
public function fields(NovaRequest $request): array
{
    return [
        ID::make()->sortable(),
        StripeInspector::make()
            ->issuesRefunds()
            ->canSee(fn ($request) => $request->user()->can('manageBilling')),
    ];
}
```

Resource tool options are metadata consumed through the Vue `panel` prop. Prefer
explicit option methods backed by `withMeta`; use dynamic options only where the
official generated resource-tool behavior is suitable.

Cards register in a resource or dashboard `cards()` method. Custom fields
register in resource `fields()`. Custom filters register in `filters()`. Add
authorization to every application-owned API route exposed by a tool, card,
field, or filter; component visibility is not route protection.

## Menus

Define custom menus in `NovaServiceProvider::boot()`:

```php
use App\Nova\Category;
use App\Nova\Dashboards\Main;
use App\Nova\Post;
use Illuminate\Http\Request;
use Laravel\Nova\Menu\MenuItem;
use Laravel\Nova\Menu\MenuSection;
use Laravel\Nova\Nova;

// Fragment: inside NovaServiceProvider::boot(), after parent::boot().
Nova::mainMenu(function (Request $request) {
    return [
        MenuSection::dashboard(Main::class)->icon('chart-bar'),
        MenuSection::make('Content', [
            MenuItem::resource(Post::class),
            MenuItem::resource(Category::class),
        ])->icon('document-text')->collapsable(),
    ];
});
```

When the main menu is fully customized, custom tool links are not inserted
automatically; add each tool's menu deliberately.

The user menu callback receives an existing `Menu` and supports `MenuItem`
objects only:

```php
use Illuminate\Http\Request;
use Laravel\Nova\Menu\Menu;
use Laravel\Nova\Menu\MenuItem;
use Laravel\Nova\Nova;

// Fragment: inside NovaServiceProvider::boot().
Nova::userMenu(function (Request $request, Menu $menu) {
    return $menu
        ->prepend(MenuItem::link(
            'My Profile',
            '/resources/users/'.$request->user()->getKey()
        ))
        ->append(MenuItem::externalLink('Help', 'https://example.com/help'));
});
```

The logout item cannot be removed. Do not place `MenuSection` or `MenuGroup`
objects in the user menu.

## Notifications

```php
use Laravel\Nova\Notifications\NovaNotification;
use Laravel\Nova\URL;

// Fragment: $user uses Laravel's Notifiable trait.
$user->notify(
    NovaNotification::make()
        ->message('Your report is ready to download.')
        ->action('Download', URL::remote('https://example.com/report.pdf'))
        ->icon('download')
        ->type('info')
);
```

Documented types are `success`, `error`, `warning`, and `info`. Application
notification classes may use `Laravel\Nova\Notifications\NovaChannel` and
`toNova()`. Use `Nova::withoutNotificationCenter()` to disable the center; the
similarly named `withoutNotifications()` call is not the documented API.

## Localization and stubs

After `nova:install`, translations live under `lang/vendor/nova`. Generate a
locale copy with:

```shell
php artisan nova:translate pt-BR
```

Use resource `label()` / `singularLabel()` and component `name()` methods
documented for each type. Frontend packages can receive translations through
`Nova::translations()` and use the generated localization helpers.

Publish customizable generation stubs with:

```shell
php artisan nova:stubs
```

Nova writes them to `stubs/nova`. Delete a local stub to fall back to Nova's
default; keep customized signatures synchronized with the installed version.

## Frontend assets

Custom packages should retain generated asset registration and build commands.
Use `Nova.request()` for the preconfigured Axios client, `Nova.visit()` for
navigation, and the documented event/toast APIs where needed. Keep route
authorization server-side.

For application-wide scripts or styles, generate a Nova asset with
`nova:asset`. The v5 docs state that generated assets are auto-loaded through
Laravel's autoloader, so no additional registration is required. Build them
with the generated `npm run dev`, `npm run prod`, or `npm run watch` scripts.
Do not assume a public path, Tailwind directive, or manifest format without
checking that scaffold.

## Global search

Set resource `$search` columns for database search. If the Eloquent model uses
Laravel Scout's `Searchable` trait, Nova automatically uses Scout unless the
resource's documented `usesScout()` method disables it. There is no documented
`public static $searchUsing = 'scout'` switch.

Use `$title` / `title()` and `subtitle()` for search result display. When a
subtitle accesses a relationship, consider targeted eager loading. Use the
official global-search and Scout pages for result limits, debounce, covers, and
`scoutQuery()`:

- [Global Search](https://nova.laravel.com/docs/v5/search/global-search.md)
- [Scout Integration](https://nova.laravel.com/docs/v5/search/scout-integration.md)

## Impersonation

Enable impersonation by adding `Laravel\Nova\Auth\Impersonatable` to the
authenticatable Eloquent model. Customize `canImpersonate()` and
`canBeImpersonated()` as documented, and consider auditing
`StartedImpersonating` / `StoppedImpersonating` events.

Do not use `Nova::impersonation(true)`; it is not the documented Nova 5 setup.
