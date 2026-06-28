# Howells Skills - Agent Instructions

## Communication Expectations
- Name the skill you are changing and the user task it is meant to serve.
- Explain whether a change affects installation, routing, references, scripts, or the skill body.
- Keep skill docs practical and executable for agents, not broad essays.

## How To Work In This Codebase
- This repo is an independent collection of `skills.sh`-compatible agent skills.
- Each skill lives in its own directory with `SKILL.md`; supporting assets/scripts should stay local to that skill.
- `README.md` is the public catalog and install guide.
- Do not copy these skills into product repos; install or invoke them from the agent environment.

## Editing Constraints
- Keep each `SKILL.md` self-contained enough for a fresh agent to use.
- Do not add hidden dependencies on local files without linking them from the skill body.
- Do not broaden a skill until its trigger and output stay clear.
- Avoid repo-specific product assumptions in reusable skills.

## Search Preferences
- Search the target skill directory before editing shared README text.
- Search related skills to avoid duplicate scope, especially UI, brand, fieldtest, mastraudit, and fenceline skills.
- For installer behavior, verify current `skills` CLI examples before changing docs.

## Commands
- `npx skills@latest add howells/skills --list` - list installable skills.
- `npx skills@latest add howells/skills --skill '*' --agent codex --global` - install all globally for Codex.
- This repo currently has no package-level test or build script; verify by reading and targeted search.

## Repo-Specific Rules
- Use Arc for development planning if a skill change spans multiple skills or install behavior.
- Use Mastra only in skills that explicitly audit or build Mastra systems; this repo is not a Mastra runtime.
- Keep README summaries synchronized with individual `SKILL.md` descriptions.
