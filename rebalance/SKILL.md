---
name: rebalance
description: "Reprioritize a project's backlog around a goal or deadline, and flag goal work too thin to build. Not for doing the work."
---

# Rebalance

Re-set a project's priorities around the user's goal: make the goal's essential delivery path Urgent and reassess everything else on current importance.

- **Scope.** Take the named project, or infer it from the repo and conversation. Take the goal and any deadline in ordinary words ("the guided design flow for tomorrow's demo"); resolve relative dates in the user's timezone. Never invent a deadline. Ask only when the target or a scope-changing decision can't be found from evidence.
- **Authority.** A request to reprioritise authorizes tracker writes within the project: priorities, spec improvements, missing goal items, blocking links and evidenced status fixes. A request for advice or a preview does not. Leave other projects' priorities alone.
- **Stop before code.** No implementation, no new delivery task. Specs and dependencies go in the tracker; no ticket files or handoff docs.

## 1. Read the real backlog

- Fetch every page of open items in every open state: backlog, in progress, blocked, review. A failed or partial fetch is not the whole backlog; say what's missing rather than concluding from it.
- Read comments and linked PRs for goal-critical, already-urgent, contradictory or unclear items.
- For goal-path items and any item with a merged PR, check whether it is already delivered, against its acceptance criteria and the code, release or running product. A merged PR doesn't prove it's deployed. Fix stale status with evidence; mark what you can't verify as unverified.
- For a large backlog, split read-only checks across parallel agents and keep tracker writes with one coordinator.

## 2. Flag work that can't be built yet

Check that tickets exist for the goal and say enough for a fresh agent to build them: problem, intended behaviour, testable acceptance, dependencies. Judge from descriptions, comments and linked specs, not titles.

- **None:** say "I couldn't find any tickets covering this goal" and what you searched. Offer to settle the open decisions, or to write the spec and tickets if the goal is clear (`grilling`, `to-spec`, `to-tickets` where installed). Then stop; don't reshuffle unrelated work or invent a backlog unless asked.
- **Too thin:** link them, name the missing decisions or acceptance criteria, and make the same offer. Don't invent requirements or mark them ready.
- **Some ready:** rebalance those and name the part of the goal still unspecified. An essential thin item can be Urgent with the project's needs-info state; urgency doesn't make it actionable.

Make the offer one concrete question; don't start the interview.

## 3. Map the goal

Trace the smallest complete user journey that demonstrates the goal, including the deployment, data and verification prerequisites it really needs. Shared titles or components don't prove a dependency. Reuse items and native blocking links. Create an item only when part of the goal has no owner, after searching for duplicates; one end-to-end increment beats a ticket per layer.

Urgency isn't readiness. Work waiting on an outside decision, credential or another owner can be Urgent and still blocked; record the blocker and never mark it ready to get it picked. Keep assignees. If the deadline can't be met, say why and propose a smaller demonstrable outcome rather than quietly changing the goal.

## 4. Set priorities

Use the user's own rules first; otherwise map to the tracker's native values:

- **Urgent:** indispensable to the goal, its blockers, and incidents or commitments that still need immediate attention.
- **High:** supports the goal without being required, or another important current commitment.
- **Normal:** useful, off the delivery path.
- **Low:** polish that can wait.

Reassess existing Urgent items too: demote stale urgency, but not a live severe incident just because it's off-goal. Missing information isn't evidence of low importance; keep the current priority when there's no basis to change it. Give the rationale for each change in the report. Don't create a parent item to record the rebalance, assign work, or move it to In Progress because it became urgent.

## 5. Report

Project, goal and deadline; how many items changed, with a one-line reason each; the urgent delivery order, blockers first, linked; anything blocked or unverified; the first actionable item, or why none is ready; any spec gap with its one-question offer. Then stop.
