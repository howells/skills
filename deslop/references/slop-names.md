# Slop names

The stock names language models reach for when they invent a person, place or
company for an example, a piece of sample data, a story or a demo. One such name
proves nothing. A cast of them, or one that does not fit the setting, is a tell that
nobody chose the name.

> **Source.** Compiled from the studies, writeups and reader reports listed under
> "Sources" at the end, last checked on 24 October 2026. No single authoritative list
> exists, and the best studies date from May and June 2026. Each name below carries
> its evidence tier. Re-check the measured claims when a new model generation ships,
> because the lists move with each release.

## Caveats

- Name habits are era-bound and family-bound. In the one study that tracked Claude
  checkpoints, "Elena Rodriguez" was absent from every checkpoint by October 2025 and
  the Elena Vasquez and Marcus Chen pairing was close to extinct by sonnet-4-6
  (Brzozowski and Chung). Treat every list here as a snapshot.
- The measurements found use creative-writing prompts: "write a story", "a name for a
  character in a novel", "a fictional expert". None found measures names in business
  examples, test data or demos, which is where the tell is most often met. The same
  habit probably carries over, but only anecdotes say so.
- A stock name is a clue, not proof of authorship. Real people are called Chen,
  Marcus and Priya, and the Ghost Couple authors note that some of the "ghost" names
  they traced may belong to real researchers. Weigh the cluster and the fit.
- Sources disagree on cause. Hamilton and Mimno point to post-training preference
  data. Max Read suggests game-forum and fan-wiki text. Laura Wattenberg argues a
  name with no human baggage and a smooth sound wins. None has been shown to be the
  cause. Do not explain the cause in an edit note.

## Names, by strength of evidence

### Measured

A controlled sample, with a figure and a model attached.

- **Elara.** The best-supported name. 85,513 times more frequent than in human text in
  gemma-3-12b stories, against a wordfreq baseline (Paech et al., Antislop). In 13.1%
  of 20,000 "write a story" outputs pooled across Claude Haiku 4.5, Gemini 3.1
  Flash-Lite, GPT-5.4-Mini and OLMo 7B Thinking (Hamilton and Mimno). Chris Thomas's
  informal test found it from GPT 5.4, Sonnet 4.6, Gemini 3.1, DeepSeek, Qwen, Kimi
  and Gemma, with no counts. Tied to every family. As "Elara Voss", it is the GPT
  name in the Ghost Couple probe, at 23% on solo prompts.
- **Elias and Mara.** 26.5% and 16.7% of the same 20,000 stories (Hamilton and
  Mimno). Pooled across four models, so no family split.
- **Marcus, and Marcus Chen.** Claude. Sonnet 4.5 returned "Marcus Chen" 100 times
  out of 100 for "a name for a software developer in a novel" (Voss, seehuhn.de), and
  "Marcus" for a protagonist's husband in 34 of 100. Across 37,500 draws from five
  Claude models, "Marcus" was picked 4,367 times: 23.6% of the 18,503 male-name
  draws, or 11.65% of all 37,500 draws. Opus 4.5 returned it
  100 out of 100 on the simple prompt (benjismith/ai-randomness). Marcus is also in
  1,822 of the 20,000 Hamilton and Mimno stories, so it is not only Claude.
- **Elena Vasquez.** Claude. 66% of single "fictional expert" prompts on
  claude-sonnet-4-20250514, falling to 6% on sonnet-4-6 and 10% on opus-4-7 (30
  prompts per checkpoint; Brzozowski and Chung). "Elena Rodriguez" was the older
  Claude default, last seen at 16% on opus-4 (May 2025).
- **Amara Okafor (or Okonkwo).** The third name of a Claude trio with Elena Vasquez
  and Marcus Chen, mostly on the Opus line, peaking at 20% of trio prompts. Dead by
  August 2025 on those checkpoints (Brzozowski and Chung).
