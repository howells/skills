# Lane E — Stability & states

Every data-driven view has four states: loading, empty, error and full. Seeded dev accounts hide the first three. Deep polish belongs to `chiaroscuro` and `signage`.

- **E1. Empty states exist and teach (BLOCKER on first-run screens, SHOULD FIX elsewhere)** — Hunt: `.map()` with no `length === 0` branch; `return null` on empty data; bare "No items" / "No data". Fix: short headline, one line of explanation, primary action to create the first item, sized like the filled view so layout doesn't jump. Filtered empty states name the filter and offer to clear it. Flag missing product copy on the human list.
- **E2. Failed requests recover cleanly (BLOCKER)** — Hunt: data hooks ignoring `error`/`isError`; `fetch` without `.ok` check; routes missing `error.tsx` / error boundary or `not-found`; bare "Something went wrong". Fix: state what failed and offer a retry or working next step.
- **E3. Waits over 400ms show an indicator (SHOULD FIX)** — Hunt: ignored `isLoading`/`isPending`, `fallback={null}`, async buttons with no pending state. Delay spinners ~150ms so fast responses don't flash.
- **E4. Loading states hold page geometry (SHOULD FIX)** — Hunt: centred spinner collapsing a list, table or card grid; `dynamic()`/`lazy()` with unsized fallback. Use skeletons matching loaded row/card height; reserve spinners for inline button actions.
- **E5. Persisted UI state is right on first paint (SHOULD FIX)** — Hunt: `useEffect` reading `localStorage` to flip theme, collapsed sidebar, tab or density after paint. Fix: blocking `<head>` script (`next-themes`) for theme, cookie read on the server for SSR layout state, or lazy `useState` + sized client placeholder.
- **E6. Dynamic numbers and labels don't jitter (SHOULD FIX)** — Hunt: counters, prices, timers, numeric columns without `tabular-nums`; buttons whose width jumps between "Save" and "Saving…".
- **E7. Constant font weight on interaction (SHOULD FIX)** — Hunt: `hover:font-medium`, `data-[state=active]:font-semibold`, `font-weight` inside `:hover`/`.active`. Signal state with colour or background instead.
- **E8. Late UI doesn't push content (SHOULD FIX)** — Hunt: conditional top banners (cookies, announcements, verify-email) mounted client-side in document flow. Overlay with `fixed` (+ safe-area padding) or decide on the server.
- **E9. Stacking from a fixed scale (SHOULD FIX)** — Hunt: `z-[9999]`, `z-index: 9999`, arbitrary high values causing toasts under modals or dropdowns under sticky headers. Move strays onto the project's scale or isolate local stacking contexts with `isolate`.
- **E10. Long user content handled (SHOULD FIX)** — Hunt: cards, table cells, breadcrumbs and sidebar items missing `min-w-0`, `truncate`, `line-clamp-*` or `wrap-anywhere`. Truncated values need a way to read the full text.
- **E11. Decorative layers stay inert (SHOULD FIX)** — Hunt: positioned glows, fades, gradients or illustrations missing `pointer-events-none` (and `select-none` on code-built illustrations).
- **E12. Optimistic updates roll back on failure (SHOULD FIX)** — Hunt: state updated before `await` with no `catch` rollback, `onMutate` without `onError`. Restore previous state and notify the user.
- **E13. Copy buttons confirm (POLISH)** — Swap icon/label to a confirmation for ~1.5s.
- **E14. Device check (always)** — Put on device list: sign up with a fresh empty account and check every screen; toggle DevTools Network → Offline and Slow 3G across core views; hard-refresh with dark mode and collapsed sidebar saved; open a modal, dropdown and toast together.
