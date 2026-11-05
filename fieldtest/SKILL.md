---
name: fieldtest
description: "QA a running web app in a real browser and report evidence-backed findings. Use for dogfooding, localhost review, console and accessibility checks, persona walkthroughs, or trying to break it. Not for building UI (`chiaroscuro`) or fixing layout (`reflow`)."
---

# Fieldtest

Test the app as rendered software and report what the browser shows. Report only; fix when asked.

## Rules

- **Use a real browser.** Source reading and shell checks are not a field test. With no browser available, label the result "not browser-verified".
- **Don't write to real destinations unasked.** `localhost` is only the frontend; its database, storage, accounts, email and payments may be production. Before submitting, seeding or typing into autosaving fields, check from config where writes land, and prefer a disposable target. Payments, emails, orders, publishing, deletes and production changes need the user's go-ahead for that action.
- **Findings come from what rendered.** A break predicted from code or a schema is labelled inferred and goes under Residual risk.
- **Measure the intended page and viewport.** Read back `location.href`, `innerWidth` and `innerHeight` after navigating or resizing; a number from the wrong page or size is worse than none.
- **Use real clicks and wait for the end state.** Programmatic clicks skip hit-testing, pointer-events and overlays. An element appearing, or a fixed sleep, is not the flow finishing.
- **Aim checks so they could fail.** A boundary between two near-identical tones proves nothing, and checking what a page declares misses what it leaves undeclared.

## Browser

Use the browser the user or host names. Otherwise use Playwriter when available: it drives the user's own Chrome, so signed-in and localhost pages render as the user sees them. Read [references/browser-session.md](references/browser-session.md) before the first command for the fallback order, Playwriter session mechanics and dev-server rules. Read each reference file with its own command.

## Run

1. Learn the app: `package.json`, routes, `git log --oneline -10`, `AGENTS.md`. Read only URL and port keys from `.env*`.
2. Use the URL given, else find it (see `references/browser-session.md`). Ask if several apps fit.
3. Load the page, confirm it is the target, and check the console and failed requests. Note the first impression before interacting.
4. Exercise the primary flow, then one empty, invalid, loading or error state, then nearby routes.
5. For broad or visual work, check ~375px and ~1440px, plus keyboard focus and accessible names on primary controls.
6. Async flows: start A, then B before A completes. A late A must not overwrite B, replay, or clear a current error.
7. Embedded apps: test inside the real host. A standalone demo covers only itself.
8. Record the primary flow when the tool can record its own actions.

A focused regression covers the affected route and one adjacent state.

- **Try to break it**: before a stress test (asked to break it or find edge cases, or a full test that touches forms, lists or async flows), read [references/stress-test.md](references/stress-test.md).
- **Returned content**: before judging images, search results, generated content or a set of examples the page returns, read [references/output-quality.md](references/output-quality.md). A working control does not make its output useful.

## Lens

Use the user's persona, else pick one:

- **First-time user**: what is this, what do I do next, can I recover from a mistake.
- **Designer**: hierarchy, spacing, type, interaction states.
- **Operator**: repeated work, density, tables, filters, bulk actions.
- **Demo presenter**: a safe first screen, awkward waits, fragile steps.
- **Responsive auditor**: overflow, tap targets, sticky overlap, narrow dialogs and tables.

A lens shapes where you look; findings still need evidence.

## Report

Fewer, better findings, leading the report. Each has route, what happened, why it matters, reproduction steps, evidence (screenshot path, console message, network status or visible state), likely cause when the code shows it, and a fix.

- **High**: blocks the primary flow, loses data, risks security, or is unusable at a key viewport.
- **Medium**: hurts comprehension, trust, accessibility or repeated work.
- **Low**: polish, minor inconsistency, weak copy.

```markdown
## Fieldtest Report

Target: [URL]
Lens: [persona]
Browser: [tool | not browser-verified]
Viewports: [sizes]
Recordings: [paths, or none]

## Findings
### High
### Medium
### Low

## What Was Tested
## Residual Risk
```

If nothing meaningful turned up, say so and list what was tested. A stress test adds the Stress table from `references/stress-test.md`.

When asked to fix: reproduce first, change the smallest code path, and re-test in the browser. Don't fix what you could not reproduce.
