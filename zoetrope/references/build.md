# Build

1. Decide whether it animates (SKILL.md). If not, say why and give the instant alternative.
2. Pick the tool, properties, curve and duration, or a spring, from `values.md`. Start from a recipe below when one matches; swap in the project's primitives and tokens.
3. Write the code with its reduced-motion variant, hover gating, and interruption behaviour for anything that can fire twice quickly.

Output the code, then at most three lines:

```
Why:          <frequency> · <purpose>
Ingredients:  <tool> · <properties> · <curve and duration, or spring>
Feel check:   <what to watch, and how>, or "none needed"
```

Recipes: press, anchored popover, dialog with scrim, sheet, notice, collapse, staggered group, hold to confirm, moving selection indicator, double-exposing crossfade, scripted without a library, reveal on scroll, comparison slider, expanding an object into its detail, layout projection without stretched text.

## Press

`scale()` shrinks the label and icon too, which is what reads as a physical press.

```css
.pressable { transition: transform 120ms var(--ease-out-quint); }
.pressable:active { transform: scale(0.97); }
```

Tailwind: `transition-transform duration-120 ease-out-quint active:scale-97`.

## Anchored popover, menu, select or tooltip

It grows out of the thing that opened it.

```css
.menu-popup {
  transform-origin: var(--transform-origin); /* Radix: var(--radix-dropdown-menu-content-transform-origin) */
  transition:
    opacity 180ms var(--ease-out-quint),
    transform 180ms var(--ease-out-quint);
}
.menu-popup[data-starting-style],
.menu-popup[data-ending-style] {
  opacity: 0;
  transform: scale(0.96);
}
.menu-popup[data-instant] { transition-duration: 0ms; } /* tooltip neighbours */
```

Tooltips use 140ms and `scale(0.97)`. Radix marks state with `data-state="open" | "closed"`; its exit needs presence handling (`forceMount` with a motion library, or its CSS animation support).

## Dialog with scrim

Centred, so it scales from the centre. The scrim fades with it so the two read as one layer.

```css
dialog {
  opacity: 1;
  transform: scale(1);
  transition:
    opacity 220ms var(--ease-out-quint),
    transform 220ms var(--ease-out-quint),
    display 220ms allow-discrete,
    overlay 220ms allow-discrete;
  @starting-style { opacity: 0; transform: scale(0.96); }
}
dialog:not([open]) { opacity: 0; transform: scale(0.96); }
dialog::backdrop {
  background: rgb(0 0 0 / 0.4);
  transition: background-color 220ms var(--ease-out-quint), display 220ms allow-discrete, overlay 220ms allow-discrete;
}
@starting-style { dialog[open]::backdrop { background: rgb(0 0 0 / 0); } }
```

`allow-discrete` on `display` and `overlay` keeps the native dialog in the top layer until its exit finishes.

## Sheet

```css
.sheet { transform: translateY(0); transition: transform 360ms var(--ease-sheet); }
.sheet[data-closed] { transform: translateY(100%); }
```

Once it can be dragged it is a gesture build.

## Notice

Notices arrive in bursts, so they use transitions, which retarget.

```css
.notice {
  opacity: 1;
  transform: translateY(0);
  transition:
    opacity 320ms var(--ease-out-quint),
    transform 320ms var(--ease-out-quint);
  @starting-style { opacity: 0; transform: translateY(100%); }
}
```

Without `@starting-style`, render with `data-mounted="false"` and flip it to `true` in an effect after first paint. When notices stack and the list closes up, opacity and height compete; tune that pair by eye in slow motion. Pause notice timers while the tab is hidden. Fill hover gaps between stacked notices with pseudo-elements so the expanded stack doesn't collapse as the pointer crosses a gap.

## Collapse

```css
.collapse {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 200ms var(--ease-out-quint);
}
.collapse[data-open] { grid-template-rows: 1fr; }
.collapse > .collapse-inner { overflow: hidden; }
```

