# Tasks Template (Reference)

The Tasks artifact (Phase 3) must be extremely methodical and procedural. It is the track the "Grounded Execution" phase runs on.

## Structuring Rules

- Checklists using `- [ ]`.
- "Incremental" development order — preferably from the domain core (Enums/DTOs) -> Interfaces/Services -> Adapters -> Presentation/Screens.

## Sample Structure

```markdown
- [ ] 1. Domain Foundation
    - [ ] 1.1 Create [Enum/DTO] with attributes x, y, z (_Requirements: 1.1_)
    - [ ] 1.2 Write a property/unit test for [Enum/DTO] (Property X)

- [ ] 2. Checkpoint — Foundation Validation
    - Stop execution, run tests if applicable, and confirm the initial infrastructure exists correctly. Ask for verification.

- [ ] 3. Application Layer / Services
    - [ ] 3.1 Create ServiceX with Y injected.
    - [ ] 3.2 Write corresponding Feature Tests (Property Z).

- [ ] 4. Checkpoint — Core Logic Validation
    - Stop execution, test the service, fix bugs before touching the UI.

- [ ] 5. Frontend / Screen Integration
    - [ ] 5.1 Update the Controller or Filament/Inertia Action
```

> **Warning:** Every code sub-task MUST reference a Requirement number or Correctness Property described in the Requirements and Design artifacts. When a Correctness Property has no PBT tooling to verify it, the sub-task still references it — just via a unit/integration test instead of a property-based one.
