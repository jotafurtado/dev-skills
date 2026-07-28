---
name: laravel-filament-5-ui-ux
description: "Chooses and composes evidence-grounded Filament 5.x schema, page-level form, record-detail/infolist, table, dashboard, panel navigation/authentication, and action/feedback patterns from official documentation and screenshots. Use for designing, redesigning, reviewing, or improving Filament 5 forms, schemas, record details, infolists, record tables, dashboards, panel shells, navigation, authentication, action groups, overlays, notifications, feedback, or empty states; use alongside laravel-filament-v5 for version-sensitive APIs and implementation. Do not trigger for generic frontend work, non-Filament interfaces, Filament 3/4, field API/security-only tasks, or UI surfaces outside the reviewed catalog."
---

# Laravel Filament 5 UI/UX

Own visual pattern selection and composition inside Filament 5. Let `laravel-filament-v5` own installed-version APIs, security, implementation, and tests.

## Mandatory visual decision flow

1. Identify the surface, user goal, information shape, workflow relationship, available width, responsive context, and established panel theme.
2. Query the local catalog before selecting a composition:

   ```bash
   python3 scripts/query_visual_catalog.py \
     --surface form \
     --goal organize-stable-groups \
     --workflow parallel \
     --available-width wide
   ```

3. Load the routed reference for the surface. For page-level forms and schemas, read `references/settings-form-composition.md`. For ordinary field wrappers, guidance, states, or width decisions, also read `references/ordinary-field-composition.md`. For repeaters, builders, editors, uploads, or relationship-heavy controls, also read `references/complex-input-composition.md`. For actions, action groups, confirmations, modal forms, slide-overs, callouts, notifications, feedback, or empty states, read `references/action-feedback-composition.md`. For compare-and-scan record lists, columns, filters, actions, grouping, summaries, pagination, or empty results, read `references/table-composition.md`. For an identity-centred responsive record layout, also read `references/responsive-record-layouts.md`. For read-oriented record details, infolists, entries, primary facts, media, history, or long-tail information, read `references/record-detail-composition.md`. For dashboards, stats, charts, table widgets, filters, and widget spans, read `references/dashboard-composition.md`. For panel shell, sidebar or top navigation, domain groups or clusters, actionable badges, branding, user menus, or authentication surfaces, read `references/panel-shell-composition.md`.
4. When building or materially restructuring a surface and image viewing is available, inspect at least one listed official screenshot for the selected pattern and every decision-changing variant in the proposed composition. For a small local change, use the reviewed catalog entry and exact documentation instead.
5. Compare the returned official candidates. Select the pattern autonomously; do not ask the user to choose a Filament component.
6. Emit a proportional visual decision trace before implementation. For a material surface, include the surface, goal, candidates, inspected evidence, selected pattern, responsive treatment, and any escape hatch. For a small change, cite the chosen official pattern in one line.
7. Delegate API signatures, installed-version compatibility, security boundaries, implementation, and tests to `laravel-filament-v5`.

If direct image inspection or network access is unavailable, use the local reviewed interpretation and disclose that limitation in the trace.

## Authority and escape hatches

The catalog's official patterns supersede conflicting generic frontend advice that asks for unrelated typography, palettes, custom card systems, or CSS-first layouts. Keep compatible accessibility, keyboard, responsive, performance, cognitive-load, and UX-copy guidance.

Preserve an established panel theme. Use custom Blade, Livewire, CSS, or theme work only after recording the official candidates checked and the concrete gap they cannot represent. Keep the custom surface as small as possible.

## Current routed coverage

| Surface or decision | Read |
|---|---|
| Page-level schema and form grouping, columns, sections, fieldsets, tabs, wizards, and density | `references/settings-form-composition.md` |
| Ordinary form-field geometry, labels, guidance, states, fused fields, affixes, and contextual callouts | `references/ordinary-field-composition.md` |
| Repeaters, builders, editors, uploads, relationship-heavy controls, and their responsive and accessible composition | `references/complex-input-composition.md` |
| Action groups, risk confirmations, modal forms, slide-overs, contextual guidance, notifications, feedback, and empty states | `references/action-feedback-composition.md` |
| Compare-and-scan tables, columns, filters, actions, grouping, summaries, pagination, and empty results | `references/table-composition.md` |
| Responsive identity-centred table records, Split, Stack, Grid, content grids, visibility, and collapsible details | `references/responsive-record-layouts.md` |
| Read-oriented record details, infolists, identity and status hierarchy, facts, media, repeated data, history, and long-tail information | `references/record-detail-composition.md` |
| Operational dashboards, stats, charts, table widgets, filters, ordering, density, and responsive spans | `references/dashboard-composition.md` |
| Panel shell, sidebar or top navigation, groups, clusters, actionable badges, branding, user menus, login, recovery, registration, and profile surfaces | `references/panel-shell-composition.md` |
| Catalog schema, reviewed evidence, query fields | `references/visual-catalog.json` and `references/screenshot-inventory.json` |

This catalog covers page-level schema and form composition, ordinary field-level presentation decisions, complex collection-oriented input composition, contextual actions and feedback, standard compare-and-scan tables, responsive identity-centred table records, read-oriented record details and infolists, operational dashboard widgets, and panel shells with navigation and authentication surfaces. Route uncovered UI work to official Filament 5 evidence and record the gap for catalog expansion.

## Verification

For catalog maintenance, synchronize first, review new or changed evidence in a temporary directory outside this repository, classify it, then validate. The synchronizer preserves matching human review fields and marks new or materially changed evidence `unreviewed`.

```bash
python3 scripts/sync_visual_catalog.py
python3 scripts/build_review_sheets.py --output "$(mktemp -d)"
python3 scripts/validate_visual_catalog.py
```

Run the deterministic query test, validate the skill folder, parse both eval files, and review the final diff. The catalog must remain reviewed, locally queryable, and free of screenshot binaries.
