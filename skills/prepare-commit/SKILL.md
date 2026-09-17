---
name: prepare-commit
description: "Prepares small atomic Git commits with Conventional Commits messages in the language established by the user or project, stages by concern, and updates an existing CHANGELOG.md when the change is notable. Use when the user asks to commit, prepare a commit, write or revise a commit message, follow Conventional Commits for a commit, or commit and push. Do not trigger on git status, diff, log, or blame alone; PR or merge-request text; rebase, merge, or cherry-pick; version bumps or releases; changelog-only edits; or an isolated mention of Conventional Commits without intent to commit. Staging files during implementation without a commit request is not a trigger."
license: MIT
metadata:
  compatibility: "Designed for Cursor, Claude Code, Codex, Windsurf, Copilot, Cline, Roo Code, and any Agent Skills-compatible harness; requires Git."
  author: jotafurtado
  version: "1.5.0"
  domain: workflow
  role: specialist
  scope: implementation
  output-format: commit
  tags: "git, commit, conventional-commits, changelog, workflow"
---

# Prepare Commit

## Preflight

Determine the language independently for each written sink — the commit message and, when applicable, a changelog entry — using this precedence order, subject to the host's higher-priority instructions:

1. **Applicable explicit user instruction**, respecting its scope and duration. A request scoped to "this commit" does not change the project's default for future commits.
2. **Documented project convention**, such as `CONTRIBUTING.md` or a style guide. Documentation takes precedence over conflicting artifact history.
3. **Existing artifact for that sink**: recent commit history (`git log --oneline -10`) for the commit message; the root `CHANGELOG.md` for a changelog entry.
4. **Current conversation language**.
5. **Fallback**: English.

Resolve each sink separately; its language does not automatically carry over to the other sink. The message and changelog entry may use different languages when no higher-precedence instruction or convention unifies them. Keep subject, body, footer values, and changelog prose in their resolved language; preserve required machine-readable tokens such as `BREAKING CHANGE` and keep type tokens (`feat`, `fix`, etc.) in English as required by Conventional Commits.

## Gates

The host agent's native protocols and current user instructions take precedence over this skill. Follow the host exactly for amend eligibility, failed or modifying hooks, push, permissions, allowed commands, and command execution. This skill narrows commit behavior; it never grants permission or overrides a more restrictive host protocol.

Flow steps describe portable operations. Whether the host allows a given operation is resolved at this seam, not re-derived in each step.

Portable guarantees:

- Never create a commit without an explicit user request. A request for a message, plan, preview, or staging alone does not authorize `git commit`.
- Never push without an explicit user request. A request to commit does not imply permission to push. A `--push` flag (or equivalent explicit phrasing, e.g. "and push") on the invocation counts as that request for the commits produced in this run only; it does not carry over to future invocations.
- Never change Git configuration, bypass hooks merely to make a commit pass, or use destructive history/worktree commands without explicit authorization and host support.
- Never stage secrets, credentials, private keys, dumps, tokens, local environment data, or unrelated changes.
- Preserve user and third-party work; do not revert, reformat, unstage, or reorganize it silently.
- Amend only when the host protocol allows it and all host preconditions hold. If the host has no amend protocol, require an explicit amend request and verify the target commit is local and unpushed. Never amend after a failed or rejected commit; create a new commit after fixing the cause. Amend hook-generated follow-up changes only when the host explicitly permits that case.
- Do not use interactive Git commands. In particular, never suggest or run `git add -p`.

## Reference routing

| Task touches | Read |
| --- | --- |
| Step 4 finds an existing root `CHANGELOG.md` | Must read [references/changelog.md](references/changelog.md) before deciding whether an entry is relevant |

## Flow

### 1. Inspect Changes

Run, in parallel when possible:

- `git status --short`
- `git diff`
- `git diff --cached`
- `git log --oneline -10`

Use this to identify:

