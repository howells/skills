---
name: deslop
description: "Audit and rewrite prose that carries AI-writing tells: inflated significance, negative parallelisms like \"not just X, but Y\", vague attribution, generic source roll-calls, assistant leakage, suspicious citations, and chatbot markup artifacts. Use when asked to check for AI slop, make text sound less like ChatGPT, explain why prose feels AI-generated, clean up LLM prose, or rewrite synthetic-sounding copy into a grounded voice."
---

# Deslop

Review, diagnose, and rewrite prose that carries common AI-writing tells. Treat patterns as clues, not proof of authorship.

The tell taxonomy in `references/signs-of-ai-writing.md` encapsulates [*Wikipedia:Signs of AI writing*](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), adapted for general prose. That article is the source of record; keep the reference in sync with it.

## Guardrails

- Do not claim a text is AI-generated from a single tell.
- Do not rely on detector tools alone; they are fooled by light edits and unseen models.
- Prefer clusters of indicators over isolated phrases.
- Do not flatten strong human prose just because it is polished.
- Preserve meaning, but do not preserve synthetic cadence.
- Weigh counter-signals before concluding: text predating broad LLM use (ChatGPT
  launched November 2022), an author who can explain their choices, and idiosyncratic
  non-standard syntax all argue against an AI origin.
- Ignore the "ineffective indicators" (a lone buzzword, em dash, or rule-of-three;
  mere polish) unless a supporting cluster is present.
- If the user only asks for a rewrite, keep diagnosis brief.

## Input Handling

- Inline text: use it directly.
- File path: read the file, then review its prose.
- URL: fetch page content before reviewing if browsing is available.
- Code or structured data: review comments, docstrings, docs, or surrounding copy only; ask if unclear.
- No input: ask for the text or file to review.

## Workflow

1. Read once for overall effect.
2. Mark the highest-signal clusters before editing.
3. Use `references/signs-of-ai-writing.md` when you need the full taxonomy.
4. Explain the issue in editorial terms, not detector jargon.
5. Rewrite toward specificity, directness, and verifiable claims.
6. Check citations, links, and markup separately when they look generated or broken.

## Highest-Signal Tells

Look first for clusters of:

- inflated significance paired with generic language,
- source-listing or media-name dropping used as a substitute for substance,
- vague attribution such as "experts say" or "observers note",
- negative parallelisms such as "not just X, but Y",
- outline-style "Despite its X, faces challenges" endings and bolt-on "Future Prospects" sections,
- assistant-style formatting: Markdown leakage, bold sprawl, title case drift, curly quotes, ornamental lists,
- a pronounced style or register shift between sections (pasted-in passage),
- leaked model artifacts such as `oaicite`, `contentReference`, or `turn0search0`,
- broken citations, `utm_source` tracking params, suspicious links, or placeholder markup.

## Rewrite Rules

- Replace generic importance language with concrete facts.
- Replace "broader trends" talk with the actual mechanism or evidence.
- Turn source roll-calls into sourced claims.
- Cut vague praise, policy-sounding abstractions, and promotional framing.
- Prefer direct verbs over "serves as", "stands as", "represents", or "underscores".
- Rewrite fake contrasts as direct statements.
- Remove conclusion-style recaps unless the genre needs them.
- Cut the crutch phrases below on sight.
- Preserve the host document's native markup.

## Overused Crutch Phrases (Cut On Sight)

These assert rigour or candour instead of demonstrating it. They are filler: delete them and state the thing plainly.

- **"load-bearing"** (load-bearing assumption / definition / detail / word / line). Say what the thing does or why it matters, not that it is structurally important.
- **The honesty family** — "keep (it / the model / us) honest", "the honest part", "to be honest", "honestly", "honest about its gaps / limits", "the honest answer". State the limitation or fact directly; announcing honesty adds nothing.
- **Related self-framing** — "to its credit", "the hard truth", "let's be real", "the uncomfortable truth", "make no mistake". Cut the preamble, keep the claim.

These rarely carry meaning the surrounding sentence does not already hold. Treat them as deletions, not rewrites.

## Output Shape

When reviewing text, use:

1. `Observed tells:` main patterns and exact phrases.
2. `Why they matter:` what the patterns do to the prose.
3. `Rewrite:` a surgical edit or clean replacement passage.
4. `Residual risk:` citation, sourcing, markup, or factual issues needing human review.

For short rewrite-only requests, provide only a short note and the revised text.

## Citation And Markup Checks

When citations or markup look suspicious:

- Verify links resolve and support the claim.
- Compare DOI/ISBN identifiers against the claimed publication.
- Flag references with no page numbers, access dates, or usable locating detail.
- Check for leaked model artifacts.
- Preserve the host system's markup instead of introducing Markdown everywhere.
- Mark anything unverified under `Residual risk`.
