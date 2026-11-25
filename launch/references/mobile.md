# Lane C — Mobile

Real-hardware mobile defects. Deep layout and phone-browser work belongs to `reflow`.

- **C1. Never disable zoom (BLOCKER)** — Hunt: `user-scalable=no`, `maximum-scale=1`, `maximumScale`, `userScalable` in viewport meta or Next.js `viewport`. Remove and fix input font size (C3).
- **C2. Hover is gated (SHOULD FIX)** — Hunt: raw CSS `:hover` outside `@media (hover: hover)` or Tailwind v3 without `future: { hoverOnlyWhenSupported: true }`. (Tailwind v4 `hover:` gates automatically.)
- **C3. Inputs are ≥16px on touch (BLOCKER)** — Hunt: `font-size` < 16px or `text-sm`/`text-xs` on `input`, `textarea`, `select`, or `contenteditable`. Fix: `text-base pointer-fine:text-sm` (Tailwind v4.1+) or `@media (pointer: coarse) { font-size: 16px }`. Never gate on width (`md:text-sm` — iPads still zoom). Add `inputmode`, `autocomplete`, `enterkeyhint`, `autocapitalize="none"` where appropriate.
- **C4. Tap targets ≥44px (SHOULD FIX)** — Hunt: icon buttons (`size-6`, `size-8`), toast dismisses, row actions without hit-area extension. Fix: `relative before:absolute before:-inset-2.5` (never overlapping neighbours).
- **C5. Taps feel instant (SHOULD FIX)** — Hunt: tappable elements missing `touch-action: manipulation` or `:active` press feedback (`active:scale-[0.97]`).
- **C6. Tap highlight cleared (SHOULD FIX)** — Set `html { -webkit-tap-highlight-color: transparent }` and verify controls have `:active` states (C5).
- **C7. `dvh`/`svh`, not `vh` (SHOULD FIX)** — Hunt: `100vh`, `h-screen`, `min-h-screen`. Fix: `h-dvh` for app shells/drawers, `min-h-svh` for marketing heroes. Desktop-only admin tools are exempt.
- **C8. Safe areas respected (SHOULD FIX)** — Hunt: `fixed`/`sticky` top/bottom bars, sheets and toasts without `env(safe-area-inset-*)`, or `env()` used without `viewport-fit=cover`.
- **C9. Overscroll contained (SHOULD FIX)** — Hunt: `touchmove` + `preventDefault()`; inner scrollers (`overflow-y-auto`) without `overscroll-contain`; app shells without `overscroll-none` on root.
- **C10. Controls non-selectable, content selectable (SHOULD FIX)** — Hunt: `select-none` on `body`/`*` (defect — remove); buttons/tabs missing `select-none` (polish).
- **C11. Gesture axes declared (SHOULD FIX)** — Hunt: carousels (`touch-action: pan-y`), vertical sheet handles (`pan-x`), 2D canvases (`none`) missing `touch-action`. Prefer CSS `scroll-snap` for carousels.
- **C12. Inline autoplay video (SHOULD FIX)** — Hunt: `<video autoPlay>` missing `muted` or `playsInline`. Respect reduced motion (A8).
- **C13. No autofocus on touch (SHOULD FIX)** — Hunt: `autoFocus` or mount `.focus()` without a `matchMedia("(pointer: fine)")` guard.
- **C14. Software keyboard doesn't cover inputs (SHOULD FIX)** — Hunt: bottom-pinned composers/footers missing `interactive-widget=resizes-content`; flag bottom composers on the device list for iPhone `visualViewport` verification.
- **C15. Fixed bottom bars clear content (SHOULD FIX)** — Pad the scroll container by fixed CTA/banner height + `env(safe-area-inset-bottom)`.
- **C16. Sticky headers leave room (SHOULD FIX)** — Cap mobile sticky header height and set `scroll-margin-top` on `[id]` to its height.
- **C17. No horizontal overflow (SHOULD FIX)** — Hunt: `w-screen` / `100vw`, fixed widths >340px, bare `<table>`/`<pre>` without `overflow-x-auto`, user strings without `wrap-anywhere`/`break-words`. Fix the overflowing element; never slap `overflow-x-hidden` on `body` (breaks `position: sticky`).
- **C18. Status bar matches top of page (POLISH)** — One `<meta name="theme-color">` per scheme matching the header background, read from repo tokens.
- **C19. Device check (always)** — Put on device list: open the dev server over LAN IP on a real phone (portrait + landscape, keyboard open) to verify tap feedback, safe areas, input zoom, overscroll and sticky hover.
