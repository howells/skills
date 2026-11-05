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

The integration skills (`gog` and `web-research`) use tools, accounts and credentials configured by the installing user. They include no account inventory or private repository dependency. Installing a skill does not provision access. The other skills may require their named applications or CLIs, as documented inside each skill.

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

Design and build polished web UI in Tailwind v4, rescue a screen that looks messy, generic or unfinished, or critique one without changing it. Use when an interface should look gorgeous or someone asks what feels off. Not for page directions (`maquette`), app shells (`armature`), screen sizes (`reflow`), Paper mockups (`paste-up`) or QA (`fieldtest`).

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

### `computer-use`

Operate macOS apps through native Codex Computer Use, including signed-in Chrome and API-backed setups. Not for browser-only QA (`fieldtest`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill computer-use --agent codex --global
```

### `deslop`

Rewrite prose that sounds synthetic, inflated, or assistant-like. Use for AI-writing tells, vague attribution, suspicious citations, chatbot artefacts. Applies to prose; for interface labels use `signage`; for machine-written code tells use `unslop`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill deslop --agent codex --global
```

### `failfast`

Remove fallbacks and swallowed errors that hide failures, and test-only code or mocks in production. Use when removing hidden defaults or legacy aliases, tests assert on mocks, or a test needs production hooks. Not for ordinary test-writing or test-first workflow (`tdd`), behaviour-preserving cleanup (`unslop`), or required compatibility.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill failfast --agent codex --global
```

### `fieldtest`

Exercise a running web app in a real browser and return evidence-backed QA findings. Use for dogfooding, localhost review, mobile defects, console and accessibility checks, persona walkthroughs, or to try to break it with hostile content, slow networks and rapid input. Report-only unless asked. Not for code-only review, building UI (`chiaroscuro`) or fixing layout (`reflow`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill fieldtest --agent codex --global
```

### `gog`

Use gogcli for configured Google accounts instead of Google connectors. Not for web research (`web-research`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill gog --agent codex --global
```

### `handfeel`

Make a web app feel native on a phone. Use when it works on desktop but feels wrong on a phone, or for PWA behavior, notch or home-indicator overlap, iOS input zoom, sticky hover, tap feedback, overscroll or the color behind Safari's bars. Not for responsive layout (`reflow`), app shells (`armature`) or motion (`zoetrope`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill handfeel --agent codex --global
```

### `maquette`

Render five page directions beside the current page, then build the chosen one. Not for a single direction (`chiaroscuro`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill maquette --agent codex --global
```

### `marginalia`

Add concise, useful JSDoc where IDE hover help or a generated API reference needs a non-obvious contract. Use for JavaScript or TypeScript APIs, components, hooks, classes, complex types, complex internal code, or package publishing. Not for obvious comments, prose docs or behaviour changes.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill marginalia --agent codex --global
```

### `mastraudit`

Prevent recurring Mastra failures while building agents, tools, workflows and MCP Apps. Use before changes, during debugging and for focused acceptance. Not for general UI review (`fieldtest`).

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

Recover project purpose, decisions and in-flight work across concurrent or older sessions; check transcripts, git, peers and the tracker for catch-ups or handoffs. Not for one current task (`memento`), rewriting the last reply (`what`), or repository cleanup (`salvage`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill muster --agent codex --global
```


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

Reprioritize a project's backlog for a goal. Not implementation (`implement`).

Give it a project, a concrete goal and an optional deadline. It checks the whole open backlog, reconciles evidenced stale statuses, makes essential unfinished work urgent, and prepares dependencies for delivery. The new priorities stand; there is no saved priority snapshot or restoration mechanism. It uses relevant `ask-matt` flows when available and stops before implementation. If no related tickets exist or the tickets are too thin to implement, it explains the gap and invites `grilling`, `to-spec` or `to-tickets` as appropriate.

```bash
npx skills@latest add howells/skills --skill rebalance --agent codex --global
```

### `reflow`

Make every view of a web app work on small laptops, tablets and phones, checked in a browser. Not for phone-browser behavior (`handfeel`) or QA reports (`fieldtest`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill reflow --agent codex --global
```

### `review`

Verify review feedback before acting on it. Use when PR bot comments arrive, reviewer findings are pasted, or an independent opinion is wanted from fable, sol, muse (wonder), opus or astra. Not for reviewing a diff, branch or PR from scratch (`code-review`), codebase health (`simplify`) or browser QA (`fieldtest`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill review --agent codex --global
```

Feedback that arrives from a bot, PR or agent loads it implicitly. To ask for an independent opinion, name the model or let the skill choose one: `$review fable <question>`, `$review sol <question>`, `$review muse <question>` (or `wonder`), `$review opus <question>`, or `$review astra <question>`. In Claude Code use `/review` with the same arguments.

### `salvage`

Rescue work that exists in only one place - detached HEADs, worktrees, unpushed branches, or stashes - then remove only what is proven merged and pushed. Use for repository cleanup that must preserve ambiguous work. For status reconstruction without cleanup use `muster`.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill salvage --agent codex --global
```

### `signage`

Rewrite interface strings into the words the audience already uses: labels, headings, buttons, status lines, empty states, generated text, and the captions in films and decks. Not for body prose (`deslop`), product names (`nomen`), layout or visual styling (`chiaroscuro`), or the type ramp (`typecase`).

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

### `typecase`

Design and enforce named typography roles across a UI codebase. Use when raw font utilities have multiplied or a type ramp needs consolidating. Not for visual direction (`chiaroscuro`), interface wording (`signage`), or one-off type polish.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill typecase --agent codex --global
```

### `unslop`

Remove machine-written code tells from a diff without changing behavior: narrating comments, one-caller wrappers, impossible guards, unused options, decorative logs, and leftover scaffolding. For behavior-changing fallback cleanup use `failfast`; for prose use `deslop`.

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

### `zoetrope`

Build, review or find web animation, and diagnose dropped frames: purpose, timing, springs, gestures, interruption and reduced motion. Not for static visual polish (`chiaroscuro`) or browser QA (`fieldtest`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill zoetrope --agent codex --global
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

Removed on 2026-10-08:

| Skill | Where its work went |
| --- | --- |
| `foreman` | Nothing. It existed to keep the expensive model planning while cheaper subagents wrote the code; that cost pressure has gone. `plimsoll` still governs process weight. |

Moved or removed on 2026-09-24:

| Skill | New home |
| --- | --- |
| `howells-lint` | The `howells/lint` repo, versioned with the preset it sets up. Install with `npx skills@latest add howells/lint --skill howells-lint --global`, then remove the old copy as above. |
| `linear` | The `howells/linearcli` repo, beside the CLI it now prefers for everyday issue work. Install with `npx skills@latest add howells/linearcli --skill linear --global`. |
| `starling` | The `howells/starlingcli` repo, rewritten to drive `starlingcli`. Install with `npx skills@latest add howells/starlingcli --skill starling --global`. |
| `xero` | Removed. It named no real tool; recreate it beside a Xero CLI if one is built. |

Consolidated on 2026-10-13:

| Skill | Where its work went |
| --- | --- |
| `astra-review` | `review astra`; the unified skill also accepts `sol`. |
| `fable-review` | `review fable`; the unified skill also accepts `opus` and `muse` (`wonder`). |
| `glm-review` | Removed; GLM is no longer a review lane. |

Install `review`, then remove the three stale copies from local and global install locations as described above.
