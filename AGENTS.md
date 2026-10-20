# dev-skills — authoring conventions

This repo is a collection of [Agent Skills](https://skills.sh) (`SKILL.md` format), one per folder under `skills/`, distributed by committing here and installing globally via `npx skills`. There is no per-project synced copy to keep in step. When you create or edit a skill, follow the conventions below.

## Content and tone

- **Write skill content in English** — `SKILL.md` and every file under `references/`. (A skill may still *produce* output in another language when that is its documented behavior or configured by user/project conventions.)
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

- This repo is MIT. **Only build from officially-licensed sources.** Never copy text from an unlicensed project; its architecture may inspire, its text may not be copied.

## Versioning and releases

- **Each skill is versioned independently** through `metadata.version` in its `SKILL.md` frontmatter, following SemVer. The collection itself has no version.
- **Every version bump gets a `CHANGELOG.md` entry** at the repo root, headed `## <skill>@<version> - YYYY-MM-DD`, written in pt-BR in Keep a Changelog sections (`Adicionado`, `Alterado`, `Corrigido`, `Removido`).
- **Every new version gets a Git tag and a GitHub release** named `<skill>@<version>`, created after the bump commit is pushed: `gh release create <skill>@<version> --title "<skill>@<version>" --notes "<that version's CHANGELOG entry>"`. Never move or reuse an existing tag.

## Adding a new skill

See the "Adding a New Skill" section in `README.md` for the mechanics (create the folder, write `SKILL.md` + `README.md`, add a row to the README table).

---

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- When graphify-out/graph.json exists, run `graphify query "<question>"` before your first grep, search or source-file read for a codebase question, and put this rule in every subagent prompt that explores code. Read raw files only for lines the graph or an earlier read already located. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
