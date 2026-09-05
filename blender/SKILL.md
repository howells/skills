---
name: blender
description: "Inspect, measure and render Blender scenes through MCP or headless CLI. Use for Blender scene, render-pipeline or MCP work. Not for 2D design files (`paste-up`)."
---

# Blender

Two ways in, and they are not interchangeable.

**Interactive**, through the MCP server, talking to an add-on inside a running Blender. The user can see everything you do. Their viewport, their unsaved edits, their file.

**Headless**, `blender -b file.blend --python script.py -- args`. Its own process, no UI, nothing shared. This is where renders and long sweeps belong.

The rule that decides which: *does this touch state the user is looking at?* Use the live MCP for inspection and user-authorized edits to the open scene. Use headless Blender on an explicit copy for long renders or batch processing; never replace the user's open file with a headless result without reconciling live edits. Choose the route by the owned document and task, not merely by whether it writes a file.

---

## 1. The single rule that outranks everything

**Look at the render. Every time. Open the actual image file.**

Not the coordinates. Not the assertion. The image.

Every serious failure in this domain has the same shape: a measurement passes, a confident report goes out, and the defect is plainly visible on screen. The measurement was aimed by an assumption about where the answer would be. It returned a number, and the number was measuring something else.

Worked example, and it is the canonical one. Eight plants were placed outside a room. A containment test reported every one clear of the room volume. Rendered, the room was *filled* with them — two masses covering a third of the frame. The test read `ob.data.vertices`, the base mesh: half-metre blobs outside the wall. The objects carried particle instancing. Through the depsgraph: **9,225 instances inside the room**, clumps 2.5 m tall reaching a third of the way across the floor. The check was not weak. It was measuring a different object.

So: render, then `Read` the PNG, then say what you see. Never describe a render you have not opened.

**Before trusting a measurement, say out loud what result would have disconfirmed you.** If nothing would have, it is not an instrument.

---

## 2. Measuring a scene without lying to yourself

### Evaluated geometry, never base geometry

`ob.data.vertices` and `ob.bound_box` on a raw object give you the mesh *before* modifiers, particle systems, geometry nodes and instancing. What renders is the evaluated result, and it can be orders of magnitude larger.

```python
dg = bpy.context.evaluated_depsgraph_get()
ev = ob.evaluated_get(dg)
cs = [ev.matrix_world @ Vector(c) for c in ev.bound_box]   # cheap, conservative
```

`evaluated_get(dg).bound_box` covers modifiers. It does **not** cover instances — particle systems, collection instances, geometry-nodes points. For those you must walk the instances:

```python
for inst in dg.object_instances:
    ob = inst.object
    if ob is None or ob.type != "MESH" or ob.hide_render:
        continue
    cs = [inst.matrix_world @ Vector(c) for c in ob.bound_box]
```

`inst.matrix_world` is the per-instance transform. `inst.is_instance` says whether it is generated; `inst.parent` names the emitter. A scene reporting 86 objects can be 9,000 instances.

### Overlap, not containment

A containment test ("is the whole bbox inside?") answers a question nobody asked. Penetration is *any* intersection:

```python
def overlaps(lo, hi, X0, X1, Y0, Y1, Z0, Z1):
    return (hi[0] > X0 and lo[0] < X1) and (hi[1] > Y0 and lo[1] < Y1) and (hi[2] > Z0 and lo[2] < Z1)
```

Containment reports "outside" for an object half-buried in a wall. That is exactly the case you are hunting.

### Refuse, do not report

A printed number beside a check is not a check. Raise:

```python
if still_inside:
    raise SystemExit(f"REFUSING: still inside the room: {still_inside}")
```

A value you read is one you can rationalise. A value you refuse on is one you cannot.

### A bounding box is conservative

Clearing a bbox guarantees no penetration. A crossing bbox does **not** prove penetration — a tree's box can cross a wall while no leaf does. Say which you mean. For "make sure nothing pokes through", conservative bbox clearance is the right, honest answer, and it is enforced by *position*, not by collision. Nothing stops the next asset being dropped through the wall. The sweep has to be re-run.

---

## 3. Things that are invisible until you render

