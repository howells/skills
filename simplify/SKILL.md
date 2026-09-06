---
name: simplify
description: "Review a diff or whole codebase for structural simplification and relevant health risks, with source-confirmed findings and optional scores. Not routine cleanup (`unslop`) or browser QA (`fieldtest`)."
disable-model-invocation: true
---

# Simplify

One review skill for selected changes or an existing codebase. Cursor's [Thermo-Nuclear Code Quality Review](https://github.com/cursor/plugins/blob/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md) supplies the structural standards; its rubric below is preserved unchanged. See the included [MIT licence](LICENSE).

## Scope and actions

- `simplify` reviews the selected diff, branch or PR. State the comparison base and include relevant surrounding code, dependencies and callers. If no scope is selected, use current uncommitted changes, otherwise branch changes against the repository's default branch. If there are no changes, say so; do not silently review the entire repository.
- `simplify whole codebase` reviews the current repository, including unchanged code. A path narrows either scope: `simplify in <path>` or `simplify whole codebase in <path>`.
- A focus such as `security` or `performance` directs attention within that scope. Explicit restrictions win. `with scores` adds scoring; without it, return findings without a scorecard. These are natural-language arguments, not harness-specific flags.

Both scopes report findings in conversation by default. A review does not authorize code edits, tracker writes, commits or publication. `Apply the fixes` authorizes implementation within the selected scope; `create Linear items` authorizes tracker work. Honor existing authorization without asking again. Do not write review artifacts into the repository unless requested.

Use the active harness's tools. No specific harness, integration or model is required. Repository instructions and explicit user constraints govern the review.

## Review the code

State the repository, revision, working-tree state and scope. Establish the project's stage using [stage guidance](references/stage.md); describe an inference as such. Stage affects impact and production-hardening expectations, but never suppresses structural simplification or weakens Cursor's approval bar.

For a whole codebase, map authored source roots and ownership boundaries, excluding dependencies, generated output and vendored code. Examine each in-scope area and trace contracts and data flow between them. For a diff, trace affected paths beyond the changed lines and distinguish new regressions from existing defects relevant to the change. Never present an unrelated pre-existing defect as introduced by the diff.

Apply the upstream structural rubric in both scopes. In whole-codebase scope, interpret its wording about a diff, PR or new growth as questions about the current implementation. An existing file over 1,000 lines warrants investigation; it does not prove a threshold-crossing regression. The approval bar is a verdict on reviewed code, not authorization to submit a PR review.

Use [review lenses](references/lenses.md) for relevant security, performance, reliability, data, test, operational and accessibility concerns. Whole-codebase reviews consider which lenses apply across the repository; diff reviews choose them from the affected behavior and contracts. Do not create a fixed panel or demand production infrastructure for an experiment. For specialist runtime questions, use an available domain skill such as `mastraudit`; rendered browser QA belongs to `fieldtest`.

Use independent read-only agents for distinct areas when the scope benefits and the harness supports them. Match available models to the work: stronger reasoning for design across packages, capable implementation models for tracing behavior, lighter models for bounded inspection. Prefer Sol, Terra and Luna where available; use equivalent models elsewhere. Give each agent its scope, repository decisions, stage, relevant rubric, existing evidence and expected findings. The coordinator checks shared boundaries and consolidates findings. Continue sequentially if delegation is unavailable.

Use existing scanners as leads, then confirm them in source. Inspect scripts before execution and run the narrowest checks needed to establish a finding or validate an authorized fix. No automatic build, typecheck, lint and full-suite ladder. A missing prerequisite or timed-out check is unavailable evidence, not a pass or a source defect; investigate the cause before retrying. Do not install tools or run commands with unrelated external side effects merely to complete a review.

## Verify and group findings

Every reported finding needs source locations and evidence. Read the cited code and relevant callers, establish what it costs, propose the simpler or safer structure, and identify the behavior or contract that must survive. Recheck delegated claims against the actual source before accepting them; unconfirmed leads stay explicitly separate from findings.

