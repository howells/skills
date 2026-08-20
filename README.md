# Howells Skills

Reusable agent skills for Codex and other `skills.sh`-compatible coding agents.

## Install

List the skills in this collection:

```bash
npx skills@latest add howells/skills --list
```

Install interactively:

```bash
npx skills@latest add howells/skills
```

Install all skills globally for Codex:

```bash
npx skills@latest add howells/skills --skill '*' --agent codex --global
```

Use `--copy` if you want independent files rather than symlinks. Restart your agent after installing new skills.

## Skills

### `aperture`

Extract components, hooks, utilities, features, or subsystems from an existing codebase into reusable packages, workspace packages, or standalone publishable repositories. Use it when code needs a clean public API, stable exports, examples, tests, and a package boundary instead of app-local imports. For a tangled god file that needs decomposition first, use `heathen`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill aperture --agent codex --global
```

### `chiaroscuro`

Create distinctive, non-generic UI design direction, Tailwind v4 visual systems, `@theme` tokens, wireframes, and design specs, plus UI polish, dark mode, responsive adaptation, and live variant comparison. Use it when a screen, page, app, or component needs a concrete visual direction that avoids generic AI-looking work. For codebase-wide reuse audits or shared-component extraction, use `componentize`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill chiaroscuro --agent codex --global
```

### `componentize`

Audit a codebase for duplicated UI and repeated component patterns, then plan or implement scoped shared components and UI package changes. Use it to reduce duplication, adapt existing primitives with props/composition, use a Turborepo `ui` package, or componentize a visually referenced region like "the panel on the right." For a standalone or publishable package, use `aperture`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill componentize --agent codex --global
```

### `deslop`

Audit and rewrite prose that sounds synthetic, inflated, generic, or assistant-like. Use it to clean up AI-writing tells, suspicious citations, vague attribution, markdown artifacts, and copy that needs a more grounded human voice.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill deslop --agent codex --global
```

### `fail-fast`

Find and remove unnecessary fallbacks, silent compatibility paths, legacy aliases, swallowed errors, permissive defaults, and ambiguous configuration behavior. Use it when a codebase should prefer one canonical path and one explicit failure mode, or to harden env handling with Envy.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill fail-fast --agent codex --global
```

### `fenceline`

Add, check, explain, or repair JavaScript and TypeScript architecture boundaries with `@howells/boundaries`. Use it for Turborepo package boundaries, source-layer profiles, app-to-app import prevention, and boundary violation fixes.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill fenceline --agent codex --global
```

### `fieldtest`

Test a rendered web app in the browser and report evidence-backed QA, UX, console, accessibility, persona-based, and responsive/mobile findings. Use it when you need to experience a local app as software - and find and report rendered defects - instead of only inspecting code.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill fieldtest --agent codex --global
```

### `foreman`

Foreman-mode implementation: the main loop plans, specs, and reviews while delegated subagents write the production code, routed across three tiers - taste for judgment-heavy surfaces, heavy for spec-complete but interlocking work, grunt for mechanical work. The task picks the tier; the model the foreman itself runs on sets the economy - a frontier host delegates harder, writes denser specs, and holds every brief and report to a terse format, while a cheaper host reserves the frontier model as a scalpel for narrow, genuinely hard problems. Host-agnostic and native-only, with no cross-CLI spend. Diffs get reviewed by the foreman itself, and fixes go back to the same agent that wrote them.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill foreman --agent codex --global
```

### `foundry`

Create, review, or revise a distinctive visual identity system - brand positioning, rendered direction options to compare, OKLCH palettes, typography, visual character, and a Tailwind v4 `@theme` token model (or `docs/brand-system.md`). Use it when a product needs a brand established before UI, loose identity ideas turned into usable direction, or a system tied directly to implementation. (Absorbs the former `brand` skill - if you have `brand` installed, uninstall it and install `foundry`.)

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill foundry --agent codex --global
```

### `heathen`

Find and refactor god components, god scripts, oversized modules, tangled multi-responsibility files, and duplicated logic in JavaScript or TypeScript codebases. Use it to identify safe decomposition steps before splitting code. For duplicated UI components, use `componentize`; heathen targets logic, modules, scripts, and file decomposition.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill heathen --agent codex --global
```

