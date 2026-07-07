# Dev Skills

A collection of [Agent Skills](https://skills.sh) for AI coding assistants — Claude Code, Cursor, Windsurf, Copilot, and any tool that speaks the `SKILL.md` format.

Each skill lives in its own folder under [`skills/`](./skills), with a `SKILL.md` (loaded by the agent) and a `README.md` (for humans browsing GitHub or skills.sh).

## Available Skills

| Skill | Description | Install |
|---|---|---|
| [laravel-nova-5](./skills/laravel-nova-5) | Build Laravel Nova 5 admin panels — resources, fields, actions, filters, lenses, metrics, dashboards. | `npx skills add jotafurtado/dev-skills --skill laravel-nova-5` |
| [laravel-filament-v5](./skills/laravel-filament-v5) | Build Filament v5 admin panels with official components first — resources, infolists, forms, tables, actions, widgets, relation managers, testing, and UI composition. | `npx skills add jotafurtado/dev-skills --skill laravel-filament-v5` |

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
