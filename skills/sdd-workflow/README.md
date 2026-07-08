# SDD Workflow

AI agent skill that enforces Spec-Driven Development: a mandatory 4-phase pipeline (Requirements -> Design -> Tasks -> Grounded Execution), inspired by the Kiro IDE, that runs before code is touched on new features, structural refactors, or complex bugs. Each phase produces a versioned markdown artifact under `specs/{feature-name}/` and pauses for explicit user approval before moving to the next phase — killing "vibe coding" in favor of documented, traceable, incremental delivery.

## Install

```bash
npx skills add jotafurtado/dev-skills --skill sdd-workflow
```

Or with Laravel Boost:

```bash
php artisan boost:add-skill jotafurtado/dev-skills --skill sdd-workflow
```

## What's Covered

- Phase 1 — Requirements: ubiquitous-language glossary, user stories, WHEN/SHALL/IF acceptance criteria geared toward Property-Based Testing
- Phase 2 — Design: mandatory Mermaid architecture diagrams, interface/signature sketches (no implementation code), data modeling, Correctness Properties, error-handling matrix, testing strategy
- Phase 3 — Tasks: incremental checklist (domain core -> services -> adapters -> presentation) with checkpoints and explicit Requirement/Property traceability
- Phase 4 — Grounded Execution: implementation strictly bound to the approved Design/Tasks, a live checklist, and a "stop on anomaly" rule instead of silent workarounds
- Reference templates defining the exact structure for each artifact

## Structure

```
sdd-workflow/
├── SKILL.md                                # Always loaded: the 4-phase pipeline and golden rules
└── references/                             # Loaded on demand per phase
    ├── requirements-template.md            # Structure for requirements.md
    ├── design-template.md                  # Structure for design.md
    └── tasks-template.md                   # Structure for tasks.md
```

## Requirements

- No specific language/framework — works on any stack
- Best suited to projects that want physically saved, versioned specs rather than chat-ephemeral plans

## License

MIT
