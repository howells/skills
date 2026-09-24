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

### Claude Code plugin

This repo is also a Claude Code plugin marketplace. Add it, then install every skill as one plugin:

```bash
claude plugin marketplace add howells/skills
```

```bash
claude plugin install howells-skills@howells
```

The marketplace also carries the `fiction` plugin. Don't install the plugin alongside a `skills.sh` install of the same skills, or each skill loads twice.

## Skills

The integration skills (`gog`, `linear`, `starling`, `xero` and `web-research`) use tools, accounts and credentials configured by the installing user. They include no account inventory or private repository dependency. Installing a skill does not provision access. The other skills may require their named applications or CLIs, as documented inside each skill.

### `armature`

Turn a web app that scrolls like a document into an app shell with fixed chrome and panes that scroll on their own. Not for visual polish (`chiaroscuro`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill armature --agent codex --global
```

### `ask-howells`

Route a situation to the skills in this collection and the command to type. Not for doing the work.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill ask-howells --agent codex --global
```

### `blender`

Inspect, measure and render Blender scenes through MCP or headless CLI. Use for Blender scene, render-pipeline or MCP work. Not for 2D design files (`paste-up`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill blender --agent codex --global
```

### `chiaroscuro`

Design and build polished web UI in Tailwind v4. Not for page directions (`maquette`), app shells (`armature`), screen sizes (`reflow`) or QA (`fieldtest`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill chiaroscuro --agent codex --global
```

### `componentize`

Consolidate shared UI, split multi-responsibility files or extract packages. Not for redesign (`chiaroscuro`), typography (`typecase`) or behaviour-preserving cleanup (`unslop`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill componentize --agent codex --global
```

### `deslop`

Rewrite prose that sounds synthetic, inflated, or assistant-like. Use for AI-writing tells, vague attribution, suspicious citations, chatbot artifacts. Applies to prose; for interface labels use `signage`; for machine-written code tells use `unslop`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill deslop --agent codex --global
```

### `fail-fast`

Remove hidden fallbacks, swallowed errors, legacy aliases and permissive defaults. Not for behaviour-preserving cleanup (`unslop`) or required compatibility.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill fail-fast --agent codex --global
```

### `fable-review`

Get an independent review from Claude Fable 5.1, then verify its claims before acting. Use for a hard judgement call: a design or architecture decision, a taste question, a plan worth arguing with. Not for a cheap conformance check (`glm-review`), a codebase grade (`simplify`), or a routine diff.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill fable-review --agent codex --global
```

### `fieldtest`

Exercise a running web app in a real browser and return evidence-backed QA findings. Use for dogfooding, localhost review, responsive or mobile defects, console and accessibility checks, and persona walkthroughs; fix only when asked. Not for code-only review, or designing and building the UI (`chiaroscuro`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill fieldtest --agent codex --global
```

### `foreman`

Run an explicitly requested delegation mode for substantial changes: the main agent decides and inspects while subagents write code. Use only when the user asks for Foreman or delegated execution. Not for ordinary implementation, tiny fixes, or docs-only work; `plimsoll` governs process weight.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill foreman --agent codex --global
```

### `gog`

Use gogcli for configured Google accounts instead of Google connectors. Not for web research (`web-research`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill gog --agent codex --global
```

### `glm-review`

Get an independent read-only review from GLM 5.3 Flash via OpenCode, then verify its claims before acting. Use when the user names GLM, or for a cheap bounded check: conformance to stated criteria, a contract, UI copy. Not for a hard judgement call (`fable-review`) or a codebase grade (`simplify`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill glm-review --agent codex --global
```

### `linear`

Use configured Linear accounts via GraphQL; choose the account that owns the target. Not for transcripts (`muster`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill linear --agent codex --global
```

### `maquette`

Render five page directions beside the current page, then build the chosen one. Not for a single direction (`chiaroscuro`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill maquette --agent codex --global
```

### `marginalia`

Add concise, useful JSDoc where IDE hover help or a generated API reference needs a non-obvious contract. Use for exported JavaScript or TypeScript APIs, components, hooks, classes, complex types, or package publishing. Not for internal code, narrating comments, prose docs or behaviour changes.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill marginalia --agent codex --global
```

### `mastraudit`

Run before writing Mastra code and before calling it done. Pre-flight: local docs, installed version, small payloads, constituent tools. Then audit execution failures first: step size, fan-out keying, suspend and resume payloads, load-bearing writes, model settings, tool keys.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill mastraudit --agent codex --global
```

### `memento`

Report what this task is doing now from live state: original ask, completed work, remaining work, branch, uncommitted files, and drift. Use when returning to a long session. For a roll-call across tasks use `muster`; for rewriting only the last reply use `what`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill memento --agent codex --global
```

### `muster`

Rebuild context across concurrent or older tasks from transcripts, git, peer sessions and the tracker. Use for catch-ups and in-flight inventories. Not for one current task (`memento`), rewriting the last reply (`what`), or repository cleanup (`salvage`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill muster --agent codex --global
```

### `next`

Claim and deliver the next item with Plimsoll; name the thread for it. Not audits (`simplify`) or recovery (`muster`).

Invoke `next` using the harness's skill invocation syntax in a fresh project task (`$next` in Codex). It skips started items, immediately claims the selected item as In Progress with session ownership, names the current thread for it where supported, checks that the work is still needed, uses parallel agents with a suitable mix of available models, implements and verifies it, then pushes a reviewable PR. It follows configured auto-merge through completion; otherwise it leaves the PR open and waits for review. It adapts to Codex, Claude Code, OpenCode, Cursor and other compatible harnesses; Sol, Terra and Luna are preferences where available.

Previously named `next-issue`; remove that installed copy when installing `next`.

Before editing, it checks the live tracker status and independently verifies whether the work is already delivered. An open but completed item gets evidence and the appropriate status correction; partially delivered work is limited to the remaining acceptance criteria.

Every selected item is introduced with a clickable ticket identifier and one short sentence explaining the outcome in everyday words, before implementation or a status correction.

Selecting a parent includes every child and nested descendant, regardless of priority. It verifies already completed children, delivers the remaining work, and keeps the parent incomplete while any required child lacks acceptance evidence. Selecting a child does not include its siblings.

It works to the selected item's spec, records necessary clarifications there, and files unrelated findings as separate, deduplicated tracker items with acceptance criteria and an evidence-based priority. Those follow-ups stay outside the current implementation. Genuine blockers are documented and resolved in the same task before returning to the original item; the stopping boundary is the selected outcome, including its necessary prerequisites.

After confirmed merge and required delivery checks, it removes its own safely merged branches and unused, clean worktree. It preserves active work, unique artifacts and anything with uncertain ownership, and reports any cleanup still pending.

### `nomen`

Generate, critique, and validate names for products, packages, CLIs, apps or features, with domain, package, GitHub, App Store and web conflict checks. Use for naming and renaming decisions. Not for interface labels (`signage`), body prose (`deslop`), or legal clearance.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill nomen --agent codex --global
```

### `paste-up`

Build a Paper mockup from a spec, or audit and repair a Paper file: tokens, fonts, artboards, crops, labels. Only for app.paper.design. Not for coded UI (`chiaroscuro`) or browser QA (`fieldtest`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill paste-up --agent codex --global
```

### `plimsoll`

Cut process weight when gate ladders, CI/build watch loops, remote Vercel builds or re-planning displace shipping. Keeps Vercel builds on the user's machine. Use near a deadline or after nothing user-visible has landed. Not `simplify`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill plimsoll --agent codex --global
```

### `product-description`

Document user-visible product behaviour from code, tests and the running product, then consolidate defects into triage. Not for marketing copy, READMEs, single-feature specs, or browser QA alone (`fieldtest`).

Imported from [Steve Ruiz's original `product-description` gist](https://gist.github.com/steveruizok/83ae5c53f2784ebf8f5fe0a3fb94480f).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill product-description --agent codex --global
```

### `rebalance`

Reprioritize a project's backlog for a goal. Not implementation (`next`).

Give it a project, a concrete goal and an optional deadline. It checks the whole open backlog, reconciles evidenced stale statuses, makes essential unfinished work urgent, and prepares dependencies for `next`. The new priorities stand; there is no saved priority snapshot or restoration mechanism. It uses relevant `ask-matt` flows when available and stops before implementation. If no related tickets exist or the tickets are too thin to implement, it explains the gap and invites `grilling`, `to-spec` or `to-tickets` as appropriate.

```bash
npx skills@latest add howells/skills --skill rebalance --agent codex --global
```

### `reflow`

Make every view of a web app work on small laptops, tablets and phones, checked in a browser. Not for QA reports (`fieldtest`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill reflow --agent codex --global
```

### `salvage`

Rescue work that exists in only one place - detached HEADs, worktrees, unpushed branches, or stashes - then remove only what is proven merged and pushed. Use for repository cleanup that must preserve ambiguous work. For status reconstruction without cleanup use `muster`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill salvage --agent codex --global
```

### `signage`

Rewrite interface strings into the words the audience already uses: labels, headings, buttons, status lines, empty states and generated text. Not for body prose (`deslop`), product names (`nomen`), layout or visual styling (`chiaroscuro`), or the type ramp (`typecase`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill signage --agent codex --global
```

### `simplify`

Review a diff or whole codebase for structural simplification and relevant health risks, with source-confirmed findings and optional scores. Not routine cleanup (`unslop`) or browser QA (`fieldtest`).

Combines Cursor's strict structural review with stage-aware risk assessment, source vetting, grouped fixes and honest coverage. Reviews relevant security, performance and reliability concerns alongside opportunities to remove complexity. Cursor's upstream rubric and MIT attribution are preserved.

```bash
npx skills@latest add howells/skills --skill simplify --agent codex --global
```

Use `simplify` for selected changes or `simplify whole codebase` for the repository; add `in <path>` to narrow either scope. Add `with scores` only when you want a scorecard. Both scopes report findings; add `apply the fixes` or `create Linear items` to request action.

In Claude Code, this personal skill takes precedence over the bundled skill with the same name.

### `starling`

Query configured Starling Bank balances and transactions. Not for Xero (`xero`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill starling --agent codex --global
```

### `typecase`

Design and enforce named typography roles across a UI codebase. Use when raw font utilities have multiplied or a type ramp needs consolidating. Not for visual direction (`chiaroscuro`), interface wording (`signage`), or one-off type polish.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill typecase --agent codex --global
```

### `unslop`

Remove machine-written code tells from a diff without changing behavior: narrating comments, one-caller wrappers, impossible guards, unused options, decorative logs, and leftover scaffolding. For behavior-changing fallback cleanup use `fail-fast`; for prose use `deslop`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill unslop --agent codex --global
```

### `what`

Re-explain only the previous reply in three plain lines: what happened, current state, next step. No new facts. Not task status (`memento`) or session recovery (`muster`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill what --agent codex --global
```

### `web-research`

Research the open web with Exa and Tavily and synthesize one cited answer. Not for browser QA (`fieldtest`) or scraping (`firecrawl-*`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill web-research --agent codex --global
```

### `xero`

Query Xero accounting data through a configured integration. Not for Starling (`starling`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill xero --agent codex --global
```

## Removed

`npx skills` copies files and does not track deletions, so a skill removed here stays on disk wherever it was installed. Uninstall the stale copy by hand: `rm -rf ~/.agents/skills/<name> ~/.claude/skills/<name> ~/.codex/skills/<name>`.

Removed on 2026-09-02. Not one had been invoked, in either Claude Code or Codex, in the whole time since it was added:

| Skill | Added | Where its work went |
| --- | --- | --- |
| `aperture` | 2026-05-21 | `componentize`, as the standalone-package scope |
| `heathen` | 2026-05-21 | `componentize`, as the god-file scope, with its scanner |
| `fenceline` | 2026-05-21 | Nothing; import-boundary work has no host |
| `foundry` | 2026-05-21 | Nothing; its shared references live on in `chiaroscuro` |
| `polyplugin` | 2026-05-22 | Nothing |
| `inquest` | 2026-08-20 | Nothing; `muster` covers rebuilding context |

Merged on 2026-09-06:

| Skill | Where its work went |
| --- | --- |
| `survey` | `simplify`, for diff or whole-codebase reviews with optional scoring. Update Simplify, then run `npx skills@latest remove survey --global --yes`. Also remove project-local copies where present. |

Moved on 2026-09-24:

| Skill | New home |
| --- | --- |
| `howells-lint` | The `howells/lint` repo, versioned with the preset it sets up. Install with `npx skills@latest add howells/lint --skill howells-lint --global`, then remove the old copy as above. |
