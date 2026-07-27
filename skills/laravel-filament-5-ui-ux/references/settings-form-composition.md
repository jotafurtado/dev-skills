# Page-level schema and form composition

Use this reference after querying the catalog for a Filament 5 schema or page-level form. It turns reviewed visual patterns into a selection decision; use `laravel-filament-v5` to verify exact API signatures against the installed project.

## Decide the structure

| Pattern | Prefer when | Avoid when | Evidence |
|---|---|---|---|
| Flat content | One short, self-explanatory group needs no added hierarchy | A group needs a name, description, semantic boundary, or deliberate spans | [layouts](https://filamentphp.com/docs/5.x/schemas/layouts.md) |
| Responsive columns | Related short fields share a row; long or high-importance fields get a deliberate wider span | A narrow viewport or equal widths would mislead | [forms overview](https://filamentphp.com/docs/5.x/forms/overview.md), [layouts](https://filamentphp.com/docs/5.x/schemas/layouts.md) |
| Sections | Two to four named groups are scanned top to bottom; descriptions explain the grouping | The container adds no hierarchy, or several large groups are usually visited one at a time | [sections](https://filamentphp.com/docs/5.x/schemas/sections.md) |
| Aside sections | A heading and explanatory description deserve their own scan lane on a wide panel | The description is too short, or narrow space would crowd controls | [aside section](https://filamentphp.com/docs/5.x/schemas/sections.md) |
| Fieldsets | A small, tightly related semantic subgroup needs an explicit shared label | A border is merely decorative, or the group needs a richer hierarchy | [fieldsets](https://filamentphp.com/docs/5.x/schemas/layouts.md) |
| Horizontal tabs | A small number of short, parallel labels require frequent switching | Labels overflow, content must remain visible together, or a sequence is required | [tabs](https://filamentphp.com/docs/5.x/schemas/tabs.md) |
| Vertical tabs | Several stable groups have enough horizontal room and a persistent navigation rail improves scanning | The viewport is too narrow for the rail or the input is sequential | [vertical tabs](https://filamentphp.com/docs/5.x/schemas/tabs.md) |
| Wizard | Each step has a required order or dependency | Users can complete the groups in any order | [wizard](https://filamentphp.com/docs/5.x/schemas/wizards.md) |
| Dense layout | Repetitive, low-risk content remains clearly distinguishable with reduced spacing | Reduced gaps would blur labels, errors, instructions, or touch targets | [dense and no-gap layouts](https://filamentphp.com/docs/5.x/schemas/layouts.md) |

## Use the visual evidence

Inspect `forms/overview` for a contained two-column settings form. It shows related short controls sharing space while longer or grouped controls use the available width deliberately.

Inspect `schemas/layout/grid/column-span` when field widths should express different expected value lengths or importance.

Inspect `schemas/layout/tabs/vertical` when stable settings groups benefit from a persistent left navigation rail and the content pane can still contain responsive columns.

Inspect `schemas/layout/section/aside` when explanatory context needs a separate desktop scan lane, and `schemas/layout/section/compact`, `schemas/layout/dense`, and `schemas/layout/no-gap` only when density remains legible.

Use contained and uncontained variants as composition decisions: choose a contained fieldset or tabs when a boundary clarifies the group; remove that container only when the surrounding hierarchy already supplies it.

## Emit the decision trace

For a material settings-form composition, state:

```text
Filament UI decision
Surface: settings form
Goal: organize stable parallel groups and use width deliberately
Candidates: sections, horizontal tabs, vertical tabs
Evidence: schemas/layout/tabs/vertical; forms/overview
Selected: vertical tabs with responsive columns inside each tab
Responsive treatment: collapse fields to one column before the navigation or inputs become unreadable
```

Replace the selected pattern and evidence with the actual decision. If no official candidate fits, name the candidates checked and the concrete gap before using custom UI.
