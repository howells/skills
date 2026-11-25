# Lane A — Accessibility

Fixes that stop excluding keyboard, screen-reader, low-vision or motion-sensitive users. Deep fixes belong to `chiaroscuro`.

- **A1. Icon buttons have a name (BLOCKER)** — Hunt: `<button>` / `<a>` with only an icon child; `aria-label="icon"`. Fix: add `aria-label` naming the action ("Close dialog", "Search"). Decorative icons beside text get `aria-hidden="true"`.
- **A2. Buttons are buttons (BLOCKER)** — Hunt: `onClick` on `div`, `span`, `li`, `svg`; `role="button"`. Fix: `<button type="button">` for actions, `<a href>` for navigation.
- **A3. Focus is visible (BLOCKER)** — Hunt: `outline-none` / `outline: none` / `outline: 0` without a `:focus-visible` replacement, or clipped by `overflow-hidden`. Fix: neutral `:focus-visible` outline (`2px`, `outline-offset: 2px` or `-2px` inside clipped boxes).
- **A4. Labels are associated (BLOCKER)** — Hunt: `<label>` without `htmlFor`/`for`; placeholder-only inputs. Fix: wire `for`/`id` or wrap the input; icon-only search inputs get `aria-label`.
- **A5. Modals manage focus (BLOCKER)** — Hunt: hand-rolled `fixed` overlays toggled by `useState` without a dialog primitive or Escape handler. Fix: swap to the project's dialog primitive (Base UI, Radix, native `<dialog>` `showModal()`); if none exists, put on human list (`chiaroscuro`).
- **A6. Hidden UI is out of tab order (BLOCKER)** — Hunt: off-screen drawers or closed panels hidden only with `opacity-0` or `translate-*`. Fix: add `inert` or `visibility: hidden` when closed.
- **A7. Errors are not colour-only (BLOCKER)** — Hunt: `border-red-*` without an adjacent message or `aria-invalid`. Fix: pair colour + icon + colocated text wired via `aria-describedby` and `aria-invalid`.
- **A8. Reduced motion honoured (BLOCKER for large movement, SHOULD FIX otherwise)** — Hunt: transforms/slides/parallax/autoplaying video/smooth-scroll without `prefers-reduced-motion` or `MotionConfig reducedMotion="user"`. Fix: swap movement for opacity (`motion-safe:` / `motion-reduce:`), gate smooth scroll under `no-preference`, never autoplay video under `reduce`, pause looping CSS on a mid-frame. Never blank out all transitions.
- **A9. Contrast passes in both themes (BLOCKER for body text, SHOULD FIX otherwise)** — Hunt: light greys (`text-gray-400`), placeholders, text on tinted badges or images, `:disabled` opacity in both themes. Floor: 4.5:1 body / 3:1 large & UI controls (WCAG AA); sanity-check APCA (`|Lc| >= 75` body, `>= 60` content labels, `>= 30` icons/borders). Repair by moving OKLCH lightness `L`, keeping hue.
- **A10. Media and illustrations labelled or hidden (SHOULD FIX)** — Hunt: `<img>` without `alt`, decorative `<svg>` without `aria-hidden="true"`, code-built illustrations without `role="img"` + `aria-label`. Missing `alt` on the primary product shot is a BLOCKER.
- **A11. DOM order matches visual order (SHOULD FIX)** — Hunt: `order-*`, `flex-row-reverse`, positive `tabindex`. Fix in markup.
- **A12. Landmarks and headings (SHOULD FIX)** — Hunt: missing `<main>`, multiple `<h1>`, skipped heading levels, missing `<html lang>`, stale `document.title` on client navigation.
- **A13. Skip link on long navigation (SHOULD FIX)** — Add `<a href="#main">` visible on `:focus-visible` when nav precedes `<main>`.
- **A14. Tooltips hold no interactive content (SHOULD FIX)** — Hunt: links or buttons inside tooltips; move to a click-triggered popover.
- **A15. Hover enhances, never enables (SHOULD FIX)** — Hunt: `opacity-0 group-hover:opacity-100` hiding action buttons. Fix: always visible on coarse pointers, reveal on `:focus-within` for keyboards.
- **A16. Async changes announced (SHOULD FIX)** — Hunt: hand-rolled toasts, inline "Saved" notices, result counts. Fix: pre-mounted `role="status"` (`aria-live="polite"`) or `role="alert"`.
- **A17. Presentation timers pause when hidden (SHOULD FIX)** — Hunt: toast/undo `setTimeout` without `visibilitychange`, hover, or focus pause. Real deadlines (session expiry) never pause.
- **A18. Focus survives removal and scrolling (SHOULD FIX)** — Hunt: deleting a focused row without moving focus to its neighbour or list heading.
- **A19. OS-accurate shortcuts (POLISH)** — Show `⌘` on macOS and `Ctrl` elsewhere; bind `e.metaKey || e.ctrlKey`.
- **A20. Device check (always)** — Put on device list: complete the core flow keyboard-only (Tab, Enter, Escape, arrows) and walk the main screen with VoiceOver (`Cmd+F5`).
