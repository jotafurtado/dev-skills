# Maintainer assets outside the install payload

Status: Accepted, amends ADR-0002

## Context

ADR-0002 retained `screenshot-inventory.json` as the discovery asset that identifies uncovered official patterns. That decision settled whether the inventory survives. It did not settle where the file lives, and the install-payload cost was never weighed.

`npx skills add <repo> --skill laravel-filament-v5-ui-ux --copy` copies the entire skill directory. Under that contract, a maintainer asset stored in `references/` reaches every consuming agent's disk even though no composition links to it and no consuming agent reads it at use time. Its only readers are release-time tools: the synchronizer that writes it, the composition validator's coverage gate, and the deterministic tests.

The discovery role is real, and it is a maintainer's role. Keeping that role while leaving the file under `skills/` conflates installed modules with release machinery.

## Decision

Move `screenshot-inventory.json` out of the skill install payload to `maintenance/filament-ui-ux/screenshot-inventory.json` at the repository root.

Draw a seam between installed modules and maintainer assets: content under `skills/` is what the installer ships; maintainer-only discovery and coverage data live outside that tree. ADR-0002's retention of the inventory stands; only its location is amended.

## Consequences

- The coverage gate keeps working from the new path; an official pattern in the inventory without a reference composition remains tracked as an uncovered pattern.
- `references/` becomes exclusively reference compositions plus the release-verification note — no JSON.
- Release tooling now spans two roots: composition files under the skill, and the screenshot inventory under `maintenance/`.
