# Signs of AI writing

A taxonomy of clues, not proof of authorship. Weigh clusters, and read the last two
sections before concluding anything. A sign points at a problem: rewording a tell
while the unsourced claim, puffery or invented citation stays underneath only hides
it. Fix the substance or flag it. Quoted watch words keep the American spelling
models emit; search for them as written.

## Content

**Regression to the mean.** The root of most content tells: the specific, unusual
fact gets swapped for generic, positive, important-sounding description, so
"inventor of the first train-coupling device" becomes "a revolutionary titan of
industry". Ask whether the description could be more specific; if the sources hold
the fact, put it back, otherwise cut or flag.

**Inflated significance.** The subject is important, pivotal, enduring or part of a
broader shift, with no information added. Mundane material (an etymology, a
population table) gets a statement of wider importance, sometimes after admitting the
subject is minor; the subject is placed amid "debates"; species writing belabours
ecosystem links and conservation status; newer output editorialises that a
distinction "matters". Watch: "stands/serves as", "is a testament/reminder", "a
crucial/pivotal/vital/key role/moment", "underscores/highlights its importance",
"reflects broader", "symbolizing its enduring/lasting", "setting the stage for",
"marking/shaping the", "represents/marks a shift", "key turning point", "evolving
landscape", "focal point", "indelible mark", "deeply rooted", "distinction matters
because".

**Canned notability.** Importance proved by describing sources rather than saying
what they found. Watch: "independent coverage", "local/regional/national media
outlets", "trade publications", "cited/featured/profiled in", "written by a leading
expert", "maintains an active social media presence". Also the model's own gloss
attributed to a named source ("Roger Ebert highlighted the lasting influence").

