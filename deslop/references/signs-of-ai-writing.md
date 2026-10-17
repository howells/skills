# Signs of AI writing

A taxonomy of clues, not proof of authorship. Weigh clusters over isolated hits, and
read "Signs of human writing" and "Ineffective indicators" before concluding anything.

> **Source.** This file adapts *Wikipedia:Signs of AI writing*
> (https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) for general prose.
> Last checked against the revision of 16 October 2026 (oldid 1380587573). Sections
> that only make sense inside Wikipedia are deliberately omitted: Articles for
> Creation submission statements and pre-declined review templates, edit summaries,
> canned user pages, permissions gaming, maintenance-template gaming and wikitext
> quirks with no general equivalent. Their generalisable parts stay: fabricated
> policies and standards, style shifts between sections, hallucinated categories and
> templates. When the article changes, re-check this file against it section by
> section.
>
> Quoted watch words keep the spelling models emit, which is usually American
> ("emphasizing", "prioritize"). Search for them as written.

## Caveats

- Detection tools beat chance but have real error rates. Paraphrasing, changes to
  markup or spacing, and models they were not trained on all fool them. Do not rely
  on them.
- People are poor judges too. A 2025 study put human readers at chance. In a 2025
  preprint, a subset of expert annotators caught 90% of generated text, while
  participants who rarely used these tools did only slightly better than chance. Knowing the patterns can guide
  an edit. It does not establish who wrote the text.
- Human writing is drifting towards model style, in speech as well as print, so the
  gap narrows.
- A sign points at a problem; it is not the problem. Rewording a tell while the
  unsourced claim, the puffery or the invented citation stays underneath only makes
  the problem harder to see. Fix the substance, or flag it.
- Word lists and tics drift by model and release. Treat the vocabulary as era-bound,
  and the behaviour underneath (inflated register, hedged authority, generic
  description) as the durable signal.

The article's most common signs in new text, as of October 2026: Markdown where the
host uses other markup, generated edit summaries (omitted here as Wikipedia-internal),
hedging disclaimers about sources, vague expressions of connection, and canned emphasis
on notability and media coverage.

## Content tells

### Regression to the mean

Most of the content tells below share one cause. A model predicts the statistically
likely continuation, and later tuning pushes it towards broadly palatable prose.
Specific, unusual facts are rare in the training data; generic, positive,
important-sounding description is common. So the specific fact gets swapped for the
generic praise, and "inventor of the first train-coupling device" becomes "a
revolutionary titan of industry". The subject ends up less specific and more
exaggerated at the same time, and the description would fit a hundred other subjects.

The editor's positive test: could this description be more specific? If the draft or
its sources hold the specific fact, put it back. If they hold nothing, the praise has
nothing under it; cut it or flag the gap.

### Inflated significance

Prose insists a subject is important, pivotal, enduring or part of a broader shift
without adding information.

- A blurry high-status summary replaces a precise fact.
- Mundane material (an etymology, a population table) gets a statement of its wider
  importance, sometimes after a preamble admitting the subject is minor.
- The subject is placed amid "debates" or said to have "participated in public
  discussions".
- Writing on species and habitats leans on tenuous links to the wider ecosystem and
  belabours conservation status, even where none is recorded.
- Since mid-2026, editorialising that a distinction or nuance is important, often
  next to a hedging disclaimer.
- Watch phrases: "stands/serves as", "is a testament/reminder", "a crucial/pivotal/
  vital/significant/key role/moment", "underscores/highlights its importance",
  "reflects broader", "symbolizing its ongoing/enduring/lasting", "contributing to
  the", "setting the stage for", "marking/shaping the", "represents/marks a shift",
  "key turning point", "evolving landscape", "focal point", "indelible mark", "deeply
  rooted", "distinction matters because".

### Canned emphasis on notability and media coverage

Copy tries to prove importance by describing the sources: what kind they are, where
they appeared, whether they can be found. What the sources say goes missing.

- Watch phrases: "independent coverage", "local/regional/national media outlets",
  "music/business/tech outlets", "trade publications", "cited/featured/profiled in",
  "written by a leading expert", "maintains an active social media presence", "was
  identified by".
- Wording lifted from the publisher's own acceptance criteria ("independent
  coverage"), as if the justification for the edit leaked into the text.
- The model's own superficial analysis attributed to a named source ("Roger Ebert
  highlighted the lasting influence") whether or not the source says anything close.
- More common in tools released from 2025. Press releases have cited clippings for
  decades. What gives a model away is the phrasing above and the attention paid to
  the sources themselves.

### Superficial analysis