A checklist for "why does the render not match the viewport".

- **`ob.hide_render = True`.** Shows in the viewport, excluded from every render. A pendant light rendered as a bare wire frame for hours because the woven shade mesh carried it. Sweep for it:
  ```python
  [o.name for o in bpy.data.objects if o.hide_render]
  ```
- **`ob.visible_camera` / `visible_shadow` / `visible_diffuse` / `visible_glossy` / `visible_transmission` / `visible_volume_scatter`.** Cycles per-ray visibility. An object can exist, cast shadows, and be invisible to camera.
- **Viewport vs render subdivision.** `modifier.levels` is the viewport, `modifier.render_levels` is the render. And `modifier.show_render` can be off while `show_viewport` is on.
- **`scene.render.use_simplify` with `simplify_subdivision_render`.** Silently flattens everything.
- **Collection `hide_render` and the view-layer `exclude` checkbox** — different flags, both fatal, neither on the object.
- **Missing UVs.** Geometry built from raw vertices has no UV layer, so image textures collapse to flat colour. A floor reads as mud. Add a UV layer before assigning an image material.
- **Material slots shared between meshes.** Retinting "the whole asset" repaints marble and cast iron together if they share a mesh. Work per material, never per object.

---

## 4. The MCP server

### What is actually installed

The official server is `projects.blender.org/lab/blender_mcp`. Registered in `~/.claude.json` as:

```json
"blender": {"type":"stdio","command":"uv",
  "args":["--directory","$HOME/blender_mcp/mcp","run","blender-mcp"],"env":{}}
```

The Blender-side add-on ships separately as `mcp-<version>.zip` and installs to
`~/Library/Application Support/Blender/<ver>/extensions/user_default/mcp`.
Server and add-on versions must match. Verify with a `diff -rq` of the installed
add-on against the release zip, ignoring `__pycache__`.

Bundled reference docs, worth grepping before trusting memory of the `bpy` API:

```
$HOME/blender_mcp/mcp/blmcp/data/api      ~2,000 .rst
$HOME/blender_mcp/mcp/blmcp/data/manual   ~2,200 .rst
```

`blender.org/lab/mcp-server` is behind Cloudflare and returns 403 to most fetchers. The wiki is a git repo and is wide open — `git clone https://projects.blender.org/lab/blender_mcp.wiki.git` — as is the Gitea JSON API at `projects.blender.org/api/v1/repos/lab/blender_mcp/{releases,tags,issues}`.

### Use the dedicated tools; `execute_blender_code` is a last resort

The server injects this at connect, and it is easy to ignore for a whole session:

> The `execute_blender_code` tool is a last resort, if there are other tools that provide the functionality you need, use those instead.

Reach first for `get_objects_summary`, `get_object_detail_summary`,
`get_blendfile_summary_*`, `render_viewport_to_path`, `render_thumbnail_to_path`,
`get_screenshot_of_window_as_image`, `search_api_docs`, `search_manual_docs`,
`jump_to_view3d_object_by_name`.

Inside `execute_blender_code`: prefer `bpy.ops` for standard actions (they handle context and defaults), `bpy.data` for precision and to avoid side effects. **Return a JSON-serialisable dict assigned to `result`** — not print output.

The sandbox is guidance, not containment. It blocks exactly four operators
(`wm.quit_blender`, `wm.read_factory_settings`, `wm.read_factory_userpref`, `wm.read_userpref`).
`save_mainfile`, `open_mainfile` and `revert_mainfile` are **not** blocked. You can destroy the user's work with a typo.

### The limits, none of which are documented on the website

| Limit | Value | Source |
|---|---|---|
| MCP→add-on socket timeout | 300 s | `blmcp/tools_helpers/connection.py` |
| Max request | 10 MiB | `blender_mcp_addon/mcp_to_blender_server.py` |
| Deferred job wall-clock | 3600 s | `blender_mcp_addon/deferred_tool.py` |
| CLI subprocess (`*_for_cli`) | 120 s | `blmcp/tools_helpers/blender_cli.py` |
| Screenshot payload | 1 MiB − 2 KiB, ×3/4 for base64 | screenshot toolcode |
| Claude Code's own tool timeout | `MCP_TOOL_TIMEOUT` in `~/.claude/settings.json` | typically 120 s |

