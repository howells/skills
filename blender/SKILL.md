---
name: blender
description: "Inspect, edit and render Blender scenes and films through the Blender MCP or headless CLI. Use for any .blend, render or Blender MCP task. Not for 2D design files (`paste-up`)."
---

# Blender

Two ways in, and they are not interchangeable:

- **Live MCP**: an add-on inside the user's running Blender. Their viewport, their unsaved edits, their file. Use it for inspection and for edits the user asked for in the open scene.
- **Headless**: `blender --factory-startup -b file.blend --python script.py -- args`. Its own process, nothing shared. Renders, long sweeps and batch work go here, on an explicit copy.

Never replace the user's open file with a headless result without reconciling their live edits.

## Rules

1. **Open the render before saying anything about it.** Read the actual PNG, then say what you see. Every serious failure here has the same shape: a measurement passes, a confident report goes out, and the defect is plainly visible on screen. Canonical case: a containment test cleared eight plants of a room; the render showed the room full of them. The test read base vertices; particle instancing put 9,225 instances inside.
2. **Measure evaluated geometry and instances, never `ob.data` or raw `bound_box`** (code below). A scene reporting 86 objects can be 9,000 instances.
3. **Fail the script, don't print the number.** A check that matters raises (`raise SystemExit("REFUSING: ...")`); a printed value gets rationalised.
4. **The MCP sandbox does not protect the file.** It blocks only quit and factory/userpref resets. `save_mainfile`, `open_mainfile` and `revert_mainfile` run. Don't save, open, revert or reload the user's file unless asked.
5. **The MCP render tools rewrite scene settings and may not restore them.** `render_viewport_to_path` sets `render.filepath`; `render_thumbnail_to_path` also changes resolution, simplify and samples. Restoration only runs if the client is still connected. Snapshot those properties before rendering, restore them yourself, compare before any save, and if you can't restore, say so and don't save. Never leave `render.filepath` pointing at a scratch directory.
6. **Never call the `*_for_cli` MCP tools.** They deadlock on the MCP pipe, time out at 120 s, return nothing and leave a stray `<name>_mcp_0001.blend`. Run `blender -b` from the shell. To snapshot the open scene: `bpy.ops.wm.save_as_mainfile(filepath=abs_path, copy=True)`, then confirm `bpy.data.filepath` is unchanged.
7. **Page every MCP response.** Above roughly 260–330 KB the add-on silently truncates: you get `Empty response from Blender` or `Unterminated string`, not an error about size. Return counts plus a slice, aggregate inside Blender, or write JSON to `bpy.app.tempdir` and return the path. Never conclude "the scene has nothing" from an empty result.
8. **Long renders go headless**, not through the MCP.

Prefer the dedicated MCP tools (`get_objects_summary`, `get_object_detail_summary`, `get_blendfile_summary_*`, `render_*_to_path`, `get_screenshot_of_window_as_image`, `search_api_docs`) over `execute_blender_code`. Inside it, assign a JSON-serialisable dict to `result`.

Read [references/mcp-server.md](references/mcp-server.md) when installing or debugging the server, hitting a timeout, or running an operation that takes minutes (the `check_is_finished` deferred contract).

## Measuring

```python
dg = bpy.context.evaluated_depsgraph_get()
ev = ob.evaluated_get(dg)
cs = [ev.matrix_world @ Vector(c) for c in ev.bound_box]   # covers modifiers, not instances

for inst in dg.object_instances:                            # particles, collection instances, GN points
    o = inst.object
    if o is None or o.type != "MESH" or o.hide_render:
        continue
    cs = [inst.matrix_world @ Vector(c) for c in o.bound_box]   # inst.is_instance, inst.parent = emitter
```

- **Test overlap, not containment.** Containment reports "outside" for an object half-buried in a wall, which is the case you are hunting: `hi[i] > lo_room[i] and lo[i] < hi_room[i]` on all three axes.
- **A bbox is conservative.** Clearing it proves no penetration; crossing it does not prove penetration. Say which you mean. Clearance is enforced by position, not collision, so re-run the sweep after adding assets.

## Invisible until you render

When the render doesn't match the viewport, check:

- `ob.hide_render` (a hidden shade mesh leaves a pendant as a bare wire), collection `hide_render`, and the view-layer `exclude` checkbox: three separate flags.
- Cycles per-ray visibility: `visible_camera`, `visible_shadow`, `visible_diffuse`, `visible_glossy`, `visible_transmission`, `visible_volume_scatter`.
- Modifier `render_levels` vs `levels`, and `show_render` vs `show_viewport`.
- `scene.render.use_simplify` with `simplify_subdivision_render`.
- Missing UVs: raw-vertex geometry has none, so image textures collapse to flat colour.
- Shared materials: recolouring "the asset" repaints marble and cast iron together. Work per material.
- Blown windows read as mirrors; check the exterior carries detail.

## The user's live session

- Don't reload to make a change; `open_mainfile` resets their view. If you must, capture and restore `view_perspective`, `view_distance`, `view_location`, `view_rotation`, `lens` and `shading` from the `VIEW_3D` region.
- `bpy.data.is_dirty` can mean their edits or yours. Don't discard or save either just to clear it.
- Say which paths you own before writing. Get off the connection when the user says they are editing.
- Keep one authoritative file per role; label snapshots, candidates and rendered evidence so a stray `.blend1` or rescue copy is never mistaken for the current scene.
- Downloaded assets (BlenderKit and similar) sit under a structural empty. A mesh-only filter orphans the children. Walk to the root (`while ob.parent: ob = ob.parent`) and move the root's `matrix_world.translation`; a child's `location` is in parent space.

## Sun and sky

- Blender 5.x sky is `MULTIPLE_SCATTERING` (was `NISHITA`), with `aerosol_density`.
- For a real sun position use NOAA, minding the branch: `azimuth = (azimuth + 180.0) if hour_angle > 0.0 else (540.0 - azimuth)`. Check against published sunrise/sunset for the site and date.
- A crisp sunbeam in every state is impossible with one window: the sun sweeps ~152° of azimuth, a wall accepts ~90°. Say so rather than chase it.
- Closed curtains cancel a beam; separating the panels took a sunlit fraction from 2.2% to 7.3%.

## Headless

- `--factory-startup` ignores the user's prefs; set render device and settings in the script.
- Args after the bare `--`: `sys.argv[sys.argv.index("--") + 1:]`.
- Detach properly. `nohup … &` inside a wrapper that exits gets killed: a render can die after "Read blend" with exit code 0 and no output. Check for output files, not the exit code.
- `bpy.ops.render.render(write_still=True)` after setting `scene.render.filepath`.
- Blender's Python loads EXRs (`bpy.data.images.load`), so score passes there even when nothing renders.

## Deeper work

- Recolouring from render passes, basis renders, scoring image differences, or shipping float images to WebGL: read [references/recolouring.md](references/recolouring.md).
- Assembling several scenes into one film (clocks, camera, light, sound, resumable renders, delivery): read [references/film-production.md](references/film-production.md).
- Estimating a long render, or a render that feels slow: read [references/render-performance.md](references/render-performance.md) before lowering quality.

## Delegating

A helper driving Blender needs in its brief: the source-of-truth file, whether the user is editing it now, the paths it owns, that it must open every render it makes, and that it must page MCP responses. Without "open the render" it reports coordinates and is wrong.
