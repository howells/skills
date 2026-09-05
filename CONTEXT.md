# Howells Skills

The independent collection of `skills.sh`-compatible agent skills. This glossary fixes the words the collection uses about itself, about what its skills return, and about the things they judge - so that twenty-two skills written at different times still speak one language.

A term earns an entry here when it appears in two or more skills, or when someone who has not read the skill would misread it. Terms internal to a single skill are defined in that skill's own `SKILL.md`.

## Language

### The collection

**Skill**:
A directory here holding a `SKILL.md` and, optionally, its own `references/`, `scripts/` and `agents/openai.yaml`. The unqualified word always means the thing you edit in this repo.
_Avoid_: skill source, skill package, command

**Installed copy**:
The materialised copy of a skill under `~/.agents/skills/<name>`, symlinked into each host. It does not auto-update when the repo changes.
_Avoid_: installed skill, deployed skill

**Invocation**:
An agent running a skill, in a host, against a repo. Distinct from the skill itself.
_Avoid_: run, call, execution

### Describing a skill

**Description**:
The frontmatter field on a `SKILL.md`, kept under about 400 characters and within the collection's 7,000-character budget, that Claude and Codex read to decide whether to route to this skill.
_Avoid_: summary, blurb

**Trigger clause**:
The routing-bearing phrase inside a description - the part naming the situation the skill is for. Two skills sharing one verbatim is a routing collision, and the consistency gate errors on it.
_Avoid_: trigger phrase, routing text

**Sync surface**:
One of the three places a skill's description lives: the `SKILL.md` frontmatter, the skill's `README.md` section, and `agents/openai.yaml`. All three must agree.
_Avoid_: install surface, metadata surface

**Cross-pointer**:
A line in one skill naming another skill's territory, so a reader lands in the right place. Terse by design.
_Avoid_: see-also, reference, link

### Reference files

**Reference file**:
A `.md` file under a skill's own `references/`, loaded at the step that needs it rather than up front.
_Avoid_: bare "reference", doc, supporting file

**Deliberate copy**:
The same reference file present in two skills on purpose, because a skill installs alone and cannot reach a sibling. Distinct from drift, which is two copies that were meant to agree and no longer do.
_Avoid_: duplicate, fork, generated copy

### What a skill returns

The first four are a ladder. Each rung is a claim about how much confirmation something has had, and moving up a rung takes work.

**Signal**:
Something a scanner, manifest or search emitted. Machine-produced and unread.
_Avoid_: hit, result, output

**Lead**:
A signal someone thinks means something, not yet confirmed against the source. Presenting a lead as settled is the most common way a skill is confidently wrong.
_Avoid_: candidate, suspicion, potential finding

**Finding**:
A claim confirmed at its source, carrying a severity and a citation. Only a confirmed lead is a finding.
_Avoid_: issue, problem, result

**Evidence**:
The excerpt, screenshot, log line or citation that makes a finding checkable by someone who was not there.
_Avoid_: proof, backup, receipt

**Verdict**:
The single judgement a skill returns, distinct from the findings underneath it.
_Avoid_: conclusion, result, summary

**Report**:
The message a skill returns in the conversation, to its stated output contract. Reporting is the act of returning that message, not of writing a document.
_Avoid_: writeup, summary document

**Tracker item**:
The durable record of work, in Linear. Anything that needs to outlive the conversation goes here rather than into repo markdown.
_Avoid_: ticket file, issue doc

**Artefact**:
A file a skill produces because someone asked for one. The exception, never the default.
_Avoid_: report file, output file

### Planning and delegating work

**Spec**:
A tracker item stating the problem, the solution, user stories and the decisions taken. It names no file paths, because those go stale faster than the spec does.
_Avoid_: plan, PRD, requirements doc

**Brief**:
What a foreman sends a subagent: a spec-complete instruction naming files, interfaces and the report format. If it names files, it is a brief, not a spec.
_Avoid_: task spec, delegate spec, prompt