Respect deliberate repository conventions and recorded tradeoffs; flag additional risk or implementation drift with evidence. Check whether findings are already tracked when tracker access is available. Retain unresolved known defects with their existing links; dismiss resolved, disproven or explicitly accepted-by-design claims with a short reason. A connected tracker alone does not authorize writes.

Group related findings by the change that would fix them together, rather than by which agent found them. Keep Cursor's structural finding order within that review; put any confirmed immediate security or data-loss danger first. Severity describes demonstrated impact at this project's stage. A structural approval blocker and an urgent production incident are different judgments; label them accurately.

## Report and follow through

Lead with a plain verdict, then scope and stage. Present the strongest clusters with source citations, impact, a concrete remedy and the behavior to preserve. Keep minor nits out when consequential findings exist. End with a coverage map: areas and lenses examined, checks actually run, skipped or sampled areas and unconfirmed leads. A partial review must never be presented as a completed whole-codebase review.

Only when scoring is requested, load [the scorecard](references/scorecard.md). Mark unreviewed or inapplicable axes `--`, adjust the denominator, and record scope, revision and criteria. A diff score describes only the reviewed changes and affected paths; it is never a repository health score.

When tracker work is requested, reuse existing items and create one actionable item per cluster, with source evidence, acceptance criteria and priority justified by actual impact and dependencies. When fixes are requested, implement the accepted scope, preserve behavior, and verify it through the affected consumer or focused tests. Use available specialist skills when useful, without requiring a separate task or automatic handoff. Commit, PR and delivery behavior follows the user's authorization and repository policy.

## Upstream review rubric

Use this skill for an unusually strict review focused on implementation quality, maintainability, abstraction quality, and codebase health.

Above all, this skill should push the reviewer to be **ambitious** about code structure. Do not merely identify local cleanup opportunities. Actively search for "code judo" moves: restructurings that preserve behavior while making the implementation dramatically simpler, smaller, more direct, and more elegant.

## Core Prompt

Start from this baseline:

> Perform a deep code quality audit of the current branch's changes.
> Rethink how to structure / implement the changes to meaningfully improve code quality without impacting behavior.
> Work to improve abstractions, modularity, reduce Spaghetti code, improve succinctness and legibility.
> Be ambitious, if there is a clear path to improving the implementation that involves restructuring some of the codebase, go for it.
> Be extremely thorough and rigorous. Measure twice, cut once.

## Non-Negotiable Additional Standards

Apply the baseline prompt above, plus these explicit review rules:

0. **Be ambitious about structural simplification.**
   - Do not stop at "this could be a bit cleaner."
   - Look for opportunities to reframe the change so that whole branches, helpers, modes, conditionals, or layers disappear entirely.
   - Prefer the solution that makes the code feel inevitable in hindsight.
   - Assume there is often a "code judo" move available: a re-organization that uses the existing architecture more effectively and makes the change dramatically simpler and more elegant.
   - If you see a path to delete complexity rather than rearrange it, push hard for that path.

1. **Do not let a PR push a file from under 1k lines to over 1k lines without a very strong reason.**
   - Treat this as a strong code-quality smell by default.
   - Prefer extracting helpers, subcomponents, modules, or local abstractions instead of letting a file sprawl past 1000 lines.
   - If the diff crosses that threshold, explicitly ask whether the code should be decomposed first.
   - Only waive this if there is a compelling structural reason and the resulting file is still clearly organized.

2. **Do not allow random spaghetti growth in existing code.**
   - Be highly suspicious of new ad-hoc conditionals, scattered special cases, or one-off branches inserted into unrelated flows.
   - If a change adds "weird if statements in random places", treat that as a design problem, not a stylistic nit.
   - Prefer pushing the logic into a dedicated abstraction, helper, state machine, policy object, or separate module instead of tangling an existing path.
   - Call out changes that make the surrounding code harder to reason about, even if they technically work.

