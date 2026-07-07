# Widgets & dashboards (`Filament\Widgets\*`)

Widgets are Livewire components. Three official templates cover almost every dashboard need — a custom widget view is the last resort, not the first. ([overview](https://filamentphp.com/docs/5.x/widgets/overview.md))

```bash
php artisan make:filament-widget MyWidget            # asks: custom / chart / stats overview / table
php artisan make:filament-widget StatsOverview --stats-overview
php artisan make:filament-widget BlogPostsChart --chart
php artisan make:filament-widget LatestOrders --table
```

## Stats overview — KPI cards

([stats-overview doc](https://filamentphp.com/docs/5.x/widgets/stats-overview.md))

```php
use Filament\Widgets\StatsOverviewWidget as BaseWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class StatsOverview extends BaseWidget
{
    protected function getStats(): array
    {
        return [
            Stat::make('Unique views', '192.1k')
                ->description('32k increase')
                ->descriptionIcon(Heroicon::ArrowTrendingUp)
                ->chart([7, 2, 10, 3, 15, 4, 17])   // inline sparkline
                ->color('success'),
        ];
    }
}
```

Note: the docs' own example uses the raw string `'heroicon-m-arrow-trending-up'` (the small "mini" variant) for `descriptionIcon()`. Using `Heroicon::ArrowTrendingUp` (the enum, per SKILL.md) is not a downgrade — Filament auto-resolves the `Heroicon` enum to the correctly-sized underlying icon for whatever context it's rendered in, so the enum form is both type-safe and produces the same result.

Optional heading above the cards: `protected ?string $heading` / `$description`.

## Chart widgets — Chart.js under the hood

([charts doc](https://filamentphp.com/docs/5.x/widgets/charts.md)) Types: `'line'`, `'bar'`, `'pie'`, `'doughnut'`, `'radar'`, `'polarArea'`, `'scatter'`, `'bubble'`.

```php
use Filament\Widgets\ChartWidget;

class BlogPostsChart extends ChartWidget
{
    protected ?string $heading = 'Blog Posts';

    protected function getData(): array
    {
        return [
            'datasets' => [['label' => 'Posts created', 'data' => [0, 10, 5, 21, 45]]],
            'labels' => ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        ];
    }

    protected function getType(): string
    {
        return 'line';
    }
}
```

- `protected string $color = 'info';` for the dataset color; raw Chart.js `backgroundColor`/`borderColor` in `getData()` for multi-dataset control.
- For time-series data from Eloquent, the docs recommend `flowframe/laravel-trend` (`Trend::model(...)->between(...)->perMonth()->count()`).
- Chart filter select: `public ?string $filter = 'today';` + `getFilters(): ?array` returning `value => label`.

## Table widgets

`make:filament-widget LatestOrders --table` — then configure `table()` exactly like a resource table (see `references/tables.md`).

## Widget behavior on any type

| Concern | API |
|---|---|
| Order on the page | `protected static ?int $sort = 2;` |
| Width | `protected int | string | array $columnSpan = 'full';` (1–12, `'full'`, or responsive array `['md' => 2, 'xl' => 3]`) |
| Visibility | `public static function canView(): bool` |
| Polling | `protected ?string $pollingInterval = '10s';` — default `5s`, set `null` to disable (do it for expensive queries) |
| Lazy loading | on by default; `protected static bool $isLazy = false;` to disable |

## Dashboard-level configuration

Replace the default dashboard by creating `app/Filament/Pages/Dashboard.php` extending `Filament\Pages\Dashboard`, then:

- **Grid columns**: `public function getColumns(): int | array` (e.g. `2`, or `['md' => 4, 'xl' => 5]`).
- **Global filters form**: `use HasFiltersForm;` + `filtersForm(Schema $schema)` on the dashboard; widgets read them via `use InteractsWithPageFilters;` and `$this->pageFilters['startDate']` — that data is **not validated**, guard before querying. Prefer `HasFiltersAction` + `FilterAction::make()` in `getHeaderActions()` when filters should validate and only apply on submit.
- **Multiple dashboards**: extra classes extending `Dashboard` with `protected static string $routePath = 'finance';`.
