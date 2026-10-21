# Interface: Typography

Typeface choice, pairing, the type ramp, tracking, rendering (smoothing, optical sizing) and OpenType features belong to `typecase`, which carries the font recommendations and the OpenType reference. This file keeps the visual rules that apply while building any screen.

## Weight

| Usage | Weight |
|-------|--------|
| Body minimum | 400 |
| Headings | 500–600 |

- MUST: No weight change on hover or selection; it shifts layout.
- MUST NOT: `font-bold` for headings in product UI. Prefer `font-semibold` or `font-medium`.

## Headings and Wrapping

- MUST: `text-balance` on short headings and `text-pretty` on paragraphs and long editorial titles. In dense UI, use `truncate` or `line-clamp-*`.
- MUST NOT: Add `leading-*` to headings unless a layout edge case requires it.
- SHOULD: Keep a display headline compact enough to read as one idea. Fix awkward wrapping by reconsidering copy, measure and size together rather than only shrinking the font.
- MUST: Check italic display words for clipped descenders (`g j p q y`); tight leading cuts them off.

## Size and Measure

- MUST NOT: `text-xs` for body copy. Default to at least `text-sm`, and `text-base` on mobile inputs.
- SHOULD: Constrain long-form text with `max-w-[*ch]` directly on the text element.

## Caps, Mono and Figures

- MUST NOT: Small caps, tracked uppercase or decorative mono (Hard Rule 1 in `SKILL.md`). Existing styling, a technical subject or an available mono token is not an exception. Use sentence case for ordinary UI text.
- MUST: Mono only for literal code, identifiers and values whose characters need inspection. Aligned figures use `tabular-nums` in the body font.
- MUST: Inspect inherited styles as well as new classes. A shared component can reintroduce mono, caps or tracking even when the caller contains none.

## Font Loading

Text never goes invisible while a font loads, and the swap never reflows the page. `typecase` carries `font-display`, preloading, fallback metrics and subsetting.

## Dark Mode

- SHOULD: Increase `line-height` slightly for light text on dark backgrounds; light text reads thinner and needs more room.

## Selection

- SHOULD: Style `::selection` from the accent at low opacity with `color: inherit`. Gradients are not supported on `::selection`.
