# Complex and collection input composition

Use this reference after querying the catalog for repeaters, builders, editors, uploads, or relationship-heavy controls. Verify exact component APIs and installed-version behavior with `laravel-filament-v5`.

## Select the workflow surface

| Pattern | Prefer when | Keep inline when | Move to a section, tab, or larger workflow when | Evidence |
|---|---|---|---|---|
| Collection items | Repeated items have related fields, a clear item identity, and native add, remove, duplicate, collapse, or reorder actions | The collection is a supporting part of one form task and each item remains short and understandable | Items need rich help, nested content, many actions, or comparison with other groups | [repeater](https://filamentphp.com/docs/5.x/forms/repeater.md), [builder](https://filamentphp.com/docs/5.x/forms/builder.md) |
| Rich content editor | The user writes formatted or long-form content with a toolbar, blocks, mentions, or merge content | The editor is the primary content field and can receive a full or wide span | Editing has its own review, collaboration, publishing, or media-management workflow | [rich editor](https://filamentphp.com/docs/5.x/forms/rich-editor.md), [markdown editor](https://filamentphp.com/docs/5.x/forms/markdown-editor.md) |
| Media uploads | Files or previews are part of the current form task | One simple attachment has a clear label and enough room for its drop zone and status | Multiple assets need selection, metadata, ordering, image editing, or a gallery workflow that no longer scans as one field | [file upload](https://filamentphp.com/docs/5.x/forms/file-upload.md) |
| Relationship controls | A user selects, searches, creates, or corrects related records in service of the current task | The relation is understandable from its label and selected values remain readable | Choosing or managing the related records needs rich record detail, multiple filters, per-record fields, or its own workflow | [select](https://filamentphp.com/docs/5.x/forms/select.md) |

Use native `Repeater` and `Builder` hierarchy instead of custom card markup. A repeater suits a stable item schema; a builder suits heterogeneous blocks whose type is part of the item identity. Give repeated items a meaningful label, number, or block heading so users can scan collapsed or completed items. Keep native add, delete, clone, collapse, and reorder affordances adjacent to the item or collection they change.

Use a table repeater only for short, uniform, row-like items with stable columns. Return to the ordinary contained item layout when help text, errors, previews, nested controls, or per-item actions would be compressed. For ordered collections, use explicit reorder buttons when they are more discoverable or operable than drag handles.

Give editors, image uploads, multiple-file previews, and relationship controls a full or deliberately wide span. Do not place them in a multi-column row intended for short scalar fields. Use an upload grid only while previews, filenames, status, and removal controls remain large enough to identify and operate.

## Responsive and accessible treatment

Start repeated item internals as a readable single column, then add columns only where labels, values, help, errors, and actions remain scannable. On smaller widths, stack item fields before reducing touch-target size or obscuring item actions. Keep add actions near the collection and do not move destructive or reorder actions away from the item they affect.

Ensure each repeated item has a distinguishable name, number, or block type; position alone is not identity. Keep add, delete, clone, collapse, reorder, browse, remove, open, download, create-related, and edit-related actions visibly named or programmatically labelled and keyboard reachable. Associate validation feedback with the affected field and item. Preserve logical focus order through toolbars, editors, upload controls, selection results, and contextual panels. Do not make selected-record state, upload progress, errors, or requiredness depend on color alone.

For relationship-heavy controls, retain readable selected labels and explicit empty, loading, and validation states. Use searchable selection when a static option list is inefficient. Use inline create or edit only for a small, bounded related-record task; move to a larger workflow when its fields or decisions would crowd the current surface.

## Decision trace

For a material complex-input composition, state:

```text
Filament UI decision
Surface: product content form
Goal: compose repeatable content blocks and supporting media
Candidates: collection items, rich content editor, media uploads
Evidence: forms/fields/builder/simple; forms/fields/repeater/table-compact; forms/fields/file-upload/multiple-grid
Selected: native Builder for heterogeneous blocks, wide FileUpload grid for the gallery
Responsive treatment: stack fields inside each block; reduce preview-grid columns before controls crowd
Accessibility: labelled blocks; keyboard-reachable add, remove, and reorder actions; item-specific errors and named uploads
```

If no official candidate fits, record the official candidates considered and the concrete gap before introducing custom Blade, Livewire, CSS, or theme work. Keep that escape hatch as small as possible.
