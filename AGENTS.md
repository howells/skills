# Howells Skills

A collection of `skills.sh`-compatible agent skills. Each skill lives in its own directory with a `SKILL.md`; supporting assets and scripts stay local to that skill. `README.md` is the public catalogue and install guide, and the list of skills lives there.

`CONTEXT.md` is the glossary. `docs/adr/` holds the decisions.

## Read before editing a skill

- `docs/descriptions.md` - the three surfaces a description must agree across, the per-skill and collection character budgets and why they exist, what belongs in portable frontmatter against host-specific installer metadata, and the rule against naming a model in a payload.
- `docs/skill-files.md` - why every referenced file sits inside its own skill directory, the deliberate copies, keeping a payload portable, and what removing a skill does not do.

## Commands

There is no build. Two Python gates are the repository-wide checks.

- `python3 scripts/check-skills.py` - the consistency gate. Run it before committing any skill change. It checks the three sync surfaces, invocation-policy parity, host UI metadata bounds, portable names, intra-skill `.md` links, per-skill and collection description budgets, trigger-clause overlap, `agents/openai.yaml` section structure, and pointers to removed skills.
- `python3 scripts/check-vocabulary.py` - flags prose that contradicts `CONTEXT.md`. Several governed words are also ordinary verbs, so the rules match the noun uses and exempt the verb ones. A flagged line that is genuinely right is fixed by adding it to `ALLOW` with a reason, never by loosening the rule.
- `python3 scripts/test-skill-helpers.py` for scanner or API-helper changes. Its temporary fixtures exercise coverage, typography evidence and GraphQL outcomes without external accounts.
- `npx skills@latest add howells/skills --list` lists installable skills.

Otherwise verify by reading and targeted search.
