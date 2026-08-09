# Dashboard composition

Use a dashboard to support a repeated operational decision, not to display every available metric. Start with the question a person must answer: what needs attention now, what changed over a meaningful period, and which record or queue requires the next action. Put the smallest summary that answers the first question before deeper trend or record detail.

## Choose native widgets by decision

Use a Stats Overview when a small number of current measures and their direction tell a person whether to investigate or act. Each stat needs a recognisable measure, comparison period when a change is shown, and concise direction or consequence. A sparkline can reinforce the trend; it does not replace the numeric value or change label.

Use a Chart widget when a trend, distribution, or series comparison answers a recurring question that one current measure cannot answer. Give it a heading, an understandable time period, labelled series, and a scale that lets people interpret the change. Do not add a chart solely because a dashboard has empty space.

Use a Table widget for a deliberately narrow operational queue: recent activity, exceptions, approvals, or work that follows from the summary. Do not duplicate the full management table without a dashboard-specific purpose. Keep identity, the decision-driving state, and the next action visible.

Use a shared dashboard filter when one named scope, such as a date range, team, or region, changes several widgets together. Show the active scope and avoid using a global filter when a question belongs to only one chart or table. Use the normal Filament action and form patterns for a filter action rather than a custom control.

## Order, spans, and density

Order widgets by decision value: current risk or state first, then the trend that explains it, then the actionable record queue. Group metrics only when they share a question or comparison period. Give a chart or activity table a wider span when its information density needs it; concise headline stats may share a row. Do not make all widgets equal width just to fill a grid.

Start from a readable narrow layout and add responsive column spans at wider breakpoints. On smaller screens, stack widgets before labels, chart controls, table actions, or filter controls become crowded. Preserve the panel theme and native widget structure; do not recreate stat tiles with hand-written Blade cards or an unrelated card system when a native widget fits.

## Meaning, feedback, and access

Use semantic trend colour only as reinforcement. Pair it with text or an icon that communicates direction and change, so an increase, decrease, warning, or healthy state remains understandable without colour. Give widget headings and descriptions enough context to explain the decision or period, not merely the data source.

Keep dashboard filters, table actions, chart controls, and linked records keyboard-reachable with visible focus and discernible names. Avoid polling or constantly changing values when it would interrupt reading, obscure feedback, or add load without a time-sensitive operational need. Retain compatible performance, responsive, feedback, and accessibility guidance from the existing panel.

## Evidence to inspect

For a material dashboard decision, inspect the reviewed catalog evidence for `panels/dashboard` (including its table-widget queue), `panels/dashboard-column-spans`, `panels/dashboard-filters`, `widgets/stats-overview/chart`, `widgets/stats-overview/heading`, `widgets/chart/line`, and `widgets/chart/filter`. Compare the local catalog candidate before implementation and include the selected pattern, widget order, responsive treatment, and inspected evidence in the visual decision trace.
