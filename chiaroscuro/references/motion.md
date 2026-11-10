# Motion

Motion belongs when it explains a change, keeps orientation, confirms input or makes waiting coherent, not to advertise that the interface was designed. `zoetrope` carries springs, gestures and frame-rate work in depth.

## Whether to animate

Frequency decides first.

| How often it's seen | Motion |
| --- | --- |
| Hundreds of times a day: command palette, keyboard actions | None |
| Tens of times: hovers, list navigation, tab switches | None, or under 150ms on opacity or colour |
| Occasionally: modals, drawers, toasts | Standard |
| Rarely: first run, success, empty state | May carry delight |

Never animate a keyboard-initiated action. If the only purpose is that it looks good and people see it often, leave it out. Every animated state change also leaves a static cue (colour, icon or label), so the state survives with motion off.

## Defaults

- Enter and exit with ease-out, move on screen with ease-in-out, run constant motion linearly, never ease-in. The built-in curves are weak; use stronger ones:

  ```css
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
  ```

- UI motion stays under 300ms: press 100-160ms, tooltips 125-200ms, dropdowns 150-250ms, modals and drawers up to about 400ms. Exits are shorter and smaller than enters.
- Never scale from `0`. Enter from about `scale(0.95)` with opacity.
- Popovers and menus grow from their trigger (`transform-origin` at the trigger, such as Base UI's `var(--transform-origin)`). Modals stay centred.
- Things leave the way they came: a panel that enters from the right exits right.
- Interactive state uses transitions, which retarget mid-flight; keyframes restart from zero, so keep them for sequences that run once. Anything a user can grab or reverse uses a spring started from the current on-screen value. Springs default to no bounce; add a little only after a gesture that carried momentum, such as a flick.
- Skip state animations on first render (`initial={false}` on an `AnimatePresence` around a state swap).
- Stagger only rare, staged entrances, a short step apart, never routine lists.
- When a cross-fade looks like two objects swapping, a 2px blur during the transition blends them.
- Use `@starting-style` for enter transitions where support allows.
- Name the properties you transition; never `transition-all`.

## Performance

- Animate `transform` and `opacity` by default and profile anything else. Large blurs, filters and masks are expensive; remove unearned ones before optimising kept ones.
- `will-change` only after seeing first-frame stutter, naming the property, and never `all`.
- Avoid high-frequency updates to inherited CSS variables across large subtrees.
- Fix unstable geometry rather than animating over it.

## Reduced motion

Honour `prefers-reduced-motion` and any product-level setting. Remove travel, zoom, parallax, shaking and decorative loops; keep state communication as an immediate change or a short opacity fade. Never hide content or delay completion because an animation was turned off.

## Checking it

Try rapid repeated input, reversal mid-flight and reduced motion. Nothing blocks interaction, delays focus, leaves an exiting layer intercepting clicks, or jumps layout before or after the transition. Slow the animation down in devtools to see what full speed hides.
