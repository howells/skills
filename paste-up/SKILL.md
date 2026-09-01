---
name: paste-up
description: "Build or audit mockups in Paper (app.paper.design): tokens, fonts, artboard layout, crops, labels."
---

# Paste-up

Paper is where the design happens before any code, and the specification everything answers to afterwards. This skill covers both jobs: draw a file from a written spec, or open a file that already exists and put it right.

Pixel parity with Paper is never the goal downstream. What Paper governs is the information architecture, the step and state model, the hierarchy, the copy intent, the density and the operational behaviour.

## Invoking it

A Paper URL is `https://app.paper.design/file/<fileId>/<page>/<nodeId>` - for example `01M1AMPBSYGK8DPDW1G5824M7K/1-0/FIE-0`. The ULID is the `fileId` every MCP call needs. `1-0` is the page. A trailing node id means the request is scoped to that one artboard; without it, the whole page is in scope.

- **URL plus an ask** ("go through this and make sure shared tokens are used") runs the repair lane.
- **No URL** runs the build lane, and the first thing to settle is which file and page to draw in.

Never read node ids back to the person who asked. Name artboards by what they show.

## Before the file opens, either lane

1. `get_guide({ topic: "paper-mcp-instructions" })`. Once per session, and again if the thread has been long enough to lose it.
2. Read the specification. Linear, the strategy repo, the project's own context and domain docs. Every view is named in writing before a single one is drawn. Building from your own idea of the product, when a spec exists, is the failure this step prevents.
3. `get_basic_info`, `get_font_family_info`, `get_tokens`. Three calls, and they decide the type and colour of everything that follows.

## Build lane

**Direct and draw are different jobs.** A Fable subagent produces the view inventory and the creative direction for each view: what it is for, who is looking at it, what is on it, what its states are. Opus subagents draw. The agent drawing a view never decides what the view is.

**Set the file up once, before any view exists.**

- Create the tokens: colour names and the type scale. Parallel agents that skip this invent four names for one hex value and the file has to be reconciled by hand afterwards.
- One artboard per view, laid out on a single horizontal row, no overlaps, named for the view. Horizontal keeps you unencumbered by height.
- Confirm the font family with `get_font_family_info` and use it. Fonts set from memory have needed a dedicated repair agent across a thousand nodes.

**Then draw.** One visual group per `write_html`, screenshot after each one, `finish_working_on_nodes` when a set is done. Screenshotting only at the end means finding six problems at once, all of them compounded.

## Repair lane

Order matters here, because a token fix touches every node and a layout fix moves them.

1. **Inventory.** `get_tree_summary`, then list every artboard: name, size, position, whether it is current or abandoned.
2. **Tokens.** `get_tokens`, then find every hard-coded value in the file. Collapse duplicates onto one name, `create_tokens` / `set_tokens`, `update_styles` across the nodes. Report which values were the same colour under different names.
3. **Fonts.** `get_font_family_info`, then every text node onto the file's family and scale.
4. **Layout.** Overlapping artboards, inconsistent gaps, a canvas that reads as a pile. Single row, even spacing.
5. **Names.** `rename_nodes` so each artboard says what it shows.
6. **Dead work.** Old experiments and superseded versions. Ask before deleting anything you did not make.
7. **The checklist below**, artboard by artboard.
8. **Comments.** `list_comment_threads`, address each one, `set_comment_thread_status`. Comments are the review channel and they are routinely never read.

Report as a table: artboard, what changed, what was left alone and why.

## The checklist

Every line here is a correction that has had to be given more than once.

- **Real images.** Actual product and material photography from the real source. Not placeholders, not stand-ins, not something approximate.
- **Every image distinct.** Repeating one photo across a view makes the design unreadable.
- **Square or landscape.** Samples and uploads are square; scenes are landscape. Never 16:9 with an awkward crop, and never a single axis scaled - set the frame and crop inside it.
- **Imagery that flatters the product.** A realistic photograph can still be the wrong photograph. Match the aspiration of the audience.
- **Shared chrome on every view.** The same sidebar, header and navigation, so the set reads as one product.
- **An app, not a document.** Browser-based does not mean a scrolling page. It should feel like a tool.
- **Text is not interface.** Paragraphs standing in for controls is a failed view, however well written.
- **One design per page.** A page with three half-ideas on it cannot be reviewed.
- **Density a stranger can parse.** The test is someone seeing it for the first time in a meeting, with the presenter talking over it. Depth is fine, an unreadable wall is not.
- **Labels and copy.** `signage` over every label, heading, button, status line and empty state. `deslop` over every sentence.
- **Data the product can actually serve.** Query the real API or database for the numbers on screen. A view designed around data that does not exist is a promise someone has to break.

## Before calling it done

- `glm-review` each artboard for clarity and whether the interface works.
- Sweep the comments and resolve them.
- Screenshot every artboard and look at it. A view that reads well alone can be wrong beside its neighbours.
- `export_combined_pdf` when it has to leave Paper, since a file link cannot always be shared.

## Gotchas, all of them measured

- **`get_jsx` blows the token limit constantly** - the largest share of recorded Paper errors. The result is written to a file and the error names the path; read it from there, or scope the read with `get_node_info` and `get_computed_styles` on a subtree.
- **`write_html` can exceed the limit too** when the subtree it returns is large. One visual group per call keeps it under.
- **Paper disconnects mid-session.** "Your Paper file is currently disconnected from the server" means wait and retry that one call. Never rebuild work already written.
- **`finish_working_on_nodes` is required and routinely skipped.** Call it when a set of nodes is done.
- **`get_computed_styles` takes an array** of node ids, even for one node.
