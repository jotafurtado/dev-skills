# Reference compositions over evidence lookup

Status: Accepted, supersedes ADR-0001, amended by ADR-0003

## Context

ADR-0001 built `laravel-filament-v5-ui-ux` as a decision procedure: a queryable catalog of official screenshots, a controlled vocabulary, a mandatory evidence workflow, and an observable decision trace. The result inverted the intended cost. Roughly 11,300 lines of apparatus — a 622-screenshot inventory, a 22-pattern catalog, and a query engine — produced 338 lines of guidance and no usable Filament code, while the sibling skill `laravel-filament-v5` shipped 45 pasteable PHP blocks in 1,625 lines.

The controlled vocabulary reached 106 terms indexing 22 answers. The forward evaluation scored 84 of 88 assertions as passing, but most assertions verified that the agent narrated a comparison and declared a delegation, not that it composed a correct interface. A full rerun was cancelled on token cost.

## Decision

`laravel-filament-v5-ui-ux` becomes a browsable library of reference compositions instead of a decision procedure.

The skill ships ready-to-adapt Filament 5 code in two layers: a complete composition per official visual pattern, plus named variants that modify it. It is consulted when building or restructuring a surface, presents the options that fit, and helps choose. It imposes no mandatory workflow, no runtime screenshot inspection, and no decision trace.

The authority boundary moves from "selection versus implementation" to **surface composition versus field API, security, and tests**. Where both skills describe the same component, `laravel-filament-v5` states that the component exists and what its signature is; `laravel-filament-v5-ui-ux` states how it is arranged within a surface.

Provenance moves inside each composition as the documentation and screenshot URLs it was derived from. `visual-catalog.json` is retired. `screenshot-inventory.json` survives as the discovery asset that identifies uncovered patterns.

Verification replaces narrative evaluation with PHP syntax linting on every composition, and a Composer fixture resolving the target Filament version as the release gate.

## Considered Options

Merging the two skills was rejected. The overlap is real, but a single skill of roughly 2,263 lines would lose the narrow trigger that determines whether a skill loads at the right moment, and the two bodies of content answer different questions.

Emitting pseudo-code while preserving ADR-0001's boundary was rejected as a restatement of the original defect.

## Consequences

- The runtime query engine and its controlled vocabulary are removed, along with the tests that exercise them.
- Narrative forward evaluations are discontinued; passing them measured dialect fluency rather than correctness.
- Emitting code exposes the skill to Filament API drift, which the Composer fixture gate is intended to catch.
- Coverage becomes measurable: patterns present in the inventory without a reference composition are tracked as expansion work.
