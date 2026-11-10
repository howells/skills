# Tailwind authoring

## Markup

- `text-*` and `leading-*` go on block-level text containers, not inline tags, unless the inline element is acting as one.
- No redundant display classes (`block` on a `<div>`), and no conflicting classes for one property unless a variant separates them.
- A list stays a `<ul>` or `<ol>`; add `role="list"` when its list styling is removed.
- `antialiased` on the app root; `isolate` on the main app shell.
- A wrapper with only visual styling that can go without losing clarity goes.

## Class preferences

- `gap-*` on the parent over margins between flex or grid children.
- `size-*` over matching `h-*` and `w-*`; `p-6` over matching axis classes. Split axes only when they differ.
- Scale values over arbitrary ones; `z-50` over `z-[50]`; slash opacity (`bg-neutral-950/5`).
- Arbitrary radii, spacing and colours reference tokens, not raw pixels. Arbitrary font sizes in `rem`.
- `not-*` variants over a base class immediately overridden; named variants (`data-closed:*`) over bracket syntax.
- v4 names: `bg-linear-*` not `bg-gradient-*`, `shrink-*` and `grow-*` not `flex-shrink-*`.
- No named line heights (`leading-tight`) in product UI; scale-backed values (`leading-6`) or `text-sm/6` shorthands.
- Readable whole-number ratios in arbitrary grid tracks.

## Variables and custom CSS

- `--spacing(n)` rather than `calc(var(--spacing) * n)`.
- CSS variables for arbitrary colours; never `theme()` in authored UI code.
- Dynamic values through an inline variable read by a class: `class="w-(--progress)" style="--progress: 72%"`.
- `@utility` rather than ad hoc class selectors; parameterise repeated patterns with `--value()` and `--modifier()`. Never nest `@utility` inside `@media` or `@supports`.
- `@custom-variant` only for genuinely new conditions.
- Remote `@import` URLs come before `@import "tailwindcss"`.
- `content-visibility: auto` can defer long off-screen sections; give it a realistic `contain-intrinsic-size` and check scroll anchoring.
