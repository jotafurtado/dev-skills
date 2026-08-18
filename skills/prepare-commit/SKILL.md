---
name: prepare-commit
description: "Prepares small atomic Git commits with Conventional Commits messages in the language established by the user or project, stages by concern, and updates an existing CHANGELOG.md when the change is notable. Use when the user asks to commit, prepare a commit, write or revise a commit message, follow Conventional Commits for a commit, or commit and push. Do not trigger on git status, diff, log, or blame alone; PR or merge-request text; rebase, merge, or cherry-pick; version bumps or releases; changelog-only edits; or an isolated mention of Conventional Commits without intent to commit. Staging files during implementation without a commit request is not a trigger."
license: MIT
metadata:
  compatibility: "Designed for Cursor, Claude Code, Windsurf, and Copilot; requires Git."
  author: jotafurtado
  version: "1.4.1"
  domain: workflow
  role: specialist
  scope: implementation
  output-format: commit
  tags: "git, commit, conventional-commits, changelog, workflow"
---

# Prepare Commit

## Preflight

Determine the language for each written sink — the commit message and, when applicable, a changelog entry — in this order:

1. Explicit user instruction. Note whether it is scoped to this run or changes the project default. A request scoped to "this commit" does not change the project's default for future commits.
2. Documented project convention.
3. The existing artefact for the sink being written: recent commit history for the commit message; the changelog file for a changelog entry.
4. Brazilian Portuguese as the fallback.

Because step 3 is sink-specific, a Portuguese commit message paired with an English changelog entry (or the reverse) is a deliberate outcome when those artefacts disagree and no higher rule unifies them. Keep the subject, body, footer values, and changelog prose in the language selected for that sink; preserve required machine-readable tokens such as `BREAKING CHANGE` and keep type tokens consistent with the project.

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
| An existing root `CHANGELOG.md` that may need an entry | `references/changelog.md` |

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
- Untracked files that look like they belong in `.gitignore` instead of in a commit.
- The repo's recent message style.
- The concern, likely type, scope, and exact paths for each possible commit.

If `git status --short` shows nothing at all — no staged, modified, or untracked files — tell the user there's nothing to commit instead of proceeding.

If changes were already staged before you got involved and they don't belong to the current request, ask the user whether to include them or leave them staged as-is. Don't unstage them and don't silently fold them into your commit message without confirming.

If untracked files match common gitignore candidates — env files beyond a checked-in example (`.env`, `.env.local`), IDE/editor metadata (`.idea/`, `.vscode/`), build or dependency output (`dist/`, `build/`, `vendor/`, `node_modules/`), OS artifacts (`.DS_Store`, `Thumbs.db`), or log files — flag them to the user before staging anything and suggest adding a `.gitignore` entry. Do not add or edit `.gitignore` yourself unless asked, and never stage these files to fulfill the request.

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
- Use the language selected in Preflight consistently for this sink.
- Prefer explaining the "why" in the body when the change isn't obvious from the diff.
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

Check whether `CHANGELOG.md` exists at the repo root. If it does not, skip this step and do not create one unprompted. If it does, read `references/changelog.md` and follow it.

### 5. Validate

Before committing, discover which project checks apply to this run:

- Detect the project's own tests, linters, or formatters and run the smallest relevant non-interactive set. Do not assume a stack or broaden the diff with an unrestricted auto-fix.
- If no usable checks are found, or a discovered check cannot be run, report what was skipped and why.
- Re-read `git diff` and `git diff --cached` to confirm only what should be included is included.

Step 5 owns check discovery for the run. Step 6 reuses that discovered set for per-concern verification after staging; it does not rediscover checks.

### 6. Stage and Commit Atomically

Split the work by concern before staging. For each concern, define its message and exact paths, then complete this loop before moving to the next:

1. Confirm the index has no pre-staged changes from another concern. If it does, stop and ask the user how to proceed; never unstage silently.
2. Stage explicit paths only: `git add -- <path-1> <path-2>`.
3. Inspect the complete candidate commit with `git diff --cached --stat` and `git diff --cached`.
4. If the cached diff contains another concern, unrelated work, or sensitive data, do not commit. Adjust only through non-interactive operations, or ask the user how to proceed.
5. Run the checks discovered in Step 5 for that concern, then inspect `git diff --cached` again if a check changed files.
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
