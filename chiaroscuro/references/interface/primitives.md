# Primitives

Small UI primitives. Load the anchor for the primitive in the work.

## Badges

Covers: badges, tags, pills, labels, chips, status indicators, and compact metadata with icons.

- Badges with a leading or trailing icon - never use symmetric `px-*`; use `pl-*`/`pr-*` and set the icon side's padding equal to the vertical padding: `py-1 pr-2 pl-1` (left icon), `py-1 pr-1 pl-2` (right icon)
- Badges never wrap: `whitespace-nowrap shrink-0`, and decide which sibling yields instead
- Badges are static information. A chip that selects, filters or removes is a real `<button>` or checkbox with its state exposed

## Avatars

Covers: profile photos, user thumbnails, testimonial people, comments, team members, and overlapping avatar groups.

- Use `outline-1 -outline-offset-1 outline-black/5` or `outline-black/10` on light surfaces; use `outline-white/10` on dark surfaces
- Give stacked/overlapping avatar groups a 2px `ring` that matches the background color (e.g. `ring-2 ring-white`)
- Fall back to initials when the image fails to load, and use `object-cover` so any source ratio fills the frame. Build initials from the first grapheme of the first and last words (`Intl.Segmenter`), not `[0]`, which breaks on emoji and combining characters; fall back to an icon when there is no name

## Icons

Covers: SVG icons, Heroicons, inline checkmarks, icon buttons, icon sizing, and icon alignment with text.

- Import from the project's existing icon family. Add a raw or custom SVG only when the domain needs a mark the family cannot supply.
- Do not wrap icons in decorative containers by default. A container is justified when it communicates a control boundary, state, category, or brand mark.
- Size icons by optical weight, adjacent type, touch target, and the family's intended grid. Do not mix outline weights or enlarge a weak glyph until it looks unlike its siblings.
- Icons next to a text group (label + supporting text) - align the icon with the first line/label using `items-start` or `items-baseline`, never `items-center` on the group
- Use `size-{n} h-lh` on SVG icons to vertically center them with adjacent text; set the `font-size` on a wrapper element instead of using top margins or manual alignment
- Use `fill-*` and `stroke-*` for explicit icon colors. `currentColor` is appropriate when an icon should inherit the surrounding control or text color.
- Always add `shrink-0` to icons inside flex containers

## Images

Covers: photos, thumbnails, screenshots, app mockups, product images, media frames, and image borders/outlines.

- Use the product's own imagery: its objects, its photography, its screenshots. Choose a set that agrees in light, colour temperature, ratio and crop, and look at the set together before using it. Each image shows the object its label names. No image is better than stock filler, a fashionable mood shot or the wrong object.
- Never use borders on photos or thumbnails - use `outline-1 -outline-offset-1 outline-black/5` or `outline-black/10` if the image needs a visible edge
- Use `outline-1 -outline-offset-1 outline-black/5` or `outline-black/10` on light surfaces; use `outline-white/10` on dark surfaces for screenshots and app UI mockups
- Use `alt=""` on images when the subject is identified by adjacent visible text
- Choose aspect ratio from the source material and layout role. Preserve a stable ratio to prevent layout shift; use consistent square or landscape crops for repeated grids, but do not force every image into one recipe or reject 16:9 when the content is natively widescreen.
- Pair `object-cover` with an `object-position` chosen for each image, so the crop keeps its subject

## SVG

Covers: inline SVG, SVG color styling, `fill`, `stroke`, `currentColor`, and SVG markup conventions.

- Omit `xmlns` on inline `<svg>` elements in HTML/JSX - only needed when the SVG is a standalone `.svg` file
- Style SVG colors with Tailwind classes (`fill-*`, `stroke-*`, `text-*` with `fill="currentColor"`/`stroke="currentColor"`) instead of hardcoded color attributes or inline ternaries - use `data-*`/`aria-*` variants or conditional classes to switch colors
- A `fill-*` or `stroke-*` class overrides a `fill`/`stroke` presentation attribute on the same element, but not one set on a child path. When a colour will not change, inspect which element actually paints

## Overflow Edges

Covers: horizontally scrolling chip rows, tab bars, carousels, wide tables, and code blocks - anything that clips at a container edge.

- When a horizontally scrolling region needs a visual continuation cue, an edge fade can communicate "more this way". Keep controls and meaningful text fully legible; a scrollbar, partial item, or explicit control may be clearer.
- Only mask edges that can actually scroll - a faded edge on fully visible content falsely signals hidden items; if both states occur, toggle the mask based on scroll position

## Border Radius

Covers: rounded cards, panels, buttons, images, screenshots, nested surfaces, and any UI element where radius consistency matters.

- Use concentric border radii on closely nested rounded elements - define the relationship explicitly with CSS variables and `calc()` so the math is enforced, e.g. `rounded-(--radius) p-(--padding)` on the outer element, `rounded-[calc(var(--radius)-var(--padding))]` on the inner
- Scale large media radii when a fixed desktop radius looks exaggerated on narrow screens. `min()` with viewport units is one available technique, not a requirement for every image.
