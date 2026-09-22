---
name: reflow
description: "Make every view of a web app work on small laptops, tablets and phones, checked in a browser. Not for QA reports (`fieldtest`)."
---

# Reflow

A responsive pass across a whole app or a named set of views: each one should look and work well on a small laptop, a tablet and a phone. Work from the product's existing design; this pass changes how layouts adapt, not what they look like at desktop width.

State at the start that you are using the `reflow` skill.

Read [`references/responsive.md`](references/responsive.md) before editing. It holds the breakpoint, input-mode, safe-area, touch-target, table and overflow rules this pass applies.

## 1. List the views

Enumerate every route in scope, and the states that change layout: empty, loaded, long content, open dialogs, sheets and menus, selection bars, error. A view left off the list is a view nobody checked. State the list before measuring.

## 2. Measure before changing

Run the app and load each view at these sizes:

| Size | Stands for |
| --- | --- |
| 1440 × 900 | reference desktop |
| 1280 × 720 | small laptop |
| 1024 × 768 | tablet landscape, cramped laptop |
| 768 × 1024 | tablet portrait |
| 390 × 844 | phone |
| 360 × 740 | narrow phone |

At each size record, per view:

- horizontal overflow: `document.scrollingElement.scrollWidth` greater than `clientWidth`, and which element causes it;
- clipped, overlapping or truncated content that hides meaning;
- navigation and primary actions reachable without hunting;
- touch targets under 44 by 44 CSS pixels on coarse pointers;
- text inputs under 16px, which make iOS zoom;
- chrome that earned its place at desktop but crowds the small screen.

Also check a phone in landscape and one view at 200% zoom. Screenshot each view at each size.

## 3. Fix at the source

Work shell first, then navigation, then text and forms, then overflow, then individual components.

- Fix the cause of each overflow rather than hiding it on an ancestor. Add `min-w-0` where a flex or grid child must shrink; scroll wide tables inside their own wrapper.
- Multi-column layouts collapse to one column on phones, with side panels behind a disclosure, sheet or tab. Never shrink columns until they are unreadable.
- Use container queries when a shared component's layout depends on its own width rather than the viewport.
- Break where the content breaks, not at device names. Three breakpoints usually suffice.
- Strip decorative borders, nested panels and wrappers at small sizes. The phone layout should feel designed for the phone, not a desktop with pieces removed.
- Gate hover-only behaviour behind a hover media query and give touch an equivalent.
- Use `h-dvh` and `min-h-dvh`, never `h-screen`, and respect safe-area insets on fixed elements.
- Leave the desktop layout unchanged unless it is the cause.

Reuse the product's components and tokens. When a fix needs a new visual idea rather than an adaptation, note it for `chiaroscuro` instead of inventing one here.

## 4. Re-measure

Repeat step 2 on every view and size, not only those you changed; a shared-component fix moves other views too. Compare before and after screenshots side by side.

## Report

A table of views by size, each cell passing or naming what still fails, followed by the fixes made and their files. Do not claim a size was checked if it was not rendered.
