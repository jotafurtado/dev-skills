# Panel shell, navigation, and authentication composition

Choose shell structure from the application's audience, destination count, and domain boundaries. Keep version-sensitive panel and authentication APIs in `laravel-filament-v5`; this reference selects the information architecture and visual composition.

## Start with audience and destination structure

Use a single panel when the same audience shares the same authentication boundary and moves between related operational domains. A navigation group then names a stable domain within that panel; it is not a visual bucket for unrelated links. Use a cluster when one cohesive domain needs its own sub-navigation and route structure. Use a separate panel when audience, authentication boundary, path/domain, or operational product differs.

Use the default sidebar for a substantial back-office: many destinations, several coherent domains, or repeated scanning between operational areas. Put related Resources and pages in named groups. Keep group names short and domain-specific. Collapse a group only when people can still discover its contents and current location; do not make an icon-only collapsed sidebar the sole representation of a group's meaning.

Use top navigation only for a small, stable set of peer destinations with short labels. It is not a compact substitute for a substantial back-office hierarchy. When labels, groups, user controls, or active-state cues compete for horizontal space, retain a responsive menu and reconsider the sidebar or panel boundary.

## Counts, identity, and account controls

Show a navigation badge only for a meaningful actionable count, such as pending approvals assigned to the current operator. Do not use a badge for vanity totals, stale metrics, or as the only explanation of a destination. A label and the destination's purpose must remain understandable without badge colour.

Configure the panel's brand identity with supported panel configuration or established theme hooks. Preserve the existing theme; do not introduce unrelated typefaces, palettes, or a CSS-first shell merely to differentiate the panel. Place account and session actions in the user menu when they are secondary to primary destinations; do not hide a common operational destination there.

## Authentication surfaces

Use the supported login, registration, password-recovery, and profile surfaces before inventing a custom account layout. Keep one focused account task in view. Preserve visible labels, logical tab and focus order, visible focus, keyboard-reachable recovery/account links, and validation or status feedback that remains understandable without colour alone. A logo, colour, or placeholder does not replace a field label, error, or action name.

Keep recovery focused: a person who cannot sign in needs a clearly named reset action and a route back to login. Treat profile/account-security work as personal account maintenance, not a broad operational settings page. Use the established panel identity consistently across anonymous and authenticated surfaces.

## Decision trace and evidence

For a material shell change, record the audience, destination shape, candidates, selected structure, responsive treatment, and inspected evidence. Inspect `panels/navigation/top-navigation` for a small peer-oriented panel; inspect `panels/navigation/group`, `panels/navigation/badge`, and `panels/cluster` for a substantial back-office; inspect `panels/login`, `panels/registration`, `panels/password-reset`, and `panels/profile` for authentication hierarchy. For brand treatment, inspect `panels/styling/brand-logo` and retain supported configuration or the established theme.
