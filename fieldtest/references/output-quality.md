# Returned content and collection coverage

Use when a page returns materials, images, recommendations, search results or generated artefacts, or when the request says to inspect every example. Browser mechanics and content quality are separate claims.

## Define the cases

Enumerate the requested cases with stable IDs before claiming coverage. Use the collection's actual membership, including empty and unavailable cases. For an open-ended search, state the bounded query, filters and snapshot rather than inventing a total universe.

Keep a compact working ledger in tool state or temporary scratch storage, outside the repo. Each row records case ID, route/query, relevant state and viewport, evidence, inspection status and finding or gap. Durable findings belong in the tracker, and the report belongs in chat unless another artefact was requested.

Track what happened precisely:

| Status | What it establishes |
| --- | --- |
| Loaded | The route or result was returned |
| Captured | A screenshot or contact sheet exists |
| Visually inspected | The reviewer opened and examined the relevant visible content |
| Interacted | The reviewer exercised the relevant controls and checked their effects |
| Unavailable or omitted | The check was blocked or not performed, with a reason |

These are independent observations: a captured screenshot need not have been inspected, and an interaction need not expose all the content. Metadata, filenames, counts and passing requests cannot substitute for viewing imagery.

## Judge the useful result

State the expected result in the user's terms before inspecting it. For example, selecting a material should return imagery suitable for that material and use, not merely a non-empty response with the right category label.

- Inspect actual images, including full-size crops when detail, finish, scale or aspect ratio matters. Contact sheets help cover a large set; inspect every sheet, then open ambiguous or small examples individually.
- Include empty, unsuitable and missing imagery. Don't silently drop them from the denominator.
- Separate presentation defects from semantic accuracy. A broken thumbnail and an irrelevant match have different causes even when they occur together.
- Check consistency across the requested variants, states and viewports. Avoid claiming every combination when only a representative sample was seen.
- For generated output, inspect the artefact the user receives, not just the success status or source that produced it.

## Report coverage honestly

Give counts against the named denominator and list gaps. For example: “34 cases requested; 34 loaded, 34 captured, 26 visually inspected, 8 uninspected. Interaction checked on 6.” Identify the remaining case IDs when the user requested all of them, and continue until those checks are completed or a concrete access limit prevents them.

A sample can support a finding about that sample. It cannot support “all checked”. Preserve the evidence-to-case mapping so a reader can reproduce each finding and see the limits of a clean result.
