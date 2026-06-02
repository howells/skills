# Interface: Animation

## Core Rules

- MUST: Honor `prefers-reduced-motion`
- MUST: Use `transform` and `opacity` for spatial/content motion. Color, background, border, and shadow transitions are acceptable for simple state feedback when they do not cause layout or paint-heavy effects.
- MUST: Every animation answers "why does this exist?" — purposeful animation orients, gives feedback, or shows relationships. It does not decorate.
- MUST: Correct `transform-origin` for element's entry point (origin-aware animation — a popover grows from the button that opened it, not from its own center)
- SHOULD: CSS for simple transitions; `motion/react` when JS control needed
- NEVER: Animate for "delight" without function
- SHOULD: The more often a user sees an animation, the shorter and subtler it should be (frequency of use)

## Motion Vocabulary

Use these terms precisely when specifying motion in design specs. Shared language prevents ambiguity between design and implementation.

### Entrances and Exits

| Term | Meaning |
|------|---------|
| Fade in / out | Appear or disappear by changing opacity |
| Slide in | Enter by sliding from off-screen (left, right, top, bottom) |
| Scale in | Grow from smaller to full size, often paired with fade |
| Pop in | Appear with slight overshoot, like bouncing into place |
| Reveal | Uncover gradually via animated clip-path or mask |
| Enter / exit | The animation an element plays when added to or removed from the screen |

### Sequencing and Timing

| Term | Meaning |
|------|---------|
| Stagger | Animate items one after another with a small delay, creating a cascade |
| Orchestration | Timing multiple animations so they feel like one coordinated motion |
| Stepped animation | Motion divided into discrete steps, like a countdown timer |
| Fill mode | Whether an element keeps its first or last frame's styles before/after the animation (e.g. `forwards`) |

### Movement and Transforms

| Term | Meaning |
|------|---------|
| Translate | Move along X or Y axis |
| Scale | Make bigger or smaller |
| Rotate | Spin around a point |
| Skew | Slant along X or Y axis, shearing out of rectangular shape |
| 3D tilt / flip | Rotate in 3D space (`rotateX` / `rotateY`) to add depth |
| Perspective | Strength of 3D effect — lower value exaggerates depth |
| Transform origin | Anchor point a scale or rotation grows or spins from |
| Origin-aware animation | Element animates out of its trigger (popover from button) rather than from its own center |

### State Transitions

| Term | Meaning |
|------|---------|
| Crossfade | One element fades out as another fades in, in the same spot |
| Continuity transition | Change that keeps the user oriented by visually connecting before and after |
| Morph | One shape smoothly turns into another |
| Shared element transition | Element travels and transforms from one position to another (thumbnail expanding into card) |
| Layout animation | Size or position change animates to new spot instead of snapping |
| Accordion / collapse | Section smoothly expands and collapses height to show or hide content |
| Direction-aware transition | Content slides one way going forward, opposite going back — navigation has a sense of direction |

### Scroll

| Term | Meaning |
|------|---------|
| Scroll-driven animation | Progress tied directly to scroll position |
| View transition | Browser morphs between two states or pages, connecting shared elements |
| Page transition | Animation when navigating from one route to another |

- NEVER: Scroll-triggered reveal animations (fade-up on scroll)
- NEVER: Parallax or scroll hijacking

### Feedback and Interaction

| Term | Meaning |
|------|---------|
| Press / tap feedback | Subtle scale-down when clicked, so it feels physical |
| Hold to confirm | Progress effect that fills while user holds a button |
| Drag to reorder | Dragging items in a list to rearrange, while others shift to make room |
| Swipe to dismiss | Dragging off-screen to close (drawer, toast) |
| Rubber-banding | Resistance and snap-back when dragging past a boundary |
| Shake / wiggle | Quick side-to-side jitter signaling error or rejected input |

### Easing

| Term | Meaning |
|------|---------|
| Ease-out | Starts fast, ends slow — the default for most UI motion |
| Ease-in | Starts slow, ends fast — usually avoided, can feel sluggish |
| Ease-in-out | Slow, fast, slow — for elements already on screen moving A to B |
| Linear | Constant speed — reserve for spinners or marquees, avoid for UI |
| Asymmetric easing | Accelerates and decelerates at different rates — feels more alive than symmetric |

### Springs

| Term | Meaning |
|------|---------|
| Spring | Motion driven by physics (tension, mass, damping) rather than fixed duration |
| Stiffness / tension | How strongly the spring pulls toward its target — higher feels snappier |
| Damping | How quickly a spring settles — lower means more bounce |
| Mass | How heavy the element feels — more mass is slower and more sluggish |
| Perceptual duration | How long a spring feels finished, even while micro-settling underneath |
| Velocity | Speed and direction — a spring carries it into the next animation when interrupted |
| Interruptible animation | Can be smoothly redirected mid-flight instead of finishing first |

