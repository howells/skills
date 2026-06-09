# Signs of AI Writing

A taxonomy of clues, not proof of authorship. Weigh clusters, not isolated hits, and
always read the counter-signals in "Signs of Human Writing" and "Ineffective
Indicators" before concluding anything.

> **Source.** This file encapsulates *Wikipedia:Signs of AI writing*
> (https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). It mirrors that
> article's taxonomy adapted for general prose; purely Wikipedia-internal tells
> (AfC submission statements, maintenance-template gaming, fabricated WP: shortcuts,
> edit-summary patterns) are deliberately omitted, while the generalizable ones —
> fabricated policies/standards, cross-section style shifts — are kept. When the
> source article changes, re-check this file against it.

## Caveats

- AI-detection tools are unreliable. They are fooled by light editing and by models
  they were not trained on. Do not rely on them.
- Most people detect AI prose at roughly chance level. Heavy LLM users reach about
  90% accuracy, mostly by recognising the patterns below — not by intuition.
- The word lists and tics drift by model and release date. Treat the specific
  vocabulary as era-bound; treat the underlying behaviour (inflated register,
  synonym-swapping, hedged authority) as the durable signal.

## Content Tells

### Inflated Significance

Prose insists a subject is important, pivotal, enduring, emblematic, or part of a
broader shift without adding concrete information.

Common pattern:

- blurry high-status summary replaces a precise fact,
- gestures at "legacy", "impact", or "the evolving landscape",
- subject is framed as symbolic when the source material is mundane,
- watch phrases: "stands as", "is a testament to", "plays a vital/significant/
  crucial/pivotal role", "reflects broader", "symbolizing", "setting the stage for",
  "marks a turning point", "leaves an indelible mark", "represents a shift".

### Notability By Assertion

Copy tries to prove importance by naming outlets, coverage, or "independent sources"
rather than summarizing what those sources actually say.

Common pattern:

- source roll-calls and "featured in"/"profiled in" laundry lists,
- "independent coverage", "media outlets", "maintains an active social media presence",
- separate "media coverage" sections that are just inventories,
- superficial analysis falsely attributed to the cited sources.

### Superficial Analysis

Shallow interpretive gloss pasted onto ordinary facts.

Common pattern:

- trailing `-ing` phrases that force a moral or thematic reading
  ("highlighting", "underscoring", "emphasizing", "reflecting", "fostering",
  "contributing to", "ensuring", "encompassing"),
- abstract claims of "valuable insights" or things that "align/resonate with",
- synthetic opinion ("generated debate", "drew praise") with no attributable source.

### Promotional Tone

Marketing, branding, travel-guide, or press-release cadence.

Common pattern:

- "boasts a", "vibrant", "rich", "profound", "groundbreaking", "renowned",
  "diverse array", "commitment to", "showcasing", "exemplifies",
- travel-brochure tics: "nestled", "in the heart of", "natural beauty",
- constant reminders of cultural heritage, prestige, or significance.

### Vague Attribution

Authority with no owner.

Common pattern:

- "experts argue", "observers note", "researchers say", "industry reports",
  "some critics", "several sources",
- weasel wording that implies a non-exhaustive list or exaggerates how many
  sources actually exist.

### Outline-Style Endings

Conclusion paragraphs that summarize "challenges", "future prospects", or "broader
implications" in generic terms.

Common pattern:

- the rigid formula "Despite its [positive qualities], [subject] faces challenges…"
  closing on a vague positive or speculative note,
- standalone "Challenges" and "Future Prospects" sections,
- generic resolution statements that resolve nothing.

### Title-As-Proper-Noun Leads

Opening sentence treats a list, broad topic, or descriptive article title as if it
were a proper noun or a single named entity, e.g. "**List of tallest buildings** is…"
or "**Sustainable urban transport** refers to the…" introduced as a standalone thing.

## Language Tells

### AI Vocabulary Density

Watch for clusters, not single words. The cluster drifts by era:

- 2023–mid-2024: additionally, boasts, bolstered, crucial, delve, emphasizing,
  enduring, garner, intricate, interplay, key, landscape, meticulous, pivotal,
  tapestry, testament, underscore, valuable, vibrant.
- mid-2024–mid-2025: align with, bolstered, crucial, emphasizing, enhance, enduring,
  fostering, highlighting, pivotal, showcasing, underscore, vibrant.
- mid-2025+: emphasizing, enhance, highlighting, showcasing.
- in comments/discussion: overuse of "concrete" ("concrete evidence",
  "concrete examples").

The specific words change; the underlying pattern is inflated register and
synonym-swapping to avoid plain language.

### Avoidance Of Plain Copulatives

