---
name: signage
description: "Rewrite interface strings into the words the audience already uses: labels, buttons, headings, errors, empty states, generated text, film captions. Use when UI copy reads as jargon or machine-made. Not for prose (`deslop`) or product names (`nomen`)."
---

# Signage

The words on an interface are signage: a label lets someone act without stopping to decode it. Agent-written UI fails in a repeating way. It promotes its own internal model of the system to the screen, or writes a sentence where a two-word label belongs, and the interface ends up beautiful and unreadable.

**The test for every word: would you say it out loud to someone who does the audience's job, and be understood?** If you would have to explain it, it is wrong on the screen. If you would sound like a clerk reading out a record, it is also wrong: say what is true, once, the way you would across a table. The tells catch what the test misses; copy that fails the test with no tell is still wrong.

## The tells

Cite them by number in findings, so a reviewer sees the pattern rather than the instance.

**Vocabulary the audience does not have**

1. **Internal nouns on screen.** A domain term, table, service or architecture word promoted to a label. `Shelf` for catalogue, `Answering` for search, `Record` for the data.
2. **Invented words for ordinary things.** If the industry has a word, use it, even when it is duller.
3. **A verb nobody performs.** `Ingest`, `Surface`, `Reconcile`, `Materialise`. People add, save, send, check, open, compare.
4. **Abstraction as a label.** `Intelligence`, `Signal`, `Context`, `Governance` where a concrete noun names the thing. Keep a term of art the audience already uses: provenance in a materials library, signal in audio tools.
5. **Naming the evidence instead of the fact.** `Vector-matched colour` for `Closest colour`. Where a market requires the derivation disclosed, put it in the value, not the label.

**Prose where a label belongs**

6. **A sentence doing a label's job.** `This page names three products` → `3 products`.
7. **Shouted declarations.** `THE PAGE AND THE RECORD DISAGREE`. Caps turn a status into a headline about the system's reasoning.
8. **Explanatory subtext under every element.** A caption explaining the thing above it admits the label failed. Fix the label and cut the caption; keep distinct help, consent, constraints and error recovery.
9. **Dimmed sentences standing in for UI.** A grey note is not a state, a control or an empty state.
10. **Scaffolding copy.** `Three ways forward:`, `Here's what we found:`, `Overview`, `Getting started` over content that is neither.

**Sentences no human would say**

11. **Template-assembled strings.** `A Hospitality Lobby in Mid-Century Modern, feeling calm, in warm muted green, evoking Nordic, in the Mid-Century.` Every slot filled, no sentence, a fact said twice. Judge generated strings as strings and fix the template.
12. **Portentous compression.** `The system reads the warehouse through one governed instrument, before the panel sits.` Grammatical and unsayable.
13. **Metaphor where a direct statement belongs.** `A dial worth turning` for `Sample size`, `Earns its keep` for `Still in use`. The figure displays the writer, makes the user decode it mid-task, and drags in connotations nobody chose. Wordplay and a knowing voice fail the same way. When a literal phrase exists, use it.
14. **Rule-of-three cadence and the closing flourish** in tooltips, body copy and empty states. Three real options are a list; three parallel clauses with nothing behind them are the tell.

**Typographic tells**

15. **Small caps and letter-spaced micro-headings.** An existing house habit is not an exception; only an explicit instruction from the user is.
16. **Case drift.** Sentence case is the default; where the product uses title case for an element type, hold it across every instance. `Save Changes` beside `Discard changes` reads as sloppy.
17. **Emoji, status theatre and box-drawing** on any user-facing surface.

**Labels that disagree**

18. **Several labels for one action or object.** `Get in touch`, `Let's talk` and `Contact us` on one page; `Archive` in the menu and `Move to storage` in the toast. One thing gets one word everywhere.

**Narrating the machinery, and hedging**

19. **How the system knows instead of what is true.** A value is `stated by`, a tool `returned`, a size `was derived from the drawing`. `No size is stated. It was derived from the drawing.` → `Estimated 120 × 60 cm`. `Stated by 412 of 9,870 records` → `412 have one`, when the denominator does not change the decision. Keep a qualifier that changes the value's meaning, certainty or coverage. Show the mechanism only when it is the point, in one plain clause.
20. **Clerical and courtroom register.** `States`, `attests`, `cites`, `is recorded as`, `per the source`, `Source ·`. Use `has`, `says`, `from`, `is`.
21. **Hedges and accounting qualifiers.** `Four of the six returned`, `where available`, `in most cases`, `nothing is guessed silently`. A qualifier stays only when it changes what the reader does next.
22. **A line under a heading that repeats it.** Cut it or make it say the next thing.
23. **A placeholder that repeats its label.** Show a format or a real example (`name@example.com`), or nothing. Helper text says why something is asked, not what the field is.

