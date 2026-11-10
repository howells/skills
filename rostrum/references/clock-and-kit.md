# The frame: one clock, a kit, versioned cuts

Contents: project layout · config · timeline · Film (the one clock) · kit · fonts · cuts in Root · Remotion gotchas.

## Project layout

A hand-built project with pnpm, not the create-video template. Pin `remotion`, `@remotion/cli` and every `@remotion/*` package to the same exact version (no caret); mixed versions fail at bundle or render time. Add only what the film uses: `fonts` always, `media` for footage and sound, `noise`, `motion-blur`, `layout-utils`, `three`. Hand-built films cut on one clock, so `@remotion/transitions` is rarely needed.

```
STORYBOARD.md  BUILD-BRIEF.md  remotion.config.ts  scripts/
public/fonts/  public/img/  public/footage/  public/audio/
src/index.ts  src/Root.tsx  src/fonts.ts  src/theme.ts  src/kit.tsx  src/data/
src/timeline.ts  src/Film.tsx  src/acts/act-<name>.tsx
src/v2/timeline.ts  src/v2/Film2.tsx  src/v2/act-<name>.tsx   # each later cut
```

## remotion.config.ts

```ts
import {Config} from '@remotion/cli/config';
Config.setEntryPoint('./src/index.ts');
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(95);
Config.setOverwriteOutput(true);
Config.setCodec('h264');
Config.setCrf(18);
// Only when the film uses WebGL (effects, light leaks, three):
// Config.setChromiumOpenGlRenderer('angle');
```

## timeline.ts

Every shot and act in absolute frames, abutting. Acts are the unit a builder owns; transitions that span two acts (a dip to dark, a lift back) are owned by Film.

```ts
export const FPS = 30;
export const SHOTS = {s01: {from: 0, to: 150}, s02: {from: 150, to: 390} /* … */} as const;
export const ACTS = {open: {from: 0, to: 390}, search: {from: 390, to: 1014} /* … */} as const;
export type ActName = keyof typeof ACTS;
export const DIP = {from: 990, to: 1014} as const;
export const TOTAL = 2700;
export const since = (f: number, shot: keyof typeof SHOTS) => f - SHOTS[shot].from;
```

## Film.tsx: the one clock

The only `useCurrentFrame()` in the film. Each act is `FC<{f: number}>` and draws only inside its range, from the absolute frame, so a piece drawn on both sides of a cut is the same piece at the same frame. Don't wrap acts in `<Sequence>`: it resets the frame each act sees, and continuations stop matching.

```tsx
const acts: readonly [ActName, FC<{f: number}>][] = [['open', ActOpen], ['search', ActSearch] /* … */];

export const Film: FC = () => {
  const f = useCurrentFrame();
  const dip = f >= DIP.from && f < DIP.to ? linear(f, DIP.from, DIP.to - DIP.from) : 0;
  return (
    <AbsoluteFill style={{background: theme.paper, overflow: 'hidden'}}>
      {acts.map(([name, Act]) => (f >= ACTS[name].from && f < ACTS[name].to ? <Act key={name} f={f} /> : null))}
      {dip > 0 ? <AbsoluteFill style={{background: theme.ink, opacity: dip}} /> : null}
      <Grain f={f} />
    </AbsoluteFill>
  );
};
```

When a film has one subject the camera never leaves, Film also draws that subject once, inside `Camera`, and acts draw screen-space type and results over it. An act's leftovers fading during the next move are a `Tail` component registered under the next act's range.

## kit.tsx (trimmed)

Curves and moves are named for their job, so builders can't pick the wrong easing.

