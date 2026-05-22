---
name: brand
description: "Create a distinctive visual identity system: brand strategy, palette, typography, visual character, rendered direction comparison, design tokens, and assets. Use when asked to create a brand, define visual identity, set up colors/fonts/tokens, generate brand directions, produce a brand system, or establish identity before UI design."
---

# Brand

Create an applied visual identity system. This is not a generic guidelines document: produce options the user can see, choose, refine, and apply to a real project.

Announce at start: "I'm using the brand skill to create a visual identity system."

## Core Rules

- Keep the work user-interactive. Brand identity is subjective; ask one focused question at a time for decisions.
- Use images, screenshots, existing sites, fonts, logos, and mood boards as first-class inputs. Visual references beat adjectives.
- Generate five genuinely different directions. If they are all variations of clean modern minimal, push harder.
- Render directions in a browser or HTML comparison page. Do not ask the user to judge typography and color from markdown alone.
- Prefer local or premium project fonts over default web fonts when available.
- Do not generate logos, wordmarks, monograms, or text-based marks with image generation. Build marks as SVG/code or flag them as designer work.
- Keep the final system practical: tokens, usage rules, assets, and examples the project can use.

## References

Load only what the task needs:

- `references/brand-identity.md`: brand identity principles, typography, color psychology, distinctiveness.
- `references/design-philosophy.md`: hierarchy, personality, visual systems, critique.
- `references/interface-colors.md`: OKLCH palettes, tinted neutrals, color weight, contrast.
- `references/interface-typography.md`: type hierarchy, readable UI typography.
- `references/typography-opentype.md`: OpenType features, tracking, font loading.
- `references/tailwind-v4.md`: Tailwind v4 token authoring when the project uses Tailwind.

## Workflow

### 1. Gather Context

Inspect the project before asking broad questions:

```bash
ls docs/brand-system.md docs/design-context.md docs/vision.md 2>/dev/null
find . -path '*/fonts/*' \( -name '*.otf' -o -name '*.ttf' -o -name '*.woff2' \) 2>/dev/null | head -40
rg -n "font-family|@font-face|next/font|localFont|google.*font|--color|@theme" app src public styles . --glob '*.{ts,tsx,css,scss,md}' 2>/dev/null | head -80
```

If a brand system already exists, ask whether to evolve, replace, or audit it.

Ask for visual references:

> Do you have screenshots, brands you admire, logos, fonts, palettes, links, or images that capture the feeling you want?

If the user has no references, ask one discovery question at a time:

- If the product were a physical space, what would it feel like?
- What should this brand never feel like?
- Who needs to trust this, and what would make them skeptical?
- What is the brand tension: warm authority, playful precision, raw refinement, accessible expertise, or something else?

### 2. Define Brand Tension

Summarize the working identity in one sentence:

```md
This brand should feel [quality A] but not [failure mode], [quality B] but not [failure mode].
```

Use that tension to guide direction generation. If the sentence is bland, keep questioning.

### 3. Generate Five Directions

Create five directions that vary across:

- Temperature: at least one warm and one cool.
- Typography: at least one serif-led and one sans-led.
- Density: at least one airy and one dense.
- Energy: at least one calm and one energetic.
- Surprise: at least one direction that pushes the user's comfort zone.

For each direction define:

```md
### Direction N: Name

Personality: One sentence capturing the tension.
Palette: brand, accent, surface, text, muted with OKLCH and hex.
Typography: display, body, mono, and why each fits.
Visual character: radius, shadows, line weight, density, motion.
Mood image prompt: atmospheric prompt with no text, logos, or brand names.
```

Use image generation only for atmospheric mood images, textures, or scenes. Avoid text and logos in generated images.

### 4. Build A Comparison Page

Create a temporary rendered comparison so the user can see the directions.

Use the project framework when obvious:

- Next.js: `app/brand-explore/page.tsx`
- Vite/static: `brand-explore.html`
- Other projects: a standalone `brand-explore.html` at a sensible temporary location

The page must include:

- Real font loading where possible.
- Color swatches with hex/OKLCH labels.
- Type specimens at display, body, and caption sizes.
- Mood image or texture for each direction.
- A mini UI preview with a button, card, input, and navigation/header treatment.
- Responsive layout that works on mobile and desktop.

Open or describe the page location, then ask:

> Which direction resonates most, or should we mix elements?

### 5. Refine The Chosen Direction

Build the selected direction into a complete system:

- Full OKLCH color scales, including tinted neutrals.
- Dark mode palette that is rebalanced rather than simply inverted.
- Semantic colors: success, warning, error, info.
- Typography scale with font roles, weights, line heights, tracking, and font-loading strategy.
- Visual character: radii, shadows, borders, icon weight, density, motion.
- Example application: buttons, cards, nav, forms, dark mode variants.

Ask for adjustment only after showing the system applied to real UI examples.

### 6. Produce Outputs

Write `docs/brand-system.md` unless the user asks for another path. Include:

- Brand summary and tension.
- Chosen direction and rejected alternatives.
- Palette with OKLCH and hex values.
- Typography system and font loading.
- Component/application examples.
- Logo/mark guidance.
- Do/don't rules.

Generate design tokens for the detected setup:

- Tailwind v4: `@theme` CSS variables.
- Tailwind v3: `tailwind.config.*` extension.
- Plain CSS: `:root` custom properties.

Create assets where useful:

- SVG logo/mark or favicon when the mark is simple enough to build in code.
- OG image template using project fonts when the app supports generated OG images.
- Atmospheric images or textures only when image generation is appropriate.

Offer to remove temporary exploration pages after finalizing the brand.

## Quality Bar

The work is complete when:

- References or discovery answers are captured.
- Five visibly distinct directions are rendered, not merely described.
- The user selects or combines a direction.
- The chosen direction has color, type, visual character, and applied examples.
- `docs/brand-system.md` and usable design tokens are produced.
- Generated assets avoid AI-rendered text/logo failures.

## Avoid

- Purple-blue gradients, Inter-only typography, white cards, and generic SaaS polish as a default.
- Accepting "clean", "modern", "premium", or "professional" without making the terms specific.
- Creating five palettes that differ only by hue.
- Ignoring local fonts in favor of generic web fonts.
- Producing brand documentation that could belong to any company.
- Skipping rendered comparison because markdown is faster.
