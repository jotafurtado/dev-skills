# Official screenshot index — see the real thing before composing

The Filament docs ship high-resolution screenshots of every component and page pattern. When building or restructuring a UI surface — especially a whole page — and you can view images, **download the relevant official screenshot and look at it** instead of imagining what "a Filament table" looks like. This grounds spacing, hierarchy, action placement, and color usage in the real design language.

## URL formula

```
https://filamentphp.com/docs/images/5.x/{light|dark}/{name}.jpg
```

`{name}` comes from the index below. Images are ~3000px wide JPEGs; `light` is enough for composition analysis. Download to a temp directory and view:

```bash
curl -sL -o /tmp/shot.jpg "https://filamentphp.com/docs/images/5.x/light/tables/example.jpg"
```

## Discovering screenshots not in this index

Every docs `.md` page declares its screenshots as `<AutoScreenshot name="..." ...>` tags. To enumerate what a page illustrates:

```bash
curl -sL "https://filamentphp.com/docs/5.x/{section}/{page}.md" | grep -oE '<AutoScreenshot name="[^"]+"' 
```

Page list: `https://filamentphp.com/docs/llms.txt`.

## Curated index — pattern → screenshot name

Whole-page and composition-level references (the most valuable ones):

| You are building | View |
|---|---|
| A complete list page / table | `tables/example` |
| A dashboard (stats + charts + nav) | `panels/dashboard` |
| Sidebar navigation with groups | `panels/navigation/group` |
| Top navigation variant | `panels/navigation/top-navigation` |
| Nav item with count badge | `panels/navigation/badge` |
| A View page with two-zone layout + tabs | `infolists/overview` |
| Login page | `panels/login` |

Tables:

| Pattern | View |
|---|---|
| Filters dropdown (icon + badge count) | `tables/overview/filters` |
| Row actions placement | `tables/overview/actions` |
| Grouped rows with group headers | `tables/grouping` |
| Column summaries footer | `tables/summaries` |
| Split/stack record layout (people, cards) | `tables/layout/demo`, `tables/layout/split` |
| Card grid layout | `tables/layout/grid` |
| Collapsible row panel for the long tail | `tables/layout/collapsible` |
| Text column as badge | `tables/columns/text/badge` |

Schemas, forms, and infolists:

| Pattern | View |
|---|---|
| Section with heading + description | `schemas/layout/section/simple` |
| Aside section (settings-page look) | `schemas/layout/section/aside` |
| Section with internal columns | `schemas/layout/section/columns` |
| Collapsed / compact / secondary sections | `schemas/layout/section/collapsed`, `.../compact`, `.../secondary` |
| Tabs on a form | `schemas/layout/tabs/simple` |
| Wizard steps | `schemas/layout/wizard/simple` |
| Dense read-only block | `schemas/layout/dense` |
| Standard field wrapper (label/required/helper) | `forms/fields/simple` |
| Repeater item cards | `forms/fields/repeater/simple` |
| Inline-label "Details card" | `infolists/entries/inline-label/section` |
| Text/icon/image primes on a page | `primes/overview/example` |

Widgets, feedback, and overlays:

| Pattern | View |
|---|---|
| Stat tiles with trend + sparkline | `widgets/stats-overview/chart` |
| Line / bar chart widgets | `widgets/chart/line`, `widgets/chart/bar` |
| Empty state with action | `components/empty-state/actions` |
| Callout (notice) variants | `components/callout/simple` |
| Confirmation modal (delete) | `actions/modal/confirmation` |
| Modal with a form | `actions/modal/form` |
| Slide-over form | `actions/modal/slide-over` |
| Grouped actions dropdown | `actions/group/simple` |

## How to use what you see

Extract composition facts, not pixels: where the primary action sits, how many visual levels exist, what is bold vs muted, where actions align, how much whitespace separates groups. Then express the same structure with the official components from the other references — never by writing CSS to imitate the screenshot.
