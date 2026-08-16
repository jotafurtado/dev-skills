# Panels — provider & panel-level configuration (`Filament\Panel`)

The panel provider is a Laravel service provider at `app/Providers/Filament/AdminPanelProvider.php`, extending `Filament\PanelProvider`. Its `panel(Panel $panel): Panel` method chains configuration on `Filament\Panel` — this is the "configuration" the 5.x docs refer to. Start visual identity here with colors, logo, and font. Use a documented custom theme or CSS hook when the provider cannot express the requirement or the project already has an established theme. ([panel configuration](https://filamentphp.com/docs/5.x/panel-configuration.md))

Snippets are focused fragments; retain the generated provider class and add the displayed imports.

For *which* panel-shell arrangement to build — top versus sidebar navigation, grouping, branding, and authentication surfaces — use `laravel-filament-v5-ui-ux`, `references/panel-shell.md`. This file is the API inventory.

## Identity — colors, logo, font

([styling overview](https://filamentphp.com/docs/5.x/styling/overview.md))

```php
use Filament\Panel;
use Filament\Support\Colors\Color;

public function panel(Panel $panel): Panel
{
    return $panel
        // ...
        ->colors([
            'primary' => Color::Indigo,
        ])
        ->brandLogo(asset('images/logo.svg'))
        ->darkModeBrandLogo(asset('images/logo-dark.svg'))
        ->brandLogoHeight('2rem')
        ->font('Poppins');
}
```

- `->colors()` maps a name to a `Color` constant, a single hex/RGB string (`'primary' => '#6366f1'` — Filament generates the palette), or a full `50 => ... 950 => ...` array of OKLCH colors. Names: `danger`, `gray`, `info`, `primary`, `success`, `warning`.
- `->brandLogo()` accepts a URL string or a closure returning view/HTML (e.g. `fn () => view('filament.admin.logo')` for an inline SVG). `->darkModeBrandLogo()` is the dark-mode variant.
- `->font()` first arg is the family name (default is Inter — only call this to change it); all Google Fonts are available via the default Bunny Fonts provider. Self-host with named args: `->font('Inter', url: asset('css/fonts.css'), provider: LocalFontProvider::class)` (`use Filament\FontProviders\LocalFontProvider;`).

## Navigation

([navigation overview](https://filamentphp.com/docs/5.x/navigation/overview.md))

```php
use Filament\Navigation\NavigationBuilder;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        // ...
        ->topNavigation();   // top nav bar instead of the default sidebar

    // Fully custom navigation (replaces auto-generated items):
    // ->navigation(fn (NavigationBuilder $builder): NavigationBuilder => $builder->items([...]))

    // ->navigation(false);  // disable built-in navigation entirely
}
```

Resource nav badges are **static getters on the resource class**, not fluent panel methods:

```php
public static function getNavigationBadge(): ?string
{
    return static::getModel()::count();
}

public static function getNavigationBadgeColor(): ?string
{
    return static::getModel()::count() > 10 ? 'warning' : 'primary';
}

protected static ?string $navigationBadgeTooltip = 'The number of users';
```

Badge color accepts `danger`, `gray`, `info`, `primary`, `success`, or `warning`; the tooltip can also be returned from `getNavigationBadgeTooltip()`. Per-item properties (`$navigationIcon`, `$navigationGroup`, `$navigationSort`) are covered in `references/resources.md`.

## Multiple panels

Each panel is its own provider. Create one with `php artisan make:filament-panel app`, which generates `app/Providers/Filament/AppPanelProvider.php`; register it in `bootstrap/providers.php` (Laravel 11+) or `config/app.php` (Laravel 10) if the command fails to. Each panel needs a unique `->id()` and `->path()`:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->id('app')
        ->path('app');
}
```

The installer's panel is marked `->default()`. Cross-panel URLs use the panel ID: `SomeResource::getUrl(panel: 'app')` — see `references/resources.md` for the full `getUrl()` inventory.

## Other panel-level switches

| Concern | API |
|---|---|
| Database notifications | `->databaseNotifications()` (optionally `position: DatabaseNotificationsPosition::Sidebar`, `use Filament\Enums\DatabaseNotificationsPosition;`) + `->databaseNotificationsPolling('30s')` — 30s default, `null` disables. Details in `references/notifications.md` |
| Multi-tenancy | `->tenant(Team::class)` enables the panel integration, but access, scoping, middleware, validation, and tests remain required; read `references/security.md` and `references/advanced-features.md` |
| Global search | `->globalSearch(false)` disables it panel-wide; per-record behavior is `$recordTitleAttribute` on the Resource (`references/advanced-features.md`) |
| Middleware | `->middleware([...])` for all panel routes, `->authMiddleware([...])` for authenticated routes only; pass `isPersistent: true` as second arg to also run on Livewire AJAX requests |

For anything beyond this inventory, route through `references/advanced-features.md` and the evidence protocol in `SKILL.md`; do not reconstruct panel APIs from v3/v4 memory.
