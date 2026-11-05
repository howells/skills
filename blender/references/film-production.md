# Film production and delivery

For several scenes becoming one Blender film.

## One assembly

- One lead owns the assembled scene, camera route, timeline and audio mix; one process owns the GPU. Helpers own separate modules or source assets.
- A scene that looks right in isolation isn't integrated until it survives the film's clock, visibility, lighting and actual camera. Append candidate objects to the current assembly; replacing it with an older file silently loses later fixes.
- Keep one cue ledger in the film's global clock: each event has a time, target and resulting state, and picture and sound both derive from it. A timing change updates every dependent cue at once.
- A held or remapped story clock freezes continuous motion (cloth, particles, reels). Per frame: evaluate story state at its mapped time, apply ongoing behaviours from elapsed film time, then the camera and overrides. Evaluate from saved base values, not accumulated transforms, so seeks and chunk restarts reproduce the same image. A finite F-curve clamps after its last key; it doesn't loop.

## Camera

- Judge everything through the actual film camera, never an overview.
- Cue, then look, then move. A destination should read before the camera travels.
- Walking needs forward translation; bob without progress reads as bouncing. Tie bob and footsteps to measured speed.
- A prop that seems to distort during travel is usually FOV change, near clipping, target interpolation or focus jumps. Diagnose before rebuilding geometry.

## Light

- Fix darkness with local lights and receiver membership, not exposure or global fill, and keep the approved colour transform.
- Emission and light are separate: fade the material and its light together.
- A light copied after its source switched off can inherit a zero-strength emission shader despite nonzero wattage. Since 5.1 `Light.use_nodes` is a no-op, so use clean light data or restore the emission graph. Prove contribution with a before/after render.
- Hidden scenery still shows in reflections and casts shadows. Turn off shadow visibility only on the offending object.
- Alpha foliage turning black means transparent-ray depth ran out; check the transparent bounce limit before touching colour.
- Check real-world scale and floor contact; small props float and penetrate.

## Found assets

Track each asset's source, licence and file identity. Approved concept art doesn't authorise generated production assets, and a proxy standing in for a requested object needs approval.

## Sound with picture

- Lock the permitted processing. "Native takes, reverb only" means no stretching or pitch change: move cues or extend picture instead. Never deliver a TTS stand-in as the approved voice.
- Carry one ambience bed across cuts rather than a run of unrelated clips.
- Hash the motion that drives footsteps against the audio export, or steps land on stale movement.
- Peak and hash checks prove placement, not balance or timing. Only listening with picture does that. 0 dBFS is not silence.

## Render and deliver

- Freeze a versioned manifest before the final render: scene, camera, timing, assets, audio and effective quality settings. Changed inputs get a new output directory, never inherited frames.
- Write each frame to a temporary name and publish it atomically, so an interrupted job resumes by redoing only invalid frames. Read a background job's state and log before restarting it.
- Label previews honestly: repeated frames or encode-time upscaling are not a full render.
- Deliver H.264, yuv420p, stereo AAC, fast-start. Watch the encoded file end to end with sound, and check it plays on a phone.
