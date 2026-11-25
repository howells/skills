# Lane G — Theming

Defect sweep of the secondary theme (and single-theme declarations). Deep colour and dark-mode design belongs to `chiaroscuro`.

Check from recon first: single-theme apps run **G1** and **G8** only; dual-theme apps run the full lane; apps with dead/unreachable `dark:` classes run **G2** and **G8**.

- **G1. Single-theme apps declare their one scheme (SHOULD FIX)** — Hunt: dark-only app missing `color-scheme: dark` (gets white native scrollbars/inputs); light-only app declaring `color-scheme: light dark` (gets dark native controls on dark-mode phones). Declare only the designed scheme.
- **G2. Half a dark mode is worse than none (BLOCKER when reachable)** — Hunt: `dark:` classes on some components while layout, inputs or text tokens ignore it, or Tailwind `media` dark mode firing on a light-only design. Put on human list: either finish the theme (`chiaroscuro`) or disable the toggle and lock `color-scheme: light`.
- **G3. Text contrast holds in both themes (BLOCKER for body text)** — Hunt: hardcoded greys (`text-gray-500`, `#6b7280`), muted/placeholder/disabled tokens, tinted badges and text over images in dark mode. On dark (`L <= 0.25`), neutral body text wants `L >= 0.85`; short brand labels clear ~6:1 around `L 0.66–0.72` without turning pastel.
- **G4. Hardcoded colours flip cleanly (SHOULD FIX)** — Hunt: `bg-white`, `text-black`, `border-gray-200`, `#fff`/`#000` in components or inline SVG `fill`/`stroke` where semantic tokens exist. Point at semantic tokens and use `currentColor` in icons; don't scatter one-off `dark:` overrides when a token scale flips at the root. Flag dark-text raster logos on the human list.
- **G5. Elevation survives dark mode (SHOULD FIX)** — Hunt: `box-shadow` depth tokens or cards/popovers with no dark-mode counterpart (black shadows vanish on dark grounds). Collapse dark elevation tokens to a subtle white ring (`0 0 0 1px rgb(255 255 255 / 0.08)` or `dark:inset-ring-white/10`), and flip image outlines to `outline-white/10`.
- **G6. Media works on both backgrounds (SHOULD FIX)** — Hunt: transparent PNGs/SVGs with dark text or linework, light-UI screenshots on dark backgrounds, charts with hardcoded axis colours, dark favicons vanishing on dark tab bars. Wire `-dark` assets with `<picture>` or theme classes; flag missing assets on the human list.
- **G7. Embedded third-party UI follows the theme (SHOULD FIX)** — Hunt: Shiki/Prism syntax highlighters, Stripe Elements, auth/chat widgets or maps hardcoded to light mode. Pass the resolved theme through.
- **G8. Browser chrome and autofill match (POLISH)** — Verify `theme-color` per scheme (C18), `color-scheme`, legible `::selection`, and `input:-webkit-autofill` inset box-shadow override if browser autofill breaks dark forms.
- **G9. First paint and clean switches** — Theme flash is E5; colour ripple on toggle is B14 (count each once).
- **G10. Device check (always)** — Put on device list: switch to the other theme and walk every route (auth, settings, empty states, error pages, modals, dropdowns, tooltips) and toggle the theme while a modal is open.
