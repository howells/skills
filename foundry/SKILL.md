---
name: foundry
description: Create, review, or revise a distinctive visual identity system — brand positioning, rendered direction options, OKLCH palette, typography, visual character, and a Tailwind v4 @theme token model (or docs/brand-system.md). Use when asked to create a brand, define visual identity, generate or compare brand directions, choose colors or fonts, set up design tokens, make a product less generic, or establish identity before UI design.
---

# Foundry

Create an applied, distinct visual identity system for a software product, website, tool, or creative project. This is not a generic guidelines document: produce options the user can see, choose, refine, and implement.

Tailwind v4 is the default implementation target. Brand output should use Tailwind v4 CSS-first tokens, `@theme`, and OKLCH-aware color thinking. Produce Tailwind v3 config, CSS Modules-first, or styled-components-first instructions only when the user explicitly asks, and use plain-CSS `:root` custom properties only when the project is not on Tailwind.

Announce at start: "I'm using the foundry skill to work on a visual identity system."

## Core Rules

- Keep the work user-interactive. Brand identity is subjective; ask one focused question at a time for decisions.
- Use images, screenshots, existing sites, fonts, logos, and mood boards as first-class inputs. Visual references beat adjectives.
- Generate genuinely different directions. Distinct directions differ in worldview, not just palette. If they are all variations of clean modern minimal, push harder.
- Render directions in a browser or HTML comparison page. Do not ask the user to judge typography and color from markdown alone.
- Prefer local or premium project fonts over default web fonts when available.
- Do not generate logos, wordmarks, monograms, or text-based marks with image generation. Build marks as SVG/code or flag them as designer work.
- Keep the final system practical: tokens, usage rules, assets, and examples the project can implement without asking what the brand means in UI.

## References

Load only the references needed for the task:

- `references/brand-identity.md`: brand identity principles, typography, color psychology, distinctiveness, brand-system structure.
- `references/design-philosophy.md`: hierarchy, personality, depth, and critique of generic UI.
- `references/interface-colors.md`: OKLCH palettes, tinted neutrals, color weight, contrast, dark mode.
- `references/interface-typography.md`: type hierarchy, readable UI typography.
- `references/typography-opentype.md`: OpenType features, tracking, font loading.
- `references/tailwind-v4.md`: Tailwind v4 token patterns when the project uses Tailwind.
- `references/tailwind-authoring.md`: utility authoring discipline.

## Start

When invoked:

1. State that you are using the `foundry` skill.
2. Determine whether the user wants to **create**, **review**, or **revise** a brand.
3. Inspect existing context before asking broad questions:

   ```bash
   ls docs/brand-system.md README.md 2>/dev/null
   find . -type f \( -iname '*brand*' -o -iname '*vision*' -o -iname '*design-context*' \) -path '*docs/*' 2>/dev/null | head -20
   find . -path '*/fonts/*' \( -name '*.otf' -o -name '*.ttf' -o -name '*.woff2' \) 2>/dev/null | head -40
   rg -n "font-family|@font-face|next/font|localFont|google.*font|--color|@theme" app src public styles . --glob '*.{ts,tsx,css,scss,md}' 2>/dev/null | head -80
   ```

   Also inspect any `docs/` brand, vision, or design-context files, existing CSS/Tailwind entry files, token files, and font imports; and screenshots or UI files if the user wants the brand applied to an interface.
4. If a brand system already exists, ask whether to **evolve, replace, or audit** it.
5. Ask for missing creative constraints only when they materially affect the work. Useful questions: What is the product, audience, and category? What should the brand feel unlike? Are there competitors, references, or anti-references? Is this for an app UI, marketing site, docs, CLI, or all of them? Are there existing fonts, logos, colors, or accessibility constraints?

Ask one question at a time when blocked. If not blocked, proceed with stated assumptions.

## Create Mode

Produce a system the user chooses by seeing it, not by reading mood words.

### 1. Gather references and tension

Ask for visual references:

> Do you have screenshots, brands you admire, logos, fonts, palettes, links, or images that capture the feeling you want?

If the user has none, ask one discovery question at a time (if the product were a physical space, what would it feel like? what should this brand never feel like? who needs to trust this, and what would make them skeptical?). Then summarize the working identity in one sentence:

```md
This brand should feel [quality A] but not [failure mode], [quality B] but not [failure mode].
```

If the sentence is bland, keep questioning.

### 2. Generate 3-5 genuinely different directions

Vary directions across temperature (at least one warm, one cool), typography (at least one serif-led, one sans-led), density (airy vs dense), energy (calm vs energetic), and at least one direction that pushes the user's comfort zone. For each direction define:

