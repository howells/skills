# Render performance

Use this reference file before estimating a long film, changing render quality to address slowness, or deciding whether persistent scene data is worthwhile. It covers timing attribution, controlled benchmarks, GPU/device state, caching, visibility, quality and a measured case study.

For scene assembly, audio and delivery checks, read [Film production and delivery](film-production.md).

## Measure the whole job

Record Blender version, engine, effective scene settings, hardware/device selection, input fingerprint and the frame/camera sample. Keep elapsed wall time separate from active work. Break down the pipeline far enough to identify the dominant cost:

| Component | Measurement |
|---|---|
| Process startup and scene/asset loading | Child process start to assembly ready |
| Manifest and asset hashing | Dedicated timer, file count and bytes hashed |
| Behaviour evaluation/depsgraph update | Time around the frame update, with deferred work attributed cautiously |
| Geometry/BVH preparation | Engine preparation statistics where available |
| Path tracing and denoising | Engine phase timers or logs, separately when available |
| Image encoding and disk write | Render/write timing and bytes written |
| Movie/audio encoding and verification | Separate encode and full-decode timers |
| Idle, sleep and interruption | Gaps between process and frame timestamps, confirmed against system evidence |

A timer around `film.at()` plus `bpy.ops.render.render(write_still=True)` includes scene updates, preparation, denoising and writing. Do not call it GPU path-tracing time. Some depsgraph work is deferred until rendering; avoid claiming precision that the available timers cannot provide.

When a small render is unexpectedly slow, inspect this breakdown before lowering resolution again. Asset loading, hashing and repeated scene initialisation do not scale with pixel count. Neither slow wall time nor one expensive still proves that the hardware cannot render the film.

## Controlled tests before choosing settings

Use identical cameras, scene state, seed, colour transform and quality settings for a paired comparison. Change one factor at a time. Start with a small representative set covering glazing, projection, alpha-heavy forest and dark reflective water, plus transitions between them.

For a resolution comparison, hold samples and caching constant. For a cache comparison, hold resolution and samples constant. Separate the first frame from warm frames and retain the test images. Compare images with aligned dimensions and an absolute metric; inspect the actual images as well. Differences near sharp edges can be small in aggregate yet visible in motion.

Test short native-frame-rate movement to judge noise and denoising shimmer. A still-image difference or one successful cross-scene sample does not certify a long sequence. Check memory usage and correctness across scene changes, including the densest foliage and the most expensive reflection/transmission state.

Before a final-film estimate, compare relevant sample counts, for example 32, 64 and 128, using the same representative views and short motion passages. Choose the fastest settings that preserve the approved image and temporal stability. A 4K opening still may have a different sample count, scene cost and cache state; its timing alone cannot predict the whole film.

## Device, cache and chunk ownership

Verify the device actually used in Cycles preferences and render logs. An engine/device label in the requested configuration is not evidence that the intended GPU is active. On Metal, inspect GPU selection, ray-tracing mode and the denoising device as separate settings. Confirm availability instead of silently accepting a CPU fallback when the estimate assumes GPU rendering.

