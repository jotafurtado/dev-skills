# Domain Docs

How the engineering skills should consume this repository's domain documentation.

## Before exploring, read these

- `CONTEXT.md` at the repository root.
- `CONTEXT-MAP.md` instead, if one is introduced later.
- Relevant ADRs under `docs/adr/`.

If these files do not exist, proceed silently. Domain documentation is created lazily as terminology and architectural decisions are resolved.

## File structure

This is a single-context repository:

```text
/
├── CONTEXT.md
├── docs/
│   └── adr/
└── skills/
```

## Use the glossary's vocabulary

Use terminology defined in `CONTEXT.md`. Avoid synonyms explicitly rejected by the glossary.

If a needed concept is absent, reconsider whether it belongs to the project vocabulary or record the gap for the domain-modeling workflow.

## Flag ADR conflicts

If proposed work contradicts an existing ADR, identify the conflict explicitly instead of silently overriding the decision.
