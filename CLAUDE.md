# dev-skills — authoring conventions

This repo is a collection of [Agent Skills](https://skills.sh) (`SKILL.md` format), one per folder under `skills/`, distributed by committing here and installing globally via `npx skills`. There is no per-project synced copy to keep in step. When you create or edit a skill, follow the conventions below.

## Content and tone

- **Write skill content in English** — `SKILL.md` and every file under `references/`. (A skill may still *produce* output in another language when that is its documented behavior, e.g. `prepare-commit` writes pt-BR commit messages.)
- **No decorative emojis** in skill files. Use plain words: `Don't` / `Do`, `Never` / `Always` — not check/cross marks.
- Keep prose dense and instructional. Prefer concrete rules and examples over general advice.

## Structure

- **`SKILL.md` holds the behavioral core** — the decision flow, gates, and routing. Keep it focused; push detail into references.
- **`references/` is one level deep and loaded on demand.** SKILL.md routes to a reference file only when the task needs it. Don't inline a whole reference's worth of detail into SKILL.md.
- Each skill ships two entry points: `SKILL.md` (loaded by the agent) and `README.md` (for humans browsing GitHub / skills.sh).
- The frontmatter `description` is what triggers the skill — make it specific, with few false positives. State both when to use and when NOT to use it.

## Accuracy

- **Ground every API signature in official docs or source — never from memory.** Prefer the docs' `.md` variant (clean markdown) and the version-matched branch source when doc prose is ambiguous about a signature.
- **Match the installed version.** Have the skill read the project's manifest (`composer.json`, `package.json`, lockfiles) instead of pinning versions in the skill text.
- **Avoid absolute rules where the framework admits more than one valid solution.** Reserve `Never` / `Always` for genuine constraints.

## Licensing

- This repo is MIT. **Only build from officially-licensed sources.** Never copy text from an unlicensed project (e.g. `ulpi-io/skills` has no license — architecture may inspire, text may not be copied).

## Adding a new skill

See the "Adding a New Skill" section in `README.md` for the mechanics (create the folder, write `SKILL.md` + `README.md`, add a row to the README table).
