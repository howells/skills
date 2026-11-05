---
name: memento
description: "Say where this task stands from live state: the ask, done, left, branch, uncommitted files and any drift. Use on returning to a long session. Not for many sessions (`muster`) or the last reply (`what`)."
---

# Memento

Someone has lost the thread and wants it back in ten seconds. Answer from what is true this minute (task list, working tree, what's running, the last few tool results), not from a recap of the conversation. Stop reading as soon as you can answer. No transcript mining, tracker or subagents; if the answer needs those, offer `muster`.

**Lead with their ask, in their words.** They've forgotten it; that's why they asked. If it was amended, give the version in force and say it changed.

**Drift is the point.** People ask because they suspect the work has wandered. "You asked for X; I'm doing Y, because Z" is worth more than a tidy list of steps. State it as a fact, not an apology.

Three tries at the same failing command is "stuck", not "working on it". A plan alone is "not started". Uncommitted work is a risk, so give the file count. "Waiting on a build" is a complete answer.

## Output

One screen, these lines and nothing else:

- **Ask.** What was asked for.
- **Now.** What you're doing this minute.
- **Done** / **Left.** Up to five each.
- **State.** Branch, uncommitted count, anything running.
- **Next.** One concrete action.
- **Drift** or **Blocked**, only when true, leading with the mismatch.
