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

## Maintenance

Repository-level maintainer commands:

```bash
npm ci
node maintenance/validate_skill.mjs skills/<skill-name>
python3 maintenance/eval_skills.py validate-datasets
python3 maintenance/eval_skills.py run --judge mock --out maintenance/evals-out
python3 maintenance/eval_skills.py run --judge description --out maintenance/evals-out
```

`--judge mock` is a simulated offline CI check, not evidence of agent quality. `--judge description` is a deterministic lexical activator, not a model benchmark. `--judge live` calls an OpenAI-compatible chat endpoint and is skipped as `missing_credentials` unless `EVAL_SKILLS_API_KEY`, `OPENAI_API_KEY`, or `OPENROUTER_API_KEY` is set (`EVAL_SKILLS_BASE_URL` and `EVAL_SKILLS_MODEL` optional; OpenRouter defaults to `google/gemini-3.5-flash-lite`). Live output evaluations use isolated prompts, not a tool-enabled coding agent; proposed code is not proof of executed tests.

```bash
EVAL_SKILLS_API_KEY=... \
EVAL_SKILLS_BASE_URL=https://openrouter.ai/api/v1 \
EVAL_SKILLS_MODEL=google/gemini-3.5-flash-lite \
python3 maintenance/eval_skills.py run --judge live --out maintenance/evals-out/live-run
```

Use `--output-only` for a candidate-versus-baseline output run without trigger repetitions. Use `--skill <name>` to scope a run. Each run writes per-case grading and timing, one benchmark per skill, and a repository summary. Fixture bytes and the base instruction are identical across variants; the candidate additionally receives the complete skill and matching references. Malformed JSON, incomplete grading, fabricated quotes, and truncated completions are infrastructure/protocol skips, not skill failures. `--gate` fails an all-skipped live bucket and genuine candidate failures, not baseline failures.

The live grader selects assertion IDs and inclusive output-line ranges. The harness copies those lines verbatim into `grading.json`, rather than asking the model to reproduce PHP backslashes or evidence text. IDs, ranges, boolean types, completeness, and duplicates are validated. Quote existence does not prove semantic correctness; review disputed grades in their full output context.

The live adapter allows up to 8,192 answer tokens, 2,048 selection tokens, and 4,096 grading tokens. Available provider token counts are persisted; missing telemetry stays null. Keep generated artifacts outside `skills/` and use a new output directory for each comparable run.

The dated [release closure](docs/research/release-closure-2026-10-04.md) records the current versions, exercised checks, live artifacts, and disputed model grades. Do not treat raw model scores as certified quality metrics.

Skill-specific verification (for example Filament composition checks) is documented in each skill's README.

The frontmatter validator uses the `yaml` package from `package-lock.json`. It accepts standard YAML scalars and mappings, validates metadata types, and explicitly permits the boolean `disable-model-invocation` client extension. Install maintainer dependencies with `npm ci`; they are not part of installed skills.

## License

MIT
