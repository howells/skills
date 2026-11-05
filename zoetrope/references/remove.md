# Remove

Put every existing animation on trial and delete or reduce the ones that can't defend themselves. "It's already there" and "it looks nice" are not defences. Deleting everything is also wrong: motion that bridges a jump (a notice that would otherwise teleport in, a panel that shows where it came from) keeps the interface from becoming disorienting.

Only subtract. Every edit deletes an animation, reduces it, or removes code it orphaned. An animation that should stay but is badly built (wrong curve, wrong origin) is listed for a review, not retuned here. Keep anything a comment or design document explains.

## Verdicts

| The animation | Verdict |
| --- | --- |
| Triggered from the keyboard | Delete |
| Seen hundreds of times a day: core navigation, tab switches, list rows, in-app route changes | Delete |
| On data being read: charts, tables, numbers, dashboards | Delete, unless it shows a real change in value on a user action. Re-animating on every mount or refresh is decoration |
| No nameable purpose, and not a rare first-time moment | Delete |
| Has a purpose but is seen tens of times a day | Reduce |
| Has a purpose but runs over 300ms, or slides or scales where a fade would carry the same meaning | Reduce |
| Everything else | Keep |

Marketing pages get more latitude: explanation and one hero entrance can stay. A scroll reveal on every section still fails; it holds content back from people who scroll fast.

## Reducing

Reduce means a smaller version of the same motion, never a different one. If the reduced version stops carrying its purpose, delete it.

| Today | Reduced to |
| --- | --- |
| Hover with scale, lift or shadow growth | Colour or opacity only, 150ms or less, `ease` |
| Slide or scale entrance on a frequent element | Opacity only, 150ms, ease-out |
| Interface motion over 300ms | 200-250ms, same curve |
| Stagger over 80ms per item or 300ms in total | 30ms per item, or fade the group as one |
| An endless pulse, shimmer or glow on a persistent element | Run once, or keep the static end state |

## Where to hunt

- Command palettes, menus and dialogs opened by a shortcut with an enter or exit.
- Tab switches, segmented controls and sidebar navigation that slide or crossfade; route transitions inside the app.
- Hover transforms on rows the cursor sweeps across; hover scale or lift on cards that aren't the primary action.
- Fade-in-on-scroll everywhere: `whileInView`, observer reveal classes, AOS, `animate-fade-in` utilities.
- Infinite loops: pulsing badges, gradient orbs, glowing borders, spinning icons that aren't loading.
- Staggered entrances on lists loaded many times a day; table rows animating in on load.
- Charts redrawing from zero on mount; numbers counting up on page load rather than on a change.
- Spinners and skeleton shimmer on work that resolves in under 300ms; the flash reads as a glitch.

Searches: `transition`, `animation`, `@keyframes`, `motion.`, `animate={`, `whileInView`, `whileHover`, `AnimatePresence`, `layout`, `stagger`, `infinite`, `animate-`, `IntersectionObserver`.

## Before deleting, check what depends on it

- **Hidden start states.** `initial={{ opacity: 0 }}`, keyframes with `forwards` fill from `opacity: 0`, a reveal class that waits for an observer. Delete the start state with the animation or the element stays invisible.
- **Code waiting for the animation.** `onAnimationEnd`, `transitionend`, `onExitComplete`, and timeouts sized to a duration. Remove the wait too, or the UI keeps pausing for motion that no longer exists.
- **Exits holding unmount.** Without the exit, `AnimatePresence` unmounts immediately; move whatever ran in `onExitComplete` to where the component closes.
- **Layout animation hiding a jump.** Removing a `layout` prop or FLIP can expose a layout shift. If it does, keep the animation and report the shift.
- **Focus timed after motion.** Move it immediately once the motion is gone.
- **Tests and selectors** that wait for animation classes or durations.

## Clean up

Delete what the removals orphaned: unreferenced `@keyframes` and animation utilities, `motion.div` that no longer has motion props (back to `div`), empty `AnimatePresence` wrappers and unused variants, motion imports in files that no longer animate, token or Tailwind config entries with no references. Search for every removed name to confirm nothing still uses it. If the motion library is no longer imported anywhere, propose removing the dependency; don't uninstall it unasked.

## Output

**Removed and reduced**, ordered by how often the user hits it:

| # | Where | Was | Verdict | Why |
| --- | --- | --- | --- | --- |
| 1 | `CommandMenu.tsx:24` | 200ms scale and fade on open | Deleted | Keyboard-triggered |
| 2 | `ProjectCard.tsx:31` | `hover:scale-105` with shadow growth | Reduced to border colour, 150ms `ease` | Hovered tens of times a day |

**Kept**: two to five animations you considered and kept, each with the purpose that saved it. Then the ones that stay but are badly built, for a review.

**Cleanup and verdict**: orphaned code removed, any dependency to drop, and a short paragraph on how over-animated it was and what to feel-check on a real device.
