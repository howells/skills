---
name: inquest
description: "Answer a question about intent, history, or provenance by sweeping every available evidence source in parallel, then return a cited answer and coverage map. Use when a claim, decision, or number needs proving beyond the code. For rebuilding current working context use `muster`."
---

# Inquest

An inquest establishes a finding from the record. It calls every witness available, writes down which ones it could not call, and returns a verdict a reader can follow back to the evidence.

Use it for "why is it built this way", "what do we actually know about X", "is this claim supported", "what happened before this broke", or any number that is about to influence a decision.

The code is not a witness to its own intent. It tells you what happens, rarely why it exists, and never what was tried first and abandoned. Reading it harder does not fix that.

## The seven categories

Evidence about a decision scatters across systems that have nothing to do with each other. You cannot tell from the question which one holds the answer, so cover all seven:

1. Source control - commits, PR bodies, review threads.
2. Issue tracker - tickets, their comments, what they blocked.
3. Long-form documents - specs, notes, handoffs.
4. Real-time chat - the channel where it was actually argued out.
5. Database and warehouse - what the data says happened.
6. Observability and error tracking - what broke, and when.
7. Product analytics - what users did before and after.

The default is coverage. Deciding up front that "docs probably won't have this" is a blind spot; searching and finding nothing is a result.

## Steps

Copy these steps into your todolist verbatim before you reason about the question. A step you skip stays in the list with a one-line `skip: <reason>`.

1. **Fix the question and the scope.** What is being asked, about what target, over what time window. If the target is vague, state your reading of it in one line and carry on rather than asking.

2. **Anchor it.** Build the seed context inline, because every investigator needs it and rediscovering it seven times is waste: file paths and symbols, `git log --follow` and `git blame` on the target, the PR numbers in the merge subjects, the ticket IDs those PRs close. Hand this to every investigator.

3. **Enumerate the sources you actually have.** Read the live tool list for `mcp__<server>__*` entries, or run `claude mcp list`. Map each server onto a category above. A category with no server is a gap you will report, not a category you drop.

4. **One investigator per category, in parallel.** Never pool them - each source has its own query vocabulary and its own failure mode, and a pooled agent searches all of them badly. Each returns the same shape: what it searched, the exact query, what it found with a citation, or an explicit nothing. Bulk reading stays in the investigators; only their findings come back.

5. **Separate what you found from what you think.** Direct evidence carries a citation - commit hash, PR number, ticket ID, message permalink, `file:line`. Everything else is inference and is labelled as inference, with the chain shown. When two sources disagree, print both; the disagreement is usually the finding. When the evidence supports more than one story, give them all rather than picking the tidy one.

6. **Write the verdict to the contract below.** Do not upgrade the hedges on the way out. Sounding more certain than the evidence is how a sweep turns back into a guess.

## Output contract

- **The question.** Restated in one line, with the target anchored - paths, symbols, window.
- **What the record shows.** Cited claims only. One bullet per fact, each traceable in under a minute.
- **What follows from it.** Inference, hedged and shown as a chain: given A and B, likely C.
- **Where the record disagrees.** Competing readings with the evidence for each. Omit if there is a clean answer.
- **What is not known.** Questions the sweep did not answer, and the searches that came back empty. "Searched the tracker for the retry threshold and found no ticket" beats "unclear".
- **Sources consulted.** One line per category, including the ones that found nothing and the ones you could not reach. Format: `<category> (<server>): <what was searched>. <what was found, or "nothing relevant", or "skipped - no server available">.` This is the coverage map. It lets the reader see what you did not check, and send you back for it.

Write the verdict through `deslop` before it goes anywhere near a person.

## Failure modes

- **A good story on thin evidence.** An uncited bullet belongs under inference or competing readings, never under what the record shows.
- **Citing the code for its own motive.** "It handles null because it checks for null" is mechanics.
- **Assuming the newest commit is the reason.** The current shape is usually accreted, not designed. Trace back.
- **Agreeing with the asker.** A suggested reason is a hypothesis to test, not a conclusion to confirm.
- **Skipping a category by anticipation.** A null result is data. A skipped search is a hole you cannot see.
