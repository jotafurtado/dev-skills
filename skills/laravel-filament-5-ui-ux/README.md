# Laravel Filament 5 UI/UX

Agent skill for selecting and composing official Filament 5 visual patterns from reviewed documentation evidence. It makes the visual decision observable before implementation and keeps custom UI as a documented escape hatch.

Release scope and verification gates: [`RELEASE.md`](./RELEASE.md).

## Install

```bash
npx skills add jotafurtado/dev-skills --skill laravel-filament-5-ui-ux
```

Install `laravel-filament-v5` as well when the task needs version-sensitive APIs, security, implementation, or tests:

```bash
npx skills add jotafurtado/dev-skills --skill laravel-filament-v5
```

## Authority and fallback

This skill exclusively selects and composes Filament 5 visual patterns. `laravel-filament-v5` owns installed-version APIs, security, implementation, and tests; install both for implementation work that changes a material UI surface.

The reviewed catalog works offline after installation. When image inspection or network access is unavailable, use its local interpretation and disclose the limitation in the visual decision trace. Use custom Blade, Livewire, CSS, or theme work only after recording the official candidates checked and the concrete gap they cannot cover.

## What the catalog covers

- Page-level schema and form composition
- Ordinary field wrappers, labels, guidance, states, fused fields, affixes, and contextual callouts
- Repeaters, builders, rich-content editors, uploads, and relationship-heavy controls
- Action groups, destructive confirmations, modal forms, slide-overs, contextual callouts, notifications, feedback, and actionable empty states
- Standard compare-and-scan tables: columns, filters, row and bulk actions, grouping, summaries, pagination, and empty results
- Read-oriented record details and infolists: identity, current status, primary facts, dense metadata, media, copyable identifiers, repeated data, and long-tail detail
- Panel shells: sidebar or top navigation, domain groups and clusters, actionable badges, supported branding, user menus, and authentication hierarchy
- Flat content, responsive grids and deliberate field spans
- Sections, aside sections, fieldsets, horizontal tabs, vertical tabs, and wizards
- Contained, uncontained, compact, secondary, dense, and no-gap treatments
- Official visual evidence and a visible decision trace
- A compact derived index as the primary selection path, with a deterministic local catalog query as an optional alternative

The skill supports Filament 5.x only. It does not replace the project's established theme or ask users to choose components when the evidence is sufficient.

## Structure

```text
laravel-filament-5-ui-ux/
├── SKILL.md
├── README.md
├── RELEASE.md
├── agents/openai.yaml
├── scripts/query_visual_catalog.py
├── scripts/build_catalog_index.py
├── scripts/sync_visual_catalog.py
├── scripts/build_review_sheets.py
├── scripts/validate_visual_catalog.py
├── scripts/run_forward_evals.py
├── scripts/release_install_smoke.py
├── scripts/validate_skill.mjs
├── references/settings-form-composition.md
├── references/ordinary-field-composition.md
├── references/complex-input-composition.md
├── references/action-feedback-composition.md
├── references/table-composition.md
├── references/responsive-record-layouts.md
├── references/record-detail-composition.md
├── references/dashboard-composition.md
├── references/panel-shell-composition.md
├── references/visual-catalog.json
├── references/visual-catalog-index.md
├── references/screenshot-inventory.json
├── references/release-verification.md
└── evals/
```

## Verification

```bash
python3 -m unittest discover -s tests -p 'test_laravel_filament_5_ui_ux.py'
python3 skills/laravel-filament-5-ui-ux/scripts/validate_visual_catalog.py
node skills/laravel-filament-5-ui-ux/scripts/validate_skill.mjs skills/laravel-filament-5-ui-ux
```

The catalog stores source URLs and original analysis, not official screenshot binaries.

## Maintain the catalog

Synchronize official evidence, inspect any new or changed records in a temporary directory outside the repository, classify the records, regenerate the compact index, and validate before committing:

```bash
python3 skills/laravel-filament-5-ui-ux/scripts/sync_visual_catalog.py
python3 skills/laravel-filament-5-ui-ux/scripts/build_review_sheets.py --output "$(mktemp -d)"
python3 skills/laravel-filament-5-ui-ux/scripts/build_catalog_index.py \
  --output skills/laravel-filament-5-ui-ux/references/visual-catalog-index.md
python3 skills/laravel-filament-5-ui-ux/scripts/validate_visual_catalog.py
```

The synchronizer uses bounded concurrency and retries, fails explicitly on incomplete crawls, writes stable JSON, retains matching human review fields, and makes new or materially changed screenshots unreviewed. The review sheet downloads images only to the requested temporary directory. The compact index is generated; never edit it by hand.
