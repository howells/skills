# Howells Skills

The independent collection of `skills.sh`-compatible agent skills. Each skill lives in its own directory with a `SKILL.md`; supporting assets and scripts stay local to that skill. `README.md` is the public catalogue and install guide.

## The skills

- `aperture` - extract a component, hook, utility or subsystem into a reusable package.
- `chiaroscuro` - UI design direction, wireframes, Tailwind v4 systems, `@theme` tokens, design specs, polish.
- `componentize` - audit a codebase for duplicated UI and plan or implement shared components.
- `deslop` - audit and rewrite prose carrying AI-writing tells.
- `fail-fast` - remove fallbacks, silent compatibility paths, legacy aliases and default env values.
- `fenceline` - add, check, explain or repair package and source architecture boundaries.
- `fieldtest` - browser QA of a rendered app with evidence-backed findings.
- `foreman` - foreman-mode implementation: the main loop plans and reviews, subagents write the code.
- `foundry` - visual identity systems, brand positioning, rendered direction options.
- `heathen` - find and refactor god components, god scripts and oversized modules.
- `marginalia` - JSDoc for public APIs and exported symbols.
- `mastraudit` - audit a codebase against current Mastra guidance.
- `nomen` - generate and validate names, with availability and conflict checks.
- `polyplugin` - create, audit or migrate agent plugins across Claude Code, Codex and Cursor.

## Three sync surfaces

Every skill's description exists in three places and they must agree: the `SKILL.md` frontmatter `description`, the skill's section in `README.md`, and `agents/openai.yaml` (installer metadata: `display_name`, `short_description`, `default_prompt`, whose `default_prompt` references `$<skill-name>`). Change one, change all three, then run the checker.

Keep each frontmatter `description` within about 500 characters - longer ones get truncated in some host listings. Use terse cross-skill pointers, not full sentences, to disambiguate overlapping scope.

## Editing skills

- Keep each `SKILL.md` self-contained enough for a fresh agent to use, with no hidden dependency on a local file that the body doesn't link.
- Don't broaden a skill unless its trigger and output stay clear, and keep repo-specific product assumptions out of reusable skills.
- Search related skills before broadening scope. The overlap hotspots are chiaroscuro/componentize/heathen/aperture (UI design, componentization, decomposition, package extraction) and foundry (brand and identity); also check fieldtest, mastraudit and fenceline.
- Search the target skill directory before editing shared README text.
- Verify current `skills` CLI examples before changing installer docs.
- Don't copy these skills into product repos; install or invoke them from the agent environment.
- Removing or renaming a skill doesn't update existing installs - `npx skills` copies files and doesn't track deletions. When a skill is deleted or merged, note it in the README and manually uninstall the stale copy from local and global install locations.

## Commands

- `python3 scripts/check-skills.py` - the consistency gate. Run before committing any skill change: it checks the three sync surfaces, intra-skill `.md` link integrity, the description budget and verbatim trigger-clause overlap between skills. Exits non-zero on errors.
- `npx skills@latest add howells/skills --list` - list installable skills.
- `npx skills@latest add howells/skills --skill '*' --agent codex --global` - install all globally for Codex.

There's no build or test script beyond `check-skills.py`; otherwise verify by reading and targeted search.
