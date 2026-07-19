# UI composition — fluid, scannable pages from official components

The gate in SKILL.md decides *which* component renders each piece of data. This file decides *how the page is organized and how it should look*. Both matter: a page built only from correct components can still overwhelm the user. Composition is where you have full design freedom — use it.

Every rule here is distilled from the official 5.x documentation screenshots. When you are unsure what a surface should look like, don't guess — load `references/screenshots.md` and view the official example before composing.

## The organizing principle

**A user should answer "what is this record and what state is it in?" within 2 seconds, and find any secondary detail within 10.** Every decision below serves that: primary information first and always visible; secondary information grouped, collapsed, or tabbed away — reachable, never in the way.

## The official design language — work with it, never against it

Filament's rendered UI already has a deliberate visual system. Custom CSS that fights it produces panels that look broken, not distinctive:

- **Calm surface**: light gray page background, white cards with large radii and near-invisible borders, generous padding. Don't add gradients, drop shadows, or tighter spacing via CSS.
- **One accent, used sparingly**: the primary color appears only on the active nav item, the single primary action, links, and focus rings. If primary-colored elements compete on one screen, the hierarchy is wrong.
- **Semantic color is reserved for state**: success/warning/danger/info appear in badges, icons, callouts, and destructive buttons — never as decoration. State is always communicated by icon + color + label together, not color alone.
- **One typeface, hierarchy by weight**: bold for headings and identity values, medium for labels, regular for values, muted gray for secondary text. Don't introduce font families or sizes via CSS.
- **Quiet by default, loud once**: exactly one filled primary button per screen (the page's main action, top right). Everything else is outlined, link-style, or an icon button.
- Panel identity comes from `->colors()`, `->brandLogo()`, `->font()` in the panel provider — not from CSS overrides. Distinctiveness lives in composition and content, not restyling.

## Page recipes

### List page (table)

Official anatomy, top to bottom — deviate only with a reason:

1. **Header**: page heading + one-line description on the left; the single filled primary action (`CreateAction`) on the right.
2. **Toolbar**: search field on the right; filters and column toggles as icon buttons at the far right (filter icon shows an active-count badge); `Group by` / `Sort by` selects on the left when used.
3. **Rows**: checkbox (only if bulk actions exist) → identity column (bold, optionally with avatar/image) → the 2–3 facts users compare → status badge → dates. Row actions right-aligned, link-style with icon (`Edit`), destructive ones red and last; 3+ actions collapse into `ActionGroup`.
4. **Footer**: "Showing X to Y of Z results" left, per-page select, page numbers right.

Guidelines observed in the official examples:

- **5–7 visible columns maximum.** Everything else exists but hidden: `->toggleable(isToggledHiddenByDefault: true)`.
- Column order = question order: identity → status (badge) → comparison facts → dates last.
- Booleans render as icons (`IconColumn->boolean()`), never "Yes"/"No" text.
- Prefer a `SelectFilter` on an enum over asking users to search for status strings.
- `->defaultSort()` should match how users think about recency/priority — an unsorted table reads as random.
- `->defaultGroup()` with subtle group-header rows replaces a redundant status column when users scan by state.
- Alternative record layouts (`Split`, `Stack`, grid) are for records where a photo/identity block matters more than comparable facts (people, products, cards) — a `Split` holds identity left, contact facts center, collapsible `Panel` for the long tail. Regular columns beat card grids for compare-and-scan work.

### Create / Edit page (form)

- Structural container per the decision order below; `->columns(2)` sections as the desktop default.
- **Settings-style pages**: `Section::make(...)->aside()` — heading and description in a left column, fields in a card on the right. This is the official look for configuration screens.
- Required marker, label above field, `->helperText()` below — never restate the label as helper text.
- Long-form fields (`Textarea`, `RichEditor`, `Repeater`, `Builder`) span full width; related short fields (start/end, min/max) share a row.
- `Repeater` items render as cards with a delete icon top-right and a centered "Add" button below — don't rebuild this with custom markup.
- **Wizard** only for genuinely sequential input (checkout, onboarding): numbered chevron steps, one `Next` filled button per step, submit on the last step.

### View page (infolist)

- Two-zone layout seen in the official example: a main `Section` (2/3 width) with identity — name, status badge, description, image — beside a narrow `Section` (1/3) with the key facts (price, flags, attributes). Below, `Tabs` for large secondary surfaces (specifications, reviews, history, raw payload) with `->badge()` counts on tab labels.
- Identity values render larger/bold via `TextEntry->size()`/`->weight()`; labels stay muted. Copyable identifiers (SKU, IDs) use `->copyable()` with a badge-like look.
- Dense fact blocks: `->inlineLabel()` (label left, value right) — the official "Details card" pattern for many short facts.
- Finite workflow statuses default to `->badge()` with a `HasColor`/`HasIcon` enum. Keep plain text when badge emphasis would imply semantics the value doesn't have.

### Dashboard

Official composition, top to bottom:

1. **Stats row** (`StatsOverviewWidget`): 3–4 tiles — muted label, large bold value, trend description with directional icon, sparkline chart. Color the *trend by its meaning* (a decrease in signups is `danger` even though a decrease in churn is `success`), not by direction.
2. **Charts** in a 2-column grid; every chart widget carries a heading (and `->description()` when the metric needs context).
3. **Recent-activity table widget** full width at the bottom.

Order widgets by decision value: what the admin acts on daily goes first. A dashboard with more than ~7 widgets needs dashboard filters or a second dashboard page.

### Navigation

- Sidebar items get an icon each; group related resources with `->navigationGroup()` labels (Shop, Content, Settings). Groups are collapsible; don't exceed ~7 items per group.
- Numeric nav badges only for actionable counts (pending orders), not vanity totals — implemented as the static `getNavigationBadge()` on the resource (see `references/panels.md`).
- Top navigation (`->topNavigation()` on the panel) suits panels with few items and no groups; the sidebar is the default for real back-offices.

### Modals and confirmation

- **Confirmation modal** (official look): compact, centered icon in a tinted circle (danger red for deletes), bold title, muted one-line question, then equal-width `Cancel` (outline) + `Confirm` (filled, status color). `->requiresConfirmation()` gives you all of it — don't rebuild.
- Action forms: small (1–4 fields) → standard centered modal; larger or reference-heavy → `->slideOver()`. Footer holds `Submit` (filled) then `Cancel` (outline), left-aligned.
- Never nest a second decision inside a modal; a modal that needs tabs should be a page.

## Choosing the structural container

Decision order — prefer the lightest structure that works:

1. **Nothing** (flat fields) — up to ~6 fields with no natural grouping. Don't wrap 3 fields in a Section just to have one.
2. **`Section`** — fields form 2–4 named groups the user scans top-to-bottom. Give every Section a heading; add `->description()` when the grouping isn't self-evident. This is the default container for resources. Variants: `->aside()` for settings pages, `->compact()`/`->secondary()` for subordinate blocks, `->collapsible()` for the long tail.
3. **`Tabs`** — 3+ groups where the user works in ONE group at a time (General / SEO / Advanced). Tabs hide content — never put a field the user must always see inside a non-default tab, and never use tabs for content that should be compared side by side. `->badge()` on a tab label signals how much lives inside.
4. **`Wizard`** — the input has a natural sequence with dependencies between steps (checkout, onboarding). Don't wizard-ify a form the user might fill in any order; that adds clicks for nothing.

Same order applies to infolists — Sections for scanning, Tabs for large read-only surfaces (details / history / raw payload).

## Visual hierarchy within a page

- **Identity first**: the top section holds what identifies the record — name/title, status badge, owner, timestamps. A user landing on the page reads only this 80% of the time.
- **Default finite workflow statuses to badges** — `TextEntry::make('status')->badge()` with an enum providing color/icon.
- **Collapse the long tail**: audit metadata, internal notes, raw payloads → `Section::make(...)->collapsible()->collapsed()`. Present but silent.
- **Dense metadata blocks**: `->inlineLabel()` on entries (label beside value) reads better than stacked label-over-value for many short facts.
- **Avoid unexplained empty space**: use `->placeholder('—')` for meaningful nullable values and `EmptyState` / `->emptyStateHeading()` for an empty collection.
- **Empty states** (official look): centered icon in a tinted circle, bold heading naming what's missing, muted one-line "get started" description, one primary action. Add the action only when the user can and should resolve the state.

## Columns and width

- Forms and infolists: `->columns(2)` on Sections is the sweet spot for desktop; 3+ only for short fields (dates, toggles, numbers).
- Long-form fields (`Textarea`, `RichEditor`, `Repeater`, `CodeEntry`) get `->columnSpanFull()` — a rich editor squeezed into half a grid is the most common layout bug.
- Related short fields should sit on the same row (start/end date, min/max) — that's what `Grid::make(2)` inside a Section is for.
- Remember: `Grid`, `Section`, and `Repeater` don't take full width by default when nested — set `->columnSpan()` deliberately.
- `->dense()` / `->gap(false)` on layout components (`Section`, `Fieldset`, `Grid`) exist for genuinely compact read-only blocks; don't default to them — official spacing is generous on purpose.

## Guidance and feedback inside the page

- Contextual warnings/tips: `Callout` with a status variant (`->warning()`, `->info()`) — tinted background, icon, bold title, muted description — near the fields it concerns, not at the top of the page.
- One-line hints under a field: the field's own `->helperText()` / `->hint()` beats a separate Text component.
- Static explanatory text between fields: `Text` prime with `->color('neutral')` — the default gray is intentionally dim; neutral is for text meant to be read.
- After any action that changes state: a `Notification`. Silent success is indistinguishable from failure.

## Smell test before finishing a page

Ask these; each "no" is a composition bug even if every component is official:

1. Can I tell what this record is and its state without scrolling?
2. Is there exactly one filled primary action on the screen?
3. Does any tab hide something the user needs on every visit?
4. Is any full-width field actually short (or any long field half-width)?
5. Does every empty collection/null value show a deliberate placeholder or empty state?
6. Is every status readable without color (icon + label present)?
7. Would removing a Section/columns level change nothing? Then remove it — structure that doesn't group anything is noise.
8. Did I add any custom CSS that only restyles what the theme already styles? Remove it.
