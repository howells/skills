# Browser session

## Fallback order

Use the browser or tab the user names, and any browser rules the host sets. Otherwise take the first available:

| Option | Notes |
| --- | --- |
| Playwriter (MCP, skill or `playwriter` CLI) | Drives the user's own Chrome: signed-in, bot-protected and localhost pages render as the user sees them, and the user can watch. |
| Codex Browser plugin or in-app browser | Good for localhost, file URLs and current-tab testing. |
| Claude desktop in-app browser | When it supports navigation, interaction and screenshots. |
| Chrome MCP | Claude Code CLI with a real Chrome connection. |
| agent-browser | When installed and the host permits it. |
| Computer use driving a visible browser | Pixels only: console, network, DOM and accessibility checks are not run. |
| None | Static inspection, labelled not browser-verified. |

If the host loads tools lazily, search for browser tools before going static. Recording support varies; check the tool's help rather than assuming a command exists.

## Playwriter

Check for a Playwriter MCP or skill the host lists, then `command -v playwriter`. Don't install it unasked.

- Read the installed docs first (the Playwriter skill, MCP tool descriptions or `playwriter skill`): they define its selectors, timeouts and helpers.
- Create your own session (`playwriter session new`) and tab (`context.newPage()`). Leave the user's tabs alone unless they point you at one.
- Use `snapshot({ page })` to find controls and `getLatestLogs({ page, sinceLastCall: true })` for console failures. Screenshot with absolute paths, only when layout is the question.
- Resize with `page.setViewportSize()` and restore it afterwards: the tab sits in the user's own window.
- If the extension is not connected or no tab has Playwriter enabled, ask the user once to click the Playwriter icon and wait. Don't switch browsers for signed-in or user-visible pages.
- For a throwaway run the user needn't see, use a headless session where offered (`playwriter session new --browser headless`).
- Its recorder captures the user's actions, not yours; treat recording your own flow as unavailable unless the docs say otherwise.
- Close your tab and session when done, unless the user wants to inspect the result.

## Dev server

- Resolve the URL from the root `package.json` (follow `scripts.dev` into a workspace if it delegates), URL and port keys in `.env*`, and framework config. Prefer the URL the server prints over a framework default.
- Start one only when the command is clearly local. Ask before `dev:all`, multi-service scripts or anything production-backed.
- A listening port may belong to a peer or another checkout. Confirm the loaded app is the target; start your own on a free port rather than stopping theirs.
- Stop only a server you started, once it is no longer needed. Never kill a process because it holds a port.
