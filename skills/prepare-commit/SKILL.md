---
name: prepare-commit
description: "Prepares small Git commits with Conventional Commits messages in the language established by the user or project and keeps CHANGELOG.md up to date. Use when the user asks to commit, stage changes, write a commit message, follow Conventional Commits, or prepare changes for versioning."
license: MIT
compatibility: "Designed for Cursor, Claude Code, Windsurf, and Copilot; requires Git."
metadata:
  author: jotafurtado
  version: "1.1.0"
  domain: workflow
  role: specialist
  scope: implementation
  output-format: commit
  tags: "git, commit, conventional-commits, changelog, workflow"
---

# Prepare Commit

## Goal

Prepare small, reviewable, traceable commits using Conventional Commits 1.0.0, and keep `CHANGELOG.md` up to date when a change is notable to users, integrators, or operators.

Determine the commit language in this order: explicit user instruction, documented project convention, recent commit history, then Brazilian Portuguese as the fallback. Keep the subject, body, and footer values in that language; preserve required machine-readable tokens such as `BREAKING CHANGE` and keep type tokens consistent with the project. A request scoped to "this commit" does not change the project's default for future commits.

## Host Precedence and Portable Guarantees

The host agent's native protocols and current user instructions take precedence over this skill. Follow the host exactly for amend eligibility, failed or modifying hooks, push, permissions, allowed commands, and command execution. This skill narrows commit behavior; it never grants permission or overrides a more restrictive host protocol.

Portable guarantees:

- Never create a commit without an explicit user request. A request for a message, plan, preview, or staging alone does not authorize `git commit`.
- Never push without an explicit user request. A request to commit does not imply permission to push.
- Never change Git configuration, bypass hooks merely to make a commit pass, or use destructive history/worktree commands without explicit authorization and host support.
- Never stage secrets, credentials, private keys, dumps, tokens, local environment data, or unrelated changes.
- Preserve user and third-party work; do not revert, reformat, unstage, or reorganize it silently.
- Amend only when the host protocol allows it and all host preconditions hold. If the host has no amend protocol, require an explicit amend request and verify the target commit is local and unpushed. Never amend after a failed or rejected commit; create a new commit after fixing the cause. Amend hook-generated follow-up changes only when the host explicitly permits that case.
- Do not use interactive Git commands. In particular, never suggest or run `git add -p`.

## Flow

### 1. Inspect Changes

Run, in parallel when possible:

- `git status --short`
- `git diff`
- `git diff --cached`
- `git log --oneline -5`

Use this to identify:

- Modified, added, removed, and untracked files.
- Changes already staged before you got involved.
- Sensitive files that must not enter the commit.
- The repo's recent message style.
- The concern, likely type, scope, and exact paths for each possible commit.

If `git status --short` shows nothing at all — no staged, modified, or untracked files — tell the user there's nothing to commit instead of proceeding.

If changes were already staged before you got involved and they don't belong to the current request, ask the user whether to include them or leave them staged as-is. Don't unstage them and don't silently fold them into your commit message without confirming.

### 2. Define Scope

Pick a short scope when it helps locate the change:

- Technical area: `auth`, `api`, `ui`, `nova`, `filament`, `inertia`, `database`, `tests`.
- Business domain: use the affected module's name when the project has one.
- No scope: use when the change is cross-cutting, small, or has no clear owner.

Avoid generic scopes like `app`, `misc`, or `update`.

### 3. Generate the Message

Conventional Commits 1.0.0 requires the structure below. Only `feat` and `fix` have required semantic meanings; the specification permits additional types, which have no implicit SemVer effect unless they carry a breaking change. Prefer the project's established types; otherwise use this unified set:

| Type | Use |
| --- | --- |
| `feat` | Adds new functionality; maps to SemVer MINOR. |
| `fix` | Corrects a bug; maps to SemVer PATCH. |
| `docs` | Changes documentation only. |
| `style` | Changes formatting without changing behavior. |
| `refactor` | Restructures code without adding a feature or fixing a bug. |
| `perf` | Improves performance. |
| `test` | Adds or corrects tests only. |
| `build` | Changes build tooling, packaging, or dependencies. |
| `ci` | Changes continuous integration configuration or scripts. |
| `chore` | Performs maintenance not covered by a more specific type. |
| `revert` | Reverts an earlier commit; reference the reverted commit when useful. |

