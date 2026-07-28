# Actions, overlays, feedback, and empty states

Choose the interaction weight from the work the user must do, not from a preference for overlays. Keep a direct frequent action visible. Put secondary, uncommon, and destructive actions in a labelled group when that prevents the surrounding record, form, or table from becoming noisy. Do not hide the only likely next step in an ambiguous overflow control.

## Overlay decision

Use a compact confirmation when the user has already supplied every needed value and only needs to acknowledge a consequential, destructive, or irreversible result. State what will happen, which record or scope is affected when useful, and provide an explicit cancel path. Danger colour can reinforce risk, but the action label, consequence text, and an icon or other cue must communicate it without colour alone.

Use a focused modal form for one short contextual task with a small number of inputs. Keep the title, required fields, validation, submit outcome, and cancellation path in one coherent reading flow. Move to another surface when the overlay becomes a scrollable mini-page or hides information needed to complete the task.

Use a slide-over when the user needs persistent surrounding record or page context, a longer supporting explanation, or a task-oriented side panel. Do not use it merely because it looks lighter than a page: if its narrow reading column makes comparison, validation, or recovery difficult, use a full page.

Use a full page for a substantial multi-stage workflow, durable navigation between stages, large reference material, or recovery that must remain available while the user works. Do not make a short contextual decision navigate away from its initiating record just to avoid a modal.

Preserve keyboard triggering, visible focus, predictable focus transfer into an overlay, and a reliable return to the trigger after dismissal. Version-sensitive action and modal APIs belong to `laravel-filament-v5`.

## Guidance and feedback scope

Place field hints beside the specific field they qualify. Use a callout for a warning, policy, or next step that applies to a nearby group or workflow before the user acts. Use action feedback or a notification for a completed result, failure recovery, or optional immediate follow-up that is not already fully communicated at the initiating control. Do not repeat the same message in a hint, callout, modal, notification, and page state; choose the narrowest level that fully explains it.

Use concise text and a recognisable icon or label for success, warning, danger, and information. A transient notification must have a discernible title and body when needed; persistent outcomes, validation, or state that users must revisit belong near the affected content instead.

## Empty states

Name what is absent and explain the state in one concise sentence. Offer an action only when the user can and should resolve that absence, such as creating the first record or connecting a required resource. Keep the action discoverable by keyboard and give it a clear label.

Treat an initial absence differently from filtered no results. An initial empty state may offer the legitimate creation action. A filtered result must explain or retain the active filters and offer a reset or adjustment path instead of inviting duplicate creation.

## Evidence to inspect

For a material interaction decision, inspect `actions/group/simple`, `actions/modal/confirmation`, `actions/modal/form`, `actions/modal/slide-over`, `panels/resources/editing`, `components/callout/simple`, `notifications/actions`, and `components/empty-state/actions` from the reviewed catalog. Include the candidates, selected interaction weight, feedback level, responsive treatment, and any full-page escalation in the visual decision trace.
