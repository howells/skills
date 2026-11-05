# Browser Session Reference

Browser setup, persona checks and severity for a rendered app QA session.

Contents: Browser Tool Selection · Playwriter Sessions · Dev URL Detection · Persona Checks · Evidence · Report Tone

## Browser Tool Selection

Honour the browser or tab the user specifies, and any browser rules the live host sets. Otherwise, when Playwriter is available, use it first; fall back down the table only when it is not:

| Environment | Preferred browser path | Notes |
| --- | --- | --- |
| Playwriter MCP, skill or `playwriter` CLI available | Playwriter | Default whenever available. Drives the user's own Chrome, so signed-in, bot-protected and localhost pages render as the user sees them and the user can watch. See Playwriter Sessions below. |
| Codex desktop or Codex with Browser plugin | Browser plugin / Codex in-app browser | Preferred for local targets, localhost apps, file URLs, screenshots, and current-tab testing. |
| Claude desktop with in-app browser | Claude desktop in-app browser | Use when it supports navigation, interaction, inspection, and screenshots. |
| Claude Code CLI with Chrome MCP | Chrome MCP | Strong default for CLI sessions with a real Chrome connection. |
| Host with agent-browser installed | agent-browser | Use when it fits the task and the host permits it; inspect current help for recording support. |
| Only native computer use (Codex Computer Use, Claude computer use, or the `computer-use` skill) | Computer use driving a visible browser | Last resort before static inspection. It sees pixels only: mark console, network, DOM and accessibility checks as not run. |
| No browser-capable option | Static inspection only | Clearly say the result was not browser-verified. |

Recording support varies by tool. Inspect the available browser tool documentation or CLI help; do not assume a recording command exists. Static-only inspection cannot record.

If the host supports lazy tool discovery, search for Browser or browser MCP capabilities before falling back to static inspection.

## Playwriter Sessions

Check for a Playwriter MCP or skill the host lists, then `command -v playwriter`. Use whichever form the host exposes: the steps below say what to do, with the CLI command where the CLI is what you have. If none is found, move to the next row; do not install it unasked.

- Before the first command, read the installed version's docs in full: the Playwriter skill or MCP tool descriptions, or the output of `playwriter skill`. They document its selectors, timeouts and helpers.
- Create your own session (CLI: `playwriter session new`) and open your own tab with `context.newPage()`. Leave the user's existing tabs alone unless they point you at one.
- After every navigation or action, print the URL, `snapshot({ page })` and `getLatestLogs({ page, sinceLastCall: true })`. That covers the console check. Take screenshots with absolute paths, and only when layout is the question.
- Resize the viewport with `page.setViewportSize()` for the mobile and desktop checks, then restore it, because the tab sits in the user's own window.
- If Playwriter reports that the extension is not connected or no tab has Playwriter enabled, ask the user once to click the Playwriter extension icon, then wait for their reply. Do not silently fall back to another browser for signed-in or user-visible pages.
- For a throwaway run the user does not need to see, a headless session keeps the user's Chrome out of it where your Playwriter form offers one (CLI: `playwriter session new --browser headless`).
- Playwriter's recorder captures what the user does, not what you do. Treat recording your own flow as unavailable unless the installed docs say otherwise.
- Close your tab and delete your session when finished, unless the user wants to inspect the result.

## Dev URL Detection

Resolve the dev URL before asking the user when possible.

Read the root `package.json`. If `scripts.dev` delegates to a workspace, follow the command and read that workspace's `package.json`.

Check only URL/port-related keys in `.env`, `.env.local`, `.env.development`, framework config, and the leaf dev script. Never quote secrets or include unrelated environment values in reports.

Before starting a dev command, verify that it is local and non-mutating. Ask before running broad scripts such as `dev:all`, scripts that start multiple services, or scripts that appear to target production-backed services.

Identify the checkout, server owner, process/session and actual port before starting or reusing a server. A listening port may belong to a peer or another checkout. Reuse only a confirmed matching app; choose a free port for your own server rather than stopping somebody else's. Starting local rendering and authorising a test write are separate decisions: resolve effective backing targets before the latter, even when the server was already running.

Prefer the actual startup URL over an inferred default, since the configured port may be occupied or overridden. Confirm the loaded app is the target. Common patterns:

| Pattern | Example | URL |
| --- | --- | --- |
| `--port N` or `-p N` | `next dev --port 4310` | `http://localhost:4310` |
| `${PORT:-N}` | `next dev --port ${PORT:-26000}` | `http://localhost:26000` unless env overrides |
| inline `PORT=N` | `PORT=8080 vite` | `http://localhost:8080` |
| `.env*` `PORT=N` | `PORT=3005` | `http://localhost:3005` |
| Vite default | `vite` | `http://localhost:5173` |
| Astro default | `astro dev` | `http://localhost:4321` |
| SvelteKit default | `vite dev` | `http://localhost:5173` |
| Next default | `next dev` | `http://localhost:3000` |

If multiple URLs or apps are plausible, ask which app to field test.

## Persona Checks

### First-time User

- Can the user tell what this is within five seconds?
- Is there one obvious first action?
- Are labels outcome-based rather than mechanism-based?
- Does the app explain empty, loading, error, and success states?
- Can the user recover after a mistake?

### Designer

- Is visual hierarchy clear?
- Does spacing follow a system?
- Is typography doing distinct jobs?
- Are interaction states designed?
- Is the page memorable for the right reason?
- Are colors, borders, shadows, and UI surfaces intentional?

### Operator

- Can repeated actions be done quickly?
- Are filters, tables, sorting, pagination, and statuses readable?
- Does dense information remain scannable?
- Are destructive or irreversible actions protected?
- Does state survive navigation when users expect it to?

### Demo Presenter

- Is the first screen safe and impressive?
- Can the presenter tell a coherent story in three minutes?
- Are there awkward waits, fragile inputs, or confusing transitions?
- Are demo data and empty states convincing?
- Is there a fallback path if a step fails?

### Responsive Auditor

- No horizontal overflow.
- Primary actions remain visible and reachable.
- Text does not overlap or clip.
- Tap targets are large enough.
- Sticky elements do not cover content.
- Dialogs, popovers, tables, and carousels adapt to narrow screens.

## Evidence

Use the best evidence available:

- screenshot path
- route and viewport
- console message
- network status
- visible state description
- DOM/accessibility snapshot
- exact reproduction steps

Avoid unsupported claims such as "feels broken" without naming what was visible or what happened.

## Report Tone

Lead with findings. Keep praise short. Do not bury serious issues in narrative.

Useful severity guide:

- **High**: blocks primary flow, causes data loss/security risk, or makes the app unusable on a key viewport.
- **Medium**: undermines comprehension, trust, conversion, accessibility, or repeated workflow efficiency.
- **Low**: polish issue, minor inconsistency, weak copy, or localized visual defect.

If you started a temporary dev server, record its process/session identity. Stop only that owned process when it is no longer needed; leave it running if the user needs to inspect the result. Never kill a process merely because it occupies a port.