### Looping and Ambient

| Term | Meaning |
|------|---------|
| Marquee | Content scrolling continuously in a loop |
| Alternate (yoyo) | Loop that plays forward then reverses, instead of jumping to start |
| Pulse | Gentle repeating scale or opacity change to draw attention |
| Idle animation | Subtle motion while waiting to be interacted with |

### Polish and Effects

| Term | Meaning |
|------|---------|
| Clip-path reveal | Clipping an element to a shape for reveals and masks |
| Mask | Hiding or revealing parts with a shape or gradient — soft, fadeable edges |
| Line drawing | SVG path that draws itself in, like a pen tracing it |
| Text morph | Text animating character by character when it changes |
| Skeleton / shimmer | Placeholder with moving sheen shown while content loads |
| Number ticker | Digits rolling or counting up to a value |
| Tabular numbers | Fixed-width digits so numbers don't shift as they change — essential for tickers, timers, counters |

### Performance Concepts

| Term | Meaning |
|------|---------|
| Jank | Visible stutter when the browser drops frames |
| Compositing | Letting the GPU move or fade an element on its own layer without layout or paint |
| `will-change` | CSS hint that an element is about to animate, so the browser promotes it to its own layer |
| Layout thrashing | Animating width, height, top, left forces layout recalculation every frame |
| Hardware acceleration | Animating `transform` and `opacity` lets the GPU keep motion smooth |

### Principles

| Principle | Meaning |
|-----------|---------|
| Purposeful animation | Motion serves a function — orient, feedback, relationships — not decoration |
| Anticipation | Small wind-up in opposite direction before a move, hinting at what's coming |
| Follow-through | Parts keep moving and settle slightly after main motion stops, adding weight |
| Squash and stretch | Deforming as it moves to convey weight, speed, flexibility |
| Perceived performance | The right animation makes an interface feel faster, even when it isn't |
| Frequency of use | The more often seen, the shorter and subtler it should be |
| Spatial consistency | Element keeps its identity and position across states — users never lose track |
| Reduced motion | Respect `prefers-reduced-motion` by toning down or removing motion |

## Easing Decision

| Context | Easing | Curve |
|---------|--------|-------|
| Entering/appearing | `ease-out` | `cubic-bezier(0.23, 1, 0.32, 1)` |
| Exiting/disappearing | `ease-in` | `cubic-bezier(0.4, 0, 1, 1)` |
| Moving while visible | `ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` |
| Color/opacity only | `linear` | — |
| Interactive/gesture | `spring` | See presets below |

- NEVER: Use `ease-in` for enter animations

### Easing Variables

```css
--ease-out-quad: cubic-bezier(0.25, 0.46, 0.45, 0.94);
--ease-out-cubic: cubic-bezier(0.215, 0.61, 0.355, 1);
--ease-out-quart: cubic-bezier(0.165, 0.84, 0.44, 1);
--ease-out-quint: cubic-bezier(0.23, 1, 0.32, 1);
--ease-out-expo: cubic-bezier(0.19, 1, 0.22, 1);

--ease-in-out-quad: cubic-bezier(0.455, 0.03, 0.515, 0.955);
--ease-in-out-cubic: cubic-bezier(0.645, 0.045, 0.355, 1);
--ease-in-out-quart: cubic-bezier(0.77, 0, 0.175, 1);
```

Order: quad → cubic → quart → quint → expo (subtle → dramatic)

## Duration

| Element | Duration |
|---------|----------|
| Micro (hover, click) | 100–150ms |
| Small (tooltip, dropdown) | 150–200ms |
| Medium (modal, panel) | 200–300ms |
| Large (page transition) | 300–400ms |

- SHOULD: Default to 200ms
- MUST: Skip animation if user triggers 100+ times/day
- MUST: Paired elements share identical duration and easing

## Spring Presets

```jsx
// Snappy (buttons, toggles)
{ type: "spring", stiffness: 400, damping: 25 }

// Gentle (subtle movement)
{ type: "spring", stiffness: 200, damping: 20 }

// Bouncy (use sparingly)
{ type: "spring", stiffness: 300, damping: 10 }
```

Use springs for: drag/drop, gestures, interruptible animations. Springs carry velocity across interruptions — a flicked element keeps its speed when redirected.
Use tweens for: fixed timing, opacity-only, <100ms.

## Scale Values

| Element | Scale |
|---------|-------|
| Modal/dialog | `0.95`–`0.98` |
| Button press | `0.97`–`0.98` |
| Card/list item | `0.98`–`0.99` |
| Tooltip | `0.95` |

