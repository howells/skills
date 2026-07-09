# Marketing Components

Component rules for marketing and landing-page sections. Load the anchor for the component in the work.

## Landing Pages

Covers: landing pages, marketing pages, stacked page sections, heroes, CTAs, pricing sections, feature sections, and full-page consistency.

- Reuse the same primary/secondary button styling across the entire page — if the hero uses a link-style secondary, every other section with a secondary action (CTA, pricing, etc.) must also use a link-style secondary
- Reuse the same font treatment (size, weight, color) when the same or similar idea appears multiple times on a page — match the existing instance exactly
- Use the same container style across the entire page — once a container style is established (outline, tinted, etc.), all subsequent containers should match
- Use the same border radius for all containers at the same level — panels, cards, and other sibling containers on a page should share a consistent radius
- Use the same column `gap-*` value across all multi-column page sections — card grids, split layouts, and any other two-column or multi-column section must share the same gap; check existing sections before adding a new one and match the value already in use
- Never place a centered/center-constrained layout directly below a left-aligned layout — use left-aligned instead, unless: the section above ends with full-width containers that create a natural divide, a background color change separates them, or a visible divider sits between
- Never have more centered heading groups than left-aligned ones on a landing page — centered headings work best for hero sections, CTAs, and sections with symmetrical content beneath (e.g. centered pricing cards, logo clouds); default to left-aligned for feature grids, split layouts, and content-heavy sections

## Headers

Covers: site headers, navigation bars, top bars, logos, mobile menus, hamburger menus, and header CTAs.

- Always wrap the main logo in an `<a href="/">` with `aria-label="Homepage"`
- Navbar button actions must always feel secondary to the hero's primary CTA — use ghost, outline, subtle, or a smaller solid button; matching the hero's color is fine if the navbar button is noticeably smaller

## Footers

Covers: page footers, footer logos, footer navigation, footer links, and social media icons.

- Logo height between `h-5` and `h-7`
- Use `font-normal` for footer links
- Social media icons must be at least `text-gray-600` — never use `text-gray-400` or lighter
- Never create logos from scratch with HTML or icons; use a real logo asset (or a placeholder image) when none is provided

## Heading Groups

Covers: headline, subheadline, and optional eyebrow groups at the top of marketing or landing page sections.

A heading group is a headline and subheadline (and optional eyebrow) at the top of a marketing or landing page section — e.g. the title and description above a feature grid, team grid, pricing table, testimonial section, CTA, or hero. These rules apply to promotional/marketing page sections only, not to blog posts, articles, documentation, or editorial content.

- Never constrain the width of a heading group wrapper — no `max-w-*`, no `max-lg:max-w-*`, no width constraints of any kind on the wrapper `<div>`. Always constrain each text element (headline, subheadline) individually with `max-w-[*ch]` directly on the element — `text-base` → `max-w-[56ch]`, `text-lg` → `max-w-[48ch]`, `text-xl` → `max-w-[40ch]`, `text-2xl`–`text-3xl` → `max-w-[40ch]`, `text-4xl` → `max-w-[35ch]`, `text-5xl` → `max-w-[30ch]`, `text-6xl` → `max-w-[24ch]`, `text-7xl` → `max-w-[20ch]`.

  Example:

  ```html
  <div class="/* never add a max width here */">
    <h2 class="mx-auto max-w-[35ch] text-4xl font-semibold tracking-tight text-balance">…</h2>
    <p class="mx-auto mt-6 max-w-[48ch] text-lg text-pretty text-gray-600">…</p>
  </div>
  ```

- Always use a left-aligned layout for heading groups when the subheadline exceeds ~120 characters (~3 lines when centered)
  - **⚠️ ask-user** if a centered layout is requested but the subheadline exceeds ~120 characters — offer a rewritten version that fits; only center if the user accepts the shorter copy

## Feature Lists

Covers: feature grids, benefit lists, product feature sections, and any section listing multiple features with titles and descriptions.

- Use `<dl>`, `<dt>`, and `<dd>` elements for feature sections that list multiple features — not `<ul>`/`<li>` or plain `<div>` groups

## Testimonials

Covers: customer quotes, reviews, social proof sections, testimonial cards, quote punctuation, avatars, and attribution.

- Use hanging punctuation for quotes — `relative before:absolute before:inline before:-translate-x-full before:content-['\201C'] after:inline after:content-['\201D']`
- Always bottom-align avatars/names across equal-height testimonial cards — `flex flex-col justify-between` on each card; group quote content and attribution in their own wrapper elements
- Never add whitespace around quote content in `<p>` tags — write `<p>The quote text</p>` not `<p> The quote text </p>` (breaks hanging punctuation)
- Follow the avatar rules in [`primitives.md`](./primitives.md#avatars) for testimonial photos
- Use unisex names when photos are random/placeholder, so names work for any photo

## Team Sections

Covers: team grids, team member cards, staff listings, about-us sections, people galleries, photos, names, roles, and bios.

- Never use landscape aspect ratios for team member images
- Use a muted color for role/job title text
- Render lists of people in a `<ul>` with `<li>` elements
- Use `alt=""` on team member photos when the person's name is visible nearby

## Logo Clouds

Covers: logo grids, customer logos, partner logos, trust bars, client rows, and collections of brand marks.

- Always distribute logos evenly across rows when wrapping — never allow an unbalanced last row (e.g. 5 on one row and 1 on the next); use a grid or layout that splits logos as evenly as possible across all rows (e.g. 3+3 instead of 5+1 for 6 logos)
- Logo clouds directly beneath a hero are an extension of the hero — match the hero's alignment; left-aligned hero → left-aligned logo cloud label and logos

### Marquee Logo Rows

When a logo row loops (marquee), the mechanics that keep it from reading as glitchy:

- Duplicate the item sequence exactly once and animate the track `translateX(0)` → `translateX(-50%)` with linear easing — the halfway point is identical to the start, so the loop is seamless with no visible reset
- Keep item widths stable so the -50% midpoint stays exact
- Fade both ends with an edge mask (`mask-x-from-90%`, see `primitives.md`: Overflow Edges) so logos don't pop in and out at the container boundary
- Pause on hover only if the logos are links; pause when off-screen always (see `animation.md`)

## Login Pages

Covers: login, sign-in, sign-up, authentication, password reset, and account access pages.

- Never use light gray or other light-tinted backgrounds (e.g. `bg-gray-50`, `bg-gray-100`, `bg-slate-50`) on login/sign-in pages — use solid white (`bg-white`) or dark (`bg-gray-900`, `bg-gray-950`, `bg-black`), unless the form content is wrapped in a distinct panel or card
