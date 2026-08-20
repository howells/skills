---
name: mastraudit
description: Audit a Mastra codebase against what actually breaks it, worst first - workflow step size and fan-out keying, suspend and resume payloads, load-bearing writes that must throw, model settings nesting, the tool keys a model actually sees - and only then containment and domain structure. Runs shipped boundary scanners where they exist and falls back to search. Use when reviewing Mastra work before shipping or auditing an existing implementation. For building rather than judging, use `$mastra`.
---

# Mastraudit

Audit a Mastra implementation in the order things actually go wrong.

That ordering is the whole point, and it is a correction. An audit that leads with architecture catches a stray `@mastra/*` import instantly and misses the incident that costs the most hours. Package boundaries are cheap to fix and rarely fatal. Execution semantics - what a step does, how fan-out results are keyed, whether a load-bearing write throws - are where runs die, and they are invisible to a structural pass.

So: **execution first, structure second.** If you run out of time, you will have spent it on the half that matters.

## Source of truth

Mastra moves fast enough that recalled API shapes are wrong more often than right. In priority order:

1. **The installed packages.** `node_modules/@mastra/*` types and embedded docs. This is what will actually run.
2. **The documentation for that version.** A local mirror if one exists, the published docs otherwise.
3. **Nothing else.** Never model memory for constructor signatures, model routing, storage, memory, workflow, or tool APIs.

Note the installed version and resolve any disagreement in favour of what is installed. Where a codebase ships its own Mastra conventions - a house package, an architecture document, a failure log - read it first; it outranks generic guidance about that codebase.

## The five-minute pass

When there is no time for the full audit, these catch the most:

1. **`modelSettings`** - is every token cap nested under it, never flat at the top level?
2. **Step size** - does any workflow step do more than one discrete thing?
3. **Fan-out** - do arms return receipts rather than bulk, and does the collector key on identity rather than array position?
4. **Load-bearing writes** - does a write a later step depends on throw on failure?
5. **Tool keys** - does the model see `verb_noun`, or a leaked camelCase shorthand?

## Use the scanners before you grep

Several of these checks are deterministic and already implemented. Where `@howells/mastra` is installed, `@howells/mastra/boundary` exports scanners that each return sorted `path: reason` findings - as of 0.2.1: `findDirectMastraImports`, `findToolIdFilenameMismatches`, `findToolsMissingAnnotations`, `findBarrelFiles`, `findFlatGenerateSettings`, `findShorthandToolKeys`, `findUnkeyedMcpClients`. Check the installed version's exports rather than trusting this list.

Run them first and spend your own attention on the judgement calls. Manual search is the fallback for codebases without the package, not the default. A hand-rolled regex that disagrees with a shipped scanner is wrong until proven otherwise - the scanner encodes calibration you cannot see.

## The check catalogue

- [Execution semantics](references/execution.md) - workflows, fan-out, concurrency, retries, suspend and resume, state and storage, long agent loops. Where the fatal failures live.
- [Structure](references/structure.md) - containment, orchestrator discipline, agents and models, tools.
- [Evidence](references/evidence.md) - observability, testing, and what counts as having verified something.

## Steps

Copy these steps into your todolist verbatim before you start. A step you skip stays in the list with a one-line `skip: <reason>`.

1. **Scope it and say it back.** Which package owns Mastra, and which surfaces are in range. If zero or several packages declare Mastra dependencies, that ambiguity is the first finding - report it and ask before auditing on a guess.

2. **Establish the source of truth.** Note installed versions. Find any codebase-local conventions document. Say which you are auditing against.

3. **Run the scanners** if they are available, and record what each returned including the empty ones. An unrun scanner is not a pass.

4. **Audit execution semantics** against `references/execution.md`. This is the longest step and it comes first on purpose.

5. **Audit structure** against `references/structure.md`.

6. **Audit evidence** against `references/evidence.md`.

7. **Report to the contract below.**

## Output contract

Findings ranked by what a failure costs, not by section order.

Each finding carries: `file:line`, the failure it invites in one sentence, and the fix. Where a finding matches a known incident class in the codebase's own failure log, cite it - a named prior incident is far more persuasive than a rule.

- **Blocking.** Would lose a run, corrupt state, or silently produce wrong output.
- **Should fix.** Real, not yet fatal.
- **Noted.** Judgement calls the codebase may have made deliberately. Ask rather than assert.
- **Not checked.** Anything skipped, and why. A short audit honestly scoped beats a long one implying coverage it did not have.

## Failure modes

- **Leading with architecture.** Containment findings are easy to produce and rarely the expensive problem. They go second.
- **Asserting an API shape from memory.** Read the installed types. This is the single most common way an audit is confidently wrong.
- **Over-strict containment.** Blanket "no `@mastra/*` outside the owner" flags legitimate infra clients. See `references/structure.md`.
- **Flagging a pattern whose exception is documented.** `onStepFinish` with `structuredOutput` is only a bug without `structuredOutput.model`. Check the narrow form before flagging.
- **Reporting a clean pass on checks you did not run.** Say what you did not check.
