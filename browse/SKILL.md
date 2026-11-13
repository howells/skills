---
name: browse
description: Drive the user's real Chromium browser, with its logins, tabs and extensions, through the browse extension and MCP server. Use for logged-in or JS-heavy sites, forms, screenshots, recordings, HAR capture, and handing logins, 2FA or payments back to the user. Not for QA reports (`fieldtest`) or native Mac apps (`computer-use`).
---

# browse

[browse](https://opencode.ai/product/browse) runs Playwright code in the user's own Chrome, Arc, Brave, Edge or other Chromium browser through its extension.

## Read the full reference (once per session)

Before the first browse call in a session, run:

```bash
browse skill
```

Read the whole output. Do not pipe it through `head` or `tail`. It ships with the installed version, so it stays current as browse updates.

## Use the MCP tools

Prefer the browse MCP server's tools (`execute`, `session_new`, `session_adopt`, `session_reset`, `network`, `recording`, `status`). Load them first if the agent defers tool schemas. The `browse` CLI has the same commands; use it only when the MCP server is not configured for this agent.

Minimal `execute` call:

```js
await page.goto("https://example.com")
return await snapshot()
```

When you finish, run `session_reset` on your own session.

## When it fails

Run `browse doctor`, then `browse status`. If an execute fails with "Running relay does not report a build id", an older relay is still running after an install or update. Tell the user that `browse relay restart` fixes it, and ask before running it, because restarting the relay detaches every agent's tabs.
