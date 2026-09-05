---
name: plimsoll
description: "Cut process weight when gate ladders, CI/build watch loops, remote Vercel builds or re-planning displace shipping. Keeps Vercel builds on the user's machine. Use near a deadline or after nothing user-visible has landed. Not `survey`."
---

# Plimsoll

A ship carries a load line painted on its hull. Loaded past it, the vessel sits too low to make way. This skill finds the line for a piece of work and puts the excess overboard.

**Payload** - the thing the person waiting will look at. A page they open, a query that returns the right answer, a video that plays, a deploy they can click. If nobody outside this session can see it, it is not payload.

**Process weight** - everything carried to make the payload safe to move: checks, CI gates, polls, reviews, plans, PR hygiene, subagent ceremony. All of it costs turns, and it is worth carrying in proportion to what it protects.

**The rule that decides every call: process weight is justified by the payload it protects, never by its own completeness.** A check nobody would act on is weight. A gate that cannot fail given what you changed is weight. A poll that changes nothing is weight. Running one more because the last one passed is how a session overloads.

This skill never licenses shipping something broken. It moves verification off the workspace and onto the payload.

## The tells

Cite by number so the pattern is visible rather than the instance.

**The gate ladder** - checks that widen because the last one passed

1. **Widening the check after it passes.** Focused test, then package typecheck, then workspace typecheck, then workspace lint, then the full suite. Each rung fires because the previous one went green. Nobody named a risk that made it necessary.
2. **A gate the change cannot break.** A workspace-wide typecheck for a three-line edit inside one package. Run the narrowest gate that could plausibly fail.
3. **Re-running a gate that already passed** because something unrelated moved.
4. **Reviewing settled work.** Spawning reviewers for a diff you have already read, or grading a decision that was taken two turns ago.
5. **A green gate reported as the outcome.** "136 passed, 1 failed" is not a deliverable.

**The watch loop** - turns spent waiting

6. **Polling something you cannot influence.** A CI run, a Vercel build, a queue. Each poll is a turn that ships nothing. Give the job a hard budget before starting it, use completion notifications where they exist, and make at most one status check at the hard stop. Do other work meanwhile; if there is no other work, say so and stop.
7. **Narrating the wait.** "Still on the same stage at 7m51s." The person reading learns nothing they could act on.
8. **Making the blocker the new job.** The build was slow, so now you are optimising the build. Note it as a tracker item and carry on with what you were sent to do.
9. **Stopping other work so a check can run.** Halting parallel agents to get a still tree is a large cost for a signal that will be stale a minute later.

**Ceremony** - process that produces no payload

10. **Re-planning work already specified.** Another plan, another review round, another restatement of the decision. If the spec exists, build against it.
11. **A reviewer for every task.** A test-writer, a spec-reviewer and a code-quality reviewer dispatched for a change one person could read in a minute.
12. **A branch and a PR per item.** Separate branches and PRs per item when one would land the lot.
13. **Tests without a named risk.** "Code changed" is not a risk. Do not send a test-writer to manufacture unit tests because a diff exists or a workflow expects a test step.
14. **Tests written against mocks.** They assert the spy was called and pass forever. They prove nothing and cost the same as a real one. Stripping them out of an existing diff is `unslop`.
15. **Tests for paths the payload never takes.** Exhaustive coverage of a code path nobody will exercise between now and the deadline.
16. **Trial and error at length.** After three failed attempts at the same thing, a fourth will not fix it. Stop and get an outside read - `fable-review` for a judgement call, `glm-review` for a bounded conformance check.

## Stop conditions

Any one of these means you are over the line. Stop the current command and run the steps.

- Three consecutive tool calls that check, poll or re-read settled ground - re-running a test, polling a build, opening a file you have already read - with no edit landing between them.
- A second poll of something you cannot influence.
- A local build, CI job or deploy has reached its written hard stop.
- A build or CI job is running and nobody wrote down its normal duration and hard stop before starting it.
- A Vercel deployment would upload source for Vercel or hosted CI to build.
- A gate wider than the package you edited.
- A deadline named in the conversation, and what you are doing right now will not be visible in the result before it.
- Someone asks whether you have actually done the thing yet, and the answer is no.
- You have already been told once to cut the checking, and you are reaching for another check.
- An hour has passed and you cannot name a user-visible change.

## Hard limits for builds and CI

These are limits, not estimates. A shorter repository timeout wins. A longer limit is allowed only when the user explicitly asks for it or an existing release contract names it; write that exception down before the job starts.

1. **Write down the normal duration and hard stop before starting.** Take the normal duration from a recent successful run of the same job, then repository documentation. If neither exists, treat the duration as unknown.
2. **Known duration:** the hard stop is the smaller of 15 minutes and the larger of twice the normal duration or the normal duration plus two minutes. A four-minute build stops at eight minutes; it never turns into a 45-minute wait.
3. **Unknown duration:** the hard stop is 10 minutes. Discovering that the job is usually slower is a reason to update the written baseline later, not permission to keep waiting now.
4. **One observation, not a watch loop.** Prefer a completion notification. Otherwise make one status check at the hard stop. Never simulate waiting with repeated short polls or narrate elapsed time.
5. **The budget covers retries.** A retry does not reset the clock. Start a fresh budget only after a code, configuration or infrastructure change that could plausibly change the result.
6. **Enforce the stop.** Give local commands a runner timeout. At the hard stop, terminate the local process. Cancel a remote job only when this session owns it and cancellation will not discard evidence another person needs; otherwise leave it running and stop waiting for it.
7. **Call a timeout a timeout.** Capture the job URL or identifier, the last meaningful output and the elapsed time. Do not report success or failure without evidence. If delivery depends on it, name the blocker and the next action; otherwise continue with the payload.

