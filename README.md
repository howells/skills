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
npx skills@latest add howells/skills --skill northstar --agent codex --global
```

Use `--copy` if you want independent files rather than symlinks.

## Skills

- `aperture` — extract reusable packages, features, components, hooks, or utilities.
- `chiaroscuro` — create distinctive Tailwind v4 UI design direction and polish.
- `deslop` — rewrite prose that carries AI-writing tells.
- `fieldtest` — test rendered web apps in a browser with evidence-backed findings.
- `foundry` — define Tailwind v4 visual identity and brand systems.
- `heathen` — find and split god components, scripts, and duplicated logic.
- `mastra-audit` — audit Mastra implementations, package boundaries, and domain folders.
- `nomen` — generate and validate names.
- `northstar` — create or revise project vision documents.

Restart your agent after installing new skills.
