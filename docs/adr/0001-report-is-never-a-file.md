# 1. Report is never a file

Date: 2026-08-24
Status: Accepted

## Context

This collection descends from an earlier skill, arc:audit, which finished every run by writing a timestamped markdown report into the repo. Most audit tooling behaves the same way, so it never looked like a choice. It was one.

The word "report" was doing two jobs at once. Sometimes it meant the message a skill hands back in conversation. Sometimes it meant a file left behind on disk. A skill author reading "report your findings" could reasonably do either, and different skills in the collection had drifted to different answers.

The real question underneath was where the durable record of a piece of work lives. Two credible answers. An in-repo audit trail is greppable, diffable, and moves with the code - you can see what an audit said six months ago and what changed since. A tracker item is one searchable record in one place, visible to people who never clone the repo.

## Decision

A report is the message a skill returns in conversation, written to that skill's stated output contract. Reporting is the act of returning that message. It's never the act of writing a document.

The durable record is a tracker item in Linear.

A file exists only when someone explicitly asked for one, and that file is called an artefact - the exception, never the default.

## Consequences

Findings stop scattering. One place to search, and no question about whether the markdown in the repo or the item in the tracker is current, because there's only ever one of them.

What it costs: no in-repo history of what an audit said. You can't diff last month's findings against this month's, and someone reading the repo alone won't see that an audit ever happened. That's accepted. Scattered repo markdown is how documentation drift starts, and drift was judged the more expensive problem.

Watch for skills quietly reintroducing a default output file, usually with a plausible-looking `--out` or a "save the summary to" step. It reads as helpful and it reopens the whole thing. The vocabulary checker has a `report-file` rule guarding this, so a reintroduction should fail the gate rather than land silently - but the rule only catches the vocabulary, not every shape the habit can take.
