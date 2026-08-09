# Laravel Filament v5 UI/UX

Agent skill that ships ready-to-adapt Filament 5 compositions. Each one is pasteable PHP anchored to the official documentation page and screenshot it was derived from.

Release scope and verification gates: [`RELEASE.md`](./RELEASE.md).

## Install

```bash
npx skills add jotafurtado/dev-skills --skill laravel-filament-v5-ui-ux
```

Install `laravel-filament-v5` as well when the task needs version-sensitive APIs, security, implementation, or tests:

```bash
npx skills add jotafurtado/dev-skills --skill laravel-filament-v5
```

## Authority and fallback

This skill owns surface composition and responsive arrangement inside Filament 5. `laravel-filament-v5` owns installed-version APIs, security, implementation, and tests; install both for implementation work.

Compositions work offline after installation — provenance travels inside each one, so nothing is fetched at use time. There is no required workflow, no mandatory screenshot inspection, and no decision trace. Use custom Blade, Livewire, CSS, or theme work only after recording the official candidates checked and the concrete gap they cannot cover.

## What the library covers

22 patterns and 76 variants across 8 surfaces:

| Surface | File |
|---|---|
| Record tables — compare-and-scan and identity-centred, with filters, grouping, summaries, bulk actions, pagination, empty states | `references/table.md` |
| Page structure — flat content, responsive columns, sections, aside sections, fieldsets, tabs, wizards, density | `references/form-layout.md` |
| Ordinary fields — geometry, labels, guidance, states | `references/form-fields.md` |
| Complex inputs — repeaters and builders, uploads, relationship controls, rich content | `references/form-inputs.md` |
| Record details and infolists — identity, status, facts, media, repeated data, long-tail detail | `references/record-detail.md` |
| Dashboards — stats, charts, table widgets, filters, responsive spans | `references/dashboard.md` |
| Panel shell — top navigation, grouped sidebar, branding, user menu, authentication surfaces | `references/panel-shell.md` |
| Actions and feedback, cross-surface — confirmations, modal forms, slide-overs, notifications, callouts, empty states | `references/action-feedback.md` |

An official pattern listed in `references/screenshot-inventory.json` without a composition is tracked as expansion work, not a defect.

The skill supports Filament 5.x only. It does not replace the project's established theme.

## Structure

```text
laravel-filament-v5-ui-ux/
├── SKILL.md
├── README.md
├── RELEASE.md
├── agents/openai.yaml
├── scripts/validate_compositions.py
├── scripts/verify_filament_apis.py
├── scripts/sync_visual_catalog.py
├── scripts/release_install_smoke.py
├── scripts/validate_skill.mjs
├── references/table.md
├── references/form-layout.md
├── references/form-fields.md
├── references/form-inputs.md
├── references/record-detail.md
├── references/dashboard.md
├── references/panel-shell.md
├── references/action-feedback.md
├── references/screenshot-inventory.json
├── references/release-verification.md
└── evals/eval_queries.json
```

## Verification

```bash
python3 -m unittest discover -s tests -p 'test_laravel_filament_v5_ui_ux.py'
python3 skills/laravel-filament-v5-ui-ux/scripts/validate_compositions.py
python3 skills/laravel-filament-v5-ui-ux/scripts/verify_filament_apis.py
node skills/laravel-filament-v5-ui-ux/scripts/validate_skill.mjs skills/laravel-filament-v5-ui-ux
```

Composition validation parses every PHP block with `php -l`. Blocks are fragments, so each is wrapped in the smallest valid context first — a class body, a method body, a chain, a statement, an array element, or a complete file. Pass `--skip-php` only where no PHP binary exists.

The library stores source URLs and original analysis, not official screenshot binaries.

## Expand the library

Synchronize official evidence, review new or changed records, then convert any newly covered pattern into a reference composition and validate:

```bash
python3 skills/laravel-filament-v5-ui-ux/scripts/sync_visual_catalog.py
python3 skills/laravel-filament-v5-ui-ux/scripts/validate_compositions.py
```

The synchronizer uses bounded concurrency and retries, fails explicitly on incomplete crawls, writes stable JSON, retains matching human review fields, and makes new or materially changed screenshots unreviewed.