Use the official [Cycles performance documentation](https://docs.blender.org/manual/en/latest/render/cycles/render_settings/performance.html) and [GPU rendering documentation](https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html), selecting the installed Blender version before applying settings.

Persistent render data is a measured choice. An earlier crash justifies a bounded reproduction and cache test; it does not establish that caching must always stay off. Conversely, fast warm frames do not establish stability across the complete film. Compare actual images, scene transitions and memory before adopting it for the relevant job.

Classify a native crash by its stack and phase before attributing it to caching or scene geometry. A failure inside a Metal shader compiler before any frame closes is different evidence from a failure after many mixed-scene updates. Preserve valid frame identities, capture the crash context and try a bounded unchanged-input retry when justified. Don't respond automatically with a complete rerender or lower quality; the cause and recovery remain unconfirmed until measured.

Cycles persistent scene data and Metal shader binary archives are separate caches. In Blender commit `fbe6228777e7`, [archive selection at `kernel.mm:402`](https://github.com/blender/blender/blob/fbe6228777e7d9afefcd61a413844e790ae75db7/intern/cycles/device/metal/kernel.mm#L402) includes the `CYCLES_METAL_DISABLE_BINARY_ARCHIVES` switch; [archive saving at line 828](https://github.com/blender/blender/blob/fbe6228777e7d9afefcd61a413844e790ae75db7/intern/cycles/device/metal/kernel.mm#L828) constructs a file URL before serialisation. A measured crash offset matched that archive-save URL construction, outside the geometry/BVH path. The upstream invalid path-string cause, a possible race and the effectiveness of bypassing archive I/O remained unproved. Diagnose and test the affected cache specifically; don't conflate it with persistent scene data or prescribe disabling both.

Use one GPU owner and coordinate with other projects using the same machine. Overlapping render, capture or other GPU-heavy processes can invalidate timings and slow both jobs. Keep chunks large enough to amortise scene loading and validation while bounding restart cost. Avoid loading Blender separately for every frame. Keep the chosen chunk size in the job configuration and report startup costs separately.

On macOS, a lifetime `caffeinate` assertion can prevent idle sleep while the runner is alive. It does not guarantee rendering through lid closure or other system suspension. Verify process lifetime and timestamp gaps rather than treating a detached launch as proof of uninterrupted progress.

Hash all inputs needed for frame reuse, but measure the cost. Re-reading gigabytes of identical assets in many short chunks can dominate a preview. Amortise validation across a frozen bounded batch without weakening the changed-input check. Retain immutable manifests and per-frame identities; never skip validation merely to improve the reported render rate.

## Visibility and quality changes

Scene visibility culling must consider camera, reflection, shadow, transmission and volume dependencies. An object outside the camera can still be required in the image. Render the affected view before and after culling and account for lights/material emission separately.

Dense alpha foliage can exhaust transparent-ray depth. Keep an explicit effective transparency budget and test the hardest view, especially through glass. Increasing every bounce limit is not a general fix for black foliage or an efficient quality policy. Trace the relevant ray/material path first.

Retain the approved engine, colour transform and framing during diagnosis. Don't switch engines, add global fill, increase all bounces, lower resolution or enable stronger denoising solely because a job feels slow. Each changes a different part of the image; make the measured change that addresses the identified cost or defect.

Record preview-only adaptations such as enlarged snow or dust separately from production assets. The same particle needs a different world-space enlargement to occupy the same number of pixels at different render resolutions. Use explicit factors and compare the actual camera image. The final factor remains one unless the authored look is deliberately changed.

## Estimate from representative evidence

Count genuinely rendered frames separately from encoded frames. For a sampled preview, count both its normal stride and any native-rate intervals, such as a fall. For a native final, require a rendered frame for every output frame.

Estimate scene work using measured costs weighted by the film's scene mix, then add expected chunk initialisation, hashing, encoding and verification. Report the range and the sample that supports it. Avoid extrapolating only warm cache rates when the intended runner repeatedly reloads, or only cold rates when it retains one loaded scene. Use measured PNG sizes for a disk estimate and retain space for the movie, lossless audio and bounded replacements.

Once the benchmark answers the named uncertainty, proceed to the requested artefact. Further checks need a specific unresolved risk. Explain a revised estimate from measured costs, not from general claims about ray tracing.

## Measured case study: a multi-scene walkthrough

These observations came from one local Cycles film workflow. They demonstrate how to separate overhead from image rendering. They are not universal speed ratios, a hardware capability claim, or certification of cache stability through long motion.

### Original sampled preview

The job rendered 3,972 actual images at 320×180. Elapsed time was about 7 hours 12 minutes. Frame timers accounted for about 5 hours 15 minutes, but those timers included update, render and write work. System sleep accounted for approximately 92 minutes. The runner performed 17 initialisations, around 85 seconds each, and repeatedly hashed 277 assets totalling 7.635 GiB.

Those categories used different timing boundaries and should not be forced into an exact additive GPU-time total. The useful comparison was against a controlled rerun, not a pixels-only extrapolation.

### Same ten frames across five cameras

| Configuration | Measured seconds per frame |
|---|---:|
| 320×180, 2 samples, persistent data off | Mean 5.925664 |
| 1280×720, 2 samples, persistent data off | Mean 6.051890 |
| 1280×720, 2 samples, persistent data on | First frame 5.3702 |
| Same persistent-data job | Following nine frames mean 1.41815 |

For this paired image comparison, mean absolute image difference was at most 0.045874 on an 8-bit 0–255 scale; the largest channel difference was 8. The images and cameras were controlled. The result supported testing persistent data in the actual sequence. It did not prove that every animated frame would remain stable or that resolution never affects cost.

### Subsequent 720p scene check

A real 16-frame check at 1280×720 and 6 samples measured:

- First frame: 16.3845 seconds.
- Following frames: median 1.94596 seconds, mean 2.48002 seconds.
- Total frame work: 53.58 seconds.
- Child process elapsed: 182.81 seconds, including 55.67 seconds of initialisation and 73.39 seconds of hashing.

The warm image work was only part of this short job. Larger bounded chunks could amortise its loading and hashing, while actual camera images and motion still needed review. The next estimate should use the intended chunking, sample count and full scene mix rather than copying any single number from this case study.
