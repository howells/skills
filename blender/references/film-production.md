# Film production and delivery

Use this reference file when several scenes must become one coherent Blender film. It covers integration and clocks, camera choreography, lighting and assets, sound, durable rendering and delivery. Apply the creative checks relevant to the requested scene; examples are diagnostic prompts, not mandatory story elements.

## One authoritative assembly

Name one integration lead and the authoritative scene, camera route, timeline and audio mix. Helpers can own separate modules or source assets. A source scene or approved candidate proves that detail in isolation; it has not been integrated until it survives the assembled film's clocks, visibility, lighting and actual camera.

Preserve approved source assets and newer room variants. Append candidate objects before capturing animation channels, continuous behaviours and light receivers. Replacing a current room with an older candidate can silently lose later furniture, rear treatment, curtains or material fixes. Transfer the required behaviour onto the current assembly and verify its intended targets.

Audit promised timed behaviours from the film camera after each integration: snowfall and accumulation, a complete set of seasonal states, curtain motion, overhead lighting and required orbits are all vulnerable to imported scenes or changed clocks. A successful append does not establish that those behaviours remain visible throughout the visit.

Keep one cue ledger in the film's global clock. Give each finite event an identity, time, target and resulting state. Derive picture and sound from that ledger. After a timing change, update reveal times, light cues, reaction pauses, camera travel, footsteps, voice placements, fall inserts and the ending together. Use a new version of the contract; don't silently change the duration of an existing render job.

### Story time and continuous behaviour

A held or remapped story clock can freeze curtains, dust, reels and other motion. Distinguish finite story events from ongoing activity:

1. Evaluate the story state at its mapped time.
2. Apply ongoing behaviours using elapsed film time after that update.
3. Apply final camera and explicitly ordered overrides.

Inspect authored F-curves. A finite curve clamps beyond its last key; advancing time does not make it loop. Loop only the channels that are meant to repeat, using their authored periods and correct pivots. Keep departure, extinction and other one-off events finite. Evaluate from saved base values rather than accumulating transforms, so backward seeks and chunk restarts reproduce the same image.

Record effective settings after all runtime overrides. A quality manifest claiming a transparency budget is insufficient if a later scene update replaces that value.

## Camera route and physical movement

Judge every promised approach, close inspection, orbit, circuit and departure from the actual film camera. A scene overview cannot establish the view through a window, prop visibility, full framing or whether a room's rear justifies walking around it.

- Establish the destination and surrounding gallery scale during travel. At close inspection, use framing and local darkness to envelop the viewer without making the next cue illegible.
- Stage cue, reaction or look, then movement. A lit destination should be readable before the camera travels. Avoid simultaneous cue and teleport-like departure.
- For a newly discovered room, hold long enough to recognise it, then approach and inspect. Preserve the reveal threshold and subsequent circuit. Don't orbit a plain, unrevealing rear merely to satisfy a path diagram; improve its authorised staging or revise the shot deliberately.
- Keep complete silhouettes, seasonal changes and important objects in frame. Check the tightest framing, not only a representative midpoint.
- Walking needs forward translation. Head bob without progress reads as bouncing. Tie bob amplitude/cadence and footstep level to measured movement speed; ease to a stop during stationary looks.
- A fall needs accelerating descent, foreground parallax, changing roll or orientation, a readable impact, a side-lying pause and a plausible rise into forward movement. Strobes and memory flashes can punctuate those actions but do not establish the fall by themselves.
- Inspect every join and approach at normal speed. A plinth that appears to distort during travel may be affected by changing field of view, near clipping, target interpolation, focus jumps or a path crossing a prop. Diagnose those before rebuilding sound geometry.

Darkness can be deliberate while important silhouettes and the next cue remain readable. Establish the ending through its intended visual and aural change; a prolonged or aimless look around a vignette does not automatically create an ending.

Use a bounded independent narrative review when the visual treatment creates a real judgement call. Give the reviewer actual frames, approved text and the specific question, such as whether an object explains too much. Preserve narrative restraint and agreed wording. Settled material needs another creative review only when integration breaks it or new feedback changes the brief.

## Light, grounding and window views

Control the scene through local lighting and receiver membership. Raising exposure or global fill can erase darkness, reveal the surrounding chamber too early and wash out another vignette. Preserve the approved colour transform while diagnosing the local cause.

