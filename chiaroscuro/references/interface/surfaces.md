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

## Empty And Loading States

- MUST: Empty and loading states inherit the same surface ladder as the populated state.
- SHOULD: Skeletons and placeholders match the eventual container structure.

## Review Questions

- Can this container be removed entirely? If not, could whitespace or a surface shift replace it?
- Does the current surface treatment make scanning faster?
- Is any surface visually louder than the content it contains?
