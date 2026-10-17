# Animation performance

Adapted from Emil Kowalski's `animation-performance`; revision and licence are in [source.md](source.md). Use this for dropped frames and property/driver choices. Keep the purpose, timing and accessibility decisions from `values.md`.

## Diagnose before changing code

List each affected element, driver, animated properties and concurrent work. Expand `transition: all` and shorthand props into the properties they drive. Name a supported cause before proposing a fix; `will-change` is a late diagnostic option.

The frame budget is about 16.7ms at 60Hz and 8.3ms at 120Hz. Design against the smaller budget. A fast laptop can hide work that misses that budget on a phone.

| Symptom | Check first | Repair when confirmed |
| --- | --- | --- |
| Stutters throughout | Layout or paint on each frame | Use an equivalent transform/opacity effect |
| Choppy shadow | Animated `box-shadow` repaints | Try `filter: drop-shadow()` and compare appearance and device cost |
| Jank during navigation/hydration | Main-thread animation competing with long tasks | Hand suitable motion to CSS or WAAPI |
| React hand-rolled motion stutters | State updates per frame | Update a motion value or the element's style through a ref |
| Drag slows as content grows | Inherited CSS variable, many affected descendants | Set the moving element's transform directly |
| Blur is expensive, especially in Safari | Radius and affected surface | Keep it below about 20px; 2-5px usually softens a crossfade |
| Unchosen properties move | `transition: all` | List the intended properties |
| One-pixel shift at start/end | Layer promotion during the transition | Test narrow `will-change: transform` after observing the shift |

## Property cost and correctness

The browser may perform **layout** (sizes and positions), **paint** (draw into layers), then **composite** (assemble layers). Starting earlier costs more.

- `transform` and `opacity` are the reliable defaults for avoiding layout and paint during motion.
- `box-shadow`, `border-radius` and text colour can repaint without changing layout.
- `width`, `height`, `padding`, `margin`, `top`, `left` and `border-width` can trigger layout, paint and composite.
- Acceleration of `filter`, `clip-path` and background colour varies across browsers and devices. Record it rather than promising it.

Use `translate()` instead of position/margin when the visual should move without reflowing its neighbours. Use `scale()` instead of size changes only when scaling the children and leaving document flow unchanged are correct. A collapse that must move following content needs real layout; keep it short and measure it. `opacity: 0` alone doesn't remove hit targets or accessibility content, so preserve hidden-state semantics.

Don't sacrifice percentage transforms for a possible acceleration gain: `translateY(100%)` correctly hides an unknown-height sheet. Hardware acceleration is progressive enhancement, not a correctness guarantee.

## Driver and main-thread work

`requestAnimationFrame` runs on the main thread alongside scripts, hydration and layout. CSS transitions/keyframes and WAAPI can hand supported properties to the compositor. A JS API calling WAAPI can be accelerated; a JS loop computing each frame cannot escape main-thread contention.

Keep Motion's readable `x`, `y`, `scale` and `rotate` shorthands by default. For motion that drops frames while the main thread is busy, try the full transform string:

```jsx
<motion.div animate={{ transform: "translateX(100px)" }} />
```

Preserve transform composition, motion values and independent timings. Don't rewrite every shorthand as a speculative optimisation. Springs, shared layouts, exits and momentum gestures remain good reasons for a library.

In a custom React animation, inspect state updates in rAF, `pointermove`, `scroll` and drag handlers. Per-frame `setState` adds React rendering work. A motion value or ref update avoids it:

```js
ref.current.style.transform = `translateY(${nextY}px)`;
// Or, with a motion value: y.set(nextY)
```

Inherited CSS variables are another source of work even without React renders. Updating `--swipe-amount` on a parent can invalidate descendant styles. Suspect it when the same drawer slows as its content grows; move the transform update to the element that moves.

## `will-change` comes late

Use it only after an observed layer shift or measured dropped frames, once property cost, main-thread work, per-frame renders, inherited variables and blur have been investigated. It cannot fix layout cost or a blocked animation driver.

Apply it to the moving element, for the needed lifetime, and keep the layer small. Remove it when no longer needed. Global promotion and large permanent layers consume GPU memory; browsers already promote many transform/opacity animations.

An expensive paint on a blurred or filtered element can justify testing layer promotion. Keep the layer as small as the effect allows and measure the benefit; this isn't a reason to promote every filtered element.

## Verify and report

Record dropped frames, long tasks, layout and paint in DevTools Performance. Use the Animations panel for timing inspection. Reproduce on a real mid-range phone using remote debugging when device performance is the claim; desktop CPU throttling doesn't model a weak GPU or limited GPU memory.

For each finding, report the element and source location, supported cause, exact before/after and evidence. Separate **supported by code**, **measured in this browser** and **verified on this device**. If device access is unavailable, name that gap. A smoother-looking laptop preview doesn't establish a device fix.

Order findings by cost: layout before paint, busy-main-thread motion before idle motion. A diagnostic request ends with the report; apply fixes when asked.
