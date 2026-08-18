# Changelog updates

Load this reference only when `CHANGELOG.md` exists at the repo root. For entry language, follow the shared ladder in Preflight of `SKILL.md` — do not apply a separate language rule here.

## Relevance

Update the changelog when the change is relevant to users, operations, integration, API, public documentation, or observable behavior.

Don't update the changelog for purely internal changes — formatting, small test tweaks, local cleanup, or maintenance with no external impact — unless the user asks for it.

## Format and Unreleased

When updating:

- Read the existing format before editing.
- Preserve the order and style already used in the file.
- Use the `## [Unreleased]` section when it exists.
- If it doesn't exist yet (but the file does), create `## [Unreleased]` in a place consistent with the file's structure.
- Classify entries by user-visible impact, not by commit type alone.

Use the existing structure when it intentionally differs. Otherwise follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)'s six categories:

| Change | Section | Rule |
| --- | --- | --- |
| `feat` | `### Added` | New user-visible capability. |
| `fix` | `### Fixed` | User-visible bug fix, except vulnerability fixes. |
| Vulnerability fix | `### Security` | Use regardless of commit type; avoid exposing exploit details. |
| Deprecation | `### Deprecated` | Announce functionality that will be removed and provide an alternative. |
| Removal | `### Removed` | State what was removed and the migration path when relevant. |
| Breaking change | `### Changed` or `### Removed` | Make the break and migration explicit; use `Removed` when removal is the cause. |
| `perf` | `### Changed` | Include only when the improvement is observable or operationally relevant. |
| `docs` | Existing custom documentation section or `### Changed` | Include only notable public-documentation changes; otherwise omit. |
| `revert` | Category matching its effect | Describe the user-visible restoration or withdrawal. |
| `refactor`, `style`, `test`, `build`, `ci`, `chore` | Usually no entry | These are normally internal. Use `### Changed`, `### Fixed`, or `### Security` only when the actual effect is notable externally. |

## Entry example

Example (default Portuguese sink from the shared ladder):

```markdown
- Adiciona filtros por status aos relatórios administrativos.
```
