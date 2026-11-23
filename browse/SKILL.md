---
name: browse
description: Drive the user's real Chromium browser, with its logins, tabs and extensions, through the browse extension and MCP server. Use for logged-in or JS-heavy sites, forms, screenshots, demo videos and recordings, HAR capture, and handing logins, 2FA or payments back to the user. Not for QA reports (`fieldtest`) or native Mac apps (`computer-use`).
---

# browse

[browse](https://opencode.ai/product/browse) runs Playwright-style code in the user's own Chrome, Arc, Brave, Edge or other Chromium browser through its extension.

## Reference

The installed CLI is the source of truth: `browse --help`, `browse tools`, and `browse <tool> --help` for each tool's options. Read the help for a tool before its first use in a session.

## Use the MCP tools

Prefer the browse MCP server's tools (`execute`, `tabs`, `status`, `recording`, `network`). Load them first if the agent defers tool schemas. The `browse` CLI has the same commands; use it only when the MCP server is not configured for this agent.

Open each tab with a chosen `id` (`tabs` action `new`, `id: "work-mail"`) and pass that id as `tab` everywhere. Some harnesses send a numeric tab id as a string, which `execute` rejects.

```js
await page.goto("https://example.com");
return await snapshot();
```

Inside `execute`, `page.mouse.down()`/`up()` are unsupported: drag with `browse.drag({ from, to, steps })`.

This is the user's own browser profile. Undo what you change on their sites (local storage, carts, drafts, boards) once the task is done, and close the tabs you opened.

## Demo videos

When the task is a screen recording of something being used, read [`references/demo-recording.md`](references/demo-recording.md) before the first take. The recorder captures no pointer and freezes animation in background tabs; that file has the cursor overlay, the tab setup and the encode step.

## When it fails

Run `browse status` and follow its `nextStep`. If an execute fails with "Running relay does not report a build id", an older relay is still running after an install or update: `browse restart` fixes it and keeps agent tabs open.
