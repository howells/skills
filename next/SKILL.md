---
name: next
description: "Deliver the next actionable tracker item with Plimsoll, then stop. Not for codebase audits (`survey`) or session recovery (`muster`)."
---

# Next

One invocation implements one selected outcome, including documented prerequisites, and pushes a reviewable PR. It follows configured auto-merge through completion; otherwise it waits for review with the PR open. A necessary blocker can be implemented in the same task; unrelated work remains separate. The user need not name the tracker, choose an item or separately invoke Plimsoll. An optional issue identifier overrides automatic selection; supplied priority and scope constraints always win.

Use the current project and its instructions. Discover integrations and accounts from the environment; never assume a particular workspace, tracker, release provider or consumer. Load the installed `plimsoll` skill when available. The essential execution rules below also apply when it is unavailable. Use the configured tracker capability, including the `linear` skill when appropriate.

## Adapt to the harness

This skill works through the capabilities exposed by its host: Codex, Claude Code, OpenCode, Cursor or another compatible harness. The portable instructions live here; `agents/openai.yaml` is optional Codex UI metadata, not a runtime dependency.

Identify the active harness from its supplied context and tools. Use its native skill invocation, project instructions, tracker access, subagent tools, model selection, permission handling and completion notifications. Do not assume Codex tool names, task links, dollar-prefixed invocation syntax or a particular provider's model identifiers are available elsewhere. Use installed help or configuration only when a needed capability is unclear; do not perform a broad environment audit.

Prefer native subagents. If delegation or per-agent model selection is unavailable, use the supported subset, state the limitation once and keep delivering. Parallel tool calls alone are not multiple agents. Do not install another harness, add credentials, change provider configuration or spawn external agent processes merely to manufacture model variety.

## Choose the item

Every time an item is selected, announce it before implementation or a tracker status change in **one short, plain-language sentence**: a clickable tracker identifier followed by the concrete outcome for the person using the product. Assume the user has no prior context. Explain technical ticket titles in everyday words; omit implementation details, jargon and prioritization reasoning. For example: "[APP-123](https://example.com/issues/APP-123): Make search show the matching products instead of an empty page." Use the actual item URL, never the example URL. For already-delivered work, use the same one-sentence format to say what already works and that its ticket status will be corrected. This announcement is mandatory even when no code change is needed; it is information, not an approval request.

1. Establish the current project, tracker scope and standing constraints from project instructions and the conversation. Ask only if multiple plausible projects or accounts remain unresolved. Do not ask the user to select among tickets the agent can rank.
2. Read open items in the tracker's native priority order. Respect an urgent-only restriction; an empty urgent queue does not authorize lower-priority work. Otherwise choose the highest-priority actionable item. Within the same priority, prefer work that unblocks an active consumer, then the oldest ready item.
3. Fetch the leading item directly from the tracker and check its current status, description, acceptance criteria, dependencies, recent comments and linked implementation. Do not rely on a cached queue, priority label or earlier conversation to establish that it is still open. Skip items already completed, cancelled or superseded; for an explicitly supplied identifier, report that state and stop instead of silently selecting another. Assess unresolved prerequisites using the blocker rule below rather than skipping an item merely because it has a dependency. Skip work that cannot proceed without a human decision, unavailable external access or confirmed active ownership by another session. A historical assignee alone is not evidence of active work. Read only enough related session state to resolve ownership; contact peers only with existing authorization.
4. Independently check whether the work is already delivered even when the tracker still says open or urgent. Compare acceptance criteria with linked commits or PRs, the relevant deployed revision when required, and current consumer behaviour. For a bug, capture a small reproduction that can actually expose the reported failure before editing; for a feature, identify which acceptance behaviour is missing. Neither an old failure report nor a merged PR alone establishes the current outcome. If all completion criteria already pass, attach the evidence and reconcile the stale status using the project's permitted completion transition; that completes this invocation without inventing a code change. If only part is delivered, state exactly what remains and implement only that gap. If verification is unavailable, keep the item open and report the missing evidence rather than assuming completion. Re-fetch status before changing it so a concurrent update is not overwritten.
5. Give the one-sentence item announcement above and proceed without a selection approval round; do not repeat it if already given while reconciling completed work. If no eligible work exists, report the actual blockers and stop; do not turn selection into a backlog audit.

## Deliver within one scope

Work to the selected item's spec and acceptance criteria without reopening settled design. Write necessary clarifications, agreed decisions and acceptance changes back to that item before implementing them; preserve existing requirements and distinguish unresolved questions from decisions. Do not create a separate repository spec document or add unrelated requirements. Use the project's established implementation and release workflow; an installed `implement` skill can supply that workflow, with Plimsoll governing optional process weight. Keep shared APIs generalizable to their domain rather than naming them for the requesting consumer.

