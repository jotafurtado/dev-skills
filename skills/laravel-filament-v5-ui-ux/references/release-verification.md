# Release verification

Evidence recorded for a `laravel-filament-v5-ui-ux` release. The candidate is the composition library; the baseline is `laravel-filament-v5` alone.

## Authority: `laravel-filament-v5`

The baseline skill owns installed-version API signatures, authorization, security, implementation, and tests. Every composition that names a signature routes there rather than restating it. A release is not reviewed until that routing holds in each shipped file.

## Gates

| Gate | Command | Passing condition |
|---|---|---|
| Composition validation | `python3 scripts/validate_compositions.py` | Every PHP block parses; every pattern carries `When`, `Not when`, and an official `Source`; no placeholder identifiers; no namespace removed in Filament 5 |
| Deterministic tests | `python3 -m unittest discover -s tests -p 'test_laravel_filament_v5_ui_ux.py'` | All pass |
| Skill structure | `node scripts/validate_skill.mjs skills/laravel-filament-v5-ui-ux` | Valid |
| Clean install | `python3 scripts/release_install_smoke.py` | Candidate and paired installs resolve from the repository origin |
| Filament resolution | `python3 scripts/verify_filament_apis.py` | Every Filament class imported and every enum case referenced by a composition exists in the resolved `filament/filament` version |

The Composer fixture is the gate that PHP syntax linting cannot cover: a renamed or removed API parses correctly and still fails at runtime. Run it before publishing, never only the linter.

The fixture resolves into `.filament-fixture/` at the repository root and is reused between runs; `--refresh` discards it, and `--constraint` targets a different version. Method calls are out of scope — resolving the receiver of a fluent chain needs type inference the fixture cannot cheaply provide, so the gate covers imported classes and enum cases, which is where version drift actually shows up.

## Coverage

Coverage is the release metric, reported by `scripts/validate_compositions.py`.

| Surface | File | Patterns | Variants |
|---|---|---|---|
| Record tables | `references/table.md` | 2 | 14 |
| Form and schema layout | `references/form-layout.md` | 9 | 11 |
| Ordinary fields | `references/form-fields.md` | 1 | 10 |
| Complex inputs | `references/form-inputs.md` | 4 | 11 |
| Record details and infolists | `references/record-detail.md` | 1 | 9 |
| Dashboards | `references/dashboard.md` | 1 | 5 |
| Panel shell and authentication | `references/panel-shell.md` | 3 | 9 |
| Actions and feedback (cross-surface) | `references/action-feedback.md` | 1 | 7 |
| **Total** | | **22** | **76** |

An official pattern present in `references/screenshot-inventory.json` without a reference composition is an uncovered pattern: expansion work, not a defect.

## Evidence: local reviewed catalog

Compositions were derived from official Filament 5.x documentation pages and their screenshots, recorded inline as each composition's `Source`. No screenshot binaries are redistributed.

## What is no longer verified

Narrative forward evaluations were discontinued in 2.0.0. They scored whether an agent described a comparison and declared a delegation, not whether it composed a correct interface, and a full rerun was cancelled on token cost. Composition parsing plus the Composer fixture replace them with checks that cannot be satisfied by narration.
