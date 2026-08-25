---
name: survey
description: "Grade an entire codebase with a stage-calibrated verdict, clustered findings, and comparable scores. Use for repository health audits where mechanical checks, source-confirmed findings, lifecycle stage, and multiple review lenses matter. For a diff or PR use code review; for Mastra use `mastraudit`."
---

# Survey

A building survey grades what is in front of it against what it is meant to be. Nobody condemns a house for having no kitchen when the walls are still going up. That is the whole idea here: **detect the stage before you judge the code.**

An audit that skips this produces the same report for a weekend prototype and a system serving real users, and the prototype's report is worthless. It is a wall of production-hardening findings - no rate limiting, no monitoring, no tests - every one of them technically true and none of them worth reading. The signal drowns. Worse, it teaches the reader that audits are noise.

So the order is: **stage, then mechanics, then judgement, then vetting.** Each phase earns the right to the next.

## What this is not

Survey grades a codebase. It does not fix one, and it deliberately stops short of the specialists:

- **A diff, PR or branch** is `/code-review`. Survey judges the repo, not the change.
- **God files and oversized modules** get reported here as a signal, then routed to `heathen` to actually decompose.
- **Fallbacks, swallowed errors and env defaults** get reported as determinism smells, then routed to `fail-fast`.
- **Package and import boundaries** route to `fenceline`; **duplicated UI** routes to `componentize`.
- **Mastra execution semantics** are `mastraudit`'s. When Mastra is detected, defer that lens to it rather than re-deriving it badly.
- **Rendered behaviour in a browser** is `fieldtest`. Survey reads code.
- **Implementing the fixes** is `foreman`, taking the clusters as briefs.

Survey produces the backlog. It never writes the code.

## The reference set

Load each at the phase that needs it, not up front:

- [Stage](references/stage.md) - the detection signals, the four calibration blocks that get pasted verbatim into every lens prompt, the severity validation table, and the advisory tone rules. Phases 1 and 4.
- [Lenses](references/lenses.md) - what each review lens looks for, what it receives, and what it returns. Phase 3.
- [Scorecard](references/scorecard.md) - the seven axes, their criteria tables, the mechanical caps, and the interpretation bands. Phases 3 and 5.

## Steps

Copy these into your todolist verbatim before you start. A step you skip stays in the list with a one-line `skip: <reason>`.

### 1. Scope and stage

Load `references/stage.md`.

Establish scope from the argument if one was given - a path, or a plain-language focus like "security" or "architecture". A focus narrows which lenses run; it does not change the process. If no scope was given, detect structure: `apps/*` and `packages/*` means a monorepo, `src/*` means standard, neither means the current directory.

Detect project type, scale and **lifecycle stage** using the signal tables in the reference file. Then apply the **security readiness gate**, which decides whether a deep security lens runs at all.

**Confirm the stage with the user before going further.** Stage drives every severity rating in the run, so an unconfirmed stage means an unreliable verdict. If they correct it, their answer wins. If no answer is available, proceed with the detected stage and mark it unconfirmed in the output.

Produces a detection summary:

```
Scope:         [path or "full codebase"]
Type:          [Next.js / React / Python / Rust / Go / mixed]
Scale:         [small / medium / large] ([N] source files)
Stage:         [prototype / development / pre-launch / production] ([signals]) [confirmed / UNCONFIRMED]
Security gate: [deep lens / lightweight] ([reason])
Database:      [yes/no]   Tests: [yes/no]   CI: [yes/no]
Focus:         [all, or the user's focus]
```

### 2. Mechanical pass

Cheap checks before expensive judgement. Anything a machine can settle should not cost a lens.

Detect tooling from the repo itself - package manager from lockfiles, build and test scripts from `package.json`, typechecker from `tsconfig.json`, linter from its config. Then run, in this order:

1. **Build.** If it fails, stop and report that. Nothing downstream is trustworthy on a broken build.
2. **Typecheck.** Report errors, continue.
3. **Lint.** Report; do not auto-fix during a survey - you are measuring, not changing.
4. **Tests**, where test tooling exists.
5. **Secrets scan**, using a scanner the repo has or a careful grep.
6. **Per-workspace pipeline coverage.** Lint and typecheck must be configured in *every* app and package, not only at the root. A monorepo whose root has the scripts while `apps/*` and `packages/*` do not has workspaces shipping unchecked. Then confirm the scripts actually run in CI - one that exists but is never executed is a soft gap.

Run scanners the project already has wired, including any house packages. Offer an unwired third-party scanner with one question and skip it without comment if declined - `npx`-ing someone else's code into a user's repo is never a silent decision.

Produces a mechanical summary and a set of signal manifests. **Manifests are leads, not findings.** A lens still opens the file before reporting anything.

### 3. Lens review

Load `references/lenses.md` and `references/scorecard.md`.

Select lenses from scale, type and the security gate - the reference has the selection table. Dispatch them as parallel read-only subagents where the harness supports it, sequentially inline where it does not. Each lens receives:

