---
name: reflow
description: "Make a web app responsive and at home on mobile: layouts on small laptops, tablets and phones, overflow, touch targets, safe areas, input zoom, tap and hover on a phone, Safari bar color, PWA install. Not for app shells (`armature`), motion (`zoetrope`) or QA reports (`fieldtest`)."
---

# Reflow

Make a web app work on every screen: how its layouts adapt across sizes, and how a phone's browser treats the page. Leave the desktop layout alone unless it is the cause. When a fix needs a new visual idea rather than an adaptation, note it for `chiaroscuro` instead of inventing one.

Asked about one symptom, go straight to its row in the table and skip the sweep.

## Rules

- **Fix the cause of overflow, never hide it on an ancestor.** Usually a flex or grid child missing `min-w-0`, or a wide table that needs its own scroll wrapper.
- **Phones get one column.** Side panels go behind a disclosure, sheet or tab; never shrink columns until they are unreadable.
- **Strip chrome as the screen shrinks.** Decorative borders, nested panels and wrappers that earned their place at desktop go. The phone layout should feel designed for the phone, not a desktop with pieces removed.
- **Break where the content breaks**, not at device names. Three breakpoints usually suffice. Container queries when a shared component depends on its own width.
- **Ask the platform, never sniff.** Use `(hover: hover)`, `(pointer: fine)`, `env()` and `dvh`. iPads have trackpads and laptops have touch screens, so gate by capability, not by user agent, screen width or `ontouchstart`.
- **CSS or a meta tag before JavaScript.** Almost every phone fix is one declaration.
- **Apply a fix only where its reason applies.** `user-select: none` on a button is correct; on body text it is a defect. State the reason with each change.
- **Desktop emulation proves layout only.** Sticky hover, the browser bars, safe areas, input zoom and the keyboard do not reproduce in it. Report each of those fixes as checked on a device or Simulator, or as unchecked; with no browser at all, every fix is unchecked.

## Symptoms

Before applying a row, read the reference file its group names. The patterns are written in Tailwind v4; in another styling system apply the same CSS.

Layout across sizes, [references/responsive.md](references/responsive.md):

| Symptom | Fix |
| --- | --- |
| Page scrolls sideways | Find the element wider than the viewport; `min-w-0` on the flex or grid child, or a scroll wrapper on the table |
| Wide table | Horizontal scroll inside its own wrapper; a card stack only for 2 to 4 columns |
| Navigation or tabs do not fit | A disclosure, dialog or compact bar chosen from the content; tab rows scroll horizontally |
| Small tap targets | At least 44 by 44 CSS pixels on coarse pointers, by expanding the hit area |
| Action or menu reachable only by hover | A tap equivalent |
| Side panel squeezes the content | Behind a disclosure, sheet or tab on phones |

Phone-browser behavior, [references/touch-and-viewport.md](references/touch-and-viewport.md):

| Symptom | Fix |
| --- | --- |
| Page zooms in when a field is focused | Raise fields below 16px to 16px at every width; never `user-scalable=no` or `maximum-scale=1` |
| Bottom UI hidden under Safari's toolbar | `100dvh` (`h-dvh`) for shells, `100svh` for heroes, never `100vh` or `h-screen` |
| Content under the notch or home indicator | `viewport-fit=cover` plus `env(safe-area-inset-*)` on every container that reaches an edge |
| Hover style stays after a tap | Put every `:hover` rule inside `@media (hover: hover) and (pointer: fine)` |
| Gray flash on tap | `-webkit-tap-highlight-color: transparent`, then give every tappable its own `:active` |
| Taps feel late | `touch-action: manipulation` on controls; feedback on press, not release |
| Pull-down refreshes the page or rubber-bands the shell | `overscroll-behavior: none` on `html`; `contain` on inner scrollers |
| Long-press selects a label or opens a callout | `user-select: none` and `-webkit-touch-callout: none` on controls only |
| Custom drag or carousel scrolls the wrong way | Native scroll-snap; otherwise `touch-action: pan-y pinch-zoom` |
| Text inflates in landscape | `-webkit-text-size-adjust: 100%` on `html` |

Each of these has its own method; read and follow the whole file:

| Symptom | Read |
| --- | --- |
| Wrong-colored bands around Safari's status bar or toolbar | [references/safari-bars.md](references/safari-bars.md) |
| The app must install, or opens from the home screen with browser chrome or the wrong icon | [references/installed-app.md](references/installed-app.md) |

## Steps

1. **Read the app.** Find the viewport meta tag (in Next.js, the `viewport` export), the global stylesheet, the theme setup, the fixed elements (headers, tab bars, sheets, toasts), the scroll containers and any manifest. List the views: every route in scope, plus the states that change layout (empty, long content, open dialogs, sheets and menus, selection bars, errors).
2. **Add the baseline** when the app targets phones and lacks it:

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

   Use the app's own selector for links styled as buttons instead of assuming `.button`. Set `theme-color` to the page's actual color at the very top edge, not the brand color. The media-qualified pair follows the OS setting; if the app has its own theme toggle, use one unqualified tag and update it from the app's theme state.
3. **Load each view at these sizes.** Set the viewport through the session's browser tool, not by resizing a window.

   | Size | Stands for |
   | --- | --- |
   | 1440 × 900 | reference desktop |
   | 1280 × 720 | small laptop |
   | 1024 × 768 | tablet landscape, cramped laptop |
   | 768 × 1024 | tablet portrait |
   | 360 × 740 | phone |

   Plus a phone in landscape (740 × 360) and one view at 200% zoom, taken as a 720 × 450 viewport. Note horizontal overflow (`document.scrollingElement.scrollWidth > clientWidth`, and the element causing it), content clipped or truncated so it loses meaning, primary actions you have to hunt for, small touch targets, fields under 16px, ungated hover, and chrome crowding the screen.
4. **Fix in this order**: shell, navigation, text and forms, overflow, individual components, then phone-browser behavior.
5. **Recheck** changed layouts and every view that uses a changed component, at the affected widths. A shared-component fix moves other views.
6. **Check phone-browser fixes on a device or the iOS Simulator.** Before checking, read [references/device-testing.md](references/device-testing.md): how to reach the app from each, what each can show, and the pass to run.

## Report

A table of views by size, each cell passing or naming what still fails. Then the fixes: file, declaration and the reason for each, with every phone-browser fix marked checked on a device or unchecked.
