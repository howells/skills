# Recipes

Starting points for the components that come up most. Adapt the selectors to the project's primitives and swap in its own tokens; the curve names are the ones defined in `values.md`. Each recipe assumes it has already passed the gate.

## Press

Any control that can be pressed. `scale()` shrinks the label and icon too, which is what reads as a physical press.

```css
.pressable {
  transition: transform 120ms var(--ease-out-quint);
}
.pressable:active {
  transform: scale(0.97);
}
```

Tailwind: `transition-transform duration-120 ease-out-quint active:scale-97`. `:active` is a real press on touch, so it needs no hover gating.

## Anchored popover, menu or select

It grows out of the thing that opened it.

```css
.menu-popup {
  transform-origin: var(--transform-origin); /* Base UI; Radix: var(--radix-dropdown-menu-content-transform-origin) */
  transition:
    opacity 180ms var(--ease-out-quint),
    transform 180ms var(--ease-out-quint);
}
.menu-popup[data-starting-style],
.menu-popup[data-ending-style] {
  opacity: 0;
  transform: scale(0.96);
}
```

Radix marks state with `data-state="open"` and `data-state="closed"` instead; the exit needs presence handling (Radix's `forceMount` with a motion library, or its CSS animation support).

## Tooltip group

```css
.tip {
  transform-origin: var(--transform-origin);
  transition:
    opacity 140ms var(--ease-out-quint),
    transform 140ms var(--ease-out-quint);
}
.tip[data-starting-style],
.tip[data-ending-style] {
  opacity: 0;
  transform: scale(0.97);
}
.tip[data-instant] {
  transition-duration: 0ms;
}
```

The first tooltip waits and animates. Moving along a toolbar after that shows each neighbour at once.

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

  @starting-style {
    opacity: 0;
    transform: scale(0.96);
  }
}
dialog:not([open]) {
  opacity: 0;
  transform: scale(0.96);
}
dialog::backdrop {
  background: rgb(0 0 0 / 0.4);
  transition: background-color 220ms var(--ease-out-quint), display 220ms allow-discrete, overlay 220ms allow-discrete;
}
@starting-style {
  dialog[open]::backdrop { background: rgb(0 0 0 / 0); }
}
```

`allow-discrete` on `display` and `overlay` keeps the native dialog in the top layer until its exit finishes.

## Sheet

```css
.sheet {
  transform: translateY(0);
  transition: transform 360ms var(--ease-sheet);
}
.sheet[data-closed] {
  transform: translateY(100%);
}
```

Once it can be dragged it becomes a gesture: see `gestures.md`.

## Notice

Notices arrive in bursts, so they use transitions, which retarget, never keyframes, which restart.

```css
.notice {
  opacity: 1;
  transform: translateY(0);
  transition:
    opacity 320ms var(--ease-out-quint),
    transform 320ms var(--ease-out-quint);

  @starting-style {
    opacity: 0;
    transform: translateY(100%);
  }
}
```

Without `@starting-style`, render with a `data-mounted="false"` attribute and flip it to `true` in an effect after the first paint. When notices stack and the list closes up, opacity and height compete; there's no formula for that pair, so tune it by eye in slow motion.

## Collapse

The one sanctioned layout animation. Keep it short.

```css
.collapse {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 200ms var(--ease-out-quint);
}
.collapse[data-open] {
  grid-template-rows: 1fr;
}
.collapse > .collapse-inner {
  overflow: hidden;
}
```

Animating grid rows from `0fr` to `1fr` reaches the content's natural height with no measuring. Where `interpolate-size: allow-keywords` is supported, `height: 0` to `height: auto` also works directly. Fade the inner content alongside if it would otherwise appear clipped.

## Staggered group

For a grid seen occasionally, not a list scrolled all day.

```css
.stagger-item {
  animation: rise 280ms var(--ease-out-quint) backwards;
  animation-delay: calc(var(--i) * 50ms);
}
@keyframes rise {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
}
```

Set `--i` inline per item (`style={{ "--i": index }}`) and cap it, so the tenth item isn't waiting half a second. Keyframes are right here because the entrance runs once; `backwards` fill holds the first frame during the delay. Never disable input while it plays.

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

Fire the action on `transitionend` of the fill, not on a timer that can drift from what's on screen.

## Moving selection indicator

With Motion, render the indicator inside the active item with a shared `layoutId` and a spring; it slides between items and interrupts cleanly.

```jsx
{isActive && (
  <motion.span layoutId="tab-indicator" transition={{ type: "spring", visualDuration: 0.25, bounce: 0 }} />
)}
```

Without a library, when both the background and the text colour change, render a second copy of the tab row styled as selected, lay it over the first, and animate its `clip-path: inset()` to the active tab's bounds. Text and background change in lockstep because one element is being revealed rather than two colours being interpolated.

## A crossfade that double-exposes

When two states visibly overlap and no curve or duration fixes it, blur the seam so the eye reads one changing thing.

```css
.swap {
  transition:
    opacity 180ms ease,
    filter 180ms ease;
}
.swap[data-swapping] {
  opacity: 0.6;
  filter: blur(3px);
}
```

## Changing numbers

A counter or price that updates in place uses tabular figures (`font-variant-numeric: tabular-nums`, Tailwind `tabular-nums`) so the digits don't jitter sideways. Animate the number only when the change itself is the news.

## Scripted, without a library

```js
panel.animate(
  [{ clipPath: "inset(0 0 100% 0)" }, { clipPath: "inset(0 0 0 0)" }],
  { duration: 480, easing: "cubic-bezier(0.77, 0, 0.175, 1)", fill: "forwards" },
);
```

The Web Animations API runs with CSS-grade performance, can be paused, reversed and cancelled, and costs no bundle.

## Reveal on scroll

Marketing and editorial pages only; never on a screen someone works in daily.

```css
.reveal {
  clip-path: inset(0 0 100% 0);
  transition: clip-path 560ms var(--ease-in-out-quart);
}
.reveal[data-seen] {
  clip-path: inset(0 0 0 0);
}
```

Set `data-seen` once from an `IntersectionObserver` with a negative bottom margin, or Motion's `useInView` with `{ once: true }`. Revealing again on every pass makes the page fight its reader.
