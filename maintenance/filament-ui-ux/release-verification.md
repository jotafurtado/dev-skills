# Release verification

Evidence recorded for a `laravel-filament-v5-ui-ux` release. The candidate is the composition library; the baseline is `laravel-filament-v5` alone.

## Authority: `laravel-filament-v5`

The baseline skill owns installed-version API signatures, authorization, security, implementation, and tests. Every composition that names a signature routes there rather than restating it. A release is not reviewed until that routing holds in each shipped file.

## Gates

| Gate | Command | Passing condition |
|---|---|---|
| Composition validation | `python3 maintenance/filament-ui-ux/scripts/validate_compositions.py` | Every PHP block parses; every pattern carries `When`, `Not when`, and an official `Source`; no placeholder identifiers; no namespace removed in Filament 5 |
| Deterministic tests | `python3 -m unittest discover -s tests -p 'test_laravel_filament_v5_ui_ux.py'` | All pass |
| Skill structure | `node maintenance/validate_skill.mjs skills/laravel-filament-v5-ui-ux` | Valid |
| Clean install | `python3 maintenance/filament-ui-ux/scripts/release_install_smoke.py` | Candidate and paired installs resolve from the repository origin |
| Filament resolution | `python3 maintenance/filament-ui-ux/scripts/verify_filament_apis.py` | Every Filament class imported and every enum case referenced by a composition exists in the resolved `filament/filament` version |

The Composer fixture is the gate that PHP syntax linting cannot cover: a renamed or removed API parses correctly and still fails at runtime. Run it before publishing, never only the linter.

The fixture resolves into `.filament-fixture/` at the repository root and is reused between runs; `--refresh` discards it, and `--constraint` targets a different version. Method calls are out of scope — resolving the receiver of a fluent chain needs type inference the fixture cannot cheaply provide, so the gate covers imported classes and enum cases, which is where version drift actually shows up.

## Preconditions

`verify_filament_apis.py` needs `php` and `composer` on `PATH` and exits before resolving anything when either is missing. The fixture directory is `.filament-fixture/` at the repository root and is gitignored. The first run, a change to the fixture manifest, or `--refresh` runs `composer install` there and needs network access to resolve `filament/filament`. A later run that already has `vendor/autoload.php` does not. `release_install_smoke.py` needs `npx` and network access to the skills installer; it is separate from the unit suite.

## Tests versus composition validation

`tests/test_laravel_filament_v5_ui_ux.py` checks maintainer behavior: fragment wrapping so `php -l` can parse a composition, screenshot-inventory synchronization, which symbols the API gate collects, sibling-file discovery, and the absence of the retired catalog query tool. It does not grade the composition a consuming agent pastes, and a green unit run is not a release pass. `validate_compositions.py` is that gate. It reads the shipped reference files, requires `When`, `Not when`, and an official `Source` on every pattern, and parses every PHP block. `verify_filament_apis.py` then checks the imported Filament classes and enum cases in those blocks against the fixture. Narrative forward runs are not a gate. They were discontinued in 2.0.0 and are not recorded as passes.

## Coverage

Coverage is the release metric, reported by `maintenance/filament-ui-ux/scripts/validate_compositions.py`.

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

An official pattern present in `maintenance/filament-ui-ux/screenshot-inventory.json` without a reference composition is an uncovered pattern: expansion work, not a defect. After a successful run, `validate_compositions.py` prints the list (or `none`); it does not fail the gate.

A family is covered only when a composition heading matches it by slug or by equal token set (stopwords ignored). Subset matches are not coverage. Composition headings that match no family are listed after the uncovered-family list; they do not fail the gate.

## Evidence: local reviewed catalog

Compositions were derived from official Filament 5.x documentation pages and their screenshots, recorded inline as each composition's `Source`. No screenshot binaries are redistributed.

## What is no longer verified

Narrative forward evaluations were discontinued in 2.0.0. They scored whether an agent described a comparison and declared a delegation, not whether it composed a correct interface, and a full rerun was cancelled on token cost. Composition parsing plus the Composer fixture replace them with checks that cannot be satisfied by narration.