- Modified, added, removed, and untracked files.
- Changes already staged before you got involved.
- Sensitive files that must not enter the commit.
- Untracked files that look like they belong in `.gitignore` instead of in a commit.
- The repo's established commit message convention and language.
- The concern, likely type, scope, and exact paths for each possible commit.

If `git status --short` shows nothing at all — no staged, modified, or untracked files — tell the user there's nothing to commit instead of proceeding.

If changes were already staged before you got involved and they don't belong to the current request, ask the user whether to include them or leave them staged as-is. Don't unstage them and don't silently fold them into your commit message without confirming.

If untracked files match common gitignore candidates — environment files beyond checked-in examples (`.env`, `.env.local`, `.env.*`), IDE/editor metadata (`.idea/`, `.vscode/`), build or dependency output (`dist/`, `build/`, `target/`, `vendor/`, `node_modules/`), OS artifacts (`.DS_Store`, `Thumbs.db`), or log files (`*.log`) — flag them to the user before staging anything and suggest adding a `.gitignore` entry. Do not add or edit `.gitignore` yourself unless asked, and never stage these files to fulfill the request.

### 2. Define Scope

Pick a short, meaningful scope when it helps locate the change within the codebase:

- **Technical layers**: `api`, `auth`, `ui`, `cli`, `db`, `core`, `config`, `deps`.
- **Domain modules**: the affected application module or bounded context (e.g., `billing`, `notifications`, `search`, `users`, `orders`).
- **No scope**: use when the change is cross-cutting, repo-wide, small, or has no single distinct owner.

Avoid vague or generic scopes such as `app`, `misc`, `code`, or `update`.

### 3. Generate the Message

Conventional Commits 1.0.0 provides a universal, language- and framework-agnostic structure. Only `feat` and `fix` have required semantic meanings; additional types have no implicit SemVer effect unless they carry a breaking change. Prefer the project's established types; otherwise use this standard set:

| Type | Use |
| --- | --- |
| `feat` | Adds new functionality; maps to SemVer MINOR. |
| `fix` | Corrects a bug; maps to SemVer PATCH. |
| `docs` | Changes documentation only. |
| `style` | Changes formatting without changing behavior. |
| `refactor` | Restructures code without adding a feature or fixing a bug. |
| `perf` | Improves performance. |
| `test` | Adds or corrects tests only. |
| `build` | Changes build tooling, packaging, external dependencies, or manifests. |
| `ci` | Changes continuous integration configurations or workflows. |
| `chore` | Performs maintenance not covered by a more specific type. |
| `revert` | Reverts an earlier commit; reference the reverted commit when useful. |

Projects may define other types. Use them only when project convention supports them; do not present the additional types above as requirements of Conventional Commits.

Format:

```text
<type>(<optional-scope>): <description>

<optional body explaining the rationale and context>

<optional footer(s)>
```

Rules:

- The description must immediately follow `: `, be short, imperative, and have no trailing period.
- Use the language resolved in Preflight consistently for the commit sink.
- Explain the "why" in the body when the reason is not self-evident from the diff.
- For a breaking change, use `!` after the type/scope (`feat(api)!: ...`) or a `BREAKING CHANGE: <explanation>` footer. Prefer both when migration guidance is useful. A breaking change may use any type and maps to SemVer MAJOR.

Examples:

```text
feat(billing): add stripe webhook signature validation

Validate incoming webhook payloads against the signing secret before processing checkout events.
```

```text
fix(auth): handle expired refresh tokens gracefully

Clear local session state and redirect to login when token rotation fails.
```

```text
refactor(core): decouple event dispatcher from logger

Allows pluggable logger implementations without modifying event dispatch logic.
```

```text
perf(db): add composite index on orders (user_id, created_at)
```

```text
feat(api)!: drop deprecated v1 endpoints

BREAKING CHANGE: The /api/v1 endpoints have been removed. Migrate consumers to /api/v2.
```

### 4. Update CHANGELOG

Check whether `CHANGELOG.md` exists at the repo root. If absent, skip this step without loading the reference or creating the file unless the user explicitly requests its creation.

