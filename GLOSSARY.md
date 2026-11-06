# Howells Skills

The collection of `skills.sh`-compatible agent skills in this repo. This glossary fixes the words the collection uses about itself; `scripts/check-vocabulary.py` enforces several of them.

## Language

**Skill**:
A directory holding a `SKILL.md` and, optionally, its own `references/`, `scripts/` and `agents/openai.yaml`. The unqualified word means the thing edited in this repo.
_Avoid_: skill package, command

**Sync surface**:
One of the three places a skill's description lives: the `SKILL.md` frontmatter, the skill's README section, and `agents/openai.yaml`. All three must agree.
_Avoid_: install surface, metadata surface

**Surface**:
Never used bare. Always qualified: sync surface, public surface, host surface, sensitive surface, agent surface, UI surface.
_Avoid_: bare "surface"

**Trigger clause**:
The phrase inside a description that names the situation the skill is for. Two skills sharing a long verbatim clause is a routing collision.
_Avoid_: trigger phrase

**Cross-pointer**:
A terse line in one skill naming another skill's territory.
_Avoid_: see-also

**Reference file**:
A `.md` file under a skill's own `references/`, loaded at the step that needs it.
_Avoid_: bare "reference", supporting file

**Deliberate copy**:
The same reference file present in two skills on purpose, because a skill installs alone and cannot reach a sibling.
_Avoid_: duplicate, fork

**Report**:
The message a skill returns in the conversation. Not a file.
_Avoid_: report file, writeup

**Artefact**:
A file a skill produces because someone asked for one. The exception, never the default.
_Avoid_: report file, output file

**Tracker item**:
The durable record of work, in Linear.
_Avoid_: ticket file, issue doc

**Brief**:
What a delegating agent sends a subagent: it names files or scope, constraints and the report format.
_Avoid_: task spec, delegate spec

**Stage**:
Where a project is in its life: prototype, development, pre-launch or production. A transitional state during a move is a *staged migration*, not a stage.
_Avoid_: phase, maturity
