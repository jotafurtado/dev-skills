# Action and feedback compositions

Ready-to-adapt compositions for acting on a record and reporting the outcome in Filament 5. Pick the interaction weight from risk, required input, and how much surrounding context the user must keep.

**This file is cross-surface.** The same decisions apply on tables, forms, schemas, and record details, so the compositions live here rather than inside one surface file. Reach for it whenever a surface needs an action, a confirmation, an overlay, a notification, a callout, or an empty state.

Examples use a `Customer` / `Order` domain consistently across this library.

`laravel-filament-v5` owns action API signatures, authorization, and tests. This file owns how the interaction is composed.

| Pattern | Use it for |
|---|---|
| [Action, feedback, and overlays](#action-feedback-and-overlays) | Acting on a record without losing task context, and reporting what happened |

---

## Action, feedback, and overlays

**When**: a user needs to act on the current record or page without losing the surrounding task context, and risk, required input, or reference material determines the interaction weight.

**Not when**: a long, multi-step, independently navigable workflow needs a full page; a notification would repeat feedback already visible beside the affected field; or an empty-state action cannot actually resolve the absence for this user.

**Alternatives**: the variants below are the alternatives — compact confirmation, focused modal form, reference-heavy slide-over, and full-page workflow are points on one scale.

**Source**: [actions/modals](https://filamentphp.com/docs/5.x/actions/modals.md) · [modal/confirmation](https://filamentphp.com/docs/images/5.x/light/actions/modal/confirmation.jpg)

The baseline: one frequent action stays direct, the rest group behind a labelled trigger, and anything consequential confirms before it runs.

```php
use Filament\Actions\Action;
use Filament\Actions\ActionGroup;
use Filament\Actions\DeleteAction;
use Filament\Actions\EditAction;
use Filament\Actions\ViewAction;
use Filament\Support\Icons\Heroicon;
use App\Models\Order;

->recordActions([
    EditAction::make(),
    ActionGroup::make([
        ViewAction::make(),
        Action::make('cancel')
            ->label('Cancel order')
            ->icon(Heroicon::XCircle)
            ->color('danger')
            ->requiresConfirmation()
            ->modalHeading('Cancel this order')
            ->modalDescription('The customer will be notified and the reserved stock released. This cannot be undone.')
            ->modalSubmitActionLabel('Yes, cancel it')
            ->action(fn (Order $record) => $record->cancel()),
        DeleteAction::make(),
    ])
        ->label('More actions')
        ->icon(Heroicon::EllipsisVertical),
])
```

**Responsive**: keep the action label, its risk, the cancel path, validation, and the result understandable when overlay content narrows or stacks. Keep a direct empty-state action reachable without a hover-only or icon-only path.

**Accessibility**: preserve keyboard triggering, visible focus, predictable focus movement into and back out of overlays, and an explicit cancel path. Name destructive consequences in text and pair danger colour with an icon or wording — never colour alone. Place one outcome message at the narrowest level that fully explains it, so feedback is not duplicated across field, callout, notification, and page.

### Variant: compact confirmation

**When**: the user already supplied the necessary information and only has to acknowledge a consequential, destructive, or irreversible operation.

**Not when**: the operation needs several inputs, substantial reference material, or a sequence that cannot be understood in a short decision.

**Source**: [modal/confirmation](https://filamentphp.com/docs/images/5.x/light/actions/modal/confirmation.jpg)

Confirmation with named consequences and an icon carrying the risk alongside colour:

```php
Action::make('refund')
    ->requiresConfirmation()
    ->color('danger')
    ->modalIcon(Heroicon::OutlinedBanknotes)
    ->modalHeading('Refund this order')
    ->modalDescription('The full amount returns to the original payment method within five business days.')
    ->modalSubmitActionLabel('Refund order')
    ->action(fn (Order $record) => $record->refund()),
```

### Variant: focused modal form

**When**: a short, focused set of inputs completes one action without needing persistent surrounding reference.

**Not when**: form and supporting information grow long enough that the modal conceals the task context or becomes a scrolling workflow.

**Source**: [modal/form](https://filamentphp.com/docs/images/5.x/light/actions/modal/form.jpg)

Modal inputs use `schema()`, and the submitted values arrive in `$data`:

```php
use Filament\Forms\Components\Select;
use Filament\Forms\Components\Textarea;

Action::make('reassign')
    ->label('Reassign owner')
    ->schema([
        Select::make('owner_id')
            ->label('New owner')
            ->options(fn () => User::query()->pluck('name', 'id'))
            ->required(),
        Textarea::make('reason')
            ->label('Reason')
            ->rows(3),
    ])
    ->action(fn (array $data, Order $record) => $record->reassign($data['owner_id'], $data['reason'])),
```

### Variant: action feedback notification

**When**: a completed action needs concise transient confirmation, failure recovery, or an optional immediate follow-up outside the control that started it.

**Not when**: the result is already fully explained beside the affected field, inside the overlay, or in persistent page state — that would duplicate the message.

**Source**: [notifications/actions](https://filamentphp.com/docs/images/5.x/light/notifications/actions.jpg)

One message, at the narrowest level that explains it, with the follow-up attached rather than described:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Order refunded')
    ->success()
    ->body('The amount returns to the original payment method within five business days.')
    ->actions([
        Action::make('view')
            ->button()
            ->url(route('orders.show', $order)),
    ])
    ->send();
```

### Variant: reference-heavy slide-over

**When**: the action needs a persistent view of the surrounding record, longer supporting content, or a task-oriented side panel.

**Not when**: the narrow panel makes comparison, validation, or a multi-step workflow harder than a page would.

**Source**: [modal/slide-over](https://filamentphp.com/docs/images/5.x/light/actions/modal/slide-over.jpg)

Same action, opened as a side panel instead of a centred modal:

```php
Action::make('editItems')
    ->label('Edit line items')
    ->slideOver()
    ->schema([
        // line item fields
    ])
    ->action(fn (array $data, Order $record) => $record->syncItems($data)),
```

### Variant: actionable empty state

**When**: the absence can be named concisely and this user can meaningfully create, connect, or otherwise resolve it.

**Not when**: a filtered no-result needs filter explanation and reset, or the user has no legitimate next action.

**Source**: [empty-state/actions](https://filamentphp.com/docs/images/5.x/light/components/empty-state/actions.jpg)

Inside a schema, the empty state names the absence and offers the resolution:

```php
use Filament\Schemas\Components\EmptyState;

EmptyState::make('No orders yet')
    ->description('When this customer places their first order, it will appear here.')
    ->icon(Heroicon::OutlinedShoppingBag)
    ->footer([
        Action::make('createOrder')
            ->label('Create order')
            ->icon(Heroicon::Plus),
    ]),
```

For a table, use the table's own empty-state API instead — see `references/table.md`, variant *distinguish empty from filtered-empty*.

### Variant: contextual callout

**When**: a warning, policy, or next-step explanation applies to a nearby group or workflow *before* the user acts.

**Not when**: the message is only a transient outcome, repeats field guidance, or is broad enough to belong in permanent documentation.

**Source**: [callout/simple](https://filamentphp.com/docs/images/5.x/light/components/callout/simple.jpg)

Place the callout beside the group it governs, not at the top of the page:

```php
use Filament\Schemas\Components\Callout;

Callout::make('Refunds close after 90 days')
    ->description('Orders older than 90 days must be refunded through the finance team.')
    ->warning(),
```

### Variant: full-page workflow

**When**: the work has multiple substantial stages, needs durable navigation or recovery, or requires more reference than an overlay can keep understandable.

**Not when**: a short contextual decision would gain navigation and make the user lose the initiating record.

**Source**: [resources/editing](https://filamentphp.com/docs/images/5.x/light/panels/resources/editing.jpg)

Stop composing an overlay and route to a page. The action becomes navigation, and the work lives in a Resource page:

```php
Action::make('startReturn')
    ->label('Start return')
    ->icon(Heroicon::ArrowUturnLeft)
    ->url(fn (Order $record): string => OrderResource::getUrl('return', ['record' => $record])),
```

`laravel-filament-v5`, `references/resources.md`, owns the page class, its registration, and `getUrl()`.