Interpretive gloss pasted onto ordinary facts, usually as a trailing `-ing` phrase.

- Watch phrases: "highlighting/underscoring/emphasizing ...", "ensuring ...",
  "reflecting/symbolizing ...", "contributing to ...", "cultivating/fostering ...",
  "encompassing ...", "enhancing ...", "valuable insights", "align/resonate with".
- Synthetic opinion ("generated debate", "drew praise") with no source that holds it.

### Promotional tone

Advertising, press-release or travel-guide cadence, even when the prompt asked for a
neutral register.

- Watch phrases: "boasts a", "vibrant", "rich", "profound", "enhancing",
  "showcasing", "exemplifies", "commitment to", "natural beauty", "nestled", "in the
  heart of", "groundbreaking", "renowned", "featuring", "diverse array".
- Constant reminders that something is cultural heritage; press-release tone about
  people and companies.
- A rewrite that claims to have removed promotional tone and has added it.
- Older models were blatantly positive. Newer ones are subtly positive and avoid
  flat superlatives such as "the best". Not all promotional writing is generated.
  Models reuse the same stock phrases whatever the topic.

### Vague connection or association

Two subjects are said to be "connected" or "associated" where the source states a
plain relationship. "Jane Doe taught science at Example University" becomes "Jane Doe
was connected with science education at Example University"; "John Doe was the CEO"
becomes "sources identified John Doe as associated with leadership of ExampleCorp".
It often comes with promotional wording ("particularly/widely associated") and
sometimes stacks one association on another.

- Watch phrases: "in connection with/to", "connected with/to", "in association
  with", "associated with".

Edit: state the actual relationship ("founded", "taught at", "was CEO of"). If the
draft does not say what the relationship was, flag the gap.

### Vague attribution and overgeneralisation

Authority with no owner, and more of it than the sources support.

- Watch phrases: "industry reports", "observers have cited", "experts argue", "some
  critics argue", "several sources/publications" when few are cited, "such as"
  before what is in fact the whole list.
- A view from one or two sources presented as widely held; "reviewers" or
  "scholars" in the plural when one person is cited.

### Outline-style endings

- The formula "Despite its [positive qualities], [subject] faces challenges...",
  closing on a vague positive note or on speculation about future initiatives.
- Standalone "Challenges", "Challenges and Legacy", "Future Outlook" or "Future
  Prospects" sections at the end of a rigid outline.
- Only the formula counts. A plain mention of a challenge is ordinary writing.

### "X and Y" headings

Headings of the form "X and Y" are common in generated articles, and "Awards and
recognition" (or a bare "Recognition" section) is close to ubiquitous. It is the
legacy and coverage habits above, given a section of their own.

### Title-as-proper-noun leads

The opening sentence treats a list, a broad topic or a descriptive title as a single
named entity: "**List of tallest buildings** is...", or "**Sustainable urban
transport** refers to the...".

## Language tells

### AI vocabulary density

Watch for clusters. One or two of these words may be chance; a passage that brings in
many of them, many times, is one of the strongest tells there is. They tend to travel
together.

Words to watch across eras: "Additionally" (especially opening a sentence), "align
with", "boasts" (meaning "has"), "bolstered", "crucial", "deep dive", "delve",
"emphasizing", "enduring", "enhance", "fostering", "garner", "highlight" (as a verb),
"interplay", "intricate/intricacies", "key" (as an adjective), "landscape" (as an
abstract noun), "meticulous/meticulously", "pivotal", "robust", "showcase",
"tapestry" (as an abstract noun), "testament", "underscore" (as a verb), "valuable",
"vibrant".

The cluster drifts by era. The dates are approximate.

- 2023 to mid-2024 (GPT-4): Additionally, boasts, bolstered, crucial, delve,
  emphasizing, enduring, garner, intricate/intricacies, interplay, key, landscape,
  meticulously, pivotal, underscore, tapestry, testament, valuable, vibrant.
- Mid-2024 to mid-2025 (GPT-4o): align with, bolstered, crucial, emphasizing,
  enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore,
  vibrant.
- Mid-2025 to mid-2026 (GPT-5): emphasizing, enhance, highlighting, showcasing, plus
  the canned-notability wording above.
- Mid-2026 on (GPT-6): challenge, clearer, dependable, echoed, foster, leverage,
  matters, multifaceted, practical, prioritize, quietly, steady, universally. This
  generation also has a structural signature; see "Narrow sentence-length band".
- Grok has its own list: superficially scientific words ("causal", "empirical",
  "correlate"), and it still overuses "underscore" in 2026.
