# Layout, spacing and surfaces

Contents: grouping and spacing · alignment · long content and overflow · surfaces and depth · app UI · viewport and stacking.

## Grouping and spacing

- Group with space first, then shared type, then a quiet divider, and a container last. If space already groups it, a border or card around it is furniture.
- The gap between groups is at least twice the gap within one. A heading sits closer to its body than to the content above it.
- Start generous and remove space only for a stated reason ("these must read as one group"), never because it feels empty. Wide screens don't oblige wide content.
- Use Tailwind's spacing scale; no `p-[13px]`. Larger screens get more absolute space between sections, stepped through the scale rather than scaled proportionally.
- Labels are a last resort. An email address, price or phone number explains itself.
- Keep density consistent within a screen: sparse for onboarding, dense for working views.
- A card is for a repeated object, an interactive cluster or a bounded tool, not for filling space. No card inside a card unless the inner one has its own state or action.
- Borderless text and icon controls need about 24px between their glyphs; bordered or filled controls about 12px. Hit areas never overlap.
- Squint at it. You should still name the first and second thing and see the groups. Strong hierarchy uses two or three of size, weight, colour and space at once.

## Alignment

- Pick a few edges and put everything on them. Edges that almost line up and gaps that are almost equal read as mistakes: share the value or make the difference obvious.
- Siblings align their shared parts on one line: titles, descriptions, prices, CTAs. Pin a card's CTA to its bottom with `mt-auto` in a flex column.
- Correct optically where geometry looks wrong: a play triangle shifts toward its point, a button's icon side takes about 2px less padding, a large heading may need `-ml-[0.05em]`, a section often wants slightly more bottom padding than top. Fix an asymmetric glyph in the SVG itself where you can.
- Constrained sections use two elements: the outer one carries the background and vertical padding, the inner one the max width, centring and horizontal padding. Left-aligned sections align to the page container's edge, never to a narrowed `max-w-* mx-auto`. Stacked sections share grid and gap values so column edges line up while scrolling.
- A bento grid has exactly as many cells as items. Reshape it rather than pad it, and prefer three to five deliberate tiles to eight messy ones.
- Visual order matches DOM order. Never reorder content with `order`, `flex-row-reverse` or grid placement.
- Use logical utilities (`ms-*`, `pe-*`, `text-start`, `inset-s-*`) so the layout mirrors in right-to-left languages. Physical sides are for physical geometry such as safe-area insets.

## Long content and overflow

- `min-w-0` on flex children that must shrink below their content, `minmax(0,1fr)` on grid tracks that must, and `shrink-0` on icons, avatars, logos and fixed controls.
- Wrap URLs, emails and long tokens with `wrap-anywhere`, never `break-all`. Truncate filenames, paths and hashes in the middle so the distinguishing end survives. Never truncate numbers, amounts or dates. A truncated value the user needs has a way to the full text.
- Text boxes get `min-h-*`, never a fixed height. Translated strings grow, short labels most, so let rows wrap.
- Hidden content always shows a cue: the next item peeks 16-32px past a scroll edge, or a disclosure control is visible. Fade an edge only when it can actually scroll, and toggle the fade with scroll position.
- An unexpected scrollbar has a source; find it. `overflow-clip` clips without creating a scroll container; use `overflow-hidden` only when you want one.
- Reusable components adapt with `@container`, not viewport breakpoints. `container-type` on a shrink-to-fit box (a flex item, inline-block or absolute element without a width) collapses it to zero; give it a width.
- Keep reading text to 45-75 characters, constrained on the text element (`max-w-[65ch]`), not on its wrapper.

## Surfaces and depth

- The default is content on the canvas. Keep a short ladder (canvas, surface, raised, overlay) with neighbouring steps about 2-4% apart in lightness: distinct, but quiet. Phones need fewer containers and flatter grouping.
- Choose one depth strategy per product: borders only (technical, dense tools), subtle shadows (most products) or layered shadows (design tools, premium). Break it only where elevation means something, such as a popover or a dragged object.
- One light source, from above. Highlights, inner edges and shadows agree with it.
- Draw edges that change with hover, focus or selection as rings (`ring-1 ring-black/5`, an inset shadow); they take no layout space. Keep `border border-transparent` under a shadow ring so forced-colours mode still draws an edge. A semi-transparent border needs `bg-clip-padding`. Never a strong border and a strong shadow together.
- Concentric radii: outer = inner + padding (+ border). Past about 24px of padding, treat the layers as separate shapes. Enforce it with variables: `rounded-(--r) p-(--p)` outside, `rounded-[calc(var(--r)-var(--p))]` inside.
- An accent edge has two jobs: severity on an alert and the current navigation item. Everything else, selected cards and category tiles included, takes a fill or a ring.
- Translucent chrome is for chrome that moving content passes behind; otherwise use a solid fill. Never stack translucent layers. Text on translucency gets more contrast and a little more weight. Where content meets a sticky header, a short masked fade reads better than a hard divider. Honour reduced transparency (raise opacity, drop blur) and `contrast-more:` (near-solid fill, defined edge):

  ```css
  @custom-variant reduced-transparency (@media (prefers-reduced-transparency: reduce));
  ```

- A modal task gets a scrim; a parallel, non-blocking panel does not.
- Decorative layers get `pointer-events-none`.
- No orphan dark band in a light page or the reverse. Step within the page's own palette; a deliberate full dark hero or footer is fine.

## App UI

- Add navigation only when there is somewhere to go. Keep the current location visible and placement consistent, so every screen answers where am I, where can I go and how do I get out. Name items for what they hold ("Library") rather than umbrellas ("Home"), and mirror the user's domain, not the code's modules.
- Empty states teach the product and offer the first action. Skeletons are for first load and mirror the final geometry. On refresh, keep loaded values on screen and update their freshness. A block that fails to load fails alone, keeps its neighbours usable and shows its last good update. Every error, blocked or finished state offers a way forward.
- Give numbers context: what's good, what changed. Colour a change by whether it's good, not by its sign; rising latency is bad. Never show percentage growth from zero; show the absolute change, marked new.
- Body text 14-16px. No display sizes in app chrome.
- Someone should be able to use it for eight hours without fatigue: quiet layer contrast, soft borders, clear resting places for the eye.

## Viewport and stacking

- `h-dvh` and `min-h-dvh`, never `h-screen`; `w-full`, never `w-screen` (`100vw` includes the scrollbar).
- `env(safe-area-inset-*)` is zero unless the viewport meta includes `viewport-fit=cover`.
- Set `scroll-padding-top` to the sticky header's height so anchors and focused elements never land beneath it.
- Use a small fixed z-index scale; no `z-[999]`. `isolate` creates a stacking context without a z-index; put it on the app shell and anywhere else you can say why. No z-index escapes a clipping ancestor, so render menus and popovers in the top layer or a portal.
