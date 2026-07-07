# Infolists — read-only display (`Filament\Infolists\Components\*`)

Used inside `public function infolist(Schema $schema): Schema` in View pages. Top-level is `$schema->components([...])`.

This is memory, not documentation: minimal signature + link. If in doubt about a specific method, fetch the `.md` doc page — don't guess.

| Component | For | Minimal signature | 5.x doc |
|---|---|---|---|
| `TextEntry` | Text, date, money, badge, lists | `TextEntry::make('title')->badge()` · `->dateTime()` · `->money('USD')` · `->markdown()` · `->listWithLineBreaks()` | [text-entry](https://filamentphp.com/docs/5.x/infolists/text-entry.md) |
| `CodeEntry`¹ | Code, JSON, payloads, logs | `CodeEntry::make('payload')->grammar(Grammar::Json)->copyable()` | [code-entry](https://filamentphp.com/docs/5.x/infolists/code-entry.md) |
| `KeyValueEntry` | Associative array / metadata | `KeyValueEntry::make('meta')` | [key-value-entry](https://filamentphp.com/docs/5.x/infolists/key-value-entry.md) |
| `ColorEntry` | Color swatch | `ColorEntry::make('color')` | [color-entry](https://filamentphp.com/docs/5.x/infolists/color-entry.md) |
| `ImageEntry` | Images, avatars | `ImageEntry::make('avatar')->circular()` · `->stacked()` | [image-entry](https://filamentphp.com/docs/5.x/infolists/image-entry.md) |
| `IconEntry` | Icon, visual boolean | `IconEntry::make('is_active')->boolean()` — omit `->boolean()` if the attribute is already cast `bool` on the model, Filament detects it automatically | [icon-entry](https://filamentphp.com/docs/5.x/infolists/icon-entry.md) |
| `RepeatableEntry` | Repeated collections/relations | `RepeatableEntry::make('comments')->schema([...])` | [repeatable-entry](https://filamentphp.com/docs/5.x/infolists/repeatable-entry.md) |

¹ `CodeEntry` requires a separate package: `composer require phiki/phiki` — Filament doesn't bundle it, so you can pick which Phiki major version to use. If a project errors on `CodeEntry`/`Grammar` with a class-not-found, this is why.

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

`ViewEntry::make('...')->view('...')` exists for genuinely custom visualizations (e.g. an interactive diagram). Using it to render a primitive from the quick map is a gate violation.