- In replies to criticism: "concrete" ("concrete evidence", "concrete facts").

Take the lists literally. A word being overused does not make its synonyms overused,
so do not widen "foster" to "nurture" or "showcase" to "display". Read context too:
"underscore" can mean a literal underline or a film score.

### Avoidance of plain copulatives

Generated prose dodges `is`, `are` and `has` with "serves as", "stands as",
"functions as", "operates as", "represents", "marks", "boasts", "features",
"maintains", "offers" and "refers to". One study found `is` and `are` fell by over
10% in academic writing during 2023, and model copyedits remove them further. Newer
output builds longer detours that shade into vague connection: "ventured into
politics as a candidate" for "was a candidate", "began his career as" for "was". In
an opening sentence, "refers to" treats the subject as a word.

Edit: use `is`, `are`, `was`, `has` or a direct verb. (`has been featured` is an
ordinary perfect tense, not this tell.)

### Negative parallelisms

Prose that corrects a misconception no reader held.

- not just X, but (also) Y; not only X, but Y; "it is not just X, it's Y",
- the same move across two sentences, hinged on "however",
- not X, but Y; "it's not X, it's Y"; "no X, no Y, just Z",
- the reversed form, Y rather than X, which is particularly common in recent output:
  "prioritizing empirical consolidation of power rather than ideological purity".

Edit: state Y. Keep the X half only when a reader plausibly believes X.

### Rule of three

