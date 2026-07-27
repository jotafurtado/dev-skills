# Ordinary field composition

Use this reference after querying the catalog with `--goal compose-ordinary-fields`. It selects a visual treatment for ordinary Filament 5 form fields; use `laravel-filament-v5` to verify exact APIs and installed-version compatibility.

| Decision | Prefer | Avoid | Evidence |
|---|---|---|---|
| Ordinary wrapper | A label, input, guidance, and feedback need the familiar vertical reading order | A dense, familiar form has short labels and values that remain scannable inline | [form fields](https://filamentphp.com/docs/5.x/forms/overview.md) |
| Inline label | A dense, familiar form has short stable labels and vertical space is constrained | Long labels, instructions, validation, or values need their own line to remain scannable | [inline labels](https://filamentphp.com/docs/5.x/forms/overview.md) |
| Field-level guidance | A short instruction, example, unit, or consequence directly qualifies one field | The text repeats the label or explains a group-wide workflow, policy, or risk | [extra field content](https://filamentphp.com/docs/5.x/forms/overview.md) |
| Placeholder example | An empty input benefits from a short, realistic example of its expected value | The text would replace the label, required state, instructions, or validation feedback | [placeholders](https://filamentphp.com/docs/5.x/forms/overview.md) |
| Auxiliary field content | An immediate field-specific action or component helps complete, verify, or understand that field | The action or information applies to multiple fields or the workflow and belongs in contextual guidance instead | [extra field content](https://filamentphp.com/docs/5.x/forms/overview.md) |
| Contextual callout | A warning, policy, next step, or other context affects a group or workflow | A short field-specific instruction would be clearer beside that field | [callouts](https://filamentphp.com/docs/5.x/schemas/callouts.md) |
| Disabled and validation states | The unavailable state or correction path is explicit and recoverable | The reason is hidden, correction is blocked, or color is the only state cue | [disabled fields](https://filamentphp.com/docs/5.x/forms/overview.md), [validation](https://filamentphp.com/docs/5.x/forms/validation.md) |
| Fused fields | Several values are interpreted as one compact concept | Controls are independently understood, need separate guidance or errors, or become unreadable on narrow screens | [fused fields](https://filamentphp.com/docs/5.x/forms/overview.md) |
| Adjoined affix | A prefix or suffix is part of the value's meaning, such as a URL scheme, currency, or unit | The content is optional guidance, an unrelated action, or broader context | [affixes](https://filamentphp.com/docs/5.x/forms/overview.md) |

## Geometry and guidance

Keep a visible, specific label for each field. Do not use helper text to restate that label. A placeholder is an example of expected input, not a substitute for a label, instruction, required marker, or error message.

Put short related fields in one row only when each label, value, helper text, and error remains easy to scan. Give long free-form values, high-importance values, and fields likely to show validation feedback a wider or full span. Start with a one-column layout and introduce spans only at breakpoints where the row remains readable. Preserve logical reading and keyboard order regardless of the visual arrangement.

Use inline labels only for familiar, repetitive fields with short stable labels. Do not apply them as general decoration or use them where labels, helper text, placeholders, validation feedback, or values need independent vertical space. Return to the ordinary wrapper before the inline arrangement becomes cramped.

Use a fused group only when values are interpreted together. Add a group label when it clarifies the shared concept. Do not fuse independently meaningful fields merely to reduce spacing, and let a fused group stack or simplify before its parts, labels, messages, or targets become crowded.

Use an adjoined affix when it belongs to the value itself. Keep it visually and semantically distinct from auxiliary actions or optional explanations.

## States and accessible feedback

Retain a label even when it is visually hidden: use the accessible hidden-label treatment rather than an empty label. Required state must be conveyed programmatically and visibly. Validation feedback must identify the affected field and remain perceivable without color alone. Preserve a clear focus indicator and do not use disabled state without explaining the condition or offering an appropriate recovery path where users need one.

Field-level guidance belongs near the field and answers a concrete question about entry, format, consequence, or immediate next action. Keep it concise and do not duplicate the label. Use a contextual callout instead when the information applies to several fields or to the workflow as a whole.

Use a placeholder only as a short example of an empty value. It disappears during entry, so it cannot carry the field's only label, required state, instruction, or validation feedback. Add an auxiliary field action or component only when it serves that field's immediate task; use a contextual callout when it serves the wider workflow.

## Decision trace

For a material field redesign, state the candidate treatments, inspected screenshots, selected geometry, responsive treatment, and accessibility consequences:

```text
Surface: vendor onboarding form fields
Goal: compose ordinary fields with actionable guidance
Candidates: ordinary wrapper, inline label, fused fields, contextual callout
Evidence: forms/fields/inline-label; forms/fields/fused-label; forms/fields/below-content/text; forms/validation
Selected: ordinary wrappers with a shared row for short identifiers, full-width legal explanation, and a labelled fused location group
Responsive treatment: stack the shared row and fused group before labels, errors, or targets crowd
Accessibility: visible labels and required markers; field-specific feedback; no state conveyed by color alone
```