- **Aris Thorne and Lena Petrova.** Gemini. Aris Thorne in 93% of single prompts on
  gemini-2.5-flash, the pair in 37% (Brzozowski and Chung; one Gemini checkpoint
  only).
- **Eleanor, Thomas, Kira Voss.** Role prompts to Sonnet 4.5, 100 runs each (Voss,
  seehuhn.de): Eleanor for 80 of 100 protagonists' wives, and for all 100 of "a woman
  in York"; Thomas for 99 of 100 "a man in York"; Kira (Voss 31, Vance 19, Vex 10) for
  a spaceship pilot.

### Measured, but lower or indirect

- **Sarah Chen.** The user-reported Claude classic is not a high-frequency measured
  name. The Ghost Couple probe found "Sarah Chen" in 0% to 13% of single prompts
  depending on checkpoint (13% on haiku-4.5, 0% on the newest), and "Sarah" appears
  in 685 of the 20,000 Hamilton and Mimno stories. Its reputation rests on
  anecdote (see below). The probe asked for fictional experts, not sales reps or
  customers, so the gap may be a prompt effect; that is a guess, not a finding.
- **Clara, Lila, Maya, Mira, Elian.** 1,260, 1,262, 633, 418 and 420 of the 20,000
  Hamilton and Mimno stories. "Lila" is the measured one; do not read it as "Lily".

### Anecdotal or unverified

A person noticed it. There is no count behind it.

- **Priya, Priya Shah, Priya Sharma.** The strongest anecdote here, and a name to
  flag in Claude output on sight. The maintainer sees it come up time and again, and
  so do friends who use Claude: invented colleagues, reps, customers and experts
  called Priya, most often Priya Shah (Claude named a sales rep "Priya Shah" in
  October 2026). The Ghost Couple paper asserts, in an appendix, that Priya is the
  first name that displaces Elena in newer Claude outputs, and cites two
  fake-testimonial sites (Priya Natarajan, Priya Sharma). No published count backs
  it yet: the paper's own results section holds no Priya data, and no Priya appears
  in the seehuhn or ai-randomness runs, which used story and role prompts rather than
  business examples. Treat it as stock when you edit; say it is reported, not
  measured, if you have to explain why.
- **Sarah Chen, as a go-to expert.** Reported by Michael Wagner (Claude, no
  measurements), by Nicolas Cole as "Red Flag #10" for AI-written posts (Threads; seen
  only as a search result), and by a reader who found Claude Sonnet 4 putting "not
  one, but two Sarah Martinez's" and "a Teresa Chen" into a novel (AI Central comment).
- **Kai, Lyra.** Named as consistent Claude outputs in Wagner's post, which cites a
  Reddit thread rather than a count.
- **Lena, Lyra, Maya, Clara, Elena.** Appear in Laura Wattenberg's informal 15-name
  test (three chatbots, five genre prompts), which gives no counts to quote.
- **Kael, Kaelen.** Antislop names "Kael" next to Elara as a fixated name but gives
  no figure for it. A Goodreads list calls it ChatGPT's top male name; that is one
  reader's claim.
- **Lily.** Appears in a name list in one Medium post that could not be retrieved.
  No other source found.
- **Dr. Elara Voss and variants** (Elara Vex, Elena Voss, Elias Vance, Dr. Elara
  Finch, Dr. Elara Solis). Max Read's essay is a real check of Amazon, but the
  variants come from linked Reddit and Twitter posts. He counted 62 Amazon books
  credited to "Elara Voss" in August 2025 and could find no earlier instance of the
  name than August 2023.
- **Unretrieved.** A large X article by TomLikesRobots ("Everyone's Name Is Elara")
  reports a five-model, 1,000-opening test and a ranked blocklist (Elara, Eira,
  Kaelen, Thorne, Hawk, Kael, Lyra, Arin, Emilia, Lena, Maya, Mara, Marcus, Elias).
  The page returned HTTP 402, so the figures are unchecked. Look there for a ready
  blocklist file.

### Searched for, no source found

