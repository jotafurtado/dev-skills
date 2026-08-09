# Complex input compositions

Ready-to-adapt compositions for collection-oriented and content-heavy Filament 5 inputs. Reach for this when a single control carries a collection, a file, a relationship, or formatted content.

Examples use a `Customer` / `Order` domain consistently across this library.

`laravel-filament-v5` owns field API signatures, validation rules, authorization, and tests. This file owns how the components are arranged.

| Pattern | Use it for |
|---|---|
| [Collection items](#collection-items) | Repeatable structured items and related records |
| [Media uploads](#media-uploads) | Uploaded images and files |
| [Relationship controls](#relationship-controls) | Selecting and creating related records |
| [Rich content editor](#rich-content-editor) | Long-form or formatted content |

---

## Collection items

**When**: each item contains related fields that need a native hierarchy, and people need to add, remove, duplicate, or reorder items that stay scannable through labels or block names.

**Not when**: the user is entering one scalar value, a table would hide essential help or per-item errors, or custom cards are proposed only to simulate native repeater or builder hierarchy.

**Alternatives**: responsive-columns, sections, rich-content-editor.

**Source**: [forms/repeater](https://filamentphp.com/docs/5.x/forms/repeater.md) · [forms/fields/repeater/simple](https://filamentphp.com/docs/images/5.x/light/forms/fields/repeater/simple.jpg)

```php
use Filament\Forms\Components\Repeater;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            Repeater::make('items')
                ->relationship()
                ->schema([
                    TextInput::make('name')
                        ->required()
                        ->live(onBlur: true),
                    TextInput::make('quantity')
                        ->numeric()
                        ->required(),
                    TextInput::make('notes'),
                ])
                ->columns(2)
                ->itemLabel(fn (array $state): ?string => $state['name'] ?? null)
                ->cloneable()
                ->orderColumn('sort')
                ->grid(2),
        ]);
}
```

**Responsive**: stack item-internal fields before labels, errors, or actions crowd, and prefer button-based reordering when drag handles are hard to use.

**Accessibility**: give each item a distinguishable visible label or number, keep add, remove, duplicate, collapse, and reorder actions named and keyboard reachable, and keep errors associated with the affected item and field.

### Variant: Collapsible items

**When**: many completed items need compact scanning while their labels still identify them.

**Not when**: the current task requires comparing or correcting several item fields together.

**Source**: [forms/fields/repeater/collapsed](https://filamentphp.com/docs/images/5.x/light/forms/fields/repeater/collapsed.jpg)

Add `collapsible()` and `collapsed()` so completed order lines start compact:

```php
Repeater::make('items')
    ->relationship()
    ->schema([
        TextInput::make('name')
            ->required()
            ->live(onBlur: true),
        TextInput::make('quantity')
            ->numeric()
            ->required(),
        TextInput::make('notes'),
    ])
    ->columns(2)
    ->itemLabel(fn (array $state): ?string => $state['name'] ?? null)
    ->cloneable()
    ->orderColumn('sort')
    ->collapsible()
    ->collapsed(),
```

### Variant: Table layout

**When**: items are short, uniform rows with stable, scannable columns.

**Not when**: an item needs rich guidance, previews, nested fields, or errors that a row would compress.

**Source**: [forms/fields/repeater/table-compact](https://filamentphp.com/docs/images/5.x/light/forms/fields/repeater/table-compact.jpg)

Replace the card layout with `table()` and `compact()` for order line rows:

```php
use Filament\Forms\Components\Repeater\TableColumn;

Repeater::make('items')
    ->relationship()
    ->table([
        TableColumn::make('Name'),
        TableColumn::make('Quantity'),
        TableColumn::make('Notes'),
    ])
    ->compact()
    ->schema([
        TextInput::make('name')
            ->required(),
        TextInput::make('quantity')
            ->numeric()
            ->required(),
        TextInput::make('notes'),
    ])
    ->cloneable()
    ->orderColumn('sort'),
```

### Variant: Reorder buttons

**When**: the order matters and explicit move controls are more discoverable or accessible than dragging.

**Not when**: the collection is not ordered.

**Source**: [forms/fields/repeater/reorderable-with-buttons](https://filamentphp.com/docs/images/5.x/light/forms/fields/repeater/reorderable-with-buttons.jpg)

Add `reorderableWithButtons()` so line order can change without drag handles:

```php
Repeater::make('items')
    ->relationship()
    ->schema([
        TextInput::make('name')
            ->required()
            ->live(onBlur: true),
        TextInput::make('quantity')
            ->numeric()
            ->required(),
        TextInput::make('notes'),
    ])
    ->columns(2)
    ->itemLabel(fn (array $state): ?string => $state['name'] ?? null)
    ->cloneable()
    ->orderColumn('sort')
    ->reorderableWithButtons(),
```

### Variant: Add action placement

**When**: the collection needs an explicit add affordance placed near the items it creates.

**Not when**: a distant or generic page action would obscure which collection receives the new item.

**Source**: [forms/fields/repeater/add-action-alignment](https://filamentphp.com/docs/images/5.x/light/forms/fields/repeater/add-action-alignment.jpg)

Label the add action and align it to the start of the order lines:

```php
use Filament\Support\Enums\Alignment;

Repeater::make('items')
    ->relationship()
    ->schema([
        TextInput::make('name')
            ->required()
            ->live(onBlur: true),
        TextInput::make('quantity')
            ->numeric()
            ->required(),
        TextInput::make('notes'),
    ])
    ->columns(2)
    ->itemLabel(fn (array $state): ?string => $state['name'] ?? null)
    ->cloneable()
    ->orderColumn('sort')
    ->addActionLabel('Add line item')
    ->addActionAlignment(Alignment::Start),
```

### Variant: Builder blocks

**When**: the collection contains heterogeneous content blocks with meaningful block types.

**Not when**: all items share one stable field structure.

**Source**: [forms/fields/builder/simple](https://filamentphp.com/docs/images/5.x/light/forms/fields/builder/simple.jpg)

Replace the single-schema `Repeater` with a `Builder` when order content needs distinct block types:

```php
use Filament\Forms\Components\Builder;
use Filament\Forms\Components\Builder\Block;
use Filament\Forms\Components\FileUpload;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\Textarea;
use Filament\Forms\Components\TextInput;

Builder::make('content')
    ->blocks([
        Block::make('heading')
            ->schema([
                TextInput::make('content')
                    ->label('Heading')
                    ->required(),
                Select::make('level')
                    ->options([
                        'h1' => 'Heading 1',
                        'h2' => 'Heading 2',
                        'h3' => 'Heading 3',
                        'h4' => 'Heading 4',
                        'h5' => 'Heading 5',
                        'h6' => 'Heading 6',
                    ])
                    ->required(),
            ])
            ->columns(2),
        Block::make('paragraph')
            ->schema([
                Textarea::make('content')
                    ->label('Paragraph')
                    ->required(),
            ]),
        Block::make('image')
            ->schema([
                FileUpload::make('url')
                    ->label('Image')
                    ->image()
                    ->required(),
                TextInput::make('alt')
                    ->label('Alt text')
                    ->required(),
            ]),
    ]),
```

---

## Media uploads

**When**: the user must add, preview, inspect, or manage one or more files, and file previews or image-editing controls need a wide enough surface.

**Not when**: a narrow scalar-field column would compress previews or upload affordances, or custom upload cards recreate the native FileUpload interaction.

**Alternatives**: collection-items, rich-content-editor.

**Source**: [forms/file-upload](https://filamentphp.com/docs/5.x/forms/file-upload.md) · [forms/fields/file-upload/simple](https://filamentphp.com/docs/images/5.x/light/forms/fields/file-upload/simple.jpg)

```php
use Filament\Forms\Components\FileUpload;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            FileUpload::make('attachment')
                ->directory('order-attachments'),
        ]);
}
```

**Responsive**: let preview grids reduce columns while preserving preview size, filenames, and remove controls, and give image editing a full workflow surface rather than embedding it in a cramped group.

**Accessibility**: keep browse, remove, open, download, and editing controls named and keyboard reachable, and provide meaningful file names and text alternatives where media meaning is not otherwise available.

### Variant: Preview grid

**When**: several visual files benefit from side-by-side recognition.

**Not when**: preview tiles become too small to identify or operate.

**Source**: [forms/fields/file-upload/multiple-grid](https://filamentphp.com/docs/images/5.x/light/forms/fields/file-upload/multiple-grid.jpg)

Replace the single attachment field with a multiple, reorderable upload for the order gallery:

```php
FileUpload::make('attachments')
    ->multiple()
    ->reorderable()
    ->appendFiles()
    ->directory('order-attachments'),
```

### Variant: Image editor

**When**: the workflow requires a crop or other image adjustment before submission.

**Not when**: the upload is a simple attachment with no editing need.

**Source**: [forms/fields/file-upload/image-editor](https://filamentphp.com/docs/images/5.x/light/forms/fields/file-upload/image-editor.jpg)

Replace the attachment field with an image upload that opens the built-in editor:

```php
FileUpload::make('image')
    ->image()
    ->imageEditor()
    ->directory('order-images'),
```

---

---

## Relationship controls

**When**: a field selects, creates, edits, or manages related records, and relationship labels need search or enough width to remain distinguishable.

**Not when**: a relation needs rich per-item fields that belong in a repeater or relation workflow, or a custom card is used where native select or relationship controls represent the task.

**Alternatives**: collection-items, sections.

**Source**: [forms/select](https://filamentphp.com/docs/5.x/forms/select.md) · [forms/fields/select/searchable](https://filamentphp.com/docs/images/5.x/light/forms/fields/select/searchable.jpg)

```php
use Filament\Forms\Components\Select;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            Select::make('customer_id')
                ->relationship(name: 'customer', titleAttribute: 'name'),
            Select::make('statuses')
                ->multiple()
                ->relationship(titleAttribute: 'name'),
        ]);
}
```

**Responsive**: preserve readable selected labels and reachable create or edit actions on narrow screens, and move a relationship-heavy workflow to its own section, tab, or larger surface when options, details, and actions cannot remain scannable inline.

**Accessibility**: name the relationship and any create or edit action clearly, do not rely on colour or truncation alone to distinguish selected related records, and keep result, selected-value, and validation feedback available to keyboard and assistive-technology users.

### Variant: Searchable selection

**When**: the relationship has enough options that scanning a static list is inefficient.

**Not when**: a short stable option set is already easy to scan.

**Source**: [forms/fields/select/searchable](https://filamentphp.com/docs/images/5.x/light/forms/fields/select/searchable.jpg)

Replace the customer select with a searchable, preloaded relationship and custom option labels:

```php
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

Select::make('customer_id')
    ->relationship(
        name: 'customer',
        modifyQueryUsing: fn (Builder $query) => $query->orderBy('name'),
    )
    ->getOptionLabelFromRecordUsing(fn (Model $record) => "{$record->name} · {$record->email}")
    ->searchable(['name', 'email'])
    ->preload(),
```

### Variant: Create or edit related

**When**: the user must resolve a missing or incorrect related record without abandoning the current task.

**Not when**: the related-record workflow is too large for an inline action.

**Source**: [forms/fields/select/create-option-modal](https://filamentphp.com/docs/images/5.x/light/forms/fields/select/create-option-modal.jpg)

Add create and edit option modals on the customer relationship select:

```php
use Filament\Forms\Components\TextInput;

Select::make('customer_id')
    ->relationship(name: 'customer', titleAttribute: 'name')
    ->createOptionForm([
        TextInput::make('name')
            ->required(),
        TextInput::make('email')
            ->required()
            ->email(),
    ])
    ->editOptionForm([
        TextInput::make('name')
            ->required(),
        TextInput::make('email')
            ->required()
            ->email(),
    ]),
```

---

## Rich content editor

**When**: a full-width editor preserves a readable writing area, the control has a toolbar or contextual panels, and editing needs more vertical space than a short scalar field.

**Not when**: the task needs only a short plain-text value, a narrow column would compress the writing area or toolbar, or custom markup is proposed to recreate an official editor.

**Alternatives**: responsive-columns, collection-items, sections.

**Source**: [forms/rich-editor](https://filamentphp.com/docs/5.x/forms/rich-editor.md) · [forms/fields/rich-editor/simple](https://filamentphp.com/docs/images/5.x/light/forms/fields/rich-editor/simple.jpg)

```php
use Filament\Forms\Components\RichEditor;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            RichEditor::make('notes'),
        ]);
}
```

**Responsive**: give the editor a full or wide span before reducing toolbar or content readability, and keep formatting controls reachable.

**Accessibility**: retain the editor label, expose formatting actions with discernible names, keep focus order coherent between the toolbar, editor, and any contextual panels, and make validation or insertion failures perceivable without color alone.

### Variant: Custom toolbar

**When**: the workflow needs a constrained, task-specific formatting set.

**Not when**: removing controls would block required authoring actions.

**Source**: [forms/fields/rich-editor/custom-toolbar](https://filamentphp.com/docs/images/5.x/light/forms/fields/rich-editor/custom-toolbar.jpg)

Constrain the rich editor toolbar to the formatting the order notes workflow actually needs:

```php
RichEditor::make('notes')
    ->toolbarButtons([
        ['bold', 'italic', 'underline', 'strike', 'link'],
        ['h2', 'h3'],
        ['blockquote', 'bulletList', 'orderedList'],
        ['undo', 'redo'],
    ]),
```

When the authoring surface should stay Markdown instead, replace the field with a constrained markdown toolbar:

```php
use Filament\Forms\Components\MarkdownEditor;

MarkdownEditor::make('notes')
    ->toolbarButtons([
        ['bold', 'italic', 'strike', 'link'],
        ['heading'],
        ['blockquote', 'codeBlock', 'bulletList', 'orderedList'],
        ['undo', 'redo'],
    ]),
```

### Variant: Contextual panels

**When**: blocks, mentions, or merge tags are part of authoring and the main writing area stays usable.

**Not when**: a panel would obscure the task or appear for irrelevant content.

**Source**: [forms/fields/rich-editor/custom-blocks](https://filamentphp.com/docs/images/5.x/light/forms/fields/rich-editor/custom-blocks.jpg)

Register merge tags for customer and order placeholders and open that panel by default:

```php
RichEditor::make('notes')
    ->mergeTags([
        'name' => 'Customer name',
        'email' => 'Customer email',
        'status' => 'Order status',
    ])
    ->activePanel('mergeTags'),
```