3. **Bias toward cleaning the design, not just accepting working code.**
   - If behavior can stay the same while the structure becomes meaningfully cleaner, push for the cleaner version.
   - Do not rubber-stamp "it works" implementations that leave the codebase messier.
   - Strongly prefer simplifications that remove moving pieces altogether over refactors that merely spread the same complexity around.

4. **Prefer direct, boring, maintainable code over hacky or magical code.**
   - Treat brittle, ad-hoc, or "magic" behavior as a code-quality problem.
   - Be skeptical of generic mechanisms that hide simple data-shape assumptions.
   - Flag thin abstractions, identity wrappers, or pass-through helpers that add indirection without buying clarity.

5. **Push hard on type and boundary cleanliness when they affect maintainability.**
   - Question unnecessary optionality, `unknown`, `any`, or cast-heavy code when a clearer type boundary could exist.
   - Prefer explicit typed models or shared contracts over loosely-shaped ad-hoc objects.
   - If a branch relies on silent fallback to paper over an unclear invariant, ask whether the boundary should be made explicit instead.

6. **Keep logic in the canonical layer and reuse existing helpers.**
   - Call out feature logic leaking into shared paths or implementation details leaking through APIs.
   - Prefer existing canonical utilities/helpers over bespoke one-offs.
   - Push code toward the right package, service, or module instead of normalizing architectural drift.

7. **Treat unnecessary sequential orchestration and non-atomic updates as design smells when the cleaner structure is obvious.**
   - If independent work is serialized for no good reason, ask whether the flow should run in parallel instead.
   - If related updates can leave state half-applied, push for a more atomic structure.
   - Do not over-index on micro-optimizations, but do flag avoidable orchestration complexity that makes the implementation more brittle.

## Primary Review Questions

For every meaningful change, ask:

- Is there a "code judo" move that would make this dramatically simpler?
- Can this change be reframed so fewer concepts, branches, or helper layers are needed?
- Does this improve or worsen the local architecture?
- Did the diff add branching complexity where a better abstraction should exist?
- Did a previously cohesive module become more coupled, more stateful, or harder to scan?
- Is this logic living in the right file and layer?
- Did this change enlarge a file or component past a healthy size boundary?
- Are there repeated conditionals that signal a missing model or missing helper?
- Is the implementation direct and legible, or does it rely on special cases and incidental control flow?
- Is this abstraction actually earning its keep, or is it just a wrapper?
- Did the diff introduce casts, optionality, or ad-hoc object shapes that obscure the real invariant?
- Is this logic living in the canonical layer, or did the diff leak details across a boundary?
- Is this orchestration more sequential or less atomic than it needs to be?

## What to Flag Aggressively

Escalate findings when you see:

- A complicated implementation where a cleaner reframing could delete whole categories of complexity.
- Refactors that move code around but fail to reduce the number of concepts a reader must hold in their head.
- A file crossing 1000 lines due to the PR, especially if the new code could be split out.
- New conditionals bolted onto unrelated code paths.
- One-off booleans, nullable modes, or flags that complicate existing control flow.
- Feature-specific logic leaking into general-purpose modules.
- Generic "magic" handling that hides simple structure and makes the code harder to reason about.
- Thin wrappers or identity abstractions that add indirection without simplifying anything.
- Unnecessary casts, `any`, `unknown`, or optional params that muddy the real contract.
- Copy-pasted logic instead of extracted helpers.
- Narrow edge-case handling implemented in the middle of an already busy function.
- Refactors that technically pass tests but make the code less modular or less readable.
- "Temporary" branching that is likely to become permanent debt.
- Bespoke helpers where the codebase already has a canonical utility for the job.
- Logic added in the wrong layer/package when it should live somewhere more central.
- Sequential async flow where obviously independent work could stay simpler and clearer with parallel execution.
- Partial-update logic that leaves state less atomic than necessary.