**There is no response-size limit, and that absence is a bug.** See below.

---

## 5. `Empty response from Blender` — a silent truncation, not your code

The most expensive failure mode in this stack, because it looks like a runtime error and is actually a size ceiling.

The add-on sets the client socket non-blocking, then calls `sendall` on it inside `except OSError: pass`. `BlockingIOError` subclasses `OSError`. Once the kernel send buffer fills (macOS `net.inet.tcp.sendspace` = 131072) the exception is swallowed, the connection closes before the terminating null byte, and the client reports:

- zero bytes → `Empty response from Blender`
- partial → `Invalid response … Unterminated string starting at: line 1 column …`

Measured: 260 KB delivered, 500 KB gone. An upstream issue measured the cut at ~327 KB (5 × 65536). Known and open; a two-line fix exists (`setblocking(True)` around the `sendall`, restored in a `finally`), needing an add-on reinstall and a Blender restart.

**What this means for you.** A large result comes back *empty rather than erroring*. That is the "instrument fails quietly" class. So:

- Page every response. Return counts plus a slice, never the full set.
- Aggregate in Blender, not in the transcript. Reduce 9,000 instances to a dozen rows before returning.
- For genuinely large data, write JSON to `bpy.app.tempdir` and return the path. Read the file from the shell.
- Never conclude "the scene has nothing" from an empty result. Re-run smaller first.

### Long operations: `check_is_finished`

A sweep that takes minutes will blow the client timeout. The sanctioned path is deferred completion, and you trigger it purely by **defining a function called `check_is_finished` at module level** in the code you send. The add-on looks it up after `exec` and, if callable, hands off to the deferred poller instead of replying.

Contract:
- return `None` → still working, keep polling
- return a `dict` → done; wrapped as `{"status":"ok","result":<dict>}` and sent
- anything else → error

It is polled on `bpy.app.timers` (0.05 s active, backing off to 1.0 s idle) **on the main thread**, so each call must be cheap or the UI stalls. Rejected in `--background` mode. Ceiling 3600 s.

Shape:

```python
import bpy
_state = {"i": 0, "rows": [], "done": False}

def _step():
    # do a small slice of work, advance _state["i"], set done when finished
    ...

def check_is_finished():
    if not _state["done"]:
        _step()
        return None
    return {"rows": _state["rows"][:40], "total": len(_state["rows"])}
```

---

The server-specific behaviours below describe the implementation this guidance was derived from, not a guarantee about every release. Record the installed Blender version and MCP server version or source revision at invocation; inspect the relevant implementation when it differs or cannot be identified.

## 6. The render tools mutate the live file

`render_viewport_to_path` sets `render.filepath`. `render_thumbnail_to_path` also
overwrites resolution, `use_simplify`, `simplify_subdivision_render` and sample count.

Both restore **only** through the deferred checker, and the poller drops a
disconnected client *without running the check function*. So a render outliving the
client timeout leaves the temporary settings in the scene. Save after that and the
damage is written into the user's file. The maintainer's own words: *"Saving while
rendering will then save using the temporary settings."*

**Therefore:**

1. Inspect the selected tool and engine, then snapshot every property it changes **before** rendering. Include `scene.render.filepath`, `resolution_percentage`, `resolution_x`, `resolution_y`, `use_simplify`, `simplify_subdivision_render`, and the active engine's sample and denoising settings (for Cycles, `scene.cycles.samples` and `scene.cycles.use_denoising`). Verify property paths against the installed Blender version.
2. Restore the complete snapshot explicitly after completion, error or disconnect, and compare every value before saving. Do not rely on the tool. If the connection prevents restoration, report the altered state and do not save the scene.
3. Never leave `render.filepath` pointing at a scratch directory — it will be saved into the file and the directory will later vanish.
4. Long renders go headless. Not through the MCP.

