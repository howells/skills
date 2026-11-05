# Marketing pages

Contents: composition · furniture · consistency · heading groups · sections and components · pricing.

## Composition

- The page is a narrative. Each section has one purpose and advances the decision; cut to the fewest sections that tell the whole story. Five well-paced sections beat ten relentless ones.
- Section rhythm matters more than any single section. Alternate weight: dense then spacious, text then visual. Never three-column cards three times running.
- Transitions between sections come from pacing, a shift in surface or a change of content, not ornamental rules, gradient dividers or patterned strips. After a strong background change, the next section visibly resets the rhythm.
- The hero says the value in one sentence, has one dominant action and at most one clearly secondary one, and picks one pattern: text-led, split with a real visual, full-bleed media or a live demo.
- Over full-bleed media, anchor the copy low or to a deliberate edge so the image keeps its dominance. Use a directional wash (`bg-linear-to-t from-black/60 via-black/20 to-transparent`), not a flat scrim, and keep supporting blocks low-fill so they sit on the image instead of boxing it.
- Social proof: real names, photos and companies; specific outcomes ("Cut deploy time from 45 minutes to 2"); monochrome logos at consistent size; a testimonial placed after the claim it supports. No invented testimonials, context-free star ratings or auto-advancing carousels.
- Motion may run longer than in product UI, but no scroll-triggered fade-ups, parallax or scroll hijacking.

## Furniture

Generated landing pages reach for these to look designed. Leave them out unless the brief genuinely calls for one.

- Gradient blobs, floating shapes, accent badges, background effects filling space.
- A bento grid with an empty or filler cell.
- Tags laid over photos; invented photo credits or plate numbers as captions. Credit a real photographer or write a plain caption.
- Image pagination labels (`01 / 4`).
- Logos built from HTML or icons; use the real asset or a placeholder image.
- Auto-playing video without consent.

## Consistency

- One primary and one secondary button style across the page. If the hero's secondary is a text link, every secondary is.
- The same idea in the same type treatment everywhere it recurs.
- One container style and one radius for containers at the same level.
- One column gap for every multi-column section; match what exists before adding a section.
- No centred layout directly below a left-aligned one, unless a full-width element, a background change or a divider separates them. Left-aligned heading groups outnumber centred ones; centre heroes, CTAs and symmetrical content such as pricing and logo clouds.
- Header actions keep the page's hierarchy: quieter than the hero's primary on a conversion page.

## Heading groups

A headline and subheadline above a marketing section. Never constrain the wrapper; constrain each text element with `max-w-[*ch]`: `text-base` 56ch, `text-lg` 48ch, `text-xl` to `text-3xl` 40ch, `text-4xl` 35ch, `text-5xl` 30ch, `text-6xl` 24ch, `text-7xl` 20ch.

```html
<div>
  <h2 class="mx-auto max-w-[35ch] text-4xl font-semibold text-balance">…</h2>
  <p class="mx-auto mt-6 max-w-[48ch] text-lg text-pretty text-gray-600">…</p>
</div>
```

Left-align a heading group whose subheadline runs past about three centred lines.

## Sections and components

- **Header:** the logo links home (`<a href="/" aria-label="Homepage">`).
- **Footer:** logo `h-5` to `h-7`, links `font-normal`, social icons no lighter than `text-gray-600`.
- **Features:** list several features as `<dl>`, `<dt>`, `<dd>`.
- **Testimonials:** hanging quote marks with `relative before:absolute before:-translate-x-full before:content-['\201C'] after:content-['\201D']`, and no whitespace inside the `<p>`. Bottom-align attribution across equal-height cards (`flex flex-col justify-between`). Use unisex names with placeholder photos.
- **Team:** portrait or square photos, never landscape; muted role text; a `<ul>` of people; `alt=""` when the name is beside the photo.
- **Logo clouds:** balance wrapped rows (3 and 3, not 5 and 1). Beneath a hero, match its alignment. A marquee duplicates the sequence once and animates the track from `0` to `-50%` linearly with stable item widths, masks both edges, and pauses off screen (on hover only when the logos are links).
- **Login:** a solid white or dark ground, not a light grey tint, unless the form sits in a distinct panel.
- **Docs:** a copy button on every code snippet.

## Pricing

- Emphasise a plan with its button and an optional "Popular" label, never a different card background. It stays a sibling in the grid.
- Align buttons across cards: `flex flex-col justify-between` on each card with everything above the button in one `<div>`.
- To let the emphasised card poke out, use grid rows, never negative margins:

  ```html
  <div class="grid lg:grid-cols-3 lg:grid-rows-[--spacing(6)_1fr_--spacing(6)]">
    <div class="lg:row-start-2"><!-- plan --></div>
    <div class="lg:row-span-full"><!-- emphasised plan --></div>
    <div class="lg:row-start-2"><!-- plan --></div>
  </div>
  ```

  Drop the last row for a card that pokes out at the top only.
- Feature checkmarks follow the icon rules: `size-4 h-lh`.
