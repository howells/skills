# Primitives

Small UI primitives. Load the anchor for the primitive in the work.

## Badges

Covers: badges, tags, pills, labels, chips, status indicators, and compact metadata with icons.

- Badges with a leading or trailing icon — never use symmetric `px-*`; use `pl-*`/`pr-*` and set the icon side's padding equal to the vertical padding: `py-1 pr-2 pl-1` (left icon), `py-1 pr-1 pl-2` (right icon)

## Avatars

Covers: profile photos, user thumbnails, testimonial people, comments, team members, and overlapping avatar groups.

- Use `outline-1 -outline-offset-1 outline-black/5` or `outline-black/10` on light surfaces; use `outline-white/10` on dark surfaces
- Give stacked/overlapping avatar groups a 2px `ring` that matches the background color (e.g. `ring-2 ring-white`)

## Icons

Covers: SVG icons, Heroicons, inline checkmarks, icon buttons, icon sizing, and icon alignment with text.

- Never generate raw SVG icons — import from the project's existing icon library, or use Heroicons if no library is established
- Never wrap icons in decorative containers (colored squares, circles with backgrounds) — use the icon directly
- Never scale icons — `viewBox="0 0 24 24"` always uses `size-6`, `viewBox="0 0 20 20"` uses `size-5`, `viewBox="0 0 16 16"` uses `size-4`; if the icon looks too small, use a different icon set, don't increase the size class
- Always use 16px/micro icons (`size-4`) when inline with `text-sm` text — checklists, feature items, comparison tables, inline labels; only use 20px/mini icons (`size-5`) for navigation list icons
- Icons next to a text group (label + supporting text) — align the icon with the first line/label using `items-start` or `items-baseline`, never `items-center` on the group
- Application UIs (dashboards, settings, admin, sidebar nav, forms) — only use Heroicons Micro (16px, `size-4`); never use 20px/mini or 24px/outline icons in application UIs
- Use `size-{n} h-lh` on SVG icons to vertically center them with adjacent text; set the `font-size` on a wrapper element instead of using top margins or manual alignment
- Use `fill-{color}` for filled icons and `stroke-{color}` for stroked icons — never use `text-{color}` with `currentColor` (legacy v2 hack)
- Always add `shrink-0` to icons inside flex containers

## Images

Covers: photos, thumbnails, screenshots, app mockups, product images, media frames, and image borders/outlines.

- Never use borders on photos or thumbnails — use `outline-1 -outline-offset-1 outline-black/5` or `outline-black/10` if the image needs a visible edge
- Use `outline-1 -outline-offset-1 outline-black/5` or `outline-black/10` on light surfaces; use `outline-white/10` on dark surfaces for screenshots and app UI mockups
- Use `alt=""` on images when the subject is identified by adjacent visible text

## SVG

Covers: inline SVG, SVG color styling, `fill`, `stroke`, `currentColor`, and SVG markup conventions.

- Omit `xmlns` on inline `<svg>` elements in HTML/JSX — only needed when the SVG is a standalone `.svg` file
- Style SVG colors with Tailwind classes (`fill-*`, `stroke-*`, `text-*` with `fill="currentColor"`/`stroke="currentColor"`) instead of hardcoded color attributes or inline ternaries — use `data-*`/`aria-*` variants or conditional classes to switch colors
- Never combine `fill="currentColor"`/`stroke="currentColor"` attributes with `fill-*`/`stroke-*` classes on the same element — the attribute conflicts with the class; use `fill-current`/`stroke-current` to inherit the text color, or drop the attribute entirely when using a specific color class like `fill-zinc-400`

## Overflow Edges

Covers: horizontally scrolling chip rows, tab bars, carousels, wide tables, and code blocks — anything that clips at a container edge.

- Fade overflowing content at the container edge instead of hard-clipping it — the fade is the affordance that says "more this way". Tailwind v4.1 mask utilities: `mask-r-from-85%` (fade the right edge), `mask-x-from-90%` (both edges); raw CSS: `mask-image: linear-gradient(to right, transparent, black 15%, black 85%, transparent)`
- Only mask edges that can actually scroll — a faded edge on fully visible content falsely signals hidden items; if both states occur, toggle the mask based on scroll position

## Border Radius

Covers: rounded cards, panels, buttons, images, screenshots, nested surfaces, and any UI element where radius consistency matters.

- Use concentric border radii on closely nested rounded elements — define the relationship explicitly with CSS variables and `calc()` so the math is enforced, e.g. `rounded-(--radius) p-(--padding)` on the outer element, `rounded-[calc(var(--radius)-var(--padding))]` on the inner
- Use `min()` with viewport units for image/screenshot border radii instead of fixed `rounded-*` values — e.g. `rounded-[min(1vw,12px)]`; the radius should match the intended value at full desktop width and scale proportionally as the screen shrinks
