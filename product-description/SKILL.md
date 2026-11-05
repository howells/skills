---
name: product-description
description: "Document a product's user-visible behaviour feature by feature from code, tests and the running product, then triage suspected defects. Not for marketing copy, READMEs, single-feature specs or browser QA alone (`fieldtest`)."
---

# Product description

Treat the product as a large state chart the user moves through with input. Describe it feature by feature, in plain language, from the user's side, with the same skeleton for every document so gaps and contradictions show up by comparison. Draft from source and tests, verify against the running product, and collect everything that looks wrong into one triage file.

**Never modify the source repo.** It is read-only reference. **Never send messages, take payments or publish to document behaviour**: a throwaway production account doesn't isolate those. Use an isolated setup for mutating flows unless the user authorized those exact actions; otherwise mark the claim unverified. **Filing triage entries upstream is outward-facing**: offer it, don't do it unasked.

## Outputs

```
README.md            purpose, conventions, document template, method, structure, coverage table
goal.md              standing instructions for every drafter: reading order, established facts, rules
glossary.md          the vocabulary; source of truth for every term of art
AGENTS.md            "Read README.md, then goal.md. The coverage table in README.md is the work list."
CLAUDE.md            "Read @AGENTS.md."
{area}/{feature}.md  one document per feature, all on the same skeleton
verification/        README.md (protocol) + one checklist per cluster of documents
bug-triage.md        every suspected defect, deduplicated, with repro, cause, severity, decision needed
```

The default is a standalone git repo. When the consuming project keeps documentation in its tracker, put the same outputs there as linked documents on the owning issue (no local repo, reports or instruction files) and check links by reading the records back instead of running the link checker.

## 1. Scope

Settle these first; ask only for what the conversation and source repo can't tell you. Record them in the README's "Scope decisions".

- **Surface.** Which app, route, role or configuration, usually the defaults. One surface per repo.
- **Source.** The source repo path and commit; every footer cites `git rev-parse --short HEAD`.
- **Verification setup.** Command or URL, account, environment, owned test data, and which side effects are authorized.
- **Out of scope**, and why.
- **The product's shape.** Read [references/product-kinds.md](references/product-kinds.md) first, each reference file with its own command, and fix, once: the unit of interaction and its five phases, the variant axis, the interrupt list, and the cross-cutting concerns in order. Changing them later means revisiting every document.

Then find where interaction state lives (state machines, reducers, controllers, routes, commands), which tests read as specs of edge cases, where the UI is, and where defaults and thresholds are defined. These go in the README's "Reference" and goal.md's reading order.

## 2. Scaffold

Read each template before writing its file. README.md from [references/README-template.md](references/README-template.md): its structure section lists every expected document grouped by how the user meets it (foundations, product areas, cross-cutting concerns), never by package. Then glossary.md from [references/glossary-guide.md](references/glossary-guide.md), goal.md from [references/goal-template.md](references/goal-template.md), and the two one-line entry files. Commit.

## 3. Pilot, foundations, hardest area: yourself, in order

These set the depth, tone and vocabulary everything else copies.

1. **Pilot.** Read [references/document-template.md](references/document-template.md) first. One small feature with a real interaction, on its full eight-section skeleton. Iterate until it's right. Depth follows the behaviour, not a length target.
2. **Foundations.** The input model (events, thresholds, what cancels and interrupts), the core data model, the mode or navigation model, the viewport or session model. They own the facts others link to; add each load-bearing number and rule to goal.md's "Things already established".
3. **Hardest area.** Read all of its state handling before writing any of it, decide which document owns each state, and record that in goal.md.

## 4. Draft the rest in parallel

One document or small cluster per subagent, prompted:

> Read `goal.md`, `README.md`, `glossary.md`, `{pilot}` and `{the foundation this depends on}`. Write `{area}/{feature}.md` on the same skeleton and depth, in the glossary's words. Return any missing term as a proposed definition; don't edit the glossary or any other document, or the source repo. End with "## Open questions and verification" and the footer. Report what code and tests couldn't tell you.

The coordinator alone edits the glossary. Before accepting a document, check: glossary words used correctly, established facts not contradicted, every interrupt row filled (even "no effect"), suspected bugs stated plainly in open questions rather than smoothed over. Mark it `drafted` in the coverage table.

## 5. Consistency pass

One term per thing, all in the glossary. Where two documents touch, one owns the behaviour and the other links. Interrupt rows and cross-cutting concerns in the same order everywhere. README structure and coverage table match the files exactly. Check links and anchors by running `python3 references/check-links.py {repo}` from this skill's directory (exit 1 is broken targets; exit 2 is incomplete coverage, so raw HTML links and renderer-specific anchors still need a look). Then deepen the documents whose open questions were thinnest.

## 6. Verification

Read [references/verification-template.md](references/verification-template.md) first, then write a protocol README and one checklist per cluster, one row per observable claim with a stable ID (`AREA-NN`), priority, setup, steps and expected result. If you can drive the product, run a first pass and say exactly what it covered. A document is `verified` only when every P1/P2 claim was observed in the running product or its failure reproduced in triage; code reading and mocked tests don't count, and visual claims need rendered inspection. A failed row may mean the document is wrong rather than the product.

## 7. Bug triage

Read [references/bug-triage-template.md](references/bug-triage-template.md) first, then gather every suspected defect from bodies and open questions, merge by root cause, and give each where the user meets it, actual versus expected, repro, the cause at file and line, severity, and the decision needed (`fix` or `product call`). Summary table first, sorted by severity.

## Resuming

Read AGENTS.md, README.md, goal.md, glossary.md and the pilot. If the source commit has moved, ask whether new documents cite the new commit or the repo stays pinned; never mix silently. Add a new feature to the structure and coverage table before writing it, then its checklist and triage entries with the next free IDs. Never renumber a checklist or triage ID once used.

## Writing rules (carry into goal.md)

- Describe the experience, not the code: "the form stays disabled until the server answers", not "the mutation sets isPending". Mechanism goes in a `> Technical note:` only when it changes what the user would expect.
- Sentence-case headings. Direct and concrete; no hedging or marketing.
- State surprising behaviour plainly, with the reason if the code gives one. If it looks like a bug, say so in open questions.
- Variants and interrupts go in tables split by phase, every cell filled.
- Link rather than repeat; foundations own thresholds and definitions.
- One Mermaid `stateDiagram-v2` per interaction, limited to states the user passes through.
- Footer: `## Open questions and verification`, a bullet list, then `Source inspected: {repo} commit \`{sha}\`.` and `Runtime verification: {not run, or environment/date and linked results}.`
- What code and tests can't settle goes in open questions; don't guess, don't block.
- Commit per document or group: `docs: add {path}`, `docs: revise {path}`.
