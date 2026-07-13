# Dev Skills

A collection of [Agent Skills](https://skills.sh) for AI coding assistants — Claude Code, Cursor, Windsurf, Copilot, and any tool that speaks the `SKILL.md` format.

Each skill lives in its own folder under [`skills/`](./skills), with a `SKILL.md` (loaded by the agent) and a `README.md` (for humans browsing GitHub or skills.sh).

## Available Skills

| Skill | Description | Install |
|---|---|---|
| [laravel-nova-5](./skills/laravel-nova-5) | Build version-matched Laravel Nova 5 features with official documentation, progressive references, authorization, and verification. | `npx skills add jotafurtado/dev-skills --skill laravel-nova-5` |
| [laravel-filament-v5](./skills/laravel-filament-v5) | Build Filament v5 admin panels with official components first — resources, infolists, forms, tables, actions, widgets, relation managers, testing, and UI composition. | `npx skills add jotafurtado/dev-skills --skill laravel-filament-v5` |
| [prepare-commit](./skills/prepare-commit) | Prepare atomic Git commits with Conventional Commits, host-safe staging, project-aware language, and CHANGELOG.md maintenance. | `npx skills add jotafurtado/dev-skills --skill prepare-commit` |
| [sdd-workflow](./skills/sdd-workflow) | Enforce a Spec-Driven Development pipeline (Requirements -> Design -> Tasks -> Grounded Execution) with versioned specs and phase-by-phase approval. | `npx skills add jotafurtado/dev-skills --skill sdd-workflow` |

## Install

Install a single skill:

```bash
npx skills add jotafurtado/dev-skills --skill <skill-name>
```

Or with Laravel Boost:

```bash
php artisan boost:add-skill jotafurtado/dev-skills --skill <skill-name>
```

Browse all skills in this repo interactively:

```bash
npx skills add jotafurtado/dev-skills
```

## Adding a New Skill

1. Create `skills/<skill-name>/SKILL.md` with YAML frontmatter (`name`, `description` are required — `description` is what triggers the skill, so make it specific).
2. Add a `skills/<skill-name>/README.md` for humans (what it does, install command, requirements).
3. Add a row to the table above.

## License

MIT
