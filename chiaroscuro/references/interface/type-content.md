# Type & Content

Copy, prose, and font-loading rules. Load the anchor for the concern in the work. Baseline type hierarchy lives in `typography.md`.

## Copywriting

Covers: headings, taglines, subtitles, descriptions, labels, list items, button text, and other UI copy.

- Headings — periods or no periods are both fine, but be consistent within a page
- Always use proper punctuation (ending period) on full sentences and paragraphs
- Use a period on any descriptive text that stands alone — taglines, subtitles, tier descriptions like "For professionals and growing teams.", single-line descriptions like "For organizations that need more power and control."
- Only omit periods on items in a list — e.g. feature bullet points in pricing cards
- Never use emojis anywhere — not in headings, descriptions, buttons, labels, or any other text

## Prose Content

Covers: raw HTML from markdown, CMS content, database content, blog posts, articles, documentation, and rendered markup where classes cannot be applied to individual elements.

- Never use the `@tailwindcss/typography` plugin — instead, create a `.prose` class that styles raw HTML elements (headings, links, lists, code blocks, images, etc.) using plain CSS with Tailwind's CSS theme variables (`var(--color-*)`, `var(--text-*)`, `var(--font-weight-*)`, `var(--radius-*)`, `--spacing(*)`, `--alpha()`); use `@variant dark { … }` and `@variant hover { … }` for dark mode and hover states; use `* + *` for vertical spacing between elements; style every element that could appear in the rendered markup — `h1`–`h6`, `p`, `a`, `ul`, `ol`, `li`, `pre`, `code`, `img`, `strong`, `blockquote`
- Apply the `.prose` wrapper class to the container element that holds the rendered HTML — `<div class="prose">` around blog post content, markdown output, CMS-generated markup, or any HTML where you can't add Tailwind classes to individual elements
- Default to `var(--text-base)` (`16px`) for prose body text; only use `var(--text-lg)` (`18px`) or larger if specifically requested or the project already uses that size for body text elsewhere
- Never set `max-width` inside the `.prose` CSS — constrain width with a `max-w-[*ch]` class alongside `prose` in the markup (e.g. `<div class="prose max-w-[65ch]">`); use `60ch`–`90ch`, matched to the site's existing content widths
- Set prose body `line-height` to at least `1.75` times the font size — e.g. `--spacing(7)` for `var(--text-base)`
- Use `text-pretty` on blog post and article titles, not `text-balance` — long editorial titles can wrap to several lines, where `text-balance` (which evens line lengths, best for short 2-3 line headings per `typography.md`) tends to produce awkward top-heavy breaks; `text-pretty` only fixes orphans
- When the article title/`h1` uses a sans-serif font, use the same sans-serif for all subheadings (`h2`–`h6`) within the article — never mix a sans-serif title with serif subheadings

## Custom Fonts

Covers: loading custom fonts, registering font theme variables, and applying display/body font utilities.

- Always load custom fonts before using them — add `<link>` tags in the HTML `<head>` (preferred); if no `<head>` is available, use `@import url('…');` at the top of the CSS file instead
- Register frequently used custom fonts in the CSS `@theme` block — e.g. `--font-display: "Oswald", sans-serif;`; optionally set `--font-display--font-feature-settings` and `--font-display--font-variation-settings` for fine-tuning
- Register headline/display fonts as `--font-display` (creates a `font-display` utility) — use `--font-sans` for body/UI fonts and `--font-display` for fonts that are only used on headings and display text; apply `font-display` on headings alongside `font-sans` on the body
