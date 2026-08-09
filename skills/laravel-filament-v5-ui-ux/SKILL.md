---
name: laravel-filament-v5-ui-ux
description: "Provides ready-to-adapt Filament 5.x compositions for record tables, form and schema page structure, everyday fields, collection and upload and relationship and rich-content controls, record details and infolists, operational dashboards, panel shells with navigation and authentication, and contextual actions with confirmations, notifications, callouts, and empty states. Use when building or restructuring a Filament 5 surface; use alongside laravel-filament-v5 for API signatures, security, and tests. Do not trigger for generic frontend work, non-Filament interfaces, Filament 3/4, small local edits, API or security-only tasks, or UI review unless the user asks for a review."
license: MIT
metadata:
  author: jotafurtado
  version: "2.1.0"
  domain: frontend
  filament_version: "5.x"
---

# Laravel Filament v5 UI/UX

A library of reference compositions for Filament 5 surfaces. Let `laravel-filament-v5` own installed-version APIs, security, implementation, and tests.

## How to use it

Find the row below that matches what you are building, read that file, and pick the composition whose `When` fits the task. Paste it and adapt the model, fields, and relations. Each composition carries the official documentation and screenshot it came from.

There is no required workflow, no mandatory screenshot inspection, and no decision trace. Pick the composition that fits and build.

If more than one composition fits, prefer the one whose `Not when` does not describe your task. If none fits, say so and record the surface as an uncovered pattern instead of improvising a composition.

## Routing

| Building or restructuring | Read |
|---|---|
| A record table | `references/table.md` |
| Page structure of a form or schema — entry point; grouping, columns, sections, tabs, wizards, density | `references/form-layout.md` |
| An everyday form field composed inside that structure — geometry, labels, guidance, states | `references/form-fields.md` |
| A collection, upload, relationship, or rich-content control composed inside that structure | `references/form-inputs.md` |
| Record details and infolists | `references/record-detail.md` |
| Operational dashboards and widgets | `references/dashboard.md` |
| Panel shell, navigation, branding, authentication surfaces | `references/panel-shell.md` |
| Actions, confirmations, overlays, notifications, callouts, empty states | `references/action-feedback.md` |

Every file above is a set of reference compositions: pasteable code with provenance. `action-feedback.md` is cross-surface and applies on top of any of the others.

These files are the only source for the surfaces they cover.

## Pairing

Compositions are code, so implementation work almost always needs `laravel-filament-v5` installed alongside this skill — it owns API signatures, authorization, security, and tests. Install both for any task that will ship the composition:

```bash
npx skills add jotafurtado/dev-skills --skill laravel-filament-v5-ui-ux --skill laravel-filament-v5
```

This skill alone is sufficient only while the work stays inside arrangement. The moment a task needs an exact signature, an authorization boundary, a migration, or a test, that is the sibling skill's territory. If it is not installed, say so before emitting a composition that depends on it rather than reconstructing those facts here.

## Authority

Official Filament composition supersedes generic frontend advice asking for unrelated typography, palettes, custom card systems, or CSS-first layouts. Keep compatible accessibility, keyboard, responsive, performance, and UX-copy guidance.

Preserve an established panel theme. Before writing custom Blade, Livewire, or CSS, name the official component you checked and the concrete gap it cannot cover, and keep the custom surface as small as possible.

Delegate API signatures, installed-version compatibility, security boundaries, implementation, and tests to `laravel-filament-v5`.
