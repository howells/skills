---
name: reflow
description: "Make every view of a web app work on small laptops, tablets and phones, checked in a browser. Not for phone-browser behavior (`handfeel`) or QA reports (`fieldtest`)."
---

# Reflow

A responsive pass across a whole app or a named set of views. It changes how layouts adapt, not what they look like at desktop width: leave the desktop layout alone unless it is the cause. When a fix needs a new visual idea rather than an adaptation, note it for `chiaroscuro` instead of inventing one.

## Rules

- **Fix the cause of overflow, never hide it on an ancestor.** Usually a flex or grid child missing `min-w-0`, or a wide table that needs its own scroll wrapper.
- **Phones get one column.** Side panels go behind a disclosure, sheet or tab; never shrink columns until they are unreadable.
- **Strip chrome as the screen shrinks.** Decorative borders, nested panels and wrappers that earned their place at desktop go. The phone layout should feel designed for the phone, not a desktop with pieces removed.
- **Break where the content breaks**, not at device names. Three breakpoints usually suffice. Container queries when a shared component depends on its own width.
- **Touch gets an equivalent for anything hover-only**, and targets of at least 44 by 44 CSS pixels.
- **`h-dvh` and `min-h-dvh`, never `h-screen`.** Fixed elements respect safe-area insets.
- **Text inputs at 16px or more on phones**, or iOS zooms the page on focus.
- Reuse the product's components and tokens.

Read [the responsive reference](references/responsive.md) when writing a fix; it has the Tailwind patterns for tables, touch targets, disclosures, safe areas and grids.

## Steps

1. **List the views**: every route in scope, plus the states that change layout (empty, long content, open dialogs, sheets and menus, selection bars, errors).
2. **Load each at these sizes** in a real browser:

   | Size | Stands for |
   | --- | --- |
   | 1440 × 900 | reference desktop |
   | 1280 × 720 | small laptop |
   | 1024 × 768 | tablet landscape, cramped laptop |
   | 768 × 1024 | tablet portrait |
   | 390 × 844 | phone |
   | 360 × 740 | narrow phone |

   Plus a phone in landscape and one view at 200% zoom. Note horizontal overflow (`document.scrollingElement.scrollWidth > clientWidth`, and the element causing it), content clipped or truncated so it loses meaning, primary actions you have to hunt for, small touch targets, small inputs, and chrome crowding the screen.
3. **Fix in this order**: shell, navigation, text and forms, overflow, then individual components.
4. **Reload every view at every size**, not only the ones you touched. A shared-component fix moves other views.

## Report

A table of views by size, each cell passing or naming what still fails, then the fixes and their files.
