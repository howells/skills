# Values

The numbers to cite. Copy them from here or from the project's own tokens; never approximate.

## Tool

Walk down the list and stop at the first that fits.

| Need | Tool |
| --- | --- |
| A state toggled by a class or attribute: hover, press, open, selected | CSS `transition` |
| An entrance when an element first renders | CSS `@starting-style` (Tailwind v4: the `starting:` variant) |
| An exit to `display: none`, or a dialog or popover leaving the top layer | `transition-behavior: allow-discrete` on `display` and `overlay`, or a library's presence handling |
| Fixed choreography that must stay smooth while the page is busy | CSS `@keyframes` on compositable properties |
| Scripted control without a dependency | Web Animations API, `element.animate()` |
| Springs, gestures, shared-layout moves, exits after unmount | Motion (`motion/react`) |
| A whole-page or route change | The View Transitions API, where supported |

## Properties

- Prefer `transform` and `opacity`. They avoid relayout and usually composite.
- `clip-path`, `filter` and colour are fine when they make the effect; measure them on a device rather than assuming they're free. Keep animated `blur()` under 20px, especially for Safari; 2-5px is enough to soften a crossfade.
- A collapse is the one accepted layout animation. Keep it short.
- Anchored origins: Base UI exposes `--transform-origin`; Radix exposes `--radix-<component>-content-transform-origin`.
- `translate()` percentages are relative to the element: `translateY(100%)` hides a sheet or notice fully whatever its height. Prefer them to pixel offsets.
- `opacity: 0` alone still takes clicks and stays in the accessibility tree. Hide the element properly at rest.

## Easing

| Motion | Curve |
| --- | --- |
| Entering or leaving | ease-out (`--ease-out-quint`) |
| Moving between two visible positions, or morphing | ease-in-out (`--ease-in-out-quart`) |
| A sheet or drawer | `--ease-sheet` |
| Colour or hover change | `ease` |
| Constant motion: a marquee, a progress fill, a hold | `linear` |
| Unsure | ease-out |

```css
@theme {
  --ease-out-quint: cubic-bezier(0.23, 1, 0.32, 1);     /* entrances and exits */
  --ease-in-out-quart: cubic-bezier(0.77, 0, 0.175, 1); /* on-screen movement */
  --ease-sheet: cubic-bezier(0.32, 0.72, 0, 1);         /* iOS-style sheet */
}
```

In Tailwind v4 each `--ease-*` token becomes an `ease-*` utility (`ease-out-quint`). Outside Tailwind, put the same custom properties on `:root`. If a needed curve isn't here or in the project, take a named one from [easing.dev](https://easing.dev/) or [easings.co](https://easings.co/) and add it to the tokens.

## Duration

| Element | Duration |
| --- | --- |
| Press feedback | 100-160ms |
| Tooltip, small popover | 125-200ms |
| Menu, select, dropdown | 150-250ms |
| Dialog, sheet, drawer | 200-400ms; a large sheet can reach 500ms |
| Onboarding, marketing, explanation | Longer when the motion is the content |

Distance matters: a panel crossing the screen needs longer than a chip moving 8px. A notice that glides in at 350-400ms with plain `ease` can suit a calm product; that's a choice to state, not a default.

Perceived speed is part of duration. Once one tooltip in a group has opened, open its neighbours instantly, with no delay and no animation (Base UI marks these `data-instant`). A spinner on work that finishes in under 300ms reads as a glitch; show nothing.

## Springs

A spring has no fixed duration. It starts from whatever is on screen and carries velocity when retargeted. Use one for anything the user can touch, drag, flick or interrupt.

Think in two numbers: how quickly it arrives and how much it overshoots. In Motion those are `visualDuration` (seconds until it visually arrives) and `bounce` (0 is none). Native damping ratio is roughly `1 - bounce`.

| Situation | Motion config |
| --- | --- |
| Default for interface motion | `{ type: "spring", visualDuration: 0.3, bounce: 0 }` |
| A settle after a flick or throw | `{ type: "spring", visualDuration: 0.35, bounce: 0.15 }` up to `bounce: 0.25` |
| Playful product, rare moment | `bounce` up to 0.3 |

Physical parameters (`mass`, `stiffness`, `damping`) don't map onto the duration and bounce API; if a library needs them, start from `{ mass: 1, stiffness: 100, damping: 20 }`, which is critically damped, and lower the damping only where bounce is earned.

A spring sampled into a CSS `linear()` easing can't carry velocity through an interruption; use a real spring wherever the motion can be interrupted. A value that follows the pointer decoratively is smoothed with `useSpring`, not bound straight to the pointer.

## Interruption and timing

- A transition retargets from the current value; `@keyframes` restart from the first frame. Springs also keep velocity. Choose by how often it can fire.
- A reversible transition can mirror its curve so the way back retraces the way out.
- A hold-to-confirm fills over about 2s with `linear`, because it's progress; an early release snaps back in about 200ms with ease-out.
- Cap a stagger: set `--i` per item and clamp it so the tenth item isn't waiting half a second.

## Reduced motion and input

- Under `prefers-reduced-motion: reduce` (Tailwind `motion-reduce:`), remove travel, zoom, parallax, bounce and loops. Keep short opacity or colour changes that explain state. Reduced motion is gentler motion, not no feedback.
- In React with Motion, `useReducedMotion()` returns the preference so a transform target can become 0.
- Every animated state change also leaves a static cue (colour, icon or label), so the state survives with motion off.
- Under `prefers-reduced-transparency: reduce`, make translucent panels solid. Under `prefers-contrast: more`, give them a solid background and a defined border.
- Gate hover motion behind `@media (hover: hover) and (pointer: fine)`; touch screens fire hover on tap. Tailwind v4's `hover:` already sits inside `@media (hover: hover)`. `:active` is a real press on touch and needs no gate.
- Avoid full-screen moving backgrounds, slow endless oscillation and abrupt brightness jumps; fade large areas during a big move.
- Changing numbers use tabular figures (`tabular-nums`) so digits don't jitter sideways.