- the stage calibration block, pasted verbatim from `references/stage.md`
- the mechanical summary and its slice of the signal manifests
- the repo's own conventions, where they exist - `CLAUDE.md`, `AGENTS.md`, contributing docs, architecture notes. **Project rules outrank generic best practice.** A lens flagging something the repo explicitly allows is wrong.
- the criteria table for the one axis it scores

Each lens returns findings as `file:line`, a one-sentence statement of what it costs, a fix, and an `Excerpt:` line carrying the exact source it saw. The excerpt is not decoration - phase 4 cannot work without it.

Produces raw findings plus one axis score per lens.

### 4. Vet and calibrate

This is the phase that separates a survey from a wall of text. **Lenses over-report. An unvetted citation is a lead, not a fact.**

Re-open the cited `file:line` for every Critical and High finding and compare it against the finding's excerpt. The question is "is what the lens saw still there, and does it mean what the lens said" - never re-derive intent from a bare line number.

Hunt three failure classes explicitly, because they will be there:

1. **By-design.** Platform conventions and tradeoffs recorded in an ADR or an architecture doc are settled decisions, not findings. Flag them only where the implementation adds risk beyond the convention. One exception cuts the other way - **code that has drifted from what its decision doc says is itself a finding.** Don't let a stale doc suppress the drift it failed to describe.
2. **Mis-attributed.** The problem is real, the citation is wrong. Re-locate it and correct the citation, or dismiss it - a finding nobody can locate cannot be fixed.
3. **Duplicate.** Already tracked in the tracker, or already considered and rejected. Drop it and say so. Merging two lenses that flagged the same line in this run is ordinary dedup and happens here too.

Then downgrade against the severity validation table for the detected stage, annotating each change: `[adjusted for <stage> - would be <original> in production]`.

Record every dismissal with a one-line reason. **"Not worth doing" is a verdict, not a failure** - writing it down stops the same finding being re-litigated on every future run.

Produces vetted findings, a dismissed list, and an explicit statement of the vet scope.

### 5. Cluster and score

**Cluster by what you would fix in one sitting, never by which lens found it.** Three findings in `src/auth/` from three different lenses are one job. Group by area of code, then by kind of work where the same change repeats across files, then by dependency where one fix unblocks another. Aim for three to eight clusters; merge the smallest if there are more, and don't invent grouping if there are fewer.

Derive the scorecard using `references/scorecard.md` - take each lens's axis score, use the **lower** where two lenses share an axis, apply the mechanical caps, and mark any axis nobody reviewed as `--` with the denominator adjusted rather than guessing it.

**The score is absolute; the stage lives in the interpretation.** A prototype at 10/21 is healthy. A production system at 10/21 needs attention. Never bend the number to flatter the stage.

### 6. Report and route

Report to the output contract below.

Where a tracker is connected, write each cluster as an item there - that is the durable record, and it is what makes the next survey's score comparable to this one. **Do not write a report file into the repo** unless the user asks for one; scattered markdown reports are how drift starts.

Then route each cluster to whatever actually fixes it, using the boundaries at the top of this file.

## Output contract

One screen. The verdict first.

```
Survey: X/21 - [band]
Scope: [scope]  Stage: [stage] [confirmed / UNCONFIRMED]

Sec [n] | Perf [n] | Arch [n] | Qual [n] | Test [n] | Resil [n] | Ops [n]
[+n/3 accessibility, when it ran]

[One line per axis that scored 0 or 1, saying why.]

Clusters, worst first:
1. [name] - [n] findings ([n] critical, [n] high) -> [where it routes]
2. ...

Vetted: [n] of [n] re-read at the cited line. [What was not vetted.]
Dismissed: [n] ([reasons in brief])
Not checked: [anything skipped, and why]
```

Rules for that block:

- **Say what you did not check.** A short survey honestly scoped beats a long one implying coverage it never had.
- **Say which findings were vetted.** A reader must never assume "vetted" applies uniformly when it does not. Critical and High are re-read; Medium and Low are unverified citations unless you say otherwise.
- **Advisory by default.** "Must fix" is for credential exposure, injection and data loss. "Should consider" is for real problems. "Worth noting" is for suggestions. Most findings are the last two.
- **An axis with no reviewer is `--`, not a guess.** Adjust the denominator and say why.

## Failure modes

- **Judging a prototype as production software.** The single most common way a survey becomes noise. Detect the stage, confirm it, and paste the calibration block into every lens prompt.
- **Presenting lens output as fact.** Lenses over-report and mis-cite. Anything you have not re-read at the cited line is a lead, and must be labelled as one.
- **Clustering by reviewer domain.** "Security findings, performance findings, architecture findings" is the report structure nobody can act on. Cluster by the sitting that fixes them.
- **Scoring an axis nobody reviewed.** Absence of review is not evidence of health. Mark it `--`.
- **Letting a skipped security lens lower the score.** The gate skipping it is a deliberate stage-appropriate decision, not a finding about the code.
- **Fixing things.** Survey reports and routes. The moment it starts editing, it has stopped measuring and become an unreviewed refactor.
- **Writing a report file nobody asked for.** The tracker is the record.
