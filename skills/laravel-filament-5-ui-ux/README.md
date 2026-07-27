# Laravel Filament 5 UI/UX

Agent skill for selecting and composing official Filament 5 visual patterns from reviewed documentation evidence. It makes the visual decision observable before implementation and keeps custom UI as a documented escape hatch.

## Install

```bash
npx skills add jotafurtado/dev-skills --skill laravel-filament-5-ui-ux
```

Install `laravel-filament-v5` as well when the task needs version-sensitive APIs, security, implementation, or tests:

```bash
npx skills add jotafurtado/dev-skills --skill laravel-filament-v5
```

## What the catalog covers

- Page-level schema and form composition
- Ordinary field wrappers, labels, guidance, states, fused fields, affixes, and contextual callouts
- Repeaters, builders, rich-content editors, uploads, and relationship-heavy controls
- Flat content, responsive grids and deliberate field spans
- Sections, aside sections, fieldsets, horizontal tabs, vertical tabs, and wizards
- Contained, uncontained, compact, secondary, dense, and no-gap treatments
- Official visual evidence and a visible decision trace
- A deterministic local catalog query

The skill supports Filament 5.x only. It does not replace the project's established theme or ask users to choose components when the evidence is sufficient.

## Structure

```text
laravel-filament-5-ui-ux/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── scripts/query_visual_catalog.py
├── scripts/sync_visual_catalog.py
├── scripts/build_review_sheets.py
├── scripts/validate_visual_catalog.py
├── references/settings-form-composition.md
├── references/ordinary-field-composition.md
├── references/complex-input-composition.md
├── references/visual-catalog.json
├── references/screenshot-inventory.json
└── evals/
```

## Verification

```bash
python3 -m unittest discover -s tests -p 'test_laravel_filament_5_ui_ux.py'
python3 skills/laravel-filament-5-ui-ux/scripts/validate_visual_catalog.py
python3 /Users/jotafurtado/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/laravel-filament-5-ui-ux
```

The catalog stores source URLs and original analysis, not official screenshot binaries.

## Maintain the catalog

Synchronize official evidence, inspect any new or changed records in a temporary directory outside the repository, classify the records, and validate before committing:

```bash
python3 skills/laravel-filament-5-ui-ux/scripts/sync_visual_catalog.py
python3 skills/laravel-filament-5-ui-ux/scripts/build_review_sheets.py --output "$(mktemp -d)"
python3 skills/laravel-filament-5-ui-ux/scripts/validate_visual_catalog.py
```

The synchronizer uses bounded concurrency and retries, fails explicitly on incomplete crawls, writes stable JSON, retains matching human review fields, and makes new or materially changed screenshots unreviewed. The review sheet downloads images only to the requested temporary directory.
