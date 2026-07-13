# Actions, Filters, and Lenses

Read the official v5 pages before implementing:

- [Defining Actions](https://nova.laravel.com/docs/v5/actions/defining-actions.md)
- [Registering Actions](https://nova.laravel.com/docs/v5/actions/registering-actions.md)
- [Defining Filters](https://nova.laravel.com/docs/v5/filters/defining-filters.md)
- [Registering Filters](https://nova.laravel.com/docs/v5/filters/registering-filters.md)
- [Defining Lenses](https://nova.laravel.com/docs/v5/lenses/defining-lenses.md)
- [Registering Lenses](https://nova.laravel.com/docs/v5/lenses/registering-lenses.md)

## Actions

Generate with `php artisan nova:action SendWelcomeEmail`. Use `--queued` only
when queueing is appropriate.

```php
<?php

namespace App\Nova\Actions;

use Illuminate\Support\Collection;
use Laravel\Nova\Actions\Action;
use Laravel\Nova\Actions\ActionResponse;
use Laravel\Nova\Fields\ActionFields;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

class SendWelcomeEmail extends Action
{
    /** @var \Stringable|string */
    public $name = 'Send Welcome Email';

    public function handle(
        ActionFields $fields,
        Collection $models
    ): ActionResponse {
        foreach ($models as $model) {
            // Dispatch application-owned mail work.
        }

        return ActionResponse::message('Emails sent successfully.');
    }

    /**
     * @return array<int, \Laravel\Nova\Fields\Field>
     */
    public function fields(NovaRequest $request): array
    {
        return [
            Text::make('Subject')->rules('required'),
        ];
    }
}
```

Match `handle()`'s return type to the installed stub if it differs. Action
`handle()` always receives a collection, including sole actions.

### Registration and authorization

```php
use App\Nova\Actions\SendWelcomeEmail;
use Laravel\Nova\Http\Requests\NovaRequest;

// Fragment: method on a Nova resource.
public function actions(NovaRequest $request): array
{
    return [
        SendWelcomeEmail::make()
            ->canSee(fn ($request) => $request->user()->can('emailAnyAccount'))
            ->canRun(
                fn ($request, $model) => $request->user()->can('email', $model)
            )
            ->confirmText('Send this email?')
            ->confirmButtonText('Send')
            ->cancelButtonText('Cancel')
            ->size('2xl'),
    ];
}
```

Execution authorization order is:

1. Registered action `canRun`, if defined.
2. Policy `runAction` or `runDestructiveAction`, if defined.
3. Policy `update` or `delete`, if defined.
4. Otherwise, deny.

`canSee` controls visibility, not whether a specific selected model may run.

### Responses

Use `ActionResponse`, and preserve documented argument order:

```php
use Laravel\Nova\Actions\ActionResponse;

// Fragment: returned from Action::handle().
return ActionResponse::message('Done!');
return ActionResponse::danger('Something went wrong.');
return ActionResponse::redirect('https://example.com');
return ActionResponse::visit('/resources/posts/new');
return ActionResponse::openInNewTab('https://example.com');
return ActionResponse::download(
    'Invoice.pdf',
    'https://example.com/invoice.pdf'
);
```

`download()` receives the desired filename first and the downloadable URL
second. Escape untrusted data included in response messages because Nova does
not escape those messages before rendering.

For a custom modal response, follow the official example and return
`Action::modal('custom-vue-component', ['value' => $value])` from `handle()`.

For a registered static download action, use the separate documented API:

```php
use Laravel\Nova\Actions\Action;

// Fragment: item returned from a resource's actions() method.
Action::downloadUrl('Download User Summaries', function () {
    return route('users.summaries');
})->standalone(),
```

### Queued and batchable actions

```php
<?php

namespace App\Nova\Actions;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Support\Collection;
use Laravel\Nova\Actions\Action;
use Laravel\Nova\Fields\ActionFields;

class GenerateReport extends Action implements ShouldQueue
{
    use InteractsWithQueue;
    use Queueable;

    public function handle(ActionFields $fields, Collection $models): void
    {
        foreach ($models as $model) {
            // Perform application-owned report work.
            $this->markAsFinished($model);
        }
    }
}
```

Queue workers must be configured and running. Nova does not support `File`
fields on queued actions. `markAsFinished()` and `markAsFailed()` update action
log state; there is no documented generic `handleResult()` hook to add.

For action batching, implement `Laravel\Nova\Contracts\BatchableAction`, use
`Illuminate\Bus\Batchable`, and copy the documented `withBatch(ActionFields
$fields, PendingBatch $batch): void` signature and callbacks. Add all imports,
including `Batch`, `PendingBatch`, and `Throwable`.

Register resource-independent actions with `->standalone()` and single-model
actions with `->sole()`. Do not invent a `$standalone` property. Use
`->withoutConfirmation()` only when immediate execution is safe and intentional.

Attach `Laravel\Nova\Actions\Actionable` to the Eloquent model only when action
logging is needed. For very high-volume actions, evaluate the documented
`withoutActionEvents` options and their audit trade-off.

## Filters

Before writing a custom filter, check whether a documented filterable field
meets the requirement. Generate select filters with
`php artisan nova:filter UserType`; use the documented `--boolean` or `--date`
option for those variants.

```php
<?php

namespace App\Nova\Filters;

use Illuminate\Contracts\Database\Eloquent\Builder;
use Laravel\Nova\Filters\Filter;
use Laravel\Nova\Http\Requests\NovaRequest;

class UserType extends Filter
{
    /** @var string */
    public $component = 'select-filter';

    public function apply(
        NovaRequest $request,
        Builder $query,
        mixed $value
    ): Builder {
        return $query->where('type', $value);
    }

    /**
     * @return array<string, string>
     */
    public function options(NovaRequest $request): array
    {
        return [
            'Administrator' => 'admin',
            'Editor' => 'editor',
        ];
    }
}
```

Filter option keys are display labels; values reach `apply()`. Register the
filter in the resource's `filters(NovaRequest $request): array` method using
`new UserType` or `UserType::make()`. For dynamic reusable filters, override
`key()` as documented so multiple instances remain unique. Select filters may
be made searchable by chaining `->searchable()` during registration.

## Lenses

Lenses customize a resource query. Generate with
`php artisan nova:lens MostValuableUsers`.

```php
<?php

namespace App\Nova\Lenses;

use Illuminate\Contracts\Database\Eloquent\Builder;
use Illuminate\Contracts\Pagination\Paginator;
use Illuminate\Support\Facades\DB;
use Laravel\Nova\Fields\ID;
use Laravel\Nova\Fields\Number;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\LensRequest;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Lenses\Lens;

class MostValuableUsers extends Lens
{
    public static function query(
        LensRequest $request,
        Builder $query
    ): Builder|Paginator {
        return $request->withOrdering(
            $request->withFilters(
                $query
                    ->select([
                        'users.id',
                        'users.name',
                        DB::raw('sum(licenses.price) as revenue'),
                    ])
                    ->join('licenses', 'users.id', '=', 'licenses.user_id')
                    ->groupBy('users.id', 'users.name')
                    ->withCasts(['revenue' => 'float'])
            ),
            fn ($query) => $query->orderBy('revenue', 'desc')
        );
    }

    public function fields(NovaRequest $request): array
    {
        return [
            ID::make('ID', 'id'),
            Text::make('Name', 'name'),
            Number::make('Revenue', 'revenue'),
        ];
    }

    public function uriKey()
    {
        return 'most-valuable-users';
    }
}
```

Always apply `withFilters()` and `withOrdering()` as documented. Select the
resource ID when “Select All Matching” and deletion should remain available.
Lenses inherit resource actions by default; call `parent::actions($request)`
when extending rather than unintentionally discarding them.

Register lenses in the resource's `lenses()` method and apply `canSee` there
when visibility is conditional. Enable lens polling or larger page sizes only
after considering query cost.
