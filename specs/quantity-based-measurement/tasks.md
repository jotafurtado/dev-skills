# Implementation Plan: Método de Medição por Unidades Concluídas (Quantity-Based)

## Overview

This plan implements the fifth measurement method — **Unidades Concluídas** (`quantity_based`) — extending the existing measurement-tracking module. The implementation proceeds incrementally: enum → migration → model validations → service logic → factories → Filament form → Blade UI → property tests. Each step builds on the previous, ensuring no orphaned code.

## Tasks

- [x]   1. Add `QuantityBased` case to `MeasurementMethod` enum
    - Add `case QuantityBased = 'quantity_based'` to `app/Enums/MeasurementMethod.php`
    - Add label `"Unidades Concluídas"` in `getLabel()`, color `"primary"` in `getColor()`, icon `Heroicon::OutlinedCubeTransparent` in `getIcon()`
    - _Requirements: 1.1, 1.2, 1.3_

- [x]   2. Create migration for quantity fields
    - Create a migration that adds `planned_quantity` (unsignedInteger, nullable) and `unit_cost` (decimal(15,2), nullable) to `wbs_nodes` table after `assigned_to`
    - Add `quantity_completed` (unsignedInteger, nullable) to `measurements` table after `completed_milestones`
    - Run the migration to verify it applies cleanly
    - _Requirements: 2.3, 2.6, 3.6_

- [x]   3. Extend `WbsNode` model with quantity-based validation
    - [x] 3.1 Add `planned_quantity` and `unit_cost` to `$fillable` and `$casts` in `app/Models/WbsNode.php`
        - Cast `planned_quantity` as `integer` and `unit_cost` as `decimal:2`
        - _Requirements: 2.3, 2.6_
    - [x] 3.2 Add `validateQuantityBasedConfig()` method and wire into `booted()` creating/updating hooks
        - When `measurement_method = quantity_based`: `planned_quantity` is required, must be integer > 0
        - `unit_cost`, when present, must be numeric > 0 with at most 2 decimal places
        - When `measurement_method != quantity_based`: skip quantity field validation entirely
        - Throw `InvalidArgumentException` with pt-BR messages matching the design's error table
        - _Requirements: 2.1, 2.2, 2.4, 2.5, 2.8, 2.9_
    - [x] 3.3 Write property test: Quantity-based configuration validation (Property 1)
        - **Property 1: Quantity-based configuration validation**
        - Use `repeat(100)` with Faker to generate random `planned_quantity` values (positive, zero, negative, null)
        - Verify acceptance for positive integers, rejection for zero/negative/null when method is `quantity_based`
        - **Validates: Requirements 2.1, 2.2, 2.9**
    - [x] 3.4 Write property test: Unit cost validation (Property 2)
        - **Property 2: Unit cost validation**
        - Use `repeat(100)` with Faker to generate random `unit_cost` values (positive, zero, negative, many decimal places)
        - Verify acceptance for positive values with ≤ 2 decimal places, rejection otherwise
        - **Validates: Requirements 2.5**
    - [x] 3.5 Write property test: Quantity fields ignored for non-quantity-based methods (Property 3)
        - **Property 3: Quantity fields ignored for non-quantity-based methods**
        - Use `repeat(100)` with Faker to generate WPs with non-quantity_based methods and random `planned_quantity`/`unit_cost`
        - Verify all configurations are accepted regardless of quantity field values
        - **Validates: Requirements 2.8**

- [x]   4. Extend `Measurement` model with quantity-completed validation
    - [x] 4.1 Add `quantity_completed` to `$fillable` and `$casts` in `app/Models/Measurement.php`
        - Cast `quantity_completed` as `integer`
        - _Requirements: 3.6_
    - [x] 4.2 Add `validateQuantityCompleted()` and `validateQuantityMonotonicity()` methods, wire into `booted()` creating/updating hooks
        - When `measurement_method = quantity_based`: `quantity_completed` is required, must be integer >= 0, must be <= `wbsNode.planned_quantity`
        - Monotonicity: `quantity_completed` must be >= previous measurement's `quantity_completed` for the same WP
        - When `measurement_method != quantity_based`: skip quantity_completed validation
        - Throw `InvalidArgumentException` with pt-BR messages matching the design's error table
        - _Requirements: 3.2, 3.3, 4.1, 4.2_
    - [x] 4.3 Write property test: Quantity completed bounds validation (Property 5)
        - **Property 5: Quantity completed bounds validation**
        - Use `repeat(100)` with Faker to generate `(quantity_completed, planned_quantity)` pairs
        - Verify acceptance for 0 ≤ qty ≤ planned_quantity, rejection otherwise
        - **Validates: Requirements 3.2, 3.3**
    - [x] 4.4 Write property test: Quantity completed monotonicity (Property 6)
        - **Property 6: Quantity completed monotonicity (non-regression)**
        - Use `repeat(100)` to generate sequences of `quantity_completed` values
        - Verify that regression (new < previous) is rejected with correct error message
        - **Validates: Requirements 4.1, 4.2**

- [x]   5. Checkpoint — Ensure all model validation tests pass
    - Ensure all tests pass, ask the user if questions arise.

