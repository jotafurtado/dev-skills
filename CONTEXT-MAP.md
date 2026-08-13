# Context Map

## Contexts

- [Dev Skills (Filament / publishing)](./CONTEXT.md) — glossary for Filament 5 skills and how this repo publishes agent skills
- [Implement with subagents](./skills/implement-with-subagents/CONTEXT.md) — parallel ticket implementation orchestrated across subagents

## Relationships

- **Dev Skills → Implement with subagents**: authoring conventions in `AGENTS.md` and the root README apply when publishing the skill; domain terms for orchestration live only in the skill context
- **Implement with subagents → Matt Pocock skills**: depends at runtime on installed `/implement`, `/tdd`, and `/code-review`; does not own or patch those skills