Patel, Shah and Nakamura as stock surnames; Willowbrook, Millbrook and Oakhaven as
stock places; Acme and similar stock company names. Nothing found ties them to a
model. Do not flag them as slop names on the strength of this file. Flag them, if at
all, as stock choices the writer should replace for being generic.

## Surnames

Surnames hold while first names drift. Brzozowski and Chung found "Okonkwo" standing in
for "Okafor", and "Marcus Williams" and "Victoria Chen" turning up on fake pages, so a
swapped first name leaves the tell in place.

- **Chen.** Claude. Marcus, Michael, David, Sarah, Mara and Victoria Chen all turn up
  (seehuhn.de; Brzozowski and Chung). Wagner's Reddit sources report Chen on
  characters in 1920s France.
- **Vasquez, and older Rodriguez.** Claude (Brzozowski and Chung; Laforge saw "Elana
  Vasquez" from Claude Opus 4).
- **Okafor, Okonkwo.** Claude's Opus line (Brzozowski and Chung).
- **Voss, Vance, Vex.** Across families. Wattenberg: "when a surname is required for
  these characters, the AIs favor Voss or Vance". Kira Voss, Vance and Vex in the
  Sonnet 4.5 pilot test (seehuhn.de); Elara Voss for GPT.
- **Thorne, Petrova.** Gemini (Brzozowski and Chung). Laforge found "Dr Thorne" 204
  times in 26 Kaggle sci-fi book descriptions, by a Gemini CLI count with no baseline.
- **Hargreaves, Hartley, Ashworth, Whitby.** Claude Sonnet 4.5, asked for a man or
  woman in York (seehuhn.de). Asking for a region returns a small stock pool for that
  region, not the region's range of names.
- **Sharma.** Priya Sharma on a fake-testimonial site, Anya and Anika Sharma among
  co-authors of a ghost "Marcus Chen" (Brzozowski and Chung). No frequency data.

## Places, settings and roles

- **Eldoria.** A Goodreads list of AI-generated books using the name had 188 entries
  when fetched; its creator attributes it to ChatGPT in fantasy prompts. Wattenberg
  also lists it. Aethelgard is described there as the next most common (about 90
  books; seen in a search result only). These are readers' lists, not measurements.
- **Whispering Woods, Eldora.** Reported in Max Read's essay from Reddit and Twitter
  posts. Secondhand.
- **Lighthouse, village, attic.** The measured settings: lighthouse in 51.2% of
  20,000 stories, village in 4,155, attic in 1,978 (Hamilton and Mimno).
- **Roles.** Keeper (48.1%), baker, mayor, clockmaker, fisherman, librarian, in the
  same study. The pattern is a name, a trade and a place arriving as a set: 49.1% of
  stories held all three.

## Edits

- **Name the role or drop the name.** If the draft invents a person only to carry an
  example, "a sales rep" does the job. Do not replace one invented person with
  another.
- **Take names from the setting.** Use the region, decade, age, role and community the
  example is about. Source them from something real: a census or registry surname
  table for that place and period, a staff directory, the user's own contacts, the
  names already in the draft.
- **Vary across a set.** Differ in origin, length, first letter and age. The names
  above lean on E, L and M initials and -a endings, so a cast that is all of those is
  worth a second look.
- **Do not swap stock for stock.** Replacing Sarah Chen with Priya Shah, or Elara with
  Lyra, keeps the tell. Antislop's own replacement tokens for "Elara" (Madelyne, Nadia,
  Freya, Isolde) are illustrations, not a safe list. Any list a model produces for you
  is the next stock list.
- **Check fit.** A Chen in 1920s France, a Vasquez in a story set in York, a
  Hargreaves at a Lagos fintech: the name is working against the setting. Fix the
  match before the variety.
- **Real names are not yours to change.** Quoted material, named sources and real
  people keep their names. Apply the guardrails in `SKILL.md`.

## What not to flag

