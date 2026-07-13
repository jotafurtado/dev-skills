# Technical Design Template

Use for `design.md`. In Requirements-First and Bugfix modes, derive it from the
approved behavior artifact. In Design-First, choose and record one level:

- **HLD:** system boundaries, components, interactions, architecture patterns,
  and non-functional decisions.
- **LLD:** contracts, algorithms, data structures, state transitions, and
  implementation-level pseudocode.

Do not write production implementation during the design phase. Signatures and
pseudocode are allowed when they clarify contracts.

## Structure

```markdown
# Design: [Spec title]

## 1. Design context

- **Mode:** [Requirements-First | Design-First HLD | Design-First LLD |
  Quick Plan | Bugfix]
- **Source:** [requirements.md revision/hash, bugfix.md revision/hash, or the
  technical brief and project evidence used for Design-First]
- **Current constraints:** [Stack, compatibility, policy, operational limits.]
- **Bugfix root-cause evidence:** [For Bugfix only: affected code paths,
  reproduction/trace evidence, and confirmed root cause.]

## 2. Overview

[Technical approach and the boundaries of this design.]

## 3. Design decisions

### DEC-001 — [Decision]

- **Choice:** [Selected approach.]
- **Rationale:** [Why it satisfies linked requirements.]
- **Alternatives considered:** [Alternatives and rejection reasons.]
- **Traceability:** [REQ/AC/NFR/BUG-AC IDs.]

## 4. Architecture and flows

[Describe components and interactions. Add Mermaid only when a diagram makes a
relationship, sequence, state transition, or data flow materially clearer.]

## 5. Components and interfaces

### [Component]

- **Responsibility:** [Single responsibility.]
- **Inputs/outputs:** [Contracts.]
- **Dependencies:** [Required collaborators.]
- **Traceability:** [Requirement or bugfix IDs.]

[Use signature sketches or pseudocode for LLD when useful; no implementation.]

## 6. Data and state

[Include only when persisted data, messages, schemas, migrations, caches, or
state transitions change. Describe compatibility and migration strategy.]

## 7. Correctness properties

### PROP-001 — [Invariant]

- **Statement:** For all [valid inputs/states], [property that remains true].
- **Validates:** [AC/NFR/BUG-AC IDs.]
- **Verification:** [PBT, unit, integration, model check, or manual evidence.]

[Include only genuine invariants. Write "No universal properties identified"
when example-based tests are more appropriate.]

## 8. Failure handling and observability

[For material failure modes, define detection, response, retry/idempotency,
logging/metrics, and user-visible behavior. A table is optional.]

## 9. Security, privacy, and performance

[Include applicable threat boundaries, authorization, sensitive data,
performance budgets, concurrency, or state "No material change".]

## 10. Testing strategy

[Map each AC/NFR/BUG-AC and PROP to the narrowest suitable automated or manual
verification. PBT is optional and used only for suitable universal properties.]

## 11. Rollout and migration

[Include only when deployment order, feature flags, backfills, compatibility,
or rollback matters.]

## 12. Open risks and questions

- **RISK-001:** [Risk, likelihood/impact, mitigation, owner.]
- **Q-001:** [Unresolved design question.]
```

## Authoring rules

- Keep decision, property, risk, and requirement references stable.
- Every design decision must trace to approved behavior or an explicit
  constraint.
- Use Mermaid, data modeling, and failure matrices conditionally, not as
  decorative mandatory sections.
- Do not invent framework APIs. Inspect the project and use version-matched
  official documentation for external systems.
- In Design-First mode, requirements derived later must remain compatible with
  the approved design. If they reveal a contradiction, return to design
  approval instead of forcing feasibility.
- In Bugfix mode, inspect the codebase and confirm or disprove the root-cause
  hypothesis before approving a corrective design.
- Resolve blocking risks/questions before tasks are generated.
