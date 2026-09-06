---
name: next
description: "Deliver the next actionable tracker item with Plimsoll, then stop. Not for codebase audits (`survey`) or session recovery (`muster`)."
---

# Next

One invocation selects, implements and verifies one tracker item, then stops. The user need not name the tracker, choose an item or separately invoke Plimsoll. An optional issue identifier overrides automatic selection; supplied priority and scope constraints always win.

Use the current project and its instructions. Discover integrations and accounts from the environment; never assume a particular workspace, tracker, release provider or consumer. Load the installed `plimsoll` skill when available. The essential execution rules below also apply when it is unavailable. Use the configured tracker capability, including the `linear` skill when appropriate.

## Adapt to the harness

This skill works through the capabilities exposed by its host: Codex, Claude Code, OpenCode, Cursor or another compatible harness. The portable instructions live here; `agents/openai.yaml` is optional Codex UI metadata, not a runtime dependency.

Identify the active harness from its supplied context and tools. Use its native skill invocation, project instructions, tracker access, subagent tools, model selection, permission handling and completion notifications. Do not assume Codex tool names, task links, dollar-prefixed invocation syntax or a particular provider's model identifiers are available elsewhere. Use installed help or configuration only when a needed capability is unclear; do not perform a broad environment audit.

Prefer native subagents. If delegation or per-agent model selection is unavailable, use the supported subset, state the limitation once and keep delivering. Parallel tool calls alone are not multiple agents. Do not install another harness, add credentials, change provider configuration or spawn external agent processes merely to manufacture model variety.

## Choose the item

Every time an item is selected, announce it before implementation or a tracker status change in **one short, plain-language sentence**: a clickable tracker identifier followed by the concrete outcome for the person using the product. Assume the user has no prior context. Explain technical ticket titles in everyday words; omit implementation details, jargon and prioritization reasoning. For example: "[APP-123](https://example.com/issues/APP-123): Make search show the matching products instead of an empty page." Use the actual item URL, never the example URL. For already-delivered work, use the same one-sentence format to say what already works and that its ticket status will be corrected. This announcement is mandatory even when no code change is needed; it is information, not an approval request.

1. Establish the current project, tracker scope and standing constraints from project instructions and the conversation. Ask only if multiple plausible projects or accounts remain unresolved. Do not ask the user to select among tickets the agent can rank.
2. Read open items in the tracker's native priority order. Respect an urgent-only restriction; an empty urgent queue does not authorize lower-priority work. Otherwise choose the highest-priority actionable item. Within the same priority, prefer work that unblocks an active consumer, then the oldest ready item.
3. Fetch the leading item directly from the tracker and check its current status, description, acceptance criteria, dependencies, recent comments and linked implementation. Do not rely on a cached queue, priority label or earlier conversation to establish that it is still open. Skip items already completed, cancelled or superseded; for an explicitly supplied identifier, report that state and stop instead of silently selecting another. Skip work with unresolved prerequisites, a required human decision or confirmed active ownership by another session. A historical assignee alone is not evidence of active work. Read only enough related session state to resolve ownership; contact peers only with existing authorization.
4. Independently check whether the work is already delivered even when the tracker still says open or urgent. Compare acceptance criteria with linked commits or PRs, the relevant deployed revision when required, and current consumer behaviour. For a bug, capture a small reproduction that can actually expose the reported failure before editing; for a feature, identify which acceptance behaviour is missing. Neither an old failure report nor a merged PR alone establishes the current outcome. If all completion criteria already pass, attach the evidence and reconcile the stale status using the project's permitted completion transition; that completes this invocation without inventing a code change. If only part is delivered, state exactly what remains and implement only that gap. If verification is unavailable, keep the item open and report the missing evidence rather than assuming completion. Re-fetch status before changing it so a concurrent update is not overwritten.
5. Give the one-sentence item announcement above and proceed without a selection approval round; do not repeat it if already given while reconciling completed work. If no eligible work exists, report the actual blockers and stop; do not turn selection into a backlog audit.

## Deliver within one scope

