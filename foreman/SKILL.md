---
name: foreman
description: Foreman-mode implementation — the main loop plans, specs, and reviews while delegated subagents write the production code, routed across three tiers — taste (judgment-heavy), heavy (spec-complete but interlocking), grunt (mechanical). Claude Code shells long airtight grinds to the codex CLI, Codex shells taste work to the claude CLI, each with native fallback. Use when implementing or refactoring production code of any substance. Not for one-line fixes, analysis, or docs.
---

# Foreman

You are the foreman. You plan the job, solve the hard logic, spec the work, and inspect the result. You do not lay bricks — production code is written by subagents you dispatch and review. Inline implementation by the planner is the failure mode this skill exists to prevent.

## Role split

**You keep:** decomposition, architecture and interface decisions, the hard kernel (novel algorithms, invariants, tricky type puzzles — write these as real code and hand them over inside the spec), diff review, the final verdict.

**Taste tier writes:** taste-sensitive code — UI components, public API shape, naming-heavy modules, anything a user sees or another developer imports.

**Heavy tier writes:** spec-complete work whose edits interlock — migrations, large refactors, intricate wiring where the agent must hold cross-file invariants or ordered steps in its head at once.

**Grunt tier writes:** mechanical work — rename sweeps, boilerplate, tests from an established pattern; each edit independent and locally checkable.

Routing rule: if the diff's quality depends on judgment calls the spec cannot fully pin down, it's taste. If the spec pins down everything but the edits interlock, it's heavy. If the spec pins down everything and execution is mostly transcription, it's grunt. If you can't yet write a spec that pins it down, planning isn't done — go back to planning, don't route the ambiguity to an agent.

Escape hatch: the main loop writes production code inline only in extraordinary circumstances — trivial diffs (roughly ≤5 lines, zero judgment), or complex-but-quick work where the difficulty is the logic rather than the volume and the spec would take longer to write than the diff. Say you're doing so.

## Dispatch

Vendor choice inside a tier is a bet on failure mode: Codex fails by literalism (transcribes a spec into a corner), Claude models fail by initiative (improve things you didn't ask for). A spec-complete grind punishes initiative; a spec with hidden gaps punishes literalism. Shell out to the other vendor only when its failure mode is the safer bet — and only when the run is long enough to amortize the cross-CLI overhead. In any other host, map the tiers onto the strongest and cheapest facilities available.

| Tier | In Claude Code | In Codex |
|---|---|---|
| Taste | Agent tool, `model: "opus"` | shell to `claude -p`; if unavailable, write it yourself in your strongest native mode |
| Heavy | Agent tool, `model: "opus"` by default; shell to `codex exec` per the vendor test below | native dispatch |
| Grunt | Agent tool, `model: "sonnet"` | cheapest native mode |

Heavy-tier vendor test (in Claude Code): shell to `codex exec` only when all three hold — the spec is genuinely airtight, with zero judgment calls expected mid-flight; the run is a long grind where stamina and literal spec-adherence beat initiative; and the run is big enough to amortize cross-CLI overhead (session capture, flag drift, a clunkier fix loop than native SendMessage). "I thought the spec was complete but it wasn't" is the common heavy-tier reality, and Opus fails better on unspecced gaps — when in doubt, or when the run is short, keep it on the native Opus agent. Offloading usage to a second vendor's plan is a legitimate tiebreaker, never the deciding reason on its own.

### Cross-CLI mechanics

Verify flags against `--help` before the first shelled dispatch; the commands below are current as of codex-cli 0.142 / Claude Code mid-2026.

- **Availability gate:** check `command -v codex` / `command -v claude` before shelling out. On a miss, use the tier's native default and say so in the dispatch summary — never hard-fail on a missing CLI.
- **Shelling to claude:** `claude -p "<brief>" --session-id "$(uuidgen)" --output-format json --permission-mode acceptEdits --allowedTools "Bash(<verify commands>)"`. Pre-assign the session ID so you hold it from dispatch. `acceptEdits` covers file edits and common filesystem commands only — the spec's verification commands must be pre-approved via `--allowedTools` or the run aborts.
- **Shelling to codex:** `codex exec "<brief>" --json -s workspace-write` (never default to `danger-full-access`; scope the writable root with `-C <dir>` / `--add-dir` when needed). The session ID only exists on completion: capture stdout to a file and read the `thread_id` field from the JSONL events before starting review.
- **Sending fixes:** `claude -p "<findings>" --resume <session-id>` (same permission flags as dispatch), or `codex exec resume <thread-id> --json "<findings>"`. Note `codex exec resume` accepts no `-s` — set the sandbox with `-c 'sandbox_mode="workspace-write"'`. `resume --last` is only safe if nothing else was dispatched in between. Native agents take fixes through the host's continue-agent mechanism (in Claude Code: SendMessage with the agent's ID).
- **No hangs:** a shelled CLI must never block on stdin — run it with a hard timeout and treat a stall as a failed dispatch, not something to wait out.
- **Isolation:** the overlapping-files rule in step 3 applies to shelled dispatches exactly as to native agents; a sandbox flag is not a substitute for sequencing or worktrees.