When editing CI itself, set the provider's native job timeout to the same hard stop, rounded up only as required by the provider. The agent-side stop still applies if the provider cannot enforce it.

## Vercel builds happen on the user's machine

This is a hard delivery rule. "Local" means the user's machine and the intended repository checkout. A hosted CI runner is remote. Vercel is the deployment and runtime target; it does not build application source.

For every preview and production deployment:

1. **Disable automatic Git deployments.** Set `git.deploymentEnabled` to `false` in the project's Vercel configuration and confirm the live project setting agrees. Do not substitute an Ignored Build Step: Vercel still starts that deployment, consumes quota and occupies a build slot before cancelling it.
2. **Pull the target settings locally.** Use `vercel pull --yes --environment=preview` for previews or `vercel pull --yes --environment=production` for production. Pin and use the repository's declared Vercel CLI version.
3. **Build once, locally.** Run `vercel build` for preview or `vercel build --prod` for production from the linked checkout, under the hard time limit above. The output is `.vercel/output`.
4. **Deploy only that artifact.** Use `vercel deploy --prebuilt` for preview or `vercel deploy --prebuilt --prod` for production. Preserve the project's required Git commit metadata when creating the deployment.
5. **Verify the deployed artifact.** Open the returned URL and exercise the payload. A successful local build is not deployment proof.

Never use `vercel`, `vercel deploy`, `vercel --prod` or `vercel deploy --prod` without `--prebuilt`. Never use a dashboard redeploy, deploy hook, Git integration or hosted CI job that causes application source to be built away from the user's machine. Hosted CI may validate source, but it must not produce the Vercel deployment artifact.

If production settings, sensitive environment variables or required Vercel system variables cannot be materialised safely on the user's machine, the deployment is blocked. State the missing input and stop. Do not fall back to a remote build. Only an explicit new instruction from the user can reverse this rule.

## Steps

Use these steps to resume delivery. Keep notes only where they clarify scope, ownership, time limits or deferred work; do not turn the intervention into a new planning ceremony.

1. **Stop and say what was running.** Name the command or the loop, in one line. Cancel anything still burning money or build minutes.
2. **Name the payload, the audience and the deadline.** "Newsstand grid renders real catalogue rows, for the Materia demo, in 45 minutes." Use the stated deadline, or write "no stated deadline" and continue. Ask only when an unknown deliverable or audience changes the work that should ship.
3. **Split the remaining work into payload and weight.** Two lists, counted. A task that appears in neither is finished or does not matter.
4. **Cut the gate ladder to one gate.** Pick the narrowest check that could plausibly catch a break in what you actually changed. Everything wider gets deferred to one pass at the end, and you say so.
5. **Timebox every build and remote gate.** Write its normal duration and hard stop, enforce the runner timeout, and arrange a completion notification or one check at the hard stop. Do this before starting it. For Vercel, build locally and deploy only with `--prebuilt`.
6. **Build the payload.** Straight line. No new branch per item, no reviewer for a change you can read yourself, no plan for work already specified.
7. **Verify against the payload, not the workspace.** Open the page. Run the query. Play the video. Click the deploy. `fieldtest` if it is an app in a browser. Do not skip this step.
8. **Report in three lines.** What landed and can be seen. What was cut, and the tracker item holding it. What is still broken. Never pair "done" with a caveat list - either it is done, or it is not and you keep working.

## How much checking is enough

The axis is reversibility, not importance.

- **Prototype and demo work.** One gate at the end. Verify by using the thing. Skip the suite, skip coverage, skip the review round. A demo is judged on whether it works in front of people.
- **Development.** Narrow gate per change, full gate before merge. Real tests over mocked ones, and only where a break would be silent.
- **Pre-launch and production.** Choose checks for named failure risks and the release contract. Data loss, auth, money and migrations warrant deeper verification of the affected behaviour; the lifecycle label alone does not justify every check for every edit.

Deleting data, rotating credentials and touching production sit outside this calibration. Those are always slow.

Before writing a new automated test, finish this sentence: "The likely silent failure is ___, and this test catches it by ___." If you cannot, do not write the test. Prefer using the real payload when that exposes the failure more directly. Existing repository-required checks can still run at the final merge gate; they do not justify adding a new test to every change.

## When Foreman also applies

Explicitly requested `foreman` governs implementation ownership; Plimsoll governs the weight around it. Never invoke Foreman merely because work is substantial. Keep one main-agent inspection of delegated code because that is ownership, not an extra review round. Cut additional reviewer agents, duplicate verification, generated tests without a named risk, repeated fix rounds for optional polish, and any full gate the risk or merge contract does not earn. If the brief and dispatch cost more than the job, Foreman no longer applies: finish the small change directly and verify the payload.

## What this is not

- Not permission to ship broken work, or to claim something works without opening it.
- Not an argument against tests. It argues against tests aimed at the workspace while the payload sits unopened.
- Not a codebase audit. Grading a repository's health is `survey`.
- Not a QA pass. Exercising a running app in a browser is `fieldtest`.
- Not a delegation strategy. Routing substantial implementation to subagents is `foreman`; this skill has final say over the process weight around that routing when both apply.
