# Prepare Commit

AI agent skill for preparing small Git commits. It writes Conventional Commits 1.0.0 messages in the language established by the user or project, keeps an existing `CHANGELOG.md` up to date when a change is notable, and defers to the host agent's native Git and permission protocols.

Current version: **1.2.0**

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
- Message language selected from user instruction, project convention, recent history, then Brazilian Portuguese as fallback
- Keep a Changelog categories, including breaking changes, deprecations, removals, and security fixes
- Atomic concern-by-concern staging with explicit paths and full cached-diff review; no interactive staging
- Flags untracked files that look like `.gitignore` candidates (env files, IDE metadata, build output, OS artifacts, logs) before staging anything
- Project tests, linters, and formatters only when the host permits their discovery and execution
- Portable safeguards: no commit or push without the corresponding explicit request, no secret staging, and no silent alteration of unrelated work

## Invocation Behavior

The frontmatter intentionally omits `disable-model-invocation`. Cursor therefore may load this skill automatically when a request clearly concerns staging or committing, which is its primary use case. It can still be invoked manually with `/prepare-commit`.

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
