# Review

A diff reviews the changed motion and anything it touches. "Audit" or "improve the animations" with no diff means the whole codebase.

## Survey a codebase first

Find the stack and motion libraries, where motion lives (tokens, theme config, keyframes, `transition`, `animate`, gesture handlers), the existing conventions, and the product's temperament. Then map which animated things are hit constantly and which rarely; that map sets severity. For a large repo, split the survey by app area across read-only helpers and give each the conventions and the frequency map.

Searches: `transition`, `animation`, `@keyframes`, `motion.`, `animate=`, `useSpring`, `whileInView`, `AnimatePresence`, `ease-in`, `transition: all`, `transition-all`, `scale(0)`, `prefers-reduced-motion`, `motion-reduce`, `transform-origin`, `setProperty('--`.

## What to look for

- **Purpose and frequency.** Motion on keyboard actions or things hit constantly; decoration on data being read.
- **Easing and duration.** `ease-in`, weak built-in curves on deliberate motion, interface motion over 300ms, every tooltip in a toolbar animating instead of only the first.
- **Origin and physicality.** `scale(0)`, pure-fade entrances, anchored popovers scaling from the centre, pressables with no press state.
- **Interruption.** Keyframes on rapidly triggered UI, fixed-duration tweens on drags, drags with no velocity-based dismissal, hard stops at boundaries.
- **Cost.** Layout properties, `transition: all`, parent custom properties driving children, `requestAnimationFrame` loops doing what CSS could.
- **Accessibility.** Movement with no reduced-motion variant, a reduced-motion variant that removes all feedback, ungated hover.
- **Cohesion.** Five hand-typed near-identical curves to merge into tokens, one bouncy component in a crisp app, crossfades that double-expose, groups arriving all at once.

## Confirm before reporting

A search hit is a lead. Re-read each at its source and drop anything deliberate, exempt or already right: a centred dialog scaling from the centre is correct; a long reveal on a marketing page can be fine; a documented trade-off is respected, not re-argued.

## Fix in this order of preference

Delete high-frequency, purposeless or keyboard-triggered motion; otherwise reduce it, fix the curve, fix the origin, make it interruptible, move it to cheaper properties, make the timing asymmetric, then polish. Every repair includes reduced motion. Keep purposeful motion the user asked for.

## Output

Highest severity first. Omit empty groups.

| Where | Now | Change | Why |
| --- | --- | --- | --- |
| `file:line` | the current code | the exact replacement, values included | one line |

- **High**: feels broken. Motion on keyboard or constant actions, `ease-in`, growing from `scale(0)`, dropped frames.
- **Medium**: noticeably off. Wrong origin, keyframes where a transition should retarget, missing reduced motion, symmetric timing on a hold.
- **Low**: polish. Stagger, a double-exposing crossfade, curves to merge into tokens.

For a codebase audit, add two to four missed opportunities after the table: places that jump or appear with no bridge, kept separate because they add rather than correct.

Close with **Ship** (no high findings, nothing that should obviously be deleted, reduced motion handled) or **Hold** (anything high), and one line on why. "The motion here is already right" is a valid result.

## After the report

"Apply the fixes" authorises edits within the reviewed scope. "Create tracker items" means one item per group of findings you would fix in one sitting, written for an agent with no context and no taste: the files and current code excerpts, the exact target values inline (curve, duration, spring), the project convention to follow, what not to touch, a done-when line and the feel check. Findings never go into a file in the repo.
