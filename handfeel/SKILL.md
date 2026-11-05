---
name: handfeel
description: "Make a web app feel native on a phone: safe areas, viewport units, input zoom, tap and hover on touch, overscroll, the color behind Safari's bars, PWA install. Not for responsive layout (`reflow`), app shells (`armature`) or motion (`zoetrope`)."
---

# Handfeel

In textiles, hand is how a cloth feels to the touch. A web app on a phone has the same test: a handful of platform defaults tell the user they are holding a website. This pass finds them and removes them, one by one.

## The line with other skills

`handfeel` owns how the browser and the touch screen behave: viewport and meta tags, safe areas, input zoom, tap, hover and selection on touch, overscroll, the colors behind the browser bars, installed-app meta, device testing. `reflow` owns how layouts adapt across sizes: breakpoints, overflow, tables, navigation, touch-target size. `armature` owns what scrolls. `zoetrope` owns motion. If a fix changes how a layout looks at a width, it is `reflow`; if it changes how the phone treats the page, it is here.

## Hard rules

1. **Never disable zoom.** `user-scalable=no` and `maximum-scale=1` fail users who need to zoom. Fix the input font size, which is what caused the zoom.
2. **Ask the platform, never sniff.** Use `(hover: hover)`, `(pointer: fine)`, `env()` and `dvh`. Do not branch on user agent, screen width or `ontouchstart` to guess at touch.
3. **Write for touch and mouse together.** iPads have trackpads, laptops have touch screens. Gate by capability, not by device.
4. **CSS or a meta tag before JavaScript.** Almost every fix is one declaration. A `useIsTouchDevice` hook to hide hover styles is the wrong tool.
5. **Apply a fix only where its reason applies.** `user-select: none` on a button is correct; on body text it is a defect. State the reason with each change.
6. **Desktop emulation proves nothing here.** Sticky hover, the browser bars, safe areas, input zoom and the keyboard do not reproduce in it. Report each fix as checked on a device or Simulator, or as unchecked.

## 1. Read the app

Find the viewport meta tag (in Next.js, the `viewport` export), the global stylesheet, the theme and color-scheme setup, the app's fixed elements (headers, tab bars, sheets, toasts), its scroll containers, and whether it has a manifest. Note the styling system: in Tailwind v4 the `hover:` variant is already gated to hover-capable pointers.

Done when you can name where each fix below goes.

## 2. Match symptoms to fixes

| Symptom | Fix |
| --- | --- |
| Hover style stays after a tap | Put every `:hover` rule inside `@media (hover: hover) and (pointer: fine)` |
| Gray flash on tap | `-webkit-tap-highlight-color: transparent`, then give every tappable its own `:active` |
| Bottom UI hidden under Safari's toolbar | `100dvh` for shells, `100svh` for heroes, never `100vh` |
| Page zooms in on focus | Raise fields below 16px to 16px |
| Taps feel late | `touch-action: manipulation` on controls; feedback on press, not release |
| Pull-down refreshes the page or rubber-bands the shell | `overscroll-behavior: none` on `html`; `contain` on inner scrollers |
| Content under the notch or home indicator | `viewport-fit=cover` plus `env(safe-area-inset-*)` on every container that reaches an edge |
| Long-press selects a label or opens a callout | `user-select: none` and `-webkit-touch-callout: none` on controls only |
| Custom drag or carousel scrolls the wrong way | Native scroll-snap; otherwise `touch-action: pan-y pinch-zoom` |
| Wrong-colored bands around Safari's bars | Read [`references/safari-bars.md`](references/safari-bars.md) |
| Installed app opens with browser chrome or the wrong icon | Read [`references/installed-app.md`](references/installed-app.md) |

Read [`references/touch-and-viewport.md`](references/touch-and-viewport.md) before applying any row except the last two: it gives the reason, the exact code and the traps for each. Read each reference file with its own command.

## 3. Apply the baseline

When the app targets phones and has none of this, add it first:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#ffffff">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0a0a0a">
```

```css
html {
  -webkit-tap-highlight-color: transparent;
  -webkit-text-size-adjust: 100%;
  overscroll-behavior: none; /* drop for a scrolling document where pull-to-refresh is welcome */
}
button, a, [role="button"] { touch-action: manipulation; }
button, [role="button"], a.button {
  user-select: none;
  -webkit-user-select: none;
  -webkit-touch-callout: none;
}
```

Use the app's own selector for links styled as buttons instead of assuming `.button`. Ordinary content links keep selection and the long-press callout.

Raise only the fields whose font size is below 16px, on every pointer type; never shrink a larger field to 16px, and never block pinch zoom.

Set `theme-color` to the page's actual color at the very top edge, not the brand color. The media-qualified pair follows the OS setting; if the app has its own theme toggle, use one unqualified tag and update it from the app's theme state. Move hover rules into the capability query as you meet them.

## 4. Bars and installed app

Run these only when the app needs them.

- Browser users see a band of the wrong color around Safari's status bar or toolbar: before fixing it, read [`references/safari-bars.md`](references/safari-bars.md) and follow the full method.
- The app will be added to the home screen or must install: before changing the manifest or icons, read [`references/installed-app.md`](references/installed-app.md).

## 5. Check on a device

Before checking, read [`references/device-testing.md`](references/device-testing.md): how to reach the app from a phone or the iOS Simulator and what each can and cannot show.

- Open every state you changed on an iPhone or in the Simulator: tap, long-press, focus an input, open the keyboard, rotate, scroll to the ends.
- Check an installed copy if the app is installable.
- Where no device or Simulator is available, say so and list each fix as unchecked.

## Report

What was wrong (symptom and reason, one line each), what changed (file and declaration), and what is checked on a device versus unchecked. Do not claim a fix works from emulation or from code alone.
