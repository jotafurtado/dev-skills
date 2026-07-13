# Feature Requirements Template

Use for `requirements.md` in Requirements-First, Design-First, and Quick Plan
feature specs. The contract is semantic: capture what and why without embedding
implementation decisions that belong in `design.md`.

Kiro uses EARS-style behavior such as:

```text
WHEN [condition or event]
THE SYSTEM SHALL [expected behavior]
```

Use the user's language while preserving stable IDs.

## Structure

```markdown
# Requirements: [Spec title]

## 1. Summary

[Purpose, user/business value, and concise context.]

## 2. Scope

### In scope

- [Behavior or outcome included.]

### Out of scope

- [Explicit exclusion that prevents scope drift.]

## 3. Context and dependencies

- **Actors:** [Users or systems.]
- **Dependencies:** [External services, existing capabilities, or none.]
- **Assumptions:** [Assumption that must be validated.]
- **Constraints:** [Regulatory, compatibility, performance, or operational.]

## 4. Glossary

[Include only when domain terms are ambiguous. Omit the section otherwise.]

## 5. Functional requirements

### REQ-001 — [Requirement name]

**User story:** As a [actor], I want [capability], so that [value].

#### Acceptance criteria

- **AC-001:** **WHEN** [condition/event], **THE SYSTEM SHALL** [observable behavior].
- **AC-002:** **IF** [exception/edge case], **THEN THE SYSTEM SHALL** [observable alternative].

### REQ-002 — [Requirement name]

[Repeat with globally unique AC IDs.]

## 6. Non-functional requirements

- **NFR-001 — [Quality]:** [Measurable security, performance, reliability,
  accessibility, compatibility, privacy, or operability requirement.]

[Omit this section only when no non-functional requirement is material.]

## 7. Edge cases

- **EDGE-001:** [Boundary or unusual scenario and expected behavior.]

## 8. Open questions

- **Q-001:** [Unresolved question, owner, and blocking/non-blocking status.]

[Write "None" when all questions are resolved.]
```

## Authoring rules

- Keep `REQ-*`, `AC-*`, `NFR-*`, `EDGE-*`, and `Q-*` IDs stable after creation.
- Acceptance criteria describe externally observable behavior and must be
  testable. Avoid class names, database tables, libraries, or implementation
  steps unless they are an explicit constraint.
- EARS is required for event/condition-driven system behavior. Plain declarative
  statements are acceptable for static constraints and non-functional
  requirements.
- Use universal language such as `FOR ALL` only when the behavior is genuinely
  invariant across an input domain. That may become a correctness property in
  `design.md`, but it does not automatically require property-based testing.
- Resolve blocking open questions before approval.
- Every acceptance criterion and material NFR must be referenced by at least one
  task and one verification method before execution completes.

## Optional requirements analysis

For complex, regulated, security-sensitive, or Quick Plan work, analyze the
draft before approval:

1. Find ambiguous terms and unmeasurable statements.
2. Find conflicting constraints or acceptance criteria.
3. Identify undeclared assumptions and missing edge cases.
4. Confirm scope exclusions and non-functional requirements.
5. Update the artifact transparently and increment its revision in `spec.yaml`.
