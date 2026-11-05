---
name: plimsoll
description: "Cut checks, CI watch loops and re-planning that crowd out shipping, and keep Vercel builds on the user's machine. Use near a deadline or when nothing visible has landed. Not for codebase review (`fettle`)."
---

# Plimsoll

A ship's load line: loaded past it, the ship can't make way. Find the line for this work and put the excess overboard.

**Payload** is what the person waiting will look at: a page that opens, a query that answers, a video that plays, a deploy they can click. **Process weight** is everything carried to make it safe to move: checks, CI, polls, reviews, plans, PR hygiene, subagents. Weight is justified by the payload it protects, never by its own completeness. This never licenses shipping something broken; it moves verification off the workspace and onto the payload.

## Use it unprompted when

- Three tool calls in a row check, poll or re-read settled ground with no edit between them.
- You are about to poll something you can't influence for the second time.
- A deadline is named and what you're doing now won't be visible before it.
- An hour has gone with no user-visible change.
- You've been told once to cut the checking and are reaching for another check.

## Then

1. Stop the loop and name it in one line.
2. Name the payload, audience and deadline: "catalogue shows live products, for the demo, in 45 minutes", or "no stated deadline".
3. Run the narrowest gate that could fail given what you changed. Defer anything wider to one pass at the end, and say so.
4. Build the payload in a straight line: no branch per item, no reviewer for a change you can read yourself, no plan for work already specified.
5. Verify the payload itself: open the page, run the query, play the video, click the deploy (`fieldtest` for an app in a browser).
6. Report in three lines: what landed and can be seen, what was cut, what's still broken. Never pair "done" with a caveat list.

## The tells

- **Gate ladder.** Widening checks because the last one passed (focused test, package typecheck, workspace typecheck, full suite); a gate the change can't break; re-running a passed gate after an unrelated change; reviewing settled work; "136 passed" reported as the outcome.
- **Watch loop.** Polling CI, a build or a queue; narrating the wait; making the blocker the new job (the build was slow, so now you're optimising the build); halting parallel agents to get a still tree.
- **Ceremony.** Re-planning specified work; a reviewer per task; a branch and PR per item when one would land the lot; a fourth attempt after three failures (get an outside read with `review` instead).
- **Test theatre.** Tests because "code changed"; tests against mocks that assert a spy was called (replace them with behaviour tests using `failfast`); coverage of paths nobody will take before the deadline. Before writing a test, finish: "The likely silent failure is ___, and this test catches it by ___." If you can't, don't write it.

Checking scales with reversibility, not importance. A demo gets one gate at the end, then you use it. Development gets the check the change could actually break. Data loss, auth, money and migrations get deep checks of the affected behaviour. Deleting data, rotating credentials and touching production are always slow.

Delegated code gets one read by the main agent; that's ownership. Cut extra reviewer agents, duplicate verification and polish rounds. If the brief costs more than the change, do it yourself.

## Builds and CI have hard stops

Before starting a build, CI job or deploy, write down its normal duration (from a recent successful run, else repo docs) and its hard stop:

- **Known duration:** the smaller of 15 minutes and the larger of twice normal or normal plus two minutes. A four-minute build stops at eight.
- **Unknown:** 10 minutes.

A shorter repo timeout wins; a longer stop only when the user or a release contract names it. Prefer a completion notification; otherwise check once, at the stop. Retries share the budget; only a change that could alter the result earns a fresh one. Give local commands a runner timeout. Cancel a remote job only if this session owns it. At the stop, report a timeout as a timeout, with the job URL, last meaningful output and elapsed time, then carry on with the payload. When editing CI, set the provider's job timeout to the same stop.

## Vercel builds on the user's machine

Vercel hosts; it does not build. For every preview and production deploy:

1. **Turn off Git deployments** with `git.deploymentEnabled: false` where the user or repo has adopted this rule; don't re-ask. In any other project, report them and ask before changing shared settings. An Ignored Build Step is no substitute: Vercel still starts the deployment, spends quota and holds a build slot.
2. `vercel pull --yes --environment=preview` (or `production`), with the repo's pinned Vercel CLI.
3. `vercel build` (`--prod` for production), under the hard stop. Output lands in `.vercel/output`.
4. `vercel deploy --prebuilt` (`--prod` for production), keeping the project's Git commit metadata.
5. Open the returned URL and exercise the payload.

Never run `vercel` or `vercel deploy` without `--prebuilt`, redeploy from the dashboard, fire a deploy hook, or let hosted CI produce the artifact. If production variables can't be pulled safely to this machine, the deploy is blocked: say what's missing and stop. Only the user can lift this rule.
