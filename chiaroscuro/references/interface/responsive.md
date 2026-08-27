# Interface: Responsive Design

## Mobile-First

Start with the narrowest common layout when that exposes the essential content order, then use Tailwind's `min-width` prefixes to add room-dependent structure:

```html
<!-- Mobile-first: base → sm → md → lg -->
<div class="flex flex-col md:flex-row gap-4 md:gap-8">
```

Mobile-first is an authoring and hierarchy discipline, not a network-performance claim. An existing desktop-oriented system can be adapted incrementally when a wholesale inversion would create unnecessary risk.

---

## Content-Driven Breakpoints

Don't chase device sizes - let content tell you where to break. Start narrow, stretch until design breaks, add breakpoint there.

Three breakpoints usually suffice. Use `clamp()` for fluid values without breakpoints:

```html
<h1 class="text-[clamp(2rem,5vw,4.5rem)]">Fluid Heading</h1>
```

---

## Detect Input Method, Not Just Screen Size

Screen size doesn't tell you input method. A laptop with touchscreen, a tablet with keyboard - use pointer and hover queries:

```html
<!-- Tailwind: fine pointer (mouse, trackpad) -->
<button class="px-3 py-2 pointer-fine:px-2 pointer-fine:py-1.5">

<!-- Tailwind: coarse pointer (touch) - larger targets -->
<button class="min-h-11 pointer-coarse:min-h-12">
```

```css
/* Custom variant in Tailwind v4 */
@custom-variant pointer-fine (@media (pointer: fine));
@custom-variant pointer-coarse (@media (pointer: coarse));

/* Gate hover effects to devices that support hover */
@custom-variant hover-hover (@media (hover: hover) and (pointer: fine));
```

- NEVER: Rely on hover for functionality - touch users can't hover
- MUST: Gate hover styles behind `hover-hover:` or `@media (hover: hover)`

---

## Safe Areas

Modern phones have notches, rounded corners, and home indicators:

```html
<body class="pb-[env(safe-area-inset-bottom)] pl-[env(safe-area-inset-left)] pr-[env(safe-area-inset-right)]">
```

```html
<!-- Enable viewport-fit -->
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

```css
/* With fallback */
.footer { padding-bottom: max(1rem, env(safe-area-inset-bottom)); }
```

---

## Responsive Images

### srcset with Width Descriptors

```html
<img
  src="hero-800.jpg"
  srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
  sizes="(max-width: 768px) 100vw, 50vw"
  alt="Hero image"
  class="w-full object-cover"
>
```

- `srcset` lists available images with actual widths (`w` descriptors)
- `sizes` tells the browser how wide the image displays
- Browser picks the best file based on viewport AND device pixel ratio

### Art Direction with `<picture>`

When you need different crops/compositions (not just resolutions):

```html
<picture>
  <source media="(min-width: 768px)" srcset="hero-wide.jpg">
  <source media="(max-width: 767px)" srcset="hero-tall.jpg">
  <img src="hero-fallback.jpg" alt="..." class="w-full">
</picture>
```

---

## Layout Adaptation Patterns

### Navigation

Desktop nav (header or sidebar) is hidden below `lg`; a hamburger reveals a dialog/disclosure mobile menu. The canonical breakpoint and class hints live in the Tactical Rules → Navigation section below and in [navigation](./data-components.md#navigation). A tablet middle stage (compact icons + labels) is optional, not required.

### Tables

Two valid strategies - choose by data density:

- **Dense/wide tables**: keep one table and let it scroll horizontally (the two-div wrapper). This is the default. See [tables](./data-components.md#tables).
- **Sparse tables (2–4 columns)**: transform to a card stack on mobile when a scroll feels heavier than the data warrants.

```html
<!-- Sparse: card-stack alternative -->
<div class="hidden md:table"><!-- Full table --></div>
<div class="md:hidden space-y-4"><!-- Card stack --></div>
```

### Progressive Disclosure

Use `<details>/<summary>` for content that can collapse on mobile:

```html
<details class="md:open" open>
  <summary class="md:hidden">Show filters</summary>
  <div><!-- Filter content --></div>
