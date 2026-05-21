# Signs of AI Writing

Use this as a taxonomy of clues, not proof of authorship.

## Content Tells

### Inflated Significance

Prose insists a subject is important, pivotal, enduring, emblematic, or part of a broader shift without adding concrete information.

Common pattern:

- blurry high-status summary replaces a precise fact,
- gestures at "legacy", "impact", or "the evolving landscape",
- subject is framed as symbolic when the source material is mundane.

### Notability By Assertion

Copy tries to prove importance by naming outlets, coverage, or "independent sources" rather than summarizing what those sources actually say.

Common pattern:

- source roll-calls,
- "featured in" laundry lists,
- "maintains an active social media presence",
- separate "media coverage" sections that are just inventories.

### Superficial Analysis

Shallow interpretive gloss pasted onto ordinary facts.

Common pattern:

- trailing `-ing` phrases that force a moral or thematic reading,
- abstract verbs like "underscoring", "highlighting", "fostering", "reflecting",
- claims of significance with no attributable reasoning.

### Promotional Tone

Marketing, branding, institutional self-description, or puff-piece cadence.

### Vague Attribution

Authority with no owner: "experts argue", "observers note", "researchers say".

### Outline-Style Endings

Conclusion paragraphs that summarize "challenges", "future prospects", or "broader implications" in generic terms.

## Language Tells

### AI Vocabulary Density

Watch for clusters, not single words:

- additionally
- align with
- bolstered
- boasts
- crucial
- delve
- emphasizing
- enduring
- enhance
- foster
- garner
- highlight
- interplay
- intricate
- key
- landscape
- meticulous
- multifaceted
- nuanced
- pivotal
- showcase
- tapestry
- testament
- underscore
- valuable
- vibrant

The specific words change; the underlying pattern is inflated register and synonym-swapping to avoid plain language.

### Avoidance Of Plain Copulatives

Generated prose often dodges `is` and `are` with inflated structures like "serves as", "stands as", "represents", "marks", "boasts", "features", "maintains", or "offers".

Edit move: use `is`, `are`, `was`, or a direct verb.

### Negative Parallelisms

Common patterns:

- not just X, but Y
- not only X, but Y
- not X, but Y
- this is not A; it is B

Default edit: rewrite as a direct statement.

### Rule Of Three

Repeated triplets of adjectives or phrases can make weak analysis sound finished.

### Elegant Variation

Needless synonym swapping avoids repeating a simple noun even when repetition would be clearer.

## Style And Formatting Tells

- Title case drift.
- Boldface sprawl.
- Inline-header vertical lists.
- Emoji in contexts where the house style would not use them.
- Frequent em dashes as an all-purpose dramatic hinge.
- Tables where prose or a simple list would be more natural.
- Decorative thematic breaks or heading-level skips.

## Assistant Leakage

Strong signs that assistant output leaked directly:

- "let's explore",
- "here's a breakdown",
- "we can also",
- "I hope this helps",
- "as of my last update",
- generic templates or fill-in-the-blank scaffolds.

## Markup And Citation Artifacts

Watch for:

- Markdown leakage in non-Markdown contexts,
- broken native markup,
- `turn0search0`, `turn1search3`, or similar retrieval markers,
- `contentReference`,
- `oaicite`,
- `oai_citation`,
- `attached_file`,
- `grok_card`,
- `attribution`,
- `attributableIndex`,
- non-existent categories/templates,
- fabricated or mismatched citations.
