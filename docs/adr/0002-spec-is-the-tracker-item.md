# 2. Spec is the tracker item; an agent instruction is a brief

Date: 2026-08-24
Status: Accepted

## Context

The collection adopted the Pocock engineering skills - /to-spec, /to-tickets, /implement, /code-review - which run as the main flow for planning and shipping work. In those skills a spec is a tracker item stating the problem, the solution, user stories and the decisions taken, and it explicitly forbids file paths and code snippets.

foreman already used the word, and meant close to the opposite. A foreman spec is an instruction pinned down hard enough that a cheap model can transcribe it into code: files, interfaces, signatures, the lot. That's not a lesser spec or a fuller one. It sits at the other end of a detail axis entirely.

So one word covered two artefacts with opposite requirements, and an agent reading "write the spec" had no way to know which was wanted. The failure mode is quiet: a spec full of paths that go stale within a fortnight, or a subagent handed a problem statement it can't act on.

## Decision

A spec is the tracker item. Problem, solution, user stories, decisions. It names no file paths, because paths go stale faster than the spec does.

A brief is what a foreman sends a subagent. It must name files, interfaces and the report format.

The distinguishing test is one line: if it names files, it's a brief.

"Spec-complete" survives as an adjective, meaning fully pinned down. A brief is spec-complete. A spec isn't trying to be.

## Consequences

The main flow keeps the word in the sense four of its skills already used, so nothing there had to change. foreman gave up the word instead - the smaller migration by a wide margin, since letting bare "spec" keep foreman's meaning would have collided with the entire planning flow.

Anyone arriving from foreman's earlier vocabulary will use "spec" for a brief out of habit. Both readings are internally coherent, which is what makes the mistake easy and slow to notice. The file-path test settles it quickly enough once you know to apply it.

Watch for the adjective drifting back into a noun. "Write me a spec-complete spec" is the sentence to catch - it means a brief, and saying so plainly avoids the whole problem.
