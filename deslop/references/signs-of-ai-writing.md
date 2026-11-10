# Signs of AI writing

A taxonomy of tells to edit. Edit clusters; a lone instance is ordinary writing. A
tell points at a problem: rewording it while the unsourced claim, puffery or invented
citation stays underneath only hides it. Fix the substance or flag it. Quoted watch
words keep the American spelling models emit; search for them as written.

## Content

**Regression to the mean.** The root of most content tells: the specific, unusual
fact gets swapped for generic, positive, important-sounding description, so
"inventor of the first train-coupling device" becomes "a revolutionary titan of
industry". Ask whether the description could be more specific; if the sources hold
the fact, put it back, otherwise cut or flag.

**Inflated significance.** The subject is important, pivotal, enduring or part of a
broader shift, with no information added. Mundane material (an etymology, a
population table) gets a statement of wider importance, sometimes after admitting the
subject is minor; the subject is placed amid "debates"; the text editorialises that a
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
"featuring", "diverse array"; constant reminders of cultural heritage. It can be
subtle: steadily positive with no flat superlatives. Check that your rewrite has not
added any.

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

## Language

**Vocabulary clusters.** One word is chance; many, repeatedly, is among the strongest
tells. Take the list literally: overuse of "foster" says nothing about "nurture",
and "underscore" can mean an underline or a film score.

Additionally (opening a sentence), align with, boasts, bolstered, challenge, clearer,
crucial, deep dive, delve, dependable, echoed, emphasizing, enduring, enhance, foster,
garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape
(abstract), leverage, matters, meticulously, multifaceted, pivotal, practical,
prioritize, quietly, robust, showcase, steady, tapestry (abstract), testament,
underscore, universally, valuable, vibrant; pseudo-scientific "causal", "empirical",
"correlate"; "concrete" as an intensifier ("concrete evidence").

**Avoided copulatives.** "Serves as", "stands as", "functions as", "represents",
"marks", "boasts", "features", "maintains", "offers", "refers to" for `is`/`has`;
some detours shade into vague connection ("ventured into politics as a candidate").
"Has been featured" is an ordinary perfect tense, not this tell.

**Negative parallelisms.** Correcting a misconception nobody held: "not just X, but
Y", "not only", "it's not X, it's Y", "no X, no Y, just Z", the two-sentence version
hinged on "however", and the reversed "Y rather than X". Keep X only when a reader
plausibly believes it.

**Rule of three.** Triplets that make thin analysis look complete; strongest where no
one would bother with a flourish, such as a change summary.

**Narrow sentence-length band.** On body prose only (skip headings, lists,
quotations, code), count words per sentence. The tell is all three together: most
sentences 8 to 20 words, low spread, almost none over 30. Noisy on a few paragraphs.
Fix by varying length where the content allows; never chop to fit a band.

## Style and formatting

- Title case headings; bold sprawl and "key takeaways" styling; inline-header lists
  (bold lead-in, colon, text).
- Bare bullet characters (•, –, emoji) or typed "1." where the host has list markup.
- Heading errors: repeating the title, skipped levels, every section top-level,
  headings holding only other headings. Emoji before headings or bullets.
- Small tables that should be prose.
- Curly quotes against a straight-quote house style, or both mixed. Weak alone.
- **Punctuation monotony:** commas and full stops only, no semicolons, colons,
  brackets or dashes across a long passage. Pairs with the sentence-length band.
- **Em dashes:** heavy, formulaic dashes, often spaced. A lone dash is ordinary.

## Assistant leakage

- Chat addressed to the user: "I hope this helps", "Certainly!", "You're absolutely
  right!", "Would you like...", "let me know", "here's a breakdown", "a
  Wikipedia-style article" (any "[genre]-style" framing); instructions left in
  ("Delete this section before submission").
- **Source disclaimers:** "While specific details are limited", "not widely
  available/documented", "in the provided sources/search results", "based on available
  information", plus speculation about what the information "likely" is; "[claim]
  should be treated as ... rather than ...", "does not by itself establish" a
  conclusion nobody drew. Delete; state what sources support; put a real gap under
  `Residual risk`.
- Unfilled placeholders: "[Entertainer's Name]", "(Add your channel URL here)",
  `2025-xx-xx` access dates, comments promising content when sources appear (check
  they are not the host's own template).
- Knowledge-cutoff lines, "it's important to note", "may vary", "In summary/In
  conclusion" paragraphs, "as an AI language model", abrupt cut-offs, needless
  synonyms for a repeated noun.

## Markup and citations

- Markdown in a host that uses other markup (`#`, `**bold**`, `[text](url)`, `---`
  between sections).
- `:::writing{variant="document" id="12345"}` wrappers; `↩` around footnotes.
- Tool markers. Remove them, and check the claim each was attached to:
  - `:contentReference[oaicite:0]{index=0}`, `oai_citation`, `Example+1`,
    `citeturn0search0`, `turn0news0`, `turn1file0`, `iturn0image0turn0image1`,
    private-use characters around a number, ref names like `0search12`,
    `({"attribution":{"attributableIndex":"3795-0"}})`;
  - `[cite: 17]`, `[cite: 3, 12, 13]`, `[span_2](start_span)` ... `[span_2](end_span)`;
  - `<grok-card data-id="e8ff4f" data-type="citation_card">`,
    `[](grok_render_citation_card_json={"cardIds":["3bb883"]})`;
  - `【29†L582-L589】`, and stripped domains run into the sentence
    ("prioritiesmedway.gov.ukmedway.gov.uk");
  - `[attached_file:1]`, `[web:1]`, `ppl-ai-file-upload` URLs.
- Tracking parameters on links: `utm_source=openai`, `utm_source=chatgpt.com`,
  `utm_source=copilot.com`, `referrer=grok.com`. Strip the parameter and check the
  link supports the claim.
- Several dead links no archive holds; bad ISBN checksums; DOIs that fail or point
  elsewhere; book citations without pages or with pages that do not support the
  claim.

## Register shift

A dramatic, unexplained shift in style or register between sections usually marks a
pasted-in passage. Edit it to the surrounding voice.
