---
name: rebalance
description: "Reprioritize a project's backlog for a goal. Not implementation (`next`)."
---

# Rebalance

Set the project's current priorities around the user's goal. Review the whole open backlog, identify the unfinished work needed for that outcome, and make its essential delivery path urgent so `next` can pick it up. Reassess everything else by its current importance. These are the new priorities: no saved priority snapshot, expiry, restoration mechanism or extra tracking system.

Use the named project, or infer it from the current repository and conversation. Accept a goal and optional deadline in ordinary language, for example: “prepare the guided design flow for tomorrow's demo.” Resolve relative dates using the user's timezone. Announce the project, concrete outcome and deadline in one short sentence. Ask only when the target or a decision affecting scope cannot be established from available evidence. Do not invent a deadline or treat an example as an instruction to edit that project's tracker.

## Use the relevant parts of Ask Matt

This skill follows `ask-matt`'s routing principles. Read the installed router when available, and invoke its supporting skills only when a specific gap needs them. The essentials below apply independently; installing the whole collection or running its setup flow is not a prerequisite.

- **Clarify the outcome:** use `grilling` for a decision the user must make, after gathering facts yourself. A stated, testable goal needs no interview.
- **Make work buildable:** use `to-spec` when the intended behaviour is missing, then `to-tickets` when it needs several independent deliveries. Prefer small end-to-end increments with testable acceptance and explicit blocking relationships. Improve existing items before creating new ones.
- **Handle raw incoming reports:** use `triage` when a report needs investigation or clarification. Already specified items do not need another triage cycle merely because their priority changes.
- **Recognise unresolved decisions:** reserve `wayfinder` for a large effort whose route cannot yet be determined. Identify that gap and keep the independently actionable work moving; do not replace a bounded rebalance with a design programme.
- **Hand off to delivery:** leave self-contained items for fresh `next` tasks. Do not invoke `implement`, start coding, or automatically open another task.

Store specs, decisions and dependency evidence in the project's configured tracker. Follow its documentation policy; do not create ticket files, handoff documents or ADRs merely because another skill uses those defaults.

## Read the actual backlog and delivery state

Discover the configured tracker and account, using `linear` when appropriate. This works in Codex, Claude Code, OpenCode, Cursor or another host: use native tools and the available skill mechanism. Do not assume provider names, credentials, personal paths or a particular tracker schema. If access is missing, state the limitation and provide a proposed rebalance without claiming it was applied.

Fetch every page of open items for the selected project, including backlog, in-progress, blocked and review states. Read priorities, descriptions, acceptance criteria, owners, labels and blocking relationships. Read relevant comments and linked PRs for goal-critical, currently urgent, contradictory or unclear items. Follow dependencies outside the project to understand them, but do not reprioritize another project's backlog without authorization. A partial page or failed lookup is not the whole backlog; report incomplete coverage and do not make bulk conclusions from it.

Check whether apparently open work is already delivered using its acceptance criteria and the relevant code, release, query or running product. Concentrate deeper checks on the goal-critical path and status corrections; this is not a whole-codebase audit. Record evidence and reconcile stale status under the project's rules. A merged PR alone does not establish deployment or completed operational evidence. Keep unresolved acceptance criteria open, and do not promote already delivered work merely because its ticket is stale. An unverifiable item remains explicitly unverified.

When useful, delegate independent read-only groups of items to native parallel agents: Luna for bounded status checks, Terra for code and dependency tracing, Sol for scope or conflicting evidence, or the host's equivalents. Use only supported models and tools. Keep tracker writes with one coordinator to avoid overlapping edits. For a small backlog, work directly. Apply `plimsoll` when available: bounded investigation, no repeated audit or polling loop.

## Establish what the goal actually requires

Trace the smallest complete user journey that demonstrates the goal and map its acceptance to existing items. Include implementation, integration, deployment, data and verification prerequisites when they are actually required. Similar titles or shared components do not prove a dependency. Read the owning code or delivery evidence when necessary to establish the relationship.

Reuse existing items and native blocking links. Create a missing item only when a concrete part of the goal has no owner in the backlog; search for duplicates first. Each item should state the observed gap, intended behaviour, relevant evidence, testable acceptance and dependencies, so a fresh agent can deliver it. Split only when independent end-to-end increments improve delivery; do not manufacture a ticket per technical layer. Check the resulting dependency graph for cycles and mistaken blockers.

Distinguish urgency from readiness. A necessary external decision, unavailable credential, observation period or another owner's active work can be urgent while still blocked. Record the actual dependency and the project's readiness role; never mark it ready just to make `next` select it. Preserve assignees and ongoing ownership. If the deadline is not achievable, say what prevents it and identify a smaller demonstrable outcome without silently changing the user's goal.

## Apply the rebalance

Invocation authorizes priority changes within the selected project, necessary spec improvements, missing goal-related items, dependency links and evidenced status reconciliation. Do not ask for another confirmation merely because these are tracker writes. A request for advice or a preview alone does not authorize mutations.

Use the user's explicit priority rules first, otherwise map these meanings to the tracker's native values:

- **Urgent:** unfinished work indispensable to the stated goal and its necessary blockers, plus independently urgent incidents or commitments that still warrant immediate attention.
- **High:** valuable near-term work that supports the goal but is not required to demonstrate it, or another important current commitment.
- **Normal:** useful work outside the immediate delivery path.
- **Low:** optional polish or minor improvements that can wait.

Reassess existing urgent items as well as promoting new ones. Demote stale urgency when its reason no longer applies. Do not preserve an old priority solely because it is already set, or demote an active severe incident simply because it is unrelated to the goal. Missing information is not evidence that something is unimportant; clarify material uncertainty and retain the current priority where there is no defensible basis to change it.

Apply only necessary changes. Add a brief rationale tied to the goal or current impact on changed items, and put shared goal context in an existing owning item or project when available. Avoid creating an administrative parent item just to record the rebalance. Re-read affected fields before writing when concurrent edits are possible; preserve unrelated labels, descriptions, owners and fresh decisions. Use native blocking relationships and existing readiness roles. Do not assign work or move it to In Progress simply because it became urgent.

Verify the written priorities, statuses and dependency links from tracker responses or a focused readback. After an uncertain write result, reconcile the item's live state before retrying. Report partial application accurately. Do not keep polling or rechecking settled items.

## Finish

Order the required work blockers-first; do not nominate a dependent item as ready while a necessary prerequisite remains unresolved or unverified. Preserve independently urgent incidents in that ordering.

Give a short plain-language report: the goal, how many items changed, the linked urgent delivery order, and any blocked or unverified part of it. Name the first actionable item for `next`, or explain why none is ready. Link changed items compactly rather than dumping the backlog. Use `deslop` when available to tighten the message.

Stop after the rebalance. The new priorities stand until the user changes them again; no automatic restoration and no implementation in this invocation.
