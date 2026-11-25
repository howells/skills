# Lane F — Motion

Catches motion that reads as broken or sluggish. Deep timing, spring and gesture craft belongs to `zoetrope`. (Layout-property animation is B5, `transition-all` B6, reduced motion A8 — count each once.)

- **F1. High-frequency and keyboard actions don't animate (BLOCKER when it delays input, SHOULD FIX otherwise)** — Hunt: enter animations on command palettes (`⌘K`), animated arrow-key highlight movement, transitions on high-frequency tab switches or keyboard shortcuts. Cut to instant; ask before removing deliberate rare celebrations.
- **F2. Nothing enters with `ease-in` (SHOULD FIX)** — Hunt: `ease-in` (not `ease-in-out`) on entrances. Entrances use `ease-out`; on-screen moves use `ease-in-out`; hovers ~150ms `ease`. Reuse existing easing tokens.
- **F3. Product UI motion stays under 300ms (SHOULD FIX)** — Hunt: `duration-500`, `0.5s`, long transition delays on product UI (hover/press 100–150ms, menus/popovers 150–250ms, modals/drawers 200–300ms; exits 20–30% faster). Page transitions (300–400ms) and gesture springs are exempt.
- **F4. Nothing enters from `scale(0)` or across the viewport (SHOULD FIX)** — Hunt: `scale(0)`, `scale-0`, `initial={{ scale: 0 }}`, `translateY(100vh)` on small elements. Start at `scale(0.95)`–`scale(0.97)` with `opacity: 0` and 8–16px travel.
- **F5. Anchored popovers scale from their trigger (SHOULD FIX)** — Hunt: scaling popovers, menus and tooltips without `transform-origin` wired to the primitive's origin variable (`--transform-origin` / `--radix-popper-transform-origin`). Centred dialogs stay centred.
- **F6. Toggled UI is interruptible (SHOULD FIX)** — Hunt: `@keyframes` on open/close toggles, drawers, accordions or toasts (restarts from zero mid-flight); fixed tweens on dragged sheets. Use CSS transitions or springs (`visualDuration`, not `duration`, so release velocity carries through).
- **F7. Paired elements share timing (SHOULD FIX)** — Hunt: dialog/drawer overlay and content using different durations or curves. Match them.
- **F8. Exits actually run (SHOULD FIX)** — Hunt: `exit` props on Motion elements with no `<AnimatePresence>` ancestor, or CSS enter animations torn down instantly by `display: none`.
- **F9. Resting elements don't animate on initial paint (SHOULD FIX)** — Hunt: `<AnimatePresence>` around tabs/toggles/icons missing `initial={false}`; `layoutId` indicators sliding in from `(0, 0)` on mount.
- **F10. Hover motion never moves its own hit area (SHOULD FIX)** — Hunt: `:hover { transform: translateY(...) }` or hover `scale` > 1.02 on the hovered element itself (flickers at the edge). Listen for hover on a stationary parent and animate a child; remove hover scale on non-clickable elements.
- **F11. Toolbar tooltips share one provider (POLISH)** — Hunt: per-tooltip `TooltipProvider` (shadcn default) causing every tooltip to wait or flash; mount one shared provider at the root (`delay` 500ms, skip window 300ms) and kill animation on `[data-instant]` / `[data-state="instant-open"]`.
- **F12. Staggers stay short (POLISH)** — Cap stagger × count under ~400ms (30–50ms per item).
- **F13. Device check (always)** — Put on device list: slow DevTools Animations to 10% and inspect enter/exit midpoints for jumps; rapidly toggle drawers/menus/accordions; check first-frame smoothness on a mid-range phone.
