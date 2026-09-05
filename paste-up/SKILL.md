---
name: paste-up
description: "Build a Paper mockup from a written specification, or audit and repair an existing Paper file: tokens, fonts, artboard layout, crops, labels. Use only for work in app.paper.design. Not for coded UI implementation (`chiaroscuro`), browser QA (`fieldtest`), or design critique with no Paper file involved."
---

# Paste-up

Paper is where the design happens before any code, and the specification everything answers to afterwards. This skill covers both jobs: draw a file from a written spec, or open a file that already exists and put it right.

Pixel parity with Paper is never the goal downstream. What Paper governs is the information architecture, the step and state model, the hierarchy, the copy intent, the density and the operational behaviour.

## Invoking it

A Paper URL is `https://app.paper.design/file/<fileId>/<page>/<nodeId>` - for example `01M1AMPBSYGK8DPDW1G5824M7K/1-0/FIE-0`. The ULID is the `fileId`; pass it on every file-scoped call that accepts it, rather than relying on whichever file was most recently opened. `1-0` is the page. A trailing node id means the request is scoped to that one artboard; without it, the whole page is in scope.

- **URL plus a repair ask** ("go through this and make sure shared tokens are used") runs the repair lane. An audit-only request uses its inventory and checklist without edits, deletion or comment resolution.
- **No URL** runs the build lane, and the first thing to settle is which file and page to draw in.

Never read node ids back to the person who asked. Name artboards by what they show.

## Before the file opens, either lane

Use the Paper MCP connection supplied by the host. If its guide or file tools are unavailable, report the missing connection and ask the user to connect the target file through the host’s supported Paper route (Paper Desktop for the local MCP server). Continue any brief preparation that does not need the connection; do not claim a file was inspected or edited.

1. `get_guide({ topic: "paper-mcp-instructions" })`. Once per session, and again if the thread has been long enough to lose it.
2. Read the available specification, linked tracker context and project docs. If none exists, derive a short list of views and states from the user’s request, state the assumptions and proceed; ask only where missing scope changes what should be built. Name the views in the brief before drawing.
3. `get_basic_info`, `get_font_family_info`, `get_tokens`. Use the existing design and written direction to establish type and colour.
4. Record the in-scope page/artboards and permitted edits. Carry that boundary through every read, repair and completion check. Inspect out-of-scope consumers before changing shared token definitions; reassign in-scope nodes or create a distinct token if a global change is not authorized.

## Build lane

**Establish direction before drawing.** Define each view's purpose, audience, content and states from the supplied specification. The current agent can direct and draw sequentially. Delegate only when available and useful; use installed specialist skills or models as optional aids, not prerequisites. A delegated drawing brief must preserve the agreed direction.

**Set the file up once, before any view exists.**

- Create the tokens: colour names and the type scale. Parallel agents that skip this invent four names for one hex value and the file has to be reconciled by hand afterwards.
- Name artboards for the views they show. Follow the file's existing organization or supplied direction; a horizontal row is one useful default for a new linear flow, not a requirement for every file.
- Confirm the font family with `get_font_family_info` and use it. Fonts set from memory have needed a dedicated repair agent across a thousand nodes.

**Then draw.** One visual group per `write_html`, screenshot after each one, `finish_working_on_nodes` when a set is done. Screenshotting only at the end means finding six problems at once, all of them compounded.

## Repair lane

Order matters here, because a token fix touches every node and a layout fix moves them.

1. **Inventory.** `get_tree_summary`, then list the in-scope artboards: name, size, position and purpose. Inspect neighbours only as needed to understand context.
2. **Tokens.** Inspect hard-coded values within scope and their intended roles. Equal values can have different semantic roles; merge only confirmed duplication. Before `create_tokens` / `set_tokens`, check all consumers affected by a definition change. Use `update_styles` only on in-scope nodes.
3. **Fonts.** Confirm installed families and correct departures from the agreed type roles. Preserve deliberate display/body/mono distinctions and existing typography outside scope.
4. **Layout.** Correct unintended overlap or spacing within scope while preserving the file's organization. Do not rearrange unrelated artboards.
5. **Names.** `rename_nodes` so each artboard says what it shows.
6. **Dead work.** Old experiments and superseded versions. Ask before deleting anything you did not make.
7. **The checklist below**, artboard by artboard.
8. **Comments.** Read in-scope comment threads. Address requests covered by the user's task; report unrelated requests separately. Resolve only comments whose requested work has actually been completed within the authorized scope.

Report as a table: artboard, what changed, what was left alone and why.

## The checklist

Every line here is a correction that has had to be given more than once.

- **Real images.** Use supplied assets or appropriate project/public sources within the task’s scope. When product photography is unavailable, state the gap; label any authorized illustrative image rather than presenting it as the real product.
- **Purposeful imagery.** Avoid accidental repetition; keep repetition when it identifies the same item or supports comparison.
- **Appropriate crops.** Choose aspect ratios from the content and supplied direction. Preserve the subject, crop inside the frame, and never distort one axis.
- **Imagery that flatters the product.** A realistic photograph can still be the wrong photograph. Match the aspiration of the audience.
- **Consistent navigation.** Reuse shared chrome where the product requires it; focused or standalone views may intentionally omit it.
- **Appropriate interaction.** Follow the product's purpose. An editor, document, marketing page and dashboard need different structures.
- **Text is not interface.** Paragraphs standing in for controls is a failed view, however well written.
- **Reviewable alternatives.** Clearly label alternatives when exploration is requested; keep the selected direction identifiable.
- **Density a stranger can parse.** The test is someone seeing it for the first time in a meeting, with the presenter talking over it. Depth is fine, an unreadable wall is not.
- **Labels and copy.** Use words the audience understands, state outcomes plainly, and remove filler. Use `signage` or `deslop` for deeper review when installed and useful.
- **Data the product can actually serve.** Verify displayed facts from supplied evidence or an authorized project data source. Use scoped reads, avoid exposing unrelated records, and do not invent production facts. Label illustrative values clearly and record the source gap when real data is unavailable.

## Before calling it done

- Review the in-scope artboards for clarity and task completion. An independent review is optional when a material uncertainty warrants it.
- Recheck in-scope comments and report their actual resolution.
- Screenshot the changed artboards and inspect them in context. A view that reads well alone can be wrong beside its neighbours.
- `export_combined_pdf` when it has to leave Paper, since a file link cannot always be shared.

## Gotchas, all of them measured

- **`get_jsx` blows the token limit constantly** - the largest share of recorded Paper errors. The result is written to a file and the error names the path; read it from there, or scope the read with `get_node_info` and `get_computed_styles` on a subtree.
- **`write_html` can exceed the limit too** when the subtree it returns is large. One visual group per call keeps it under.
- **Paper disconnects mid-session.** "Your Paper file is currently disconnected from the server" means wait and retry that one call. Never rebuild work already written.
- **`finish_working_on_nodes` is required and routinely skipped.** Call it when a set of nodes is done.
- **`get_computed_styles` takes an array** of node ids, even for one node.
