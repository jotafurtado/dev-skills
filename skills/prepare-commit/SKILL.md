---
name: prepare-commit
description: "Prepares Git commits with Conventional Commits messages in Brazilian Portuguese and keeps CHANGELOG.md up to date. Use when the user asks to commit, stage changes, write a commit message, follow Conventional Commits, or prepare changes for versioning."
license: MIT
compatible_agents:
  - Claude Code
  - Cursor
  - Windsurf
  - Copilot
tags:
  - git
  - commit
  - conventional-commits
  - changelog
  - workflow
metadata:
  author: jotafurtado
  version: "1.0.0"
  domain: workflow
  role: specialist
  scope: implementation
  output-format: commit
---

# Prepare Commit

## Goal

Prepare small, reviewable, traceable commits using Conventional Commits, and keep `CHANGELOG.md` up to date when a change has meaningful impact on the product, API, integration, operations, or public documentation.

Commit message language: **Brazilian Portuguese by default.** Only write commit messages in another language if the user explicitly says so for that project or that commit.

## Safety Rules

- Never create a commit without an explicit request from the user.
- If the user asks only for a message, a plan, or a preview, do not run `git add` or `git commit`.
- Never change Git configuration.
- Never use destructive commands such as `git reset --hard`, `git checkout --`, `git clean`, rebase, or force push without explicit approval.
- Always create a new commit rather than amending an existing one, unless the user explicitly asks for `--amend`.
- If a pre-commit hook fails, don't bypass it with `--no-verify`. Fix the underlying issue, re-stage, and create a new commit.
- Never stage files that contain secrets, credentials, or local environment data — `.env`, private keys, dumps, tokens, credential files.
- Preserve unrelated changes made by the user. Don't revert, reformat, or reorganize files outside the scope of the commit.
- If third-party changes are mixed into the same file, understand the context before editing or staging.

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
- The main type of change: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, or `revert`.

If `git status --short` shows nothing at all — no staged, modified, or untracked files — tell the user there's nothing to commit instead of proceeding.

If changes were already staged before you got involved and they don't belong to the current request, ask the user whether to include them or leave them staged as-is. Don't unstage them and don't silently fold them into your commit message without confirming.

### 2. Define Scope

Pick a short scope when it helps locate the change:

- Technical area: `auth`, `api`, `ui`, `nova`, `filament`, `inertia`, `database`, `tests`.
- Business domain: use the affected module's name when the project has one.
- No scope: use when the change is cross-cutting, small, or has no clear owner.

Avoid generic scopes like `app`, `misc`, or `update`.

### 3. Generate the Message

Use Conventional Commits, with the description in Brazilian Portuguese:

```text
<type>(<scope>): <descrição em português>

<corpo opcional explicando o motivo>
```

Rules:

- The description should be short, imperative or descriptive, no trailing period.
- Write it in clear Portuguese.
- Prefer explaining the "why" in the body when the change isn't obvious from the diff.
- Use `feat` only for new functionality.
- Use `fix` only for a behavior correction.
- Use `refactor` when the expected behavior doesn't change.
- Use `chore` for maintenance with no direct user impact.
- For a breaking change, mark it with `!` after the type/scope (`feat(api)!: ...`) and add a `BREAKING CHANGE: <explanation>` footer describing what breaks and, when relevant, how to migrate.

Examples:

```text
feat(filament): adiciona filtros por status aos relatórios
```

```text
fix(auth): corrige validação de sessão expirada

Evita redirecionamentos incorretos quando o token já foi invalidado.
```

### 4. Update CHANGELOG

First check whether `CHANGELOG.md` exists at the repo root. If it doesn't, **skip this step** — don't create one unprompted; a changelog is a deliberate project decision, not something to introduce as a side effect of a commit.

If it exists, update it when the change is relevant to users, operations, integration, API, public documentation, or observable behavior.

Don't update the changelog for purely internal changes — formatting, small test tweaks, local cleanup, or maintenance with no external impact — unless the user asks for it.

When updating:

- Read the existing format before editing.
- Preserve the language, order, and style already used in the file.
- Use the `## [Unreleased]` section when it exists.
- If it doesn't exist yet (but the file does), create `## [Unreleased]` in a place consistent with the file's structure.
- Classify entries into sections compatible with the existing pattern.

Default mapping:

- `feat` -> `### Added`
- `fix` -> `### Fixed`
- `refactor`, `perf`, `style` -> `### Changed`
- Removals -> `### Removed`
- `docs` -> `### Documentation` if that section already exists; otherwise `### Changed`

Write entries in the same language as the rest of the changelog file, for example:

```markdown
- Adiciona filtros por status aos relatórios administrativos.
```

### 5. Validate

Before committing:

- Run tests or minimal checks proportional to the change.
- Check whether the project has a configured formatter/linter and run it scoped to the changed files when possible — e.g. `vendor/bin/pint --dirty --format agent` if `vendor/bin/pint` exists, or the project's own lint/format script (`package.json` scripts, `Makefile`, etc.). Don't assume a specific tool; detect what the project actually uses.
- If tests or formatters can't be run, tell the user why.
- Re-read `git diff` and `git diff --cached` to confirm only what should be included is included.

### 6. Stage and Commit

Stage only the files relevant to this commit. Avoid `git add .` when there are unrelated changes or sensitive files present.

If the diff spans more than one unrelated concern (e.g. a bug fix mixed with an unrelated refactor), propose splitting it into separate commits instead of writing one commit that mixes both — smaller, single-purpose commits are the point of this skill.

Create the commit with a HEREDOC to preserve accents and line breaks:

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <descrição em português>

<corpo opcional>
EOF
)"
```

After the commit:

- Run `git status --short`.
- Report the short commit hash, the message used, and any check that passed or is still pending.
