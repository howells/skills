---
name: glm-review
description: "Get an independent read-only review from GLM 5.3 Flash via OpenCode, then verify its claims before acting. Use when the user names GLM, or for a cheap bounded check: conformance to stated criteria, a contract, UI copy. Not for a hard judgement call (`fable-review`) or a codebase grade (`simplify`)."
---

# GLM review

GLM 5.3 Flash is the cheap second-opinion lane: a bounded contract check, conformance to stated criteria, UI copy, search relevance, or any concrete review that benefits from an independent read. What comes back is a set of leads. Verify each one before you act on it.

The question decides the lane rather than its importance. A check with a right answer comes here. A judgement call with no checkable answer goes to `fable-review`, which costs a great deal more.

## The coding plan is the only route

Run the model as `zai-coding-plan/glm-5.3-flash`. The same weights are reachable through `zai/`, `openrouter/z-ai/` and `opencode-go/`; those bill against different accounts and this skill uses the coding plan.

Confirm the lane before the first invocation in a session:

```bash
opencode models zai-coding-plan | grep -qx 'zai-coding-plan/glm-5.3-flash' && echo lane-ok
```

Model listing establishes availability, not successful authentication. Check the actual invocation outcome before reporting a completed review.

Without `lane-ok`, stop and name the cause: `opencode` missing from the path, Z.AI Coding Plan credentials absent (`opencode auth list` shows no `Z.AI Coding Plan` entry), or the lane authenticated but no longer serving that model. Swapping in another provider, another GLM size, or another model is a failed run.

## Build a bounded brief

Investigate first, so GLM gets verified current facts rather than rediscovering the repository. A brief carries:

- the exact question or decision;
- the artifact: paths, relevant excerpts, diff or base commit, current status;
- constraints, settled decisions, and explicit non-goals;
- the review lenses that matter here;
- validation already run, and known uncertainty;
- the boundary, verbatim: `Read-only review. Do not edit files or run state-changing commands.`

Ask for a verdict, findings with `file:line` evidence, disagreements with the proposed direction, and concrete changes.

The brief is done when someone with no access to this session could act on it alone. "Review this repo" fails that bar; narrow the artifact and the questions first.

## Invoke

Run from the repository under review. Set `REPO` to its absolute path, `SCOPE` to a short label and `PROMPT` to the complete brief before using the example. Confirm the installed CLI supports the flags with `opencode run --help`.

```bash
OPENCODE_PERMISSION='{"*":"deny","read":"allow","glob":"allow","grep":"allow","list":"allow"}' \
opencode run \
  --pure \
  --dir "$REPO" \
  --agent plan \
  --model zai-coding-plan/glm-5.3-flash \
  --title "GLM review: $SCOPE" \
  --format default \
  -- "$PROMPT" < /dev/null
```

Run it through the Python wrapper below rather than this shell form when you need the timeout: the redirect matters either way.

Leave `--auto` off. Plan mode and `--pure` do not by themselves isolate MCP integrations or prove read-only access.

Restrict the run with the `OPENCODE_PERMISSION` environment variable, as a JSON **object**, set on the invocation:

```
OPENCODE_PERMISSION='{"*":"deny","read":"allow","glob":"allow","grep":"allow","list":"allow"}'
```

Measured on opencode 1.18.31, and each of these cost a wasted run:

- The object form is enforced. The **array** form (`[{permission,action,pattern}]`) is accepted and silently ignored, even though opencode's own session log prints permissions in that shape. Do not copy the log's format.
- A run-scoped `OPENCODE_CONFIG` file does **not** restrict `opencode run`. Its `permission` and `tools` blocks show up in `opencode debug config` and never reach the session: the session is created with only the `question`, `plan_enter` and `plan_exit` denies. A config file alone leaves bash enabled.
- `--pure` and plan mode do not restrict tools either. Plan's resolved permission set is `* allow`.

Verify rather than assume: after a run, `opencode.log` records one `message=evaluated permission=<tool>` line per tool call with the rule that matched. `action.permission=*` on a tool you meant to deny means the restriction did not apply. If you cannot establish the restriction, say the read-only lane is unavailable rather than claiming a sandbox you did not get. Do not change the user's persistent configuration. Current primary documentation: [configuration](https://opencode.ai/docs/config/), [permissions](https://opencode.ai/docs/permissions/) and [MCP servers](https://opencode.ai/docs/mcp-servers/).

Retry once on a transport or internal-server failure. Report an authentication, quota, or billing rejection and stop without retrying: those repeat.

Wait for actual output. A started process or a created session is not a review.

**Close stdin.** `opencode run` blocks indefinitely on an open stdin pipe: it never starts the session, never writes to the database, and returns zero bytes, so the failure leaves no trace to diagnose afterwards. Pass `stdin=subprocess.DEVNULL`. This is the single most common way a run returns nothing.

Run it with Python `subprocess.Popen(start_new_session=True, stdin=DEVNULL)` and `communicate(timeout=...)`, terminating the process group on timeout. Do not assume GNU `timeout` exists on macOS. Write the captured output to a file as well as reading it, so a killed run still leaves whatever arrived.

**Budget 1800 seconds, not 600.** Measured over 236 runs: the median review takes about 300s, ten exceeded 600s and the longest ran 1262s. Duration tracks the input the model reads, so the largest briefs are the ones a tight limit kills, and a review killed at 600s typically had minutes of work left. Point a brief at a minified bundle or a large dist file and it will need every second of the budget; scope reads to source where you can.

At the limit, terminate the run, say so, and stop. Output that arrives empty or cut off mid-findings is a failed run, and is reported as one rather than salvaged into a partial verdict.

## Verify, then report

Check every material claim against the source, the diff, the tests, or the running product. A claim you could not confirm stays labelled unconfirmed.

Return:

- the scope GLM received;
- findings you verified, most serious first;
- claims that failed verification, and what you found instead;
- recommended changes, kept separate from changes already made;
- any lane failure.

Pasting GLM's reply verbatim is not a report. Implement nothing unless implementation was already part of the user's request.
