# UI composition — fluid, scannable pages from official components

The gate in SKILL.md decides *which* component renders each piece of data. This file decides *how the page is organized and how it should look*. A page built only from correct components can still overwhelm the user. The defaults below are the skill's strong starting position, not Filament API contracts: follow them unless a specific domain, workflow, accessibility, responsive, or established-theme requirement justifies a deviation.

When you are unsure what a surface should look like, load `references/screenshots.md` and inspect the official example before composing.

## On this page

- Organizing principle and Filament-aligned defaults
- Page recipes for lists, forms, views, dashboards, navigation, and modals
- Structural containers, hierarchy, width, and feedback
- Final composition review

## The organizing principle

Use this internal usability target: a user should recognize the record and its state in roughly 2 seconds and find secondary detail in roughly 10. Treat the numbers as a review heuristic, not a claim of measured usability; primary information stays visible while secondary information is grouped, collapsed, or tabbed away.

## Filament-aligned defaults

Filament's rendered UI already has a deliberate visual system. Begin with these defaults, then use documented theme configuration or CSS hooks when the product needs a deliberate variation:

- **Calm surface**: preserve the active theme's surface, border, radius, shadow, and spacing rhythm unless the project has a documented reason to change it.
- **Intentional accent**: use the primary color for navigation state, primary actions, links, and focus without letting many accented elements compete at once.
- **Semantic color carries meaning**: success/warning/danger/info fit statuses, callouts, and destructive actions. Communicate state with text and, where useful, an icon so color is not the only signal.
- **Coherent typography**: use the panel font and component hierarchy first. Extend typography through the project's documented theme when the product requires it.
- **Quiet by default, loud once**: default to one filled primary action for the current task. Emphasize multiple actions only when the workflow genuinely has peer outcomes and their hierarchy remains clear.
- Start panel identity with `->colors()`, `->brandLogo()`, and `->font()` in the panel provider. A documented custom theme remains a valid extension point.

## Page recipes

### List page (table)

Default Filament anatomy, top to bottom — deviate when the workflow requires it:

1. **Header**: page heading and optional concise description; place the primary action, often `CreateAction`, where it is easy to find.
2. **Toolbar**: search field on the right; filters and column toggles as icon buttons at the far right (filter icon shows an active-count badge); `Group by` / `Sort by` selects on the left when used.
3. **Rows**: checkbox only when bulk actions exist, then identity, the facts users compare, status, and dates. Keep destructive actions distinct and last. Default to `ActionGroup` for 3+ low-frequency actions; keep a common action outside the group when speed matters.
4. **Footer**: "Showing X to Y of Z results" left, per-page select, page numbers right.

Guidelines observed in the official examples:

- **Default to 5–7 visible desktop columns.** Exceed that range only when users must compare the extra facts simultaneously and the responsive table remains usable; make secondary columns toggleable otherwise.
- Column order = question order: identity → status (badge) → comparison facts → dates last.
- Prefer `IconColumn->boolean()` for compact, familiar boolean states; use explicit text when an icon would be ambiguous to the audience.
- Prefer a `SelectFilter` on an enum over asking users to search for status strings.
- When order matters, make `->defaultSort()` match how users think about recency or priority.
- `->defaultGroup()` with subtle group-header rows replaces a redundant status column when users scan by state.
- Alternative record layouts (`Split`, `Stack`, grid) are for records where a photo/identity block matters more than comparable facts (people, products, cards) — a `Split` holds identity left, contact facts center, collapsible `Panel` for the long tail. Regular columns beat card grids for compare-and-scan work.

### Create / Edit page (form)

- Default to two columns for related short fields on desktop, then adjust through the structural-container decision below.
- **Settings-style pages**: `Section::make(...)->aside()` — heading and description in a left column, fields in a card on the right. This is the official look for configuration screens.
- Required marker, label above field, `->helperText()` below — never restate the label as helper text.
- Long-form fields (`Textarea`, `RichEditor`, `Repeater`, `Builder`) span full width; related short fields (start/end, min/max) share a row.
- `Repeater` items render as cards with a delete icon top-right and a centered "Add" button below — don't rebuild this with custom markup.
- **Wizard** only for genuinely sequential input (checkout, onboarding): numbered chevron steps, one `Next` filled button per step, submit on the last step.

### View page (infolist)

- For records with a clear identity/detail split, consider the official example's two-zone layout: a wider identity `Section`, a narrower key-facts `Section`, then `Tabs` for large secondary surfaces. Use a simpler layout when the record does not have that hierarchy.
- Identity values render larger/bold via `TextEntry->size()`/`->weight()`; labels stay muted. Copyable identifiers (SKU, IDs) use `->copyable()` with a badge-like look.
- Dense fact blocks: `->inlineLabel()` (label left, value right) — the official "Details card" pattern for many short facts.
- Finite workflow statuses default to `->badge()` with a `HasColor`/`HasIcon` enum. Keep plain text when badge emphasis would imply semantics the value doesn't have.

### Dashboard

Default composition, top to bottom:

