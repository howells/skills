---
name: ask-howells
description: "Route a situation to the skills in this collection and the command to type. Not for doing the work."
disable-model-invocation: true
---

# Ask Howells

Nobody remembers thirty-odd skills. Describe where you are, and this names what to type next.

## Rules

1. **Recommend, then stop.** Answer with the route and the exact first invocation, in the host's syntax (`/next` in Claude Code, `$next` in Codex). Don't start the work, open the files or fire the skill.
2. **Open a skill before making a claim about it.** The map below is a summary. Before saying anything load-bearing about what a skill does - that it covers a case, skips a step, or makes another unnecessary - read that skill's `SKILL.md` from where it is installed. Where the map and a `SKILL.md` disagree, the `SKILL.md` is right.
3. **Explicit-only skills are missing from the list, not from the machine.** `maquette`, `simplify` and this router don't appear in the skill list an agent is given. Check the install directory before reporting any skill as absent.
4. **When two skills are close, give the test that separates them** - usually one concrete question - and say why the other one is wrong here.
5. **When nothing fits, say so.** This map covers this collection only. Don't stretch a skill to cover a situation it wasn't written for.

## The map

### Shipping tracked work

- **The backlog is out of order for a goal or deadline** → `rebalance`. It reprioritises and stops before any code.
- **Deliver the next item** → `next`, one fresh task per item. It claims the item, builds it and opens a PR.
- **Reading or writing tracker items directly** → `linear`, which ships with the `howells/linearcli` repo rather than this collection.
- **You want subagents to write the code while the main agent decides and inspects** → `foreman`. Only when asked for by name.
- **Checks, polls or re-planning are crowding out anything visible** → `plimsoll`. It applies inside every route here.

Route: `rebalance` → `next`, repeated. `plimsoll` whenever delivery stalls.

### Building UI

- **A whole page whose direction isn't settled** → `maquette`: five directions beside the current page, pick one, it builds it.
- **One direction, a component or a region** → `chiaroscuro`.
- **The app scrolls like a document and should behave like an app** → `armature`.
- **It breaks on laptops, tablets or phones** → `reflow`.
- **Raw font utilities have multiplied** → `typecase`.
- **Labels, buttons, headings or empty states read badly** → `signage`.
- **Duplicated components, or a file doing too many jobs** → `componentize`.
- **Motion: should it animate, build it, review it, or find where it should move** → `zoetrope`.
- **See it running and find what's wrong** → `fieldtest`. Reports only unless asked to fix.
- **The design lives in a Paper file** → `paste-up`.

Route for a new page: `maquette` → `armature` if it's an app shell → `reflow` → `signage` → `fieldtest`.

### Code quality

- **Review a diff or a whole codebase** → `simplify`. It reports; fixing needs asking for.
- **A diff reads machine-written** → `unslop`. Behaviour stays the same.
- **Errors swallowed, fallbacks hiding failures** → `fail-fast`. Behaviour changes on purpose.
- **Setting up lint** → `howells-lint`, which ships with the `howells/lint` package repo rather than this collection.
- **Exported APIs need hover docs** → `marginalia`.
- **Any Mastra code** → `mastraudit`, before writing and before calling it done.

Route: `simplify` → the skill each finding points at.

### A second opinion

- **A hard judgement call** - architecture, taste, a plan worth arguing with → `fable-review`.
- **A cheap bounded check** against stated criteria → `glm-review`.

### Lost the thread

- **The last reply didn't land** → `what`.
- **Where this task stands** → `memento`.
- **Several tasks, or older ones** → `muster`.
- **Git work stranded in worktrees, stashes or unpushed branches** → `salvage`. Run `muster` first if you don't know what's still live.

### Writing

- **Prose** → `deslop`.
- **Interface strings** → `signage`.
- **A name for a product, package or feature** → `nomen`.
- **Documenting what a product does, feature by feature** → `product-description`.

### Accounts and tools

`gog` (Google Workspace), `web-research` (the open web), `blender` (3D scenes). `linear` and `starling` ship with their CLIs, in `howells/linearcli` and `howells/starlingcli`.

## Close pairs

| Pair | The test |
| --- | --- |
| `maquette` / `chiaroscuro` | Is the direction for a whole page still open? Yes: `maquette`. |
| `chiaroscuro` / `armature` | Is the problem how it looks, or what scrolls? Scrolling: `armature`. |
| `chiaroscuro` / `zoetrope` | Is the question how it looks still, or how it moves? Moves: `zoetrope`. |
| `reflow` / `fieldtest` | Do you want it fixed at every size, or a report of what's wrong? Fixed: `reflow`. |
| `unslop` / `fail-fast` | Should behaviour stay exactly the same? Yes: `unslop`. |
| `unslop` / `simplify` | Cleaning a diff, or judging its structure? Judging: `simplify`. |
| `deslop` / `signage` | Paragraphs, or words on a control? Controls: `signage`. |
| `fable-review` / `glm-review` | Is there a right answer to check against? Yes: `glm-review`. |
| `what` / `memento` / `muster` | The last reply, this task, or many tasks. |
| `rebalance` / `next` | Deciding the order, or doing the work? Doing: `next`. |

## Output

```
Route:  `skill` → `skill`
Why:    <one line tied to their situation>
Type:   <the exact first invocation>
```

Add one line for each point in the route where the user decides something or should review. Nothing else.
