# Dev Skills

This repository publishes reusable agent skills whose behavior is defined by concise core instructions, routed references, deterministic helpers, and forward-tested examples.

## Language

**Filament 5 visual authority**:
The responsibility of `laravel-filament-5-ui-ux` to choose and compose Filament 5 interface patterns. `laravel-filament-v5` retains authority over version-matched APIs, security, implementation, and tests.
_Avoid_: Shared visual authority, generic frontend authority

**Official visual pattern**:
A Filament 5 presentation option evidenced by official documentation and screenshots, including component choice, composition, spacing, responsive behavior, and information hierarchy.
_Avoid_: Screenshot style, component example

**Visual option space**:
The set of official Filament 5 visual patterns that can plausibly satisfy a surface, user goal, data shape, and responsive context. The UI/UX skill must compare this set before selecting a pattern.
_Avoid_: Component list, design inspiration

**Visual pattern family**:
A decision-oriented grouping of official screenshots that share one presentation strategy while exposing meaningful variants, such as horizontal versus vertical tabs, contained versus uncontained sections, or desktop versus mobile table composition.
_Avoid_: Screenshot folder, component documentation page

**Pre-interpreted visual catalog**:
A three-layer Filament 5 knowledge asset: a complete raw screenshot inventory, decision-oriented visual pattern families, and individual variant records only where a visual difference changes pattern selection.
_Avoid_: Screenshot gallery, component API index

**Decision-changing variant**:
An official visual variation whose conditions, tradeoffs, or responsive behavior can change the selected composition, such as horizontal versus vertical tabs, contained versus uncontained layouts, or desktop versus mobile table arrangements.
_Avoid_: Cosmetic variation, duplicate screenshot

**Visual evidence**:
The official Filament 5 documentation page and relevant screenshot used to ground a UI/UX decision.
_Avoid_: Inspiration, visual guess

**Tiered visual evidence policy**:
Every UI task queries the pre-interpreted visual catalog. Building or materially restructuring a surface also requires inspecting at least one relevant official screenshot when image viewing is available. Small local changes may rely on the catalog interpretation and exact documentation. When direct inspection is unavailable, the agent discloses that limitation.
_Avoid_: Optional screenshot lookup, image inspection for every trivial edit

**Visual decision trace**:
A compact, externally observable record of the surface, user goal, official candidates, inspected visual evidence, selected pattern, and any justified escape hatch. Its detail scales from a one-line citation for a small change to a pre-implementation comparison for material composition work.
_Avoid_: Design rationale dump, screenshot summary

**Compact index** / **índice compacto**:
A generated Markdown projection of the reviewed Filament 5 visual catalog that lists pattern identifiers, surfaces, goals, responsive contexts, routed references, and evidence counts plus the controlled vocabulary per dimension. It is the primary offline selection path and must stay byte-identical to a fresh regeneration from `visual-catalog.json`.
_Avoid_: Hand-edited catalog summary, second source of truth

**Autonomous visual selection**:
The UI/UX skill compares the official visual option space and selects a supported pattern without asking the user to choose components. It asks only when an unresolved product decision would materially change the outcome.
_Avoid_: Component-selection interview, silent product assumption
