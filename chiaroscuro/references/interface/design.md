# Interface: Design

## Shadows

- MAY: Layer ambient and direct shadows when the product's elevation model benefits from it. Derive the values from the surface, scale, and background rather than copying a universal recipe.
- SHOULD: Prefer `box-shadow` over `border` for subtle edges - shadows blend with backgrounds and avoid subpixel rendering issues:

```css
/* Preferred: shadow blends with any background */
box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.08);

/* Also works: inset variant */
box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.08);

/* Fallback: explicit border when shadow isn't practical */
border: 1px solid rgb(0 0 0 / 0.05);
```

## Borders

- MAY: Use device-pixel-aware hairlines when the rendering remains crisp across the target browsers:

```css
:root {
  --border-hairline: 1px;
  @media (min-resolution: 2dppx) { --border-hairline: 0.5px; }
}
```

## Radii

- SHOULD: Derive nested radii concentrically (`innerRadius ≈ outerRadius - inset`) and adjust optically when the geometry looks uneven.

## Contrast

- MUST: Meet the project's adopted accessibility contrast standard; use WCAG requirements as the shipping floor unless the project specifies a stricter method. APCA can be an additional design diagnostic, not an assumed compliance standard.
- MUST: Keep `:hover`, `:active`, and `:focus` states at least as legible as the default while making the state perceptible.
- MUST: Color-blind friendly chart palettes

## Gradients

- SHOULD: Eased gradients to avoid banding ([tool](https://larsenwork.com/easing-gradients))
- SHOULD: `mask-image` over gradient for fades:

```css
.fade-bottom { mask-image: linear-gradient(to bottom, black 80%, transparent); }
```

- NEVER: Fade on scrollable content

## Scrollbars

- NEVER: Custom page scrollbar
- SHOULD: Custom scrollbar only in contained elements (code blocks)

## Focus

- MUST: Focus indicators reach sufficient contrast against adjacent colors and remain coherent with the system. Neutral or brand-colored indicators are both valid when visible.

## Color Restraint

- SHOULD: One accent color per view
- SHOULD: Use existing tokens before adding new
- NEVER: Purple gradients, multicolor gradients (AI slop)
- NEVER: Glow effects as affordances

## AI Slop Detection

Concrete patterns that signal AI-generated design. Grep-friendly - each is a specific code smell, not a vibe.

### Visual Tells

| Pattern | What to look for | Why it's slop |
|---------|-----------------|---------------|
| Gratuitous gradients | `bg-gradient-to-*` or `linear-gradient` used decoratively, not functionally | AI defaults to gradients for "visual interest" instead of actual design |
| Glow effects | `shadow-[0_0_*]`, `drop-shadow`, `box-shadow` with blur >20px and color | Glow as decoration is a ChatGPT-era tell - real UIs use shadows for depth |
| `transition: all` | `transition-all` or `transition: all` | Lazy blanket transitions cause jank and unintended animations; specify properties |
| Visual monotony | Every card/section uses identical padding, radius, shadow | AI reuses the same container recipe everywhere - hierarchy should come from content and spacing, not uniform container dressing |
| Placeholder text shipped | `"Lorem ipsum"`, `"Your text here"`, `"Description goes here"` | AI leaves placeholder copy; real products have real content |
| Emoji as design | Emoji used as section icons or feature illustrations | AI substitutes emoji for actual iconography or illustration |

### Structural Tells

| Pattern | What to look for | Why it's slop |
|---------|-----------------|---------------|
| Hero → Features → Testimonials → CTA | Cookie-cutter landing page structure | Every AI landing page uses this exact layout |
| Uniform border-radius | Same `rounded-*` on every element | AI applies one radius globally instead of varying by context |
| White cards on white bg | Cards with `bg-white` on a `bg-white` or `bg-gray-50` parent | Creates a flat, lifeless hierarchy with no real depth |
| Centered everything | Every section center-aligned with `text-center mx-auto` | AI defaults to center alignment; real layouts use asymmetry |
| Unconsidered font fallback | A generic stack is used accidentally and conflicts with the intended voice | Typographic character should be chosen; a deliberate system stack can still be right for product UI |

### Code Tells

- NEVER: `transition-all` - specify exact properties (`transition-colors`, `transition-transform`)
- NEVER: `isolation: isolate` used as a "just in case" stacking context - use only when you can explain why (a deliberate app-shell isolation boundary per `layout.md`/`tailwind-authoring.md` is a valid such reason)
- NEVER: `blur-*` > `blur-xl` (20px) on decorative elements - large blurs tank performance for no purpose
- NEVER: Multiple gradient overlays stacked - simplify to one or use a solid color with opacity

## Decorative Elements

- MUST: Question whether any decorative element earns its place - overlays, background shapes, and accent graphics are furniture by default. If it can be removed without reducing comprehension, remove it.
- MUST: `pointer-events: none` on any decorative overlay that survives the cut
- SHOULD: `user-select: none` on code illustrations

## Primitives

- NEVER: Mix component libraries (Radix + Headless + Base UI)
- MUST: Use project's existing primitives
- MUST: Preserve accessible keyboard/focus behaviour using the project's existing primitives. For a composite widget with no suitable primitive, choose a library only when the task warrants that dependency; do not add one for a contained change.
