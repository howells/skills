# Howells Skills - Agent Instructions

## Communication Expectations
- Name the skill you are changing and the user task it is meant to serve.
- Explain whether a change affects installation, routing, references, scripts, or the skill body.
- Keep skill docs practical and executable for agents, not broad essays.

## How To Work In This Codebase
- This repo is an independent collection of `skills.sh`-compatible agent skills.
- Each skill lives in its own directory with `SKILL.md`; supporting assets/scripts should stay local to that skill.
- Each skill also carries `agents/openai.yaml` (installer/host metadata: `display_name`, `short_description`, `default_prompt`). It is a third sync surface — update it whenever the skill's frontmatter `description` changes, keeping `default_prompt` referencing `$<skill-name>`.
- `README.md` is the public catalog and install guide.
- Do not copy these skills into product repos; install or invoke them from the agent environment.
- Removing or renaming a skill here does not update existing installs (`npx skills` copies files; it does not track deletions). When a skill is deleted or merged, note it in the README and manually uninstall the stale copy from local/global install locations.

## Editing Constraints
- Keep each `SKILL.md` self-contained enough for a fresh agent to use.
- Do not add hidden dependencies on local files without linking them from the skill body.
- Do not broaden a skill unless its trigger and output stay clear.
- Avoid repo-specific product assumptions in reusable skills.
- Keep each skill's frontmatter `description` within ~500 characters (long descriptions get truncated in some host listings). Use terse cross-skill pointers, not full sentences, to disambiguate overlapping scope.

## Search Preferences
- Search the target skill directory before editing shared README text.
- Search related skills to avoid duplicate scope. The known overlap hotspots are chiaroscuro/componentize/heathen/aperture (UI design, componentization, decomposition, package extraction) and foundry (brand/identity); also check fieldtest, mastraudit, and fenceline before broadening scope.
- For installer behavior, verify current `skills` CLI examples before changing docs.

## Commands
- `npx skills@latest add howells/skills --list` - list installable skills.
- `npx skills@latest add howells/skills --skill '*' --agent codex --global` - install all globally for Codex.
- `python3 scripts/check-skills.py` - consistency gate. Run before committing any skill change: it checks the three sync surfaces (frontmatter description ↔ README section ↔ `agents/openai.yaml`), intra-skill `.md` link integrity, the ~500-char description budget, and verbatim trigger-clause overlap between skills. Exits non-zero on errors.
- This repo has no package-level test or build script beyond `check-skills.py`; otherwise verify by reading and targeted search.

## Repo-Specific Rules
- Use Arc for development planning if a skill change spans multiple skills or install behavior.
- Use Mastra only in skills that explicitly audit or build Mastra systems; this repo is not a Mastra runtime.
- Keep README summaries and each skill's `agents/openai.yaml` synchronized with its `SKILL.md` description; `scripts/check-skills.py` enforces this.
