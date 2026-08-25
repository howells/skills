---
name: memento
description: "Report what this task is doing now from live state: original ask, completed work, remaining work, branch, uncommitted files, and drift. Use when returning to a long session or checking whether an agent is still on track. For a roll-call across tasks use `muster`; for rewriting only the last reply use `what`."
---

# Memento

Someone has lost the thread and wants it back in ten seconds. Answer from what is true this minute - the task list, the working tree, what is running - not from a recap of the conversation. Where the transcript and the repo disagree, the repo is right.

`muster` is the archaeological version: many sessions, transcript mining, tracker sweep. This is the cheap one, about a single session, and it should cost seconds.

**Drift is the point.** Nobody asks this out of curiosity. They ask because they suspect they have lost track, and what they need to know is whether the work is still the work they asked for. *You asked for X; I am doing Y, because Z* is worth more than a tidy list of completed steps, and it is the one thing invisible from outside. State it plainly when it is true - as a fact, not an apology.

**Lead with their ask, in their words.** They have forgotten it; that is why they asked. Opening with your current sub-task confirms nothing. If the ask was amended, give the version in force and say it changed.

## Reading

Task list, working tree, running processes, the last few tool results. Stop as soon as you can answer. No transcript mining, no tracker, no subagents - if the honest answer needs those, say so and offer `muster`.

Three attempts at the same failing command is "stuck", not "working on it". A step nobody has edited is "not started", however certain the plan. Uncommitted work is a risk, so give the file count. "Waiting on a build" is a complete answer.

## Output contract

One screen. These lines, nothing else - no preamble, no restating the question.

- **Ask.** What was asked for.
- **Now.** What you are doing this minute.
- **Done** / **Left.** Up to five each.
- **State.** Branch, uncommitted count, anything running.
- **Next.** One concrete action.
- **Drift** or **Blocked**, only when true, leading with the mismatch.

Write it through `deslop`. If it takes three paragraphs, they have to read it twice to decide whether to interrupt you.