Use multiple parallel agents with a deliberate variety of models whenever the item has useful independent work. This skill explicitly requests delegation; the user does not need to repeat that instruction. Split bounded subtasks with distinct ownership and run them concurrently while the coordinator advances integration or another independent part of the item.

Choose model roles first, then resolve them to models actually available in the active harness:

- **Reasoning:** demanding diagnosis, architecture and interlocking reasoning. Prefer Sol when available.
- **Implementation:** bounded implementation and integration work. Prefer Terra when available.
- **Focused work:** mechanical edits, narrow investigation and acceptance checks. Prefer Luna when available.

Sol, Terra and Luna are preferences, not dependencies. In Claude Code, OpenCode, Cursor or any other host, map these roles to its configured models and supported delegation controls; never pass an unrecognized alias or assume the host exposes every model its provider offers. Use a mix when the subtasks warrant it; do not select the same model for every agent by default or force all three into every item. State the selected roles and models briefly when delegating. Give agents only the context and files they need. The coordinator integrates and inspects their changes; extra reviewers need a specific unresolved risk. Keep a truly tiny or inseparable change local rather than inventing work to occupy agents.

Preserve authorization already given. Do not repeat an approval request merely because the workflow reached another step. Invocation authorizes selecting and implementing the item and its necessary, documented prerequisites, committing and pushing that work, and opening or updating its PR; it does not independently authorize destructive operations, external messages or release actions outside the user's existing scope. Complete the reviewable work before requesting any genuinely missing authorization.

Follow repository worktree and branch ownership rules. Keep durable decisions and evidence on the owning tracker item where project policy requires it. Record only what another session needs: scope, current commit/worktree, completed verification and the exact remaining action. Do not merge unrelated branches or start another item as part of cleanup.

## Capture unrelated work without taking it on

When implementation reveals an unrelated defect or improvement, record it in Linear when Linear owns the project, otherwise in the configured tracker. This workflow includes creating those follow-up items and updating the selected item's spec and evidence; do not ask for repeated permission for these routine tracker writes. Respect account access and project policy. If tracker access is unavailable, include a concise draft in the final response and state that it was not filed.

Search for an existing item describing the same behaviour before creating one. Add new evidence to the matching item instead of duplicating it. Keep each new item self-contained: a plain title, observed behaviour and evidence, who is affected, the desired outcome, testable acceptance criteria, and a link to the item that exposed it. Mark uncertain findings as needing investigation rather than asserting an unverified defect. Keep this capture brief, then return to the selected item; do not start an audit or investigate every possible improvement.

Set priority using the project's policy and the finding's measured impact on the current work. If no policy is defined, use these meanings and map them to the tracker's native values:

- **Urgent:** an active severe incident or an evidenced blocker of an explicitly urgent delivery with no viable workaround.
- **High:** blocks the selected item's acceptance or a near-term committed outcome, without meeting the urgent threshold.
- **Normal:** meaningful independent work that does not prevent the selected delivery.
- **Low:** optional polish or minor inconvenience with a practical workaround.

Include one sentence explaining the priority. A finding does not inherit Urgent merely because it was discovered during an urgent item. For an existing item, change priority only when new evidence warrants it and explain the change without overwriting a concurrent decision.

If the finding does not prevent the selected outcome, link it as related and continue the original work. Include the filed follow-up links in the final response. Creating unrelated follow-ups does not authorize implementing them.

## Resolve necessary blockers in the same task

A blocker belongs in this task when evidence shows that the selected item's acceptance cannot pass without it. This applies both to existing documented dependencies and blockers discovered during implementation. Optional cleanup, adjacent features and speculative improvements remain separate.

1. Verify the blocker is still open and actually unresolved, using the same status and delivery checks as the selected item. Reuse or create its tracker item, record the specific acceptance criterion it prevents, and link the blocking relationship. Keep each item's spec and evidence distinct.
2. Introduce the linked blocker in one short, plain-language sentence explaining why it is needed for the original outcome. Proceed without asking the user to restart or approve routine dependency work. Priority restrictions govern selection of the original item; a necessary prerequisite may have a lower priority and still be required work.
3. Implement the smallest complete prerequisite, verify it, then resume and verify the original outcome. Use the existing task, branch and delivery path where repository policy allows; do not create a separate task or PR solely because the prerequisite has its own identifier. Parallelize independent work where useful. Apply the same test for any further dependency: it must demonstrably be necessary for the original acceptance, not merely related to another blocker.
4. Record verification evidence and the appropriate status on each item. Include the original outcome and its prerequisites in the PR handoff below; keep completion pending wherever merge or deployment evidence is still required. Summarize the supporting items alongside the original item.

