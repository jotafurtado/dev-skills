# Notifications (`Filament\Notifications\Notification`)

Silent actions feel broken — after any state change, send feedback (already mandated in `references/actions.md`). Filament has three delivery channels: **flash** (session, instant), **database** (persisted, polled), **broadcast** (real-time via websockets).

Signatures below are focused fragments; import `Filament\Notifications\Notification` and any action/enum classes in the host class.

## Flash notifications

`send()` flashes via session — works from anywhere in request-handling code, including JavaScript, not just Livewire components. Not from queued jobs: a queue worker has no user session, so the flash never reaches the browser — use the database or broadcast channel there. ([overview](https://filamentphp.com/docs/5.x/notifications/overview.md))

```php
use Filament\Actions\Action;
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->send();
```

| Concern | Chainable |
|---|---|
| Status (icon + color) | `->success()` / `->warning()` / `->danger()` / `->info()` |
| Body text | `->body('Changes have been saved.')` |
| Custom icon | `->icon('heroicon-o-document-text')->iconColor('success')` |
| Duration | `->duration(5000)` (ms) or `->seconds(5)` — default 6 s |
| Persistent | `->persistent()` (no auto-close) |
| Action buttons | `->actions([Action::make('undo')->button()])` |

## Database notifications

Persisted per-user; the panel polls for new ones. Enable per panel in the panel provider (see `references/panels.md`):

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        // ...
        ->databaseNotifications();
}
```

Position defaults to the topbar; force sidebar with `->databaseNotifications(position: DatabaseNotificationsPosition::Sidebar)` (import `Filament\Enums\DatabaseNotificationsPosition`).

Send:

```php
use Filament\Notifications\Notification;

$recipient = auth()->user();

Notification::make()
    ->title('Saved successfully')
    ->sendToDatabase($recipient);
```

Polling defaults to `'30s'`; change with `->databaseNotificationsPolling('30s')` in the panel provider, or `->databaseNotificationsPolling(null)` to disable.

Actions on database notifications can mark read state: `->actions([Action::make('view')->button()->markAsRead()])` (also `->markAsUnread()`). ([database notifications](https://filamentphp.com/docs/5.x/notifications/database-notifications.md))

## Broadcast notifications

Real-time delivery via Laravel Echo + a websockets driver (Pusher, Ably, etc.). Requires Echo configured in `config/filament.php` (`broadcasting.echo` section) and `VITE_*` env entries. ([broadcast notifications](https://filamentphp.com/docs/5.x/notifications/broadcast-notifications.md))

```php
use Filament\Notifications\Notification;

$recipient = auth()->user();

Notification::make()
    ->title('Saved successfully')
    ->broadcast($recipient);
```

## Testing

Assert flash notifications in Livewire tests with `->assertNotified()` (optionally pass the title or a full `Notification` object). See `references/testing.md` and [testing notifications](https://filamentphp.com/docs/5.x/testing/testing-notifications.md).