If it exists, you must read [references/changelog.md](references/changelog.md) before deciding whether to add an entry. Follow that reference for relevance, structure, and classification, using the entry language resolved in Preflight.

### 5. Validate

Before staging and committing, discover applicable checks from the project's scripts, configuration, and CI, accounting for available tools and versions. Manifests guide this discovery; their presence does not authorize a stock command, tool, or policy flag.

- Select the smallest sufficient set for the touched files or packages. It may require tests, lint, and typecheck together; do not stop at one command when other configured checks cover distinct risks.
- Run non-interactively. Never execute long-running whole-repository test suites when scoped checks suffice.
- Prefer read-only/check-only modes supported by the configured tools. Never let linters or formatters silently rewrite files outside the commit scope.
- If no checks are configured or a configured check is unavailable, report what was skipped and why. If an executed check fails, report the failure as such, not as a skip or a pass. Follow the host's failure protocol before proceeding.

Step 5 owns discovery and selection for the run. Step 6 runs the applicable subset for each concern after staging, without rediscovering checks.

### 6. Stage and Commit Atomically

Split the work by concern before staging. For each concern, define its message and exact paths, then complete this loop before moving to the next:

1. Confirm the index has no pre-staged changes from another concern. If it does, stop and ask the user how to proceed; never unstage silently.
2. Stage explicit paths only: `git add -- <path-1> <path-2>`.
3. Inspect the complete candidate commit with `git diff --cached --stat` and `git diff --cached`.
4. If the cached diff contains another concern, unrelated work, or sensitive data, do not commit. Adjust only through non-interactive operations, or ask the user how to proceed.
5. Run the checks discovered in Step 5 for that concern, then inspect `git diff --cached` again if a check changed files.
6. Commit that concern using the host-permitted literal message transport below, run `git status --short`, and repeat the loop for the next concern.

Never use `git add .`, `git add -A`, `git add -p`, or another interactive staging command. If separate concerns share the same file, path-based staging cannot split them atomically; ask the user to separate the file changes or approve one coherent commit instead of suggesting interactive staging.

#### Literal Commit Message Transport

Choose a host-permitted method that treats the subject, body, and footers as data, preserving Unicode, quotes, dollar signs, backticks, and intentional paragraph breaks:

1. **Prefer direct process arguments (argv)** when the host API supports them without a shell. Pass the complete message as one `-m` value, or use multiple `-m` values for separate paragraphs. Git joins repeated `-m` values as paragraphs; this does not make an interpolated shell command string safe. Keep footers that belong together in the same paragraph.
2. **Otherwise, use a temporary message file** through host-permitted operations. Create a unique file outside the staging paths, write the complete message literally as UTF-8 without a BOM, and pass its path to `git commit -F`. Protect the path as one argument using the actual shell's quoting rules or the process API's argument handling. Arrange cleanup before attempting the commit: remove only the temporary file you created on both success and failure.

For either method, use `--cleanup=verbatim` to preserve the intended message rather than relying on Git's configurable cleanup defaults (see [git-commit](https://git-scm.com/docs/git-commit)). Git's usual final line-terminator normalization is not message corruption. Hook behavior remains subject to the Gates.

No quoting recipe is universally safe across shells. If the host cannot provide literal transport and, for the file method, controlled encoding and cleanup, report the limitation before creating a commit; do not substitute a lossy or shell-interpreted message.

### 7. Push (only when requested)

Recognize `--push` or equivalent explicit phrasing as the push authorization required by the portable guarantees above.

- Push once, after every commit in the current run has been created — not after each individual commit inside the Step 6 loop.
- Never force-push. If the push is rejected (e.g., the remote has diverged), report the error and ask the user how to proceed instead of retrying with `--force`.

## Verify

After each commit:

- Report the short commit hash, the message used, and any check that passed or is still pending.

After the run:

- Report remaining staged, unstaged, or untracked files.
- Push only per Step 7. If pushed, report the branch, remote, and commit hashes.
