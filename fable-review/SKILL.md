---
name: fable-review
description: "Get an independent review from Claude Fable 5.1 through the Claude CLI, then verify its claims before acting. Use for a hard judgement call: a design or architecture decision, a taste question, a plan worth arguing with. Not for a cheap conformance check (`glm-review`), a codebase grade (`survey`), or a routine diff."
---

# Fable review

Fable is the expensive lane, for the calls that are genuinely hard: which of two architectures survives contact, whether a plan's premise holds, whether an interface reads the way its author thinks it does. Use it sparingly and on questions where a second opinion changes what you do next.

What comes back is a set of leads. Verify each one before acting on it.

`glm-review` is the other lane, and the two are chosen by the kind of question rather than by importance. A bounded conformance check - does this match the stated criteria, does this contract hold, is this copy right - goes to GLM and costs almost nothing. A judgement call with no checkable answer goes here.

## One route, three hosts

The Claude CLI is the route, and it works the same from Claude Code, Codex and OpenCode, because all three can run a shell command.

```bash
printf '%s' "$PROMPT" | claude -p \
  --model fable \
  --effort high \
  --permission-mode plan \
  --disallowedTools "Edit,Write,NotebookEdit"
```

**Pass the prompt on stdin.** `--disallowedTools` is variadic and will otherwise swallow a positional prompt as tool names, which fails with `Permission deny rule "…" matches no known tool` and never reaches the model.

Run it from the repository under review; the CLI reads files relative to the working directory. Add `--add-dir` for a path outside it.

Confirm the lane before the first invocation in a session:

```bash
printf 'Reply with exactly: lane-ok' | claude -p --model fable --permission-mode plan --output-format json
```

Require a successful JSON response whose `result` is `lane-ok`. Inspect returned model metadata when available and stop if it identifies a different model; the text alone proves responsiveness, not exact model identity. If the CLI omits model metadata, report identity as unverified rather than asserting the exact version.

Without `lane-ok`, stop and name the cause: `claude` missing from the path, credentials absent or expired, or the alias no longer resolving to Fable. Substituting Opus, Sonnet or a different provider's model is a failed run, because the point of the lane is which model answered.

**Do not substitute the Claude Code subagent.** In Claude Code a fable subagent is reachable through the Agent tool, and it inherits this session's context and instructions. That makes it useful for delegated work and useless as an independent read, since it has already been told what you think. The subprocess starts clean, which is the whole value.

Plan mode and denied edit tools reduce write access, but a successful refusal probe is not proof that every write route is blocked. Keep the written read-only boundary in the brief. When source reading is sufficient, restrict built-in tools to `Read,Glob,Grep`; otherwise remember that shell access can still mutate state and use the host's execution controls.

`--effort high` is the default for this skill. Raise it to `xhigh` or `max` for a question where the reasoning is the deliverable.

## Build a bounded brief

Investigate first, so Fable spends its turn on the judgement rather than on rediscovering the repository. A brief carries:

- the question, stated as a decision someone has to make;
- the artifact: paths, excerpts, diff or base commit, current status;
- the options already on the table, and what each would cost;
- constraints, settled decisions, and explicit non-goals;
- validation already run, and what remains uncertain;
- the boundary, verbatim: `Read-only review. Do not edit files or run state-changing commands.`

Ask for a verdict, the reasoning that leads to it, where it disagrees with the proposed direction, and what it would need to change its mind.

A brief that names no decision gets an essay. "Review this architecture" fails that bar; "we chose X over Y for reason Z - what does that cost us in eighteen months" does not.

## Wait for it

A single-file judgement call returns in under a minute at high effort. A brief spanning several files and a real decision takes longer.

Give the run ten minutes. A review still silent past that is a hang: kill it, say so, and stop. Output that arrives empty or cut off mid-argument is a failed run, reported as one rather than salvaged into a partial verdict.

Retry once on a transport or internal-server failure. Report an authentication, quota, or billing rejection and stop without retrying, because those repeat.

## Verify, then report

Check every material claim against the source, the diff, the tests, or the running product. A claim you could not confirm stays labelled unconfirmed. Fable argues well, and a well-argued wrong claim is the failure mode this step exists to catch.

Return:

- the question Fable was given;
- its verdict, and whether you agree;
- findings you verified, most serious first;
- claims that failed verification, and what you found instead;
- recommended changes, kept separate from changes already made;
- any lane failure.

Pasting the reply verbatim is not a report. Implement nothing unless implementation was already part of the request.

## Where this fits

- A bounded conformance or contract check, cheaply: `glm-review`.
- A whole-codebase grade with a comparable score: `survey`.
- Correctness review of a diff: the host's own code review.
- Rebuilding what happened rather than judging it: `muster`.
