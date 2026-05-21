---
name: fieldtest
description: Test a rendered web app in the browser with evidence-backed QA, UX, responsive, console, accessibility, and persona-based findings. Use when asked to dogfood an app, browse or experience a local web app, field test a feature, inspect UI behavior, validate a frontend change, check responsive/mobile issues, find rendered bugs, review a localhost app, or produce a practical browser QA report before shipping.
---

# Fieldtest

Use this skill to evaluate the app as rendered software, not just as code. The output should be grounded in browser evidence: routes visited, viewport sizes, interactions tried, console/network signals, screenshots when available, and reproducible findings.

## References

Load `references/browser-session.md` when running a full field test, resolving a dev URL, choosing a persona lens, or formatting a report.

## Start

When invoked:

1. State that you are using the `fieldtest` skill.
2. Determine the mode:
   - report-only QA
   - QA plus fixes
   - focused check of a route, feature, or regression
   - responsive/mobile audit
   - persona browsing
3. If the user did not specify a URL, detect the dev server from the codebase.
4. If the app is not running and the correct dev command is clear, start it only after confirming it is local, non-mutating, and not a broad `dev:all` or production-backed command. If multiple apps or commands are plausible, ask one concise question.
5. Choose the browser tool that best matches the host environment; do not default to a weaker browser path when a first-class local browser is available.

Default to report-only unless the user explicitly asks you to fix issues.

## Browser Tool Selection

Use the most capable browser available in the current environment:

- **Codex desktop / Codex with Browser plugin**: use the Browser plugin or Codex in-app browser for local targets such as `localhost`, `127.0.0.1`, `file://`, or the current in-app tab.
- **Claude desktop with an in-app browser**: use the desktop in-app browser when it can navigate, interact, inspect, and screenshot the target.
- **Claude Code CLI with Chrome MCP**: use Chrome MCP for navigation, screenshots, console messages, page text, and interaction.
- **No interactive browser tool available**: use Playwright from the terminal for scripted navigation, viewport checks, screenshots, console capture, and accessibility snapshots.
- **Last resort**: use static code inspection only if no browser-capable path exists, and clearly label the result as not browser-verified.

For local web apps, do not satisfy a field test with shell-only checks when a browser-capable tool is available. The point of the skill is rendered behavior.

If the environment supports lazy tool discovery, search for the Browser plugin or browser MCP before falling back to Playwright.

## Context Scan

Read enough codebase context to understand intent without auditing the whole repo:

- `package.json` and delegated workspace `package.json` files
- framework config such as `next.config.*`, `vite.config.*`, `astro.config.*`, or `playwright.config.*`
- route files such as `app/**/page.*`, `pages/**`, `src/routes/**`, or equivalent
- recent changes with `git log --oneline -10` and `git status --short`
- design, product, or brand docs when present
- app-specific instructions such as `AGENTS.md`

When reading `.env*` for port detection, inspect only the keys needed to resolve local URLs, such as `PORT`, `HOST`, or framework-specific dev-server variables. Do not quote or summarize secrets in the report.

Summarize this into a short pinned context:

- intent
- likely primary flows
- stack
- dev URL
- routes in scope
- persona or testing lens

Use the summary while browsing; do not keep raw file dumps in mind longer than needed.

## Browser Session

Work from evidence:

1. Open the target URL and confirm the page actually loaded.
2. Check console errors and obvious network failures.
3. Capture the first impression before interacting.
4. Exercise the primary flow.
5. Trigger at least one empty, invalid, loading, or error state when safe.
6. Navigate to nearby or important secondary routes.
7. Check responsive behavior at mobile and desktop widths when the task is broad or visual.
8. Check keyboard and accessible-name basics for primary controls.

For destructive actions, payments, emails, orders, publishing, or production mutations, stop and ask before executing.

## Persona Lenses

If the user gives a persona, use it. Otherwise choose the most relevant lens:

- **First-time user**: clarity, orientation, labels, next step, error recovery.
- **Designer**: hierarchy, spacing, typography, distinctiveness, interaction quality.
- **Operator**: repeated workflows, density, tables, filters, bulk actions, status clarity.
- **Demo presenter**: narrative, reliability, impressive moments, hazards during walkthroughs.
- **Responsive auditor**: mobile fit, overflow, target sizes, viewport-specific layout.

Do not turn persona browsing into vague taste commentary. Findings still need evidence and impact.

## Findings

Report findings only when they are supported by browser evidence. Prefer fewer, better findings over a long list of minor impressions.

Each finding should include:

- severity or priority
- route/screen
- what happened
- why it matters
- reproduction steps
- evidence, such as screenshot path, console message, network status, or visible state
- likely cause when code inspection supports it
- suggested fix

If there are no meaningful issues, say that clearly and mention what was tested.

## Fix Mode

When the user asks for fixes:

1. Reproduce the issue in the browser.
2. Inspect the smallest relevant code path.
3. Make scoped edits.
4. Run the relevant checks.
5. Re-test the route or flow in the browser.

Do not fix speculative issues that were not reproduced unless the user explicitly wants a code audit too.

## Output

For a full report, use:

```markdown
## Fieldtest Report

Target: [URL]
Mode: [report-only | QA plus fixes | focused route]
Lens: [persona/lens]
Viewports: [sizes tested]

## Findings

### High

### Medium

### Low

## What Was Tested

## Residual Risk
```

For a focused check, keep the output shorter but still include target, steps, and result.

## Completion Check

Before finishing, verify that:

- the app was actually loaded in a browser
- the tested URL and viewport sizes are named
- console/network issues were checked when tooling allowed
- findings include reproduction steps or concrete evidence
- destructive flows were not executed without confirmation
- fixes, if made, were re-tested in the browser
