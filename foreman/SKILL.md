---
name: foreman
description: Foreman-mode implementation — the main loop plans, specs, and reviews while delegated subagents write the production code, routed across three tiers — taste (judgment-heavy), heavy (spec-complete but interlocking), and grunt (mechanical). Cross-CLI delegation — Claude Code shells heavy work to the codex CLI; Codex shells taste work to the claude CLI, each with native fallback. Use when implementing or refactoring production code of any substance. Not for one-line fixes, analysis, or docs.
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

Each host shells out only where the other vendor beats its native option — Claude models for judgment and taste, Codex for long, exacting, spec-following execution. In any other host, map the tiers onto the strongest and cheapest facilities available.

| Tier | In Claude Code | In Codex |
|---|---|---|
| Taste | Agent tool, `model: "opus"` | shell to `claude -p`; if unavailable, write it yourself in your strongest native mode |
| Heavy | shell to `codex exec`; if unavailable, a native fast-tier agent | native dispatch |
| Grunt | Agent tool, `model: "sonnet"` | cheapest native mode |

### Cross-CLI mechanics

Verify flags against `--help` before the first shelled dispatch; the commands below are current as of codex-cli 0.142 / Claude Code mid-2026.

- **Availability gate:** check `command -v codex` / `command -v claude` before shelling out. On a miss, use the fallback column above and say so in the dispatch summary — never hard-fail on a missing CLI.
- **Shelling to claude:** `claude -p "<brief>" --session-id "$(uuidgen)" --output-format json --permission-mode acceptEdits --allowedTools "Bash(<verify commands>)"`. Pre-assign the session ID so you hold it from dispatch. `acceptEdits` covers file edits and common filesystem commands only — the spec's verification commands must be pre-approved via `--allowedTools` or the run aborts.
- **Shelling to codex:** `codex exec "<brief>" --json -s workspace-write` (never default to `danger-full-access`; scope the writable root with `-C <dir>` / `--add-dir` when needed). The session ID only exists on completion: capture stdout to a file and read the `thread_id` field from the JSONL events before starting review.
- **Sending fixes:** `claude -p "<findings>" --resume <session-id>` (same permission flags as dispatch), or `codex exec resume <thread-id> --json "<findings>"`. Note `codex exec resume` accepts no `-s` — set the sandbox with `-c 'sandbox_mode="workspace-write"'`. `resume --last` is only safe if nothing else was dispatched in between. Native agents take fixes through the host's continue-agent mechanism (in Claude Code: SendMessage with the agent's ID).
- **No hangs:** a shelled CLI must never block on stdin — run it with a hard timeout and treat a stall as a failed dispatch, not something to wait out.
- **Isolation:** the overlapping-files rule in step 3 applies to shelled dispatches exactly as to native agents; a sandbox flag is not a substitute for sequencing or worktrees.

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
