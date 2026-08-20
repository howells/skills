---
name: what
description: Cut the last message down to what actually happened - short, and translated out of jargon and tool names into what was done and what it means for the reader. Called because the previous reply was long and dense, so brevity is the product. Re-explains, never re-answers, and never starts new work. Use when a reply did not land, when an agent has been grinding and the last update made no sense, or for "wait, what did you just do". For the state of the whole task instead, use `memento`.
---

# What

The last message did not land. Usually because it was long, dense and full of jargon.

Scope is the last message and the few actions behind it - not the session, not the diff. Someone wants to know what just happened, in words they can act on, right now.

**Short is the product.** They are asking because they were handed a wall of text. Another wall, in friendlier words, fails. Aim for a tenth of what you are explaining: forty lines become four. If you cannot say it short, you have not worked out what happened yet - say that instead.

**Re-explain, never re-answer.** No new work, no new information, no tools beyond looking at what you already did. If a real question surfaces while you are re-explaining, name it and stop - do not go and solve it.

## Short and translated, both

Length and jargon are two failures and fixing one does not fix the other. Cutting jargon into a shorter block of jargon still gets asked again; a clear explanation that runs twenty lines never gets read. Do both, every time.

- **Never let a tool name stand in for what happened.** Not "ran Edit on `foreman/SKILL.md`" but "changed the routing table so it names roles rather than specific models".
- **Drop internal nouns.** Say it the way you would to someone who does not know this codebase.
- **Facts survive exactly.** Every path, command, filename, number, URL and decision stays as it was. Simplify the explanation around the facts, never the facts.
- **Flatten the structure.** Drop headings and ceremony. A table becomes sentences. Keep a list only where the thing genuinely had parts.

## Say if the fog was real

Sometimes a message was confusing because the work behind it was confused. Verbose output is a good hiding place for not knowing.

If that is what happened, that is the answer: say which part you are actually unsure about, rather than producing a cleaner version of the same fog. It is far more useful than a tidy summary that repeats a wrong assumption in better prose.

## Output contract

Four short lines. Not four paragraphs, and not four lines each carrying a subordinate clause. No preamble, no restating the question.

- **Did.** What actually happened.
- **Means.** What that means for the reader.
- **Next.** What happens now, or what they need to decide.
- **Unsure**, only when true. What you do not actually know.

If something genuinely will not compress, give the one-line version and offer the detail rather than delivering it unasked.

House voice: plain, direct, no filler and no persona. Write it through `deslop`.