Triplets of adjectives or phrases ("adjective, adjective, adjective"; "short phrase,
short phrase, and short phrase") that make thin analysis look complete. The sign is
stronger where nobody would bother with a flourish, such as a change summary.

### Narrow sentence-length band

The mid-2026 generation (GPT-6) writes many more full stops and commas than earlier
models, in shorter sentences held to a band of roughly 8 to 20 words. The prose reads
as tidy and even, with nothing long and nothing abrupt.

Measurable check, on body prose only (skip headings, list items, quotations and
code): split into sentences at terminal punctuation and count the words in each.
The signature is all three together:

- most sentences fall between 8 and 20 words,
- the spread of sentence lengths is low,
- almost no sentence runs past 30 words.

Reference points come from one maintainer's pipeline, the same brief given to two
model families. GPT-6.1 prose had 69 to 89% of its sentences in the band, a standard
deviation of about 5 words, and no sentence over 30 words. Claude prose had 35 to 46%
in the band and a standard deviation of 10 to 12. These are two observations, not
thresholds. A few paragraphs give noisy figures, so read the measure alongside
punctuation monotony (below) and the vocabulary.

Edit: vary length where the content allows. Join two related sentences with a
semicolon or a subordinate clause; let the sentence that carries a qualification run
long; keep a short one where it lands a point. Do not chop long sentences to fit any
band.

## Style and formatting tells

- Title case in headings, capitalising every main word.
- Boldface sprawl: mechanical emphasis, every instance of a chosen term in bold,
  "key takeaways" styling. Some newer apps are told to avoid it.
- Inline-header vertical lists: each item a bold lead-in, a colon, then the text,
  sometimes with no punctuation after the lead-in.
- Bare bullet characters (•, -, –, #, emoji) or typed "1." numbering where the host
  has its own list markup.
- Heading errors: a heading repeating the document's title before the content,
  skipped levels, top-level headings used for every section (Markdown translated
  into another markup), headings that hold nothing but other headings.
- Emoji in front of headings or bullets. Rarer now, still seen.
- Small, barely formatted tables that would read better as prose; Markdown table
  syntax inside another markup's tables.
- Curly quotation marks and apostrophes where the house style uses straight ones,
  or a mix of both in one text. Weak alone: word processors, phone and desktop
  smart-quote settings and professional typesetting all produce curly quotes, and
  some model families do not.
- Punctuation monotony: commas and full stops only, with no semicolons, colons,
  brackets or dashes across a long passage. This is the side effect of newer models
  being hard-coded off em dashes (see "Historical indicators"): with dashes banned,
  they stopped reaching for the alternatives too. The article now treats heavy
  comma-and-full-stop use as a sign of its own, though it flags the frequency claim
  as needing a citation. It pairs with the narrow sentence-length band.

## Assistant leakage

### Collaborative communication

Correspondence, advice or prewriting meant for the user, pasted in as content, or left
inside markup comments.

- Watch phrases: "I hope this helps", "Of course!", "Certainly!", "You're absolutely
  right!", "Would you like...", "is there anything else", "let me know", "more
  detailed breakdown", "here is a", "here's a breakdown", "a Wikipedia-style
  article" (or any "[genre]-style" framing).
- Instructions to the user left in the text: "Delete this section before
  submission", checklists of what the user should have before publishing.
- Clerk or customer-service register in replies: claims to have "carefully
  reviewed", apologies for any inconvenience the writer "may have" caused, "if there
  are specific issues, please point them out", requests to focus on the content
  rather than its origin, assurances that the writer put in their own effort.

### Hedging disclaimers about sources and usage

Tools that search the web often fail to find something and then say it is not
publicly available, pairing that with what the information "likely" is and why it
matters. Both the speculation and the claim of unavailability are unsupported. Since
mid-2026, the disclaimer is often about how a source should be read: a "Y rather than
X" warning that a claim should be treated as tradition, opinion or symbol rather than
fact, or a caution that the evidence "does not establish" some conclusion nobody drew.

- Watch phrases: "While specific details are limited/scarce", "not widely
  available/documented/disclosed", "in the provided/available sources/search
  results", "based on available information", "[claim] should be treated/presented
  as ... rather than ...", "does not by itself establish".

Edit: delete the disclaimer. State what the sources do support; list a real gap under
`Residual risk`.

### Placeholders and templates

- Fill-in-the-blank scaffolds left unfilled: "[Entertainer's Name]", "(Add your
  channel URL here)", "(If available)".
- Placeholder dates such as `2025-xx-xx` in citation fields, usually the access date.
- Comments saying text or images should be added when sources become available.
  Check first that the comment is not boilerplate from the host's own template.

## Markup and citation artefacts

### Markup leakage

- Markdown where the host uses other markup: `#` headings, `**bold**` or `*bold*`,
  `[text](example.com)` links, `---` breaks between every section, `##` read by the
  host as a numbered list. Markdown alone is weak evidence, since plenty of people
  write it. Markdown mixed with broken native markup, or wrapped in a fenced code
  block, is strong.
- Broken or malformed native markup: unclosed brackets and templates, garbled
  generated dates.
- Hallucinated categories, templates and template parameters, including plausible
  names that never existed and ones deleted before the model's cutoff. Categories with
  words dropped ("Category people") are a strong tell. Other bad categories are
  common human errors and only corroborate.
- `:::writing{variant="document" id="12345"}` wrappers, sometimes closed with `:::`.
  Seen from June 2026; source unclassified.
- `↩` characters around footnotes.

### Tool-specific reference markers

Leaked internal formatting is close to proof that the text came from a model.

- ChatGPT: `:contentReference[oaicite:0]{index=0}`, `oai_citation`, `Example+1` or
  `Microsoft Learn+3`, `citeturn0search0` and `turn0search0` (also `turn0news0`,
  `turn1file0`, `iturn0image0turn0image1`), the bare number in private-use
  characters, ref names such as `0search12`, and
  `({"attribution":{"attributableIndex":"3795-0"}})`.
- Gemini: `[cite: 17]`, `[cite: 3, 12, 13]`, and `[span_2](start_span)` ...
  `[span_2](end_span)` around claims.
- Grok: `<grok-card data-id="e8ff4f" data-type="citation_card">` (`grok_card`) and
  `[](grok_render_citation_card_json={"cardIds":["3bb883"]})`.
- DeepSeek: lenticular brackets with daggers and line ranges, `【29†L582-L589】`. The
  same output can run stripped link domains into the sentence: "pedestrian
  enhancements as prioritiesmedway.gov.ukmedway.gov.uk."
- Perplexity: `[attached_file:1]` and `[web:1]` at the ends of sentences;
  `ppl-ai-file-upload` in cited storage URLs.

### Citation problems

- Several broken external links that no web archive holds. One dead link is link rot;
  also allow for paywalled links and URLs mangled by bots or a bad paste.
- Invalid ISBN checksums, DOIs that do not resolve, and DOIs that resolve to an
  unrelated article.
- Book citations with no page number, or with pages that do not support the claim,
  typically for a general, widely cited book with no link to a searchable copy.
- Tracking parameters left in URLs: `utm_source=openai`, `utm_source=chatgpt.com`,
  `utm_source=copilot.com`, `referrer=grok.com`. These show a tool found the link,
  not that it wrote the prose.
- Named references declared but never used; reference-reuse syntax repeated wrongly
  after every sentence; low-numbered database IDs that point at irrelevant papers.
- Fabricated or mismatched citations.

## Miscellaneous

- A pronounced shift in style, vocabulary or register between sections, or against
  the writer's other writing (flawless prose next to rough messages). Someone who has
  used these tools for years tends to drift with each model generation. The reverse
  holds too: a style unchanged since before 2022 argues against a model. Non-native
  writers mix English varieties, and many people write more formally in some venues,
  so only a dramatic, unexplained shift counts.
- References to policies, guidelines, standards or shortcuts that do not exist, and
  misquotation of real ones.
- Models differ. Each has an idiolect. In late-2024 comparisons, ChatGPT and Grok
  dwelt on broader context more than Gemini and Claude, whose answers were also more
  concise.
- Bias in content: as of 2026, several frontier models show a pro-authoritarian lean
  on some political prompts (more so in Chinese-language answers) and criticise
  governments in freer countries more readily than repressive ones. Check political
  framing against sources.

## Signs of human writing

Read these before concluding. They argue against a model as the writer.

- The text predates 30 November 2022, ChatGPT's public launch.
- The writer can explain their choices, mistakes included, and produce the real
  source when asked.
- Syntax that models, aiming at a "formal, neutral" tone, avoid:
  - simple "there is" and "it has" phrases,
  - plain verbs: wrote, moved, used, tried, died (not authored, relocated, utilised,
    attempted, passed away),
  - true superlatives and definite claims: "one of the best", "the only", "the
    first",
  - ordinary qualifiers and intensifiers: very, perhaps, tends to,
  - the occasional wordy construction: "as a result of", "in order to", "all of
    the", "the fact that".
- Idiosyncratic, non-standard syntax and a personal voice.

An edit must not strip these out. Replacing "wrote" with "authored", or deleting
every "perhaps", moves a human draft towards the model register.

## Ineffective indicators

Weak or misleading alone, and some point the other way. Do not flag a text on these:

- Perfect grammar. Many writers are skilled or trained.
- A mix of casual and formal registers, or prose that sounds both clinical and
  emotional. It may be a technical writer being casual, youth, playfulness,
  neurodivergence, or several authors.
- "Bland" or "robotic" prose. Model output skews positive and verbose, which few
  readers would call robotic.
- "Fancy", academic or formal prose in general. The overused items are specific
  words, and formality as a whole does not correlate.
- Transition words in isolation ("Additionally", "Consequently", "Notably"). Only a
  few are overused, and style guides accept them.
- Unsourced content. Most unsourced text predates these tools, and current tools cite
  readily, if not always accurately.
- Correct native markup, or one inexplicable markup glitch, which is more often an
  editor or a buggy tool.
- Detector-tool output (see "Caveats").
- A single vocabulary word, em dash or rule of three in otherwise grounded prose.

## Historical indicators

Common in older output and rarer now; still useful for older text. Dates are
approximate.

- Knowledge-cutoff disclaimers (2022 to 2023): "up to my last training update", "as
  of my last knowledge update", speculation about sources it "cannot access".
- Didactic disclaimers (November 2022 to 2024): "it's important/critical/crucial to
  note/remember/consider", "worth noting", "may vary", often safety advice to an
  imagined reader.
- Section summaries and "Conclusion" sections: "In summary", "In conclusion",
  "Overall", and paragraphs that end by restating themselves.
- Prompt refusals: "as an AI language model", "I cannot offer medical advice, but I
  can...", apologies.
- Abrupt cut-offs where generation hit a limit. A bad paste or a copyright problem can
  look the same.
- Access dates unexpectedly old relative to the edit (a citation added in December
  2025 with an access date of December 2024). Copied citations and offline work cause
  this too.
- Lexical diversity, or elegant variation: needless synonyms to avoid repeating a
  simple noun, a side effect of the repetition penalty in older models. It does not
  apply across pieces generated separately, and many non-native writers are taught to
  avoid repetition.

### Em dashes (2022 to September 2026)

Models used em dashes far more than non-professional writers in the same genre, in
places a person would put a comma, brackets, a colon or a hyphen. They used them
formulaically, as a hinge to punch up a clause or a parallelism, and often with
spaces either side against typographic convention. The habit showed most in
discussion and least in article text.

Vendors then suppressed it. OpenAI tuned GPT-5.1 against dashes, and a July 2026 study
found that of current models only Claude used em dashes more than professional
writers, while ChatGPT used fewer. From September 2026 the newest models are
increasingly hard-coded not to use them at all. Older models stay in use, so a
dash-heavy draft is still a weak clue, and a draft with no dashes proves nothing. The
current tell is the side effect: see punctuation monotony under "Style and formatting
tells".

When removing a dash, choose by function: a semicolon between related clauses,
brackets for an aside, a colon before an explanation, or two sentences of different
lengths. Do not reach for a comma by default.
