---
name: deslop
description: "Rewrite prose that sounds synthetic, inflated, or assistant-like. Use for AI-writing tells, vague attribution, suspicious citations, chatbot artifacts. Applies to prose; for interface labels use `signage`; for machine-written code tells use `unslop`."
---

# Deslop

Review, diagnose, and rewrite prose that carries common AI-writing tells. Treat patterns as clues, not proof of authorship.

The tell taxonomy in `references/signs-of-ai-writing.md` encapsulates [*Wikipedia:Signs of AI writing*](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), adapted for general prose. Maintainers: that article is the source of record - re-check the reference file against it when the article changes.

State at the start that you are using the `deslop` skill.

## Guardrails

- Do not claim a text is AI-generated from a single tell.
- Do not rely on detector tools alone; they are fooled by light edits and unseen models.
- Prefer clusters of indicators over isolated phrases.
- Do not flatten strong human prose just because it is polished.
- Before editing, note what belongs to the writer: vocabulary, bluntness, humour, hedges that express real doubt, digressions, level of polish. Keep those. Cut in proportion to the tells present, and leave a sentence that works alone.
- Do not invent a fact, figure, example, quotation or source to make a sentence specific. Use what the draft or its sources contain; where they contain nothing, cut the sentence or list the gap under `Residual risk`.
- Preserve meaning, but do not preserve synthetic cadence.
- Preserve text presented as a verbatim quotation. Flag concerns or offer a separately labelled paraphrase; do not silently alter a source's words.
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
- Interface strings - labels, headings, buttons, status lines, empty states: hand to `signage`. They are signage rather than prose, and the tells differ. If `signage` is unavailable, continue the prose pass, leave interface strings unchanged and identify them as unreviewed.
- No input: ask for the text or file to review.

## Workflow

1. Read once for overall effect.
2. Mark the highest-signal clusters before editing.
3. Use the two catalogues when you need the full taxonomy: `references/signs-of-ai-writing.md` for encyclopaedic, reference and report prose, and `references/rhetorical-tells.md` for essays, newsletters, posts and announcements. The crutch-phrase list lives in this file, below.
4. Explain the issue in editorial terms, not detector jargon.
5. Rewrite toward specificity, directness, and verifiable claims.
6. Check citations, links, and markup separately when they look generated or broken.
7. Re-read the rewrite against the same tells before returning it. Removing one pattern often produces another: a deleted contrast comes back as a colon reveal, a cut recap as a quotable closing line.

When asked only to check, audit or flag, do not rewrite. For each pattern give its name, the quoted line and the edit in a few words. Give no score and no verdict on who wrote the text.

## Highest-Signal Tells

Look first for clusters of:

- inflated significance paired with generic language,
- source-listing or media-name dropping used as a substitute for substance,
- vague attribution such as "experts say" or "observers note",
- negative parallelisms such as "not just X, but Y",
- mannered metaphor standing in for a direct statement, such as "a dial worth turning" for "a parameter worth varying",
- openers that announce a point or claim a lone insight: "Here's the thing", "What most people get wrong",
- staged delivery: a colon reveal ("The surprising part: nobody measured it"), several denials before the claim, stacked fragments,
- an abstraction doing what a person did ("the decision emerged", "the data tells us"), hiding the actor,
- sentences that state importance and withhold the content: "The implications are significant",
- commentary on the prose itself: "Let that sink in", "The key point is", "As we'll see",
- a closing line that restates the point as an aphorism,
- outline-style "Despite its X, faces challenges" endings and bolt-on "Future Prospects" sections,
- assistant-style formatting: Markdown leakage, bold sprawl, title case drift, curly quotes where the house style uses straight quotes, ornamental lists,
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
- Replace mannered metaphor with the literal phrase, per the section below.
- Remove conclusion-style recaps unless the genre needs them.
- Delete a quotable closing line and end on the last concrete sentence. Do not write a better aphorism in its place.
- Name the actor. "The decision emerged" becomes "the board decided", when the draft says who decided.
- Cut commentary that calls a point important, surprising or subtle. Supply the reason as a fact from the draft, or let the point stand.
- Apply the portability test: a sentence that would fit unchanged in a piece about a different subject says nothing about this one. Cut it or make it specific.
- Prefer the verb to the verb phrase: "decided" for "made a decision", "can" for "has the ability to".
- Cut the crutch phrases below on sight.