```md
### Direction N: Name

Positioning: audience, category tension, and personality in one sentence.
Palette: brand, accent, surface, text, muted — named roles with OKLCH values, fallback hex where useful, contrast risks, color-blind considerations.
Typography: display, body, mono choices or characteristics, hierarchy, and why each fits; OpenType notes when relevant.
Visual character: radius, shadows, line weight, density, icon style, motion temperament.
Tailwind v4 implementation: `@theme` variables, semantic token names, example utility usage.
UI implications: what buttons, cards, navigation, forms, tables, and empty states should feel like.
Mood image prompt: atmospheric prompt with no text, logos, or brand names.
```

Do not make five minor color variations of one idea.

### 3. Build a comparison page

Create a temporary rendered comparison so the user can see the directions. Use the project framework when obvious (Next.js: `app/brand-explore/page.tsx`; Vite/static: `brand-explore.html`; otherwise a standalone `brand-explore.html`). The page must include real font loading where possible, color swatches with hex/OKLCH labels, type specimens at display/body/caption sizes, a mood image or texture per direction, a mini UI preview (button, card, input, nav/header), and a responsive layout.

Open or describe the page location, then ask:

> Which direction resonates most, or should we mix elements?

### 4. Refine the chosen direction

Build the selected direction into a complete system: full OKLCH color scales including tinted neutrals; a dark-mode palette that is rebalanced, not simply inverted; semantic colors (success, warning, error, info); a typography scale with roles, weights, line heights, tracking, and font-loading strategy; visual character (radii, shadows, borders, icon weight, density, motion); and an example application (buttons, cards, nav, forms, dark-mode variants). Ask for adjustment only after showing the system applied to real UI examples.

### 5. Produce outputs

Write `docs/brand-system.md` unless the user asks for another path (this is the default deliverable for Create Mode as well as Apply Mode). Include the brand summary and tension, chosen direction and rejected alternatives, palette with OKLCH and hex, typography system and font loading, component/application examples, logo/mark guidance, and do/don't rules. Then generate design tokens for the detected setup: Tailwind v4 `@theme` CSS variables (default), Tailwind v3 `tailwind.config.*` extension only if the project is on v3, or plain CSS `:root` custom properties for non-Tailwind projects. Offer to remove temporary exploration pages after finalizing.

## Apply Mode

When applying or revising a brand in a codebase:

1. Locate the shared Tailwind v4 CSS entry and token source.
2. Confirm the project uses Tailwind v4. If it does not, make the Tailwind v4 migration requirement (or the plain-CSS fallback) explicit before editing styling.
3. Update tokens and representative UI surfaces in the smallest coherent slice.
4. Prefer existing design-system primitives over one-off markup.
5. Keep brand rules canonical. Do not leave old and new token systems side by side.

If producing a document, create or update `docs/brand-system.md` by default.

## Tailwind v4 Requirements

Brand implementation guidance must use `@theme` for design tokens, OKLCH for brand colors when possible, semantic color roles (not only raw palette names), and utility examples compatible with Tailwind v4. Avoid safelists, `important` hacks, and adding `tailwind.config.*`. Explain required `@source` coverage when class generation depends on monorepo paths.

## Asset Guidance

Do not rely on image models to generate precise wordmarks or readable text. For marks and logos, prefer simple editable SVG/code marks when feasible; treat generated raster imagery as mood or campaign imagery, not a definitive logo; and make asset limitations explicit when a professional designer or trademark check is needed. Use image generation only for atmospheric mood images, textures, or scenes, with no text or logos in the prompt. If no image-generation tool is available, use CSS gradients/textures and keep the prompt as documentation.

## Review Mode

When reviewing a brand system, lead with issues:

1. Generic identity that could fit any product in the category.
2. Palette without semantic roles or accessibility checks.
3. Typography that lacks hierarchy or implementation details.
4. Tailwind v4 conflicts, Tailwind v3 config, or token duplication.
5. Visual direction that contradicts the product audience.
6. Brand rules too abstract to guide UI implementation.

If the user asked only for a review, do not overwrite files. Provide findings and proposed edits.

## Avoid

- Purple-blue gradients, Inter-only typography, white cards, and generic SaaS polish as a default.
- Accepting "clean", "modern", "premium", or "professional" without making the terms specific.
- Creating directions that differ only by hue.
- Ignoring local fonts in favor of generic web fonts.
- Producing brand documentation that could belong to any company.
- Skipping the rendered comparison because markdown is faster.

## Completion Check

Before finishing, verify that the brand:

- Has a clear audience and personality.
- Presented visibly distinct directions as rendered output (not merely described), and the user selected or combined one.
- Provides color, type, spacing/surface, motion, and component guidance.
- Includes a usable token model (Tailwind v4 `@theme` by default) and `docs/brand-system.md`.
- Avoids generic mood-board language and AI-rendered text/logo failures.
- Can be implemented by a future agent without asking what the brand means in UI.
