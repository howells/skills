---
name: plimsoll
description: "Cut process weight when gate ladders, build-watch loops and re-planning have displaced shipping. Use near a deadline, or after a stretch with nothing user-visible. Aims verification at what ships, not the workspace. Not `survey`."
---

# Plimsoll

A ship carries a load line painted on its hull. Loaded past it, the vessel sits too low to make way. This skill finds the line for a piece of work and puts the excess overboard.

**Payload** - the thing the person waiting will look at. A page they open, a query that returns the right answer, a video that plays, a deploy they can click. If nobody outside this session can see it, it is not payload.

**Process weight** - everything carried to make the payload safe to move: checks, gates, polls, reviews, plans, PR hygiene, subagent ceremony. All of it costs turns, and it is worth carrying in proportion to what it protects.

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

6. **Polling something you cannot influence.** A CI run, a Vercel build, a queue. Each poll is a turn that ships nothing. Set one check at the end of the expected duration and do other work meanwhile; if there is no other work, say so and stop.
7. **Narrating the wait.** "Still on the same stage at 7m51s." The person reading learns nothing they could act on.
8. **Making the blocker the new job.** The build was slow, so now you are optimising the build. Note it as a tracker item and carry on with what you were sent to do.
9. **Stopping other work so a check can run.** Halting parallel agents to get a still tree is a large cost for a signal that will be stale a minute later.

**Ceremony** - process that produces no payload

10. **Re-planning work already specified.** Another plan, another review round, another restatement of the decision. If the spec exists, build against it.
11. **A reviewer for every task.** A test-writer, a spec-reviewer and a code-quality reviewer dispatched for a change one person could read in a minute.
12. **A branch and a PR per item.** Separate branches and PRs per item when one would land the lot.
13. **Tests written against mocks.** They assert the spy was called and pass forever. They prove nothing and cost the same as a real one.
14. **Tests for paths the payload never takes.** Exhaustive coverage of a code path nobody will exercise between now and the deadline.
15. **Trial and error at length.** After three failed attempts at the same thing, a fourth will not fix it. Stop and get an outside read - `fable-review` for a judgement call, `glm-review` for a bounded conformance check.

## Stop conditions

Any one of these means you are over the line. Stop the current command and run the steps.

- Three consecutive tool calls that check, read or poll without an edit between them.
- A second poll of something you cannot influence.
- A gate wider than the package you edited.
- A deadline named in the conversation and no payload that survives it.
- Someone asks whether you have actually done the thing yet, and the answer is no.
- An hour has passed and you cannot name a user-visible change.

## Steps

Copy these into your todolist verbatim before you start. A step you skip stays in the list with a one-line `skip: <reason>`.

1. **Stop and say what was running.** Name the command or the loop, in one line. Cancel anything still burning money or build minutes.
2. **Name the payload, the audience and the deadline.** "Newsstand grid renders real catalogue rows, for the Materia demo, in 45 minutes." If you cannot fill in all three, the first question goes to the user, not to another check.
3. **Split the remaining work into payload and weight.** Two lists, counted. A task that appears in neither is finished or does not matter.
4. **Cut the gate ladder to one gate.** Pick the narrowest check that could plausibly catch a break in what you actually changed. Everything wider gets deferred to one pass at the end, and you say so.
5. **Build the payload.** Straight line. No new branch per item, no reviewer for a change you can read yourself, no plan for work already specified.
6. **Verify against the payload, not the workspace.** Open the page. Run the query. Play the video. Click the deploy. `fieldtest` if it is an app in a browser. Do not skip this step.
7. **Report in three lines.** What landed and can be seen. What was cut and when it comes back. What is still broken. Never pair "done" with a caveat list - either it is done, or it is not and you keep working.

## How much checking is enough

The axis is reversibility, not importance.

- **Prototype and demo work.** One gate at the end. Verify by using the thing. Skip the suite, skip coverage, skip the review round. A demo is judged on whether it works in front of people.
- **Development.** Narrow gate per change, full gate before merge. Real tests over mocked ones, and only where a break would be silent.
- **Pre-launch and production.** The full ladder earns its weight. Data loss, auth, money and migrations are worth every check you can run.

Deleting data, rotating credentials and touching production sit outside this calibration. Those are always slow.

## What this is not

- Not permission to ship broken work, or to claim something works without opening it.
- Not an argument against tests. It argues against tests aimed at the workspace while the payload sits unopened.
- Not a codebase audit. Grading a repository's health is `survey`.
- Not a QA pass. Exercising a running app in a browser is `fieldtest`.
- Not a delegation strategy. Routing implementation to subagents is `foreman`; this skill only says when the ceremony around that routing has outgrown the work.
