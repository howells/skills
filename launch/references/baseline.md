# Global baseline

Apply this floor first in Phase 4 when missing. Merge missing declarations into existing root files rather than creating a second stylesheet or viewport tag. Express values in the project's styling system and tokens. Never invent values marked `←`; read them from the repo or put them on the human list.

## Head

```html
<html lang="en"> <!-- ← real content language -->
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content" />

<!-- Dual-theme apps. Single-theme apps: one theme-color and single color-scheme. -->
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#ffffff" /> <!-- ← light header bg -->
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0a0a0a" />  <!-- ← dark header bg -->
<meta name="color-scheme" content="light dark" />

<!-- Skip preload when using next/font -->
<link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin />
```

Next.js App Router equivalent:

```tsx
export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  interactiveWidget: "resizes-content",
  colorScheme: "light dark",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#0a0a0a" },
  ],
};
```

`viewport-fit=cover` makes `env(safe-area-inset-*)` non-zero. `interactive-widget=resizes-content` shrinks Android Chrome's layout viewport when the keyboard opens (iOS Safari ignores it; bottom composers still need `visualViewport` handling and an iPhone check). Never include `maximum-scale` or `user-scalable=no`.

## Root CSS

```css
html {
  -webkit-text-size-adjust: 100%;
  -webkit-tap-highlight-color: transparent; /* every control then needs its own :active */
  font-synthesis: none;
  overscroll-behavior: none; /* app shells only; omit on scrolling documents */
}

body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

:focus-visible {
  outline: 2px solid var(--focus-ring, currentColor);
  outline-offset: 2px;
}

input, textarea, select { font-size: 16px; }
button, a, input, select, textarea, [role="button"] { touch-action: manipulation; }
button, [role="button"] { user-select: none; -webkit-user-select: none; }

h1, h2, h3 { text-wrap: balance; }
p { text-wrap: pretty; }
[id] { scroll-margin-top: 64px; } /* ← sticky header height */

@media (prefers-reduced-motion: no-preference) {
  html { scroll-behavior: smooth; }
}

.no-transitions, .no-transitions * { transition: none !important; }
```

## Root gates

- **Hover**: gate `:hover` behind `@media (hover: hover) and (pointer: fine)`. Tailwind v4 `hover:` does this automatically; Tailwind v3 needs `future: { hoverOnlyWhenSupported: true }`.
- **Reduced motion**: swap movement for opacity at shared tokens/keyframes; wrap Motion apps in `<MotionConfig reducedMotion="user">`. Never `* { animation: none !important; transition: none !important; }`.
- **Theme switch**: `next-themes` takes `disableTransitionOnChange`.
- **Dev-only mounts**: gate devtools, inspectors and pickers behind `process.env.NODE_ENV === "development"` (or `import.meta.env.DEV`) with dynamic import so they never enter the production bundle.
