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

## What the first slice covers

- Settings-form composition
- Responsive columns and deliberate field spans
- Sections, horizontal tabs, vertical tabs, and wizard avoidance
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
├── references/settings-form-composition.md
├── references/visual-catalog.json
└── evals/
```

## Verification

```bash
python3 -m unittest discover -s tests -p 'test_laravel_filament_5_ui_ux.py'
python3 /Users/jotafurtado/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/laravel-filament-5-ui-ux
```

The catalog stores source URLs and original analysis, not official screenshot binaries.