Projects may define other types. Use them only when project convention supports them; do not present the additional types above as requirements of Conventional Commits.

Format:

```text
<type>(<scope opcional>): <descrição>

<corpo opcional explicando o motivo>

<rodapé(s) opcional(is)>
```

Rules:

- The description must immediately follow `: `, be short, clear, and have no trailing period.
- Use the language selected in the Goal section consistently.
- Prefer explaining the "why" in the body when the change isn't obvious from the diff.
- Use `feat` only for new functionality.
- Use `fix` only for a behavior correction.
- Use `refactor` when the expected behavior doesn't change.
- Use `chore` for maintenance with no direct user impact.
- For a breaking change, use `!` after the type/scope (`feat(api)!: ...`) or a `BREAKING CHANGE: <explanation>` footer. Prefer both when migration guidance is useful. A breaking change may use any type and maps to SemVer MAJOR.

Examples:

```text
feat(filament): adiciona filtros por status aos relatórios
```

```text
fix(auth): corrige validação de sessão expirada

Evita redirecionamentos incorretos quando o token já foi invalidado.
```

### 4. Update CHANGELOG

First check whether `CHANGELOG.md` exists at the repo root, subject to the host's allowed read/edit operations. If it doesn't, skip this step; don't create one unprompted.

If it exists, update it when the change is relevant to users, operations, integration, API, public documentation, or observable behavior.

Don't update the changelog for purely internal changes — formatting, small test tweaks, local cleanup, or maintenance with no external impact — unless the user asks for it.

When updating:

- Read the existing format before editing.
- Preserve the language, order, and style already used in the file.
- Use the `## [Unreleased]` section when it exists.
- If it doesn't exist yet (but the file does), create `## [Unreleased]` in a place consistent with the file's structure.
- Classify entries by user-visible impact, not by commit type alone.

Use the existing structure when it intentionally differs. Otherwise follow Keep a Changelog's six categories:

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

Write entries in the same language as the rest of the changelog file, unless the user explicitly requested a different language for this commit — in that case, follow their request instead, even if it doesn't match the rest of the file. Example (default, Portuguese):

```markdown
- Adiciona filtros por status aos relatórios administrativos.
```

### 5. Validate

Before committing:

- Run tests, linters, or formatters only when the host protocol permits the required discovery and commands.
- When permitted, detect the project's own checks and run the smallest relevant non-interactive set. Do not assume a stack or broaden the diff with an unrestricted auto-fix.
- If the host restricts this workflow to Git inspection/commit commands, skip project checks rather than conflicting with that protocol. Report checks not run and why.
- Re-read `git diff` and `git diff --cached` to confirm only what should be included is included.

### 6. Stage and Commit Atomically

Split the work by concern before staging. For each concern, define its message and exact paths, then complete this loop before moving to the next:

1. Confirm the index has no pre-staged changes from another concern. If it does, stop and resolve according to the host protocol and user direction; never unstage silently.
2. Stage explicit paths only: `git add -- <path-1> <path-2>`.
3. Inspect the complete candidate commit with `git diff --cached --stat` and `git diff --cached`.
4. If the cached diff contains another concern, unrelated work, or sensitive data, do not commit. Adjust only through non-interactive operations allowed by the host, or ask the user how to proceed.
5. Run permitted checks for that concern, then inspect `git diff --cached` again if a check changed files.
6. Commit that concern, run `git status --short`, and repeat the loop for the next concern.

Never use `git add .`, `git add -A`, `git add -p`, or another interactive staging command. If separate concerns share the same file, path-based staging cannot split them atomically; ask the user to separate the file changes or approve one coherent commit instead of suggesting interactive staging.

Create the commit with a HEREDOC to preserve accents and line breaks:

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <descrição>

<corpo opcional>
EOF
)"
```

After the commit:

- Run `git status --short`.
- Report the short commit hash, the message used, and any check that passed or is still pending.
- Do not push unless the user explicitly requested it and the host protocol permits it.
