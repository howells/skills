# Find

Restraint is the point: most candidates should fail. At most five to seven suggestions for a whole app, fewer for one view, ordered by leverage. Survey the stack, the existing motion tokens and the product's temperament first, so suggestions extend what's there. A crisp dashboard earns fewer and subtler suggestions than a consumer app.

## Where to look

- **Pressables with no press state.** `:active { transform: scale(0.97) }` over 120ms ease-out.
- **Destructive actions confirmed by one click** where a hold would prevent slips. A `clip-path` fill over 2s linear, 200ms snap-back.
- **Content that teleports**: conditional renders (`{isOpen && …}`), `display: none` toggles, expanding sections, list inserts on a list that isn't high-frequency. Entrances from `scale(0.96)` and `opacity: 0` with `@starting-style`; transitions, not keyframes, so repeat triggers retarget.
- **Panels with no link to their trigger**, or that leave a different way than they came. Scale from the trigger's origin; exit along the entry path.
- **Groups that pop in all at once** on a page seen occasionally. A 30-80ms stagger.
- **Draggables that snap with no physics.** A spring with release velocity, a flick-to-dismiss threshold, rubber-banding at edges.
- **Rare moments rendered flat**: a finished setup, an empty state, a first success. The only place for delight.

Every suggestion carries exact values from `values.md` (curve, duration or spring, properties), its reduced-motion variant, and hover gating when it involves hover.

## Output

| # | Where | Now | Purpose | Frequency | Motion, with exact values |
| --- | --- | --- | --- | --- | --- |

Then **Rejected**: two to five places you considered and turned down, each with the reason (keyboard-triggered, seen constantly, data being read, no purpose). Then one line on how much motion this interface actually needs and the one suggestion worth doing first. If nothing survives, say so; that is a good result. "Build row N" hands a row to the build job.
