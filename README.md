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

Extract components, hooks, utilities, features, or subsystems from an existing codebase into reusable packages, workspace packages, or standalone publishable repositories. Use it when code needs a clean public API, stable exports, examples, tests, and a package boundary instead of app-local imports.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill aperture --agent codex --global
```

### `chiaroscuro`

Create distinctive UI direction, Tailwind v4 design specs, wireframes, visual systems, and post-implementation polish. Use it when a screen, page, app, or component needs a concrete visual direction that avoids generic AI-looking interface work.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill chiaroscuro --agent codex --global
```

### `componentize`

Audit and improve repeated UI by finding duplicated components, repeated JSX patterns, and missed reuse opportunities. Use it to promote scoped shared components, adapt existing primitives, or move reusable UI into the right package boundary.

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

Find and remove unnecessary fallbacks, silent compatibility paths, legacy aliases, swallowed errors, permissive defaults, and ambiguous configuration behavior. Use it when a codebase should prefer one canonical path and one explicit failure mode.

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

Test a rendered web app in the browser and report evidence-backed QA, UX, responsive, console, accessibility, and persona-based findings. Use it when you need to experience a local app as software instead of only inspecting code.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill fieldtest --agent codex --global
```

### `foundry`

Create, review, or revise a distinctive visual identity system — brand positioning, rendered direction options to compare, OKLCH palettes, typography, visual character, and a Tailwind v4 `@theme` token model (or `docs/brand-system.md`). Use it when a product needs a brand established before UI, loose identity ideas turned into usable direction, or a system tied directly to implementation. (Absorbs the former `brand` skill — if you have `brand` installed, uninstall it and install `foundry`.)

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill foundry --agent codex --global
```

### `heathen`

Find and refactor god components, god scripts, oversized modules, tangled multi-responsibility files, and duplicated logic in JavaScript or TypeScript codebases. Use it to identify safe decomposition steps before splitting code.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill heathen --agent codex --global
```

### `marginalia`

Add useful, concise JSDoc to JavaScript and TypeScript APIs, exports, components, hooks, classes, complex types, and behavior where IDE hover help matters. Use it when documentation should clarify public or non-obvious code without commenting everything.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill marginalia --agent codex --global
```

### `mastraudit`

Audit Mastra implementations in JavaScript and TypeScript codebases. Use it to check current Mastra guidance, contain Mastra dependencies and imports, organize Mastra code into clear domain folders, and keep product behavior in runtime/domain code instead of Mastra wrappers.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill mastraudit --agent codex --global
```

### `nomen`

Generate, critique, and validate names for projects, products, apps, packages, CLIs, brands, and features. Use it when naming or renaming something and when current availability, conflict, package, GitHub, or domain checks matter.

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