Generated prose dodges `is` and `are` with inflated structures: "serves as",
"stands as", "represents", "marks", "boasts", "features", "maintains", "offers",
"refers to". AI copyedits measurably reduce simple `is`/`are` usage.

Edit move: use `is`, `are`, `was`, or a direct verb.

### Negative Parallelisms

Common patterns:

- not just X, but (also) Y
- not only X, but Y
- not X, but Y ("not a mirror but a portal")
- this is not A; it is B

Often used to "clear up a misconception" that no reader actually held.

Default edit: rewrite as a direct statement.

### Rule Of Three

Repeated triplets of adjectives or phrases ("adjective, adjective, adjective";
"short phrase, short phrase, and short phrase") that make weak analysis sound
finished and comprehensive.

### Elegant Variation / Lexical Diversity

Needless synonym swapping to avoid repeating a simple noun even when repetition
would be clearer — a visible side effect of repetition penalties.

Caveat: non-native English speakers and some careful stylists do this naturally.
A single instance is not a tell.

## Style And Formatting Tells

- Title case drift in headings (capitalising every main word).
- Boldface sprawl — mechanical emphasis, every instance of a chosen term bolded,
  "key takeaways" styling.
- Inline-header vertical lists: a bold lead-in followed by a colon inside each item.
- Bare bullet characters (•, -, –, #, emoji) or explicit "1." numbering where the
  host system has its own list markup.
- Em dashes used as an all-purpose dramatic hinge.
- Curly/smart quotation marks and apostrophes where the house style uses straight ones.
- Tables where prose or a simple list would be more natural.
- Heading levels skipped (h2 → h4) or decorative thematic breaks before headings.
- Emoji in contexts where the house style would not use them.

## Assistant Leakage

Strong signs that assistant output leaked directly:

- "let's explore", "here's a breakdown", "we can also", "I hope this helps",
- knowledge-cutoff and gap disclaimers: "as of my last update", "based on my
  training data", speculation about sources it "cannot access",
- collaborative-tone boilerplate: offers to take criticism, reminders to assume
  good faith, calls to "focus on the content, not the contributor",
- phrasal templates, placeholder text, and fill-in-the-blank scaffolds.

## Markup And Citation Artifacts

### Markup leakage

- Markdown in a non-Markdown context (`#` headers, `**bold**`, backtick code),
- broken or malformed native markup, unclosed brackets/templates,
- retrieval/search markers: `turn0search0`, `turn1search3`, and similar,
- reference-bug tags: `contentReference`, `oaicite`, `oai_citation`, `+1`,
  `attached_file`, `grok_card`,
- attribution tags: `attribution`, `attributableIndex`,
- non-existent or out-of-place categories and templates.

### Citation problems

- broken external links,
- invalid DOI/ISBN, or DOIs that resolve to an unrelated article,
- book citations with no page numbers, URLs, or usable locating detail,
- `utm_source` and other tracking parameters left in citation URLs,
- named references declared but never used in the text,
- citation formats applied incorrectly or unconventionally,
- fabricated or mismatched citations.

## Miscellaneous Tells

- A pronounced shift in writing style, vocabulary, or register between sections —
  a strong sign part of an article was pasted in from a model.
- Overwhelmingly exhaustive, oddly thorough edit/change summaries.
- Unsolicited "submission statement" preambles explaining the work.
- Maintenance/cleanup tags pre-placed by the author without justification.
- References to non-existent policies, guidelines, or shortcuts in discussion.
- Wikilawyering: invoking real rules but misapplying them.

## Signs Of Human Writing (Counter-Signals)

Read these before concluding. They argue *against* AI authorship:

- The text predates broad public LLM use (ChatGPT launched November 2022). Older
  material is very unlikely to be AI-generated.
- The author can explain their editorial choices coherently when asked.
- Idiosyncratic, non-standard syntax and personal voice that a model smooths away.

## Ineffective Indicators

Weak or misleading on their own — do not flag a text on these alone:

- A single "AI vocabulary" word, em dash, or rule-of-three in otherwise grounded prose.
- Polish, fluency, or correctness by itself. Strong human writing is also polished.
- Detector-tool output (see Caveats).
- Any one formatting quirk without a supporting cluster of content tells.

## Historical Indicators

Largely obsolete but still seen in older AI text:

- Didactic disclaimers and educational preambles (common Nov 2022–2024).
- Section-end summaries / recaps.
- Prompt-refusal leakage: "I can't help with that", "As an AI language model…".
- Abrupt mid-sentence cut-offs where generation hit a limit.
- Outdated or anachronistic citation access-dates (future-dated or impossible dates).
