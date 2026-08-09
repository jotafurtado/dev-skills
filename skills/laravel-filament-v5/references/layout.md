# Layout & static content — schemas (`Filament\Schemas\Components\*`)

Apply to both forms AND infolists (same Schema system in v5).

For *which* page structure to build — grouping, columns, sections, tabs, wizards, density — use `laravel-filament-v5-ui-ux`, `references/form-layout.md`. This file is the API inventory.

Table signatures are focused fragments. Code blocks include the imports needed by the shown composition; add surrounding schema/class context.

## Structural components

| Component | Minimal signature | 5.x doc |
|---|---|---|
| `Section` | `Section::make('Details')->description('...')->columns(2)->collapsible()->schema([...])` | [sections](https://filamentphp.com/docs/5.x/schemas/sections.md) |
| `Grid` | `Grid::make(3)->schema([...])` | [layouts](https://filamentphp.com/docs/5.x/schemas/layouts.md) |
| `Tabs` | `Tabs::make()->tabs([Tabs\Tab::make('General')->schema([...])])` | [tabs](https://filamentphp.com/docs/5.x/schemas/tabs.md) |
| `Wizard` | `Wizard::make([Wizard\Step::make('Order')->schema([...])])` | [wizards](https://filamentphp.com/docs/5.x/schemas/wizards.md) |
| `Fieldset` | `Fieldset::make('Label')->columns(2)->schema([...])` — bordered, labeled group; `->contained(false)` drops the border | [layouts](https://filamentphp.com/docs/5.x/schemas/layouts.md) |
| `Flex` | `Flex::make([Section::make([...]), Section::make([...])->grow(false)])->from('md')` — flexbox widths, not the grid system; `from()` sets the breakpoint where it stops stacking | [layouts](https://filamentphp.com/docs/5.x/schemas/layouts.md) |
| `Group` | `Group::make([...])` — plain wrapper, no visual styling; mainly useful with `->relationship(...)` to entangle a set of fields with a single related record (see `references/forms.md`) | [source](https://github.com/filamentphp/filament/blob/5.x/packages/schemas/src/Components/Group.php) |

Important: `Grid`, `Section`, and `Repeater` **don't take full width by default** — use `->columnSpan(...)` or `->columnSpanFull()`.

## Prime components — static content WITHOUT custom Blade

Use these BEFORE reaching for a custom Blade view. ([primes doc](https://filamentphp.com/docs/5.x/schemas/primes.md))

| Component | Minimal signature | Notes |
|---|---|---|
| `Text` | `Text::make('Explanatory note')->color('neutral')` | Default color is dim `gray`; `->badge()` + `->color('warning')` renders as a badge; accepts `HtmlString` / inline Markdown via `str()->inlineMarkdown()->toHtmlString()` |
| `Icon` | `Icon::make(Heroicon::Star)->color('warning')->tooltip('...')` | |
| `Image` | `Image::make(url: asset('images/logo.svg'), alt: 'Logo')->imageSize(...)` | |
| `UnorderedList` | `UnorderedList::make(['Tables', 'Schemas', 'Actions'])` — items can be plain strings or `Text` components | Never a hand-written `<ul>` |

## Callout — notices, alerts, tips

([callouts doc](https://filamentphp.com/docs/5.x/schemas/callouts.md)) Use `Callout` before hand-building an alert box with a colored `<div>`:

```php
use Filament\Actions\Action;
use Filament\Schemas\Components\Callout;

Callout::make('Session expiring soon')
    ->description('Save your work to avoid losing changes.')
    ->warning()                    // or ->info() / ->success() / ->danger()
    ->actions([Action::make('save')->button()])
```

- Status variants set icon + colors automatically; `->color(null)` keeps the icon but drops the background.
- `->icon(Heroicon::OutlinedLightBulb)` for a custom icon.

## EmptyState — "nothing here yet" inside a schema

([empty-states doc](https://filamentphp.com/docs/5.x/schemas/empty-states.md)) For tables, use the table's own `->emptyStateHeading()` API instead (see `references/tables.md`).

```php
use Filament\Actions\Action;
use Filament\Schemas\Components\EmptyState;
use Filament\Support\Icons\Heroicon;

EmptyState::make('No users yet')
    ->description('Get started by creating a new user.')
    ->icon(Heroicon::OutlinedUser)
    ->footer([Action::make('createUser')->icon(Heroicon::Plus)])
```

`->contained(false)` removes the card background/border when it should blend into the page.
