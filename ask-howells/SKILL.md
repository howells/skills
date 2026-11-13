---
name: ask-howells
description: "Route a situation to the skills in this collection and the command to type. Not for doing the work."
disable-model-invocation: true
---

# Ask Howells

## Rules

1. **Recommend, then stop.** Answer with the route and the exact first invocation, in the host's syntax (`/chiaroscuro` in Claude Code, `$chiaroscuro` in Codex). Don't start the work, open the files or fire the skill.
2. **Open a skill before making a claim about it.** The map below is a summary. Before saying anything load-bearing about what a skill does - that it covers a case, skips a step, or makes another unnecessary - read that skill's `SKILL.md` from where it is installed. Where the map and a `SKILL.md` disagree, the `SKILL.md` is right.
3. **Explicit-only skills are missing from the list, not from the machine.** `fettle` and this router don't appear in the skill list an agent is given. Check the install directory before reporting any skill as absent. A skill from another repo (`implement`, `code-review`, `howells-lint`, `linear`, `starling`) is optional: check it is installed before giving its invocation, and if it isn't, say which repo ships it.
4. **When two skills are close, give the test that separates them** - usually one concrete question - and say why the other one is wrong here.
5. **When nothing fits, say so.** This map covers this collection only. Don't stretch a skill to cover a situation it wasn't written for.

## The map

### Shipping tracked work

- **The backlog is out of order for a goal or deadline** → `rebalance`. It reprioritises and stops before any code.
- **Deliver an item** → `implement` where installed (from `mattpocock/skills`). One fresh task per item.
- **Reading or writing tracker items directly** → `linear` where installed (from `howells/linearcli`).

Route: `rebalance`, then deliver each item.

### Building UI

- **Options to choose between, for a page, component or region** → `maquette`: live variants in the app, switch or compare, keep one, delete the rest.
- **One settled direction, whether a page, component or region** → `chiaroscuro`.
- **A screenshot, page or frame that feels off, visual critique only** → `chiaroscuro`. It names what's off and asks; it changes nothing until asked.
- **The app scrolls like a document and should behave like an app** → `armature`.
- **It breaks on laptops, tablets or phones, or works on a phone but feels like a website: safe areas, viewport units, input zoom, touch, overscroll, Safari's bars, PWA install** → `reflow`.
- **Raw font utilities have multiplied** → `typecase`.
- **Labels, buttons, headings or empty states read badly** → `signage`.
- **Duplicated components, or a file doing too many jobs** → `componentize`.
- **Motion: should it animate, build it, review it, find where it should move, cut it back, name an effect, or diagnose stutter** → `zoetrope`. Includes preserving identity through expanding models and diagrams.
- **See it running and find what's wrong, including the usefulness of returned images or results** → `fieldtest`. Reports only unless asked to fix.
- **The design lives in a Paper file** → `paste-up`.
- **A product film or video, a new cut of one, or sound for it** → `rostrum`. It sends motion, look and words to `zoetrope`, `chiaroscuro` and `signage`.

Route for a new page: `maquette` when options are wanted, otherwise `chiaroscuro`; then `armature` if it needs an app shell → `reflow` → `signage` → `fieldtest`.

### Code quality

- **Review a branch or PR against its spec and repo standards** → `code-review` where installed (from `mattpocock/skills`).
- **Review the structure of a diff or whole codebase** → `fettle`. It reports numbered clusters, then fixes the ones you pick. A focus (`security`, `performance`, `state machines`) narrows it.
- **A diff reads machine-written** → `unslop`. Behaviour stays the same.
- **Errors swallowed, fallbacks hiding failures** → `failfast`, including test-only code and mocks in production. Behaviour changes on purpose.
- **Setting up lint** → `howells-lint` where installed (from `howells/lint`).
- **Exported APIs need hover docs** → `marginalia`.
- **Any Mastra code** → `mastraudit`, before writing and before calling it done.

### A second opinion

- **Review feedback has arrived (bot, PR comments, agent, model), or an independent read of a decision, code or stated criteria is wanted** → `review`. For an independent read, add a model argument; a named model takes precedence, otherwise the skill selects the lane for the question.

### Lost the thread

- **Where this task stands** → `memento`.
- **Work in flight across concurrent sessions, an older project's purpose, or a cross-session handoff** → `muster`.
- **Git merge or rebase conflicts, or work stranded in worktrees, stashes or unpushed branches** → `salvage`. Run `muster` first if you don't know what's still live.

### Writing

- **Prose** → `deslop`.
- **Interface strings** → `signage`.
- **A name for a product, package or feature** → `nomen`.
- **Documenting what a product does, feature by feature** → `product-description`.

### Accounts and tools

`browse` (the user's real browser, with their logins, through the browse extension), `gog` (Google Workspace), `research` (questions answered from primary sources, through Fieldwork when configured), `blender` (3D scenes), `computer-use` (native macOS app control, Chrome included, through the session's native Computer Use tools, with a headless Codex runner as fallback; ordinary browser-only QA stays with `fieldtest`). Where installed, `linear` and `starling` ship with their CLIs, in `howells/linearcli` and `howells/starlingcli`.

## Close pairs

| Pair | The test |
| --- | --- |
| `chiaroscuro` / `armature` | Is the problem how it looks, or what scrolls? Scrolling: `armature`. |
| `chiaroscuro` / `zoetrope` | Is the question how it looks still, or how it moves? Moves: `zoetrope`. |
| `reflow` / `fieldtest` | Do you want it fixed at every size, or a report of what's wrong? Fixed: `reflow`. |
| `unslop` / `fettle` | Cleaning a diff, or judging its structure? Judging: `fettle`. |
| `review` / `fettle` | Feedback to act on or an independent opinion on a bounded question, or a structural health review? Feedback or opinion: `review`. |

## Output

```
Route:  `skill` → `skill`
Why:    <one line tied to their situation>
Type:   <the exact first invocation>
```

Add one line for each point in the route where the user decides something or should review. Nothing else.