- [x]   6. Extend `EvCalculationService` with quantity-based calculation
    - [x] 6.1 Add `calculateQuantityBasedPercent(WbsNode $wp, int $quantityCompleted): float` method
        - Returns `round(($quantityCompleted / $wp->planned_quantity) * 100, 2)`
        - _Requirements: 3.4_
    - [x] 6.2 Extend `recordMeasurement()` to accept optional `?int $quantityCompleted` parameter
        - When method is `quantity_based`: calculate `percentComplete` via `calculateQuantityBasedPercent()`, persist `quantity_completed` in the measurement record
        - Pass `quantity_completed` to the `updateOrCreate` data array
        - Wrap in existing `DB::transaction()`
        - _Requirements: 3.4, 3.5, 3.7, 3.8_
    - [x] 6.3 Write property test: Quantity-based measurement calculation (Property 4)
        - **Property 4: Quantity-based measurement calculation**
        - Use `repeat(100)` with Faker to generate valid `(quantity_completed, planned_quantity, BAC)` triples
        - Verify `percent_complete = round((qty / planned) × 100, 2)` and `earned_value = round(BAC × (qty / planned), 2)`
        - **Validates: Requirements 3.4, 3.5, 3.7**
    - [x] 6.4 Write property test: Quantity-based measurement upsert (Property 7)
        - **Property 7: Quantity-based measurement upsert**
        - Use `repeat(100)` to create duplicate measurements for same (wbs_node_id, status_date)
        - Verify exactly one record exists after upsert with updated values
        - **Validates: Requirements 3.8**

- [x]   7. Extend factories for quantity-based testing
    - [x] 7.1 Add `quantityBased(int $plannedQuantity, ?float $unitCost = null)` method to `WbsNodeFactory`
        - Sets `measurement_method = quantity_based`, `planned_quantity`, and optionally `unit_cost`
        - _Requirements: 2.1, 2.4_
    - [x] 7.2 Add `quantityBased(int $quantityCompleted, int $plannedQuantity)` method to `MeasurementFactory`
        - Sets `measurement_method = quantity_based`, `quantity_completed`, and calculates `percent_complete` automatically
        - _Requirements: 3.6, 3.7_
    - [x] 7.3 Write property test: Quantity fields round-trip persistence (Property 8)
        - **Property 8: Quantity fields round-trip persistence**
        - Use `repeat(100)` with Faker to generate valid `planned_quantity`, `unit_cost`, and `quantity_completed` values
        - Persist to database and read back, verify exact equivalence for integers and decimal precision for `unit_cost`
        - **Validates: Requirements 2.3, 2.6, 3.6, 9.1, 9.2, 9.3**

- [x]   8. Checkpoint — Ensure all service and factory tests pass
    - Ensure all tests pass, ask the user if questions arise.

- [x]   9. Extend `ManageWbsNodes` form with conditional quantity fields
    - Add `TextInput::make('planned_quantity')` — integer, required when `quantity_based`, visible only when `measurement_method = quantity_based` using `->visible(fn (Get $get))` reactive
    - Add `TextInput::make('unit_cost')` — with BRL mask (`R$` prefix, `$money` mask), optional, visible only when `measurement_method = quantity_based`
    - Make `measurement_method` select `->live()` so visibility reacts to changes
    - Ensure the `EditAction` and `CreateAction` pass the new fields through correctly, catching `InvalidArgumentException` as per existing pattern
    - _Requirements: 2.1, 2.4, 2.7, 2.8, 2.9, 6.1_

- [x]   10. Extend `MeasurementPage` PHP class for quantity-based recording
    - [x] 10.1 Update `initializeForms()` to load `quantity_completed` from carry-forward measurement for quantity_based WPs
        - Add `quantity_completed` key to `$wpForms` state array
        - _Requirements: 7.5_
    - [x] 10.2 Update `recordMeasurement()` to handle `quantity_based` method
        - Read `quantity_completed` from form data, call `$evService->recordMeasurement($wp, $percentComplete, null, $quantityCompleted)` for quantity_based WPs
        - _Requirements: 3.1, 3.4, 3.5_

- [x]   11. Extend Blade template with quantity-based measurement UI
    - [x] 11.1 Add `@elseif($method === \App\Enums\MeasurementMethod::QuantityBased)` block in the measurement form section
        - Numeric input for `quantity_completed` with `wire:model.defer`
        - Label showing "X / {planned_quantity} unidades" reference
        - Real-time calculations via Alpine.js (`x-data`, `x-on:input`): % Complete, EV, and suggested AC when `unit_cost` is defined
        - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
    - [x] 11.2 Add `quantity_completed` column to the measurement history table
        - Show `quantity_completed` for quantity_based measurements, "—" for other methods
        - _Requirements: 6.6_
    - [x] 11.3 Add suggested AC pre-fill logic for quantity-based WPs
        - When `unit_cost` is defined, calculate and display `AC sugerido = quantity_completed × unit_cost` in BRL format
        - Pre-fill the AC field with the suggested value; user can override before saving
        - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x]   12. Checkpoint — Ensure all tests pass and UI renders correctly
    - Ensure all tests pass, ask the user if questions arise.

- [x]   13. Write property test: Historical immutability for quantity-based measurements (Property 9)
    - **Property 9: Historical immutability for quantity-based measurements**
    - Use `repeat(100)` to create quantity_based measurements at past status dates, advance project status_date, attempt updates
    - Verify all update attempts on historical records are rejected
    - **Validates: Requirements 7.1**

- [x]   14. Final checkpoint — Ensure all tests pass
    - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate the 9 correctness properties defined in the design using Pest v4 with `repeat(100)` and Faker
- Unit tests validate specific examples and edge cases
- All UI text is in pt-BR; all code identifiers are in English
- Monetary fields use BRL mask pattern (`R$` prefix, `$money` Alpine mask)
- Domain validations throw `InvalidArgumentException`, caught by Filament actions with `Notification::make()->danger()`
