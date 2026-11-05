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

Design and build polished web UI in Tailwind v4, rescue a screen that looks messy, generic or unfinished, or critique one without changing it. Use when an interface should look gorgeous or someone asks what feels off. Not for design options (`maquette`), app shells (`armature`), screen sizes (`reflow`), Paper mockups (`paste-up`) or QA (`fieldtest`).

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

Control Mac apps, including signed-in Chrome, through native Codex Computer Use from Codex or Claude Code. Not for browser-only QA (`fieldtest`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill computer-use --agent codex --global
```

### `deslop`

Rewrite prose that reads as machine-written or inflated: vague attribution, staged contrasts, crutch phrases, fake citations, chatbot artefacts. Use for drafts, docs, posts and PR text. Not for interface strings (`signage`) or code (`unslop`).

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

QA a running web app in a real browser and report evidence-backed findings. Use for dogfooding, localhost review, console and accessibility checks, persona walkthroughs, or trying to break it. Reports unless asked to fix. Not for building UI (`chiaroscuro`) or fixing layout (`reflow`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill fieldtest --agent codex --global
```

### `gog`

Work in Gmail, Calendar, Drive, Docs and Sheets through the authenticated gog CLI instead of Google connectors. Not for web research (`web-research`).

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

Explore design options for a page, component or region as live variants in the running app, switch or compare them, then keep one and delete the rest. Use when asked for options, alternatives or directions. Not for one settled direction (`chiaroscuro`) or Paper (`paste-up`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill maquette --agent codex --global
```

### `marginalia`

Add short JSDoc where IDE hovers or generated API docs need a contract the types don't show. Use for JS/TS exports, components, hooks, generics, tricky internals and packages about to publish. Not for deleting restating comments (`unslop`), README or guide prose, or behaviour changes.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill marginalia --agent codex --global
```

### `mastraudit`

Prevent recurring Mastra failures in agents, tools, workflows, storage, Studio and MCP Apps. Use when writing, debugging or auditing Mastra code. Not for general UI review (`fieldtest`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill mastraudit --agent codex --global
```

### `memento`

Say where this task stands from live state: the ask, done, left, branch, uncommitted files and any drift. Use on returning to a long session. Not for many sessions (`muster`) or the last reply (`what`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill memento --agent codex --global
```

### `muster`

Catch up on work across concurrent or older sessions: what's in flight, who owns it, what was decided, and a handoff when asked. Not for this task's status (`memento`), the last reply (`what`) or git conflicts and cleanup (`salvage`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill muster --agent codex --global
```


### `nomen`

Generate, critique and check names for products, packages, CLIs, apps or features, with domain, registry, GitHub, App Store and web conflict checks. Use when naming or renaming something. Not for interface labels (`signage`) or legal clearance.

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill nomen --agent codex --global
```

### `paste-up`

Build a mockup in Paper (app.paper.design) from a spec, or audit and repair a Paper file: tokens, fonts, artboards, crops, labels. Not for coded UI (`chiaroscuro`) or browser QA (`fieldtest`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill paste-up --agent codex --global
```

### `plimsoll`

Cut checks, CI watch loops and re-planning that crowd out shipping, and keep Vercel builds on the user's machine. Use near a deadline or when nothing visible has landed. Not for codebase review (`simplify`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill plimsoll --agent codex --global
```

### `product-description`

Document a product's user-visible behaviour feature by feature from code, tests and the running product, then triage suspected defects. Not for marketing copy, READMEs, single-feature specs or browser QA alone (`fieldtest`).

Imported from [Steve Ruiz's original `product-description` gist](https://gist.github.com/steveruizok/83ae5c53f2784ebf8f5fe0a3fb94480f).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill product-description --agent codex --global
```

### `rebalance`

Reprioritize a project's backlog around a goal or deadline, and flag goal work too thin to build. Not for doing the work (`implement`).

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

Resolve git conflicts when a merge, rebase, cherry-pick, revert or stash apply or pop reports CONFLICT or leaves conflict markers, including mid-task. Rescue stranded work in detached HEADs, worktrees, unpushed branches and stashes; remove only copies proven merged and pushed. Not for status recovery (`muster`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill salvage --agent codex --global
```

### `signage`

Rewrite interface strings into the words the audience already uses: labels, buttons, headings, errors, empty states, generated text, film and deck captions. Use when UI copy reads as jargon or machine-made. Not for body prose (`deslop`), product names (`nomen`) or visual styling (`chiaroscuro`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill signage --agent codex --global
```

### `simplify`

Strict structural review of a diff or whole codebase: finds restructurings that delete complexity, and real security, performance or data risks. Reports findings; edits only when asked. Not for diff tidy-ups (`unslop`), fallback removal (`failfast`) or browser QA (`fieldtest`).

```bash
npx skills@latest add howells/skills --skill simplify --agent codex --global
```

Use `simplify` for selected changes or `simplify whole codebase` for the repository; add `in <path>` to narrow either scope. Add `with scores` only when you want a scorecard. Both scopes report findings; add `apply the fixes` or `create Linear items` to request action.

Claude Code's bundled `/simplify` edits a diff for reuse and efficiency; this one reports structural findings and edits only when asked. In Claude Code, this personal skill takes precedence over the bundled skill with the same name.

### `typecase`

Replace a UI codebase's scattered font utilities with a few named type roles and a scanner that holds them, and choose the faces. Use when text sizes have multiplied or a type ramp needs designing. Not for visual direction (`chiaroscuro`) or wording (`signage`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill typecase --agent codex --global
```

### `unslop`

Strip machine-written tells from a diff without changing behaviour: narrating comments, one-caller wrappers, impossible guards, unused options, decorative logs, leftover scaffolding. Not for structural review (`simplify`), behaviour-changing fallback removal (`failfast`) or prose (`deslop`).

Install globally for Codex:

```bash
npx skills@latest add howells/skills --skill unslop --agent codex --global
```

### `what`

Re-explain only the previous reply in three plain lines: what happened, where things stand, what's next. No new facts. Not task status (`memento`) or session recovery (`muster`).

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
