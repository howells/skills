# Interface: Surfaces

Surface treatment communicates grouping, depth, and pace. The default is content on the canvas. A card, panel, border, shadow, or translucent layer must solve a real hierarchy or interaction problem.

## Surface Ladder

- Define a small ladder such as canvas, surface, raised, and overlay.
- Keep neighboring levels close enough to feel related and distinct enough to read.
- Use spacing and proportion before adding borders, fills, or elevation.
- Reconfigure the ladder at small breakpoints. Mobile often needs fewer containers, less padding, and flatter grouping.

## Cards, Panels, and Dividers

- Use a card for a repeated object, an interactive cluster, or a genuinely bounded tool, not to fill empty space.
- Use a panel when content needs independent behavior, scrolling, or a persistent boundary.
- Use a divider only when spacing and surface contrast do not make the grouping legible.
- Avoid nested cards unless the nested object has its own state or action boundary.
- Keep empty, loading, error, and populated states on the same geometry and surface ladder.

## Elevation

Choose elevation from the product's physical metaphor and existing tokens.

- Flat products can use surface contrast and inset rings alone.
- A raised popover, menu, drag object, or modal may need a shadow to clarify overlap.
- Layered shadows can create natural elevation, but they are a technique, not a universal three-layer recipe.
- Avoid combining a strong border and a strong shadow unless both communicate different information.
- Keep an elevated surface related to its canvas; a darker fill often reads as inset unless the established system says otherwise.
- Test shadow color and opacity separately in dark mode. Some systems should remove it; others benefit from a restrained, tinted shadow alongside surface contrast.

## Concentric Geometry

Nested rounded shapes should feel cut from one system. Derive an inner radius from the outer radius and the intervening inset rather than repeating the same radius. Adjust optically where the mathematical result looks wrong.

## Translucent Chrome

Translucency is useful when fixed or floating chrome overlaps moving content and the content should remain perceptible. It is not a default material.

- Prefer a solid surface when nothing passes behind the element.
- Keep text and controls legible over the full range of underlying content.
- Avoid stacking translucent layers; the result becomes unpredictable and expensive.
- A modal task usually needs a scrim. A parallel, non-blocking panel may use separation without one.
- Progressive or masked blur is appropriate only when it solves a visible edge problem over imagery. Start with one restrained layer and measure before adding more.
- Honor `prefers-reduced-transparency` where supported by raising opacity and removing blur:

```css
@custom-variant reduced-transparency (@media (prefers-reduced-transparency: reduce));
```

```html
<header class="bg-white/70 backdrop-blur-lg reduced-transparency:bg-white reduced-transparency:backdrop-blur-none">
```

## Review

- Can this container be removed without losing meaning or behavior?
- Does the surface make scanning or interaction faster?
- Is elevation explaining overlap, or decorating a rectangle?
- Does the hierarchy survive mobile, dark mode, long content, and reduced transparency?
