# Film production and delivery

For several scenes becoming one Blender film. Examples are diagnostic prompts, not required story elements. A Blender film does not imply permission to build a game-engine version.

Contents: one assembly · camera · light and windows · projection and props · found assets · sound · freeze, resume, deliver

## One assembly

- One lead owns the assembled scene, camera route, timeline and audio mix; one process owns the GPU. Helpers own separate modules or source assets.
- A source scene or approved candidate proves detail in isolation only. It isn't integrated until it survives the film's clocks, visibility, lighting and actual camera.
- Don't replace a current room with an older candidate: it silently loses later furniture, curtains and material fixes. Append candidate objects, then carry animation channels, behaviours and light receivers onto the current assembly.
- After each integration, re-check promised timed behaviours from the film camera: snowfall and accumulation, every seasonal state, curtain motion, overhead lights, orbits.
- Keep one cue ledger in the film's global clock: each finite event has an identity, time, target and resulting state. Derive picture and sound from it. After a timing change, update reveals, light cues, pauses, camera travel, footsteps, voice, inserts and the ending together, as a new contract version.
- Get the requested sequencing and sound approval before the expensive final render.

### Story time and continuous behaviour

A held or remapped story clock freezes curtains, dust and reels. Per frame:

1. Evaluate story state at its mapped time.
2. Apply ongoing behaviours from elapsed film time.
3. Apply the final camera and ordered overrides.

A finite F-curve clamps after its last key; it doesn't loop. Loop only channels meant to repeat, with their authored periods and pivots. Evaluate from saved base values, not accumulated transforms, so seeks and chunk restarts reproduce the same image. Record effective settings after all runtime overrides; a later scene update can replace the manifest's value.

## Camera

Judge every approach, close inspection, orbit and departure through the actual film camera; an overview can't show the view through a window or whether a room's rear earns a walk around it.

- Cue, then reaction or look, then movement. A lit destination should read before the camera travels; no teleport-like departure on the cue.
- A newly discovered room: hold to recognise, then approach and inspect. Don't orbit a plain rear just to satisfy a path diagram.
- Keep whole silhouettes and seasonal changes in frame at the tightest framing, not a midpoint.
- Walking needs forward translation; bob without progress reads as bouncing. Tie bob and footstep level to measured speed; ease to a stop on looks.
- A fall needs accelerating descent, foreground parallax, changing roll, a readable impact, a side-lying pause and a plausible rise. Strobes and flashes punctuate it; they don't establish it.
- A prop that seems to distort during travel is usually FOV change, near clipping, target interpolation, focus jumps or the path crossing it. Diagnose before rebuilding geometry.
- Darkness is fine while silhouettes and the next cue stay readable. An ending needs an intended visual and aural change; aimless looking around isn't one.

For a real judgement call (does this object explain too much?), give an independent reviewer actual frames, the approved text and the one question. Don't re-review settled material unless integration broke it.

## Light and windows

- Fix darkness with local lights and receiver membership. Raising exposure or global fill erases darkness, reveals the chamber early and washes out other vignettes. Keep the approved colour transform.
- Emission and light are separate channels. Fade the material and its light together; fading wattage alone leaves a glowing object. A moving pendant's light and shadow move with it.
- A light copied after its source switched off can inherit a zero-strength emission shader despite nonzero wattage. Since 5.1 `Light.use_nodes` is a no-op, so setting it false doesn't bypass the shader. Use clean light data or restore the emission graph. Check an opaque lantern base isn't blocking the origin. Prove contribution with a before/after render; a glowing lantern doesn't prove a lit floor.
- Check real-world scale and floor contact: trunks, longcase clocks, chairs, side tables and small practicals float, oversize and penetrate shelves. A reading corner needs usable chair/table spacing, window clearance and a visible clock in the render.
- Align frost and condensation to the actual opening; a misplaced overlay reads as a ghost doorway. Check snow against boots, footprints against the departure path, door swing against figures.
- Window to an exterior: check camera rays at the pane edges at both ends of the path. Hidden backing cards and trees still show in reflections and cast shadows; disabling camera visibility doesn't remove shadows. Turn off shadow visibility only on the offending scenery.
- Alpha foliage turns black when transparent-ray depth runs out. Check the material's alpha path and the effective transparent bounce limit before changing colour or adding fill; verify in the densest view and through glass.

