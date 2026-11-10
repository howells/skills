# Touch and viewport fixes

Contents: hover, tap highlight, viewport units, input zoom and keyboard, tap delay and press feedback, overscroll, safe areas, selection, gestures, text inflation.

## Hover stays after a tap

Touch has no hover, so browsers fake one: the first tap applies `:hover` and keeps it until the user taps elsewhere. A button that scales up on hover stays scaled up.

```css
@media (hover: hover) and (pointer: fine) {
  .button:hover { background: var(--gray-3); }
}
```

`(hover: hover)` means the primary pointer can hover. `(pointer: fine)` means the primary pointer is accurate, such as a mouse or a pen; together they exclude devices that fake hover on a finger tap. Tailwind v4's `hover:` already compiles to `@media (hover: hover)`; plain `:hover` in CSS modules and global CSS does not. Never make hover the only way to reach something. Touch users get press feedback from `:active`.

## Gray flash on tap

iOS Safari and Android Chrome paint a translucent highlight over a tapped element. It fights the press feedback you designed.

```css
html { -webkit-tap-highlight-color: transparent; }
```

This removes the only feedback the browser gave, so every tappable element needs an `:active` state in the same change.

## Wrong height

`100vh` is the largest viewport, the height with the browser bars collapsed. At load the toolbar is showing, so a `100vh` element overflows and a bottom-pinned button sits under it.

```css
.app { height: 100dvh; }        /* shells and drawers: tracks the bars as they move */
.hero { min-height: 100svh; }   /* first screens: the smallest viewport, never cut off */
```

`dvh` resizes while the bars move, which is right for a shell and causes shifts in scrolling content. `lvh` is the old `vh`; you almost never want it. In Tailwind use `h-dvh`, `min-h-dvh`, `min-h-svh`, never `h-screen`.

## Input zoom and the keyboard

iOS Safari zooms the page when focus lands on a field whose text is under 16px and does not zoom back. This is why people reach for `maximum-scale=1`, which is the wrong fix: it blocks pinch zoom too.

Find each `input`, `textarea` and `select` style below 16px and raise it to 16px (Tailwind `text-base`) at every width. Leave larger fields alone; a blanket `font-size: 16px` shrinks them. Do not gate it behind `(pointer: coarse)` or a breakpoint: the zoom follows the font size, not the pointer or the screen, and a phone in landscape is wider than `sm`.

Set the keyboard on the field: `inputmode="numeric"` for codes, `"decimal"` for amounts, `type="email"` and `type="tel"` for those fields, `autocapitalize="none"` and `autocorrect="off"` on usernames and codes, `enterkeyhint="send"`, `"search"` or `"done"` so the return key says what it does. Do not autofocus on touch screens: it opens the keyboard unasked.

The keyboard differs by platform. iOS Safari keeps the layout viewport the same height and covers the page; to keep a bottom-pinned input visible, size or offset it from `window.visualViewport`. Android Chrome shrinks the layout viewport when the viewport meta tag adds `interactive-widget=resizes-content`, so `dvh` layouts follow the keyboard. Both need a real device.

## Taps feel late

Two causes stack.

The double-tap-zoom wait: browsers delay a tap to see if a second is coming. `width=device-width` removes most of it; `touch-action: manipulation` removes the rest on that element.

```css
button, a, [role="button"] { touch-action: manipulation; }
```

Feedback on release: a button that only changes on `click` responds when the finger leaves, which reads as lag even at 0ms. Style `:active` (100 to 160ms, ease-out, using the codebase's own motion tokens). In JavaScript, listen to `pointerdown`, not `click`, for the feedback only.

## Overscroll and pull-to-refresh

Scrolling past the top refreshes the page on Android Chrome and rubber-bands the whole page on iOS. That suits a document and breaks an app with its own scrollers, a drawer dragged down, or a canvas.

```css
html { overscroll-behavior: none; }
.sheet-content { overflow-y: auto; overscroll-behavior: contain; }
```

`none` on the root; `contain` on children, which keeps the container's own bounce but stops the page behind it from moving. Never block this with a `touchmove` listener that calls `preventDefault()`: it stops scrolling and makes the listener non-passive, which costs frames. Leave `html` alone when the app is a scrolling document where pull-to-refresh is welcome.

## Safe areas

By default the browser letterboxes the page inside the safe area. A native app paints edge to edge and pads its content away from the notch, Dynamic Island and home indicator.

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

```css
.app-header { padding-top: env(safe-area-inset-top); }
.bottom-bar { padding-bottom: env(safe-area-inset-bottom); }
.sheet      { padding-bottom: calc(1rem + env(safe-area-inset-bottom, 0px)); }
```

Without `viewport-fit=cover` every `env(safe-area-inset-*)` is `0px`. A fixed header does not protect content in the document flow: it scrolls under the notch, and in landscape it runs into the side insets. Pad every container whose text or controls can reach an unsafe edge, fixed or not, and keep its own spacing with `max()` or `calc()`:

```css
.page { padding-inline: max(1rem, env(safe-area-inset-left)) max(1rem, env(safe-area-inset-right)); }
```

Check all four insets in landscape, both ways round. Once the page paints under the bars, the colors behind them need setting: read `safari-bars.md`.

## Selection and callouts

Holding a finger on a web button selects its label or raises the copy/share callout. Native controls never do. Text that is a control is not selectable; text that is content must stay selectable.

```css
button, [role="button"], .tab, .chip, .drag-handle {
  user-select: none;
  -webkit-user-select: none;   /* Safari still needs the prefix */
  -webkit-touch-callout: none; /* no callout on links or images used as controls */
}
```

Use the app's own class names for controls. Ordinary content links keep selection and the long-press callout. Never put `user-select: none` on `body`.

## Gestures and carousels

`touch-action` names what the browser may still do, not what you handle. `pan-y` on a horizontal carousel says: the browser keeps vertical panning, the script takes horizontal. `none` says the element handles everything; use it only where that is true, or the user cannot scroll past it.

Prefer a native track: `scroll-snap-type: x mandatory` on the track and `scroll-snap-align: start` on slides. The browser's physics beat a hand-written spring and `touch-action` becomes unnecessary. When script implements the drag, use `touch-action: pan-y pinch-zoom` so vertical scroll and zoom still work.

## Text inflates in landscape

iOS Safari enlarges text it judges too small when the phone rotates, which breaks a layout sized for its own type.

```css
html { -webkit-text-size-adjust: 100%; }
```

Use `100%`, never `none`, which stops text scaling with zoom in older browsers.
