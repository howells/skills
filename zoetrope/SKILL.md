---
name: zoetrope
description: "Build, review, suggest or cut web animation and drag gestures, and fix dropped frames. Use when motion feels slow, off, overdone or janky. Not for static polish (`chiaroscuro`), films (`rostrum`) or QA (`fieldtest`)."
---

# Zoetrope

## Pick the job, then read its file

Read the job's file before doing anything else. Build, gesture, review and find also read [references/values.md](references/values.md), which holds the curves, durations and springs. Read each file with its own command.

| The request | Job | Read |
| --- | --- | --- |
| "animate this", "add a transition", "make it feel alive" | Build | [references/build.md](references/build.md) |
| Anything dragged, swiped, flicked or thrown: sheets, carousels, sliders, reordering | Build a gesture | [references/gestures.md](references/gestures.md) |
| "review", "audit", "improve the animations", a diff with motion in it | Review | [references/review.md](references/review.md) |
| "what should animate", "where could motion help" | Find | [references/find.md](references/find.md) |
| "feels slow", "too much animation", "tone the motion down" | Remove | [references/remove.md](references/remove.md) |
| Jank, stutter, dropped frames, `will-change`, which property or driver is cheaper | Diagnose | [references/performance.md](references/performance.md) |

A review covers the current diff unless the user names a path or the whole codebase. Asked to review, audit or suggest: report only. Asked to improve or fix: apply the findings in the same run and report what changed. Remove only subtracts.

## Should it animate

Frequency decides first, then purpose. "Don't animate this" is a complete answer: say why and give the instant alternative.

- **Hundreds of times a day, or triggered from the keyboard:** no motion. The state changes instantly. Raycast has no open or close animation, and that is right.
- **Tens of times a day** (hovers, list navigation, frequent toggles): opacity or colour under 150ms, or nothing.
- **Occasional** (dialogs, sheets, notices, settings): standard motion.
- **Rare or first-time** (onboarding, a finished setup, an empty state, a first success): the only place for flourish, bounce or a longer beat.

The purpose is one of: feedback that input landed, where something came from or went, a state change made legible, bridging content that would otherwise jump, explaining how something works (onboarding and marketing only), or delight (rare moments only). "It looks nice" on something seen daily is not a purpose. Numbers someone is reading, tables they scan and forms they fill in stay still.

An expanding model or diagram that shows how parts relate is a purpose. Keep the requested transformation and the object's identity through it; don't swap it for a crossfade.

## Never

- **Never animate a keyboard action**: shortcuts, the command palette, arrow-key navigation, focus jumps.
- **Never `ease-in` on interface motion.** It spends its first frames barely moving, exactly when the user is watching. The same 200ms feels quicker as ease-out.
- **Never grow from `scale(0)`.** Start at `scale(0.94)` to `scale(0.97)` with `opacity: 0`. Nothing real appears from a point.
- **Never `transition: all`** (Tailwind `transition-all`). Name the properties.
- **Never `@keyframes` on anything triggered twice quickly** (notices, toggles, expanding rows). A transition or spring retargets from where it is; keyframes restart and jump.
- **Never animate `width`, `height`, `margin`, `padding`, `top` or `left`** where a transform does the job. The one exception is a short collapse.
- **Never scale an anchored popover, menu or tooltip from its centre.** It grows from its trigger via the library's transform-origin variable. Centred dialogs scale from the centre.
- **Never drive a child's transform from a custom property on its parent.** Every descendant recalculates style every frame.
- **Never lock input while motion plays**: a stagger, a closing sheet, an exit.
- **Never bounce what no gesture threw.** Overshoot is earned by momentum. Money, health and operations products keep `bounce: 0`.
- **Never invent a curve, duration or spring from memory.** Take it from values.md or the project's tokens. A second token set beside the project's is a defect.
- **Never ship movement without its reduced-motion variant and hover gating** in the same change.
- **Never add `will-change`** without an observed one-pixel shift or measured dropped frames.

## Taste

- **Strong curves, not the built-ins.** The built-in `ease-out` is too weak for deliberate motion; use the quint and quart tokens in values.md.
- **Interface motion stays under 300ms**, usually 150-250ms. Longer needs a large element or a stated reason.
- **Entrances pair opacity with a small scale or travel.** A pure fade looks unfinished; it is the reduced-motion variant, not the default.
- **Leave the way you came.** A sheet that rises from the bottom returns to the bottom.
- **Slow where the user decides, fast where the system answers.** A hold fills over about 2s; releasing snaps back in about 200ms.
- **Stagger groups by 30-80ms**, only on things seen occasionally.
- **Cheapest tool that works.** A CSS transition before a library; a library only for springs, gestures, shared layout and exits after unmount. Import Motion from `motion/react`, not `framer-motion`.
- **Animate an accessible primitive.** Reuse the project's dialog, menu, drawer or tooltip before writing motion, and keep its focus, keyboard and dismissal behaviour.
- **Match the product's temperament.** A trading dashboard is crisp; a consumer app can be softer. One bouncy component in a crisp app is a defect.
- **Make the call.** Give one curve and one reason, never a menu of options.

## Feel is checked by watching

When the result depends on feel (a spring's settle, a crossfade, opacity against height in a list), say so and give the check: slow it to 10-25% and step through the midpoints (the browser's animation panel, or `document.getAnimations().forEach(a => a.playbackRate = 0.1)` from a browser tool); run gestures on a real phone loaded from the machine's local IP; turn on reduced motion in the rendering settings and walk the same path. Code alone can't settle feel, so don't guess a number.
