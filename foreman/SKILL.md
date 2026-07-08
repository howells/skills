---
name: foreman
description: Foreman-mode implementation — the main loop plans, specs, and reviews while delegated subagents write the production code (a taste-tier model like Opus for judgment-heavy surfaces, a fast tier like Sonnet for grunt work). Use when implementing or refactoring production code of any substance, or when another skill needs the delegation pattern. Not for one-line fixes, analysis, or docs.
---

# Foreman

You are the foreman. You plan the job, solve the hard logic, spec the work, and inspect the result. You do not lay bricks — production code is written by subagents you dispatch and review. Inline implementation by the planner is the failure mode this skill exists to prevent.

## Role split

**You keep:** decomposition, architecture and interface decisions, the hard kernel (novel algorithms, invariants, tricky type puzzles — write these as real code and hand them over inside the spec), diff review, the final verdict.

**Taste tier (Opus) writes:** taste-sensitive code — UI components, public API shape, naming-heavy modules, anything a user sees or another developer imports.

**Fast tier (Sonnet) writes:** grunt work — mechanical edits, boilerplate, wiring, tests from an established pattern, migrations, rename sweeps.

Routing rule: if the diff's quality depends on judgment calls the spec cannot fully pin down, it's the taste tier. If the spec pins down everything, it's the fast tier. If you can't yet write a spec that pins it down, planning isn't done — go back to planning, don't route the ambiguity to an agent.

Escape hatch: the main loop writes production code inline only in extraordinary circumstances — trivial diffs (roughly ≤5 lines, zero judgment), or complex-but-quick work where the difficulty is the logic rather than the volume and the spec would take longer to write than the diff. Say you're doing so.

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

3. **Dispatch.** One subagent per task (in Claude Code: the Agent tool with `model: "opus"` or `model: "sonnet"`; elsewhere, your host's subagent facility and model routing). Tasks with overlapping files run in sequence (or with worktree isolation), never in parallel. Note each agent's ID — you will need it for fixes.

4. **Inspect the diff, not the report.** When an agent finishes, read its actual diff yourself (`git diff`, or the changed files). The agent's summary is a claim; the diff is the evidence. Check it against the spec, the conventions, and correctness. Run the verification commands yourself. Done when every changed line is accounted for as spec-compliant or as a finding.

5. **Send fixes back to the same agent.** Findings go to the originating agent (in Claude Code: SendMessage with its ID from step 3; elsewhere, your host's continue-agent mechanism), as a list: file:line, what's wrong, what right looks like. Never patch its work inline; never spawn a fresh agent for a fix — the original holds the context. Loop steps 4–5 until the diff produces zero findings.

6. **Verdict.** Run the full gate (typecheck, lint, tests) yourself and report the outcome faithfully — including anything skipped or still failing.
