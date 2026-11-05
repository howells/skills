# Type in use

The type ramp, pairing and OpenType features belong to `typecase`. These are the rules that apply while building any screen.

## Roles and hierarchy

- Each piece of text has one role (title, body, label, value, action, metadata) and looks the same everywhere. Three sizes or fewer per section; try weight, colour, space or position before another size.
- Headings at 500-600; no `font-bold` in product UI. Body at least 400.
- No weight change on hover, selection or the active navigation item; it shifts layout.
- Heavy elements (bold icons, large text) sit at lower contrast so they don't overpower what's beside them.
- Visual and document hierarchy are separate. An `<h2>` can look quiet; heading levels still run in order for assistive technology.
- Labels at 12-13px in the body face, sentence case. No `text-xs` body copy. Inputs on phones are at least 16px (`max-sm:text-base`), or iOS zooms on focus.
- Inspect inherited styles as well as new classes. A shared component can reintroduce mono, caps or tracking the caller never asked for.
- Large display text tightens its tracking slightly; body stays near zero. This is never licence for tracked uppercase.

## Wrapping and measure

- `text-balance` on short headings, `text-pretty` on paragraphs and long editorial titles, `truncate` or `line-clamp-*` in dense UI.
- Leave `leading-*` off headings unless an edge case needs it, and check italic display descenders (`g j p q y`) aren't clipped by tight leading.
- Fix an awkward display wrap by reconsidering copy, measure and size together, not only by shrinking the font.
- Style `::selection` from the accent at low opacity with `color: inherit`.

## Detail

- `…` not `...`, curly quotes, and an ellipsis on actions that ask a follow-up and on progress ("Rename…", "Saving…").
- Non-breaking spaces glue units and shortcuts: `10 MB`, `⌘ K`.
- `tabular-nums` wherever numbers change or line up, in the body face.
- Dates, numbers and currency through `Intl`; plurals through `Intl.PluralRules`, never "1 members". Relative times switch to absolute dates after about a week.
- `translate="no"` on brand names, code and identifiers so page translation leaves them intact.
- No emoji in interface text.

## Rich text

For rendered markdown, CMS or database HTML where classes can't go on each element:

- Use the project's rich-text treatment when it is coherent. A local `.prose` class built from theme variables gives precise control; `@tailwindcss/typography` is fine when already accepted and themed deliberately.
- Body at `var(--text-base)` unless the project already uses larger body text, with line height at least 1.75 (`--spacing(7)` at 16px).
- Never set `max-width` inside `.prose`; constrain it in markup alongside the class (`prose max-w-[65ch]`), matched to the site's content widths.
- Article titles take `text-pretty`, not `text-balance`, which makes long titles top-heavy.
- A sans-serif article title means sans-serif subheadings too.

## Custom fonts

- Load fonts through the framework's font path or self-host them with preload; avoid CSS `@import`. Text never goes invisible while a font loads, and the swap never reflows the page.
- Register fonts in `@theme`: `--font-sans` for body and UI, `--font-display` for faces used only on headings and display text.