1. **Stats row** (`StatsOverviewWidget`): default to 3–4 decision-relevant tiles using a clear label, value, and optional trend/sparkline. Color a trend by its meaning, not merely its direction.
2. **Charts** in a 2-column grid; every chart widget carries a heading (and `->description()` when the metric needs context).
3. **Recent-activity table widget** full width at the bottom.

Order widgets by decision value: what the admin acts on daily goes first. At roughly seven independent widgets, require an explicit decision to group them, add dashboard filters, or move a workflow to a second focused page.

### Navigation

- Use icons consistently when they improve recognition; group related Resources with `->navigationGroup()` labels. At roughly seven items in one group, require an explicit decision about naming, clusters, or a different audience structure.
- Numeric nav badges only for actionable counts (pending orders), not vanity totals — implemented as the static `getNavigationBadge()` on the resource (see `references/panels.md`).
- Top navigation (`->topNavigation()` on the panel) suits panels with few items and no groups; the sidebar is the default for real back-offices.

### Modals and confirmation

- **Confirmation modal** (official look): compact, centered icon in a tinted circle (danger red for deletes), bold title, muted one-line question, then equal-width `Cancel` (outline) + `Confirm` (filled, status color). `->requiresConfirmation()` gives you all of it — don't rebuild.
- Default action forms with 1–4 focused fields to a standard modal; use a `->slideOver()` or page when the flow is larger or reference-heavy.
- If a modal accumulates nested decisions or several tabs, reassess whether the workflow deserves a page.

## Choosing the structural container

Decision order — prefer the lightest structure that works:

1. **Nothing** (flat fields) — default for up to roughly six fields with no natural grouping. Do not add a Section that conveys no hierarchy.
2. **`Section`** — default when fields form 2–4 named groups scanned top-to-bottom. Add a heading or description when it clarifies the grouping. Variants include `->aside()` for settings pages, `->compact()`/`->secondary()` for subordinate blocks, and `->collapsible()` for the long tail.
3. **`Tabs`** — default for 3+ groups where the user usually works in one group at a time (General / SEO / Advanced). Keep always-needed or side-by-side comparison content outside non-default tabs. `->badge()` can signal how much lives inside.
4. **`Wizard`** — the input has a natural sequence with dependencies between steps (checkout, onboarding). Don't wizard-ify a form the user might fill in any order; that adds clicks for nothing.

Same order applies to infolists — Sections for scanning, Tabs for large read-only surfaces (details / history / raw payload).

## Visual hierarchy within a page

- **Identity first**: put the name/title, state, owner, or other identifying facts early when they orient the user's task.
- **Default finite workflow statuses to badges** — `TextEntry::make('status')->badge()` with an enum providing color/icon.
- **Collapse the long tail**: audit metadata, internal notes, raw payloads → `Section::make(...)->collapsible()->collapsed()`. Present but silent.
- **Dense metadata blocks**: `->inlineLabel()` on entries (label beside value) reads better than stacked label-over-value for many short facts.
- **Avoid unexplained empty space**: use `->placeholder('—')` for meaningful nullable values and `EmptyState` / `->emptyStateHeading()` for an empty collection.
- **Empty states** (official look): centered icon in a tinted circle, bold heading naming what's missing, muted one-line "get started" description, one primary action. Add the action only when the user can and should resolve the state.

## Columns and width

- Forms and infolists: default Sections to two columns on desktop; use 3+ only for short fields when responsive behavior supports it.
- Long-form fields (`Textarea`, `RichEditor`, `Repeater`, `CodeEntry`) usually need `->columnSpanFull()` or another deliberately wide span.
- Related short fields often benefit from the same row (start/end date, min/max), which `Grid::make(2)` inside a Section can express.
- Remember: `Grid`, `Section`, and `Repeater` don't take full width by default when nested — set `->columnSpan()` deliberately.
- `->dense()` / `->gap(false)` on layout components (`Section`, `Fieldset`, `Grid`) exist for genuinely compact read-only blocks; don't default to them — official spacing is generous on purpose.

## Guidance and feedback inside the page

- Contextual warnings/tips: `Callout` with a status variant (`->warning()`, `->info()`) — tinted background, icon, bold title, muted description — near the fields it concerns, not at the top of the page.
- One-line hints under a field: the field's own `->helperText()` / `->hint()` beats a separate Text component.
- Static explanatory text between fields: `Text` prime with `->color('neutral')` — the default gray is intentionally dim; neutral is for text meant to be read.
- After a state change, ensure the host communicates the result. Reuse built-in action/page feedback when present; add or customize a `Notification` for custom flows without duplicating it.

## Smell test before finishing a page

Use these as defaults with explicit exceptions, not framework pass/fail contracts:

1. Can I tell what this record is and its state without scrolling?
2. Is there one filled primary action, or a documented peer-outcome reason for more?
3. Does any tab hide something the user needs on every visit?
4. Is any full-width field actually short (or any long field half-width)?
5. Does every empty collection/null value show a deliberate placeholder or empty state?
6. Is every status readable without color (icon + label present)?
7. Would removing a Section/columns level change nothing? Then remove it — structure that doesn't group anything is noise.
8. Does custom CSS solve a documented theme/product need, and does it use a supported hook without duplicating existing component styling?
