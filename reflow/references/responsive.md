# Responsive patterns (Tailwind v4)

Written in Tailwind v4; in another styling system apply the same CSS.

## Input mode

Screen size does not tell you the input. A touchscreen laptop and a tablet with a keyboard both exist. In Tailwind v4, `hover:` already applies only under `@media (hover: hover)`, so hover styles are safe; hover-only *behaviour* (a menu that opens on hover, actions revealed on hover) still needs a tap equivalent. Size by pointer with the built-in `pointer-fine:` and `pointer-coarse:` variants:

```html
<button class="min-h-11 pointer-fine:min-h-8 pointer-fine:px-2">
```

## Touch targets

On coarse pointers every target is at least 44 by 44 CSS pixels, counting invisible hit area. Keep a small visual control small and expand its hit area without overlapping neighbours:

```jsx
<button className="relative">
  <span
    className="absolute top-1/2 left-1/2 size-[max(100%,2.75rem)] -translate-1/2 pointer-fine:hidden"
    aria-hidden="true"
  />
  <Icon className="size-4" />
</button>
```

`2.75rem` is 44px. `pointer-fine:hidden` returns the space to a mouse.

## Navigation and menus

- Essential navigation stays reachable at every width. Choose the pattern from the information architecture (disclosure, dialog, compact bar); do not assume `lg` or a hamburger without trying the content.
- Horizontal menus (tabs, pill navs) never overflow their parent; they scroll horizontally when the items do not fit.

## Tables

- **Dense or wide tables** (the default): one table that scrolls horizontally inside a two-div wrapper. The outer div is `overflow-x-auto whitespace-nowrap` with negative margins cancelling the page padding (`-mx-4 sm:-mx-6 lg:-mx-8 -my-2`); the inner is `inline-block min-w-full align-middle` with matching padding (`px-4 sm:px-6 lg:px-8 py-2`).
- **Sparse tables (2–4 columns)**: a card stack on phones when a scroll is heavier than the data warrants.

## Disclosures

When content collapses on narrow screens, keep its `<summary>` available at every width so resizing keeps both the user's state and a way back:

```html
<details open>
  <summary class="min-h-11 cursor-pointer">Filters</summary>
  <div><!-- filter content --></div>
</details>
```

A class cannot set the `open` attribute. If desktop must show the content permanently expanded, reconcile `open` with the breakpoint in script before hiding the summary, and restore the user's narrow-screen state.

## Text and forms

- Body text around 16px on phones; dense metadata can go smaller when contrast and face keep it legible.
- Fix a cramped heading group by constraining each text element (`max-w-[32ch]`), not the wrapper with `max-w-*`.
- `shrink-0` on icons, images, avatars and fixed-size controls that distort when squeezed.

## Grids, logo rows and radii

- Divider-separated grids are reconfigured at each breakpoint where columns change: reset first and last padding, drop vertical dividers when collapsing to one column, add horizontal dividers between rows.
- Wrapped logo rows and tile grids stay balanced at every breakpoint (3 + 3, not 5 + 1).
- Radii on images and screenshots scale with the viewport: `rounded-[min(1vw,12px)]` rather than a fixed `rounded-*`.
