---
name: fieldtest
description: "Exercise a running web app in a real browser and return evidence-backed QA findings. Use for dogfooding, localhost review, mobile defects, console and accessibility checks, persona walkthroughs, or to try to break it with hostile content, slow networks and rapid input. Report-only unless asked. Not for code-only review, building UI (`chiaroscuro`) or fixing layout (`reflow`)."
---

# Fieldtest

Evaluate the app as rendered software. Every finding rests on browser evidence: route, viewport, interaction, console and network signal, screenshot or recording, and reproduction steps. Say you are using `fieldtest`.

## Hard rules

- **Report only.** Fix only when the user asks.
- **Use a browser.** Do not satisfy a field test with shell checks or source reading when a browser is available. Static-only results are labelled "not browser-verified", and the completion check is not claimed.
- **Check where a write lands before making one.** `localhost` names the frontend, not its database, storage, accounts or email. Resolve the effective destinations from config and runtime, inspect only the settings needed, redact credentials, and prefer a disposable target. An unknown destination is unverified. Permission to browse is not permission to seed data or write remotely; apply the host's approval rules to the real destination.
- **Destructive or external actions** (payments, emails, orders, publishing, deletes, production changes) need explicit authorisation for that action. Ask if it is missing.
- **Never report a number from the wrong page or size.** See Measurement discipline.

## Browser

Honour the user's and host's browser choice. Otherwise use Playwriter when available: it drives the user's own Chrome, so signed-in and localhost pages render as the user sees them. If it is absent, use the strongest other browser. Read `references/browser-session.md` before the first command: it holds the fallback table, Playwriter session rules, dev URL detection, persona checks and the severity guide.

## Run

1. **Mode**: report-only QA, QA plus fixes, focused route or regression, responsive or mobile audit, persona walkthrough, or stress test.
2. **Context scan.** Read `package.json` (and the delegated workspace's), framework and route files, `git log --oneline -10`, `git status --short`, product docs and `AGENTS.md`. For `.env*`, read only URL and port keys; never quote secrets. Pin a summary: intent, primary flows, stack, dev URL, backing targets and permitted effects, routes in scope, lens.
3. **URL.** Use the one given, else detect it (see `references/browser-session.md`). Start a dev server only if the right command is clear, local and non-mutating, never `dev:all` or a production-backed script. If several apps or commands fit, ask one question.
4. **Load** the page and confirm it is the target. Check the console and failed requests.
5. **Capture the first impression** before interacting.
6. **Exercise the primary flow.**
7. **Trigger one empty, invalid, loading or error state** when safe.
8. **Visit nearby and secondary routes.**
9. **Check mobile (~375px) and desktop (~1440px)** for broad or visual tasks.
10. **Check keyboard and accessible names** on primary controls.
11. **Async flows**: start A, then B before A completes. A late response must not replace B, and an unrelated update must not replay A or clear a current error.
12. **Embedded apps**: test in the real host. A standalone demo covers only itself; report each separately.
13. **Record** a ~30s clip of the primary flow on a full test if the tool supports it. A reader should be able to verify the finding from the clip alone. Skip when it cannot record.

A focused regression covers the affected route and one adjacent state.

### Try to break it

Read `references/stress-test.md` when the user asks to stress-test, break or find edge cases, or a full test touches forms, lists or async flows. It holds the hostile content set, abuse and network cases, environment extremes and report rows.

### Judge returned content

Read `references/output-quality.md` when the page returns images, search results, generated content or a collection of examples, or the user says to inspect every one. A working control does not make its output useful.

## Measurement discipline

Each rule here is a measurement that once returned a confident wrong number.

- **Assert the viewport and URL before every measurement.** Read back `innerWidth+"x"+innerHeight` and `location.href`. If either is wrong, reset and retry; never report a number from the wrong size or page.
- **Let the instrument find the defect.** A check aimed where you already expect the answer cannot disconfirm you. State beforehand what result would have.
- **Prove the capture could show the defect.** Two areas close in tone prove nothing about their boundary. Check the precondition (contrast, state, data present); refuse the capture if it fails.
- **Pair every "declared thing is right" check with a "nothing left undeclared" check.** A gate on what a page declares is blind to a page declaring nothing.
- **Wait for the end state, not the first appearance.** Wait on the condition that means finished, not on an element appearing or a fixed sleep.
- **A synthetic click is not a tap.** Programmatic clicks bypass hit-testing, pointer-events and overlays. Use the tool's real click and assert the intended change.
- **Put thresholds in the driver script, not in your head.** A value you read can be rationalised; one you refuse on can be trusted.

## Lenses

Use the user's persona, else pick one. Questions for each are in `references/browser-session.md`.

- **First-time user**: clarity, orientation, next step, error recovery.
- **Designer**: hierarchy, spacing, type, interaction quality.
- **Operator**: repeated work, density, tables, filters, bulk actions.
- **Demo presenter**: narrative, reliability, hazards mid-walkthrough.
- **Responsive auditor**: fit, overflow, target sizes, sticky overlap.

Findings still need evidence and impact; no taste commentary.

## Findings

Report only what browser evidence supports. Fewer, better findings beat a long list. Lead with findings; keep praise short. Each finding has: severity, route or screen, what happened, why it matters, reproduction steps, evidence (path, console message, network status or visible state), likely cause when code supports it, and a suggested fix. If nothing meaningful turned up, say so and list what was tested.

## Fix mode

When asked to fix: reproduce in the browser, inspect the smallest relevant code path, make scoped edits, run the relevant checks, re-test in the browser. Capture before and after clips when the tool can record. Do not fix what was not reproduced.

## Output

```markdown
## Fieldtest Report

Target: [URL]
Mode: [report-only QA | QA plus fixes | focused check | responsive audit | persona walkthrough | stress test]
Lens: [persona or lens]
Browser: [tool | static inspection only, not browser-verified]
Viewports: [sizes tested]
Recordings: [paths, or none]

## Findings
### High
### Medium
### Low

## What Was Tested
## Residual Risk
```

A focused check is shorter but keeps target, steps and result. A stress test adds the Stress table from `references/stress-test.md`.

## Completion check

- The app loaded in a browser; the URL and viewports are named.
- Console and network were checked where the tool allowed.
- Findings carry reproduction steps or concrete evidence.
- Collection coverage names the inspected cases and the omissions; loaded or captured does not count as visually inspected.
- No destructive flow ran without confirmation.
- Fixes were re-tested in the browser.
- Recordings were captured, or their absence is stated.
