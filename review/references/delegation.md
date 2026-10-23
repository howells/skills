# Harness threads

Use this route whenever the harness can start a separate thread or task with a chosen model, such as T3 Code's `delegate_task`. The review becomes a child thread of the current one: visible to the user, tracked by the harness, and independent of this conversation. Do not probe or start a CLI first.

Discover the provider instances and current models from `orchestrator_capabilities`, including configured custom models. Match the argument to the requested family and version, not to whichever model a native tool happens to list. For `muse` or `wonder`, select the standard `muse-wonder-<version>` model, not Spark or the separate full variant unless requested.

For same-provider work, prefer a native subagent only when it supports the selected model and can start without inheriting conversation history. Otherwise, and for cross-provider work, use `delegate_task` with the discovered `providerInstanceId`, exact `model`, and the model's supported high-effort option. Supply only the bounded brief as `task`, with `role: "review"` and a stable `clientRequestId` for this round. Do not create a top-level thread for a review.

Use the most restrictive supported runtime mode. T3's `approval-required` mode is an approval boundary, not an operating-system read-only sandbox; keep the read-only instruction in the brief and report the actual isolation. If the user requires enforced read-only command execution, use the Codex CLI route for Sol or Astra rather than claiming delegation enforces it. Do not grant full access just to avoid a prompt.

Retain the returned `taskId`. Prefer async delegation for long work and use the host's completion notification. Read `task_status` when the answer is needed mid-turn; do not create polling agents or duplicate active work. An elapsed wait budget does not cancel the task. Cancel it with `task_cancel` if abandoning the invocation or enforcing the 1800-second review limit.

Require a completed task with a non-empty final answer and no remaining child work. Verify the returned provider and model against the selected target; an absent identity remains unverified. A failure or incomplete task is not a verdict.

For another review round, call `delegate_task` again with the original brief, prior findings, verification, responses and unresolved objections. Give each round a new `clientRequestId`, stable across retries of that round. The backing `childThreadId` is not a continuation target; do not send it a message to start a new round.

If T3 is present but its tools are missing from the initial catalogue, make one bounded direct call to `orchestrator_capabilities` before declaring it unavailable. An ACP host that supplies `T3_ACP_MCP_NODE` can use its supported transport:

```bash
ELECTRON_RUN_AS_NODE=1 "$T3_ACP_MCP_NODE" ${T3_ACP_MCP_ENTRYPOINT:+"$T3_ACP_MCP_ENTRYPOINT"} \
  acp-mcp-call orchestrator_capabilities '{}'
```

Use the same transport for `delegate_task`, `task_status` and `task_cancel`, passing structured JSON with the discovered target. Do not invent model IDs or replace an available app-owned route with an ordinary shell subprocess.
