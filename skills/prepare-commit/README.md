# Prepare Commit

AI agent skill for preparing small Git commits. It writes Conventional Commits 1.0.0 messages in the language established by the user or project, keeps an existing `CHANGELOG.md` up to date when a change is notable, and defers to the host agent's native Git and permission protocols.

Current version: **1.5.0**

## Install

```bash
npx skills add jotafurtado/dev-skills --skill prepare-commit
```

Or with Laravel Boost:

```bash
php artisan boost:add-skill jotafurtado/dev-skills --skill prepare-commit
```

## What's Covered

- Host precedence for amend, hooks, push, permissions, and allowed commands
- Conventional Commits types: `feat` and `fix` have specification-defined semantics; additional project types are supported
- Independent language selection for commit messages and changelog entries through Preflight: applicable explicit user instruction, documented project convention, the destination's existing artifact, conversation language, then English
- Language- and framework-agnostic scopes across technical layers (`api`, `auth`, `ui`, `cli`, `db`, `core`) and domain modules (`billing`, `notifications`, `search`)
- Conditional changelog maintenance: a root `CHANGELOG.md` requires loading the [changelog reference](references/changelog.md) before deciding whether an entry is needed; absent changelogs are not created unless requested
- One authority for changelog relevance and organization: the reference preserves intentional project formats and uses Keep a Changelog as the default, with entry language resolved by Preflight
- Project-derived checks from actual scripts, configuration, and CI: the smallest sufficient non-interactive set for the affected work, with unavailable checks distinguished from failures
- Literal multiline message transport permitted by the host: direct Git arguments preferred, otherwise a UTF-8 temporary file without a BOM; no universal shell-quoting guarantee
- Atomic concern-by-concern staging with explicit paths and full cached-diff review; no interactive staging
- Flags untracked files that look like `.gitignore` candidates (env files, IDE metadata, build output, OS artifacts, logs) before staging anything
- Portable safeguards: no commit or push without the corresponding explicit request, no secret staging, and no silent alteration of unrelated work
- Optional `--push` flag: pushes once after all of the run's commits, still bound by host push permissions, and never force-pushes
## Invocation Behavior

The frontmatter intentionally omits `disable-model-invocation`. Compatible agent harnesses (Cursor, Claude Code, Codex, Windsurf, Copilot, Cline, Roo Code, etc.) may load this skill automatically when a request clearly concerns committing, which is its primary use case. It can also be invoked manually with `/prepare-commit`. Staging during implementation, git inspection, and PR text are not triggers.

## Requirements

- A Git repository
- No specific language/framework — works on any stack

## Standards

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [Cursor Agent Skills](https://cursor.com/docs/skills)
- [Agent Skills specification](https://agentskills.io/)

## Maintenance

```bash
npm ci
node maintenance/validate_skill.mjs skills/prepare-commit
python3 maintenance/eval_skills.py validate-datasets
python3 maintenance/eval_skills.py run --judge mock --out maintenance/evals-out
```

## License

MIT
