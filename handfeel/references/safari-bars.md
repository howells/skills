# Color behind Safari's bars

Contents: how Safari picks the color, map the edges, add the strips, set the colors, check.

A web page's edges are the bands Safari paints behind its status bar and toolbar. By default they rarely match the page.

## How Safari picks the color

Safari 26 ignores `theme-color` in browser tabs. Keep the tag for installed apps and other browsers, but it does not settle these bands, and it cannot give the top and bottom different colors. Safari extends the solid color of a **fixed element at each edge**. In observed behavior the element needs at least 5px on screen; confirm that on the target Safari version. Safari picks up a change of the strip's color when the screen changes, even without a scroll.

It extends a **solid color only**. A fixed image, canvas, video or horizontal gradient never continues under the bars. A full-bleed photo or 3D view cannot run behind the address bar; the best available is a solid band that matches its edge. Safari can also show scrolling content behind its controls; that is a different case, which these strips do not change.

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

Each edge gets a solid strip with 5px on screen, plus a fade into the page across the safe-area inset, so there is no hard line. The 5px strips stay visible when the insets are zero, desktop included; only the fades follow the inset. So each strip must match the background next to it and must not cover content.

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

With two `theme-color` tags that differ by `prefers-color-scheme`, select the one script updates, or replace them with the single tag above when `setEdges` drives every state.

Done when every state from step 1 calls `setEdges` with its two colors.

## 4. Check

- In a desktop browser, narrow and wide, screenshot every state: each strip must blend with the background next to it and cover no content. Device emulation does not draw Safari's bars, so this checks only that nothing looks wrong.
- On an iPhone in Safari, or in the iOS Simulator (it draws the bars), open each state, move between them without scrolling, and scroll where the colors change. Until this is done, report the bands as unchecked.

Report the edge map from step 1, the files changed, and which states were checked on a device.
