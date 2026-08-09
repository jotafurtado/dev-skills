# Dev Skills

This repository publishes reusable agent skills whose behavior is defined by concise core instructions, routed references, and deterministic helpers.

## Language

**Filament 5 visual authority**:
The responsibility of `laravel-filament-v5-ui-ux` to compose Filament 5 surfaces. `laravel-filament-v5` retains authority over version-matched API signatures, security, implementation, and tests.
_Avoid_: Shared visual authority, generic frontend authority

**API inventory**:
A `laravel-filament-v5` reference file that states which official Filament 5 components exist for a surface and what their signatures are. It may name a composition decision so the decision is not skipped in silence, but it never resolves one: which option to choose is a reference composition's job.
_Avoid_: Component guide, recipe, composition, selection guide

**Reference composition**:
Ready-to-adapt Filament 5 code for a whole surface, anchored to an official visual pattern and carrying its provenance. This is the unit the skill hands to a consuming agent.
_Avoid_: Snippet, example, template

**Composition variant**:
A named modification of a reference composition whose conditions change the resulting arrangement, such as horizontal versus vertical tabs or desktop versus mobile table treatment.
_Avoid_: Cosmetic variation, option flag

**Official visual pattern**:
A Filament 5 presentation option evidenced by official documentation and screenshots. Each reference composition realizes exactly one of these.
_Avoid_: Screenshot style, component example

**Composition provenance**:
The official documentation page and screenshot a reference composition was derived from, declared inside the composition itself.
_Avoid_: Citation, reference link, evidence record

**Visual pattern family**:
A grouping of official patterns that share one presentation strategy while exposing meaningful variants.
_Avoid_: Screenshot folder, component documentation page

**Visual option space**:
The set of reference compositions that plausibly satisfy a surface and its user goal. The skill presents this set and helps choose within it; it does not decide on the user's behalf.
_Avoid_: Component list, design inspiration

**Uncovered pattern**:
An official visual pattern present in the screenshot inventory that has no reference composition yet. Tracked as expansion work, not as a defect.
_Avoid_: Missing feature, gap