## Preferred Remedies

When you identify a code-quality problem, prefer suggestions like:

- Delete a whole layer of indirection rather than polishing it.
- Reframe the state model so conditionals disappear instead of getting centralized.
- Change the ownership boundary so the feature becomes a natural extension of an existing abstraction.
- Turn special-case logic into a simpler default flow with fewer exceptions.
- Extract a helper or pure function.
- Split a large file into smaller focused modules.
- Move feature-specific logic behind a dedicated abstraction.
- Replace condition chains with a typed model or explicit dispatcher.
- Separate orchestration from business logic.
- Collapse duplicate branches into a single clearer flow.
- Delete wrappers that do not meaningfully clarify the API.
- Reuse the existing canonical helper instead of introducing a near-duplicate.
- Make type boundaries more explicit so the control flow gets simpler.
- Move the logic to the package/module/layer that already owns the concept.
- Parallelize independent work when that also simplifies the orchestration.
- Restructure related updates into a more atomic flow when partial state would be harder to reason about.

Do not be satisfied with "maybe rename this" feedback when the real issue is structural.
Do not be satisfied with a merely cleaner version of the same messy idea if there is a plausible path to a much simpler idea.

## Review Tone

Be direct, serious, and demanding about quality.
Do not be rude, but do not soften major maintainability issues into mild suggestions.
If the code is making the codebase messier, say so clearly.
If the implementation missed an opportunity for a dramatic simplification, say that clearly too.

Good phrases:

- `this pushes the file past 1k lines. can we decompose this first?`
- `this adds another special-case branch into an already busy flow. can we move this behind its own abstraction?`
- `this works, but it makes the surrounding code more spaghetti. let's keep the behavior and restructure the implementation.`
- `this feels like feature logic leaking into a shared path. can we isolate it?`
- `this abstraction seems unnecessary. can we just keep the direct flow?`
- `why does this need a cast / optional here? can we make the boundary more explicit instead?`
- `this looks like a bespoke helper for something we already have elsewhere. can we reuse the canonical one?`
- `i think there's a code-judo move here that makes this much simpler. can we reframe this so these branches disappear?`
- `this refactor moves complexity around, but doesn't really delete it. is there a way to make the model itself simpler?`

## Output Expectations

Prioritize findings in this order:

1. Structural code-quality regressions
2. Missed opportunities for dramatic simplification / code-judo restructuring
3. Spaghetti / branching complexity increases
4. Boundary / abstraction / type-contract problems that make the code harder to reason about
5. File-size and decomposition concerns
6. Modularity and abstraction issues
7. Legibility and maintainability concerns

Do not flood the review with low-value nits if there are larger structural issues.
Prefer a smaller number of high-conviction comments over a long list of cosmetic notes.

## Approval Bar

Do not approve merely because behavior seems correct.
The bar for approval is:

- no clear structural regression
- no obvious missed opportunity to make the implementation dramatically simpler when such a path is visible
- no unjustified file-size explosion
- no obvious spaghetti-growth from special-case branching
- no obviously hacky or magical abstraction that makes the code harder to reason about
- no unnecessary wrapper/cast/optionality churn obscuring the real design
- no clear architecture-boundary leak or avoidable canonical-helper duplication
- no missed opportunity for an obvious decomposition that would materially improve maintainability

Treat these as presumptive blockers unless the author can justify them clearly:

- the PR preserves a lot of incidental complexity when there is a plausible code-judo move that would delete it
- the PR pushes a file from below 1000 lines to above 1000 lines
- the PR adds ad-hoc branching that makes an existing flow more tangled
- the PR solves a local problem by scattering feature checks across shared code
- the PR adds an unnecessary abstraction, wrapper, or cast-heavy contract that makes the design more indirect
- the PR duplicates an existing helper or puts logic in the wrong layer when there is a clear canonical home

If those conditions are not met, leave explicit, actionable feedback and push for a cleaner decomposition.