## Mannered Prose

Mannered prose substitutes metaphor and flourish for direct statement. Instead of "a parameter worth varying", the mannered writer produces "a dial worth turning". Instead of "this point still matters", they write "this point earns its keep". The phrases exist to display the writer, not to convey the idea, and readers can tell. That is why mannered prose irritates: it makes the reader work harder so the writer can perform. It is also imprecise. Metaphors drag in connotations the writer did not choose and cannot control.

The fix is to say what you mean. When a literal phrase is available, use it.

Ask of any figurative phrase: what is the literal claim underneath, and is the figure doing work the literal claim cannot? A metaphor that names something with no plain word - a term of art, a genuinely novel idea - stays. One that dresses up a claim you could have written straight goes.

| Written | Say |
| --- | --- |
| A dial worth turning | A parameter worth varying |
| This point earns its keep | This point still matters |
| The load-bearing wall of the argument | Name the claim the argument depends on |
| Where the rubber meets the road | Name the step that actually decides it |
| The north star for the team | The goal, or the metric |

The table is direction rather than a lookup: each fix names what the figure was standing in for. Judge a mannered phrase by whether the plain version says the same thing in fewer words, and prefer the plain version when it does.

## Overused Crutch Phrases (Cut On Sight)

This section applies to formal or technical prose. In conversational or casual writing, colloquialisms like "to be honest", "honestly", and "let's be real" are legitimate voice markers, not AI evidence - do not cut them there.

These assert rigour or candour instead of demonstrating it. They are filler: delete them and state the thing plainly.

- **"load-bearing"** (load-bearing assumption / definition / detail / word / line). Say what the thing does or why it matters, not that it is structurally important.
- **The honesty family** - "keep (it / the model / us) honest", "the honest part", "to be honest", "honestly", "honest about its gaps / limits", "the honest answer". State the limitation or fact directly; announcing honesty adds nothing.
- **Related self-framing** - "to its credit", "the hard truth", "let's be real", "the uncomfortable truth", "make no mistake". Cut the preamble, keep the claim.

- **Announcements** - "here's the thing", "here's why", "it turns out", "let me be clear", "the real issue is". Start at the point.
- **Emphasis instructions** - "let that sink in", "full stop", "read that again", "this matters because", "the key point is". If the sentence needs the help, make it more specific.
- **Filler** - "it's worth noting", "at its core", "at the end of the day", "when it comes to", "in today's world", "in order to", and intensifiers such as "truly", "fundamentally" or "genuinely" where the sentence means the same without them.

These rarely carry meaning the surrounding sentence does not already hold. Treat them as deletions, not rewrites.

## Output

When reviewing text, use:

1. `Observed tells:` main patterns and exact phrases.
2. `Why they matter:` what the patterns do to the prose.
3. `Rewrite:` a surgical edit or clean replacement passage.
4. `Residual risk:` citation, sourcing, markup, or factual issues needing human review.

For short rewrite-only requests, provide only a short note and the revised text.

## Citation And Markup Checks

When citations or markup look suspicious, verify external sources when fetching is available and permitted. Otherwise mark those checks unverified and continue the wording and markup checks that can be done locally.

- Verify links resolve and support the claim.
- Compare DOI/ISBN identifiers against the claimed publication.
- Flag references with no page numbers, access dates, or usable locating detail.
- Check for leaked model artifacts.
- Preserve the host system's markup instead of introducing Markdown everywhere.
- Mark anything unverified under `Residual risk`.
