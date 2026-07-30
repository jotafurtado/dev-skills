# Separate Filament 5 UI/UX authority

Status: Accepted

## Context

`laravel-filament-v5` already documents official components, composition guidance, and screenshot references, but agents can satisfy its broad implementation workflow without inspecting the relevant visual evidence or comparing the official visual option space. This repeatedly leads to custom or generic interface patterns where Filament 5 already provides a suitable composition.

Adding more visual detail to the same skill would increase its routing depth and instruction load without making visual selection observable. A separate skill introduces coordination cost, but gives visual tasks a narrow trigger, a mandatory evidence workflow, and focused evaluation.

## Decision

Create `laravel-filament-5-ui-ux` as the exclusive authority for visual pattern discovery, selection, composition, responsive behavior, and UI/UX review inside Filament 5 interfaces.

Keep `laravel-filament-v5` authoritative for installed-version resolution, API signatures, implementation, security, and tests. It delegates material visual work to `laravel-filament-5-ui-ux`; the UI/UX skill delegates version-sensitive implementation facts back to `laravel-filament-v5`.

The UI/UX skill uses a pre-interpreted catalog with three layers:

1. A complete inventory of official Filament 5 documentation screenshots.
2. Decision-oriented visual pattern families.
3. Individual records for variants whose differences can change pattern selection.

Every UI task queries the catalog. Material composition work inspects at least one relevant official screenshot when image viewing is available. The agent makes the selection autonomously and emits an externally observable visual decision trace whose detail scales with the task. Custom UI requires a documented official-component gap.

## Consequences

- Visual decisions become evidence-based and testable instead of depending on optional reference loading.
- The two skills must cross-route explicitly and avoid contradictory visual guidance.
- Catalog synchronization, interpretation coverage, documentation-link validation, and adversarial behavioral evaluations become release gates.
- The repository stores official URLs, metadata, and original analysis rather than redistributing screenshot binaries.
- The new skill supports Filament 5.x only.