## Projection and props

- A projector is a mechanism: moving footage, native reel rotation, film wound on the measured reel axes, a taut path through the actual rollers and gate. Restrained mechanical jitter, coordinated flicker, a readable beam and dust; camera shake doesn't sell it. Sequence cut, hold, turn, departure. Remove superseded ideas from the checklist so they can't return.
- Pond: a concealed fracture stays concealed until its cue; use still-water ambience for still water (a stream recording moves the location). A picnic blanket must read as fabric at the edge, not malformed water. Check critical props from the moving camera.

## Found assets and foliage

- Track source, licence, file identity and authorised adaptation. Approved concept art doesn't authorise generated production assets; a proxy replacing a requested sourced object needs approval too.
- Photographic leaves need intact textures and UVs. A scatter's bbox can cover the floor while leaving holes; measure occupancy or ray hits, look at the image, and ground every visible trunk.
- Trees disappearing while leaves stay are separate visibility states. Cover the whole required floor, including return travel, and keep leaf lighting consistent after the trees go.
- Each disappearing tree is its own ledger event, irregularly spaced if asked. Recomputing a sound trigger every frame fires a burst of breaker clicks; schedule the recorded breaker once per event, same reverb on on and off.

## Sound with picture

- Lock the permitted processing. Native full takes with reverb only means no stretching or pitch change: move cues or extend picture instead. Keep full word endings and the reverb release. Never deliver a TTS stand-in as the approved voice.
- Continuous ambience with transitions, not a run of unrelated clips; carry the bed across cuts under narration. Night ecology, believable placement. Dry footsteps derive from translation and stop on looks.
- Hash the motion recording that drives footsteps against the audio manifest; a refreshed route with an old audio export passes take checks with steps on the wrong movement.
- An ending may need exact silence or a quiet bed; follow the latest direction. 0 dBFS is not silence.
- Technical checks (source hash, dry-stem correlation, peak below 0 dBFS, digital-zero intervals) prove placement and integrity, not balance or timing. Only unmuted playback with picture does that.

## Freeze, resume, deliver

- Use the shortest actual-camera excerpt that can expose the open defect; native frame rate when motion, flicker or denoising is at issue. Once it's resolved, move to the full low-cost preview. Don't add review gates without a new risk.
- Freeze a versioned manifest before rendering: scene, camera route, timing contract, modules, assets, audio, motion recording, effective quality settings. Fingerprint each frame. Changed inputs get a new output directory, never inherited frames.
- Write each frame to a temporary name, check it, publish atomically with its identity record. Close the movie only after encode, full decode and a final input check. On interruption keep matching frames and lossless audio; redo only invalid work.
- Before resuming a background job, read its state, process and log. Don't duplicate a healthy runner or restart one stopped because direction changed. Update or stop scheduled prompts when the brief changes or delivery is done.
- Label media honestly: six unique frames per second repeated in a 24 fps MP4 is a sampled preview; upscaling at encode isn't a higher-resolution render. Preview-enlarged snow or particles stay explicit, final factor one.
- Deliver H.264/yuv420p, stereo AAC, fast-start. Check exact duration, frame count, dimensions, blackouts, every voice placement and the ending, with a full decode. Watch the encoded film end to end and listen with picture. Desktop playback isn't phone playback.
- Share the actual MP4 inline and as a download when the host supports it; a status claim or contact sheet isn't the film. Close every promised detail with rendered evidence or an approved omission.
