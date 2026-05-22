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

Install one skill globally for Codex:

```bash
npx skills@latest add howells/skills --skill chiaroscuro --agent codex --global
```

Use `--copy` if you want independent files rather than symlinks.

## Skills

- `aperture` — extract reusable packages, features, components, hooks, or utilities.
- `chiaroscuro` — create distinctive Tailwind v4 UI design direction and polish.
- `componentize` — audit duplicated UI and promote scoped shared components.
- `deslop` — rewrite prose that carries AI-writing tells.
- `fenceline` — add and check JavaScript/TypeScript architecture boundaries.
- `fieldtest` — test rendered web apps in a browser with evidence-backed findings.
- `foundry` — define Tailwind v4 visual identity and brand systems.
- `heathen` — find and split god components, scripts, and duplicated logic.
- `marginalia` — add concise JSDoc to APIs, exports, and complex code.
- `mastraudit` — audit Mastra implementations, package boundaries, and domain folders.
- `nomen` — generate and validate names.
- `polyplugin` — create and validate dual Claude Code and Codex plugins.

Restart your agent after installing new skills.
