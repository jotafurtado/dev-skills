# Responsive record layouts

Start by separating two different jobs. Keep a standard compare-and-scan table when people must evaluate the same facts across peer records. Choose an identity-centred record layout when each row is primarily one person, account, item, or case whose identity and grouped supporting details matter more than simultaneous column comparison. Do not switch to a card-like row merely to make a desktop table look more visual.

## Select the record hierarchy

Use Split when identity, a small set of primary facts, and a row action form one horizontal desktop scan line. Let the identity stay recognisable while supporting details sit beside it; stack the same information at the breakpoint where the horizontal relationship would crowd names, labels, values, or actions. Avoid Split when several facts still need accurate column-to-column comparison or when one side has long, variable content.

Use Stack to keep tightly related details in one readable vertical unit, such as contact channels or a compact status-and-metadata cluster. Use nested Stack only while the order remains obvious when it becomes a mobile row. Avoid it for independent facts that users must compare across records, or when it hides a common action beneath dense prose.

Use Grid for grouped peer details that benefit from equal tracks, and use a content grid when each record can be scanned as an independent identity unit at wider breakpoints. Reduce the number of content-grid columns before identity, labels, selection controls, or actions become too small. Avoid a content grid when the task is still compare-and-scan: it trades cross-record alignment for per-record hierarchy.

Disable growth only when a short identity or fixed-width fact should keep its natural space and the remaining content can use the saved width. Do not use growth behaviour to create visual balance while leaving critical content truncated or actions displaced.

Make secondary information collapsible only after the identity and decision-driving state remain visible, the collapsed content has a meaningful summary, and users can discover and operate the control. Avoid collapsing information needed for the recurring task, current selection, error recovery, or a common action.

## Transform, do not shrink

At the mobile breakpoint, deliberately re-order the hierarchy: keep identity first, retain the state or fact that changes the next decision, keep the primary action discoverable, and move secondary supporting details into a readable stack or expandable area. Do not simply compress a desktop row, hide every label, or move all actions into an unlabeled overflow control.

Retain keyboard access and visible focus for selection, expand/collapse, and row actions at every breakpoint. Preserve a logical reading order, distinguish controls with discernible labels, and do not use layout, visibility, or colour as the only way to communicate a record's state or the availability of an action.

## Evidence to inspect

For a material responsive-record decision, inspect the paired official evidence in `visual-catalog.json`: `tables/layout/split-desktop` and `tables/layout/split-desktop/mobile`, `tables/layout/stack` and `tables/layout/stack/mobile`, `tables/layout/grid` and `tables/layout/grid/mobile`, `tables/layout/collapsible` and `tables/layout/collapsible/mobile`, plus `tables/layout/column-grid`, `tables/layout/grow-disabled`, and `tables/layout/stack-hidden-on-mobile`. Record the desktop candidate, mobile transformation, and retained identity, state, selection, and action affordances in the visual decision trace.
