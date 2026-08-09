# Panel shell compositions

Ready-to-adapt panel shell compositions for Filament 5. Pick the one whose `When` matches the task, paste it into the panel provider, and rename destinations, groups, and account surfaces to the target domain.

Examples use a `Customer` / `Order` domain consistently across this library.

`laravel-filament-v5` owns panel API signatures, authorization, and tests. This file owns how the shell is arranged. Skeletons live in the panel provider (`Filament\Panel`), not in a Resource.

| Pattern | Use it for |
|---|---|
| [Small panel top navigation](#small-panel-top-navigation) | Few peer destinations in a persistent horizontal scan |
| [Back-office sidebar navigation](#back-office-sidebar-navigation) | Many domain destinations with grouped scanning and queues |
| [Authentication surface hierarchy](#authentication-surface-hierarchy) | Sign-in, recovery, registration, and personal profile |

---

## Small panel top navigation

**When**: a small, stable set of peer destinations fits in a persistent horizontal scan, and people frequently switch among a few areas without needing a deep domain hierarchy.

**Not when**: labels, destinations, or domain groups would crowd the horizontal bar, or the panel is a substantial back-office whose navigation needs persistent grouped scanning.

**Alternatives**: [Back-office sidebar navigation](#back-office-sidebar-navigation).

**Source**: [navigation/overview](https://filamentphp.com/docs/5.x/navigation/overview.md) · [panels/navigation/top-navigation](https://filamentphp.com/docs/images/5.x/light/panels/navigation/top-navigation.jpg)

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->id('admin')
        ->path('admin')
        ->topNavigation();
}
```

**Responsive**: preserve a readable, keyboard-operable menu when the horizontal space contracts, and move to a responsive menu before labels, user controls, or active-state cues collide.

**Accessibility**: make the current destination perceptible without colour alone, and keep every navigation and user-menu control named, keyboard reachable, and visibly focused.

### Variant: Top navigation

**When**: there are few peer destinations with short, stable labels.

**Not when**: a horizontal bar would hide, wrap, or flatten a meaningful domain hierarchy.

**Source**: [panels/navigation/top-navigation](https://filamentphp.com/docs/images/5.x/light/panels/navigation/top-navigation.jpg)

Keep `->topNavigation()` on the panel, and give each peer resource a short label, icon, and ascending sort so the top bar stays scannable:

```php
use BackedEnum;
use Filament\Support\Icons\Heroicon;

protected static ?string $navigationLabel = 'Orders';

protected static string | BackedEnum | null $navigationIcon = Heroicon::OutlinedShoppingCart;

protected static ?int $navigationSort = 2;
```

### Variant: User menu

**When**: account and session actions are secondary to the primary destinations.

**Not when**: a common operational destination is hidden inside a user menu.

**Source**: [panels/navigation/user-menu](https://filamentphp.com/docs/images/5.x/light/panels/navigation/user-menu.jpg)

Add `userMenuItems()` on the panel for secondary account actions — keep Customers and Orders in the primary navigation, not here:

```php
use App\Filament\Pages\Settings;
use Filament\Actions\Action;

->userMenuItems([
    Action::make('settings')
        ->url(fn (): string => Settings::getUrl())
        ->icon('heroicon-o-cog-6-tooth'),
    'profile' => fn (Action $action) => $action->label('Edit profile'),
    'logout' => fn (Action $action) => $action->label('Log out'),
])
```

### Variant: Supported panel identity

**When**: the panel needs a brand mark or configured identity that remains coherent across shell surfaces.

**Not when**: an unrelated typeface or palette is proposed merely to make the shell feel distinctive.

**Source**: [panels/styling/brand-logo](https://filamentphp.com/docs/images/5.x/light/panels/styling/brand-logo.jpg)

Add brand identity to the panel chain with documented color, logo, and font configuration:

```php
use Filament\Support\Colors\Color;

->colors([
    'primary' => Color::Indigo,
])
->brandLogo(asset('images/logo.svg'))
->darkModeBrandLogo(asset('images/logo-dark.svg'))
->brandLogoHeight('2rem')
->font('Poppins')
```

---

## Back-office sidebar navigation

**When**: many destinations need a persistent vertical scan, a single audience works across several coherent business domains, and a small number of queues need immediate action.

**Not when**: a group is only visual decoration rather than a named domain boundary, or a cluster or separate panel is needed because the work has its own route structure, audience, or authentication boundary.

**Alternatives**: [Small panel top navigation](#small-panel-top-navigation), domain cluster.

**Source**: [navigation/overview](https://filamentphp.com/docs/5.x/navigation/overview.md) · [panels/navigation/group](https://filamentphp.com/docs/images/5.x/light/panels/navigation/group.jpg)

```php
use Filament\Navigation\NavigationGroup;
use Filament\Panel;
use Filament\Support\Icons\Heroicon;

public function panel(Panel $panel): Panel
{
    return $panel
        ->id('admin')
        ->path('admin')
        ->navigationGroups([
            NavigationGroup::make()
                ->label('Customers')
                ->icon(Heroicon::OutlinedUsers),
            NavigationGroup::make()
                ->label('Orders')
                ->icon(Heroicon::OutlinedShoppingCart),
        ]);
}
```

**Responsive**: retain the active destination, group names, and actionable counts when the sidebar becomes a responsive menu, and do not make a collapsed icon-only shell the only way to discover a group or its current state.

**Accessibility**: keep group labels, expanded state, badges, and the current destination understandable without colour alone, and make collapse, expand, navigation, and user controls keyboard reachable with visible focus.

### Variant: Domain navigation groups

**When**: items belong to a stable, user-recognisable business domain within the same panel.

**Not when**: a group merely compensates for unclear domain ownership or hides unrelated destinations.

**Source**: [panels/navigation/group](https://filamentphp.com/docs/images/5.x/light/panels/navigation/group.jpg)

Assign each resource to the matching group configured on the panel — on `OrderResource`, for example:

```php
use UnitEnum;

protected static string | UnitEnum | null $navigationGroup = 'Orders';
```

### Variant: Actionable navigation badge

**When**: a count represents work a person can meaningfully act on, such as pending approvals.

**Not when**: the count is a vanity total, stale metric, or the only explanation of the destination.

**Source**: [panels/navigation/badge](https://filamentphp.com/docs/images/5.x/light/panels/navigation/badge.jpg)

Add badge getters on `OrderResource` for the pending queue — badges are resource methods, not panel fluent calls:

```php
public static function getNavigationBadge(): ?string
{
    return (string) static::getModel()::query()
        ->where('status', 'pending')
        ->count();
}

public static function getNavigationBadgeColor(): ?string
{
    return static::getModel()::query()
        ->where('status', 'pending')
        ->exists()
        ? 'warning'
        : 'primary';
}

public static function getNavigationBadgeTooltip(): ?string
{
    return 'Orders waiting for approval';
}
```

### Variant: Domain cluster

**When**: a cohesive domain needs its own sub-navigation and route structure while serving the same panel audience.

**Not when**: a simple group communicates the structure, or the domain has a separate audience and authentication boundary.

**Source**: [panels/cluster](https://filamentphp.com/docs/images/5.x/light/panels/cluster.jpg)

Discover clusters on the panel, define the cluster class, then point related resources at it with `$cluster`:

```php
->discoverClusters(in: app_path('Filament/Clusters'), for: 'App\\Filament\\Clusters')
```

```php
use BackedEnum;
use Filament\Clusters\Cluster;
use Filament\Support\Icons\Heroicon;

class OrdersCluster extends Cluster
{
    protected static string | BackedEnum | null $navigationIcon = Heroicon::OutlinedShoppingCart;

    protected static ?string $navigationLabel = 'Orders';
}
```

```php
use App\Filament\Clusters\Orders\OrdersCluster;

protected static ?string $cluster = OrdersCluster::class;
```

---

## Authentication surface hierarchy

**When**: a person must sign in, recover access, register, or maintain their own account, and the task needs one clear form hierarchy and immediate feedback.

**Not when**: a custom authentication layout is proposed before checking the supported panel authentication surface and established theme.

**Alternatives**: [Small panel top navigation](#small-panel-top-navigation), [Back-office sidebar navigation](#back-office-sidebar-navigation).

**Source**: [users/overview](https://filamentphp.com/docs/5.x/users/overview.md) · [panels/login](https://filamentphp.com/docs/images/5.x/light/panels/login.jpg)

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->id('admin')
        ->path('admin')
        ->login()
        ->registration()
        ->passwordReset()
        ->profile();
}
```

**Responsive**: keep the focused account task, labels, validation feedback, and recovery links readable before adding decorative shell content, and preserve a single-column form flow that does not displace feedback on narrow screens.

**Accessibility**: retain visible labels, logical focus order, visible focus, announced validation or status feedback, and keyboard access to recovery and account links; do not use brand colour, a logo, or a placeholder as the only explanation of a field, error, or action.

### Variant: Sign-in and registration

**When**: the panel supports account entry or registration and a clear path between them is appropriate.

**Not when**: registration is not an allowed account lifecycle for this panel.

**Source**: [panels/login](https://filamentphp.com/docs/images/5.x/light/panels/login.jpg)

Keep the account-entry pair on the panel when registration is allowed:

```php
->login()
->registration()
```

### Variant: Password recovery

**When**: a person who cannot sign in needs a focused recovery action and a route back to login.

**Not when**: recovery is hidden, unlabeled, or competes with unrelated navigation.

**Source**: [panels/password-reset](https://filamentphp.com/docs/images/5.x/light/panels/password-reset.jpg)

Enable the password-reset surface on the panel:

```php
->passwordReset()
```

### Variant: Profile and account security

**When**: authenticated people need to maintain their own identity or account security without entering operational navigation.

**Not when**: a broad administrative settings workflow is presented as a personal account form.

**Source**: [panels/profile](https://filamentphp.com/docs/images/5.x/light/panels/profile.jpg)

Keep the simple personal profile surface on the panel, and label the user-menu profile action clearly:

```php
use Filament\Actions\Action;

->profile()
->userMenuItems([
    'profile' => fn (Action $action) => $action->label('Edit profile'),
])
```