An emissive material and an actual light are separate channels. Trace whether brightness comes from emission, direct/reflected illumination or both. Fade the relevant material channel and its light together; fading light energy alone can leave a glowing object. A moving pendant needs its light and resulting shadow to move coherently.

A light copied after its source has switched off can inherit a zero-strength emission shader even when its wattage is nonzero. Inspect the effective node inputs after the scene-time update. Since Blender 5.1, `Light.use_nodes` is a deprecated no-op ([API reference](https://docs.blender.org/api/5.3/bpy.types.Light.html)); setting it false does not bypass the shader. For an independent practical, use clean light data or explicitly restore the intended emission graph and animate its real inputs. Check whether an opaque lantern base blocks the light origin. Prove contribution with an actual before/after camera render before adjusting power; a glowing lantern alone does not demonstrate a lit floor.

Measure evaluated geometry and complete asset hierarchies, as described in the main skill. Confirm real-world scale and contact with the actual floor. Check trunks, longcase clocks, chairs, side tables and small practicals for floating bases, exaggerated size and shelf penetration. A reading arrangement needs usable chair/table spacing, window clearance and a visible clock; plausible coordinates do not replace its rendered view. Reuse curtains and retain their animation without closing the required view.

Align frost and condensation to the actual door or window opening. A misplaced overlay can read as a second ghost doorway. Check snow accumulation against boots and ground contact, and tie footprints to the departure path and timing. Inspect door swing and figure clearance together; intersecting them is a defect unless deliberately directed.

For a window or portal containing an exterior scene:

- Constrain the view through the actual pane/opening, including the front/reverse transition and glass cue. Check camera rays at the pane edges and at both ends of the camera path.
- Hidden backing cards and trees may remain visible in reflection or cast shadows outside the intended opening. Inspect per-ray visibility and isolate the offending set. Disabling camera visibility alone does not remove its shadows.
- If measured ray evidence identifies unintended scenery shadows, change shadow visibility only on that scenery. Preserve the real room's meshes, glass and lighting behaviour. Keep legitimate reflection, transmission and volume dependencies.
- Alpha foliage can turn black when transparent-ray depth is exhausted. Inspect material alpha paths and the effective transparent bounce limit before changing its colour or adding fill. Verify the correction in the densest view and through glass.

## Projection and practical detail

A projector should be a coherent mechanism. Use moving footage, retain the native reel rotation, measure the reel axes and wind film on them. Route a taut film path through the actual rollers and gate. Check direction and clearance in the camera view before inventing alternative mechanics.

Use restrained mechanical jitter, coordinated flicker, a readable beam and dust. Arbitrary camera shake does not make a projected image feel mechanically unstable. Sequence the projection cut, the viewer's hold or reaction, the turn and departure. Remove superseded alternatives from the delivery checklist so an old blank-wall or reverse-reel idea cannot quietly return.

For pond staging, keep a concealed fracture concealed until its cue. Use still-water ambience when the water is essentially still. A stream recording can change the perceived location. Ensure a picnic blanket reads as fabric of the intended type and sits at the edge, rather than appearing to be malformed water. Confirm axe or other critical prop visibility from the moving film camera; an overhead layout view is insufficient. Prove any small ripple and final extinction at their intended time.

## Found assets, foliage and disappearance

Track source, licence/credit, file identity and any authorised adaptation. Approval for generated concept art does not authorise generated production assets. Respect a found-asset requirement; simple geometry proxies also need appropriate authorisation when they replace a requested sourced object.

Photographic leaf assets need intact textures and UVs. Check visible coverage at camera height and actual occupied floor area. A scatter's bounding box can cover the floor while leaving bare holes throughout it. Measure mesh/instance occupancy or ray hits, inspect the resulting image, and ground every visible trunk against the real floor height.

If trees disappear but leaves remain, author those as separate visibility states. Explicitly cover the full required chamber floor, including return travel, instead of assuming the original forest scatter extends there. Keep leaf lighting consistent after the trees are removed.

Give each disappearing tree or group a distinct event in the cue ledger. Use irregular, readable spacing where requested. Recomputing a sound trigger on every frame can create a burst of breaker clicks within milliseconds. Schedule the heavy recorded breaker once per event, with the same intended reverb on both on and off cues. Include a confused look around when the removal is meant to reveal the chamber's scale.

## Narration and sound with picture

Lock the permitted processing explicitly. When narration is native full takes with reverb only, preserve speed, pitch, word endings and the established faders; don't stretch takes to repair sequencing. Move cues or extend picture instead. Retain full ends and a deliberate reverb release where required. An abrupt unfinished phrase often reads as an editing bug. Never deliver a temporary text-to-speech stand-in as the approved voice.

Build continuous ambience with transitions rather than a succession of unrelated clips. Carry the underlying drone or room bed across picture cuts when requested, adjusting its level beneath narration. Use appropriate night ecology and believable close/distant placement. Leaf steps should support the voice. Derive dry footsteps from translation so they stop during a look; an existing reverb decay may remain after the physical step stops.

Keep these measurements distinct:

| Check | What it establishes |
|---|---|
| Source hash and cue duration | The selected complete take and its placement |
| Dry-stem PCM correlation after the established constant gain | Native source samples are retained within the documented encoding tolerance |
| Mix peak below 0 dBFS | No full-scale clipping at the measured stage |
| Digital-zero intervals and noise-floor/RMS measurements | Silence or bed continuity; neither establishes audibility or dramatic suitability alone |
| Unmuted playback with picture | Perceived balance, continuity, timing and intelligibility |

Hash the motion recording used to build footsteps and compare it with the audio manifest. A refreshed route with an older audio export can pass take-identity checks while its steps follow the wrong movement. Include audio source, dry/reverb stems, cue contract and output identities in the frozen render inputs.

An ending may require exact silence or a continuous quiet bed. Honour the latest direction and record it; neither is a universal policy. Don't label 0 dBFS as silence. Technical PCM checks, muted playback and media-error counters do not constitute listening approval.

## Freeze, resume and deliver

Use the shortest actual-camera excerpt or still sequence that can expose the unresolved defect. Where motion, flicker or denoising is at issue, render a short native-frame-rate passage. Once that evidence resolves the named concern, progress to the complete low-cost sequencing preview. Avoid adding successive review gates without a new risk.

Before rendering, freeze a versioned manifest containing the scene, route/camera, timing contract, behaviour and support modules, external assets, source/audio manifests, motion recording and effective quality settings. Store a fingerprint with each completed frame. Deliberately change an isolated dependency or use a known stale record once to prove the reuse guard refuses it. A changed input needs a new output directory or an explicitly audited bounded replacement; it must not inherit unmatched frames.

Write each frame to a temporary name, verify dimensions and successful closure, then atomically publish it with its identity record. Close the movie only after encode checks, a full decode and a final input check; replace the deliverable atomically. Preserve matching frames and lossless audio after interruption. Restart only failed or invalidated work.

Before resuming any background job, read its current state, process identity and log. Don't duplicate a healthy runner or restart a job intentionally stopped because newer direction superseded it. Scheduled completion prompts can become stale: update or pause them when the creative brief changes, and stop repetition after successful delivery.

Label the media accurately. Rendering six unique frames per second and repeating them in a 24 fps MP4 is a sampled preview. Enlarging a low-resolution image during encoding does not produce a genuinely rendered higher-resolution film. Keep any enlarged preview snow or particles explicit, with the final factor set to one unless the user approves a production change.

For delivery:

- Check exact encoded duration and frame count, dimensions, intentional blackouts, all voice placements and the agreed ending. Verify complete decoding, not just container metadata.
- Inspect the actual encoded film through the whole journey, including every approach, circuit, seasonal change, join, fall and final walk. Test normal playback. Stills, excerpts and zero dropped-frame callbacks cover different risks; none alone approves the whole film.
- Listen with picture, separately from technical source checks. If the user requested preview approval, obtain it before the expensive complete render.
- Use a broadly playable MP4 such as H.264/yuv420p with stereo AAC and fast-start metadata. Preserve the rendered frames and lossless audio. A compatible encoding profile does not prove playback on a phone; distinguish actual device playback from desktop/browser verification.
- Share the actual MP4 inline and as a usable download in the current conversation when the host supports it. A status claim or contact sheet is not the requested film.
- Close every promised detail with rendered evidence or an explicit approved omission/replacement. Keep implementation status, technical validation, creative review and user acceptance distinct.
