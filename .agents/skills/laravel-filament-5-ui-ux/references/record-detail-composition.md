# Record-detail and infolist composition

Use this reference after querying the catalog for a read-oriented Filament 5 record page or infolist. It selects visual hierarchy; use `laravel-filament-v5` to verify installed-version entry, layout, and action APIs before implementation.

## Start with the record hierarchy

Put the record identity and the current state that changes the next decision first. Follow with the small set of primary facts people use most often. Move dense metadata, repeated data, media collections, history, and long-tail information after that first scan path. Do not make every fact equally prominent or move current state below secondary detail.

Use a simple detail flow for a short, self-explanatory record. Use a two-zone identity-and-facts composition when recognition and current status need to remain prominent while compact facts form a separate scannable block. Use a larger secondary surface when history, related records, media, or several substantial groups would turn the page into a long undifferentiated list. Do not use a record-detail composition where staff instead need cross-record comparison; keep that work in a table.

## Select entry treatments by meaning

Use inline labels for a dense, familiar fact block with short labels and values. Keep a vertical label-value flow for long values, ambiguous labels, explanatory text, validation or recovery context, and narrow layouts where an inline pair would crowd.

Use a readable status label with a badge or icon as reinforcement when current state affects the next decision. Never make colour or an unlabelled icon the only state cue. Use media when it helps recognise or verify the record, not as decoration. Make identifiers copyable only when people genuinely need to transfer them; retain an accessible name and keyboard operation for the copy control.

Show a placeholder when an expected absent value has meaning, so it cannot be confused with an omitted field or loading data. Do not fill optional, inconsequential facts with placeholders merely to make the layout look complete.

Use a repeatable detail when a person must inspect structured repeated items as units. Choose its layout from the information shape: ordinary contained items for distinct units, a grid for grouped peer facts, and a table-like arrangement when repeated attributes need alignment. Move a large history or related-record workflow to a dedicated secondary surface instead of burying it in a dense infolist.

Collapse long-tail detail only when its trigger names what is available and identity, current state, primary facts, error recovery, and the common next action remain visible. A collapsed area is not a way to hide information needed for the recurring task.

## Responsive and accessible treatment

Start with a readable narrow flow. When a wide record page stacks, retain identity, status, and primary facts before secondary metadata. Restore vertical labels before inline pairs collide, and keep media alternatives, disclosures, copy controls, and entry actions keyboard reachable with visible focus.

Preserve labels or equivalent accessible names for every entry. State must be understandable without colour. Give every copy or disclosure control a discernible label. Do not rely on visual placement alone to explain which facts belong together.

## Evidence to inspect

For a material record-detail composition, inspect `panels/resources/viewing`, `infolists/overview`, `infolists/entries/simple`, `infolists/entries/inline-label/section`, `infolists/entries/text/badge`, `infolists/entries/icon/boolean`, `infolists/entries/image/limited`, `infolists/entries/text/copyable`, `infolists/entries/placeholder`, `infolists/entries/repeatable/table`, `schemas/layout/tabs/simple`, and `infolists/entries/text/expandable-limited-list` from `visual-catalog.json`.

Record the candidates, selected hierarchy, retained mobile scan path, state treatment, and the handling of secondary detail in the visual decision trace. Do not state version-sensitive entry signatures here; delegate them to `laravel-filament-v5`.
