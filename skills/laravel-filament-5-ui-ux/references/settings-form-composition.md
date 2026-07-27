# Settings-form composition

Use this reference after querying the catalog for a Filament 5 settings form. It turns the reviewed visual patterns into a selection decision; use `laravel-filament-v5` to verify exact API signatures against the installed project.

## Decide the structure

| Pattern | Prefer when | Avoid when | Evidence |
|---|---|---|---|
| Responsive columns | Related short fields share a row and longer content needs a deliberate span | A narrow viewport or unequal importance makes equal columns misleading | [forms overview](https://filamentphp.com/docs/5.x/forms/overview.md), [layouts](https://filamentphp.com/docs/5.x/schemas/layouts.md) |
| Sections | Two to four named groups are scanned top to bottom; descriptions explain the grouping | The container adds no hierarchy, or several large groups are usually visited one at a time | [section](https://filamentphp.com/docs/5.x/schemas/layouts.md) |
| Horizontal tabs | A small number of short, parallel labels require frequent switching | Labels overflow, content must remain visible together, or a sequence is required | [tabs](https://filamentphp.com/docs/5.x/schemas/tabs.md) |
| Vertical tabs | Several stable groups have enough horizontal room and a persistent navigation rail improves scanning | The viewport is too narrow for the rail or the input is sequential | [vertical tabs](https://filamentphp.com/docs/5.x/schemas/tabs.md) |
| Wizard | Each step has a required order or dependency | Users can complete the groups in any order | [wizard](https://filamentphp.com/docs/5.x/schemas/wizards.md) |

## Use the visual evidence

Inspect `forms/overview` for a contained two-column settings form. It shows related short controls sharing space while longer or grouped controls use the available width deliberately.

Inspect `schemas/layout/grid/column-span` when field widths should express different expected value lengths or importance.

Inspect `schemas/layout/tabs/vertical` when stable settings groups benefit from a persistent left navigation rail and the content pane can still contain responsive columns.

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