`*_for_cli` variants: **do not call them.** They pass no `stdin`, so the child Blender inherits the MCP client's live JSON-RPC pipe and deadlocks, timing out at 120 s. They cannot corrupt the source file — `synced_blend_for_cli` writes a `copy=True` snapshot — but they leave a stray numbered `<name>_mcp_0001.blend` beside it and return nothing. Run `blender -b` from the shell instead.

---

## 7. Working in someone's live session

The user is looking at this. Treat their viewport as their document.

- **Never reload the file to make a change.** `bpy.ops.wm.open_mainfile` resets their view. Edit the live session through the MCP instead. If you genuinely must reload, capture and restore `view_perspective`, `view_distance`, `view_location`, `view_rotation`, `lens` and `shading` from `screen.areas` → `VIEW_3D` → `region_3d`.
- **Check `bpy.data.is_dirty` before touching anything.** Dirty means unsaved edits in progress. Stop.
- **Say which paths you own** before writing, and get off the connection entirely when the user says they are editing. Idle, the setup touches nothing; every risk needs a deliberate call.
- **One source of truth, one file.** A capture/replay layer that records and reapplies arrangements will destroy hand placement — it did, repeatedly. Anchors get captured while child transforms do not; a name-match breaks when a fresh append drops its `.001` suffix; asset wrappers get deleted and orphan every child. Delete the layer. The `.blend` is the truth.
- **Guard against stray scene files.** Copies accumulate (`.blend1` backups, rescue copies) and each is a file someone can open by mistake and arrange for an hour. Keep exactly one `.blend` in the working directory; put snapshots in a separate `locked/` directory.

### Asset structure

Downloaded assets (BlenderKit and similar) wrap their contents in a structural
**empty**. A mesh-only filter deletes the wrapper and orphans every child. When
removing or moving an asset, walk to the root:

```python
def root(ob):
    while ob.parent is not None:
        ob = ob.parent
    return ob
```

Move the root's `matrix_world.translation`, not the child's `location` — `location` is in parent space and will surprise you.

---

## 8. Render passes and recolouring without re-rendering

The reason to decompose at all: paint applied to an 8-bit render multiplies onto pixels that are already clipped, so the sunlit part of a wall has been flattened to white and there is nothing left to tint. Everything upstream of the tone map must stay float.

### The identity

Cycles composes a diffuse surface as

```
combined = diffuse_colour × (diffuse_direct + diffuse_indirect) + rest
```

The lighting terms are **already divided by the diffuse colour**. So swapping paint replaces a factor rather than multiplying by a second one:

```
out = mix(albedo, paint, mask) × light + rest
```

Verify the decomposition before trusting anything built on it: recolour back to the grey the scene was rendered at and difference against the beauty pass. The floor is half-float storage precision. A mean relative error around 2.5e-4 is right; anything larger means the passes are wired wrong.

### Two methods, different costs

| | renders | gets right | gets wrong |
|---|---|---|---|
| **passes** | 1 | the surface's own reflectance, exactly | light bouncing *off* it onto the room still carries the grey it was traced with, so a bright paint comes out too dark |
| **basis** | 4 (black + unit R, G, B) | first-order inter-reflection, including the surface lighting itself | second-order bounces |

Light transport is linear in albedo, so
`L(c) = L(0) + c_r(L(R) − L(0)) + c_g(L(G) − L(0)) + c_b(L(B) − L(0))`.
Same four images on the wire; the shader becomes three multiply-adds.

### Scoring it honestly

**Do not use per-pixel relative error.** It divides by a number approaching zero in every shadowed corner, so a negligible absolute miss in a dark pixel reports as hundreds of percent and swamps the mean. Scored that way the better method looked three times worse. Use **absolute luminance error reported against the mean luminance of the region**.

**Refuse on a resolution mismatch.** A basis at 420×280 compared against passes at 480×320 reads pixels at unrelated positions and returns a plausible 52.8% where the honest answer was a few percent. It does not error and does not look wrong.

**p90/p10 is not a contrast measure.** It is near scale-invariant and will barely move across experiments that changed things substantially.

### Getting passes out

