---
name: simplify
description: "Strict structural review of a diff or whole codebase: finds restructurings that delete complexity, and real security, performance or data risks. Reports findings; edits only when asked. Not for diff tidy-ups (`unslop`), fallback removal (`failfast`) or browser QA (`fieldtest`)."
disable-model-invocation: true
---

# Simplify

A demanding review of structure. The question is not "could this be a bit cleaner?" but "is there a reframing that makes whole branches, modes, helpers or layers disappear?" Behaviour stays; complexity goes.

## Scope

- `simplify`: uncommitted changes, else the branch against the default branch. Trace callers and affected paths beyond the changed lines. No changes: say so; don't fall back to the whole repo.
- `simplify whole codebase`: every authored source root, skipping dependencies, generated and vendored code.
- `in <path>` narrows either. A named focus (`security`, `performance`) steers attention. `with scores` adds the [scorecard](references/scorecard.md); read it only then.
- Report only. Edit code when asked to apply fixes; write tracker items when asked to create them.

## What to push for

Be ambitious. Look for the code-judo move: a reorganisation that uses the existing architecture so the change becomes dramatically smaller and more direct. Prefer deleting complexity to moving it around; a refactor that leaves the reader holding as many concepts as before is not a simplification.

Flag hard:

- **A file crossing 1,000 lines.** Ask whether to decompose first; waive only for a compelling structural reason. In whole-codebase scope an existing large file is a lead, not a regression.
- **Spaghetti growth.** Ad-hoc conditionals, one-off booleans, nullable modes and special cases bolted into busy or unrelated flows. A design problem, not a nit: push the logic behind its own abstraction, state model or module.
- **Indirection that doesn't earn its keep.** Thin wrappers, identity abstractions, pass-through helpers, generic "magic" hiding a simple data shape.
- **Muddy boundaries.** Casts, `any`, `unknown`, needless optionality, loosely shaped objects, silent fallbacks papering over an unclear invariant.
- **Wrong home.** Feature logic leaking into shared paths, a bespoke helper beside the canonical one, logic in the wrong package or layer, copy-paste instead of one flow.
- **Orchestration.** Independent async work serialised for no reason; related updates that can leave state half-applied.
- **"Temporary" branching** that will become permanent.

Remedies, most ambitious first: delete the layer; reframe the state model so the conditionals vanish; move the ownership boundary so the feature extends an existing abstraction; turn special cases into one default flow; replace condition chains with a typed model or dispatcher; separate orchestration from business logic; split the file; reuse the canonical helper. Don't settle for "maybe rename this" when the problem is structural.

Working code is not the bar. Structure passes only with no structural regression, no visible path to a dramatically simpler version left untaken, no unjustified file growth, no spaghetti, no wrapper or cast churn, and no boundary leak or helper duplication. Otherwise ask for the cleaner decomposition, concretely.

## Calibrate

- **Stage sets severity; it never excuses structure.** Infer prototype, development, pre-launch or production from release notes, live deploy and monitoring config, and real users. A custom domain or commit count doesn't prove production; when unsure, write `stage: unconfirmed`. Don't demand production hardening of an experiment.
- **A structural blocker is not an incident.** Severity is demonstrated impact: Critical (exploitable exposure, imminent data loss), High (major failure, corruption, blocked critical flow), Medium (bounded correctness, performance or maintenance cost), Low (local structural debt). A Low finding can still block structural approval; don't call it urgent.
- **Diff versus existing.** Never present a pre-existing defect as introduced by the diff; raise it only where it bears on the change.
- **Other risks when the scope raises them.** Auth, untrusted input, secrets, payments, uploads, webhooks: security. Queries, loops, rendering, bundles: performance. Migrations and transactional writes: data. Async I/O, retries, state transitions: reliability. User-facing UI: accessibility. Mastra internals: `mastraudit`. Rendered behaviour: `fieldtest`.
- **Scanners, thresholds and advisories are leads.** Confirm every finding in source, with its callers. Run only checks that settle a specific question; no build, typecheck, lint and test ladder. A missing tool or timed-out check is a coverage gap, not a pass or a defect.
- **Recorded decisions win.** Repo instructions and documented trade-offs outrank generic advice; flag drift from them, not the choice itself.
- **Large scopes:** split areas across read-only helpers if available, and recheck every delegated claim in source before reporting it.

## Report

Lead with a one-line verdict, then scope (base or revision) and stage. Group findings by the change that would fix them together. Order: confirmed security or data-loss danger, then structural regressions, missed code-judo, spaghetti growth, boundary and type problems, file size, modularity, legibility. Prefer a few high-conviction findings; drop nits while bigger problems stand.

```
[severity] path/to/file:line
Cost: what it breaks or makes harder, and where.
Direction: the simpler structure or fix.
Keep: the behaviour or contract that must survive.
Excerpt: the exact source that shows it.
```

Be direct; don't soften a structural problem into a suggestion. The register:

- `this pushes the file past 1k lines. can we decompose this first?`
- `this adds another special case to an already busy flow. can we move it behind its own abstraction?`
- `this refactor moves complexity around but doesn't delete it. can the model itself get simpler?`
- `i think there's a code-judo move here: reframe this so these branches disappear.`

End with coverage: areas and risks examined, checks run, what was sampled or skipped, leads left unconfirmed. Never present a partial pass as a whole-codebase review.

Asked to apply fixes: implement the accepted findings with behaviour preserved and exercise the affected path. Asked for tracker items: reuse existing ones, one item per cluster with evidence and acceptance criteria.