```tsx
const ease = {out: Easing.bezier(0.23, 1, 0.32, 1), inOut: Easing.bezier(0.77, 0, 0.175, 1)}; // quint out, quart in-out

/** 0 to 1 across `duration` frames from `at`, clamped. An `at` of Infinity (an exit that never comes) stays 0. */
export const tween = (f: number, at: number, duration: number, curve = ease.out) =>
  Number.isFinite(at)
    ? interpolate(f, [at, at + duration], [0, 1], {easing: curve, extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
    : 0;
export const mix = (p: number, from: number, to: number) => from + (to - from) * p;
export const arrive = (f: number, at: number, d: number) => tween(f, at, d, ease.out);  // entering or leaving
export const move = (f: number, at: number, d: number) => tween(f, at, d, ease.inOut);  // between two visible places
export const linear = (f: number, at: number, d: number) => tween(f, at, d, (t) => t);   // sweeps, pushes, dips
/** Weight coming to rest, no overshoot. */
export const settle = (f: number, at: number) => (f < at ? 0 : spring({frame: f - at, fps: FPS, config: {stiffness: 120, damping: 26}}));
/** A little overshoot: only for something that snaps or is thrown into place. */
export const snap = (f: number, at: number) => (f < at ? 0 : spring({frame: f - at, fps: FPS, config: {stiffness: 210, damping: 17, mass: 0.8}}));

/** Fade and rise into place; never from nothing. `out` fades it away. */
export const Rise: FC<{f: number; at: number; dy?: number; out?: number; style?: CSSProperties; children: ReactNode}> =
  ({f, at, dy = 16, out = Infinity, style, children}) => {
    const p = arrive(f, at, 20);
    const o = arrive(f, out, 14);
    return <div style={{...style, opacity: p * (1 - o), transform: `translateY(${mix(p, dy, 0) - 8 * o}px)`}}>{children}</div>;
  };

/** A world in its own pixels, seen by a camera centered on (x, y) at scale s. */
export const Camera: FC<{x: number; y: number; s: number; children: ReactNode}> = ({x, y, s, children}) => (
  <div style={{position: 'absolute', width: 1920, height: 1080, transformOrigin: '0 0',
    transform: `translate(${960 - x * s}px, ${540 - y * s}px) scale(${s})`}}>{children}</div>
);
/** Camera between keys on the on-screen curve, scale eased in log space so zooms feel even. */
export const camAt = (f: number, keys: readonly {at: number; x: number; y: number; s: number}[]) => {
  const n = keys.findIndex((k) => k.at > f);
  if (n <= 0) return keys[n === 0 ? 0 : keys.length - 1];
  const a = keys[n - 1], z = keys[n];
  const p = interpolate(f, [a.at, z.at], [0, 1], {easing: ease.inOut});
  return {x: mix(p, a.x, z.x), y: mix(p, a.y, z.y), s: a.s * Math.pow(z.s / a.s, p)};
};

/** Grain that changes every other frame, and a soft vignette, over everything. */
export const Grain: FC<{f: number}> = ({f}) => {
  const seed = Math.floor(f / 2) % 48;
  return (/* SVG feTurbulence (seed) at ~0.16 opacity, multiply, plus a radial vignette at ~9% */ null);
};
```

Add the film's own moves beside these (typing a phrase, a tool call rising in mono, a result settling, a sample with a layered paper shadow) as components, so every act draws them identically. A thread that recurs across acts (an id, a sample) is one component used everywhere.

## fonts.ts

Imported once from `Root.tsx` and `Film.tsx`. `loadFont` holds the render until the face has loaded.

```ts
import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';
export const fontsReady = Promise.all([
  loadFont({family: 'Inter', url: staticFile('fonts/InterVariable.woff2'), weight: '100 900'}),
  loadFont({family: 'IBM Plex Mono', url: staticFile('fonts/IBMPlexMono-Regular.otf'), weight: '400'}),
]);
```

Anything that measures text in the DOM (lift-outs, underlines under a word, `@remotion/layout-utils`) waits for `fontsReady` behind its own `delayRender`, or it measures the fallback face.

## Cuts in Root.tsx

Every cut stays registered, so any earlier cut can be re-rendered.

```tsx
<Composition id="Film" component={Film} durationInFrames={TOTAL} fps={FPS} width={1920} height={1080} />
<Composition id="Film2" component={Film2} durationInFrames={TOTAL2} fps={FPS} width={1920} height={1080} />
```

A later cut imports the earlier kit and data rather than editing them; a change that would alter an earlier cut goes in the new cut's folder.

## Remotion gotchas

- All motion comes from the frame. CSS transitions and animations, Tailwind `animate-*` and `transition-*`, `requestAnimationFrame` and timers don't render. `Math.random()` differs per frame and per worker; use `random(seed)`.
- `interpolate` throws on a non-finite or non-increasing input range; guard as `tween` does. `spring` before its start frame must be clamped to 0 by hand.
- Use `<Img>` and `staticFile()`; a plain `<img>` can be captured before it loads.
- Footage and sound: `<Video>` and `<Audio>` from `@remotion/media`. Trim with `trimBefore` and `trimAfter` in frames; `startFrom` and `endAt` are the old names.
- `@remotion/three`: `<ThreeCanvas>` needs `width` and `height`; never use `useFrame()`, drive everything from the frame. Render with `--gl=angle --concurrency=1`.
- `npx remotion ffmpeg` and `npx remotion ffprobe` exist when ffmpeg isn't installed. Use `-fps_mode vfr`, not the deprecated `-vsync`.
