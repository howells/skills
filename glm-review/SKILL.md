---
name: glm-review
description: "Get an independent read-only review from GLM 5.3 Flash on the Z.AI Coding Plan via OpenCode, then verify its claims before acting. Use when the user names GLM, or for a cheap bounded check: conformance to stated criteria, a contract, UI copy. Not for a hard judgement call (`fable-review`) or a codebase grade (`survey`)."
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
opencode run \
  --pure \
  --dir "$REPO" \
  --agent plan \
  --model zai-coding-plan/glm-5.3-flash \
  --title "GLM review: $SCOPE" \
  --format default \
  -- "$PROMPT"
```

Leave `--auto` off. Plan mode and `--pure` do not by themselves isolate MCP integrations or prove read-only access.

Before invoking the model, inspect the resolved configuration locally (`opencode debug config` and `opencode debug agent plan`); do not print credentials or unrelated configuration into the conversation. Apply a run-scoped configuration that denies every tool except `read`, `glob` and `grep`, denies shell/edit/subagent access, and disables each inherited MCP server by name. In V1, permissions use `permission` and MCP entries accept `enabled: false`; V2 uses a different permission schema. Use the installed version's schema and verify the resolved agent's effective permissions before running. Configuration files merge: an empty `mcp` object or a minimal `OPENCODE_CONFIG` file does not erase inherited servers or specific allow rules. Do not change the user's persistent configuration.

If the host cannot establish those restrictions, pass the relevant source and diff as the brief in a verified isolated environment, or report that the read-only lane is unavailable. A prose refusal probe is not a substitute for inspecting permissions. Current primary documentation: [configuration](https://opencode.ai/docs/config/), [permissions](https://opencode.ai/docs/permissions/) and [MCP servers](https://opencode.ai/docs/mcp-servers/).

Retry once on a transport or internal-server failure. Report an authentication, quota, or billing rejection and stop without retrying: those repeat.

Wait for actual output. A started process or a created session is not a review. Enforce a ten-minute wall-clock limit with the host’s process-tree timeout, or a runner using Python `subprocess.Popen(start_new_session=True)` and `communicate(timeout=600)` that terminates the process group on timeout. Short tool yields must preserve the running session. Do not assume GNU `timeout` exists on macOS. At the limit, terminate the run, say so, and stop. Output that arrives empty or cut off mid-findings is a failed run too, and is reported as one rather than salvaged into a partial verdict.

## Verify, then report

Check every material claim against the source, the diff, the tests, or the running product. A claim you could not confirm stays labelled unconfirmed.

Return:

- the scope GLM received;
- findings you verified, most serious first;
- claims that failed verification, and what you found instead;
- recommended changes, kept separate from changes already made;
- any lane failure.

Pasting GLM's reply verbatim is not a report. Implement nothing unless implementation was already part of the user's request.
