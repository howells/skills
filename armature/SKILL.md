---
name: armature
description: "Turn a web app that scrolls like a document into an app shell with fixed chrome and panes that scroll on their own. Not for visual polish (`chiaroscuro`)."
---

# Armature

An armature is the fixed frame inside a sculpture that everything else hangs on. A tool, dashboard or workflow needs one: a window that never scrolls, chrome that stays in view, and panes that each manage their own overflow. Without it, headers, filters, toolbars and previews scroll away and the product reads as a long document.

State at the start that you are using the `armature` skill.

This is layout and finish. Keep the palette, tokens, vocabulary and every behaviour. Add no new visual concept, routes, endpoints or features. When the work needs a new visual direction as well, do the shell first, then hand over to `chiaroscuro`.

A single document flow is still right when the task is genuinely linear - a sign-up form, an article, a one-screen setting. Choose from the task, not by habit.

## 1. Find why the window scrolls

Read the root layout and each route. The usual causes:

- the root layout wraps every route in one scroll container, so every page scrolls under the nav;
- routes set `min-h-screen` or fixed pixel heights and let the body grow;
- a centred `max-w-* mx-auto` document column holds content that wants the full frame;
- flex and grid children lack `min-h-0` or `min-w-0`, so overflow escapes to the page;
- media boxes use fixed heights or aspect ratios that ignore the viewport.

Note which routes already own their panes. They are the standard the rest are brought up to.

## 2. Write the shell contract

State it before editing, in a few numbered lines specific to the product. The default:

1. The body is a fixed `h-dvh` frame: app chrome, then a main region with `min-h-0` and clipped overflow. At desktop widths the window itself never scrolls.
2. Every route fills that frame and declares its own scroll regions, using the product's scroll-area component where it has one. A route has at most a fixed toolbar row, one primary scrolling pane, and optional side panes that are fixed or scroll independently.
3. Page titles, counts and primary actions live in the chrome or the toolbar and never scroll away. Reuse any existing mechanism for routes to place content in the chrome, and extend it rather than inventing a second one.
4. One shared layout primitive (toolbar plus panes) in the product's UI package or app layer, used on every route instead of hand-rolled flex per page.
5. Below the desktop breakpoint, panes collapse into one scrolling column with the toolbar sticky at the top. Touch targets stay at least 44 by 44 CSS pixels.

## 3. Decide each route

Give every route one line: what is fixed, what scrolls, what docks. Common shapes:

- **List or grid** - fixed toolbar and filters, scrolling results; a selection bar docks to the bottom of the results pane.
- **Record or detail** - fixed record header; a subject pane (preview, image, canvas) that sizes to the available height and does not scroll; an inspector pane that scrolls on its own. Content previously stacked below the fold moves into the inspector as sections.
- **Stage** - the canvas, 3D view or media fills the frame; controls sit in a fixed-width side pane that scrolls independently.
- **Focused form** - stays a centred form, vertically centred in the frame, scrolling only when it overflows.

Remove fixed pixel heights and square boxes that ignore the viewport; size the subject to its pane.

## 4. Finish the frame

- Pane padding and toolbar height come from a small set of spacing tokens.
- Use one divider treatment between panes: a single hairline in the border token. No cards inside cards. Nested radii are concentric.
- A scrolling pane shows a top hairline or faint shadow only once it has scrolled, so fixed rows read as chrome.
- Loading, empty and error states render inside the pane they belong to, so the frame never jumps when data arrives.
- Focus moves correctly into panes, each scroll region has an accessible name, a skip link lands on the main region, and panes keep their scroll position on back navigation.
- Run `signage` over any label moved or added, when installed.

## 5. Prove it

In a real browser, at 1440 by 900 and 1280 by 720, on every route in scope:

- `document.scrollingElement.scrollHeight` equals its `clientHeight`;
- after scrolling each primary pane to the bottom, the chrome, toolbar and fixed panes are still fully visible;
- keyboard tab order moves through the panes in reading order.

At 390 by 844, check the collapsed single column and the sticky toolbar. Check for console errors, run an accessibility scan, and screenshot each route before and after. Look at the pairs together: the user's subject should lead, with controls quiet around it.

## Report

The cause of the scrolling, the shell contract, the routes changed, the scroll-height measurement per route, and anything left out of scope.
