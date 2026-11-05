# Vocabulary

Turn a loose description of a motion effect into its name. Read for the sensation described ("springy", "draws itself in"), lead with the term and a one-line definition, then give one or two close alternates with how they differ. If nothing fits, name the nearest term and say it's an approximation. A naming question wants a name, not an essay.

```
**Origin-aware animation**: the element grows out of its trigger, like a popover from the button that opened it, instead of from its own centre.

Close alternates:
- **Transform origin**: the anchor point itself, if they're asking what to set.
```

## Entrances and exits

- **Fade in / out**: appears or disappears by opacity.
- **Slide in**: enters from off-screen along one edge.
- **Scale in**: grows from slightly smaller to full size, usually with a fade.
- **Pop in**: scales in with a slight overshoot. Contrast **bounce**, a spring that overshoots and settles after any move.
- **Reveal**: content uncovered gradually by a clip-path or mask.
- **Enter / exit**: the animation played when an element is added to or removed from the page.

## Sequencing and timing

- **Keyframes**: defined points (0%, 50%, 100%) the browser fills between.
- **Interpolation / tween**: generating the in-between frames.
- **Stagger**: items animate one after another with a small delay, a cascade.
- **Orchestration**: timing several animations to read as one motion.
- **Fill mode**: whether an element holds its first or last frame outside the animation's run.
- **Stepped animation**: discrete jumps, like a countdown.

## Transforms

- **Translate, scale, rotate, skew**: move, resize, spin, shear.
- **3D tilt / flip**: `rotateX` or `rotateY` for depth; **perspective** sets how strong it looks.
- **Transform origin**: the point a scale or rotation grows or spins from.
- **Origin-aware animation**: the element grows out of its trigger rather than its own centre.

## Between states

- **Crossfade**: one element fades out as another fades in, in the same spot.
- **Continuity transition**: before and after visibly connected, so the user stays oriented.
- **Morph**: one shape smoothly becomes another (the Dynamic Island).
- **Shared element transition**: an element travels and transforms into its counterpart elsewhere, like a thumbnail into a card. Contrast **layout animation**: one element animating to its own new size or position instead of snapping.
- **Accordion / collapse**: a section expands and collapses its height.
- **Direction-aware transition**: forward slides one way, back slides the other.
- **View transition**: the browser morphs between two states or pages, connecting shared elements. **Page transition** is any animation on route change.

## Scroll

- **Scroll reveal**: elements fade or slide in as they enter the viewport.
- **Scroll-driven animation**: progress tied directly to scroll position.
- **Parallax**: layers move at different speeds while scrolling.

## Feedback and gesture

- **Press / tap feedback**: a slight scale-down on press.
- **Hold to confirm**: a fill that completes while the button is held.
- **Drag to reorder**: dragging a list item while the others shift to make room.
- **Swipe to dismiss**: dragging something off-screen to close it.
- **Rubber-banding**: rising resistance and snap-back past a boundary, the iOS overscroll.
- **Momentum / velocity**: speed carried from a flick or into an interrupted spring.
- **Interruptible animation**: redirected mid-flight instead of finishing first.
- **Shake / wiggle**: a quick side-to-side jitter for rejected input.
- **Ripple**: a circle expanding from the tap point.

## Easing and springs

- **Ease-out**: fast then slow; the default for anything responding to the user. **Ease-in**: slow then fast; avoided in interfaces. **Ease-in-out**: slow, fast, slow; for movement between two visible points. **Linear**: constant; spinners, marquees, progress.
- **Asymmetric easing**: accelerates and decelerates at different rates.
- **Spring**: motion driven by stiffness, damping and mass rather than a set duration. **Damping** sets how quickly it settles; **stiffness** how hard it pulls.
- **Perceptual duration**: how long a spring looks finished, though it keeps micro-settling.

## Ambient and loops

- **Marquee**: content scrolling continuously in a loop.
- **Alternate / yoyo**: a loop that plays forward then reverses.
- **Pulse**: a repeating gentle scale or opacity change. **Float**: a slow up-and-down drift. **Orbit**: circling another element. **Idle animation**: motion while nothing is happening.

## Effects

- **Clip-path**: clipping to a hard-edged shape, for reveals and comparison sliders. Contrast **mask**: the same idea with soft, fadeable edges.
- **Before / after slider**: a draggable divider wiping between two overlaid images.
- **Line drawing**: an SVG path that draws itself in.
- **Text morph**: text changing character by character.
- **Number ticker**: digits rolling or counting to a value; needs **tabular numbers** so digits don't shift.
- **Skeleton / shimmer**: a placeholder with a moving sheen while content loads.
- **Typewriter**: text appearing one character at a time.

## Performance and principles

- **Jank / dropped frame**: visible stutter when a frame misses its deadline. **Compositing**: moving or fading a layer without redoing layout or paint. **Layout thrashing**: animating properties that force layout every frame.
- **Anticipation**: a small wind-up before a move. **Follow-through**: parts settling after the main motion stops. **Squash and stretch**: deforming to show weight and speed.
- **Spatial consistency**: an element keeps its identity and position across states.
- **Perceived performance**: the right motion makes an interface feel faster than it is.
