# Gestures

For anything a finger or pointer moves directly: drags, swipes, sheets, carousels, sliders, reorderable lists. A gesture feels physical when four things hold: it responds on contact, the object stays under the finger, the motion can be caught and reversed at any moment, and the release carries the finger's speed into the settle.

## Respond on contact

- Show feedback on pointer-down. Waiting for `click` or pointer-up makes the control feel dead.
- Commit on pointer-up, and let moving off the target cancel it; moving back on re-arms it. Native `:active` plus `click` already behave this way; custom pointer handlers must reproduce it.
- Remove waits on the input path: debounces, artificial delays, a transition that must finish before input is accepted. Only pay the double-tap delay where double-tap exists.
- Feedback is continuous. A slider, drawer or drag updates every frame of the gesture, not once at the end.

## Track one to one

- Call `setPointerCapture(event.pointerId)` on pointer-down so tracking continues when the pointer leaves the element.
- Keep the offset from where the user grabbed. Snapping the element's centre to the pointer breaks the illusion on the first frame.
- Require about 10px of movement before committing to a direction; below that, it's a tap.
- Watch every plausible gesture from the first move (horizontal swipe, vertical scroll, long press) and drop the others once intent is clear. Recognisers that only report a finished swipe throw away the continuous input feedback needs.
- Ignore extra touch points once a drag has started, or a second finger makes the element jump.
- Keep a short history of recent positions with timestamps; velocity at release comes from it, not from the last two events.

## Interrupt from where it is

- Never lock input during a transition. A sheet that's closing can be grabbed and follows the finger.
- Start every new animation from the value currently on screen, never from the logical target. Starting from the target is the visible jump when an animation is interrupted.
- Springs retarget from the current value and velocity by default, which is why they're the tool here. CSS transitions retarget but drop velocity; keyframes restart.
- When a gesture reverses, carry velocity through the change. Replacing one animation with another at the turn stops dead and restarts.
- Animate x and y as separate springs. One spring on a 2D distance falls out of step when the two axes move at different speeds.

## Hand the finger's speed to the settle

At release, pass the pointer's velocity into the spring so there's no seam between dragging and animating. Motion takes it directly:

```js
animate(sheet, { y: target }, { type: "spring", visualDuration: 0.35, bounce: 0.15, velocity: releaseVelocityPxPerSecond });
```

Some spring APIs want velocity relative to the distance left to travel: `velocity / (target - current)`.

## Throw to where it's heading

Choose the snap point from where the motion would come to rest, not from where the finger let go. That's what makes a small flick move a sheet a long way.

```js
// Same deceleration model as momentum scrolling. rate 0.998 feels like a normal scroll; 0.99 is snappier.
const restingOffset = (velocityPxPerSecond / 1000) * rate / (1 - rate);
const target = nearestSnapPoint(currentPosition + restingOffset);
```

Decide open versus closed from the direction of the velocity at release, not from which side of halfway the sheet sits.

For a dismiss, a quick flick is enough on its own: dismiss when the distance passes a threshold or the release speed is above roughly 0.1px per millisecond. Tune both on a real device.

## Soft edges

Past a boundary, the element follows less and less instead of stopping at an invisible wall. A hard stop reads as frozen; rising resistance reads as responsive with nothing further.

```js
// overshoot: px past the edge; size: the element's size on that axis; c = 0.55 is the scroll-view constant
const rubberBand = (overshoot, size, c = 0.55) =>
  (overshoot * size * c) / (size + c * Math.abs(overshoot));
```

## Direction and depth

- Intermediate frames should point at the outcome: a control that expands toward the finger telegraphs where it's going.
- A UI surface that arrives as frosted glass animates its blur and scale together, so it reads as a material arriving rather than a fade.
- A modal task dims what's behind it; a panel that works alongside the page keeps the page lit and uses offset or translucency instead.
- For very fast movement, a slight stretch or blur along the direction of travel reads better than a sharp streak.

## Sound and haptics

When motion is paired with sound or vibration, all of it fires on the same frame, from the event that caused it (the snap, the toggle flipping), and only on moments that matter: commit, success, error, snap. Feedback on everything teaches people to ignore it.

## Reduced motion

A gesture still tracks the finger under reduced motion; that's direct manipulation, not decoration. What changes is the settle: drop the overshoot, shorten the travel, or cross-fade to the end state.
