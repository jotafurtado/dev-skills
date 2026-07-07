# Prepare Commit

AI agent skill for preparing Git commits. Writes Conventional Commits messages in Brazilian Portuguese, keeps `CHANGELOG.md` up to date when the change warrants it, and follows a strict safety flow (never commits without an explicit request, never runs destructive Git commands, never stages secrets).

## Install

```bash
npx skills add jotafurtado/dev-skills --skill prepare-commit
```

Or with Laravel Boost:

```bash
php artisan boost:add-skill jotafurtado/dev-skills --skill prepare-commit
```

## What's Covered

- Inspecting `git status`/`git diff` to classify the change type and scope
- Conventional Commits messages, descriptions in Brazilian Portuguese by default
- `CHANGELOG.md` maintenance — only when the file already exists and the change is externally relevant
- Detecting and running the project's own formatter/linter before committing (not hardcoded to one stack)
- Safe staging (no blind `git add .`) and commit via HEREDOC to preserve accents/line breaks

## Requirements

- A Git repository
- No specific language/framework — works on any stack

## License

MIT
