# Laravel Nova 5 Skill

Coding-agent skill for implementing and reviewing confirmed Laravel Nova 5
projects with official, versioned APIs.

Version: **2.0.0**

## Install

```bash
npx skills add jotafurtado/dev-skills --skill laravel-nova-5
```

Or with Laravel Boost:

```bash
php artisan boost:add-skill jotafurtado/dev-skills --skill laravel-nova-5
```

## Activation and safety

The skill activates for explicit Laravel Nova signals such as `laravel/nova`,
Nova resources, fields, actions, metrics, dashboards, or tools. A generic
“admin panel” or “back-office” request does not activate it. Filament code is
routed to a Filament-specific skill.

Before producing Nova code, the agent must read both `composer.json` and
`composer.lock` and confirm that `laravel/nova` resolves to version 5.x. It then
uses Nova's official documentation index and the relevant v5 page:

- <https://nova.laravel.com/docs/llms.txt>
- <https://nova.laravel.com/docs/v5/installation.md>
- <https://laravel.com/docs>
- <https://cursor.com/docs/skills>

Undocumented signatures are not guessed.

## Coverage

- Resources, fields, panels, tabs, validation, and repeaters
- Relationships, relatable queries, pivot fields, and relationship policies
- Nova access gates, policy defaults, Nova-specific policies, and visibility
- File storage, metadata, validation, downloads, and deletion
- Actions, queues, batching, filters, and lenses
- Value, Trend, Partition, Progress, and Table metrics
- Default and custom dashboards
- Tools, resource tools, cards, custom fields/filters, menus, and notifications
- Localization, assets, search, stubs, and impersonation
- Proportional Laravel-compatible testing without fabricated Nova helpers

## Structure

```text
laravel-nova-5/
├── SKILL.md
├── README.md
└── references/
    ├── resources.md
    ├── fields.md
    ├── relationships.md
    ├── authorization.md
    ├── files.md
    ├── actions-and-filters.md
    ├── metrics-and-dashboards.md
    ├── customization.md
    └── testing.md
```

All references are one level below `SKILL.md` for progressive loading.

## Compatibility

This skill targets Nova 5.x. Nova's current official installation documentation
lists Composer 2 and Laravel 10.x through 13.x, plus frontend requirements for
custom Nova packages. The installed Composer lockfile and generated Nova
scaffolds remain the source of truth for each project.

## License

MIT
