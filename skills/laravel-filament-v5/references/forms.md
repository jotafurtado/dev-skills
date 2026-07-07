# Forms — editing (`Filament\Forms\Components\*`)

Used inside `public static function form(Schema $schema): Schema`. Top-level is `$schema->components([...])`.

| Component | For | Minimal signature | 5.x doc |
|---|---|---|---|
| `TextInput` | Text, email, number, password | `TextInput::make('email')->email()->required()` | [text-input](https://filamentphp.com/docs/5.x/forms/text-input.md) |
| `Textarea` | Plain long text | `Textarea::make('notes')->rows(4)` | [textarea](https://filamentphp.com/docs/5.x/forms/textarea.md) |
| `Select` | Options, relationships | `Select::make('author_id')->relationship('author', 'name')->searchable()->preload()` | [select](https://filamentphp.com/docs/5.x/forms/select.md) |
| `Checkbox` / `Toggle` | Boolean | `Toggle::make('is_active')` | [toggle](https://filamentphp.com/docs/5.x/forms/toggle.md) |
| `ToggleButtons` | Few visible options (status!) | `ToggleButtons::make('status')->options(OrderStatus::class)->inline()` | [toggle-buttons](https://filamentphp.com/docs/5.x/forms/toggle-buttons.md) |
| `Radio` / `CheckboxList` | Options in a list | `CheckboxList::make('tags')->options([...])` | [checkbox-list](https://filamentphp.com/docs/5.x/forms/checkbox-list.md) |
| `DateTimePicker` | Date/time (also `DatePicker`, `TimePicker`) | `DateTimePicker::make('published_at')` | [date-time-picker](https://filamentphp.com/docs/5.x/forms/date-time-picker.md) |
| `FileUpload` | Files, images | `FileUpload::make('attachment')->image()` — default is **private**; `->visibility('public')` only if needed | [file-upload](https://filamentphp.com/docs/5.x/forms/file-upload.md) |
| `RichEditor` / `MarkdownEditor` | Rich text | `RichEditor::make('body')` | [rich-editor](https://filamentphp.com/docs/5.x/forms/rich-editor.md) |
| `Repeater` | Repeated rows / relations | `Repeater::make('items')->schema([...])` — doesn't take full width by default | [repeater](https://filamentphp.com/docs/5.x/forms/repeater.md) |
| `Builder` | Flexible content blocks | `Builder::make('content')->blocks([...])` | [builder](https://filamentphp.com/docs/5.x/forms/builder.md) |
| `TagsInput` | List of strings | `TagsInput::make('tags')` | [tags-input](https://filamentphp.com/docs/5.x/forms/tags-input.md) |
| `KeyValue` | Edit associative array | `KeyValue::make('meta')` | [key-value](https://filamentphp.com/docs/5.x/forms/key-value.md) |
| `ColorPicker` | Pick a color | `ColorPicker::make('color')` | [color-picker](https://filamentphp.com/docs/5.x/forms/color-picker.md) |
| `CodeEditor` | Edit code/JSON | `CodeEditor::make('config')->language(Language::Json)` — uses `Filament\Forms\Components\CodeEditor\Enums\Language`, **not** the `Phiki\Grammar\Grammar` enum that `CodeEntry` (infolists) uses; the two components don't share an API despite both editing/showing code | [code-editor](https://filamentphp.com/docs/5.x/forms/code-editor.md) |
| `Hidden` | Hidden value | `Hidden::make('user_id')` | [hidden](https://filamentphp.com/docs/5.x/forms/hidden.md) |

## Recurring form patterns

- **Relationship selects**: always `->relationship('author', 'name')->searchable()->preload()`. To let the user create a related record inline, add `->createOptionForm([...])`.
- **Reactive fields**: `->live()` (or `->live(onBlur: true)` for text inputs) plus injected `Get`/`Set` from `Filament\Schemas\Components\Utilities\*` — never `Filament\Forms\Get` (v3/v4).
- **Conditional per operation**: inject `string $operation` or compare `Operation::Create` / `Operation::Edit` — never string comparisons.
- **Slug fields**: `->live(onBlur: true)` on the source + `->disabled()->dehydrated()` on the slug when it must persist but not be edited.
- **Saving fields to a related model**: layout components (`Section`, `Grid`, `Fieldset`) accept `->relationship('metadata')` for `BelongsTo`/`HasOne`/`MorphOne` — the wrapped fields load and save on the related record automatically. Never write manual mutators for this.
- **Enums**: `->options(OrderStatus::class)` works on `Select`, `ToggleButtons`, `Radio`, `CheckboxList` when the enum implements `HasLabel`.
