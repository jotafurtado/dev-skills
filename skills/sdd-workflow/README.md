# SDD Workflow

Portable Agent Skill for Kiro-inspired Spec-Driven Development. It creates
numbered, versioned specifications, supports the official Feature and Bugfix
workflow variants, and executes tasks only from approved or explicitly generated
artifacts with traceability and verification.

Current version: **2.0.0**

## Install

```bash
npx skills add jotafurtado/dev-skills --skill sdd-workflow
```

Or with Laravel Boost:

```bash
php artisan boost:add-skill jotafurtado/dev-skills --skill sdd-workflow
```

## Invocation behavior

The skill remains available for automatic invocation, but its description is
intentionally narrow. It should activate only when the user explicitly mentions
SDD, Kiro-style specs, spec-driven development, avoiding vibe coding, writing a
spec, or planning before implementation. Ordinary feature, refactor, and bug
requests do not trigger it.

It can always be invoked manually with `/sdd-workflow`.

## Workflow modes

- **Feature — Requirements-First:** `requirements.md → design.md → tasks.md`,
  with approval after requirements and design.
- **Feature — Design-First:** HLD or LLD `design.md → requirements.md → tasks.md`,
  with approval after design and requirements.
- **Quick Plan:** asks blocking questions up front, then generates all three
  artifacts without intermediate gates.
- **Bugfix Spec:** `bugfix.md → design.md → tasks.md`, preserving current,
  expected, and unchanged behavior.

Implementation starts only when the current user request authorizes it. Tasks
may run individually or as all required incomplete tasks.

## What's Covered

- Mandatory sequential identifiers such as `001-user-authentication` and
  `002-payment-reconciliation`.
- Persistent workflow state, approvals, revisions, and hashes in `spec.yaml`.
- EARS acceptance criteria with stable traceability IDs.
- Optional correctness properties and property-based testing where appropriate.
- Dependency-aware required/optional tasks with observable outcomes and checks.
- Resume, invalidation, synchronization, per-task evidence, and final
  convergence against acceptance criteria.
- Host precedence and explicit execution authorization.

## Artifact location

Artifacts are stored in a project-root directory:

```text
sdd-specs/
└── 001-user-authentication/
    ├── spec.yaml
    ├── requirements.md   # or bugfix.md
    ├── design.md
    └── tasks.md
```

The numeric prefix is monotonic and never reused or renumbered. The workflow
scans existing immediate child directories, increments the highest prefix, and
uses at least three digits.

## Structure

```
sdd-workflow/
├── SKILL.md
└── references/
    ├── requirements-template.md
    ├── bugfix-template.md
    ├── design-template.md
    ├── tasks-template.md
    └── spec-state-template.yaml
```

References are loaded only for the active phase.

## Kiro fidelity and portable extensions

The modes, artifact names, EARS semantics, approval gates, Bugfix behavior, and
optional PBT guidance follow the official Kiro documentation. The following are
intentional portable extensions:

- `sdd-specs/` instead of `.kiro/specs/`;
- `spec.yaml` for state normally held by the Kiro product UI;
- explicit numbering, content hashes, invalidation, and host-neutral execution
  rules.

The exact Markdown headings and metadata are this skill's schema, not Kiro
requirements.

## Requirements

- No specific language/framework — works on any stack
- A repository where `sdd-specs/` can be versioned
- Best suited to work that benefits from durable planning rather than
  chat-ephemeral implementation

## Official references

- [Kiro Specs](https://kiro.dev/docs/specs/)
- [Feature Specs](https://kiro.dev/docs/specs/feature-specs/)
- [Requirements-First](https://kiro.dev/docs/specs/feature-specs/requirements-first/)
- [Design-First](https://kiro.dev/docs/specs/feature-specs/tech-design-first/)
- [Quick Plan](https://kiro.dev/docs/specs/quick-plan/)
- [Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs/)
- [Analyze Requirements](https://kiro.dev/docs/specs/analyze-requirements/)
- [Correctness with Property-Based Tests](https://kiro.dev/docs/specs/correctness/)
- [Cursor Agent Skills](https://cursor.com/docs/skills)

## License

MIT
