# Interface: Layout

## Principles

- MUST: Deliberate alignment (grid/baseline/edges/optical centers)
- MUST: Every layout element has a job: hierarchy, grouping, navigation, affordance, state, content meaning, or domain character
- MUST: Remove UI furniture: purposeless chrome, decorative wrappers, filler panels, floating badges, fake controls, ornamental dividers, and background effects that do not change user understanding
- MUST: Verify mobile, laptop, ultra-wide (simulate at 50% zoom)
- MUST: Respect safe areas via `env(safe-area-inset-*)`
- MUST: No unwanted scrollbars — fix overflows
- SHOULD: Optical alignment: ±1px when perception beats geometry — icons beside text, play triangles in circular buttons, and text in buttons usually need a 1–2px nudge to look centered; section vertical padding often wants slightly more bottom than top to feel balanced
- SHOULD: Balance icon/text lockups (stroke, weight, size, spacing, color)

## Cross-Element Alignment

- MUST: Sibling cards, columns, and tiers align shared elements on the same Y — titles, descriptions, prices, and CTAs each sit on one shared baseline across all items. Misaligned baselines read as broken, not casual.
- MUST: Pin CTAs to card bottoms (`mt-auto` in a flex column) so buttons form one clean horizontal line regardless of content height above them.

## Multi-Span Grids

- MUST: No dead cells — in bento/multi-span grids, verify the `col-span`/`row-span` values interlock with no empty voids; `grid-flow-dense` backfills holes. Prefer 3–5 intentional tiles over 8 messy ones.

## Flex Sizing

- MUST: Add `min-w-0` to flex children that must shrink below their content size. Flex items default to `min-width: auto` and will not shrink past their content without it — applies from page-level layouts (fluid content area next to a fixed `flex-1` sidebar) down to small pieces (a truncated label in a row, a flexible input beside a fixed button).
- MUST: Add `shrink-0` to flex children that must never compress — icons, SVGs, images, logos, avatars, and any fixed-size control that distorts when squeezed.

## Constrained Sections

- MUST: Use a two-element pattern for constrained page sections — the outer element handles background and vertical padding; the inner element handles `max-width`, centering, and horizontal padding. Apply it consistently across a page so content edges align while scrolling.

  ```html
  <section class="{vertical-padding}">
    <div class="{max-width} mx-auto {horizontal-padding}">
      ...
    </div>
  </section>
  ```

- MUST: Left-aligned sections align to the page container edge — never narrow `max-w-* mx-auto` to fake it. Set `max-w-*` at the page level and constrain inner content separately.
- SHOULD: Align containers that occupy the same proportion across stacked sections so their column edges line up — share grid definitions and gap values.
- SHOULD: For the strictest page-wide consistency, define one shared grid (e.g. 12 columns) and give every section explicit spans (`col-span-12/8/6/4`) instead of per-section ad hoc widths — inconsistent section widths become a checkable violation. Collapse all spans to `col-span-full` below the mobile breakpoint.
- SHOULD: Avoid nested `max-w-*` on grids/lists that already fill their container; let them align to the page edges. Nested `max-w-*` is fine for self-contained units meant to feel bounded (pricing cards, forms, comparison tables, centered media).

## Viewport

- MUST: `h-dvh` not `h-screen` (respects mobile browser chrome)
- MUST: Fixed elements respect `safe-area-inset-*`

## Purpose Check

Before keeping a visual container, ask:

- What does this help the user understand or do?
- Does it change hierarchy, grouping, affordance, state, navigation, or domain meaning?
- Would removing it make the screen less usable or less legible?

If the answer is no, remove it. Distinction should come from proportion, typography, spacing, domain-specific structure, and purposeful state treatment, not extra decoration.

## Z-Index

MUST use fixed scale — no arbitrary values like `z-[999]`:

| Layer | Tailwind | CSS Variable |
|-------|----------|--------------|
| Base | `z-0` | — |
| Dropdown | `z-10` | `--z-dropdown: 100` |
| Sticky | `z-20` | — |
| Modal | `z-30` | `--z-modal: 200` |
| Toast | `z-40` | `--z-toast: 400` |
| Tooltip | `z-50` | `--z-tooltip: 300` |

### Avoiding Z-Index

- SHOULD: Use `isolate` (Tailwind) to create stacking context without z-index:

```jsx
<div className="isolate">
  {/* New stacking context, no global z-index conflict */}
</div>
```
