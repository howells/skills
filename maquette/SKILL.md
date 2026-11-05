---
name: maquette
description: "Explore design options for a page, component or region as live variants in the running app, switch or compare them, then keep one and delete the rest. Use when asked for options, alternatives or directions. Not for one settled direction (`chiaroscuro`) or Paper (`paste-up`)."
---

# Maquette

A maquette is the small model a sculptor makes before committing to the full piece. For UI: the current version plus several genuinely different directions, rendered in the running app behind a temporary picker, one choice, then the chosen direction built properly and every rejected one removed.

When the user already gave a direction, or asked to match or extend an existing design, build it with `chiaroscuro` instead.

## Hard Rules

1. **Exploration runs only in development.** Guard the selection, compare mode and picker together, not only the visible picker. Outside development the host renders `Current` and ignores the `maquette` URL key, so production is unchanged until the user chooses.
2. **Directions differ on a named axis:** structure, density, emphasis, type, voice or interaction model. Two that differ only in accent colour or copy are one direction; replace one.
3. **One source of truth.** All directions share content, data, state, events and validation. Never fork an API call, loader, mutation or business rule. Vary presentation only.
4. **Every direction is complete.** Real content at the real item count, the whole piece and its core path working. No fragment, mood board, lorem ipsum or dead button.
5. **No small caps, tracked uppercase or decorative mono.** No eyebrows, kickers, section labels, chips or table headings in capitals. Mono is for literal code, identifiers and values whose characters need inspecting. Proper acronyms keep their capitals.
6. **No prose where interface belongs.** A paragraph explaining a screen means the screen has failed. Replace it with a label, a control, a value or nothing. Keep only consent, constraints and error recovery.
7. **Four to six type styles, in chosen faces.** Use the product's named roles. Before choosing a new face, read the bundled [font guidance](references/font-guidance.md), choose from it and follow its never-use list; Instrument Serif is the first name on that list.
8. **Reuse before you build.** Use the existing component, shell, header or control, in this product or any package the user pointed to. A second version of an existing control is a defect.
9. **One of each.** One corner-radius scale with concentric nesting, one icon family at one stroke weight, one control height per density. Touch targets at least 44 by 44 CSS pixels.

Rules 5 to 9 are `chiaroscuro`'s. Directions differ within them, never by breaking them.

## Workflow

### 1. Scope and inspect

One piece per run: a page, a component or a region. If the request spans several ("the dashboard"), pick the highest-leverage piece and offer the rest as later runs.

Read the piece, its shell, tokens and real content. The product's density and voice bound how far the boldest direction may go. Note any uncommitted work first, so cleanup never sweeps it up.

### 2. Name the set

Before any code, write down `Current` and the new directions, each with a name and an axis position. Three directions for a component or region, five for a page; never more than five unless asked.

Name each by its visible idea (`Ledger`, `Index`, `Rail`), never `A`, `B` or an abstract adjective. Picker labels, URL keys and the final question use the same names. For a new route, `Current` is a conservative baseline built from the product's shell, components and tokens.

### 3. Build into the real app

Host the directions where the piece really renders: its real route, shell, neighbours and data. No standalone preview app. Only if the app cannot run, build one self-contained HTML file with the same picker.

Each direction lives in its own temporary file. Lift effects, loaders and mutations above the choice; only the host imports a direction:

```tsx
const directions = { current: Current, ledger: Ledger, index: Index }
const Direction = directions[active]
return <Direction model={sharedModel} actions={sharedActions} />
```

- Never edit a shared component, token, global stylesheet or layout for a direction; that changes `Current`, the other directions and production at once. Wrap or copy inside the direction's file.
- Scope styles to the direction: Tailwind classes, a CSS module or a selector under its root. A plain stylesheet import applies to every direction.
- Never gitignore direction files. Tailwind v4 skips ignored files when scanning for classes, so the direction renders unstyled.

### 4. Mount the picker

Read [references/picker.md](references/picker.md) when building `DirectionPicker`: URL contract, keys, framework gotchas, markup and compare mode. It is review tooling with a fixed look, never styled with the project's tokens, or it becomes part of the design being judged.

- **Switch** (always): one direction at a time, full size, instant.
- **Compare** (component or region only): every direction side by side at its real width. A page is judged by switching, never in thumbnails, because spacing and scale are what is being chosen.

### 5. Look, then ask once

Flip through every direction in a browser at desktop and phone width and fix what is broken. Without a browser, say so and give the URL.

Then ask one question: the picker URL, `Current` and every direction as options, one line each on when it wins and what it costs. Never mark a favourite. Asked directly, answer from how often the piece is seen and the product's personality, not from what was fun to build.

If the user wants another round, delete the rejected directions, keep the picker, and build new positions around the one they leaned toward.

### 6. Keep one, delete the rest

1. Move the chosen direction into the project's own file layout and naming.
2. Delete every other direction (including `Current` unless chosen), `DirectionPicker`, the direction map, the URL key, the development guard, and anything only they used.
3. Harden the chosen path: empty, loading, failure, keyboard, mobile and dark-mode states. Use `chiaroscuro` when installed.
4. Search for `DirectionPicker`, `maquette` and every rejected direction name; leftovers hide in imports and styles. The diff from the start holds the chosen direction and nothing else.

If the user asks to keep the picker, keep it and the directions and say what remains.

## Gotchas

- Near-identical directions teach nothing. If two converge while building, cut one and say so; two distinct directions beat five padded ones.
- Vary one primary axis and let the rest follow. A dense direction needing a smaller type step is coherence, not a second axis.
- Judging on a blank route hides the real neighbours and data.
