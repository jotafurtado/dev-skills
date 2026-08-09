# Release 2.0.0

`laravel-filament-v5-ui-ux` is a Filament 5.x only composition library. It ships ready-to-adapt code for forms, schemas, record tables, record details and infolists, dashboards, panel shells, and contextual actions with feedback. It does not provide Filament 3.x or 4.x guidance.

## What changed in 2.0.0

This is a breaking change to what the skill delivers. Previous versions returned a selection procedure; this version returns code.

- **Reference compositions replace evidence lookup.** Every surface ships pasteable PHP with the official documentation and screenshot it was derived from, declared inline. See [`docs/adr/0002-reference-compositions-over-evidence-lookup.md`](../../docs/adr/0002-reference-compositions-over-evidence-lookup.md).
- **No required workflow.** The mandatory decision flow, the runtime screenshot inspection, and the visual decision trace are removed. The skill presents the compositions that fit and helps choose.
- **Authority boundary moved.** From "selection versus implementation" to surface composition versus field API, security, and tests. Where both skills describe a component, `laravel-filament-v5` states that it exists and what its signature is; this skill states how it is arranged.
- **Removed:** the catalog query engine, the controlled vocabulary, the derived compact index, `visual-catalog.json`, and the narrative forward evaluations. Passing them measured dialect fluency, not correctness.
- **Retained:** `references/screenshot-inventory.json` as the discovery asset that identifies official patterns without a reference composition yet.

## Coverage

22 patterns and 76 variants across 8 surfaces, all lint-clean. Coverage is the release metric: an official pattern present in the screenshot inventory without a reference composition is expansion work, reported by `scripts/validate_compositions.py`.

## Authority boundary

This skill owns surface composition and responsive arrangement. Install `laravel-filament-v5` alongside it when the task also needs installed-version APIs, implementation, security, or tests; that skill owns those concerns.

Install the composition library alone when a task is design only:

```bash
npx skills add jotafurtado/dev-skills --skill laravel-filament-v5-ui-ux
```

Install both skills for implementation work:

```bash
npx skills add jotafurtado/dev-skills --skill laravel-filament-v5-ui-ux --skill laravel-filament-v5
```

## Runtime fallbacks and maintenance

The compositions work offline after installation; each one carries its provenance URLs so nothing is fetched at use time. Custom Blade, Livewire, CSS, or theme work is an escape hatch only after naming the official candidates checked and the concrete gap they cannot cover.

Synchronize the screenshot inventory, review new or changed evidence, and convert any newly covered official pattern into a reference composition before a maintenance release. The repository stores URLs and original analysis, not official screenshot binaries.

## Release gates

Run composition validation (`scripts/validate_compositions.py`), the deterministic tests, eval JSON parsing, the clean-install smoke test (`scripts/release_install_smoke.py`), and a final authority-boundary review. Composition validation is the substantive gate: it parses every PHP block with `php -l` under the six fragment shapes, and rejects a pattern missing `When`, `Not when`, or an official `Source`. Verify the compositions resolve against the target Filament version with `scripts/verify_filament_apis.py`, which resolves a Composer fixture and checks every imported Filament class and enum case against the installed source. The verification reference records the candidate comparison. Keep the skill presented under the Jota Furtado Dev Skills repository origin.