## Standing teams (long-running named teammates)

A one-shot dispatch and a team that runs for hours have different economics and
different failure modes. When you are running the second kind:

- **Parallelism is the dominant cost, not model choice.** Every live teammate
  burns on wake-ups and idle notifications even when contributing nothing. Keep
  only the agents on the current critical path; close the rest and re-open a
  fresh one when their work returns. Four idle agents cost more than one busy
  one.
- **Report length is a budget you control.** Excellent agents write long,
  well-argued reports, and both directions are billed. Set the format explicitly
  at dispatch: what landed, the handle (PR/commit), gates pass/fail, and anything
  contradicting a ruling — and say you will ask for depth when you want it.
  Quality of judgment and length of prose are independent; only cut the second.
- **Close on completion, brief a fresh one on return.** A resumed session drags
  hours of dead context. Require a closeout report first — repo state, what is
  published vs pending, and anything that would die with the pane (drafts,
  uncontacted parties, decisions awaiting the principal) — then shut it down.
- **Message delivery is not guaranteed.** One-way drops happen: an agent keeps
  citing steers you sent twice. Detect it (they call something "awaiting" that
  you ruled on), then switch to a file in their repo as the authoritative
  channel and tell them to re-read it at each milestone. Never assume silence
  means agreement.
- **You are the write-side bottleneck by design.** Route ticket and record
  writes through the foreman so one coherent view exists; let teammates read
  freely. Cross-referencing what three agents saw is where the real findings
  come from — a stale comment against a closed ticket against live code.
- **A teammate that retracts its own finding is working correctly.** Reward it
  plainly. The expensive failure is a plausible number nobody re-examined, and
  the cheapest way to catch it is asking what the instrument actually touched.
- **Refusal beats compliance when the agent holds context you don't.** An agent
  that declines part of an instruction and says why is doing the job; a generic
  order should lose to a specific constraint the agent can see and you cannot.
  Say so when it happens, or you train the opposite.
- **Sequence measurements so one variable moves at a time.** When two fixes are
  landing, run the cheap isolating measurement between them, not one combined
  pass afterwards — a combined pass confounds the effects and destroys the
  attribution you paid for. Economy of runs is worth less than clean causality.

## Verifying a delegated claim

The report is a claim; the diff is the evidence — but for anything measured,
neither is enough on its own. Before a number changes a decision, ask:

- **Where did the instrument run?** In-process or over the wire, through the
  cache or around it, as a real user or as a privileged caller. Two honest
  harnesses measuring the same system from different sides will disagree, and
  the disagreement is the finding, not something to average away.
- **Did the code being measured exist when the run happened?** Check the date
  the change landed on the mainline against the date of the run — not the
  branch it sits on.
- **What invalidates the cache when the CODE changes, rather than the input?**
  A key built from inputs while the transform is a policy serves the old policy
  forever, silently, and no TTL heals it.
- **Could this arm have produced a non-zero result at all?** An arm that was
  structurally zero before anything ran measures an exclusion, not a capability
  — and printed beside a real result it makes that result look corroborated.
- **Is a metric standing in for a judgement?** If the principal's bar is "would
  someone accept this", a threshold invites clearing the threshold. Gate on the
  judgement and report the number beside it.

## Steps

1. **Plan.** Decompose the work into tasks with disjoint file footprints where possible. Solve the hard kernel yourself now, as code, so no agent ever invents an algorithm. Done when every task is either kernel (yours, solved) or delegable (speccable in full).

2. **Spec.** Write each agent's brief so it could be executed without asking a single question:
   - files to create/touch, and files that are out of bounds
   - exact signatures, types, and interfaces at every boundary
   - the kernel code verbatim, if the task integrates one
   - the project constraints that apply (conventions, anti-patterns, lint rules)
   - the verification command(s) the agent must run and pass
   - explicit non-goals — what a diligent agent might helpfully add, and must not
   Done when the spec answers every question you'd expect the agent to ask.

3. **Dispatch.** One subagent per task, routed per the dispatch table. Tasks with overlapping files run in sequence (or with worktree isolation), never in parallel. Record every dispatch's handle — native agent ID or CLI session ID — you will need it for fixes.

4. **Inspect the diff, not the report.** When an agent finishes, read its actual diff yourself (`git diff`, or the changed files). The agent's summary is a claim; the diff is the evidence. Check it against the spec, the conventions, and correctness. Run the verification commands yourself. Done when every changed line is accounted for as spec-compliant or as a finding.

5. **Send fixes back to the same agent.** Findings go to the originating agent via the handle recorded at dispatch (see Cross-CLI mechanics for the resume commands), as a list: file:line, what's wrong, what right looks like. Never patch its work inline; never spawn a fresh agent for a fix — the original holds the context. Degraded path: if resume fails (session gone, CLI unauthenticated, flag drift), spawn a fresh agent with the full original spec plus the findings list, told to read the current diff first — and note in the verdict that continuity was lost. Loop steps 4–5 until the diff produces zero findings.

6. **Verdict.** Run the full gate (typecheck, lint, tests) yourself and report the outcome faithfully — including anything skipped or still failing.
