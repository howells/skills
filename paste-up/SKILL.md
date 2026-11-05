---
name: paste-up
description: "Build a mockup in Paper (app.paper.design) from a spec, or audit and repair a Paper file: tokens, fonts, artboards, crops, labels. Not for coded UI (`chiaroscuro`) or browser QA (`fieldtest`)."
---

# Paste-up

Paper is where the design happens before code, and the specification the code answers to afterwards. Downstream, pixel parity is never the goal. Paper governs the information architecture, the step and state model, the hierarchy, the copy intent, the density and the behaviour.

## Hard rules

The same rules `chiaroscuro` applies to code, so a mockup never needs correcting for them later. The product's existing styling is no exception: fix it inside scope, report it outside. Only an explicit instruction from the user overrides one.

1. **No small caps, tracked uppercase or decorative mono.** No eyebrows, kickers, section labels, chips or table headings in capitals. Mono only for literal code, identifiers and values whose characters need inspecting. Acronyms keep their capitals.
2. **No prose where interface belongs.** A paragraph explaining a screen means the screen has failed; replace it with a label, a control, a value or nothing. Headings name things; they do not headline them. Keep only consent, constraints and error recovery.
3. **Four to six type styles, in chosen faces.** Use the product's named roles; a new size or weight needs a job no role does. Never use Instrument Serif, Playfair Display, Poppins, Montserrat, Roboto or Arial for a new face. Before choosing one, read [references/font-guidance.md](references/font-guidance.md) and choose from its recommendations. Read each reference file with its own command.
4. **Reuse before you build.** Use the existing component, shell, header or control, in this product or any package the user points to. A second version of an existing control is a defect.
5. **One of each.** One corner-radius scale with concentric nesting, one icon family at one stroke weight, one control height per density.
6. **Touch targets at least 44 by 44 CSS pixels.**
7. **Look at the whole screen, desktop and phone.** Walk the boards in order as the user would. Read computed styles for caps, letter spacing and mono; a screenshot hides them.

## The file

A Paper URL is `https://app.paper.design/file/<fileId>/<page>/<nodeId>`, e.g. `01M1AMPBSYGK8DPDW1G5824M7K/1-0/FIE-0`. Pass the `fileId` on every file-scoped call rather than relying on whichever file was last opened. A trailing node id scopes the request to that artboard; without one the page is in scope. An untidy rest-of-file does not widen a one-board request.

Never read node ids back to the user. Name artboards by what they show.

If the Paper tools are missing, say so and ask the user to connect the file (Paper Desktop runs the local MCP server). Never claim a file was inspected or edited without them.

Start every session with `get_guide({ topic: "paper-mcp-instructions" })` (again if the thread is long enough to have lost it), then `get_basic_info`, `get_font_family_info`, `get_tokens`.

A token definition is shared: check its consumers outside scope before changing it, and create a distinct token rather than make an unauthorised global change.

## Build

Work from the spec. With none, derive the views and states from the request, state the assumptions and draw.

- **Tokens before any view**: colour names and the type scale. Parallel agents without them invent four names for one hex, and the file has to be reconciled by hand.
- **Fonts from `get_font_family_info`**, never from memory. Fonts set from memory once needed a repair agent across a thousand nodes.
- **One visual group per `write_html`, screenshot after each**, `finish_working_on_nodes` when a set is done. Screenshotting only at the end finds six compounded problems at once.
- **After the first complete view**, zoom out, check its hierarchy, and draw the next state beside it so each action stays connected to its consequence.
- **Borrowing another interface's look**: name the features borrowed and keep the target product's tasks, objects and states. Copying its screens can quietly replace the app being designed.

A brief handed to a helper carries the agreed direction and the hard rules.

## Repair

Order matters: a token fix touches every node and a layout fix moves them. An audit-only request reports against these steps without editing, deleting or resolving anything.

1. **Inventory.** `get_tree_summary`; list the in-scope artboards with name, size and purpose.
2. **Tokens.** Replace hard-coded values with tokens. Equal values can have different roles; merge only real duplication.
3. **Fonts.** Correct departures from the type roles and the hard rules. Report typography outside scope.
4. **Layout.** Fix unintended overlap and spacing. A flow shows its start, reading order, branches and returns. Leave unrelated artboards where they are.
5. **Names.** `rename_nodes` so each artboard says what it shows.
6. **Dead work.** Delete superseded boards only where the user has explicitly said so, and only those it covers. Ask before deleting anything else you did not make. Requested explorations stay, labelled apart from the current design.
7. **The checklist below**, artboard by artboard.
8. **Comments.** Do the in-scope requests; report the rest. Resolve a thread only when its work is done.

Report a table: artboard, what changed, what was left alone and why.

Before "one page with the current version of every screen" or any whole-app consolidation, read [references/consolidation.md](references/consolidation.md).

## Checklist

Each line is a correction given more than once.

- **Real images**, supplied or properly sourced. Without product photography, say so; label any illustrative image.
- **Crops chosen from the content**, subject kept, never stretched on one axis. No accidental repetition.
- **Imagery that flatters the product.** A realistic photo can still be the wrong photo; match the audience's aspiration.
- **Text is not interface.** Paragraphs standing in for controls fail the view, however well written.
- **Density a stranger can parse**: someone seeing it for the first time in a meeting, with the presenter talking over it.
- **Plain labels**: the audience's words, outcomes stated, no filler (`signage` goes deeper).
- **Data the product can actually serve.** No invented production facts; label illustrative values.
- **A presentable sequence**: someone opening the file finds the start, follows each action to its next state, and can tell the current design from alternatives and notes.

`export_combined_pdf` when the work has to leave Paper; a file link cannot always be shared.

## Gotchas

- **`get_jsx` blows the token limit constantly**, the largest share of recorded Paper errors. The error names a file holding the result; read it there, or scope with `get_node_info` and `get_computed_styles` on a subtree.
- **`write_html` can exceed it too** when the returned subtree is large. One visual group per call keeps it under.
- **"Your Paper file is currently disconnected from the server"** means wait and retry that one call. Never rebuild work already written.
- **`finish_working_on_nodes` is routinely skipped.** Call it when each set of nodes is done.
- **`get_computed_styles` takes an array** of node ids, even for one node.
