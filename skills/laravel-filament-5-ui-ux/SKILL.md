---
name: laravel-filament-5-ui-ux
description: "Chooses and composes evidence-grounded Filament 5.x UI/UX patterns for settings forms from official documentation and screenshots. Use for designing, redesigning, reviewing, or improving a Filament 5 settings form; use alongside laravel-filament-v5 for version-sensitive APIs and implementation. Do not trigger for generic frontend work, non-Filament interfaces, Filament 3/4, non-settings Filament surfaces, or API/security-only tasks."
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

3. Load the routed reference for the surface. For settings forms, read `references/settings-form-composition.md`.
4. When building or materially restructuring a surface and image viewing is available, inspect at least one listed official screenshot. For a small local change, use the reviewed catalog entry and exact documentation instead.
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
| Settings form grouping, columns, sections, horizontal tabs, vertical tabs, wizard avoidance | `references/settings-form-composition.md` |
| Catalog schema, reviewed evidence, query fields | `references/visual-catalog.json` and `references/screenshot-inventory.json` |

This thin slice covers settings-form composition. Do not infer that its small catalog covers other Filament surfaces; route uncovered UI work to official Filament 5 evidence and record the gap for catalog expansion.

## Verification

For catalog maintenance, synchronize first, review new or changed evidence in a temporary directory outside this repository, classify it, then validate. The synchronizer preserves matching human review fields and marks new or materially changed evidence `unreviewed`.

```bash
python3 scripts/sync_visual_catalog.py
python3 scripts/build_review_sheets.py --output "$(mktemp -d)"
python3 scripts/validate_visual_catalog.py
```

Run the deterministic query test, validate the skill folder, parse both eval files, and review the final diff. The catalog must remain reviewed, locally queryable, and free of screenshot binaries.
