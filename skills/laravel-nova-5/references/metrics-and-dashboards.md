# Metrics and Dashboards

Read:

- [Defining Metrics](https://nova.laravel.com/docs/v5/metrics/defining-metrics.md)
- [Registering Metrics](https://nova.laravel.com/docs/v5/metrics/registering-metrics.md)
- [Dashboards](https://nova.laravel.com/docs/v5/customization/dashboards.md)

Nova 5 documents five metric types: Value, Trend, Partition, Progress, and
Table. Use the generated class and result type for the installed version.

## Value and trend metrics

Generate with `nova:value` or `nova:trend`:

```php
<?php

namespace App\Nova\Metrics;

use App\Models\User;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Metrics\Value;
use Laravel\Nova\Metrics\ValueResult;
use Laravel\Nova\Nova;

class NewUsers extends Value
{
    public function calculate(NovaRequest $request): ValueResult
    {
        return $this->count($request, User::class);
    }

    public function ranges(): array
    {
        return [
            30 => Nova::__('30 Days'),
            60 => Nova::__('60 Days'),
            365 => Nova::__('365 Days'),
        ];
    }

    public function cacheFor(): ?\DateTimeInterface
    {
        return now()->addMinutes(5);
    }

    public function name()
    {
        return 'Users Created';
    }
}
```

```php
<?php

namespace App\Nova\Metrics;

use App\Models\User;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Metrics\Trend;
use Laravel\Nova\Metrics\TrendResult;

class UsersPerDay extends Trend
{
    public function calculate(NovaRequest $request): TrendResult
    {
        return $this->countByDays($request, User::class);
    }

    public function ranges(): array
    {
        return [
            7 => '7 Days',
            30 => '30 Days',
        ];
    }
}
```

The v5 docs list count, average, sum, max, and min helpers for value metrics and
interval-specific helpers for trends. Copy the needed helper's current
signature instead of generalizing every helper to one argument list. Query
builders may be used where documented to scope data.

Cache only when staleness is acceptable. Verify filter, range, and tenant
behavior before caching sensitive or user-specific results.

## Partition, progress, and table metrics

```php
<?php

namespace App\Nova\Metrics;

use App\Models\User;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Metrics\Partition;
use Laravel\Nova\Metrics\PartitionResult;

class UsersPerPlan extends Partition
{
    public function calculate(NovaRequest $request): PartitionResult
    {
        return $this->count($request, User::class, 'plan')
            ->label(fn ($value) => match ($value) {
                'basic' => 'Basic',
                'pro' => 'Professional',
                default => ucfirst((string) $value),
            });
    }
}
```

```php
<?php

namespace App\Nova\Metrics;

use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Metrics\Progress;
use Laravel\Nova\Metrics\ProgressResult;

class OnboardingCompletion extends Progress
{
    public function calculate(NovaRequest $request): ProgressResult
    {
        return $this->result(80, 100);
    }
}
```

```php
<?php

namespace App\Nova\Metrics;

use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Metrics\MetricTableRow;
use Laravel\Nova\Metrics\Table;

class NewReleases extends Table
{
    /**
     * @return array<int, MetricTableRow>
     */
    public function calculate(NovaRequest $request): array
    {
        return [
            MetricTableRow::make()
                ->title('Version 1.0')
                ->subtitle('Initial application release')
                ->icon('star'),
        ];
    }
}
```

Avoid examples that assert time-sensitive framework release status. Use
application data and official result APIs for links, actions, icons, prefixes,
suffixes, formatting, and colors.

## Register metrics

Metrics are registered in a resource's `cards()` method or a dashboard's
`cards()` method:

```php
use App\Models\User;
use App\Nova\Metrics\NewUsers;
use App\Nova\Metrics\UsersPerDay;
use Laravel\Nova\Http\Requests\NovaRequest;

// Fragment: method on a Nova resource.
public function cards(NovaRequest $request): array
{
    return [
        NewUsers::make()
            ->defaultRange(30)
            ->width('1/3'),

        UsersPerDay::make()
            ->refreshWhenActionsRun()
            ->refreshWhenFiltersChange()
            ->canSeeWhen('viewUsersPerDay', User::class),
    ];
}
```

Use `onlyOnDetail()` for detail metrics and scope calculations with the
documented request resource ID. `refreshWhenActionsRun()` and
`refreshWhenFiltersChange()` are opt-in. `canSee` and `canSeeWhen` belong on the
registered metric instance.

## Default dashboard

Nova ships with `App\Nova\Dashboards\Main`. Customize its `cards()` method:

```php
<?php

namespace App\Nova\Dashboards;

use App\Nova\Metrics\NewUsers;
use Laravel\Nova\Dashboards\Main as Dashboard;

class Main extends Dashboard
{
    public function cards(): array
    {
        return [
            NewUsers::make()->width('1/3'),
        ];
    }
}
```

The default `Main` dashboard is not generated with
`php artisan nova:dashboard Main`; it ships with Nova. Use the command for a
custom dashboard, for example:

```shell
php artisan nova:dashboard UserInsights
```

Custom dashboards extend `Laravel\Nova\Dashboard`. Customize the navigation
name with the documented instance method:

```php
<?php

namespace App\Nova\Dashboards;

use App\Nova\Metrics\UsersPerDay;
use Laravel\Nova\Dashboard;

class UserInsights extends Dashboard
{
    public function cards(): array
    {
        return [
            UsersPerDay::make(),
        ];
    }

    public function name()
    {
        return 'User Insights';
    }
}
```

Do not use `label()` for the dashboard navigation name.

## Register and authorize dashboards

Register dashboard instances in `NovaServiceProvider::dashboards()` with
`::make()`. Apply visibility authorization during registration, not through an
invented dashboard `authorize()` method:

```php
use App\Models\User;
use App\Nova\Dashboards\Main;
use App\Nova\Dashboards\UserInsights;

// Fragment: method on App\Providers\NovaServiceProvider.
protected function dashboards(): array
{
    return [
        Main::make(),
        UserInsights::make()
            ->canSeeWhen('viewUserInsights', User::class),
    ];
}
```

The equivalent closure form is
`UserInsights::make()->canSee(fn ($request) => ...)`. Use
`showRefreshButton()` on a registered dashboard when users need to refresh all
contained metrics manually.