- Render layer sockets are spelled in full: `"Diffuse Direct"`, not `"DiffDir"`.
- Multilayer EXR is gated behind `image_settings.media_type`.
- `ID Mask` takes its index on an **input socket**.
- File Output uses `directory` plus `file_output_items.new(type, name)`.
- The compositor tree is `scene.compositing_node_group`.
- Object pass indices → `ID Mask` → RGBA coverage mattes, four material regions per texture.
- For a basis, hold **seed and sampling constant** across the four renders and turn denoising off — a denoiser's bias shows up as a fixed offset in a differenced result.
- Write `Linear Rec.709`, view transform `Standard`, look `None`, exposure 0.

### Getting them into a browser

A browser cannot read OpenEXR and an 8-bit intermediate clips exactly the highlights the exercise exists to preserve. Pack **half-float** and upload straight into WebGL2:

```js
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA16F, w, h, 0, gl.RGBA, gl.HALF_FLOAT, new Uint16Array(bytes));
gl.getExtension("OES_texture_float_linear");  // filtering needs it; without it every sampler returns black
```

Gzip the raw `.f16` and decompress with `DecompressionStream("gzip")`.

**Row order is a trap.** Blender hands back pixel rows bottom-up. If the packer reverses them, the file is top-down and the shader must flip `v`. Both halves have to agree; a stale pack with only one of them stands the room on its ceiling.

---

## 9. Gates that are blind by construction

- **A gate measuring what a material region *claims* is blind to a region claiming nothing.** A check that skips regions under 100 px (reasonably — percentiles of a sliver are meaningless) will pass a cornice reduced to 0 px. Two mechanisms are needed and both must stay: a `SURVIVES` check catching a *declared* region reduced to nothing, and an `unclaimed` mask catching a region no material ever declared.
- **Before judging an image, prove the image could have shown the defect.** A boundary fault is invisible when both sides are close in tone, and harmonious schemes hide exactly that class. Assert the separation — median rendered luminance of both adjacent regions — and refuse below a threshold. A hostile crop that is not actually hostile is worse than no crop.
- **`$?` after a pipe reports the last command's status**, not the one you care about.
- **Never suppress stderr in a driver script.** A whole screen recording shipped dead because every interaction silently failed into `/dev/null`.

---

## 10. Sun and sky

- Blender 5.x sky is `MULTIPLE_SCATTERING` (was `NISHITA`), with `aerosol_density`.
- For a real sun position use the NOAA algorithm, and mind the branch: NOAA's `arccos` is measured from south, and which side of the meridian you are on decides the sign.
  ```python
  azimuth = (azimuth + 180.0) if hour_angle > 0.0 else (540.0 - azimuth)
  ```
  Verify against published sunrise/sunset for the site and date before building on it.
- **"A crisp shadow in every state" is geometrically impossible with one window.** The sun sweeps ~152° of azimuth between morning and evening; a wall accepts a beam across ~90°. Say so rather than chasing it.
- Closed curtains cancel a sunbeam entirely. Separating the panels took a sunlit fraction from 2.2% to 7.3%.
- Blown windows read as mirrors. Check the exterior actually carries detail rather than clipping to white.

---

## 11. Headless

```bash
blender -b scene.blend --factory-startup --python script.py -- --arg value
```

- `--factory-startup` keeps user add-ons and preferences out of it. Reproducible.
- Everything after the bare `--` is yours: `sys.argv[sys.argv.index("--") + 1:]`.
- Run it as a properly detached background task. `nohup … &` inside a wrapper that then exits will have its child killed — a render can die after "Read blend" with an exit code of 0 and no output at all. Check for output files, not the exit code.
- `bpy.ops.render.render(write_still=True)` after setting `scene.render.filepath`.
- Blender's Python can open EXRs (`bpy.data.images.load`), which makes it the right place to score passes even when no rendering is involved.

---

## 12. Delegating this

A subagent driving Blender needs, in its brief: which file is the source of truth, whether the user is editing it right now, that it must open every render it makes, that it must page MCP responses, and which paths it owns. Without the "open the render" instruction it will report coordinates and be wrong.

Escalate to a Fable subagent for genuine judgement calls — composition, whether a scene reads as designed rather than assembled, whether a measured difference matters. Not for mechanics.
