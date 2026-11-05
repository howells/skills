# Colour and dark mode

Contents: system · ramps · meaning · contrast · dark mode.

## System

- Reuse the project's tokens and notation; a consistent hex system beats hex with stray `oklch()` values. A new system is written in OKLCH in `@theme`.
- One neutral ramp, one accent ramp, and only the status ramps the product renders. A second accent earns its place only when two things must be told apart at a glance.
- Two tiers. Primitives are named by hue (`--color-brand-600`) and never used in components; semantic tokens are named by role (`--color-text-secondary`, `--color-surface`) and are what components use. Role names that evoke the product's world (`--ink`, `--paper`) beat template names.
- Never borrow a token because its value is right today. A border token used as text colour breaks when borders get lighter; add the missing role instead.
- Follow the project's neutral family. Never mix `gray`, `slate`, `zinc` and `neutral`.
- Two shades that are almost the same are one token used twice, or drift. Pick one.
- Never invent colours on the fly.

## Ramps

- Hold the hue and move lightness. Chroma peaks mid-ramp and falls toward both ends; high chroma at very light or very dark steps looks harsh or clips. HSL hue angles don't carry over to OKLCH.
- Step the light end more finely, about 0.04-0.05 in lightness per step from 50 to 200.
- Across hues, match lightness step for step and set chroma as the same proportion of each hue's own maximum. Copying one chroma number across hues leaves yellows weak beside reds.
- Tint neutrals toward the brand hue at chroma 0.005-0.015, warm or cool but never both. Pure grey looks dead. No pure black text; use something like `oklch(0.15 0.01 h)`.
- Choose the page ground deliberately: pure white for crisp product and form screens, a faint tint such as `oklch(0.98 0.005 h)` for long reading.

```css
@theme {
  --color-brand-50: oklch(0.97 0.02 250);
  --color-brand-200: oklch(0.86 0.07 250);
  --color-brand-500: oklch(0.55 0.15 250);
  --color-brand-700: oklch(0.39 0.12 250);
  --color-brand-950: oklch(0.18 0.06 250);
}
```

- Declare a vivid P3 colour after its sRGB value, inside `@media (color-gamut: p3)`.
- Gradients interpolate `in oklab` by default; use `in oklch` when a two-hue gradient greys out in the middle. Fade content with `mask-image`, not an overlaid gradient. Keep text off gradients where you can.

## Meaning

- One colour, one meaning across the interface. Hues within about 15° read as the same colour, so status hues sit at least 15° from the accent.
- Colour draws attention, so spend it: one accent per view, mostly on the primary action. Fill the primary action's background; accent-coloured text on a neutral button reads as a link.
- Action colours stay interactive. Nothing static wears them.
- Never colour alone: pair it with an icon, label or position. The screen still reads in greyscale.
- Grey text on a coloured ground looks washed out; use a darker shade of that ground's hue.
- Alpha is fine for hairline rings and deliberate overlay steps (`ring-black/5`, `bg-white/10`). As a stand-in for missing palette shades it gives unpredictable contrast.

## Contrast

- WCAG AA is the floor: 4.5:1 for text, 3:1 for large text (24px, or 18.67px bold), 3:1 for control boundaries, states and meaningful graphics. Placeholder text counts. Decorative elements and inactive controls are exempt.
- Within the floor, contrast sets depth. Primary text 12-21:1 dark on light (7-12:1 light on dark), supporting text 4.5-7:1, dividers and quiet fills 1.1-1.5:1. Something minor that shouts, or something important that fades, is a defect even when every ratio passes.
- Measure the rendered pair against what is actually behind it: alpha, `color-mix()`, a translucent header over scrolling content, text on an image (measure the worst region or add a scrim).
- `text-white` on a Tailwind `500` fill usually fails 4.5:1; move the fill to `600`.
- Hover, active and focus states are at least as legible as rest.
- To fix a failing pair, change lightness; hue barely moves contrast.

## Dark mode

- A second design, not an inversion. Keep the contrast relationships and hierarchy and re-derive the values: lower the accent's chroma a step or two (what's confident on white is neon on near-black), widen separation at the dark end, and remeasure every pair.
- Swap semantic tokens in one block, with one switching mechanism. Default to Tailwind's `dark:` variant on `prefers-color-scheme`; add a manual toggle only when asked, and then use a class everywhere. A media query driving some tokens and a class driving others half-themes the page.
- Cards sit slightly lighter than the page (`dark:bg-gray-900` on `gray-950`) with `dark:inset-ring dark:inset-ring-white/5`. Drop light-mode shadows that turn muddy; keep a re-tuned one only where it explains overlap.
- Give light text on dark a little more line height.
- `color-scheme: dark` (`scheme-only-dark` on `<html>` for dark-only sites) so scrollbars and native controls follow. One `<meta name="theme-color">` per scheme, matching the top of the page. Give native `<select>` an explicit background and text colour for Windows dark mode.
- Prevent a flash of the wrong theme with server-provided state or an early bootstrap, and disable transitions for the frame of a theme switch.
- Inline SVG takes `dark:fill-*` and `dark:stroke-*`. External SVGs and raster images that don't hold up on dark (photos, screenshots, mockups, textures) need real `-dark` files with the same composition; `invert` or `brightness` filters are never the final treatment. Identify which images need variants and wire them in; generating them is image work outside this skill.
- Make ornaments such as quote marks very faint (`dark:text-white/5`).
- Under `prefers-contrast: more`, give each appearance its own stronger value.
