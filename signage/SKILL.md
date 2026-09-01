---
name: signage
description: "Replace invented interface vocabulary with the words the audience already uses. Labels, headings, buttons, status lines, empty states and template-generated strings, checked against how a person doing that job would say them out loud. Use after building or designing any UI. For body prose use `deslop`; for names use `nomen`."
---

# Signage

The words on an interface are signage. A label's whole job is to let someone act without stopping to decode it. Agent-written UI fails at this in a specific, repeating way: the model reaches for the vocabulary of its own internal model of the system, or it writes a sentence where a two-word label belongs, and the result is an interface that is beautiful and unreadable.

This is a comprehension pass: the user has to know what the button does.

**The test that decides every word: would you say it out loud to someone who does the audience's job, and be understood?** If you would have to explain it, it is wrong on the screen. Word choice gets the test; the tells below catch the failures the test cannot see.

## The tells

Cite by number in findings, so a reviewer sees the pattern rather than the instance. Copy that reads as plain English and is still unclear has no tell number - it is caught by the test alone, and reported against the test.

**Vocabulary the audience does not have**

1. **Internal nouns on screen.** A domain term, table name, service name, or architecture word promoted to a label. The user never saw the schema. `Shelf` for catalogue, `Answering` for search, `Record` for the data.
2. **Invented words for ordinary things.** A coined term where a standard one exists. If the industry already has a word, use the industry's word, even when it is duller.
3. **A verb nobody performs.** `Ingest`, `Surface`, `Reconcile`, `Materialise` on a button. People add, save, send, check, open, compare.
4. **Abstraction as a label.** `Intelligence`, `Signal`, `Context`, `Instrument`, `Governance` where a concrete noun would name the actual thing on screen. Keep an abstraction when it is the term of art the audience already uses in their trade - provenance in a materials library, signal in audio tools.
5. **A label naming the evidence rather than the fact.** `Vector-matched colour` instead of `Closest colour`. The user wants the property; how it was derived is not the label. A market that requires the derivation disclosed is the exception, and it belongs in the value, not the label.

**Prose where a label belongs**

6. **A sentence doing a label's job.** `This page names three products` is a heading trying to be an essay. `3 products`.
7. **Shouted declarations.** `THE PAGE AND THE RECORD DISAGREE`, `PROOF YOU CAN ORDER`. Caps turn a status into a headline about the system's own reasoning.
8. **Explanatory subtext under every element.** A caption telling the user what the thing above it means is an admission the label above it has failed. Fix the label; delete the caption.
9. **Lighter grey text standing in for real UI.** A dimmed sentence is not a state, a control, or an empty state. It is a note to self left on the screen.
10. **Scaffolding copy.** `Three ways forward:`, `Here's what we found:`, `Overview`, `Getting started` as a heading over content that is neither.

**Sentences no human would say**

11. **Template-assembled descriptions.** `A Hospitality Lobby in Mid-Century Modern, feeling calm, in warm muted green, evoking Nordic, in the Mid-Century.` Every slot filled, no sentence produced, and the same fact stated twice. Read generated strings as strings, and judge the words against the audience rather than against the template's own logic.
12. **Portentous compression.** `Candor reads the warehouse through one governed instrument, before the panel sits.` Grammatical, meaningless, and unsayable to another person.
13. **Being clever in front of someone trying to work.** Wordplay, metaphor, and a knowing voice in a label. The user is mid-task.
14. **Rule-of-three cadence and the closing flourish** in body copy, tooltips, and empty states. Three options the user can actually take are a list, which is fine; the tell is three parallel clauses with nothing behind them.

**Typographic tells that read as machine-made**

15. **Small caps and letter-spaced micro-headings.** They add emphasis the content does not support.
16. **Title Case Drift** across labels that should be sentence case, and sentence case where the product's convention is title case. Pick one and hold it.
17. **Emoji, status theatre, and box-drawing** in any user-facing surface.

## Substitutions

The model's word on the left, the audience's word on the right. Direction for the pass rather than a dictionary to apply blind.

| Written | Say |
| --- | --- |
| Shelf | Catalogue |
| Answering | Search |
| The record | The data, or name the actual source |
| Resolve (outside conflict and review UIs) / Reconcile | Fix, match, choose |
| Surface / Expose | Show |
| Ingest | Import, add |
| Leverage / Utilise | Use |
| Unlock / Enable | Open, turn on |
| Seamless / Frictionless | Name what is actually easy, or delete |
| Journey | Name the task |
| Evoking | In the style of, or delete |
| Signal | The named fact itself |
| Provenance | Where it came from, unless the trade uses the word |
| Instrument / Governed | Delete; say what it does |
| Sampleability | Whether you can get a sample |
| Artefact | The thing's actual name |

## Steps

Copy these steps into your todolist verbatim before you start. A step you skip stays in the list with a one-line `skip: <reason>`.

1. **Fix the scope and the audience.** Name the screens or the diff, and name who reads them in one line, in their own job title. `Working interior designers`, not `end users`. A pass without a named audience produces generic copy, because the test in this skill has nothing to measure against.
2. **Find the ubiquitous language.** Read any glossary the project keeps before judging a word. Where it keeps none, judge by the test alone and report the gap as a finding for `domain-modeling`, rather than blocking the pass or inventing a glossary.
3. **Extract every string.** Labels, headings, buttons, status lines, tooltips, empty states, error text, and anything generated from a template. Read them as a flat list, out of layout. Copy that survives only because the design carries it is the copy this pass exists to catch.
4. **Apply the test mechanically, string by string.** Reject any label over eight words, any label carrying a subordinate clause, any label using a verb phrase where a noun belongs, and any word the step 1 audience would not use in a work conversation. Each rejection gets a tell number and a `file:line` or a node reference.
5. **Rewrite to the shortest sayable form.** Shorter is only better when it stays sayable, because a shortened piece of jargon is still jargon. Keep every fact the user needs, drop facts the same string already states, and where a string comes from a template, fix the template rather than the rendered instance.
6. **Check the rewrites against the glossary and its avoid-list**, so the fix does not reintroduce a term the domain model rejected, or invent a second word for a thing that already has one.
7. **Render it and read it in place.** A label that works in a list can still be wrong at its real size next to its real neighbours.
8. **Report.** Counts by tell number, the before-and-after table, and any term you could not settle without a decision from the owner.

## Where this fits

- Body prose, docs, and PR descriptions: `deslop`.
- Product, feature and package names: `nomen`.
- A layout or mockup that confuses while every word in it is plain: `chiaroscuro`.
- Deciding what a concept *is* before naming it: `domain-modeling`.
- Machine-written tells in code rather than on screen: `unslop`.
