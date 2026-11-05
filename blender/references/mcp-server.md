# The Blender MCP server

Server behaviour below was read from the source of one release. When the installed version differs, check the named file before relying on it.

## Install and docs

The official server is `projects.blender.org/lab/blender_mcp`. Find the actual checkout from the harness MCP configuration. A stdio registration looks like:

```json
"blender": {"type":"stdio","command":"uv",
  "args":["--directory","/absolute/path/to/blender_mcp/mcp","run","blender-mcp"],"env":{}}
```

The Blender add-on ships separately as `mcp-<version>.zip` and installs to `~/Library/Application Support/Blender/<ver>/extensions/user_default/mcp`. Server and add-on versions must match; check with `diff -rq` of the installed add-on against the release zip, ignoring `__pycache__`.

Grep the bundled docs before trusting memory of `bpy`: `<checkout>/mcp/blmcp/data/api` (~2,000 .rst) and `<checkout>/mcp/blmcp/data/manual` (~2,200 .rst).

`blender.org/lab/mcp-server` returns 403 to most fetchers (Cloudflare). The wiki clones freely (`git clone https://projects.blender.org/lab/blender_mcp.wiki.git`), as does the Gitea API at `projects.blender.org/api/v1/repos/lab/blender_mcp/{releases,tags,issues}`.

## Limits (none documented on the website)

| Limit | Value | Source |
|---|---|---|
| MCP→add-on socket timeout | 300 s | `blmcp/tools_helpers/connection.py` |
| Max request | 10 MiB | `blender_mcp_addon/mcp_to_blender_server.py` |
| Deferred job wall-clock | 3600 s | `blender_mcp_addon/deferred_tool.py` |
| CLI subprocess (`*_for_cli`) | 120 s | `blmcp/tools_helpers/blender_cli.py` |
| Screenshot payload | 1 MiB − 2 KiB, ×3/4 for base64 | screenshot toolcode |
| Claude Code tool timeout | `MCP_TOOL_TIMEOUT` in `~/.claude/settings.json` | typically 120 s |

There is no response-size limit, and that absence is the bug below.

## `Empty response from Blender` is truncation

The add-on sets the client socket non-blocking, then calls `sendall` inside `except OSError: pass`. `BlockingIOError` subclasses `OSError`. Once the kernel send buffer fills (macOS `net.inet.tcp.sendspace` = 131072) the exception is swallowed and the connection closes before the terminating null byte:

- zero bytes → `Empty response from Blender`
- partial → `Invalid response … Unterminated string starting at: line 1 column …`

Measured: 260 KB delivered, 500 KB lost; an upstream issue puts the cut at ~327 KB (5 × 65536). The fix is two lines (`setblocking(True)` around the `sendall`, restored in a `finally`) plus an add-on reinstall and Blender restart. Propose it separately; don't patch the add-on during scene work unless the user asked for server maintenance.

## Long operations: `check_is_finished`

A sweep that takes minutes blows the client timeout. Define a module-level function named `check_is_finished` in the code you send; the add-on finds it after `exec` and hands off to its deferred poller instead of replying.

- returns `None` → still working, poll again
- returns a `dict` → done; sent as `{"status":"ok","result":<dict>}`
- anything else → error

It is polled on `bpy.app.timers` (0.05 s active, backing off to 1.0 s) on the main thread, so each call must be cheap or the UI stalls. Rejected in `--background`. Ceiling 3600 s.

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

## Why the render tools leave settings behind

Both `render_*_to_path` tools restore their temporary settings only through the deferred checker, and the poller drops a disconnected client without running it. A render that outlives the client timeout leaves the temporary settings in the scene; a later save writes them into the user's file. The maintainer: *"Saving while rendering will then save using the temporary settings."*

Snapshot before rendering: `scene.render.filepath`, `resolution_percentage`, `resolution_x`, `resolution_y`, `use_simplify`, `simplify_subdivision_render`, and the engine's sample and denoise settings (Cycles: `scene.cycles.samples`, `scene.cycles.use_denoising`).

## Why `*_for_cli` deadlocks

They pass no `stdin`, so the child Blender inherits the MCP client's live JSON-RPC pipe. They cannot corrupt the source (`synced_blend_for_cli` writes a `copy=True` snapshot), but they leave the numbered snapshot beside it and return nothing.
