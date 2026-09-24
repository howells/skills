# Values

The numbers and rules to cite. Copy values from here or from the project's own tokens; never approximate from memory. Where a rule has an exception, the exception is written next to it.

## Choosing the tool

Walk down the list and stop at the first that fits.

| Need | Tool |
| --- | --- |
| A state you toggle with a class or attribute: hover, press, open, selected | CSS `transition` |
| An entrance when an element first renders | CSS `@starting-style` (Tailwind v4: the `starting:` variant) |
| An exit to `display: none`, or a dialog or popover leaving the top layer | `transition-behavior: allow-discrete` on `display` and `overlay`, or a library's presence handling |
| Fixed choreography that must stay smooth while the page is busy | CSS `@keyframes`, which runs off the main thread |
| Scripted control without a dependency | Web Animations API, `element.animate()` |
| Springs, gestures, shared-layout moves, exits after unmount | A motion library |
| A whole-page or route change | The View Transitions API, where supported |

JavaScript driven by `requestAnimationFrame` drops frames while the browser is parsing, running scripts or painting. Use CSS or the Web Animations API for motion that is decided in advance; use a library for motion that reacts to input.

## Properties

- Prefer `transform` and `opacity`. They avoid layout and paint and can run on the compositor.
- `clip-path`, `filter` and colour are fine when they produce the effect; measure them on a real device rather than assuming they're free. Keep an animated `blur()` under about 20px, as larger radii get expensive, especially in Safari.
- `width`, `height`, `margin`, `padding`, `top` and `left` relayout on every frame. The accepted exception is a collapse, where there's no transform equivalent; keep it short.
- **Never grow from `scale(0)`.** Start at `scale(0.94)`-`scale(0.97)` with `opacity: 0`. Nothing real appears from a point.
- **Scale from the trigger.** Popovers, menus, selects and tooltips take `transform-origin` from their anchor. Base UI exposes `--transform-origin`; Radix exposes `--radix-<component>-content-transform-origin`. Centred dialogs are exempt and scale from the centre.
- `translate()` percentages are relative to the element itself: `translateY(100%)` moves by exactly its own height, so a sheet or notice hides fully whatever its content.
- Set the transform on the moving element. Updating a custom property on a parent that children read makes the browser recalculate style for every child, every frame.
- `transition: all` (Tailwind `transition-all`) animates properties nobody chose. Name them.

### In Motion

Animating the full `transform` string (`animate={{ transform: "translateX(120px)" }}`) runs through the Web Animations API and is hardware accelerated. The independent shorthands `x`, `y`, `scale` and `rotate` are computed on the main thread each frame. Prefer the full string; use the shorthands when transforms compose with different timings (an `x` slide plus a `whileHover` scale), when a value is a motion value, or when it's set through `style`. With shorthands or a CSS transition, a narrow `will-change: transform` for the duration helps; with `@keyframes` or the full string it isn't needed. Import from `motion` (`motion/react`), not the old `framer-motion` package.

## Easing

| Motion | Curve |
| --- | --- |
| Entering or leaving | ease-out |
| Moving between two visible positions, or morphing | ease-in-out |
| Colour or hover change | `ease` |
| Constant motion: a marquee, a progress fill | `linear` |
| Unsure | ease-out |

`ease-in` is wrong for interface motion: it spends its first frames barely moving, which is exactly when the user is looking. The same 200ms feels quicker as ease-out than as ease-in.

The built-in `ease-out` is weak for deliberate motion. Standard stronger curves, as tokens:

```css
@theme {
  --ease-out-quint: cubic-bezier(0.23, 1, 0.32, 1);    /* entrances and exits */
  --ease-in-out-quart: cubic-bezier(0.77, 0, 0.175, 1); /* on-screen movement */
  --ease-sheet: cubic-bezier(0.32, 0.72, 0, 1);         /* iOS-style sheet */
}
```

In Tailwind v4 each `--ease-*` token becomes an `ease-*` utility (`ease-out-quint`). Outside Tailwind, put the same custom properties on `:root`.

A reversible transition can mirror its curve so the way back retraces the way out.

## Duration

| Element | Duration |
| --- | --- |
| Press feedback | 100-160ms |
| Tooltip, small popover | 125-200ms |
| Menu, select, dropdown | 150-250ms |
| Dialog, sheet, drawer | 200-400ms; a large sheet can reach 500ms |
| Onboarding, marketing, explanation | Longer when the motion is the content |

