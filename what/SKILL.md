---
name: what
description: Say plainly what just happened - the last message and the handful of actions behind it, translated out of jargon and tool names into what was actually done and what it means for the reader. Re-explains, never re-answers, and never starts new work. Use when a reply did not land, when an agent has been grinding and the last update made no sense, or for "wait, what did you just do". For the state of the whole task instead, use `memento`.
---

# What

The last message did not land. Say it again, properly.

Scope is the last message and the few actions behind it - not the session, not the diff. Someone wants to know what just happened, in words they can act on.

**Re-explain, never re-answer.** No new work, no new information, no tools beyond looking at what you already did. If a real question surfaces while you are re-explaining, name it and stop - do not go and solve it.

## Plain means translated, not shortened

Shortening jargon leaves jargon. If the reply comes back and gets asked the same question again, the first attempt was the same words with fewer of them.

- **Never let a tool name stand in for what happened.** Not "ran Edit on `foreman/SKILL.md`" but "changed the routing table so it names roles rather than specific models".
- **Drop internal nouns.** Say it the way you would to someone who does not know this codebase.
- **Facts survive exactly.** Every path, command, filename, number, URL and decision stays as it was. Simplify the explanation around the facts, never the facts.
- **Simpler, not necessarily shorter.** If an idea needs room to be clear, give it room. The target is impossible-to-misunderstand.
- **Flatten the structure.** Drop headings and ceremony. A table becomes sentences. Keep a list only where the thing genuinely had parts.

## Say if the fog was real

Sometimes a message was confusing because the work behind it was confused. Verbose output is a good hiding place for not knowing.

If that is what happened, that is the answer: say which part you are actually unsure about, rather than producing a cleaner version of the same fog. It is far more useful than a tidy summary that repeats a wrong assumption in better prose.

## Output contract

Four lines, more only if genuinely needed. No preamble, no restating the question.

- **Did.** What actually happened.
- **Means.** What that means for the reader.
- **Next.** What happens now, or what they need to decide.
- **Unsure**, only when true. What you do not actually know.

House voice: plain, direct, no filler and no persona. Write it through `deslop`.
