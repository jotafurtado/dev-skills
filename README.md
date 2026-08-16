# Jota Furtado Dev Skills

A collection of [Agent Skills](https://skills.sh) for AI coding assistants — Claude Code, Cursor, Windsurf, Copilot, and any tool that speaks the `SKILL.md` format.

Each skill lives in its own folder under [`skills/`](./skills), with a `SKILL.md` (loaded by the agent) and a `README.md` (for humans browsing GitHub or skills.sh).

## Available Skills

| Skill | Description | Install |
|---|---|---|
| [laravel-nova-5](./skills/laravel-nova-5) | Build version-matched Laravel Nova 5 features with official documentation, progressive references, authorization, and verification. | `npx skills add jotafurtado/dev-skills --skill laravel-nova-5` |
| [laravel-filament-v5](./skills/laravel-filament-v5) | Build Filament v5 admin panels with official components first — resources, infolists, forms, tables, actions, widgets, relation managers, security, and tests. | `npx skills add jotafurtado/dev-skills --skill laravel-filament-v5` |
| [laravel-filament-v5-ui-ux](./skills/laravel-filament-v5-ui-ux) | Ready-to-adapt Filament 5 compositions for tables, forms, record details, dashboards, panel shells, and action feedback — pasteable code with official provenance. | `npx skills add jotafurtado/dev-skills --skill laravel-filament-v5-ui-ux` |
| [prepare-commit](./skills/prepare-commit) | Prepare atomic Git commits with Conventional Commits, host-safe staging, project-aware language, and CHANGELOG.md maintenance. | `npx skills add jotafurtado/dev-skills --skill prepare-commit` |
| [sdd-workflow](./skills/sdd-workflow) | Run Kiro-inspired Requirements-First, Design-First, Quick Plan, and Bugfix specs with sequential IDs, persistent state, and verified execution. | `npx skills add jotafurtado/dev-skills --skill sdd-workflow` |
| [implement-with-subagents](./skills/implement-with-subagents) | Orchestrate parallel `/implement` waves over the ready-for-agent frontier with isolated workers and orchestrator-owned review/commit. | `npx skills add jotafurtado/dev-skills --skill implement-with-subagents` |

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
