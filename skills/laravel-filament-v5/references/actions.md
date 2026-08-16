# Actions (`Filament\Actions\*` — ALWAYS this namespace)

`Filament\Tables\Actions\*` was **removed** in v5. Every action — page header, table row, bulk, infolist, form — imports from `Filament\Actions\*`.

Signatures below are focused fragments; import each action class and the host `Filament\Tables\Table` in the target class.

For *which* action and feedback arrangement to build — grouping, confirmation, overlays, notifications, callouts, empty states — use `laravel-filament-v5-ui-ux`, `references/action-feedback.md`. This file is the API inventory.

| Component | Minimal signature | 5.x doc |
|---|---|---|
| `Action` | `Action::make('approve')->requiresConfirmation()->action(fn ($record) => ...)` | [overview](https://filamentphp.com/docs/5.x/actions/overview.md) |
| Action with modal/form | `Action::make('edit')->schema([TextInput::make('reason')])` — modals use `->schema()`, **not** `->form()` | [modals](https://filamentphp.com/docs/5.x/actions/modals.md) |
| `CreateAction`, `EditAction`, `ViewAction`, `DeleteAction`, `ActionGroup`, `BulkAction`, `DeleteBulkAction`, `ImportAction`, `ExportAction` | `DeleteAction::make()` | [overview](https://filamentphp.com/docs/5.x/actions/overview.md) |

## Where actions live on a table

```php
use Filament\Actions\ActionGroup;
use Filament\Actions\CreateAction;
use Filament\Actions\DeleteAction;
use Filament\Actions\DeleteBulkAction;
use Filament\Actions\EditAction;
use Filament\Actions\ViewAction;
use Filament\Tables\Table;

$table
    ->recordActions([          // per row
        ActionGroup::make([
            ViewAction::make(),
            EditAction::make(),
            DeleteAction::make(),
        ]),
    ])
    ->toolbarActions([         // above the table
        CreateAction::make(),
    ])
    ->groupedBulkActions([     // on selected records
        DeleteBulkAction::make(),
    ])
```

## Conventions

- **Confirmation**: destructive or irreversible actions get `->requiresConfirmation()` — never a bare `->action()` that deletes.
- **Modal with input**: `->schema([...])` + the data arrives in `->action(function (array $data, $record) { ... })`.
- **Authorization**: custom actions that read or mutate protected data need explicit authorization. Use policies and the action's documented authorization API; `->visible()` / `->hidden()` improve the UI but are not the server-side boundary. Read `references/security.md`.
- **Visibility**: use `->visible(fn ($record) => ...)` / `->hidden(...)` for presentation instead of conditionally building the actions array.
- **Feedback**: first check whether the Resource page or built-in action already sends success/failure feedback. Add or customize a `Filament\Notifications\Notification` for custom state changes when needed, without emitting a duplicate notification.
- **Row actions**: when several low-frequency actions make a row noisy, wrap them in `ActionGroup::make([...])`; keep the common action easy to reach and destructive actions last.
- **Icons**: for Heroicons in PHP, prefer `->icon(Heroicon::PencilSquare)` for autocomplete and contextual sizing. Use string names for installed third-party/custom icon sets, as documented by Filament's icons guide.
- **Business logic**: follow the project's existing architecture. Keep small UI-local mutations readable in the callback; delegate reusable, transactional, or domain-heavy work to the established application/domain layer.
