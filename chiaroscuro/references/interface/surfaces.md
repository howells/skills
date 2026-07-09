# Interface: Surfaces

Surface treatment communicates depth, grouping, and pace. Every surface must earn its place — the default is flat content on the canvas, not content inside a container.

## Surface Ladder

- MUST: Define a clear ladder such as canvas -> surface -> raised -> overlay.
- MUST: Keep neighboring steps visually close enough that hierarchy feels coherent.
- SHOULD: Use borders, tinted fills, and whitespace before introducing stronger shadows.

## Cards, Panels, And Dividers

- MUST: The default is no container. Content lives on the canvas until a card or panel earns its place by solving a real grouping, interaction, or hierarchy problem.
- SHOULD: Use open layouts with spacing and background shifts for routine sectioning. Dividers are an escalation, not a default.
- SHOULD: Cards earn their place when they represent repeated items, interactive clusters, or genuinely framed tools — not when empty space feels uncomfortable.
- MUST: Dividers are a last resort after spacing and surface shifts. When used, they stay quiet — they support grouping, not visual branding.
- MUST: Nested cards need a strong product reason.

## Breakpoint Reconfiguration

- SHOULD: Reduce visual framing as screen real estate tightens.
- MUST: Re-evaluate card density, padding, and borders at smaller breakpoints instead of merely stacking the same desktop treatment.
- SHOULD: Merge adjacent surfaces on mobile when extra chrome slows scanning.

## Visual Weight

- MUST: Use surface contrast to clarify priority, not decorate empty space.
- SHOULD: Let whitespace do work before adding more borders or fills.
- MUST NOT: Create a checkerboard of alternating panels without information hierarchy to justify it.

## Shadows And Elevation

- MUST NOT: Pair a shadow with a solid gray border. Use `ring-1 ring-black/5` or `ring-1 ring-black/10` (or the `950` step of the neutral) instead.
- MUST NOT: Make an elevated element (card, modal, popover with `shadow-*`) darker than its canvas. Use `white` or the lightest neutral, not `gray-100`/`gray-50`. Darker fills are fine for inset panels and wells that have no outer shadow.
- MUST: Remove all shadows in dark mode — use `dark:shadow-none` and lean on the surface ladder and faint inset rings for separation. See [dark-mode.md](./dark-mode.md).

### Layered Shadow Recipes

Tailwind's default single-layer shadows read blunt. Tuned elevation stacks several soft layers with doubling offsets and low, equal alphas. Three tiers — pick one per component state; never stack multiple shadow utilities on one element:

```css
@theme {
  /* sm — controls, pills, compact cards (the final 0 0 0 1px layer IS the ring) */
  --shadow-crafted-sm: 0px 2px 3px -1px rgb(0 0 0 / 0.1), 0px 1px 0px 0px rgb(25 28 33 / 0.02), 0px 0px 0px 1px rgb(25 28 33 / 0.08);
  /* md — cards, panels, popovers (default elevated surface) */
  --shadow-crafted-md: 0px 0px 0px 1px rgb(0 0 0 / 0.06), 0px 1px 1px -0.5px rgb(0 0 0 / 0.06), 0px 3px 3px -1.5px rgb(0 0 0 / 0.06), 0px 6px 6px -3px rgb(0 0 0 / 0.06), 0px 12px 12px -6px rgb(0 0 0 / 0.06), 0px 24px 24px -12px rgb(0 0 0 / 0.06);
  /* lg — hero media, feature callouts, modal-scale containers */
  --shadow-crafted-lg: 0 2.8px 2.2px rgb(0 0 0 / 0.034), 0 6.7px 5.3px rgb(0 0 0 / 0.048), 0 12.5px 10px rgb(0 0 0 / 0.06), 0 22.3px 17.9px rgb(0 0 0 / 0.072), 0 41.8px 33.4px rgb(0 0 0 / 0.086), 0 100px 80px rgb(0 0 0 / 0.12);
}
```

The baked-in `0 0 0 1px` layer in sm/md replaces `ring-1` — don't add another ring on top. All tiers still obey `dark:shadow-none`.

## Translucent Chrome

Translucency is functional, not decorative: it lets fixed chrome (sticky headers, toolbars, sheets) float over content instead of consuming an opaque strip of the canvas, and material weight communicates layer hierarchy. It still must earn its place — if the chrome never overlaps scrolling content, a solid surface is simpler and cheaper (see `performance.md` on auditing decorative `backdrop-blur-*`).

- SHOULD: Build sticky nav, toolbars, and sheets as translucent layers — `backdrop-blur-*` plus a semi-transparent background (`bg-white/60 backdrop-blur-xl backdrop-saturate-150`) — with content scrolling underneath.
- MUST NOT: Stack a light translucent surface on another translucent surface — legibility collapses.
- SHOULD: Bigger surfaces read as thicker material: a full sheet gets stronger blur and a deeper shadow than a small chip.
- MUST: Keep text legible over translucency — higher contrast and slightly heavier weight than the same text on a solid surface; keep colored text and accents on solid layers, not the translucent foreground.
- SHOULD: Prefer a scroll edge effect over a hard 1px divider under sticky chrome — a small blur or gradient mask where content meets the floating layer, applied only where overlap actually happens.
- SHOULD: Dim to focus, separate to keep flow — a modal task pairs its surface with a dimming scrim; a parallel, non-blocking panel uses translucency and offset without a scrim.
- SHOULD: On enter/exit, animate blur radius and scale together so the surface reads as material arriving, not a plain opacity fade.
- SHOULD: Where floating UI overlaps busy imagery (a fixed nav over a hero photo), use progressive blur instead of one flat blur band — stack a few `backdrop-blur` layers with doubling radii, each masked to a shifted gradient band, so intensity ramps smoothly instead of ending in a hard smudge edge. Reserve it for imagery; the scroll edge effect above covers text content:

```css
.progressive-blur { position: absolute; inset: 0 0 auto 0; height: 6rem; pointer-events: none; }
.progressive-blur > div { position: absolute; inset: 0; }
.progressive-blur > div:nth-child(1) { backdrop-filter: blur(1px);  mask-image: linear-gradient(to top, transparent 0%, black 25%, black 50%, transparent 75%); }
.progressive-blur > div:nth-child(2) { backdrop-filter: blur(4px);  mask-image: linear-gradient(to top, transparent 25%, black 50%, black 75%, transparent 100%); }
.progressive-blur > div:nth-child(3) { backdrop-filter: blur(16px); mask-image: linear-gradient(to top, transparent 50%, black 75%); }
```

- MUST: Honor `prefers-reduced-transparency: reduce` — raise the background to near-opaque and drop the blur:

```css
@custom-variant reduced-transparency (@media (prefers-reduced-transparency: reduce));
```

```html
<header class="bg-white/60 backdrop-blur-xl reduced-transparency:bg-white reduced-transparency:backdrop-blur-none">
```

## Empty And Loading States

- MUST: Empty and loading states inherit the same surface ladder as the populated state.
- SHOULD: Skeletons and placeholders match the eventual container structure.

## Review Questions

- Can this container be removed entirely? If not, could whitespace or a surface shift replace it?
- Does the current surface treatment make scanning faster?
- Is any surface visually louder than the content it contains?
