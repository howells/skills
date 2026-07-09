# Browser Session Reference

Use this reference when running a rendered app QA session.

## Browser Tool Selection

Pick the browser with the strongest fit for the active host:

| Environment | Preferred browser path | Notes |
| --- | --- | --- |
| Codex desktop or Codex with Browser plugin | Browser plugin / Codex in-app browser | Preferred for local targets, localhost apps, file URLs, screenshots, and current-tab testing. |
| Claude desktop with in-app browser | Claude desktop in-app browser | Use when it supports navigation, interaction, inspection, and screenshots. |
| Claude Code CLI with Chrome MCP | Chrome MCP | Strong default for CLI sessions with a real Chrome connection. |
| Any environment with no first-class browser | Playwright from terminal | Use for deterministic scripts, viewport checks, screenshots, console capture, and accessibility snapshots. If Playwright browsers are not provisioned, suggest `npx playwright install chromium`, or fall back to static inspection if installation is not permitted. |
| No browser-capable option | Static inspection only | Clearly say the result was not browser-verified. |

Use the strongest available browser tool before falling back. A field test should exercise rendered behavior, not just source code.

Recording support varies by rung: Claude-in-Chrome (`gif_creator`), agent-browser record, and Playwright video can capture a clip. Static-only inspection cannot record.

If the host supports lazy tool discovery, search for Browser or browser MCP capabilities before choosing Playwright.

## Dev URL Detection

Resolve the dev URL before asking the user when possible.

Read the root `package.json`. If `scripts.dev` delegates to a workspace, follow the command and read that workspace's `package.json`.

Check only URL/port-related keys in `.env`, `.env.local`, `.env.development`, framework config, and the leaf dev script. Never quote secrets or include unrelated environment values in reports.

Before starting a dev command, verify that it is local and non-mutating. Ask before running broad scripts such as `dev:all`, scripts that start multiple services, or scripts that appear to target production-backed services.

Common patterns:

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
| React Router default | `react-router dev` | `http://localhost:3000` |

If multiple URLs or apps are plausible, ask which app to field test.

## Minimum Session

For a broad app field test:

1. Load the target URL.
2. Record the browser tool, viewport, and route.
3. Inspect console errors.
4. Take or describe the initial rendered state.
5. Exercise the primary action.
6. Check one error or empty state.
7. Navigate to two adjacent routes.
8. Recheck at mobile width around `375px`.
9. Recheck at desktop width around `1440px`.

For a focused regression, test only the affected route and one adjacent state.

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
- Are colors, borders, shadows, and surfaces intentional?

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