Implement the existing acceptance criteria without reopening settled design. Define missing details only where they affect the result. Use the project's established implementation and release workflow; an installed `implement` skill can supply that workflow, with Plimsoll governing optional process weight. Keep shared APIs generalizable to their domain rather than naming them for the requesting consumer.

Use multiple parallel agents with a deliberate variety of models whenever the item has useful independent work. This skill explicitly requests delegation; the user does not need to repeat that instruction. Split bounded subtasks with distinct ownership and run them concurrently while the coordinator advances integration or another independent part of the item.

Choose model roles first, then resolve them to models actually available in the active harness:

- **Reasoning:** demanding diagnosis, architecture and interlocking reasoning. Prefer Sol when available.
- **Implementation:** bounded implementation and integration work. Prefer Terra when available.
- **Focused work:** mechanical edits, narrow investigation and acceptance checks. Prefer Luna when available.

Sol, Terra and Luna are preferences, not dependencies. In Claude Code, OpenCode, Cursor or any other host, map these roles to its configured models and supported delegation controls; never pass an unrecognized alias or assume the host exposes every model its provider offers. Use a mix when the subtasks warrant it; do not select the same model for every agent by default or force all three into every item. State the selected roles and models briefly when delegating. Give agents only the context and files they need. The coordinator integrates and inspects their changes; extra reviewers need a specific unresolved risk. Keep a truly tiny or inseparable change local rather than inventing work to occupy agents.

Preserve authorization already given. Do not repeat an approval request merely because the workflow reached another step. Invocation authorizes selecting and implementing the item; it does not independently authorize destructive operations, external messages or release actions outside the user's existing scope. Complete the reviewable work before requesting any genuinely missing authorization.

Follow repository worktree and branch ownership rules. Keep durable decisions and evidence on the owning tracker item where project policy requires it. Record only what another session needs: scope, current commit/worktree, completed verification and the exact remaining action. Do not merge unrelated branches or start another item as part of cleanup.

## Plimsoll during execution

- Name the payload: the page, query or other consumer behaviour that will demonstrate acceptance. Verify that directly. Passing tests alone does not establish delivery.
- Choose the narrowest check that could catch a plausible failure in the change. Run required final repository checks once at the delivery boundary. Do not widen checks because the previous check passed, generate tests without a named risk or add a review agent to every item.
- Diagnose failures before retrying. On a database timeout, inspect the actual connection, `pg_stat_activity`, wait events and blocking sessions, plus `pg_stat_statements` when available, before changing timeouts or query shape. Confirm the target database before any fixture or data write. If access is missing, state the diagnostic limitation rather than guessing.
- Set a written duration and enforced hard stop before a build or deployment. Use Plimsoll's limits: with a known normal duration, the smaller of 15 minutes and the larger of twice normal or normal plus two minutes; otherwise 10 minutes. A shorter repository limit wins; a longer existing release contract or explicit user exception must be recorded before starting. Build and publish are distinct operations with distinct budgets. Reuse an unchanged verified build artifact when only publication failed.
- Prefer completion notifications; otherwise make one status check at the hard stop. Do useful independent work meanwhile. Do not turn waiting into repeated polls. A retry needs new evidence and a meaningful change; it does not reset the budget by itself.
- For Vercel, build on the user's machine and deploy the prebuilt artifact through the project's release entrypoint. Never substitute a remote source build. Verify the deployed revision and exercise the actual consumer behaviour.
- After three failed attempts at the same problem, stop guessing. Obtain a bounded independent diagnosis if available, or report the measured blocker and exact next action. Do not make release infrastructure, unrelated cleanup or the whole backlog the new assignment.

## Finish and stop

Complete the authorized commit, merge and release steps and attach acceptance evidence to the tracker item. Respect the project's completion rules: merged, deployed and verified are separate states. Evidence-only work remains open until its required evidence exists; another code change cannot substitute for an observation period.

Return the item and outcome, the relevant commit/release/evidence links, and any remaining blocker. Claim completion only for what was verified. Then stop. Each subsequent item belongs in a fresh task; do not automatically create another task, clear context or continue the queue unless the user explicitly requests that behaviour.