Grid rows from `0fr` to `1fr` reach the content's natural height with no measuring. Where `interpolate-size: allow-keywords` is supported, `height: 0` to `auto` works directly. Fade the inner content alongside if it would otherwise look clipped.

## Staggered group

For a grid seen occasionally, not a list scrolled all day.

```css
.stagger-item {
  animation: rise 280ms var(--ease-out-quint) backwards;
  animation-delay: calc(min(var(--i), 8) * 50ms);
}
@keyframes rise { from { opacity: 0; transform: translateY(6px); } }
```

Set `--i` inline per item. Keyframes are right here because the entrance runs once; `backwards` holds the first frame during the delay.

## Hold to confirm

For a destructive action where one click is too easy.

```css
.hold-fill {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 200ms var(--ease-out-quint); /* release: quick */
}
.hold:active .hold-fill {
  clip-path: inset(0 0 0 0);
  transition: clip-path 2s linear; /* press: steady progress */
}
```

Commit only when the forward transition finishes while the hold is still active. Check the event's target and property, cancel on release or `pointercancel`, and never commit from the reverse transition's `transitionend`.

## Moving selection indicator

With Motion, render the indicator inside the active item with a shared `layoutId`:

```jsx
{isActive && (
  <motion.span layoutId="tab-indicator" transition={{ type: "spring", visualDuration: 0.25, bounce: 0 }} />
)}
```

Without a library, when background and text colour both change, render a second copy of the tab row styled as selected, lay it over the first, and animate its `clip-path: inset()` to the active tab's bounds. Text and background change in lockstep because one element is revealed rather than two colours interpolated.

## A crossfade that double-exposes

When two states visibly overlap and no curve fixes it, blur the seam so the eye reads one changing thing.

```css
.swap { transition: opacity 180ms ease, filter 180ms ease; }
.swap[data-swapping] { opacity: 0.6; filter: blur(3px); }
```

## Scripted, without a library

```js
panel.animate(
  [{ clipPath: "inset(0 0 100% 0)" }, { clipPath: "inset(0 0 0 0)" }],
  { duration: 480, easing: "cubic-bezier(0.77, 0, 0.175, 1)", fill: "forwards" },
);
```

The Web Animations API can be paused, reversed and cancelled, and costs no bundle.

## Reveal on scroll

Marketing and editorial pages only, and once per element.

```css
.reveal { clip-path: inset(0 0 100% 0); transition: clip-path 560ms var(--ease-in-out-quart); }
.reveal[data-seen] { clip-path: inset(0 0 0 0); }
```

Set `data-seen` once from an `IntersectionObserver` with a negative bottom margin, or Motion's `useInView({ once: true })`.

## Comparison slider

Overlay the two images and clip the top one with `clip-path: inset(0 50% 0 0)`, driven from the pointer position so both stay registered. Track it like any drag (pointer capture, offset from the grab point).

## Expand an object into its detail

For a model or diagram whose transformation explains how parts relate.

- Keep stable IDs so the selected object visibly becomes the detail. Preserve its material, proportions and relationship to its neighbours.
- Hold the camera or viewport steady through one transformation. Don't recentre, zoom and explode at once unless each is needed.
- Keep enough parent and sibling context to show where the detail belongs. Expand from the selected object and return along the same path.
- Run nested expansion, sibling selection and contraction through one state model. Retarget from the visible intermediate state when interrupted; never remount an unrelated scene or lock input.
- Watch every path at normal speed and at midpoints. The viewer should follow the same object throughout; a crossfade hides the failure without fixing it.

## Layout projection without stretched text

A shared-layout card can expand smoothly while its labels visibly stretch. In Motion, put `layout="position"` on content that should move without resizing, and keep its typography at the destination's real size. If the parent still projects scale onto its children, separate the animated background from the content layer, or use the library's scale-correction pattern.

Step through opening, reversing halfway, switching selection and closing, and look at text, icons, borders and corners on intermediate frames. A resting-state screenshot can't show the distortion.
