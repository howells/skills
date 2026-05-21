---
name: foundry
description: Create, review, or revise a Tailwind v4 visual identity system with brand positioning, palette, OKLCH @theme tokens, typography, surface character, motion personality, and reusable UI identity rules. Use when asked to create a brand, define visual identity, choose colors or fonts, make a product less generic, produce docs/brand-system.md, or establish identity before UI design.
---

# Foundry

Use this skill to create a distinct, usable brand identity system for a software product, website, tool, or creative project. The system must be practical enough to implement, not just mood words.

Tailwind v4 is mandatory. Brand output must use Tailwind v4 CSS-first tokens, `@theme`, OKLCH-aware color thinking, and utility-ready implementation guidance. Do not produce Tailwind v3 config, CSS Modules-first, styled-components-first, or framework-agnostic styling instructions unless the user explicitly asks for a non-code brand document.

## References

Load only the references needed for the task:

- `references/brand-identity.md` for identity direction and brand-system structure.
- `references/design-philosophy.md` for non-generic UI taste and critique.
- `references/tailwind-v4.md` for mandatory Tailwind v4 token patterns.
- `references/tailwind-authoring.md` for utility authoring discipline.
- `references/interface-colors.md` for color and contrast rules.
- `references/interface-typography.md` for typography rules.
- `references/typography-opentype.md` for advanced type details.

## Start

When invoked:

1. State that you are using the `foundry` skill.
2. Determine whether the user wants to create, review, or revise a brand.
3. Inspect existing context before asking questions:
   - `docs/brand-system.md`
   - `docs/design-context.md`
   - `docs/vision.md`
   - `README.md`
   - existing CSS, Tailwind entry files, token files, and font imports
   - screenshots or UI files if the user wants the brand applied to an interface
4. Ask for missing creative constraints only when they materially affect the work.

Useful questions:

- What is the product, audience, and category?
- What should the brand feel unlike?
- Are there competitors, references, or anti-references?
- Is this for an app UI, marketing site, docs, CLI, or all of them?
- Are there existing fonts, logos, colors, or accessibility constraints?

Ask one question at a time when blocked. If not blocked, proceed with stated assumptions.

## Create Mode

When creating a brand, produce 3-5 genuinely different directions before recommending one. Each direction should include:

- Positioning: audience, category tension, and personality.
- Visual character: density, sharpness, surface treatment, imagery, icon style, and motion temperament.
- Palette: named roles, OKLCH values, fallback hex values where useful, contrast risks, and color-blind considerations.
- Typography: primary and secondary type choices or characteristics, hierarchy, and OpenType notes when relevant.
- Tailwind v4 implementation: `@theme` variables, semantic token names, and example utility usage.
- UI implications: what buttons, cards, navigation, forms, tables, and empty states should feel like.

Do not make five minor color variations of the same idea. Distinct directions should differ in worldview, not just palette.

## Apply Mode

When applying or revising a brand in a codebase:

1. Locate the shared Tailwind v4 CSS entry and token source.
2. Confirm the project uses Tailwind v4. If it does not, make the Tailwind v4 migration requirement explicit before editing styling.
3. Update tokens and representative UI surfaces in the smallest coherent slice.
4. Prefer existing design-system primitives over one-off markup.
5. Keep brand rules canonical. Do not leave old and new token systems side by side.

If producing a document, create or update `docs/brand-system.md` by default.

## Tailwind v4 Requirements

Brand implementation guidance must:

- Use `@theme` for design tokens.
- Use OKLCH for brand colors when possible.
- Include semantic color roles, not only raw palette names.
- Avoid safelists and `important` hacks.
- Avoid adding `tailwind.config.*`.
- Explain required `@source` coverage when class generation depends on monorepo paths.
- Keep utility examples compatible with Tailwind v4.

## Asset Guidance

Do not rely on image models to generate precise wordmarks or readable text. For marks and logos:

- Prefer simple editable SVG/code marks when feasible.
- Treat generated raster imagery as mood or campaign imagery, not a definitive logo.
- Make asset limitations explicit when a professional designer or trademark check is needed.

## Review Mode

When reviewing a brand system, lead with issues:

1. Generic identity that could fit any product in the category.
2. Palette without semantic roles or accessibility checks.
3. Typography that lacks hierarchy or implementation details.
4. Tailwind v4 conflicts, Tailwind v3 config, or token duplication.
5. Visual direction that contradicts the product audience.
6. Brand rules that are too abstract to guide UI implementation.

If the user asked only for a review, do not overwrite files. Provide findings and proposed edits.

## Completion Check

Before finishing, verify that the brand:

- Has a clear audience and personality.
- Includes a usable Tailwind v4 token model.
- Provides color, type, spacing/surface, motion, and component guidance.
- Avoids generic mood-board language.
- Can be implemented by a future agent without asking what the brand means in UI.