- NEVER: Scale from `0` — minimum `0.95`

## Layout Animations

- MUST: Use `layout="position"` instead of `layout` on elements whose aspect ratio changes during animation (prevents text/image distortion).

## Patterns

### Modal Entry (scale in + fade)
```jsx
initial={{ opacity: 0, y: 20, scale: 0.98 }}
animate={{ opacity: 1, y: 0, scale: 1 }}
exit={{ opacity: 0, y: 10, scale: 0.98 }}
```

### Dropdown (origin-aware scale in)
```jsx
initial={{ opacity: 0, scale: 0.95, y: -8 }}
animate={{ opacity: 1, scale: 1, y: 0 }}
transition={{ duration: 0.15, ease: "easeOut" }}
style={{ transformOrigin: "top" }}
```

### Staggered List
```jsx
const container = { visible: { transition: { staggerChildren: 0.03 } } };
const item = { hidden: { opacity: 0, y: 8 }, visible: { opacity: 1, y: 0 } };
```

### AnimatePresence

| Mode | Use |
|------|-----|
| `sync` | Default, simultaneous enter/exit |
| `wait` | Exit completes before enter |
| `popLayout` | Exiting element pops from layout |

Use `popLayout` for lists with exit animations.

### Swipe to Dismiss
```jsx
onDragEnd={(_, info) => {
  if (info.velocity.x > 500 || Math.abs(info.offset.x) > 100) dismiss();
}}
```

## Theme Switching

- MUST: Disable transitions during theme change

```js
function setTheme(theme) {
  document.documentElement.classList.add('no-transitions');
  document.documentElement.setAttribute('data-theme', theme);
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      document.documentElement.classList.remove('no-transitions');
    });
  });
}
```

```css
.no-transitions, .no-transitions * { transition: none !important; }
```

## Reduced Motion

- MUST: Provide reduced-motion fallback for every animation
- SHOULD: Use opacity fade as fallback

```jsx
const shouldReduce = useReducedMotion();
<motion.div animate={{ opacity: 1, y: shouldReduce ? 0 : 20 }} />
```

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Buttons feel dead | Press feedback: `active:scale-[0.97]` |
| Element appears from nowhere | Start at `scale(0.95)`, not `0` — use scale in |
| Jittery animation (jank) | Add `will-change: transform` to promote to compositor layer |
| Hover causes flicker | Animate child, not parent |
| Popover scales from wrong point | Origin-aware animation: set `transform-origin` to trigger location |
| Sequential tooltips feel slow | Skip delay after first (warm state) |
| Touch targets too small | 44px minimum via pseudo-element |
| Something still feels off | Subtle blur (<20px) can mask issues |
| Hover fires on mobile | `@media (hover: hover) and (pointer: fine)` |
| Numbers shift during animation | Use tabular numbers (`tabular-nums`) for tickers and counters |
| Spring animation never settles | Increase damping — perceptual duration matters more than mathematical convergence |

## Performance

- MUST: Use `transform` and `opacity` for motion. Keep color/background/border/shadow transitions short and limited to state feedback.
- MUST: Pause looping animations when off-screen
- NEVER: Animate `width`, `height`, `top`, `left`, `margin`, `padding`

| Don't | Do |
|-------|-----|
| `width` | `scaleX` |
| `height` | `scaleY` |
| `top`/`left` | `translate` |

### Performance Tiers

| Tier | Techniques | Thread |
|------|------------|--------|
| **S** | `transform`, `opacity`, `filter`, `clip-path` via CSS/WAAPI/Motion | Compositor |
| **A** | Same values via rAF/GSAP on layered elements | Main |
| **B** | FLIP/layout animations (setup + S/A) | Main → Compositor |
| **C** | `background-color`, CSS variables, SVG `d` | Paint |
| **D** | `width`, `height`, `margin`, layout | Full pipeline |
| **F** | Style/layout thrashing | Avoid completely |

- MUST: Prefer `motion/react` (uses WAAPI) — S-Tier, smooth under main thread load
- SHOULD: Avoid rAF-based libraries (GSAP, anime.js) — A-Tier, vulnerable to jank

### CSS Variables Warning

- NEVER: Animate CSS variables for `transform`/`opacity` — always triggers paint (C-Tier)
- NEVER: Animate global CSS variables — inheritance triggers style recalc on ALL descendants (F-Tier)

```css
/* F-Tier: Inheritance bomb */
html { --progress: 0; }
.box { transform: translateY(calc(var(--progress) * 100px)); }

/* Safe: Disable inheritance */
@property --progress {
  syntax: "<number>";
  inherits: false;
  initial-value: 0;
}
```

If you must use CSS variables, use `@property { inherits: false }` to prevent cascade.
