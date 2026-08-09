# Infolists — read-only display (`Filament\Infolists\Components\*`)

Top-level configuration uses `$schema->components([...])`, but the method signature depends on its owner:

In the Resource class, use a static method shared by its View page:

```php
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Schema;

public static function infolist(Schema $schema): Schema
{
    return $schema->components([
        TextEntry::make('name'),
    ]);
}
```

In a custom `ViewRecord` page, use an instance method for the page-specific infolist:

```php
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Schema;

public function infolist(Schema $schema): Schema
{
    return $schema->components([
        TextEntry::make('name'),
    ]);
}
```

Do not make the Resource method non-static or the custom View page method static. See the official [Viewing records](https://filamentphp.com/docs/5.x/resources/viewing-records.md) examples.

The remaining snippets are focused fragments. If in doubt about a method, fetch its `.md` page instead of guessing.

| Component | For | Minimal signature | 5.x doc |
|---|---|---|---|
| `TextEntry` | Text, date, money, badge, lists | `TextEntry::make('title')->badge()` · `->dateTime()` · `->money('USD')` · `->markdown()` · `->listWithLineBreaks()` | [text-entry](https://filamentphp.com/docs/5.x/infolists/text-entry.md) |
| `CodeEntry`¹ | Code, JSON, payloads, logs | After `composer require phiki/phiki`: `CodeEntry::make('payload')->grammar(Grammar::Json)->copyable()` | [code-entry](https://filamentphp.com/docs/5.x/infolists/code-entry.md) |
| `KeyValueEntry` | Associative array / metadata | `KeyValueEntry::make('meta')` | [key-value-entry](https://filamentphp.com/docs/5.x/infolists/key-value-entry.md) |
| `ColorEntry` | Color swatch | `ColorEntry::make('color')` | [color-entry](https://filamentphp.com/docs/5.x/infolists/color-entry.md) |
| `ImageEntry` | Images, avatars | `ImageEntry::make('avatar')->circular()` · `->stacked()` | [image-entry](https://filamentphp.com/docs/5.x/infolists/image-entry.md) |
| `IconEntry` | Icon, visual boolean | `IconEntry::make('is_active')->boolean()` — omit `->boolean()` if the attribute is already cast `bool` on the model, Filament detects it automatically | [icon-entry](https://filamentphp.com/docs/5.x/infolists/icon-entry.md) |
| `RepeatableEntry` | Repeated collections/relations | `RepeatableEntry::make('comments')->schema([...])` | [repeatable-entry](https://filamentphp.com/docs/5.x/infolists/repeatable-entry.md) |

¹ `CodeEntry` requires `composer require phiki/phiki` plus `use Phiki\Grammar\Grammar;`. Filament does not bundle Phiki, allowing the project to choose its major version.

## Frequently useful `TextEntry` modifiers

- `->badge()` — renders as badge; combine with a `HasColor`/`HasIcon`/`HasLabel` enum cast on the model so color/label/icon come for free.
- `->dateTime()` / `->date()` / `->since()` — date formatting; never format dates by hand.
- `->money('USD')` / `->numeric()` — number formatting.
- `->markdown()` / `->html()` — rich content; never pull an external Markdown lib.
- `->copyable()` — built-in copy to clipboard; never write custom JS for this.
- `->placeholder('—')` — what to show when the state is null; prefer this over conditional Blade.
- `->limit(50)` / `->words(10)` — truncation.
- `->inlineLabel()` — label beside the value instead of above; good for dense metadata blocks (see `ui-composition.md`).

## Escape hatch

`ViewEntry::make('...')->view('...')` exists for genuinely custom visualizations (for example, an interactive diagram). Use it only after checking that no documented entry on this surface expresses the requirement; record that gap near the implementation or in the change summary.
