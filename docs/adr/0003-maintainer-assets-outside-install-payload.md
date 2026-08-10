# Maintainer assets outside the install payload

Status: Accepted, amends ADR-0002

## Context

ADR-0002 retained `screenshot-inventory.json` as the discovery asset that identifies uncovered official patterns. That decision settled whether the inventory survives. It did not settle where the file lives, and the install-payload cost was never weighed.

`npx skills add <repo> --skill laravel-filament-v5-ui-ux --copy` copies the entire skill directory. Under that contract, a maintainer asset stored in `references/` reaches every consuming agent's disk even though no composition links to it and no consuming agent reads it at use time. Its only readers are release-time tools: the synchronizer that writes it, the composition validator's coverage gate, and the deterministic tests.

The discovery role is real, and it is a maintainer's role. Keeping that role while leaving the file under `skills/` conflates installed modules with release machinery.

## Decision

Draw a seam between installed modules and maintainer assets: content under `skills/` is what the installer ships, and everything whose only reader is a maintainer lives outside that tree.

Move to `maintenance/` at the repository root:

- `screenshot-inventory.json`, the discovery asset
- the release scripts: composition validation, Filament API verification, inventory synchronization, and the clean-install smoke test
- the release-verification note, which documents those gates
- `validate_skill.mjs`, which validates any skill in the repository and was reachable only through one skill's directory

ADR-0002's retention of the inventory stands; only its location is amended.

## Consequences

- The coverage gate keeps working from the new path; an official pattern in the inventory without a reference composition remains tracked as an uncovered pattern.
- `references/` becomes exclusively reference compositions.
- Maintainer tooling lives in one root. Release commands gain a longer path, and scripts that derive paths from their own location compute them from the repository root instead of a skill root.
- `validate_skill.mjs` becomes visibly repository-wide. Housing it under one skill is why two other skills carried non-conforming frontmatter undetected.
