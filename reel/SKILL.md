---
name: reel
description: "Package UI and motion work as short, looping clips for X, launch posts and changelogs, composing `browse`, `rostrum` and `zoetrope`."
---

# Reel

Short, muted, looping clips (6–25 s) that show off UI and motion work in a phone timeline (X, launch posts, changelogs, newsletters). Every rule follows from that context: small, muted and scrolled past, so the viewer must get the point in the first second.

For full narrative product films (45–100 s, storyboarded acts, sound), use `rostrum` directly.

## 1. Pick the mode

```
What is being packaged?
├── Live component or product flow (clicks, hovers, drags, real app state)
│   ├── Standard real-time flow → capture with `browse` (follow its demo-recording guide)
│   └── Motion-critical 60 fps loop (springs, transitions, hover reel) → temporary isolated route + frame-stepped Playwright capture
├── Composed explainer (before/after comparison, easing graph, 1× then 4× slow-mo)
│   └── Build in Remotion with `rostrum`, using curves and timing from `zoetrope`
└── "Put it on a page so I can record it myself"
    └── Temporary recording stage route in the app (no render)
```

For frame-stepped Playwright captures, pause the browser clock, step one frame at a time and delete `Element.prototype.animate` (unless the page requires WAAPI with no fallback) so CSS transitions, Motion springs and rAF share one deterministic clock with zero dropped frames. Never deliver raw Playwright `recordVideo` webm.

## 2. Show one look before the full render

1. Send 2–4 stills (or a one-item clip for a hover reel) and wait for a go before burning minutes on a full render.
2. When asked for look changes, re-send only the affected frames.
3. Once the look is approved, apply timing-only tweaks and render straight away without another preview round.

## 3. Frame and format

- **Explainers and comparisons:** `1080×1080` at 2× (`2160×2160`). Use `1920×1080` at 2× only for one horizontal row; 16:9 reads too small in a phone feed.
- **Live components:** leave 40 px of page background around a compact card and 60 px around a wide component. Cap at the component's real max width.
- **Resolution:** pick device scale factor so `min(width, height) × DSF ≥ 2000`, keeping the long side ≤ `4096 px` (above that breaks H.264 level 5.2 in QuickTime and X).
- **Encoding:** silent phone-safe MP4 — H.264, `yuv420p`, `+faststart`, even dimensions, `crf 14`–`18`, 60 fps for frame-stepped / Remotion renders (30 fps for `browse` CDP captures).

## 4. What's on screen

- **Strip the wrapper, keep the component.** Remove outer borders, shadows, rounded demo frames, replay buttons and `01 Spring`-style labels so the clip never reads as a screenshot of a page. Keep the component's own copy, labels and theme from current source (re-read source before every render).
- **Fill the frame.** In explainers, scale small components 2–3× (tiny spinners up to 8×) so the subject fills 60–80% of the frame. In live captures, raise DSF instead of CSS-scaling.
- **Real fonts, exact alignment.** Load the product's own faces and wait for `document.fonts.ready`. Check left edges and centres with `getBoundingClientRect` so loops never jitter by 1–2 px.
- **No clipped motion or text jitter.** Let overshooting springs overflow their container; put `will-change: transform` on buttons whose text scales on press so glyphs don't re-rasterise mid-press.
- **Comparisons:** identical scale, mirrored around centre, triggered on the same frame; easing comparisons share duration so only the curve differs.

## 5. Timing and cursor

Holds always start too long; when asked to shorten without a number, cut holds by 25–50%.

- **Lengths:** click-throughs 6–9 s; composed explainers 20–26 s.
- **Hook immediately:** first scene reads in under a second with no caption; first action starts at 0.3–0.4 s; hard cuts only between scenes.
- **Click-throughs:** glide 0.55 s, settle 0.15 s, click (button press `1 → 0.97` over 90 ms, back over 160 ms), hold 0.6 s.
- **Hover reels (per item):** rest 0.2 s, glide in 0.65 s, hold 0.65 s, glide out 0.6 s, rest 0.5 s, hard cut.
- **Comparisons (5–7 s per scene):** run twice at 1×, then once at 4× slow motion held open (keep the third run at 1× when comparing duration, or slow-mo hides the difference), with 0.6–0.9 s stillness between runs.
- **Loops:** end on frame 0's exact state.
- **Cursor:** use `browse`'s injected cursor + click pulse for live captures (or real macOS cursor sprites in composed renders). Start and end off-frame so frame 0 and the final frame show only the component; glide on a gentle curve and stop dead while hover or click plays.

## 6. Recording stages (user records themselves)

When asked for a page to screen-record manually: one item at a time centred on a clean full page with site chrome and dev badges hidden; fix the stage height to the tallest item so nothing shifts; wire `Space`/`→` and `Shift+Space`/`←` (skipping inputs) to step and remount each demo fresh; warn if editing a shared component affects the live site.

## 7. Verify and deliver

1. Probe with `ffprobe` (`codec_name,pix_fmt,width,height,r_frame_rate,duration`) to confirm `h264`, `yuv420p`, even dimensions and `+faststart`.
2. Extract an idle frame, a mid-motion frame and the final frame plus a full contact sheet (`ffmpeg -i out.mp4 -vf "fps=30/<duration>,scale=360:-1,tile=6x5" -frames:v 1 sheet.png`, or `rostrum`'s `sheet.sh`), and inspect them for alignment, clipping and cursor placement.
3. Name outputs with duration (`<name>-9s.mp4`) and keep the previous render until the new one is approved. Delete any temporary recording route when done.
4. Deliver via `stow` if installed (else the absolute local path), state resolution, fps, length, size and which frames you checked, and offer one concrete next cut with its time saving.
