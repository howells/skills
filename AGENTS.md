# Howells Skills

The independent collection of `skills.sh`-compatible agent skills. Each skill lives in its own directory with a `SKILL.md`; supporting assets and scripts stay local to that skill. `README.md` is the public catalogue and install guide.

## The skills

- `chiaroscuro` - end-to-end UI design, implementation, responsive and accessible behavior, browser verification, and polish.
- `componentize` - consolidate duplicated UI, god files and code that should be a package.
- `deslop` - audit and rewrite prose carrying AI-writing tells.
- `fail-fast` - remove fallbacks, silent compatibility paths, legacy aliases and default env values.
- `fable-review` - request an independent Claude Fable 5.1 read on a hard judgement call, then verify it.
- `fieldtest` - browser QA of a rendered app with evidence-backed findings.
- `foreman` - foreman-mode implementation: the main loop plans and reviews, subagents write the code.
- `glm-review` - request a read-only GLM 5.3 Flash review on the Z.AI Coding Plan, then verify its findings.
- `linear` - select the right one of Daniel's two Linear accounts and use its GraphQL API directly.
- `marginalia` - JSDoc for public APIs and exported symbols.
- `mastraudit` - audit a Mastra codebase against what actually breaks it, execution semantics before structure.
- `memento` - report what you are working on right now, from current state, in one screen.
- `muster` - roll-call of work in flight: transcripts, live git state, peer sessions, tracker.
- `nomen` - generate and validate names, with availability and conflict checks.
- `paste-up` - design in Paper: build a file from a spec, or audit and repair an existing one from its URL.
- `plimsoll` - cut process weight when gates, polling and re-planning have displaced shipping.
- `product-description` - document a product's user-visible behaviour outside-in, then verify and triage it.
- `salvage` - rescue work that exists in only one place, then clear away branches, worktrees and stashes that are provably redundant.
- `signage` - replace invented interface vocabulary with the words the audience already uses.
- `starling` - query every configured Starling Bank account through the agent-first CLI and synced 1Password credentials.
- `survey` - grade a whole codebase and return a stage-calibrated verdict with a comparable score, clustered by what you would fix in one sitting.
- `typecase` - constrain text styling to a few named type roles and enforce it with a scanner.
- `unslop` - strip machine-written tells out of a diff without changing behaviour.
- `what` - cut the last message down to what happened, short and in plain language.
- `web-research` - combine Exa and Tavily discovery and extraction into one source-grounded synthesis.
- `xero` - query Xero through the existing offledger CLI and synced 1Password credentials.

## Three sync surfaces

Every skill's description exists in three places and they must agree: the `SKILL.md` frontmatter `description`, the skill's section in `README.md`, and `agents/openai.yaml` (installer metadata: `display_name`, `short_description`, `default_prompt`, whose `default_prompt` references `$<skill-name>`). Change one, change all three, then run the checker.

Keep each frontmatter `description` within about 400 characters and the collection total under the 7,000 the consistency gate enforces. Codex gives the initial skill list at most 2% of the context window or 8,000 characters, shortening descriptions first when it runs out; Claude truncates crowded listings. The gate's 7,000 leaves headroom under the documented cap. Front-load the use case and use terse cross-skill pointers to disambiguate overlapping scope.

Keep shared discovery in portable `SKILL.md` frontmatter: `name` and `description`. A description states when the skill should fire *and when it should not* - every one carries a `Not for …` clause naming the skill that owns the adjacent territory. Codex-only metadata belongs in `agents/openai.yaml`, under `interface` (UI), `policy` (invocation) or `dependencies` (required MCP servers, declared as `tools` entries with `type`, `value`, `description`, `transport` and `url`); the consistency gate checks each field sits in its own section. If a skill becomes explicit-only, pair Claude's `disable-model-invocation: true` with Codex's `policy.allow_implicit_invocation: false`; otherwise omit both and keep implicit discovery enabled. Current sources: [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) and [Claude Code Skills](https://code.claude.com/docs/en/skills).

## Reference files live in the skill that uses them

`npx skills` installs one skill at a time, so an installed skill has to stand alone:
every file it references sits inside its own directory. A reference needed by two
skills is copied into both, and the duplication is deliberate.

There is no shared source layer. One existed while five design references served two
skills; the second was removed on 2026-09-02, leaving `chiaroscuro` as the only
consumer, so the sources were folded into it. See `docs/adr/0004`.

If a second skill ever needs one of those files again, copy it and note both copies
here. Reintroduce a source layer only when the copies are numerous enough that keeping
them in step by hand is the thing going wrong.

## Editing skills

- Keep each `SKILL.md` self-contained enough for a fresh agent to use, with no hidden dependency on a local file that the body doesn't link.
- Don't broaden a skill unless its trigger and output stay clear, and keep repo-specific product assumptions out of reusable skills.
- Search related skills before broadening scope. The overlap hotspots are chiaroscuro/componentize/typecase (UI design, componentization and decomposition, the type ramp); also check fieldtest and mastraudit. what/memento/muster overlap on reporting state - what decodes the last message and actions, memento is this session's task now, muster sweeps many sessions.
- Search the target skill directory before editing shared README text.
- Verify current `skills` CLI examples before changing installer docs.
- Don't copy these skills into product repos; install or invoke them from the agent environment.
- Removing or renaming a skill doesn't update existing installs - `npx skills` copies files and doesn't track deletions. When a skill is deleted or merged, note it in the README and manually uninstall the stale copy from local and global install locations.

## Commands

- `python3 scripts/check-skills.py` - the consistency gate. Run before committing any skill change: it checks the three sync surfaces, Claude/Codex invocation-policy parity, Codex UI metadata bounds, portable names, intra-skill `.md` links, per-skill and collection description budgets, trigger-clause overlap, `agents/openai.yaml` section structure, and pointers to removed skills. Exits non-zero on errors.
- `python3 scripts/check-vocabulary.py` - the vocabulary gate. Flags prose that contradicts `CONTEXT.md`: a bare "surface", a bare "reference", foreman's "spec" where it means a brief, "stage" used for a staged migration, a report written as a file. Several governed words are also ordinary verbs, so the rules match the noun uses and exempt the verb ones - "surface the conflict" is correct and stays. A flagged line that is genuinely right is fixed by adding it to `ALLOW` with a reason, not by loosening the rule. Exits non-zero on violations.
- `npx skills@latest add howells/skills --list` - list installable skills.
- `npx skills@latest add howells/skills --skill '*' --agent codex --global` - install all globally for Codex.

There is no build. The two Python gates above are the repository-wide checks; otherwise verify by reading and targeted search.

## Agent skills

### Issue tracker

Linear, team `SKI` (Skills). Linear is the record, not markdown in this repo. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical roles, unrenamed, live on `SKI` alongside its `Bug`/`Improvement`/`Feature` labels. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context - one `CONTEXT.md` glossary and `docs/adr/` at the root. See `docs/agents/domain.md`.
