# Lane B — Performance

Catches work that hides on a fast laptop and stalls mid-range phones. Deep fixes belong to `zoetrope` (animation perf) or `fettle` (architecture/queries).

- **B1. Media reserves its space (BLOCKER)** — Hunt: `<img>`, `<video>`, `<iframe>` without `width`/`height` or `aspect-ratio`; `next/image` `fill` in an unsized parent. Fix: add dimensions or `aspect-ratio`.
- **B2. Fonts preloaded, subset, minimal weights (SHOULD FIX)** — Hunt: un-preloaded `@font-face` woff2 (missing `crossorigin`), >3 unused weights, `.ttf`/`.otf` served to browsers, missing `font-synthesis: none`. (`next/font` handles preload; check only used weights are listed.)
- **B3. Hero preloaded, below-the-fold lazy (SHOULD FIX)** — Hunt: LCP hero image with `loading="lazy"` (remove it; add `priority` / `<link rel="preload" as="image">`); below-the-fold gallery/list images missing `loading="lazy" decoding="async"`. Never `priority` on every image.
- **B4. Images sized to display (SHOULD FIX)** — Hunt: raw `<img>` when an image component exists; >300KB PNG/JPG photos in `public/`; `unoptimized` on `next/image`. Use WebP/AVIF + `sizes`/`srcset`.
- **B5. Animate compositor properties only (BLOCKER on frequent interactions, SHOULD FIX otherwise)** — Hunt: transitions/keyframes on `width`, `height`, `margin`, `padding`, `top`, `left`. Swap to `transform`, `opacity`, `clip-path`, or `grid-template-rows: 0fr -> 1fr` for rare accordions.
- **B6. No `transition-all` / `transition: all` (SHOULD FIX)** — Hunt: `transition-all`, `transition: all`, bare Tailwind `transition` where broad. Name exact properties (`transition-[opacity,transform]`).
- **B7. No React `setState` per frame (BLOCKER)** — Hunt: `set*` inside `onScroll`, `onPointerMove`, `requestAnimationFrame`. Write directly to a ref's `style.transform` or a Motion value.
- **B8. Navigation motion stays off main thread (SHOULD FIX)** — Hunt: `layoutId` / layout animations firing during route navigation or data fetch; prefer CSS transitions or compositor transforms.
- **B9. No parent CSS custom properties driving child transforms per frame (SHOULD FIX)** — Hunt: `setProperty("--x", ...)` per frame on a container read by children; set `transform` on the moving element directly.
- **B10. Blur under 20px (SHOULD FIX)** — Hunt: `blur(` > 20px on animated elements, `backdrop-filter: blur()` on full-viewport overlays, `blur-3xl` glows.
- **B11. Targeted `will-change` (POLISH)** — Hunt: `will-change: all`, `will-change` on `*`, or naming layout properties. Keep only on elements with observed first-frame hitching.
- **B12. Long lists virtualised (BLOCKER when unbounded, SHOULD FIX >200 rows)** — Hunt: unpaginated `.map()` over user/server data with no virtualiser. Simple list: add project's virtualiser; complex table: human list (`fettle`).
- **B13. Off-screen work pauses (POLISH)** — Hunt: looping `<video>`, infinite keyframes, `<canvas>` loops, `setInterval` polling without `IntersectionObserver` / `visibilitychange`.
- **B14. Theme toggles don't tween every colour (SHOULD FIX)** — Hunt: `ThemeProvider` missing `disableTransitionOnChange`, or custom toggle missing `.no-transitions` double-rAF guard.
- **B15. Static content routes stay static (SHOULD FIX)** — Hunt: `force-dynamic`, `cache: "no-store"`, or `cookies()`/`headers()` in marketing/blog/docs layouts (often caused by an auth-aware CTA — resolve that CTA on the client instead).
- **B16. Debounced search & passive scroll listeners (SHOULD FIX)** — Hunt: `fetch` directly inside `onChange` (debounce ~300ms + `AbortController`); unthrottled layout reads in `scroll`/`resize`; non-passive scroll listeners.
- **B17. Heavy rarely-used UI code-split (SHOULD FIX)** — Hunt: editors, chart kits, syntax highlighters or namespace icon imports loaded statically in root layout. Lazy-import with a sized skeleton fallback.
- **B18. Device check (always)** — Put on device list: profile the production build on a mid-range phone over remote debugging and run Lighthouse mobile against the production build (never dev server).