A documented blocker does not override access, ownership or authorization boundaries. If it requires unavailable credentials, an external decision, another active owner's work, an observation period or an unauthorized operation, complete the independent work and report exactly what is needed. Do not take over another owner's changes, invent evidence or reset Plimsoll's budgets because another ticket was added. Keep the dependency chain tied to the original outcome; discovering a separate initiative does not turn this task into a queue sweep.

## Plimsoll during execution

- Name the payload: the page, query or other consumer behaviour that will demonstrate acceptance. Verify that directly. Passing tests alone does not establish delivery.
- Choose the narrowest check that could catch a plausible failure in the change. Run required final repository checks once at the delivery boundary. Do not widen checks because the previous check passed, generate tests without a named risk or add a review agent to every item.
- Diagnose failures before retrying. On a database timeout, inspect the actual connection, `pg_stat_activity`, wait events and blocking sessions, plus `pg_stat_statements` when available, before changing timeouts or query shape. Confirm the target database before any fixture or data write. If access is missing, state the diagnostic limitation rather than guessing.
- Set a written duration and enforced hard stop before a build or deployment. Use Plimsoll's limits: with a known normal duration, the smaller of 15 minutes and the larger of twice normal or normal plus two minutes; otherwise 10 minutes. A shorter repository limit wins; a longer existing release contract or explicit user exception must be recorded before starting. Build and publish are distinct operations with distinct budgets. Reuse an unchanged verified build artifact when only publication failed.
- Prefer completion notifications; otherwise make one status check at the hard stop. Do useful independent work meanwhile. Do not turn waiting into repeated polls. A retry needs new evidence and a meaningful change; it does not reset the budget by itself.
- For Vercel, build on the user's machine and deploy the prebuilt artifact through the project's release entrypoint. Never substitute a remote source build. Verify the deployed revision and exercise the actual consumer behaviour.
- After three failed attempts at the same problem, stop guessing. Obtain a bounded independent diagnosis if available, or report the measured blocker and exact next action. Do not make release infrastructure, unrelated cleanup or the whole backlog the new assignment.

## Push the PR and follow the project's merge policy

For implementation work, the minimum handoff is a committed, pushed branch and an open, reviewable PR against the project's intended base, with the acceptance evidence and all supporting tracker items linked. A local commit or pushed branch alone is not that handoff. Update the existing PR when one already owns this work. Do not push implementation directly to the base branch. Evidence-only status reconciliation does not require a manufactured PR.

Inspect the project's actual merge policy and this PR's eligibility. Auto-merge may be a forge setting, merge queue or repository automation; the repository merely allowing auto-merge does not prove this PR is enrolled. Use the configured mechanism and follow any existing policy for enabling it on this PR. Never enable repository-wide auto-merge or bypass required reviews just to complete this workflow.

- **Auto-merge is configured for this work:** follow the PR through required checks, approvals and merge. Address actionable failures and conflicts caused by this work, then push the corrections to the same PR. Verify that the forge reports the PR merged and record the resulting commit; a green check, queued merge or deleted branch is not merge evidence. Complete any authorized post-merge release and consumer verification required by the project. Do not claim the item is finished while required delivery evidence is missing.
- **Auto-merge is not configured:** leave the PR open and ready for review, report its link and check status, and wait for review or a user instruction. Do not manually merge, enable auto-merge, deploy the unmerged work or select another item. This is the intended handoff, not a failure. Resume the same PR when feedback or a merge event arrives.

Waiting uses available completion notifications and bounded waits under Plimsoll, never repeated status polling. If the host cannot wait for an external event, or the written wait budget expires, leave a precise pending state with the PR link, completed checks and the remaining event. Do not invent a continuing background watch. A pending merge remains pending; it is not completion. Create recurring monitoring only if the user explicitly requests it.

Attach acceptance evidence to the selected item and each prerequisite handled. Respect the project's tracker rules: ready for review, merged, deployed and verified are separate states. Evidence-only work remains open until its required evidence exists; another code change cannot substitute for an observation period.

Return the item and outcome, the PR and relevant commit/release/evidence links, any filed follow-ups with their priorities, and the exact current state: awaiting review, awaiting auto-merge, merged, or verified delivery. Claim only what was verified. After the handoff or completed delivery, do not continue the queue. Each subsequent independent item belongs in a fresh task; do not automatically create another task or clear context.