**Tier**:
Which class of subagent a task is routed to - taste for judgement-heavy work, heavy for interlocking work a brief can pin down, grunt for mechanical work.
_Avoid_: level, class, model tier

### Judging a codebase

**Stage**:
Where a project is in its life: prototype, development, pre-launch or production. It sets what counts as severe. A deliberate transitional state during a move is a *staged migration*, not a stage.
_Avoid_: phase, maturity, lifecycle stage

**Severity**:
How much a finding costs, judged against the project's stage rather than in the abstract. The same code earns different severities at prototype and in production.
_Avoid_: priority, importance

**Lens**:
One reviewer's angle on a codebase - security, performance, architecture - defined inline and dispatched with the context it needs.
_Avoid_: reviewer, agent, pass

**Cluster**:
A group of findings you would fix in one sitting, grouped by area, kind of work or dependency order. Never grouped by which lens found them.
_Avoid_: category, bucket, group

**God file**:
A file carrying so many responsibilities that changing one means reading all of them. Authored source over 1000 lines, or anything over 2000.
_Avoid_: monolith, large file, big module

**Boundary**:
A line across which imports are constrained - between packages, between apps, or between source layers.
_Avoid_: barrier, wall, interface

**Scanner**:
A deterministic shipped check that returns the same answer every run. Run the scanners before writing a regex; a hand-rolled search that disagrees with one is wrong until proven otherwise.
_Avoid_: linter, checker, tool

**Manifest**:
A stored list of signals collected in one pass, carried forward as context. A plugin's own metadata file is a *plugin manifest*, which is a different thing.
_Avoid_: bare "manifest" for plugin metadata, inventory, index

**Tell**:
A detail that reveals text or code as machine-written - a comment narrating the line below, a negative parallelism, a one-caller wrapper.
_Avoid_: smell, artifact, marker

### Design work

**Design spec**:
The written visual direction for a screen or system: tokens, type scale, spacing, states.
_Avoid_: bare "spec" for visual work, style guide

**Direction**:
A distinct visual approach, produced to be compared against others rather than accepted alone.
_Avoid_: option, concept, mockup

**Token**:
A named design value in a Tailwind v4 `@theme` block - a colour, a size, a radius. Not a unit of model input.
_Avoid_: variable, custom property

**Primitive**:
A low-level building block in a design system: a button, an input, a stack. Not a base capability and not an underlying skill.
_Avoid_: component, base component, atom

**UI surface**:
A visible plane in an interface that content sits on - a card, a panel, a sheet, the page ground itself. The design skills own this sense, and inside them the bare word is understood.
_Avoid_: container, background, layer

**Persona**:
An invented user with a specific goal and constraint, used to walk an interface and surface what a feature list would miss.
_Avoid_: user type, profile, archetype

### Working across sessions

**Thread**:
One line of work in flight, with its own branch, scope and next move. A repo can have several at once, held by different sessions.
_Avoid_: task, workstream, stream

**Transcript**:
The stored record of a past session, read to rebuild context rather than to replay it.
_Avoid_: history, log, conversation

**Coverage map**:
A statement of which evidence sources were searched, which came back empty and which were skipped. An empty search and a skipped source are different results and are reported differently.
_Avoid_: test coverage, sources list

### Words used everywhere

**Surface**:
A place where something is exposed to a consumer. Never used bare - always qualified, as in sync surface, public surface, host surface, sensitive surface, agent surface, UI surface.
_Avoid_: bare "surface", interface, boundary

**Drift**:
Two things that should agree no longer agreeing. Qualify it to say which two: surface drift, copy drift, doc drift, contract drift.
_Avoid_: divergence, rot, staleness

**Gate**:
A check that decides whether you proceed. Qualify it: the consistency gate is `check-skills.py`, a security gate decides whether a lens runs, a CI gate is lint and typecheck.
_Avoid_: check, blocker, precondition
