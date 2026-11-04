---
name: selvedge
description: "Make the color behind mobile Safari's status bar and toolbar match the page's edges, on every screen and as it scrolls. Use when a band of the wrong color sits around Safari's bars. Not for safe-area layout or screen sizes (`reflow`)."
---

# Selvedge

The selvedge is the finished edge of a cloth. On an iPhone, a web page's edges are the bands Safari paints behind its status bar and toolbar, and by default they rarely match the page.

State at the start that you are using the `selvedge` skill.

## How Safari picks the color

In the browser, as opposed to a web app added to the home screen, `theme-color` alone does not settle these bands, and it cannot give the top and bottom different colors. Safari takes each band's color from a **fixed element at that edge**: a strip with at least 5px on screen. It picks up a change of the strip's color when the screen changes, even without a scroll.

It extends a **solid color only**. An image, a canvas, a video or a gradient running across the width never continues under the bars. A full-bleed photo or 3D view can't run behind the address bar; the best available is a solid band that matches its edge.

`viewport-fit=cover` must be on the viewport meta tag, or none of this applies.

## 1. Map the edges

List every state the page can show with something reaching the top or bottom edge: routes, full-screen views, overlays and sheets that reach an edge, both color themes, and scroll positions where the edge's color changes. For each, write the solid color at the very top and the very bottom.

Done when every state has a top color and a bottom color.

## 2. Add the strips

Two empty elements, last in `body` and outside any ancestor with a `transform`, `filter` or `contain`, which would pin a fixed element to that ancestor instead of the screen:

```html
<div class="edge-top" aria-hidden="true"></div>
<div class="edge-bottom" aria-hidden="true"></div>
```

Each edge gets a solid strip with 5px on screen, plus a fade into the page across the safe-area inset, so there is no hard line and nothing covers content. Where the inset is zero, as on desktop, the fade has no height.

```css
:root {
  --edge-top: #ffffff;    /* the first state's colors from step 1 */
  --edge-bottom: #ffffff;
}
html { background: var(--edge-top); }
body { background: var(--edge-bottom); }

.edge-top::before,
.edge-top::after,
.edge-bottom::before,
.edge-bottom::after {
  content: "";
  position: fixed;
  left: 0;
  right: 0;
  z-index: 9; /* above the page's content and sheets, below dialogs that dim the whole screen */
  pointer-events: none;
}
.edge-top::after { top: -7px; height: 12px; background: var(--edge-top); }
.edge-bottom::after { bottom: -7px; height: 12px; background: var(--edge-bottom); }
.edge-top::before {
  top: 5px;
  height: env(safe-area-inset-top, 0px);
  background: linear-gradient(to bottom, var(--edge-top), transparent);
}
.edge-bottom::before {
  bottom: 5px;
  height: env(safe-area-inset-bottom, 0px);
  background: linear-gradient(to top, var(--edge-bottom), transparent);
}
```

Fit the `z-index` into the page's own stacking: a strip must sit above anything that reaches its edge, or Safari samples that element instead.

## 3. Set the colors from one place

One function sets both edges, and `theme-color` for the browsers and home-screen apps that read it:

```js
const themeColor = document.querySelector('meta[name="theme-color"]');
if (!themeColor) throw new Error("Missing theme-color meta tag");

function setEdges(top, bottom = top) {
  const root = document.documentElement.style;
  root.setProperty("--edge-top", top);
  root.setProperty("--edge-bottom", bottom);
  themeColor.content = top;
}
```

Call it at every state change from step 1, with values from the page's color tokens. Where an edge's color changes as the page scrolls, also call it on scroll (once per animation frame), on resize, and on `pageshow`, so a restored scroll position gets its colors.

Done when every state from step 1 calls `setEdges` with its two colors.

## 4. Check

- In a desktop browser at phone size, screenshot every state: the strips must not show. Device emulation does not draw Safari's bars, so this checks only that nothing looks wrong.
- On an iPhone in Safari, open each state, move between them without scrolling, and scroll where the colors change. Until this is done, report the bands as unchecked.

## Report

The edge map from step 1, the files changed, and which states were checked on an iPhone.

Technique from Josh Puckett, [Seamless Backgrounds on Mobile Safari](https://joshpuckett.me/seamless-mobile-safari).