### `inquest`

Answer a question about intent or history from evidence rather than from the code, sweeping every source available in the session - source control, tickets, chat, docs, database, observability, analytics - one investigator each in parallel. Returns a cited answer plus a coverage map where an empty search and a skipped source are both reported. Use it when a claim needs proving, a decision needs explaining, or a number needs a source. To rebuild your own working context, use `muster`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill inquest --agent codex --global
```

### `marginalia`

Add useful, concise JSDoc to JavaScript and TypeScript APIs, exports, components, hooks, classes, complex types, and behavior where IDE hover help matters. Use it when adding or improving docs for public APIs, exported symbols, generated API docs, or package publishing - clarifying non-obvious code without commenting everything or changing behavior.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill marginalia --agent codex --global
```

### `mastraudit`

Audit a Mastra codebase against what actually breaks it, worst first - workflow step size and fan-out keying, suspend and resume payloads, load-bearing writes that must throw, model settings nesting, the tool keys a model actually sees - and only then containment and domain structure. Runs shipped boundary scanners where they exist and falls back to search. Use it when reviewing Mastra work before shipping or auditing an existing implementation. For building rather than judging, use the `$mastra` skill.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill mastraudit --agent codex --global
```

### `memento`

Answer "what are you working on right now" from current state rather than from the transcript - the original ask, what landed, what is left, the live branch and uncommitted files, and whether the work has drifted from what was requested. Returns one screen with no archaeology. Use it when returning to a long-running session, checking an agent is still on track, or telling an agent to report in. For a sweep across many sessions, use `muster`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill memento --agent codex --global
```

### `muster`

Rebuild working context after time away or across concurrent agent sessions - recent transcripts newest-first, live branch and PR state, peer sessions and the paths each one owns, and the tracker. Returns a status-tagged brief of every thread in flight with one concrete next move. Use it for "catch me up", "where did I leave off", or before resuming work started in another session. To investigate a question against external evidence, use `inquest`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill muster --agent codex --global
```

### `nomen`

Generate, critique, and validate names for projects, products, apps, packages, CLIs, brands, and features. Use it when naming or renaming something and when current availability, conflict, package, GitHub, domain, or App Store / app-directory checks matter.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill nomen --agent codex --global
```

### `polyplugin`

Create, audit, or migrate agent plugins that work across Claude Code, Codex, and Cursor. Use it for multi-host manifests, shared plugin metadata, Cursor `.cursor-plugin` packaging, marketplace entries, and deciding whether a skill collection should become a plugin.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill polyplugin --agent codex --global
```

### `salvage`

Find and rescue work that exists in only one place - detached HEADs, uncommitted worktrees, unpushed branches, stashes - then remove only what is provably merged and pushed. Names what each salvaged thread was for from the branch and the tracker, and treats any worktree that might belong to a live peer session as untouchable. Use it for tidying branches, worktrees and stashes, or before a machine cleanup. To rebuild your own working context instead, use `muster`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill salvage --agent codex --global
```

### `unslop`

Strip the tells of machine-written code from a diff without changing what it does - comments narrating the line below, one-caller wrappers, guards against states the types forbid, options nobody passes, decorative log output and leftover scaffolding. Run it before commit or review. Behaviour-changing cleanups belong elsewhere - fallbacks and swallowed errors are `fail-fast`, oversized modules are `heathen`, doc comments worth keeping are `marginalia`, and prose is `deslop`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill unslop --agent codex --global
```

### `what`

Cut the last message down to what actually happened - short, and translated out of jargon and tool names into what was done and what it means for the reader. Called because the previous reply was long and dense, so brevity is the product. Re-explains, never re-answers, and never starts new work. Use it when a reply did not land, when an agent has been grinding and its last update made no sense, or for "wait, what did you just do". For the state of the whole task instead, use `memento`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill what --agent codex --global
```
