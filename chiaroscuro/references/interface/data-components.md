# Data & App Components

Component rules for data-dense and application UI. Load the anchor for the component in the work.

## Tables

Covers: data tables, comparison tables, table headings, row dividers, horizontal scrolling tables, and table containers.

- Never use uppercase text in table headings - use normal sentence case instead
- Never let table headings wrap - use `whitespace-nowrap` on `<th>` elements
- Never put tables in containers or cards - place them directly on the background
- Only use horizontal lines to divide rows - no vertical lines, no outer borders
- Always use `w-full` so tables fill their container
- Hide table headings with `sr-only` when the column content is self-explanatory - typically tables with 2–3 columns where headings add no value
- Right-align numeric columns and their headings so values and heading share one edge; keep one decimal precision within a column or metric
- Give the record name the width it needs before secondary columns; truncate secondary columns first
- Add row checkboxes only when selecting rows enables a bulk action, and make a selected row look different from a hovered or focused one
- Show a row's status once - one badge or one tag, not both
- Show a real zero as `0`; mark missing or inapplicable values differently, with a muted mark that has an accessible name such as "No data"
- Always make tables responsive if all columns won't fit on smaller screens - use a two-div wrapper around the table:
  - Outer div: `overflow-x-auto whitespace-nowrap` with negative horizontal and vertical margins - horizontal margins cancel the page container's padding (e.g. `-mx-4 sm:-mx-6 lg:-mx-8`), vertical margin is always `-my-2`
  - Inner div: `inline-block min-w-full align-middle` with horizontal padding that matches the container's padding (e.g. `px-4 sm:px-6 lg:px-8`) and `py-2`
  - Always match the negative horizontal margins and horizontal padding to the actual container padding used in the page layout
  - Example implementation:
  ```html
  <!-- Example assumes container padding of px-4 sm:px-6 lg:px-8 -->
  <div class="-mx-4 -my-2 overflow-x-auto whitespace-nowrap sm:-mx-6 lg:-mx-8">
    <div class="inline-block min-w-full px-4 py-2 align-middle sm:px-6 lg:px-8">
      <table>
        …
      </table>
    </div>
  </div>
  ```

## Dashboards

Covers: dashboard layouts, stat grids, KPI cards, metric cards, admin panels, analytics views, and summary data.

- Never allow stat or metric card titles to wrap; use `truncate` to keep them on a single line
- Never put icons in stat/metric cards - use plain text labels and values only
- Always use container queries for responsive dashboard widgets, not media queries

## Navigation

Covers: sidebar nav, header nav, mobile menus, tabs, tab bars, vertical menus, active states, and current-page indicators.

- When an app has navigation, every destination stays reachable on small screens. How it adapts (tab bar, sheet, disclosure) is a phone composition decision; `reflow` covers the mechanics. A focused experience with nowhere to go needs no menu
- Never use a high-contrast or primary-color background for active nav items - use darker text color, a soft/muted background, or both
- Never change `font-weight` between nav item states (default, hover, active) - use color and background changes only
- Horizontal menus (tabs, tab bars, pill navs) must never overflow the parent container - use horizontal scrolling when items don't fit
- Never use icons in top header horizontal navigation links - use text-only links
- When centering nav links on the page (not just between side items), use a three-section flex layout: `<div class="flex flex-1 items-center">` for the left section (logo), the nav links in their natural width (no `flex-1`), and `<div class="flex flex-1 items-center justify-end">` for the right section (actions). The matching `flex-1` gutters force the centered group to the true page center. Apply the same pattern when centering a logo: keep the logo in its natural width and use `flex-1` on the side sections to center it on the page rather than between the surrounding items.

## Pagination

Covers: pagination, page number links, previous/next buttons, and paged navigation controls.

- Hide page numbers on mobile when pagination includes both page numbers and previous/next buttons

## Description Lists

Covers: `<dl>`, `<dt>`, and `<dd>` content, term/detail pairs, metadata groups, and definition-style lists.

- Style `<dt>` elements with higher contrast text color and a slightly heavier font weight (e.g. `font-medium`); style `<dd>` elements with regular font weight and a lower contrast color - this lets links inside `<dd>` elements use the higher contrast color to stand out
