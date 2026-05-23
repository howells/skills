# Interface: Layout

## Principles

- MUST: Deliberate alignment (grid/baseline/edges/optical centers)
- MUST: Every layout element has a job: hierarchy, grouping, navigation, affordance, state, content meaning, or domain character
- MUST: Remove UI furniture: purposeless chrome, decorative wrappers, filler panels, floating badges, fake controls, ornamental dividers, and background effects that do not change user understanding
- MUST: Verify mobile, laptop, ultra-wide (simulate at 50% zoom)
- MUST: Respect safe areas via `env(safe-area-inset-*)`
- MUST: No unwanted scrollbars — fix overflows
- SHOULD: Optical alignment: ±1px when perception beats geometry
- SHOULD: Balance icon/text lockups (stroke, weight, size, spacing, color)

## Viewport

- MUST: `h-dvh` not `h-screen` (respects mobile browser chrome)
- MUST: Fixed elements respect `safe-area-inset-*`

## Purpose Check

Before keeping a visual container, ask:

- What does this help the user understand or do?
- Does it change hierarchy, grouping, affordance, state, navigation, or domain meaning?
- Would removing it make the screen less usable or less legible?

If the answer is no, remove it. Distinction should come from proportion, typography, spacing, domain-specific structure, and purposeful state treatment, not extra decoration.

## Z-Index

MUST use fixed scale — no arbitrary values like `z-[999]`:

| Layer | Tailwind | CSS Variable |
|-------|----------|--------------|
| Base | `z-0` | — |
| Dropdown | `z-10` | `--z-dropdown: 100` |
| Sticky | `z-20` | — |
| Modal | `z-30` | `--z-modal: 200` |
| Toast | `z-40` | `--z-toast: 400` |
| Tooltip | `z-50` | `--z-tooltip: 300` |

### Avoiding Z-Index

- SHOULD: Use `isolate` (Tailwind) to create stacking context without z-index:

```jsx
<div className="isolate">
  {/* New stacking context, no global z-index conflict */}
</div>
```
