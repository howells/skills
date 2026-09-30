---
name: fable-review
description: "Get an independent review from Claude Fable 5.1, then verify its claims before acting. Use for a hard judgement call: a design or architecture decision, a taste question, a plan worth arguing with. Not for code questions (`astra-review`), bounded checks (`glm-review`) or a codebase grade (`simplify`)."
---

# Fable review

Fable is the judgement lane, for the calls that are genuinely hard: which of two architectures survives contact, whether a plan's premise holds, whether an interface reads the way its author thinks it does. Use it sparingly and on questions where a second opinion changes what you do next.

What comes back is a set of leads. Verify each one before acting on it.

## Choosing the lane

Three review skills send a brief to an outside model, chosen by the kind of question rather than its importance:

| The question | Lane |
| --- | --- |
| A bounded check against criteria the brief states: a contract, a spec, copy against a style guide | `glm-review` - cheap |
| An answer the repository can settle: what changed when, whether a diff does what it claims, where it breaks | `astra-review` - frontier, runs read-only commands |
| A judgement call with no checkable answer: architecture, taste, a plan, with the evidence in the brief | `fable-review` - frontier, reads files only |

A routine correctness pass over a diff is the host's own code review, not a lane.

## The route

The Claude CLI is the route, and it works the same from Claude Code, Codex and OpenCode, because all three can run a shell command.

```bash
claude -p \
  --model fable \
  --effort high \
  --permission-mode plan \
  --tools "Read,Glob,Grep" \
  --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
  --disallowedTools "Edit,Write,NotebookEdit" \
  --output-format json \
  < brief.md
```

- **Pass the brief on stdin, and close it.** `--disallowedTools` is variadic and will otherwise swallow a positional prompt as tool names, which fails with `Permission deny rule "…" matches no known tool` and never reaches the model.
- Run it from the repository under review; the CLI reads files relative to the working directory. Add `--add-dir` for a path outside it.
- `--tools "Read,Glob,Grep"` removes every other built-in tool, including the shell. `--allowedTools` would only preapprove tools, not remove the rest. The empty strict MCP config keeps unrelated integrations from starting.
- Plan mode and the denied edit tools reduce write access, but a successful refusal is not proof that every write route is blocked. Keep the read-only boundary in the brief as well.
- `--output-format json` returns the answer with its metadata, so the model that served it can be checked.
- `high` effort is the default for this skill. Use a different effort only when the user explicitly asks for one.

Confirm the lane before the first invocation in a session:

```bash
printf 'Reply with exactly: lane-ok' | claude -p --model fable --effort high --permission-mode plan --output-format json
```

The CLI may return a result object or an array of messages; in the latter case read the final message with `type: "result"`. Require `is_error: false`, a `result` of exactly `lane-ok`, and `claude-fable-5-1` among the keys of `modelUsage`. The `fable` alias resolves to that id, not to the literal string `fable`. Stop if `modelUsage` names a different model or version. If `modelUsage` is absent, the lane may still run, but the report must call the model's identity unverified rather than assert the exact version.

Without `lane-ok`, stop and name the cause: `claude` missing from the path, credentials absent or expired, or the alias no longer resolving to Fable. Substituting Opus, Sonnet or another lab's model is a failed run, because the point of the lane is which model answered.

**Do not substitute the Claude Code subagent.** In Claude Code a fable subagent is reachable through the Agent tool, and it inherits this session's context and instructions. That makes it useful for delegated work and useless as an independent read, since it has already been told what you think. The subprocess starts clean, which is the whole value. If you are already running on Fable, the subprocess gives an independent context but not an independent model: say so in the report, or use `astra-review` if the question fits it.

## Build a bounded brief

Investigate first, so Fable spends its turn on the judgement rather than on rediscovering the repository. A brief carries:

- the question, stated as a decision someone has to make;
- the artifact: paths, excerpts, diff or base commit, current status. Fable cannot run `git`, so paste the diff or the excerpts it needs;
- the options already on the table, and what each would cost;
- constraints, settled decisions, and explicit non-goals;
- validation already run, and what remains uncertain;
- the boundary, verbatim: `Read-only review. Do not edit files or run state-changing commands.`

Ask for a verdict, the reasoning that leads to it, where it disagrees with the proposed direction, and what it would need to change its mind.

A brief that names no decision gets an essay. "Review this architecture" fails that bar; "we chose X over Y for reason Z - what does that cost us in eighteen months" does not.

## Run it and wait

Enforce a limit of 1800 seconds of wall-clock time on the subprocess and its children. Launch it through Python `subprocess.Popen(start_new_session=True)`, pass the brief with `communicate(input=..., timeout=1800)` so stdin closes, and kill the process group on `TimeoutExpired`. Don't assume GNU `timeout` exists on macOS. A short tool yield is fine if it returns a live session; it must not kill the review.

A multi-file judgement brief measured at 119 seconds at high effort, in the one run timed so far. Duration tracks how much the model reads and how hard the question is, so a brief that sends it through many files will use more of the limit.

A run succeeded when it exits 0 and the result has `is_error: false` and non-empty `result` text. A started process is not a review. At the limit, kill it, say so, and stop. Output that arrives empty or cut off mid-argument is a failed run, reported as one rather than salvaged into a partial verdict.

Retry once on a transport or internal-server failure. Report an authentication, quota, billing or rate-limit rejection and stop without retrying, because those repeat.

## Verify, then report

Check every material claim against the source, the diff, the tests, or the running product. A claim you could not confirm stays labelled unconfirmed. Fable argues well, and a well-argued wrong claim is the failure mode this step exists to catch.

Return:

- the question Fable was given;
- its verdict, and whether you agree;
- findings you verified, most serious first;
- claims that failed verification, and what you found instead;
- recommended changes, kept separate from changes already made;
- any lane failure, including a run where Fable reviewed its own model's work.

Pasting the reply verbatim is not a report. Implement nothing unless implementation was already part of the request.

## Where this fits

- A question the code can settle, with commands to prove it: `astra-review`.
- A cheap check against stated criteria: `glm-review`.
- A whole-codebase grade with a comparable score: `simplify`.
- A routine correctness pass over a diff: the host's own code review.
- Rebuilding what happened rather than judging it: `muster`.
