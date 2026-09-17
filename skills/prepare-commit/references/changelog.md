# Changelog updates

When Step 4 finds an existing root `CHANGELOG.md`, read this reference before deciding whether an entry is relevant. Resolve the entry language only through [Preflight in `SKILL.md`](../SKILL.md#preflight).

## Relevance

Update the changelog when the change is relevant to users, operations, integration, API, public documentation, or observable behavior.

Don't update the changelog for purely internal changes — formatting, small test tweaks, local cleanup, or maintenance with no external impact — unless the user asks for it.

## Format and Unreleased

When updating:

- Read the existing format before editing.
- Preserve intentional structure, headings, order, style, and bullet conventions. A language instruction for a new entry does not authorize translating historical entries or reorganizing the file.
- Use the existing unreleased section and its heading. If absent, add one consistent with the file's structure; use `## [Unreleased]` above the latest release when no custom convention applies.
- Write concise entries describing user impact.
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

## Entry examples

Match the language resolved for the changelog sink in Preflight of `SKILL.md`:

```markdown
### Added
- Stripe webhook signature validation for checkout events.
```

```markdown
### Fixed
- Handle expired refresh tokens gracefully during session restoration.
```
