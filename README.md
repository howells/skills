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

## Skills

### `chiaroscuro`

Design polished responsive web UI with Tailwind v4. Not for browser QA (`fieldtest`), reuse (`componentize`), copy (`signage`) or typography (`typecase`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill chiaroscuro --agent codex --global
```

### `componentize`

Consolidate code around a clear ownership boundary: deduplicate shared UI, split a confirmed multi-responsibility file, or extract a coherent package. Use when the outcome asked for is reuse, decomposition or a package boundary. Not for visual redesign (`chiaroscuro`), typography rules (`typecase`), or behaviour-preserving cleanup (`unslop`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill componentize --agent codex --global
```

### `deslop`

Rewrite prose that sounds synthetic, inflated, or assistant-like. Use for AI-writing tells, vague attribution, suspicious citations, chatbot artifacts, or copy that should sound grounded and human. Applies to prose; for interface labels use `signage`; for machine-written code tells use `unslop`.

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

Get an independent review from Claude Fable 5.1 through the Claude CLI, then verify its claims before acting. Use for a hard judgement call: a design or architecture decision, a taste question, a plan worth arguing with. Not for a cheap conformance check (`glm-review`), a codebase grade (`survey`), or a routine diff.

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

Run an explicitly requested delegation mode for substantial changes: the main agent decides and inspects while subagents write code. Use only when the user asks for Foreman or delegated execution. Delegation never requires new tests. Not for ordinary implementation, tiny fixes, or docs-only work; `plimsoll` governs process weight.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill foreman --agent codex --global
```

### `gog`

Use gogcli for Daniel's Google accounts instead of Google connectors. Not for public web research (`web-research`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill gog --agent codex --global
```

### `glm-review`

Get an independent read-only review from GLM 5.3 Flash on the Z.AI Coding Plan via OpenCode, then verify its claims before acting. Use when the user names GLM, or for a cheap bounded check: conformance to stated criteria, a contract, UI copy. Not for a hard judgement call (`fable-review`) or a codebase grade (`survey`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill glm-review --agent codex --global
```

### `linear`

Use either Linear account when MCP has the wrong one. Not for transcripts (`muster`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill linear --agent codex --global
```

### `marginalia`

Add concise, useful JSDoc where IDE hover help or a generated API reference needs a non-obvious contract. Use for exported JavaScript or TypeScript APIs, components, hooks, classes, complex types, or package publishing. Not for self-explanatory internal code, narrating comments, prose docs, or anything that changes behavior.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill marginalia --agent codex --global
```

### `mastraudit`

Audit a Mastra codebase against execution failures first: workflow step size, fan-out keying, suspend and resume payloads, load-bearing writes, model settings, and visible tool keys. Use for pre-ship review or an existing Mastra implementation. For building Mastra features use `$mastra`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill mastraudit --agent codex --global
```

### `memento`

Report what this task is doing now from live state: original ask, completed work, remaining work, branch, uncommitted files, and drift. Use when returning to a long session or checking whether an agent is still on track. For a roll-call across tasks use `muster`; for rewriting only the last reply use `what`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill memento --agent codex --global
```

### `muster`

Rebuild working context across concurrent or older agent tasks from transcripts, git state, peer sessions, and the tracker. Use for 'catch me up', 'where did I leave off', or 'what is in flight', returning every active thread and its next move. Not for one current task (`memento`), rewriting the last reply (`what`), or repository cleanup (`salvage`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill muster --agent codex --global
```

### `nomen`

Generate, critique, and validate names for products, projects, packages, CLIs, apps, brands, or features, with domain, package, GitHub, App Store and web conflict checks. Use for naming and renaming decisions. Not for interface labels (`signage`), body prose (`deslop`), or legal clearance.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill nomen --agent codex --global
```

### `paste-up`

Build a Paper mockup from a written specification, or audit and repair an existing Paper file: tokens, fonts, artboard layout, crops, labels. Use only for work in app.paper.design. Not for coded UI implementation (`chiaroscuro`), browser QA (`fieldtest`), or design critique with no Paper file involved.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill paste-up --agent codex --global
```

### `plimsoll`

Cut process weight when gate ladders, build-watch loops and re-planning have displaced shipping. Use near a deadline, or after a stretch with nothing user-visible. Aims verification at what ships, not the workspace. Not `survey`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill plimsoll --agent codex --global
```

### `product-description`

Document a product outside-in as user-visible behavior drafted from code and tests, verified in the running product, and consolidated into bug triage. Use for complete experience documentation across web, mobile, canvas, CLI, chat, or agent products. Not for marketing copy, a README, a single-feature spec, or browser QA alone (`fieldtest`).

Imported from [Steve Ruiz's original `product-description` gist](https://gist.github.com/steveruizok/83ae5c53f2784ebf8f5fe0a3fb94480f).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill product-description --agent codex --global
```

### `salvage`

Rescue work that exists in only one place - detached HEADs, worktrees, unpushed branches, or stashes - then remove only what is proven merged and pushed. Use for repository cleanup where ambiguous work must be preserved and each surviving thread named. For status reconstruction without cleanup use `muster`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill salvage --agent codex --global
```

### `signage`

Rewrite interface strings into the words the audience already uses: labels, headings, buttons, status lines, empty states and generated text. Use when reviewing UI copy for comprehension. Not for body prose (`deslop`), product names (`nomen`), layout or visual styling (`chiaroscuro`), or the type ramp (`typecase`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill signage --agent codex --global
```

### `starling`

Query Starling. Not for Xero (`xero`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill starling --agent codex --global
```

### `survey`

Grade an entire codebase with a stage-calibrated verdict, clustered findings, and comparable scores. Use for repository health audits where mechanical checks, source-confirmed findings, lifecycle stage, and multiple review lenses matter. For a diff or PR use code review; for Mastra use `mastraudit`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill survey --agent codex --global
```

### `typecase`

Design, migrate and enforce a small set of named type roles across a UI codebase, with a census and a scanner. Use when raw size, weight, tracking, leading, family or case utilities have multiplied, or a type ramp needs designing or collapsing. Not for general visual direction (`chiaroscuro`), interface wording (`signage`), or one-off typography polish.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill typecase --agent codex --global
```

### `unslop`

Remove machine-written code tells from a diff without changing behavior: narrating comments, one-caller wrappers, impossible guards, unused options, decorative logs, and leftover scaffolding. Use before commit or review. For behavior-changing fallback cleanup use `fail-fast`; for prose use `deslop`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill unslop --agent codex --global
```

### `what`

Rewrite only the previous agent reply into three short, plain-language lines: what happened, where things stand, and what comes next. Use when the last message was dense, jargon-heavy, or unclear. It re-explains existing content and gathers no new facts. Not for whole-task status (`memento`) or cross-session context (`muster`).

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

Query Xero. Not for Starling (`starling`).

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
