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

## Timing and Implementation

Choose timing from distance, scale, frequency and consequence; there is no universal duration or curve. Prefer CSS transitions for local, deterministic state changes and a motion library only when gestures, interruption or layout continuity need it. Fix unstable geometry rather than animating over it. Values, springs, gestures and performance belong to `zoetrope`.

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

## Checking It

Try motion with rapid repeated input, reversal and reduced motion. Nothing should block interaction, delay focus, leave an exit layer intercepting input, or jump layout before or after the transition.

If installed, use `zoetrope` for specialist motion craft and the library's own documentation for current API facts. This contract remains sufficient when they are absent.
