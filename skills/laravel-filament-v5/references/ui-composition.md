# UI composition — fluid, scannable pages from official components

The gate in SKILL.md decides *which* component renders each piece of data. This file decides *how the page is organized*. Both matter: a page built only from correct components can still overwhelm the user. Composition is where you have full design freedom — use it.

## The organizing principle

**A user should answer "what is this record and what state is it in?" within 2 seconds, and find any secondary detail within 10.** Every decision below serves that: primary information first and always visible; secondary information grouped, collapsed, or tabbed away — reachable, never in the way.

## Choosing the structural container

Decision order — prefer the lightest structure that works:

1. **Nothing** (flat fields) — up to ~6 fields with no natural grouping. Don't wrap 3 fields in a Section just to have one.
2. **`Section`** — fields form 2–4 named groups the user scans top-to-bottom. Give every Section a heading; add `->description()` when the grouping isn't self-evident. This is the default container for resources.
3. **`Tabs`** — 3+ groups where the user works in ONE group at a time (General / SEO / Advanced). Tabs hide content — never put a field the user must always see inside a non-default tab, and never use tabs for content that should be compared side by side.
4. **`Wizard`** — the input has a natural sequence with dependencies between steps (checkout, onboarding). Don't wizard-ify a form the user might fill in any order; that adds clicks for nothing.

Same order applies to infolists — Sections for scanning, Tabs for large read-only surfaces (details / history / raw payload).

## Visual hierarchy within a page

- **Identity first**: the top section holds what identifies the record — name/title, status badge, owner, timestamps. A user landing on the page reads only this 80% of the time.
- **Default finite workflow statuses to badges** — `TextEntry::make('status')->badge()` with an enum providing color/icon. Keep plain text when color or badge emphasis would imply semantics the value does not have.
- **Collapse the long tail**: audit metadata, internal notes, raw payloads → `Section::make(...)->collapsible()->collapsed()`. Present but silent.
- **Dense metadata blocks**: `->inlineLabel()` on entries (label beside value) reads better than stacked label-over-value for many short facts.
- **Avoid unexplained empty space**: use `->placeholder('—')` for meaningful nullable values and `EmptyState` / `->emptyStateHeading()` for an empty collection. Add an action only when the user can and should resolve the state.

## Columns and width

- Forms and infolists: `->columns(2)` on Sections is the sweet spot for desktop; 3+ only for short fields (dates, toggles, numbers).
- Long-form fields (`Textarea`, `RichEditor`, `Repeater`, `CodeEntry`) get `->columnSpanFull()` — a rich editor squeezed into half a grid is the most common layout bug.
- Related short fields should sit on the same row (start/end date, min/max) — that's what `Grid::make(2)` inside a Section is for.
- Remember: `Grid`, `Section`, and `Repeater` don't take full width by default when nested — set `->columnSpan()` deliberately.

## Tables that stay scannable

- **5–7 visible columns maximum.** Everything else exists but hidden: `->toggleable(isToggledHiddenByDefault: true)`.
- Column order = question order: identity → status (badge) → the 2–3 facts users filter/compare by → dates last.
- 3+ row actions collapse into `ActionGroup::make([...])` — a row with five buttons is noise.
- Prefer a `SelectFilter` on an enum over asking users to search for status strings.
- `->defaultSort()` should match how users think about recency/priority — an unsorted table reads as random.

## Guidance and feedback inside the page

- Contextual warnings/tips: `Callout` with a status variant (`->warning()`, `->info()`) — near the fields it concerns, not at the top of the page.
- One-line hints under a field: the field's own `->helperText()` / `->hint()` beats a separate Text component.
- Static explanatory text between fields: `Text` prime with `->color('neutral')` — the default gray is intentionally dim; neutral is for text meant to be read.
- After any action that changes state: a `Notification`. Silent success is indistinguishable from failure.

## Smell test before finishing a page

Ask these; each "no" is a composition bug even if every component is official:

1. Can I tell what this record is and its state without scrolling?
2. Does any tab hide something the user needs on every visit?
3. Is any full-width field actually short (or any long field half-width)?
4. Does every empty collection/null value show a deliberate placeholder or empty state?
5. Would removing a Section/columns level change nothing? Then remove it — structure that doesn't group anything is noise.
