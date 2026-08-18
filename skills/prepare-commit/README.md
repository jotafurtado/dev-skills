# Prepare Commit

AI agent skill for preparing small Git commits. It writes Conventional Commits 1.0.0 messages in the language established by the user or project, keeps an existing `CHANGELOG.md` up to date when a change is notable, and defers to the host agent's native Git and permission protocols.

Current version: **1.4.1**

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
- Language for each sink (commit message, changelog entry) selected from user instruction, project convention, the existing artefact for that sink, then Brazilian Portuguese as fallback
- When a root `CHANGELOG.md` exists, routes to `references/changelog.md` for relevance, Keep a Changelog classification (including breaking changes, deprecations, removals, and security fixes), and entry format
- Atomic concern-by-concern staging with explicit paths and full cached-diff review; no interactive staging
- Flags untracked files that look like `.gitignore` candidates (env files, IDE metadata, build output, OS artifacts, logs) before staging anything
- Project tests, linters, and formatters discovered once in validation, then reused per concern when staging
- Portable safeguards: no commit or push without the corresponding explicit request, no secret staging, and no silent alteration of unrelated work
- Optional `--push` flag: pushes once after all of the run's commits, still bound by host push permissions, and never force-pushes

## Invocation Behavior

The frontmatter intentionally omits `disable-model-invocation`. Cursor therefore may load this skill automatically when a request clearly concerns committing, which is its primary use case. It can still be invoked manually with `/prepare-commit`. Staging during implementation, git inspection, and PR text are not triggers.

## Requirements

- A Git repository
- No specific language/framework — works on any stack

## Standards

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [Cursor Agent Skills](https://cursor.com/docs/skills)
- [Agent Skills specification](https://agentskills.io/)

## License

MIT
