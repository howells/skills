# Render performance

For estimating a long film, a render that feels slow, or deciding on persistent scene data.

## Attribute the time before changing quality

Keep wall time separate from active work, and break the job down far enough to find the dominant cost: process start and scene load, asset hashing, depsgraph update, BVH preparation, path tracing and denoising, image write, movie encode and decode check, and idle or sleep gaps (confirm against system evidence).

A timer around `film.at()` plus `render.render(write_still=True)` includes update, preparation, denoise and write; it is not GPU path-tracing time. When a small render is unexpectedly slow, check this breakdown before lowering resolution again: loading, hashing and re-initialisation don't scale with pixels.

## Controlled tests

- Paired comparisons hold camera, scene state, seed, colour transform and quality fixed and change one factor. Resolution tests hold samples and caching; cache tests hold resolution and samples. Separate first frame from warm frames.
- Cover the hard cases: glazing, projection, alpha-heavy forest, dark reflective water, and transitions between scenes.
- Compare images at aligned dimensions with an absolute metric, and look at them; small aggregate differences at sharp edges show in motion.
- Judge noise and denoise shimmer from short native-frame-rate passages, not stills.
- Before a final estimate, compare sample counts (e.g. 32, 64, 128) on the same views and passages; pick the fastest that keeps the approved image stable.

## Device, cache and chunks

- Verify the device actually used in Cycles preferences and render logs; a requested label is not evidence. On Metal, GPU selection, ray-tracing mode and denoise device are separate settings. Don't accept a silent CPU fallback when the estimate assumes GPU.
- Persistent scene data is a measured choice. One past crash justifies a bounded test, not a permanent ban; fast warm frames don't prove stability across the whole film.
- Classify a native crash by stack and phase first. Cycles persistent data and Metal shader binary archives are separate caches: one measured crash sat in archive-save URL construction (`intern/cycles/device/metal/kernel.mm`, which also reads `CYCLES_METAL_DISABLE_BINARY_ARCHIVES`), outside geometry/BVH. Test the specific cache; don't disable both or rerender everything at lower quality by reflex.
- One GPU owner per machine; overlapping GPU jobs invalidate timings and slow both.
- Chunks big enough to amortise load and validation, small enough to bound restarts. Never load Blender per frame.
- `caffeinate` prevents idle sleep only; it doesn't survive lid close. Check timestamp gaps.
- Hash every input needed for frame reuse, but measure it: re-hashing gigabytes per short chunk can dominate a preview. Amortise validation over a frozen batch; never skip it to improve the reported rate.

## Visibility and quality

- Culling must respect camera, reflection, shadow, transmission and volume dependencies. Render before and after.
- Black dense foliage is usually exhausted transparent-ray depth; raising every bounce limit isn't the fix. Trace the path, keep an explicit transparency budget, test the hardest view through glass.
- Don't switch engine, add global fill, raise all bounces, drop resolution or denoise harder because a job feels slow. Make the change that addresses the measured cost.
- Preview-only enlargements (snow, dust) are explicit factors; the same particle needs different enlargement per resolution. Final factor is one.

## Estimates

Count rendered frames separately from encoded ones (sampled stride plus any native-rate intervals). Weight measured per-scene costs by the film's scene mix, add chunk init, hashing, encode and verification, and report a range with the sample behind it. Don't extrapolate warm-cache rates for a runner that reloads, or cold rates for one that doesn't. Size disk from measured PNGs plus movie, lossless audio and replacements.

## Case study: one multi-scene Cycles walkthrough

Not universal ratios; an example of overhead hiding behind "slow rendering".

- A 320×180 sampled preview of 3,972 frames took 7 h 12 m. About 92 min was system sleep; 17 runner initialisations cost ~85 s each; every chunk re-hashed 277 assets (7.6 GiB).
- Same ten frames, five cameras, 2 samples: 320×180 at 5.93 s/frame vs 1280×720 at 6.05 s/frame. Resolution barely mattered. With persistent data on at 720p: first frame 5.37 s, next nine 1.42 s mean. Max image difference 8/255.
- A 16-frame 720p, 6-sample check: 53.6 s of frame work inside 182.8 s elapsed, of which 55.7 s was initialisation and 73.4 s hashing.
