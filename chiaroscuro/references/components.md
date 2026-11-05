# Components

Contents: buttons · tables · dashboards · navigation · description lists · badges · avatars · icons · images and SVG · charts.

## Buttons

- One primary per view or action cluster; two or three tiers in a view. A fourth tier means some actions belong in a menu or nowhere.
- Weight matches consequence. Forward progress is strongest; a destructive action is serious, set apart, paired with words rather than colour alone, and never the default.
- Everything pressable looks pressable, and nothing static does.
- Only the control heights the product needs. Horizontal padding follows the height (`px-3`, `px-4`, `px-5`), not pill padding by default. Modest radius unless the product has a reason for pills.
- `font-medium` or `font-semibold`, body face, sentence case, one line, short verbs from the user's domain. `tabular-nums` for counts.
- Loading never shrinks or relabels the button. A disabled button says why when the reason isn't obvious.
- Shadows, if any, are subtle; no gradients faking hierarchy.

## Tables

- Sentence-case headings that never wrap (`whitespace-nowrap`). Hide headings with `sr-only` when two or three self-explanatory columns don't need them.
- Tables sit directly on the background, never in a card. Horizontal row dividers only: no vertical lines, no outer border. `w-full`.
- Right-align numeric columns and their headings; one decimal precision per column.
- The record name gets its width first; secondary columns truncate first.
- Row checkboxes only when selection enables a bulk action, and a selected row looks different from a hovered or focused one.
- One status per row: a badge or a tag, not both.
- A real zero shows `0`. Missing or inapplicable values get a muted mark with an accessible name such as "No data".
- Sort by column when people compare or locate records; keep a deliberate order when the sequence means something. Paginate or virtualise when the measured collection requires it, not at an arbitrary count.
- When columns won't fit, scroll horizontally with two wrappers whose margins and padding match the page container:

  ```html
  <div class="-mx-4 -my-2 overflow-x-auto whitespace-nowrap sm:-mx-6 lg:-mx-8">
    <div class="inline-block min-w-full px-4 py-2 align-middle sm:px-6 lg:px-8">
      <table>…</table>
    </div>
  </div>
  ```

## Dashboards

- Stat titles never wrap (`truncate`). No icons in stat cards: label and value only.
- Widgets adapt with container queries.
- Filters are visible, not buried in menus.

## Navigation

- Every destination stays reachable on small screens; how it adapts (tab bar, sheet, disclosure) is a phone composition decision.
- The active item gets darker text, a soft background or both, never a high-contrast or primary fill. No weight change between states.
- Horizontal tab and pill navs never overflow their parent; they scroll.
- No icons in top header links.
- To centre links on the page, not between the side items: left and right sections each `flex flex-1` (the right one `justify-end`), the links at natural width between them. Centre a logo the same way.
- Hide page numbers on phones when pagination also has previous and next.
- Breadcrumbs from three levels deep.

## Description lists

`<dt>` in the higher-contrast colour and `font-medium`; `<dd>` regular and lower contrast, so links inside it can use the stronger colour.

## Badges

- Static information only. A chip that selects, filters or removes is a real button or checkbox with its state exposed.
- Never wrap: `whitespace-nowrap shrink-0`; decide which sibling yields.
- With an icon, the icon side's padding equals the vertical padding: `py-1 pr-2 pl-1` for a leading icon.

## Avatars

- `outline-1 -outline-offset-1 outline-black/5` on light, `outline-white/10` on dark. Overlapping groups get a 2px ring in the background colour.
- `object-cover`; fall back to initials when the image fails, built from the first grapheme of the first and last words (`Intl.Segmenter`, not `[0]`, which breaks on emoji), then to an icon when there is no name.

## Icons

- One family from the project, one stroke style. A custom SVG only for a mark the family can't supply.
- Match rendered stroke to the adjacent text: about 1.5px beside regular text, 2px beside medium or semibold. A 24px-grid icon drawn at 16px thins its stroke, so use the library's absolute stroke option (Lucide's `absoluteStrokeWidth`) or `vector-effect: non-scaling-stroke`.
- Outline for the default state, fill for selected or active. Never use the two interchangeably.
- Draw with `currentColor` and take state from CSS colour; strip hardcoded fills.
- No decorative container around an icon unless it marks a control boundary, state, category or brand.
- Beside a label and supporting text, align to the first line (`items-start` or `items-baseline`), never centre on the group. `size-4 h-lh` centres an icon on its line; set the font size on a wrapper rather than nudging with margins.
- Under `dir="rtl"`, mirror only icons whose meaning follows reading direction: back and forward arrows, chevrons, send. Never logos, checkmarks, clocks or media playback.

## Images and SVG

- Choose a set that agrees in light, colour temperature, ratio and crop, and look at it together. Each image shows the object its label names.
- No borders on photos. A visible edge is `outline-1 -outline-offset-1 outline-black/10` (`outline-white/10` on dark), pure black or white, never a tinted neutral that fringes. Skip it on transparent artwork.
- Ratio from the source and the layout role; stable to prevent shift; consistent in a repeated grid, but widescreen content can stay widescreen. Pair `object-cover` with an `object-position` chosen per image.
- Explicit dimensions; lazy-load below the fold; prioritise the real largest image.
- Where images come from users or a feed, check the layout with an all-white image, an all-black image and none.
- Large media radii can shrink on narrow screens.
- Inline `<svg>` omits `xmlns` and takes colour from `fill-*`, `stroke-*` or `currentColor`. A class overrides a presentation attribute on the same element but not on a child path; when a colour won't change, find which element actually paints.
- Inline autoplaying video needs `muted`, `playsinline`, a poster and a reduced-motion plan; pause it off screen. Prefer it to animated GIF.

## Charts

- Establish whether values are discrete, ordered or continuous. A smooth curve implies intermediate values; use marks, steps or bands when those match the data.
- Keep units, domains, denominators and baselines honest. When scales differ between charts, make it visible.
- Sample data shows the encoding's range: gaps, extremes, mixed signs.
- Trace one value from source to mark to tooltip and back.
- A forecast is a dashed continuation with a labelled projected endpoint.
- No legend for a single series the title already names.
- One entity, one hue across every chart in a collection.
- Show uncertainty where the data has it, and give each chart a text or table alternative.
- Across a collection, share the grammar (type roles, axes, grids, palette roles, line weight) while keeping the distinctions the data needs; flattening every texture can erase them.
