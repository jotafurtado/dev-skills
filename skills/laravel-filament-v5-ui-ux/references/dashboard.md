# Dashboard compositions

Ready-to-adapt dashboard compositions for Filament 5. Pick the one whose `When` matches the task, paste it, and rename the model, measures, and queue to the target domain.

Examples use an `Order` operations domain consistently across this library.

`laravel-filament-v5` owns widget API signatures, authorization, and tests. This file owns how the widgets are arranged for an operational decision.

| Pattern | Use it for |
|---|---|
| [Operational dashboard](#operational-dashboard) | Current order state, a meaningful trend, then a narrow actionable queue |

---

## Operational dashboard

**When**: a person needs to notice today's order state, investigate a meaningful trend, then act on recent or exceptional orders.

**Not when**: a custom card system is proposed when a Stats Overview, Chart, or Table widget can express the decision; every available metric receives equal size, prominence, or polling; or a chart is chosen for visual novelty without a question, period, or comparable scale.

**Alternatives**: a single stats-overview, chart-widget, or table-widget when only one of those answers the question.

**Source**: [widgets/overview](https://filamentphp.com/docs/5.x/widgets/overview.md) · [panels/dashboard](https://filamentphp.com/docs/images/5.x/light/panels/dashboard.jpg)

Assemble the dashboard in decision order — numbers of the day, then trend, then the actionable queue — and register that order explicitly:

```php
use App\Filament\Widgets\ActionableOrdersQueue;
use App\Filament\Widgets\OrderOperationsStats;
use App\Filament\Widgets\OrdersTrendChart;
use Filament\Pages\Dashboard as BaseDashboard;

class Dashboard extends BaseDashboard
{
    public function getWidgets(): array
    {
        return [
            OrderOperationsStats::class,
            OrdersTrendChart::class,
            ActionableOrdersQueue::class,
        ];
    }

    public function getColumns(): int | array
    {
        return [
            'md' => 2,
            'xl' => 3,
        ];
    }
}
```

```php
use App\Models\Order;
use Filament\Support\Icons\Heroicon;
use Filament\Widgets\StatsOverviewWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class OrderOperationsStats extends StatsOverviewWidget
{
    protected static ?int $sort = 1;

    protected ?string $pollingInterval = null;

    protected ?string $heading = 'Orders today';

    protected ?string $description = 'Current fulfilment pressure before deeper trend or queue work.';

    protected function getStats(): array
    {
        return [
            Stat::make('Open orders', Order::query()->open()->count())
                ->description('Needs fulfilment attention')
                ->descriptionIcon(Heroicon::ArrowTrendingUp)
                ->chart([12, 14, 13, 15, 18, 17, 21])
                ->color('warning'),
            Stat::make('Paid today', Order::query()->paidToday()->count())
                ->description('12% above yesterday')
                ->descriptionIcon(Heroicon::ArrowTrendingUp)
                ->chart([8, 9, 11, 10, 12, 13, 16])
                ->color('success'),
            Stat::make('Exceptions', Order::query()->exceptions()->count())
                ->description('Payment or fulfilment blocked')
                ->descriptionIcon(Heroicon::ExclamationTriangle)
                ->chart([3, 2, 4, 5, 4, 6, 5])
                ->color('danger'),
        ];
    }
}
```

```php
use App\Models\Order;
use Filament\Widgets\ChartWidget;
use Flowframe\Trend\Trend;
use Flowframe\Trend\TrendValue;

class OrdersTrendChart extends ChartWidget
{
    protected static ?int $sort = 2;

    protected ?string $heading = 'Orders over the last 7 days';

    protected ?string $description = 'Volume that explains whether today is an outlier.';

    protected string $color = 'info';

    protected int | string | array $columnSpan = [
        'md' => 2,
        'xl' => 2,
    ];

    protected function getData(): array
    {
        $data = Trend::model(Order::class)
            ->between(
                start: now()->subDays(6)->startOfDay(),
                end: now()->endOfDay(),
            )
            ->perDay()
            ->count();

        return [
            'datasets' => [
                [
                    'label' => 'Orders placed',
                    'data' => $data->map(fn (TrendValue $value) => $value->aggregate),
                ],
            ],
            'labels' => $data->map(fn (TrendValue $value) => $value->date),
        ];
    }

    protected function getType(): string
    {
        return 'line';
    }
}
```

```php
use App\Filament\Resources\Orders\OrderResource;
use App\Models\Order;
use Filament\Actions\Action;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;
use Filament\Widgets\TableWidget;

class ActionableOrdersQueue extends TableWidget
{
    protected static ?int $sort = 3;

    protected int | string | array $columnSpan = 'full';

    public function table(Table $table): Table
    {
        return $table
            ->heading('Orders needing action')
            ->description('Exceptions and fulfilment blockers after the summary.')
            ->query(
                Order::query()
                    ->whereIn('status', [
                        'payment_failed',
                        'awaiting_fulfilment',
                        'exception',
                    ])
                    ->latest(),
            )
            ->columns([
                TextColumn::make('number')
                    ->label('Order')
                    ->searchable(),
                TextColumn::make('customer.name')
                    ->label('Customer'),
                TextColumn::make('status')
                    ->badge(),
                TextColumn::make('total')
                    ->money('USD'),
                TextColumn::make('created_at')
                    ->since()
                    ->label('Waiting'),
            ])
            ->recordActions([
                Action::make('open')
                    ->url(fn (Order $record): string => OrderResource::getUrl('view', ['record' => $record])),
            ])
            ->paginated([5]);
    }
}
```

**Responsive**: start with a readable one-column widget flow, then give the trend and queue wider spans only when their density needs it; keep headline metrics and the next actionable exception visible before secondary analytics.

**Accessibility**: pair semantic trend colour with a readable direction and change label; give widgets concise headings and descriptions that state the decision or time period; keep dashboard filters, table actions, and chart controls named, keyboard reachable, and visibly focused.

### Variant: Decision-relevant stats

**When**: a small number of current measures and their direction let a person decide whether to investigate or act.

**Not when**: stat tiles merely repeat available data, omit their comparison period, or form an unrelated card system.

**Source**: [widgets/stats-overview](https://filamentphp.com/docs/5.x/widgets/stats-overview.md) · [widgets/stats-overview/chart](https://filamentphp.com/docs/images/5.x/light/widgets/stats-overview/chart.jpg)

Keep the Stats Overview as the first widget. Each tile needs a recognisable measure, comparison or consequence text, and colour only as reinforcement:

```php
use App\Models\Order;
use Filament\Support\Icons\Heroicon;
use Filament\Widgets\StatsOverviewWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class OrderOperationsStats extends StatsOverviewWidget
{
    protected static ?int $sort = 1;

    protected ?string $pollingInterval = null;

    protected ?string $heading = 'Orders today';

    protected ?string $description = 'Current fulfilment pressure before deeper trend or queue work.';

    protected function getStats(): array
    {
        return [
            Stat::make('Open orders', Order::query()->open()->count())
                ->description('Needs fulfilment attention')
                ->descriptionIcon(Heroicon::ArrowTrendingUp)
                ->chart([12, 14, 13, 15, 18, 17, 21])
                ->color('warning'),
            Stat::make('Paid today', Order::query()->paidToday()->count())
                ->description('12% above yesterday')
                ->descriptionIcon(Heroicon::ArrowTrendingUp)
                ->chart([8, 9, 11, 10, 12, 13, 16])
                ->color('success'),
            Stat::make('Exceptions', Order::query()->exceptions()->count())
                ->description('Payment or fulfilment blocked')
                ->descriptionIcon(Heroicon::ExclamationTriangle)
                ->chart([3, 2, 4, 5, 4, 6, 5])
                ->color('danger'),
        ];
    }
}
```

### Variant: Trend chart

**When**: change over time, distribution, or a comparison between series answers a recurring question that a single metric cannot.

**Not when**: the values need exact record-level action first, or the chart has no stated decision, period, or meaningful scale.

**Source**: [widgets/charts](https://filamentphp.com/docs/5.x/widgets/charts.md) · [widgets/chart/line](https://filamentphp.com/docs/images/5.x/light/widgets/chart/line.jpg)

Place the Chart widget after the stats. State the period in the heading, and keep a local period control only when it answers this chart's question:

```php
use App\Models\Order;
use Filament\Widgets\ChartWidget;
use Flowframe\Trend\Trend;
use Flowframe\Trend\TrendValue;

class OrdersTrendChart extends ChartWidget
{
    protected static ?int $sort = 2;

    protected ?string $heading = 'Orders over the selected period';

    protected ?string $description = 'Volume that explains whether today is an outlier.';

    protected string $color = 'info';

    public ?string $filter = 'week';

    protected int | string | array $columnSpan = [
        'md' => 2,
        'xl' => 2,
    ];

    protected function getFilters(): ?array
    {
        return [
            'week' => 'Last 7 days',
            'month' => 'Last 30 days',
            'year' => 'This year',
        ];
    }

    protected function getData(): array
    {
        [$start, $per] = match ($this->filter) {
            'month' => [now()->subDays(29)->startOfDay(), 'perDay'],
            'year' => [now()->startOfYear(), 'perMonth'],
            default => [now()->subDays(6)->startOfDay(), 'perDay'],
        };

        $trend = Trend::model(Order::class)
            ->between(start: $start, end: now()->endOfDay());

        $data = $per === 'perMonth'
            ? $trend->perMonth()->count()
            : $trend->perDay()->count();

        return [
            'datasets' => [
                [
                    'label' => 'Orders placed',
                    'data' => $data->map(fn (TrendValue $value) => $value->aggregate),
                ],
            ],
            'labels' => $data->map(fn (TrendValue $value) => $value->date),
        ];
    }

    protected function getType(): string
    {
        return 'line';
    }
}
```

### Variant: Table-widget queue

**When**: people need a compact queue of recent, exceptional, or actionable records after reading the summary.

**Not when**: the dashboard duplicates a full management table without a narrower operational purpose.

**Source**: [widgets/overview](https://filamentphp.com/docs/5.x/widgets/overview.md) · [panels/dashboard](https://filamentphp.com/docs/images/5.x/light/panels/dashboard.jpg)

Keep the Table widget last. Show identity, decision-driving state, and the next action — not the whole orders resource:

```php
use App\Filament\Resources\Orders\OrderResource;
use App\Models\Order;
use Filament\Actions\Action;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;
use Filament\Widgets\TableWidget;

class ActionableOrdersQueue extends TableWidget
{
    protected static ?int $sort = 3;

    protected int | string | array $columnSpan = 'full';

    public function table(Table $table): Table
    {
        return $table
            ->heading('Orders needing action')
            ->description('Exceptions and fulfilment blockers after the summary.')
            ->query(
                Order::query()
                    ->whereIn('status', [
                        'payment_failed',
                        'awaiting_fulfilment',
                        'exception',
                    ])
                    ->latest(),
            )
            ->columns([
                TextColumn::make('number')
                    ->label('Order')
                    ->searchable(),
                TextColumn::make('customer.name')
                    ->label('Customer'),
                TextColumn::make('status')
                    ->badge(),
                TextColumn::make('total')
                    ->money('USD'),
                TextColumn::make('created_at')
                    ->since()
                    ->label('Waiting'),
            ])
            ->recordActions([
                Action::make('open')
                    ->url(fn (Order $record): string => OrderResource::getUrl('view', ['record' => $record])),
            ])
            ->paginated([5]);
    }
}
```

### Variant: Dashboard filters

**When**: one shared time period, scope, or named subset changes several widgets and the active scope must remain visible.

**Not when**: a local chart or table question can be answered by a scoped control without changing unrelated widgets.

**Source**: [widgets/overview](https://filamentphp.com/docs/5.x/widgets/overview.md) · [panels/dashboard-filters](https://filamentphp.com/docs/images/5.x/light/panels/dashboard-filters.jpg)

Add a shared filters form on the dashboard and read `$this->pageFilters` from widgets that should move together. Guard the values before querying — live filter data is not validated. Prefer `HasFiltersAction` with `FilterAction` when filters should validate and apply only on submit:

```php
use Filament\Forms\Components\DatePicker;
use Filament\Pages\Dashboard as BaseDashboard;
use Filament\Pages\Dashboard\Concerns\HasFiltersForm;
use Filament\Schemas\Components\Section;
use Filament\Schemas\Schema;

class Dashboard extends BaseDashboard
{
    use HasFiltersForm;

    public function getWidgets(): array
    {
        return [
            OrderOperationsStats::class,
            OrdersTrendChart::class,
            ActionableOrdersQueue::class,
        ];
    }

    public function getColumns(): int | array
    {
        return [
            'md' => 2,
            'xl' => 3,
        ];
    }

    public function filtersForm(Schema $schema): Schema
    {
        return $schema
            ->components([
                Section::make()
                    ->schema([
                        DatePicker::make('startDate')
                            ->label('From'),
                        DatePicker::make('endDate')
                            ->label('Until'),
                    ])
                    ->columns(2),
            ]);
    }
}
```

```php
use App\Models\Order;
use Filament\Support\Icons\Heroicon;
use Filament\Widgets\Concerns\InteractsWithPageFilters;
use Filament\Widgets\StatsOverviewWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;
use Illuminate\Database\Eloquent\Builder;

class OrderOperationsStats extends StatsOverviewWidget
{
    use InteractsWithPageFilters;

    protected static ?int $sort = 1;

    protected ?string $pollingInterval = null;

    protected ?string $heading = 'Orders in scope';

    protected ?string $description = 'Headline measures for the selected period.';

    protected function getStats(): array
    {
        $startDate = $this->pageFilters['startDate'] ?? null;
        $endDate = $this->pageFilters['endDate'] ?? null;

        $orders = Order::query()
            ->when($startDate, fn (Builder $query) => $query->whereDate('created_at', '>=', $startDate))
            ->when($endDate, fn (Builder $query) => $query->whereDate('created_at', '<=', $endDate));

        return [
            Stat::make('Open orders', (clone $orders)->open()->count())
                ->description('Needs fulfilment attention')
                ->descriptionIcon(Heroicon::ArrowTrendingUp)
                ->color('warning'),
            Stat::make('Paid', (clone $orders)->paid()->count())
                ->description('Completed payment in scope')
                ->descriptionIcon(Heroicon::ArrowTrendingUp)
                ->color('success'),
            Stat::make('Exceptions', (clone $orders)->exceptions()->count())
                ->description('Payment or fulfilment blocked')
                ->descriptionIcon(Heroicon::ExclamationTriangle)
                ->color('danger'),
        ];
    }
}
```

### Variant: Responsive widget span

**When**: a trend or activity widget needs more horizontal space than a concise metric while smaller viewports can stack it.

**Not when**: equal spans obscure operational priority, or a wide widget leaves no readable mobile fallback.

**Source**: [widgets/overview](https://filamentphp.com/docs/5.x/widgets/overview.md) · [panels/dashboard-column-spans](https://filamentphp.com/docs/images/5.x/light/panels/dashboard-column-spans.jpg)

Pair a responsive `getColumns()` grid with per-widget `$columnSpan` values. Concise stats share the row; the chart and queue claim wider spans only where density needs them:

```php
class Dashboard extends BaseDashboard
{
    public function getWidgets(): array
    {
        return [
            OrderOperationsStats::class,
            OrdersTrendChart::class,
            ActionableOrdersQueue::class,
        ];
    }

    public function getColumns(): int | array
    {
        return [
            'default' => 1,
            'md' => 2,
            'xl' => 3,
        ];
    }
}
```

```php
class OrderOperationsStats extends StatsOverviewWidget
{
    protected static ?int $sort = 1;

    protected int | string | array $columnSpan = [
        'md' => 2,
        'xl' => 3,
    ];

    // ...
}
```

```php
class OrdersTrendChart extends ChartWidget
{
    protected static ?int $sort = 2;

    protected int | string | array $columnSpan = [
        'md' => 2,
        'xl' => 2,
    ];

    // ...
}
```

```php
class ActionableOrdersQueue extends TableWidget
{
    protected static ?int $sort = 3;

    protected int | string | array $columnSpan = 'full';

    // ...
}
```
