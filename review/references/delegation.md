# Harness threads

Use this route whenever the harness can start a separate thread or task with a chosen model, such as T3 Code's `delegate_task`. The review becomes a child thread of the current one: visible to the user, tracked by the harness, and independent of this conversation. Do not probe or start a CLI first.

Follow live host orchestration, failure, routing and approval instructions when they differ from these examples. Use the returned thread link verbatim.

Discover the available models and supported options through the active harness: `orchestrator_capabilities` in T3 Code, otherwise that harness's model catalogue and native delegation controls. Include configured custom models. Match the argument to the requested family and version; do not silently substitute whichever model a native tool happens to list. For `muse` or `wonder`, select the standard `muse-wonder-<version>` model, not Spark or the separate full variant unless requested.

For same-provider work, prefer a native subagent only when it supports the selected model and can start without inheriting conversation history. Otherwise, and for cross-provider work, use `delegate_task` with the discovered `providerInstanceId`, exact `model`, and the model's supported high-effort option. Supply only the bounded brief as `task`, with `role: "review"` and a stable `clientRequestId` for this round. Do not create a top-level thread for a review.

Before dispatch, ensure the brief and essential external evidence have durable locations. The host's persisted task record can hold the brief; files available only in temporary storage need an authorised durable copy. Keep private material in private storage, check copies are complete and include exact locations in the handoff. Link them from the owning tracker item when updates are authorised.

Preserve the runtime mode required by the live host and user. T3's approval modes are approval boundaries, not operating-system read-only sandboxes; keep the read-only instruction in the brief and report the actual isolation. If enforced read-only execution is required but the selected route cannot provide it, report that limitation; use a permitted CLI route only when the live host allows it. Do not widen permissions to evade a refusal.

Retain the returned `taskId` and follow the host's returned next action and completion notifications. Do not poll a running delegate or create polling agents or duplicate active work. An elapsed wait budget does not cancel the task. Cancel it with the host's task-cancellation tool if abandoning the invocation or enforcing the 1800-second review limit.

Record task identity, selected provider/model, actual isolation, current ownership, evidence locations and the scope of approvals and holds in a durable handoff. Include unanswered questions' exact text, host identifiers when available and answer status. On recovery, reconcile this with live host state before resuming authorised work. Preserve a visible unanswered question; if it is missing or expired and user input is still needed, raise one question through the supported question tool with a recommendation, then yield until an explicit answer. A restart, timeout, selected default or unrelated message is not an answer. Keep completed work idle and follow the live host's rules for further review rounds.

Require a completed task with a non-empty final answer and no remaining child work. Verify the returned provider and model against the selected target; an absent identity remains unverified. A failure or incomplete task is not a verdict.

For another review round, call `delegate_task` again with the original brief, prior findings, verification, responses and unresolved objections. Give each round a new `clientRequestId`, stable across retries of that round. The backing `childThreadId` is not a continuation target; do not send it a message to start a new round.

If T3 is present but its tools are missing from the initial catalogue, make one bounded direct call to `orchestrator_capabilities` before declaring it unavailable. An ACP host that supplies `T3_ACP_MCP_NODE` can use its supported transport:

```bash
ELECTRON_RUN_AS_NODE=1 "$T3_ACP_MCP_NODE" ${T3_ACP_MCP_ENTRYPOINT:+"$T3_ACP_MCP_ENTRYPOINT"} \
  acp-mcp-call orchestrator_capabilities '{}'
```

Use that transport only for operations permitted by the live host, passing structured JSON with the discovered target. Do not invent model IDs or replace an available app-owned route with an ordinary shell subprocess.
