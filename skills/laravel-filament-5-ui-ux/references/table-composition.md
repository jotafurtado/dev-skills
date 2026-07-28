# Table composition

Use a standard table when people need to compare the same facts across many peer records. Do not replace that scan path with cards, stacked identity panels, or a detail-first layout merely to make the surface more decorative. Use a card or identity-centred layout only when each record needs materially different content, rich preview context, or a narrow-screen treatment that cannot preserve meaningful row comparison.

## Start with the comparison question

Ask what a user must distinguish before choosing columns. Order the row around that task:

1. Put the record identity first: the name, title, or identifier that lets someone locate a row.
2. Put the state that changes the decision next: status, availability, approval, or exception.
3. Follow with the few comparable facts used to decide between records.
4. Put dates, recency, and other supporting facts after the decision facts unless time is the primary comparison.
5. Keep row actions at the end, visually separate from data and limited to actions on that one record.

Avoid equal priority for every available field. Hide, move to record detail, or make optional any fact that does not support the recurring comparison. Preserve a stable column order across filters and pagination so users do not have to relearn the scan path.

## Filters, state, and actions

Use filters for recurring, purposeful subsets that users can name before they scan: a status, date range, owner, category, or exception state. Avoid using filters as a substitute for obvious columns or for a one-off search query. Keep the filter trigger close to search and expose active filtering or an explicit reset so a smaller result set is understandable.

Use text plus a recognisable icon, label, or other non-colour cue for status and boolean values. A coloured badge or checkmark can reinforce meaning, but red/green alone must not carry it. Prefer a concise status label when the difference drives a decision; use a boolean icon only when its meaning is conventional, labelled through accessible text, and remains distinguishable without colour.

Put a primary, frequent per-record action directly in the row. Group secondary, destructive, or less frequent record actions under a labelled action menu when showing them inline would crowd comparison data. Do not hide the only common next step in an ambiguous overflow menu.

Enable bulk selection only when people genuinely operate on several records at once, the selection scope is clear, and every bulk operation is safe for a mixed selection. Group destructive or uncommon bulk actions. Make the selected count, consequences, confirmation, and recovery path visible; do not imply that selection spans other pages unless the implementation explicitly supports that scope.

## Grouping, summaries, pagination, and empty results

Use grouping when a shared attribute is itself a useful way to scan the list, such as workflow status or date bucket. Keep ordinary columns when cross-group comparison matters more than the group boundary. Make grouping collapsible only when users can still discover that records exist inside each group.

Use summaries for aggregates that change a table-level decision, such as the count of exceptions, a monetary total, or an average needed to judge the list. Avoid decorative totals or averages that compete with the row data. Ensure a summary names both its measure and its scope when filters, pagination, or grouping could change it.

Choose pagination that keeps a large result set tractable while retaining the comparison context. Show the visible range and total when that helps users understand completeness. Do not use a simpler pagination treatment when people must jump among distant result pages or understand their position in a large list.

Treat no records and no matching records as different states. An initial empty result should name what is absent and offer the appropriate create action when users can create it. A filtered empty result should retain or explain the active filters and offer a clear reset, not invite users to create a duplicate record.

## Responsive and accessible treatment

On narrow widths, retain identity and the state or fact that drives the decision. Use an official responsive table layout to stack or collapse secondary information only after checking that the remaining visible row still supports the comparison. Do not turn every row into a card if that removes the ability to compare peers.

Keep table headers associated with values, give icon-only controls discernible names, preserve keyboard access to row and bulk actions, and retain visible focus. Sorting, filtering, pagination, grouping, selected state, status, and empty-state meaning must be perceivable without colour alone.

## Evidence to inspect

For a material table decision, inspect the relevant reviewed evidence in `visual-catalog.json`: `tables/overview/columns`, `tables/overview/filters`, `tables/actions/group`, `tables/actions/bulk`, `tables/grouping`, `tables/summaries`, `tables/pagination/default`, and `tables/empty-state`. Compare the local catalog candidate before implementation and include the selected table pattern and inspected evidence in the visual decision trace.
