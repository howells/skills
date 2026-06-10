# Interface: Dark Mode

Covers: dark-mode styling, light-to-dark conversion, dark-mode contrast, dark-mode surfaces, and dark-mode images/SVGs.

Dark mode is not an inversion. It is a second design that preserves the *contrast relationships* of the light design while looking good on a dark canvas. It does not need to preserve every light-mode detail.

## Design Rules

- MUST: Maintain the same contrast ratios as light mode — re-derive colors, never just invert.
- SHOULD: Default to the OS preference via Tailwind's built-in `dark:` variant (`prefers-color-scheme`). Add a manual toggle only when the user explicitly asks for one.
- MUST: Remove all shadows in dark mode — use `dark:shadow-none`. Separation comes from the surface ladder and faint inset rings, not elevation.
- MUST: On dark-only sites, add `scheme-only-dark` to `<html>` (or the top-level element) so native elements — scrollbars, form controls, `color-scheme` — render dark.

## Surface And Component Rules

- MUST NOT: Keep large branded or colored panels in dark mode. Use the page background and separate sections with a light divider instead.
- SHOULD: Style cards only slightly lighter than the page (e.g. `dark:bg-gray-900` on a `dark:bg-gray-950` page); add `dark:inset-ring dark:inset-ring-white/5` for definition.
- SHOULD: Make decorative quote marks and similar ornaments very faint (e.g. `dark:text-white/5`).
- MUST NOT: Use multiple heading text colors in dark mode (e.g. dark gray + brand). Use one light color — `white` or `gray-100` — for all heading text.

## SVG Rules

- MUST: For inline `<svg>`, style dark mode with Tailwind `dark:*` classes (`dark:fill-*`, `dark:stroke-*`, `dark:text-*`).
- MUST: For external SVG files referenced via `<img>`, create a real dark variant alongside the original (e.g. `logo.svg` + `logo-dark.svg`). Never substitute CSS filters (`invert`, `brightness`) or opacity for a true dark variant.

## Raster Image Rules

- MUST: Audit the page for rasterized images that need dark variants — photos, screenshots, product mockups, decorative backgrounds, textures, and rasterized illustrations.
- MUST NOT: Use CSS filters (`invert`, `brightness`, `contrast`, `opacity`) as the final dark treatment for raster images. Generate real dark-mode image files.
- A true dark variant keeps the original dimensions, composition, softness/fades, and foreground hues; only background and lightness shift so the image reads on a dark canvas. Save it with a `-dark` suffix (e.g. `bg.jpg` → `bg-dark.jpg`) and wire it into the dark UI.

Note: generating raster image assets is outside chiaroscuro's code-focused scope. When a real dark image file is required, hand off to a dedicated image-generation workflow (the standalone `dark-mode-image` skill, which in turn uses `imagegen`, is the intended handoff where available). Chiaroscuro's job is to identify which images need variants and wire the results in — not to render pixels.

## Workflow

1. Inspect the existing UI and the project's Tailwind conventions.
2. Convert markup to include appropriate `dark:*` classes following the rules above.
3. Audit raster images and inline/external SVGs for dark variants.
4. Hand off raster variant generation; style SVGs inline.
5. Verify both modes for contrast, missing variants, and images that still assume a light background.