- One common name in a document. Chen is among the most common surnames in the world,
  and Marcus, Sarah and Maya are ordinary names.
- A name the writer gave, or can explain.
- A name in a story or example that predates November 2022.
- A name that fits and was plainly chosen: a family, a client or a place the text
  already describes.

The tell is the cast taken together (Elena Vasquez, Marcus Chen and Amara Okafor in
one scenario), a trade-place-name set (Elias, lighthouse keeper), or a stock name in a
setting that does not fit it.

## Sources

Measured:

- Hamilton and Mimno, "Elias in the Lighthouse, Again? Diagnosing Low Diversity in LLM
  Stories", arXiv 2605.26492, 26 May 2026. 20,000 stories, four small models, five
  prompts. https://arxiv.org/abs/2605.26492
- Brzozowski and Chung, "The Ghost Couple: Correlated LLM Name Priors and Their
  Haunting of the Web and Academic Publishing", arXiv 2606.02184, 1 June 2026. Nine
  Claude, eleven GPT and one Gemini checkpoint, 30 prompts per condition. The
  probing tables are useful; the paper has internal inconsistencies (prompt-set and
  checkpoint counts, some percentages), so quote table values. Its Priya claim is
  unsupported by its own results. https://arxiv.org/html/2606.02184v1
- Paech et al., "Antislop: A Comprehensive Framework for Identifying and Eliminating
  Repetitive Patterns in Language Models", arXiv 2510.15061. The Elara figure
  (85,513x, gemma-3-12b) is its only name statistic. https://arxiv.org/html/2510.15061v1
- Jochen Voss, "AI Names", seehuhn.de, 18 January 2026. Claude Sonnet 4.5, 100 runs per role.
  https://www.seehuhn.de/blog/ai-names/
- benjismith, "ai-randomness" (GitHub). Five Claude models, 37,500 draws, including
  18,503 male-name draws. The Marcus count and both denominators were checked on
  30 October 2026 against the [published analysis at commit 6401e8e](https://github.com/benjismith/ai-randomness/blob/6401e8e41e85ac761b3657512122e1c12e2d03f4/output/random-names-analysis.json).
  https://github.com/benjismith/ai-randomness

Informal or anecdotal:

- Wattenberg, "The 2025 Name of the Year is Elara", Namerology, 15 December 2025.
  https://namerology.com/2025/12/15/2025-name-of-the-year-is-elara-the-favorite-name-of-ai/
- Read, "Who is Elara Voss?", Read Max, 7 August 2025; coined "promptonym".
  https://maxread.substack.com/p/who-is-elara-voss
- Thomas, "The Elara problem", 5 June 2026. Dozens of models, no counts.
  https://microblog.christhomas.co.uk/blog/the-elara-bias
- Laforge, "The Sci-Fi naming problem", 22 July 2025. Counts come from an LLM tool
  and are unchecked. https://glaforge.dev/posts/2025/07/22/the-sci-fi-naming-problem-are-llms-less-creative-than-we-think/
- Wagner, "The Problem with Dr. Sarah Chen", The Augmented Educator, 5 October 2025.
  Anecdotal throughout. https://www.theaugmentededucator.com/p/the-problem-with-dr-sarah-chen
- AI Central, "First, we kill all the em-dashes", 15 December 2025 (reader comment on
  Sarah Martinez and Teresa Chen). https://substack.aicentral.blog/p/first-we-kill-all-the-em-dashes
- Goodreads, "Eldoria in AI-generated fiction" (reader-made list).
  https://www.goodreads.com/list/show/225618._Eldoria_in_AI_generated_fiction
- Cole, "Red Flag #10: The Mysterious Sarah Chen" (Threads; search result only, not
  fetched). https://www.threads.com/@nicolascole77/post/DVtE9vRlA4X/
- TomLikesRobots, "Everyone's Name Is Elara: Creating a Blocklist for AI Character-Name
  Slop" (X; not retrieved, HTTP 402). https://x.com/TomLikesRobots/article/2074504762448339243