**Superficial analysis.** Interpretive gloss on ordinary facts, usually a trailing
`-ing` phrase: "highlighting/underscoring/emphasizing", "ensuring", "reflecting/
symbolizing", "contributing to", "cultivating/fostering", "encompassing",
"enhancing", "valuable insights", "align/resonate with". Synthetic opinion ("generated
debate", "drew praise") with no source.

**Promotional tone.** Press-release or travel-guide cadence in a neutral brief:
"boasts a", "vibrant", "rich", "profound", "showcasing", "exemplifies", "commitment
to", "natural beauty", "nestled", "in the heart of", "groundbreaking", "renowned",
"featuring", "diverse array"; constant reminders of cultural heritage. Newer models
are subtly rather than blatantly positive and avoid flat superlatives. A rewrite that
claims to remove promotional tone and adds it is a tell.

**Vague connection.** "Connected with", "associated with", "in connection/association
with" where the source states a plain relationship: "Jane Doe taught science at
Example University" becomes "was connected with science education at". Often stacked
or intensified ("widely associated"). State the relationship or flag the gap.

**Vague attribution.** "Industry reports", "observers have cited", "experts argue",
"several sources" when few are cited; plural "reviewers" for one person; "such as"
before the whole list; one or two sources presented as a widely held view.

**Outline endings.** "Despite its [positives], [subject] faces challenges...", closing
on a vague positive or future initiatives; standalone "Challenges and Legacy" or
"Future Outlook" sections. Only the formula counts.

**Headings and leads.** "X and Y" headings, above all "Awards and recognition". Leads
that treat a list or topic as a named entity: "**List of tallest buildings** is...",
"**Sustainable urban transport** refers to the...".

## Language

**Vocabulary clusters.** One word is chance; many, repeatedly, is among the strongest
tells. Take the lists literally: overuse of "foster" says nothing about "nurture",
and "underscore" can mean an underline or a film score. The cluster drifts by era:

- 2023 to mid-2024 (GPT-4): Additionally (opening a sentence), boasts, bolstered,
  crucial, delve, emphasizing, enduring, garner, intricate/intricacies, interplay, key
  (adjective), landscape (abstract), meticulously, pivotal, underscore, tapestry
  (abstract), testament, valuable, vibrant; also deep dive, highlight (verb), robust,
  showcase.
- Mid-2024 to mid-2025 (GPT-4o): align with, bolstered, crucial, emphasizing, enhance,
  enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant.
- Mid-2025 to mid-2026 (GPT-5): emphasizing, enhance, highlighting, showcasing, plus
  canned-notability wording.
- Mid-2026 on (GPT-6): challenge, clearer, dependable, echoed, foster, leverage,
  matters, multifaceted, practical, prioritize, quietly, steady, universally.
- Grok: pseudo-scientific "causal", "empirical", "correlate"; still "underscore".
- Replies to criticism: "concrete" ("concrete evidence").

**Avoided copulatives.** "Serves as", "stands as", "functions as", "represents",
"marks", "boasts", "features", "maintains", "offers", "refers to" for `is`/`has`;
newer detours shade into vague connection ("ventured into politics as a candidate").
"Has been featured" is an ordinary perfect tense, not this tell.

**Negative parallelisms.** Correcting a misconception nobody held: "not just X, but
Y", "not only", "it's not X, it's Y", "no X, no Y, just Z", the two-sentence version
hinged on "however", and the reversed "Y rather than X", now especially common. Keep
X only when a reader plausibly believes it.

**Rule of three.** Triplets that make thin analysis look complete; strongest where no
one would bother with a flourish, such as a change summary.

**Narrow sentence-length band.** The GPT-6 signature. On body prose only (skip
headings, lists, quotations, code), count words per sentence. The tell is all three
together: most sentences 8 to 20 words, low spread, almost none over 30. Observed:
GPT-6.1 put 69 to 89% of sentences in the band with a standard deviation near 5;
Claude 35 to 46% with 10 to 12. Two observations, not thresholds, and noisy on a few
paragraphs. Fix by varying length where the content allows; never chop to fit a band.

## Style and formatting

- Title case headings; bold sprawl and "key takeaways" styling; inline-header lists
  (bold lead-in, colon, text).
- Bare bullet characters (•, –, emoji) or typed "1." where the host has list markup.
- Heading errors: repeating the title, skipped levels, every section top-level,
  headings holding only other headings. Emoji before headings or bullets.
- Small tables that should be prose.
- Curly quotes against a straight-quote house style, or both mixed. Weak alone.
- **Punctuation monotony:** commas and full stops only, no semicolons, colons,
  brackets or dashes across a long passage. The side effect of models being trained
  off em dashes; pairs with the sentence-length band.
- **Em dashes:** heavy, formulaic dashes (often spaced) were the 2022 to 2025 tell.
  Vendors have since suppressed them; only Claude still exceeds professional writers.
  A dash-heavy draft is a weak clue and a dashless one proves nothing.

## Assistant leakage

- Chat addressed to the user: "I hope this helps", "Certainly!", "You're absolutely
  right!", "Would you like...", "let me know", "here's a breakdown", "a
  Wikipedia-style article" (any "[genre]-style" framing); instructions left in
  ("Delete this section before submission").
- Clerk register in replies to criticism: "carefully reviewed", apologies for any
  inconvenience, asking to focus on content rather than origin.
- **Source disclaimers:** "While specific details are limited", "not widely
  available/documented", "in the provided sources/search results", "based on available
  information", plus speculation about what the information "likely" is. Newer: "[claim]
  should be treated as ... rather than ...", "does not by itself establish" a
  conclusion nobody drew. Delete; state what sources support; put a real gap under
  `Residual risk`.
- Unfilled placeholders: "[Entertainer's Name]", "(Add your channel URL here)",
  `2025-xx-xx` access dates, comments promising content when sources appear (check
  they are not the host's own template).
- Older output: knowledge-cutoff lines, "it's important to note", "may vary", "In
  summary/In conclusion" paragraphs, "as an AI language model", abrupt cut-offs,
  access dates long before the edit, needless synonyms for a repeated noun.

## Markup and citations

- Markdown in a host that uses other markup (`#`, `**bold**`, `[text](url)`, `---`
  between sections). Weak alone; strong mixed with broken native markup or inside a
  code fence.
- Hallucinated categories, templates and parameters; dropped-word categories
  ("Category people") are strong.
- `:::writing{variant="document" id="12345"}` wrappers; `↩` around footnotes.
- Tool markers, close to proof:
  - ChatGPT: `:contentReference[oaicite:0]{index=0}`, `oai_citation`, `Example+1`,
    `citeturn0search0`, `turn0news0`, `turn1file0`, `iturn0image0turn0image1`,
    private-use characters around a number, ref names like `0search12`,
    `({"attribution":{"attributableIndex":"3795-0"}})`.
  - Gemini: `[cite: 17]`, `[cite: 3, 12, 13]`, `[span_2](start_span)` ...
    `[span_2](end_span)`.
  - Grok: `<grok-card data-id="e8ff4f" data-type="citation_card">`,
    `[](grok_render_citation_card_json={"cardIds":["3bb883"]})`.
  - DeepSeek: `【29†L582-L589】`, and stripped domains run into the sentence
    ("prioritiesmedway.gov.ukmedway.gov.uk").
  - Perplexity: `[attached_file:1]`, `[web:1]`, `ppl-ai-file-upload` URLs.
- `utm_source=openai`, `utm_source=chatgpt.com`, `utm_source=copilot.com`,
  `referrer=grok.com`: a tool found the link, not necessarily wrote the prose.
- Several dead links no archive holds; bad ISBN checksums; DOIs that fail or point
  elsewhere; book citations without pages or with pages that do not support the
  claim; unused named references; reference reuse after every sentence; low database
  IDs pointing at irrelevant papers.

## Other

- A dramatic, unexplained shift in style or register between sections, or against
  the writer's other writing. A style unchanged since before 2022 argues against a
  model.
- Policies, standards or guidelines that do not exist, or misquoted real ones.
- Political framing: several frontier models lean pro-authoritarian on some prompts.
  Check against sources.

## Signs of human writing

Text from before 30 November 2022; a writer who can explain choices and produce
sources; "there is" and "it has"; plain verbs; true superlatives; ordinary qualifiers;
the occasional wordy "in order to" or "the fact that"; idiosyncratic syntax. An edit
must not strip these out.

## Indicators that do not work

Perfect grammar; mixed registers; "bland" or "robotic" prose; formality in general;
isolated transitions ("Additionally", "Notably"); unsourced content; one markup
glitch; detector scores (beaten by paraphrase, and people judge at near chance); a
single vocabulary word, dash or triplet in otherwise grounded prose.