Interface motion stays under 300ms unless the element is large or its character calls for it. A notice that glides in at 350-400ms with plain `ease` can suit a calm product; that's a choice to state, not a default. Distance matters: a panel crossing the screen needs longer than a chip moving 8px.

Perceived speed is part of duration. Once one tooltip in a group has opened, open its neighbours instantly with no delay and no animation (Base UI marks these with `data-instant`). A quicker spinner makes the same wait feel shorter.

## Springs

A spring has no fixed duration; it settles according to its parameters, it starts from whatever value is on screen, and it carries velocity when retargeted. Use one for anything the user can touch, drag, flick or interrupt.

Think in two numbers: how quickly it arrives, and how much it overshoots. In Motion that's `visualDuration` (seconds until it visually arrives) and `bounce` (0 is none). The damping ratio used in native toolkits is roughly `1 - bounce`.

| Situation | Motion config |
| --- | --- |
| Default for interface motion | `{ type: "spring", visualDuration: 0.3, bounce: 0 }` |
| A settle after a flick or throw | `{ type: "spring", visualDuration: 0.35, bounce: 0.15 }` to `bounce: 0.25` |
| Playful product, rare moment | `bounce` up to 0.3 |

Overshoot is earned by momentum. A menu that fades in and wobbles feels wrong; a card thrown into place that overshoots slightly feels right. Serious products (money, health, operations) keep `bounce: 0`.

For hand-written CSS a spring can be sampled into a `linear()` easing, but that copy can't carry velocity through an interruption; use a real spring wherever the motion can be interrupted.

For a value that follows the pointer decoratively, smooth it with a spring (`useSpring`) rather than binding it straight to the pointer position.

## Interruption and timing

- **Anything triggered twice quickly uses a transition or a spring.** A transition retargets from the current value; `@keyframes` restarts from its first frame and jumps. This covers notices stacking, toggles, expanding rows, anything a user can double-click.
- **Leave the way you came.** A sheet that rises from the bottom returns to the bottom. A symmetric path is what makes a swipe to dismiss obvious.
- **Slow where the user decides, fast where the system answers.** A hold-to-confirm fills over about 2s with `linear` easing, because it's progress; releasing early snaps back in about 200ms with ease-out.
- **Stagger groups by 30-80ms per item**, only on things seen occasionally, and never block input while the stagger plays.

## Reduced motion and input

- Under `prefers-reduced-motion: reduce` (Tailwind `motion-reduce:`), remove travel, zoom, parallax, bounce and loops. Keep short opacity or colour changes that explain state. Reduced motion is gentler motion, not no feedback.
- In React with Motion, `useReducedMotion()` returns the preference so a transform target can become 0.
- Under `prefers-reduced-transparency: reduce`, make translucent panels and bars solid. Under `prefers-contrast: more`, give them a solid background and a defined border.
- Gate hover motion behind `@media (hover: hover) and (pointer: fine)`, because touch screens fire a hover on tap. Tailwind v4's `hover:` already sits inside `@media (hover: hover)`.
- Avoid full-screen moving backgrounds, slow endless oscillation and abrupt brightness jumps; fade large surfaces during a big move.

## Checking feel

- Slow it to 10-25% in the browser's animation panel, or multiply the durations by five. Check the origin, that the curve doesn't stop abruptly, and that paired properties stay in step.
- Step frame by frame to find drift between properties meant to move together.
- Run gestures on a real touch device: load the dev server on a phone by the machine's local IP.
- Enable reduced motion in the browser's rendering settings and walk the same path.
- Look again later. Flaws invisible while building show up with fresh eyes.

## Defects

Each is a finding in review and a self-check before finishing a build.

| Defect | Instead |
| --- | --- |
| Motion on a keyboard action or something used constantly | An instant state change |
| `ease-in` on interface motion | ease-out, or `--ease-out-quint` |
| Weak built-in easing on a deliberate animation | A strong token curve |
| Growing from `scale(0)` | `scale(0.95)` with `opacity: 0` |
| Anchored popover scaling from the centre | The library's transform-origin variable |
| `transition: all` or `transition-all` | The named properties |
| Keyframes on something triggered repeatedly | A transition, or a spring |
| Layout properties animated where a transform would do | `transform` and `opacity` |
| Interface motion over 300ms with no stated reason | 150-250ms |
| Parent custom property driving child transforms | Transform set on the element |
| No reduced-motion handling on movement | A gentler variant |
| Ungated hover motion | Hover and fine-pointer media query |
| Symmetric timing on a press or hold | Slow press, quick release |
| A group arriving all at once | 30-80ms stagger |
| Bounce on motion no gesture threw | `bounce: 0` |
