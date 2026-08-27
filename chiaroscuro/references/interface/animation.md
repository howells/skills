# Interface: Motion Contract

Motion belongs when it explains change, preserves orientation, confirms input, or makes waiting feel coherent. It does not belong merely to advertise that the interface was designed.

## Decide Before Animating

For each motion treatment, define:

- **Purpose** - orientation, continuity, feedback, relationship, or perceived speed.
- **Trigger and frequency** - a first-run transition can carry more presence than an action repeated dozens of times.
- **Origin and path** - motion should emerge from the control, edge, or object that caused it and return coherently.
- **Interruption** - rapid input, reversal, dismissal, and navigation must not wait for a decorative timeline to finish.
- **Reduced motion** - identify what disappears, shortens, or becomes an immediate state change.
- **Performance risk** - test the real device and content rather than assuming a property or library is free.

If purpose is unclear, omit the motion.

## Temperament

- Keep frequent feedback short and quiet. Save longer or more expressive motion for rare, consequential changes.
- Give direct manipulation immediate feedback. A press, drag, submission, or dismissal should acknowledge input without delay.
- Preserve spatial logic. A popover grows from its trigger; a panel usually exits toward the edge it entered from; forward and backward navigation should feel related.
- Use one physical metaphor within a flow. Elements should not feel heavy in one transition and weightless in the next without a reason.
- Avoid scroll hijacking, gratuitous parallax, ambient loops, and repeated reveal choreography. Scroll-linked motion needs a real explanatory function and a non-motion equivalent.

## Timing and Curves

Choose timing from distance, scale, frequency, and consequence. There is no universal duration or curve.

- Simple state feedback should finish quickly enough to feel attached to the action.
- Entrances commonly decelerate; exits may be brisker; objects moving between visible positions often benefit from easing at both ends.
- Springs are useful for interruptible, gesture-led, or spatial motion when their settling behavior matches the product. Easing curves are often clearer for deterministic state changes. Neither is categorically superior.
- Stagger only when sequence carries meaning. Long cascades make content feel slow.

Test perceived completion, not only the declared duration. A spring that micro-settles or an opacity tail that lingers can keep the interface feeling busy after the user considers it done.

## Implementation

- Prefer CSS transitions or keyframes for local, deterministic state changes.
- Use a motion library when gestures, interruption, orchestration, layout continuity, or exit presence genuinely require it.
- Animate `transform` and `opacity` when they produce the right effect, but assess paint, memory, layer count, and visual quality in context. Color, shadow, filter, mask, clip, and geometry changes are not forbidden; they require proportionate testing.
- Do not leave `will-change` applied broadly or permanently. Add it narrowly when measurement shows a benefit.
- Keep dynamic content stable. Reserve space where possible, avoid late geometry changes, and make number changes optically steady with tabular figures when appropriate.
- Avoid animating layout as a workaround for an unstable layout. Fix the geometry first.

## Reduced Motion

Honor `prefers-reduced-motion` and any product-level motion setting.

- Remove large travel, zoom, parallax, shaking, and nonessential looping.
- Preserve necessary state communication with an immediate change, a short fade, or another low-motion signal.
- Do not hide content or delay completion because an animation was disabled.
- Test the complete path with reduced motion enabled; a media query in source is not proof that the experience still works.

## Loading and Perceived Speed

- Acknowledge actions immediately.
- Prefer stable skeleton geometry or honest progress for meaningful waits. Use a spinner only when indeterminate waiting is the clearest model.
- Do not animate a placeholder so aggressively that waiting becomes the focal point.
- Keep optimistic updates reversible and distinguish pending from confirmed state.
- Motion cannot compensate for avoidable latency, layout shift, or missing progress feedback.

## Verification

Exercise motion with pointer, keyboard, touch when available, rapid repeated input, reversal, reduced motion, slow hardware, and long content. Check:

- no blocked interaction or delayed focus;
- no accidental scroll or clipping;
- no stale exit layer intercepting input;
- no layout jump before or after the transition;
- no sustained CPU, paint, or memory cost disproportionate to the effect;
- the user can still understand the state change with motion reduced.

If installed, use `animate` for specialist implementation craft, `motion` for current library/API facts, and the animation review skills for focused audits. This contract remains sufficient when they are absent.
