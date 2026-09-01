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

Extract app-local components, hooks, utilities, or subsystems into reusable packages with stable exports and tests. Use for package extraction or moving code to its own repository. For in-place decomposition use `heathen`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill aperture --agent codex --global
```

### `chiaroscuro`

Design, build, restyle, and polish user-facing web interfaces end to end with distinctive visual direction, Tailwind v4, responsive and accessible behavior, and browser verification. Use for components, screens, pages, apps, dark mode, responsiveness, or UI that should feel complete. For brand identity use `foundry`; for reuse audits use `componentize`; for interface copy use `signage`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill chiaroscuro --agent codex --global
```

### `componentize`

Find duplicated UI and turn it into scoped shared components or UI-package primitives. Use for componentization, repeated React/Tailwind patterns, Turborepo `ui` packages, or adapting an existing component through props and composition. For standalone package extraction use `aperture`; for oversized logic files use `heathen`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill componentize --agent codex --global
```

### `deslop`

Rewrite prose that sounds synthetic, inflated, generic, or assistant-like. Use for AI-writing tells, vague attribution, suspicious citations, chatbot artifacts, or copy that should sound grounded and human. Applies to prose; for interface labels and microcopy use `signage`; for machine-written code tells use `unslop`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill deslop --agent codex --global
```

### `fail-fast`

Remove hidden fallbacks, swallowed errors, legacy aliases, permissive defaults, and silent compatibility paths. Use when configuration or control flow should have one canonical path and explicit failure modes, including deterministic environment handling with Envy.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill fail-fast --agent codex --global
```

### `fenceline`

Add, check, explain, or repair JavaScript and TypeScript architecture boundaries with `@howells/boundaries`. Use for Turborepo package rules, app-to-app import prevention, source-layer profiles, package tags, or fixing violations without weakening the intended architecture.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill fenceline --agent codex --global
```

### `fieldtest`

Test a rendered web app in a real browser and return evidence-backed QA findings. Use for dogfooding, localhost review, responsive or mobile defects, console or accessibility checks, persona walkthroughs, and frontend validation that must exercise the running interface rather than inspect code alone.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill fieldtest --agent codex --global
```

### `foreman`

Implement substantial production changes in foreman mode: the main agent plans, briefs, and reviews while subagents write code, routed by taste, heavy, or grunt work. Use for implementation or refactoring that benefits from delegated execution. Skip for tiny fixes or documentation-only work.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill foreman --agent codex --global
```

### `foundry`

Create, review, or revise a distinctive visual identity system: positioning, rendered direction options, OKLCH palette, typography, visual character, and Tailwind v4 tokens. Use when a product needs brand identity established before interface design. For screen-level UI direction use `chiaroscuro`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill foundry --agent codex --global
```

### `glm-review`

Get an independent read-only review from GLM 5.3 Flash on the Z.AI Coding Plan via OpenCode, then verify its claims before acting. Use when the user asks for a GLM review, or a cheap second opinion on a diff, plan, contract or UI.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill glm-review --agent codex --global
```

### `heathen`

Find and refactor god components, oversized modules, tangled scripts, and multi-responsibility JavaScript or TypeScript files. Use for safe decomposition, responsibility splits, and extracting duplicated logic inside a codebase. For repeated UI components use `componentize`; for package extraction use `aperture`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill heathen --agent codex --global
```

### `inquest`

Answer a question about intent, history, or provenance by sweeping every available evidence source in parallel, then return a cited answer and coverage map. Use when a claim, decision, or number needs proving beyond the code. For rebuilding current working context use `muster`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill inquest --agent codex --global
```

### `marginalia`

Add concise, useful JSDoc where IDE hover help matters. Use for public JavaScript or TypeScript APIs, exports, components, hooks, classes, complex types, generated API docs, or package publishing. Clarifies non-obvious behavior without commenting everything or changing code.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill marginalia --agent codex --global
```

### `mastraudit`

Audit a Mastra codebase against execution failures first: workflow step size, fan-out keying, suspend and resume payloads, load-bearing writes, model settings, and visible tool keys. Use for pre-ship review or an existing Mastra implementation. For building Mastra features use `$mastra`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill mastraudit --agent codex --global
```

### `memento`

Report what this task is doing now from live state: original ask, completed work, remaining work, branch, uncommitted files, and drift. Use when returning to a long session or checking whether an agent is still on track. For a roll-call across tasks use `muster`; for rewriting only the last reply use `what`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill memento --agent codex --global
```

### `muster`

Rebuild working context across concurrent or older agent tasks from transcripts, git state, peer sessions, and the tracker. Use for 'catch me up', 'where did I leave off', or 'what is in flight', returning every active thread and its next move. For evidence-backed investigation use `inquest`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill muster --agent codex --global
```

### `nomen`

Generate, critique, and validate names for products, projects, packages, CLIs, apps, brands, or features. Use for naming or renaming work where domain, package, GitHub, App Store, directory, or web conflict checks matter.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill nomen --agent codex --global
```

### `polyplugin`

Create, audit, or migrate agent plugins across Claude Code, Codex, and Cursor. Use for multi-host manifests, marketplace metadata, shared capability paths, release and version alignment, or deciding whether a skill collection should become a plugin.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill polyplugin --agent codex --global
```

### `product-description`

Document a product outside-in as user-visible behavior drafted from code and tests, verified in the running product, and consolidated into bug triage. Use for complete experience documentation across web, mobile, canvas, CLI, chat, or agent products.

Imported from [Steve Ruiz's original `product-description` gist](https://gist.github.com/steveruizok/83ae5c53f2784ebf8f5fe0a3fb94480f).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill product-description --agent codex --global
```

### `salvage`

Rescue work that exists in only one place - detached HEADs, worktrees, unpushed branches, or stashes - then remove only what is proven merged and pushed. Use for repository cleanup where ambiguous work must be preserved and each surviving thread named. For status reconstruction without cleanup use `muster`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill salvage --agent codex --global
```

### `signage`

Replace invented interface vocabulary with the words the audience already uses. Labels, headings, buttons, status lines, empty states and template-generated strings, checked against how a person doing that job would say them out loud. Use after building or designing any UI. For body prose use `deslop`; for names use `nomen`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill signage --agent codex --global
```

### `survey`

Grade an entire codebase with a stage-calibrated verdict, clustered findings, and comparable scores. Use for repository health audits where mechanical checks, source-confirmed findings, lifecycle stage, and multiple review lenses matter. For a diff or PR use code review; for Mastra use `mastraudit`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill survey --agent codex --global
```

### `unslop`

Remove machine-written code tells from a diff without changing behavior: narrating comments, one-caller wrappers, impossible guards, unused options, decorative logs, and leftover scaffolding. Use before commit or review. For behavior-changing fallback cleanup use `fail-fast`; for prose use `deslop`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill unslop --agent codex --global
```

### `what`

Rewrite only the previous agent reply into three short, plain-language lines: what happened, where things stand, and what comes next. Use when the last message was dense, jargon-heavy, or unclear. It re-explains existing content; for whole-task status use `memento`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill what --agent codex --global
```
