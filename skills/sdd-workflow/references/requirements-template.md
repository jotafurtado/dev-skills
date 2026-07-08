# Requirements / BDD Template (Reference)

The Requirements artifact (Phase 1) must follow a formal structure, limiting scope to tangible business rules. It must adopt Ubiquitous Language and Acceptance Criteria based on "SHALL/WHEN/IF".

## Mandatory Structure

### 1. Introduction

Brief summary of the module or feature's purpose, its vital integrations, and macro scope.

### 2. Glossary

Definition of the domain's key terms, to eliminate ambiguity.

### 3. Business Requirements (Epics / Details)

For each major function, create a block containing the User Story and its Criteria.

#### Example Structure:

### Requirement 1: [Requirement Name]

**User Story:** As a [Actor], I want [Action / Feature], so that [Business Goal — Value].

#### Acceptance Criteria

Use formal grammar and binding, affirmative sentences. Make systemic conditions explicit to guarantee precision and testability (with a focus on Property-Based Testing whenever possible).

1. **WHEN** [context/action], **THE** [System/Service] **SHALL** [required action / calculation].
2. **IF** [edge case/exception], **THEN THE** [System/Service] **SHALL** [alternative path].
3. **FOR ALL** [elements of a list/tree], the [result] **SHALL** [guaranteed universal behavior].

> **SDD Tip:** Each acceptance criterion of a requirement must later be traceable to a test-execution Task.
