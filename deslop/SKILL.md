---
name: deslop
description: "Rewrite prose that reads as machine-written or inflated: vague attribution, staged contrasts, crutch phrases, fake citations, chatbot artefacts. Use for drafts, docs, posts and PR text. Not for interface strings (`signage`) or code (`unslop`)."
---

# Deslop

Find the tells that make prose read as generated, and rewrite towards specific, direct, verifiable sentences in the writer's own voice.

## Rules

- **Keep the writer.** Before editing, note what is theirs: vocabulary, bluntness, humour, hedges that express real doubt, digressions, the level of polish. Keep it. Cut in proportion to the tells, and never flatten strong human prose because it is polished. An opinionated, lively draft stays opinionated and lively.
- **Never invent** a fact, figure, example, name, quotation or source to make a sentence specific. Use what the draft and its sources hold; where they hold nothing, cut the sentence or list the gap under `Residual risk`.
- **Quotations stay verbatim.** Flag a concern or offer a separately labelled paraphrase.
- **Keep the meaning, not the cadence.**
- **No authorship verdicts.** A tell is a reason to edit, never evidence of who wrote it. Edit clusters; one tell, perfect grammar or a formal register is ordinary writing.
- **Interface strings go to `signage`**: labels, headings, buttons, status lines, empty states. In code, review only comments, docstrings and docs.

## Look first for

Clusters of:

- generic, important-sounding description where a specific fact belongs; inflated significance; name-dropping sources or media instead of saying what they found;
- vague attribution (`experts say`, `observers note`) and vague connection (`associated with`, `connected to`) where the draft could state the relationship;
- hedging about sources: `not widely documented`, `based on available information`, `should be treated as X rather than Y`;
- negative parallelisms: `not just X, but Y` and the reversed `Y rather than X`;
- openers that announce a point or claim a lone insight: `Here's the thing`, `What most people get wrong`;
- staged delivery: a colon reveal (`The surprising part: nobody measured it`), several denials before the claim, stacked fragments;
- an abstraction doing what a person did (`the decision emerged`, `the data tells us`);
- sentences that state importance and withhold the content (`The implications are significant`), and commentary on the prose itself (`Let that sink in`, `As we'll see`);
- a closing line that restates the point as an aphorism; `Despite its X, faces challenges` endings; bolt-on `Future prospects` sections;
- even rhythm: most sentences 8–20 words, almost none over 30, nothing but commas and full stops;
- assistant formatting: Markdown leakage, bold sprawl, title case drift, curly quotes against a straight-quote house style, ornamental lists;
- stock invented names, or a whole cast of them (one is not a tell);
- a sharp register shift between sections (a pasted-in passage);
- leaked tool markers (`oaicite`, `turn0search0`, `[cite: 1]`, `grok_card`, `【29†L582-L589】`, `[web:1]`), `utm_source` parameters, broken citations, placeholder markup.

Read [`references/signs-of-ai-writing.md`](references/signs-of-ai-writing.md) before editing prose that reports: docs, READMEs, reports, reference and encyclopaedic text. Read [`references/rhetorical-tells.md`](references/rhetorical-tells.md) before editing prose that argues or sells: essays, posts, newsletters, announcements, PR descriptions. Before judging invented people, places or companies, read [`references/slop-names.md`](references/slop-names.md). Read each reference file with its own command.

## Rewriting

- Replace importance language and `broader trends` talk with the concrete fact, mechanism or evidence.
- Turn a source roll-call into sourced claims.
- Use the direct verb: `is` for `serves as`, `stands as`, `represents`; `decided` for `made a decision`; `can` for `has the ability to`. Keep plain verbs plain; never trade `wrote` for `authored`.
- State the relationship: `associated with` becomes `founded` or `taught at` when the draft says which; otherwise flag the gap.
- Name the actor: `the board decided`, when the draft says who.
- Rewrite fake contrasts as direct statements.
- Delete the quotable closer and end on the last concrete sentence. Do not write a better aphorism in its place.
- Cut commentary that calls a point important, surprising or subtle. Give the reason as a fact, or let the point stand.
- Replacing a dash, pick by function: a semicolon between related clauses, brackets for an aside, a colon before an explanation, or two sentences of different lengths. Not a comma by default.
- **Portability test:** a sentence that would fit unchanged in a piece on another subject says nothing about this one. Cut it or make it specific.

Removing one pattern often breeds its substitute. Re-read the rewrite for these swaps: a cut contrast returns as a colon reveal or `Y rather than X`; a cut closer returns as a better aphorism; a cut dash returns as a comma splice or a run of short sentences; cut puffery returns as a vaguer `associated with`.

### What to keep or add

An editor who only cuts produces encyclopaedia register, which is the register a model defaults to. Where the draft has the material and the genre allows, keep or add:

- a point of view, stated as the writer's own;
- why something matters, with the concrete reason (importance without content is the tell; with its reason it is often the point);
- varied sentence length, and the full range of punctuation, including the writer's own semicolons, colons, brackets and dashes;
- plain verbs (wrote, moved, used, tried, died) and ordinary qualifiers (very, perhaps, tends to);
- true superlatives the facts support: `the first`, `the only`;
- dry wit drawn from the material, never bolted on;
- the vivid specific: the name, the number, the odd detail a model would smooth into `a revolutionary titan of industry`.

Encyclopaedic and reference prose stays neutral: add specifics, plain verbs and varied rhythm, keep attributed viewpoints, and add no opinions or jokes.

### Mannered prose

Mannered prose puts a figure where a statement belongs: `a dial worth turning` for `a parameter worth varying`, `this point earns its keep` for `this point still matters`, `the north star for the team` for `the goal`. It displays the writer, makes the reader work, and drags in connotations nobody chose. Ask what the literal claim is, and whether the figure does work the literal claim cannot. A metaphor naming something with no plain word stays; one dressing up a claim you could write straight goes.

### Crutch phrases

In formal and technical prose, delete these on sight; they assert rigour or candour instead of showing it. In casual writing, `honestly` and `let's be real` can be voice; leave them.

- **`load-bearing`**, in any combination. Say what the thing does.
- **The honesty family:** `keep (it / us / the model) honest`, `the honest part`, `to be honest`, `honestly`, `honest about its limits`, `the honest answer`. State the limitation.
- **Self-framing:** `to its credit`, `the hard truth`, `the uncomfortable truth`, `let's be real`, `make no mistake`.
- **Announcements:** `here's the thing`, `here's why`, `it turns out`, `let me be clear`, `the real issue is`.
- **Emphasis instructions:** `let that sink in`, `full stop`, `read that again`, `this matters because`, `the key point is`.
- **Filler:** `it's worth noting`, `at its core`, `at the end of the day`, `when it comes to`, `in today's world`, and `truly`, `fundamentally`, `genuinely` where the sentence means the same without them.

Ordinary qualifiers and the occasional `in order to` are not on this list.

## Citations and markup

When citations look generated, check that links resolve and support the claim, that DOI and ISBN match the publication, and that each citation has usable locating detail. Fetch when available; otherwise mark them unverified. Keep the host's markup rather than introducing Markdown.

## Output

Edit files in place; for pasted text, return the revised text. Then list the tells changed (pattern and exact phrase) and, only if any, `Residual risk:` sourcing, citation or factual gaps for a human. Asked only to check: the list without the rewrite.