</details>
```

---

## Tactical Rules (Tailwind v4)

Concrete breakpoint rules. Audit order: page shell → navigation → text/forms → overflow → component patterns.

### Page Shell

- MUST: Every layout adapts from mobile to desktop via responsive prefixes (`sm:`, `md:`, `lg:`) adjusting columns, spacing, font sizes, and visibility.
- MUST: Multi-column desktop layouts (sidebars, secondary nav, filter panels) collapse to a single column on small screens - use a mobile menu or disclosure, never shrink the columns.
- MUST: Use `min-h-dvh`/`min-h-svh`/`min-h-lvh`, never `min-h-screen`.

### Navigation

- MUST: Every app keeps essential navigation available at narrow widths. Choose a disclosure, dialog, compact bar, or another pattern that fits the information architecture; do not assume `lg` or a hamburger without testing the content.
- MUST: Horizontal menus (tabs, pill navs) never overflow the parent - horizontally scroll when items don't fit.

### Text, Forms, And Touch Targets

- MUST: Body copy and controls remain comfortably readable and operable on mobile. `16px` is a strong baseline for body text and text inputs; dense metadata may be smaller when contrast, typeface, and context keep it legible.
- MUST: If a text input's font size is below `16px`, add `max-sm:text-base/{lh}` to prevent iOS zoom.
- MUST: Small/icon buttons meet the touch-target minimum on coarse pointers - see [interactions.md](./interactions.md) → Touch Targets for the canonical size and hit-area pattern.
- MUST NOT: Fix cramped heading groups by constraining the wrapper with `max-w-*`; constrain each text element directly with `max-w-[*ch]`. See [heading groups](./marketing-components.md#heading-groups).

### Overflow And Flexible Sizing

- MUST: Add `min-w-0` to flex children that must shrink and `shrink-0` to those that must not. See [layout.md](./layout.md) → Flex Sizing.
- MUST: Make tables horizontally scroll when columns won't fit, using the two-div wrapper. See [tables](./data-components.md#tables).

### Component Patterns

- SHOULD: Use container queries when a reusable component's layout genuinely depends on its allocated width rather than the viewport. Place the query container close enough to express that boundary without creating unnecessary containment.
- SHOULD: Reconfigure divider-separated grids at each breakpoint where columns change - reset first/last padding, drop vertical dividers when collapsing to one column, add horizontal dividers between rows.
- SHOULD: Keep wrapped logo clouds balanced on every breakpoint (avoid `5+1`). See [logo clouds](./marketing-components.md#logo-clouds).
- SHOULD: Use `min()` with viewport units for image/screenshot border radii instead of fixed `rounded-*` - e.g. `rounded-[min(1vw,12px)]`.

## Testing

Don't trust DevTools alone. DevTools device emulation misses:

- Actual touch interactions
- Real CPU/memory constraints
- Font rendering differences
- Browser chrome/keyboard appearances

Test on representative real devices when the audience, risk, or available hardware warrants it. At minimum combine responsive browser exercise with keyboard, pointer, touch emulation, zoom, landscape, and slow-device checks where relevant.

---

## Strip Chrome at Smaller Breakpoints

The earn-its-place bar rises as space shrinks. Elements that justified themselves on a wide screen may become furniture on mobile.

- SHOULD: Remove decorative borders, dividers, and container chrome that don't aid comprehension at small sizes
- SHOULD: Collapse wrapper panels into flat content stacks - padding and spacing group content without visual framing
- SHOULD: Simplify multi-level hierarchy to fewer levels on mobile - two levels of nesting rarely survive a narrow viewport
- SHOULD: Let content fill the viewport edge-to-edge where appropriate, rather than inset into cards or panels

The goal is not a stripped-down version - it's the essential version. Mobile should feel intentionally designed, not desktop with pieces removed.

---

## Anti-Patterns

- AVOID: New desktop-only assumptions that make the narrow layout an afterthought.
- NEVER: Device detection instead of feature detection
- NEVER: Separate mobile/desktop codebases
- NEVER: Ignore tablet and landscape orientations
- NEVER: Assume all mobile devices are powerful
- NEVER: Keep decorative containers or visual framing that only served the desktop layout
