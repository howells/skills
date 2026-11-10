# README template

Placeholders are `{like this}` (angle brackets vanish on GitHub); each is an instruction or a menu of examples, so replace every one with real prose. Keep the section order. The "Structure" block and the "Coverage" table are the plan; keep them exact mirrors of the files on disk.

---

# {product} product description

A written description of the user experience of {product}: what the user sees, what they can do, and exactly what happens when they do it.

## Purpose

{product} is, from the user's point of view, a large state chart, moved through with {the product's inputs: pointer events, drags, modifier keys, shortcuts / taps and swipes / commands and flags / form submissions}. Most of that behavior is implicit, spread across {where it lives: state machines, reducers, handlers, tests, the UI}. No single place says, in plain language, "when the user does X, this happens, and this happens if they do Y halfway through."

This project is that place. It describes the full experience a user has on {the surface being described: a specific route of the app / the default installation / the production site with a fresh account}, in {the default configuration, with nothing customized}.

The documents are for anyone who needs to understand or change the product, or judge whether a behavior is intentional. They describe the experience, not the implementation.

### What this is not

- Not API documentation. {Say where that lives.}
- Not organized by package. {The product's packages or modules} are not described separately; each behavior is described once, where the user meets it.
- Not a technical design document. A technical detail critical to the experience appears only in a block quote labeled `Technical note:`.

## Conventions

- Describe the experience, not the code. "{an experiential sentence}" rather than "{the same thing said about the code}".
- Use a `Technical note:` only when the mechanism changes what the user would expect.
- Use sentence case for headings.
- Name the vocabulary consistently. The [glossary](glossary.md) is the source of truth for terms like {five or six of the product's load-bearing terms}.
- Every document ends with the inspected source commit, a separate runtime-verification status, and open questions.
- When a behavior is surprising, say so, and why if known. Do not smooth it over.

## The work to be done

Each document describes one feature, large ({example}) or small ({example}), in full, including its edge cases and interactions with other features.

### Document template

Every feature document follows the same skeleton, so documents are comparable and nothing is skipped.

1. **Summary.** One paragraph describing the feature abstractly. For example: "{one-sentence summary of the pilot feature}."
2. **The simple case.** The common path in prose.
3. **The interaction, event by event.** The five phases of {the product's unit of interaction: a gesture / a page or form lifecycle / an invocation / a turn}: {name them in the product's words: starting; ending at once; becoming extended; while extended; finishing}. What starts it and what is captured, what happens if it ends at once, what is decided the moment it becomes extended, what updates live, and what is committed at the end. Include a small state diagram (Mermaid `stateDiagram-v2`) of the states the user passes through.
4. **Modifiers.** A table of {Shift, Alt/Option, Ctrl/Cmd, and Space / the product's variant axis: roles, record states, flags, modes}, and what each one does when set at the start and when changed *during* the interaction.
5. **Cancel and interrupt.** The same checklist in every document:
   - {The user's explicit abort: Escape, Stop, Ctrl+C, a Cancel button}
   - {The user doing something else mid-way: switching tools, modes, tabs, or conversations; navigating away; sending another message}
   - {The events the product treats as a clean "complete": a menu opening, undo or redo, a submit from elsewhere}
   - {The environment failing: window loses focus, network lost, request fails or times out, session expires}
   - {The page or process going away: reload, tab closed, terminal closed, app backgrounded}
   - {Something else changing the target: deleted, locked, edited by another user or tab, changed on disk}
   - {The input channel changing: a second input device, autofill, a pipe closing, touch cancel}
   {Rewrite this list for the product from the five interrupt families in the skill's product-kinds.md. It must be identical, and in the same order, in every document.}
6. **Interactions with other systems.** {The product's cross-cutting concerns, in a fixed order: permissions, history or undo, containers or parents, locked or readonly state, offline, collaboration or multi-device, notifications, configuration and preferences.}
7. **Edge cases.** Anything a user could notice that is not covered above.
8. **Open questions and verification.** The inspected {source repo} commit, runtime-verification status, and any behavior that could not be confirmed.

Item 5 matters most. Asking the same interrupt questions of every feature is how gaps and inconsistencies are found.

Method and order of work: [goal.md](goal.md). Verification protocol: [verification/README.md](verification/README.md). Progress is tracked in the [coverage table](#coverage) below.

### Scope decisions

- **{Excluded thing}.** {Why, and whether it gets a document later.}
- **{Concern described inside each document rather than separately}.** {Why: a separate document would drift.}
- **{Concern described once in a cross-cutting document rather than in every feature}.** {Why.}
- **Interaction shape.** The unit of interaction is {a gesture / a form lifecycle / an invocation / a turn} and its phases are {the five names}. The interrupt list and the order of cross-cutting concerns are fixed as written in the document template above.
- **Numbered rules.** These are prose documents, not numbered specifications. Stable heading anchors are enough for cross-references.

## Structure

```
README.md                        this file
goal.md                          the standing instructions for whoever drafts
AGENTS.md, CLAUDE.md             entry points for agents: read README.md, then goal.md
glossary.md                      shared vocabulary
bug-triage.md                    suspected defects collected from every document, with repro steps and decisions needed

verification/
  README.md                      how to run a hand-verification pass and record results
  {cluster}.md                   checklists for {area}/ and {area}/
  ...

foundations/
  {name}.md                      {one-line gloss, wrapping to a second indented line if needed}
  ...

{area}/
  {feature}.md                   {gloss}
  {sub-area}/
    {feature}.md                 {gloss}
  ...

cross-cutting/
  {concern}.md                   {gloss}
  ...
```

## Coverage

Status is one of `not started`, `drafted`, or `verified`.

| Document | Status |
| --- | --- |
| glossary.md | not started |
| bug-triage.md | not started |
| verification/ ({n} checklists) | not started |
| foundations/{name}.md | not started |
| ... | not started |

## Reference

The source of truth is {the source repo} at `{path or URL}`. The relevant locations are:

- `{path}`: {the surface this project describes}
- `{path}`: {where interaction state lives}
- `{path}`: {the domain objects}
- `{path}`: {the UI}
- `{path}`: {behavioral tests}
- `{path}`: {subsystems that shape the experience: hit testing, validation, scheduling, caching, sync, etc.}
