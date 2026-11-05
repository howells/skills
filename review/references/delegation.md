# Harness delegation

Use this when the harness can start a separate thread or task with a chosen model, such as T3 Code's `delegate_task`. Don't start a CLI first. Give the user the returned thread link verbatim.

- **Find the model through the harness**: `orchestrator_capabilities` in T3 Code, otherwise its model catalogue, custom models included. Match the requested family and version exactly rather than taking whatever a native tool lists. For `muse` or `wonder`, pick the standard `muse-wonder-<version>`, not Spark or the full variant unless asked.
- **Choose the route.** Use a native subagent only for the same provider, when it runs the selected model and starts without this conversation's history. Otherwise call `delegate_task` with the discovered `providerInstanceId`, exact `model`, its high-effort option, the brief as `task`, `role: "review"` and a `clientRequestId` stable for this round. Never create a top-level thread for a review.
- **Read-only is in the brief.** T3 approval modes are not an operating-system sandbox, so keep the read-only line in the brief and report the actual isolation. Don't widen permissions to get past a refusal.
- **Wait, don't poll.** Keep the `taskId` and follow the host's next action and completion notice. Cancel with the host's cancel tool if you abandon the review or it passes 30 minutes.
- **Done** means a completed task with a non-empty answer. Check the returned provider and model against the target.
- **Another round** is a new `delegate_task` with the original brief, prior findings, your verification and remaining objections, and a new `clientRequestId`. Never message the backing `childThreadId`.

If T3 is present but its tools are missing from the initial catalogue, call `orchestrator_capabilities` once directly before calling it unavailable. An ACP host that supplies `T3_ACP_MCP_NODE` exposes it like this:

```bash
ELECTRON_RUN_AS_NODE=1 "$T3_ACP_MCP_NODE" ${T3_ACP_MCP_ENTRYPOINT:+"$T3_ACP_MCP_ENTRYPOINT"} \
  acp-mcp-call orchestrator_capabilities '{}'
```
