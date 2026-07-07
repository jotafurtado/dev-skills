# Actions (`Filament\Actions\*` — ALWAYS this namespace)

`Filament\Tables\Actions\*` was **removed** in v5. Every action — page header, table row, bulk, infolist, form — imports from `Filament\Actions\*`.

| Component | Minimal signature | 5.x doc |
|---|---|---|
| `Action` | `Action::make('approve')->requiresConfirmation()->action(fn ($record) => ...)` | [overview](https://filamentphp.com/docs/5.x/actions/overview.md) |
| Action with modal/form | `Action::make('edit')->schema([TextInput::make('reason')])` — modals use `->schema()`, **not** `->form()` | [modals](https://filamentphp.com/docs/5.x/actions/modals.md) |
| `CreateAction`, `EditAction`, `ViewAction`, `DeleteAction`, `ActionGroup`, `BulkAction`, `DeleteBulkAction`, `ImportAction`, `ExportAction` | `DeleteAction::make()` | [overview](https://filamentphp.com/docs/5.x/actions/overview.md) |

## Where actions live on a table

```php
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
- **Visibility**: `->visible(fn ($record) => ...)` / `->hidden(...)` — prefer over conditionally building the actions array.
- **Feedback**: after a state change, send `Notification::make()->title('...')->success()->send()` (`Filament\Notifications\Notification`). Silent actions feel broken.
- **Row actions**: 3+ actions on a row → wrap in `ActionGroup::make([...])`, most common first (View, Edit, Delete).
- **Icons**: `->icon(Heroicon::PencilSquare)` — enum only, never string names.
- **Business logic**: the closure in `->action()` should delegate to an application-layer action/service class; the Filament action handles UI concerns (confirmation, notification, redirect).
