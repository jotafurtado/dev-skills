# Design Template (Reference)

The Design artifact (Implementation Plan — Phase 2) defines *how* the code will fulfill the Requirements' specifics — it is the Architecture blueprint. It serves as the guide the Tasks will be literally traced from.

## Mandatory Structure

### 1. Overview & Design Decisions

Technical summary of what will be built (or what will NOT be built — e.g. "We will not create new tables, only Models/DTOs"). Include the rationale, numbered.

### 2. Architecture

Mandatory use of **Mermaid** diagrams to express data flows (sequence diagrams) or components (graphs).

### 3. Components and Interfaces

Tables and code blocks with quick "sketches" of signatures (interfaces, service constructor signatures with injected dependencies, DTO/Enum signatures).

> **Rule:** Do not write the code implementation, only the signatures — the plan must stay focused on abstractions.

### 4. Data Models (Database Modeling)

Table design (required migrations), or, if not a database entity, the mapping of the transiting JSON structure.

### 5. Correctness Properties

The differentiator for Property-Based Tests.
*Definition:* A property that must remain immutably true throughout the system's execution, regardless of inputs.
Example: "Property 1: SV = EV - PV (Validates: Requirements 1.1)". Define at least the key properties to be tested for the architecture.

Properties must be defined regardless of the stack's testing tooling. If the project has no Property-Based Testing library available, keep the properties here and note in section 7 (Testing Strategy) that they will be verified through targeted unit/integration tests instead — the property is a design invariant, not a testing-library feature.

### 6. Error Handling

A matrix (table) of which anomalies can occur and how to handle them without crashing the system or polluting the logs.

### 7. Testing Strategy

State whether Unit Tests, Integration Tests, or Property-Based Tests will be used, mapping which requirements are checked by which Mock/Test files.