## Strings with a job

These come up in every product; write them this way unless the product has its own established pattern.

- **Buttons start with a verb and name the object:** `Save draft`, `Delete project`. Never `OK`, `Yes`, `No` or `Let's go!`. An icon button's accessible name follows the same rule: `Delete project`, not `Trash`.
- **Links name their destination.** `Read the billing docs`, never `Click here`. Two `Learn more` links on a page need suffixes: `Learn more about exports`.
- **Errors say what failed and how to fix it, beside the field:** `Enter a date as DD/MM/YYYY`, not `Invalid date`; `Unable to save. Check your connection and try again.`, not `Oops! Something went wrong.` No blame, no exclamation marks. Show a known requirement as helper text before the error.
- **Confirmations name the action and the object:** title `Delete 'Q3 report'?`, body says what is lost (`This permanently deletes the report and its 4 comments.`), buttons `Delete report` and `Cancel`. Never `Are you sure?`. A reversible, frequent action gets an undo instead: `Project archived. Undo`.
- **Status copy pairs:** `Saving changes…` resolves to `Changes saved`. No `successfully`. A failure says what did not happen, then the next step; a partial result gives both counts (`9 of 12 files uploaded. Retry 3`).
- **Empty states say what the place is and offer one next action.** A filtered empty state names the query and the exit: `No results for 'quarterly'. Clear filters`.
- **Toggles describe the on state:** `Send read receipts`, not `Don't send read receipts`.
- **Tone follows the stakes:** light in onboarding and empty states, neutral in settings, plain and unplayful in errors and destructive actions. Cut `Please` from routine instructions. Address the reader as `you`; `we` in an error reads as deflection.
- **Build sentences whole.** `"You have " + n + " messages"` and `n === 1 ? "" : "s"` break in other languages. Use one message with placeholders and the locale's plural rules (ICU or `Intl.PluralRules`), and format numbers, dates and lists with `Intl`.

## Substitutions

Direction for the pass, not a dictionary to apply blind.

| Written | Say |
| --- | --- |
| Shelf / Answering / The record | Catalogue / Search / the data, or name the source |
| Resolve (outside conflict and review UIs) / Reconcile | Fix, match, choose |
| Surface / Expose | Show |
| Ingest | Import, add |
| Leverage / Utilise | Use |
| Unlock / Enable | Open, turn on |
| Seamless / Frictionless | Name what is easy, or delete |
| Journey | Name the task |
| Evoking | In the style of, or delete |
| Signal / Provenance | The named fact / where it came from, unless the trade uses the word |
| Instrument / Governed | Delete; say what it does |
| Sampleability | Whether you can get a sample |
| Artefact | The thing's actual name |
| A dial worth turning / Earns its keep / Where the rubber meets the road | Name the setting / the plain fact / the step |
| Stated by / States / Source · X | Has, says, from X, or just the value |
| Returned / The reply / Read as | Delete; give what came back |
| Measured, derived or inferred from | The value; keep `Estimated` where it changes certainty |
| N of M returned / First page of N | Delete, unless the count changes what the reader does |

## Steps

Scale to the request: a few labels need direct edits and a line of explanation.

1. **Name the audience by job title** (`working interior designers`, not `end users`). Without one the test has nothing to measure against.
2. **Learn the product's vocabulary.** Read any glossary first. List the noun used for each object and the verb for each action, and the case per element type, from the existing strings and locale files (`t(`, `locales/**/*.json`, `*.po`). New copy uses those words. With no glossary, judge by the test and name the gap for `domain-modeling`.
3. **Read every in-scope string as a flat list**, out of layout: labels, headings, buttons, status lines, tooltips, empty states, errors and template output. Copy that survives only because the design carries it is what this pass exists to catch.
4. **Rewrite to the shortest sayable, most literal form.** A shortened piece of jargon is still jargon. Keep every fact the user needs; long strings stay where consent, error recovery or an unambiguous action need the length. Fix templates rather than rendered instances. Change display text only: keep translation keys, IDs, stored values, placeholders and format syntax, and update tests that assert the old wording.
5. **Read it in place** when the app runs: a label that works in a list can be wrong beside its real neighbours. If plain labels still leave objects or actions unclear, the problem is the model or layout; report it to its owner rather than renaming again.
6. **Report** the changes, with a before-and-after table and tell numbers for a larger pass, plus unresolved terms and anything not seen rendered.

## Where this fits

- Body prose, docs and PR descriptions: `deslop`.
- Product, feature and package names: `nomen`.
- A layout that confuses while every word is plain: `chiaroscuro`.
- Deciding what a concept is before naming it: `domain-modeling`.
- Text size, weight and case: `typecase`.
