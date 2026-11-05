---
name: armature
description: "Turn a web app that scrolls like a document into an app shell with fixed chrome and panes that scroll on their own. Not for visual polish (`chiaroscuro`)."
---

# Armature

A tool, dashboard or workflow needs a fixed frame: a window that never scrolls, chrome that stays in view, and panes that manage their own overflow. Without one, headers, filters, toolbars and previews scroll away and the product reads as a long document.

This is layout only. Keep the palette, tokens, wording and every behaviour; add no visual concept, route, endpoint or feature. If it also needs a new visual direction, do the shell first, then hand over to `chiaroscuro`. A genuinely linear task (sign-up, article, a one-screen setting) stays a document.

## 1. Find why the window scrolls

Usual causes:

- the root layout wraps every route in one scroll container, so every page scrolls under the nav;
- routes set `min-h-screen` or fixed pixel heights and let the body grow;
- a centred `max-w-* mx-auto` column holds content that wants the whole frame;
- flex and grid children lack `min-h-0` or `min-w-0`, so overflow escapes to the page;
- media boxes have fixed heights or aspect ratios that ignore the viewport.

Routes that already own their panes are the standard the rest are brought up to.

## 2. The shell

Adapt this default to the product:

1. The body is a fixed `h-dvh` frame: app chrome, then a main region with `min-h-0` and clipped overflow. At desktop widths the window never scrolls.
2. Every route fills the frame and declares its own scroll regions, with the product's scroll-area component if it has one. A route has at most a fixed toolbar row, one primary scrolling pane, and side panes that are fixed or scroll on their own.
3. Titles, counts and primary actions live in the chrome or toolbar and never scroll away. If routes can already place content in the chrome, extend that mechanism rather than adding a second.
4. One shared toolbar-plus-panes primitive in the product's UI package or app layer, used on every route instead of hand-rolled flex.
5. Below the desktop breakpoint, panes collapse into one scrolling column with a sticky toolbar.

## 3. Each route

Decide what is fixed, what scrolls and what docks. Common shapes:

- **List or grid**: fixed toolbar and filters, scrolling results; a selection bar docks to the bottom of the results pane.
- **Record**: fixed header; the subject (preview, image, canvas) sizes to the available height and does not scroll; an inspector pane scrolls on its own, taking the content that used to stack below the fold as sections.
- **Stage**: the canvas, 3D view or media fills the frame; controls sit in a fixed-width side pane that scrolls independently.
- **Focused form**: stays a centred form, vertically centred, scrolling only when it overflows.

Size the subject to its pane; remove fixed pixel heights and square boxes.

## 4. Finish

- Pane padding and toolbar height come from a few spacing tokens.
- One divider between panes: a single hairline in the border token. No cards inside cards; nested radii are concentric.
- A scrolling pane shows a top hairline or faint shadow only once it has scrolled, so fixed rows read as chrome.
- Loading, empty and error states render inside their pane, so the frame never jumps when data arrives.
- Each scroll region has an accessible name, tab order follows the panes in reading order, a skip link lands on the main region, and panes keep their scroll position on back navigation.

## 5. Check in a browser

At 1440 × 900 and 1280 × 720, on every route in scope, `document.scrollingElement.scrollHeight` equals `clientHeight`, and with each primary pane scrolled to the bottom the chrome, toolbar and fixed panes are still fully visible. At 390 × 844, check the single column and sticky toolbar. Look at the result: the user's subject should lead, with controls quiet around it.

Report the cause of the scrolling, the shell as adapted, the routes changed, and anything left out of scope.
