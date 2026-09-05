---
name: muster
description: "Rebuild context across concurrent or older tasks from transcripts, git, peer sessions and the tracker. Use for catch-ups and in-flight inventories. Not for one current task (`memento`), rewriting the last reply (`what`), or repository cleanup (`salvage`)."
---

# Muster

A muster is a roll-call: every hand named, present or absent. That is the job here. It lists what is in flight right now, the state each thread is actually in, and what to do next. It is not a summary of what you did.

Use it for "catch me up", "where did I leave off", "what is running", or before picking up work you started somewhere else.

The reason this earns a skill is concurrency. When several sessions run against the same repos, the expensive mistake is two agents standing on the same branch, or resuming a thread another session already merged, reverted or abandoned. Forgetting what you did is cheap next to that.

## What counts as the record

Four sources, and no one of them is authoritative on its own.

- **Your transcripts** hold what was decided and why. They go stale the moment another session pushes.
- **Live git and PR state** holds what is actually true of the code right now.
- **Peer sessions** hold work in progress that exists nowhere else yet.
- **The tracker** holds what other people believe the state to be.

A transcript is history. A ticket is a claim. Only git and the running sessions are current.

## Steps

Use these steps to organize the roll-call. Keep any task list brief and record coverage gaps; do not copy the workflow verbatim.

1. **Lock the scope and say it back.** The window - "recent" is a real range, default seven days. The topic, if one was named. The workspace, default the active one. Never read another project's transcripts unasked, and never quietly narrow "everything" to "the last few".

2. **Take the roll of live sessions first.** Discover the current harness and its session/task APIs. In Codex, use the available task-list/read tools for user tasks and agent-list tools for this task's subagents; neither is automatically a census of the other. Use Claude's session tools when available. Record which harnesses are covered and which are unavailable. A busy peer's ownership changes what you may touch; an absent API is not evidence that nobody is working.

3. **Read the available history.** Prefer the harness's task-history APIs, including archived tasks when in scope. For Claude filesystem history, discover the matching directory under `~/.claude/projects/`; a path such as `/Users/name/Sites/repo` commonly maps to `-Users-name-Sites-repo`, including the leading hyphen. Verify the directory instead of relying on an encoding guess. For Codex, prefer task-history tools; if unavailable, inspect scoped session metadata under its configured home in `sessions/` and `archived_sessions/` and match the recorded workspace before reading content. Order candidates by activity timestamps or modification time, not filename. Search the topic first and read matching regions; skip subagent and eval history unless requested. For many candidates, delegate bounded independent slices when useful; for one or two, read directly. Return goal, decisions, corrections, unfinished work and artefacts with task/session identifiers. Report empty and unavailable sources separately.

4. **Verify every claim against live state.** Take each branch, PR and ticket the mining surfaced and check it: `git log`, `git status`, `gh pr view`. For ordinary merges, ancestry can prove integration. A negative ancestry or patch-id result cannot disprove a squash merge. Use the merged PR’s recorded head and destination, compare that head with the current branch tip, and inspect later commits separately. PR state alone does not prove post-merge branch work landed; an empty three-dot diff is not a substitute for this check. A pushed branch is an off-machine copy, but does not prove integration or completion, and a ticket marked done proves only that someone said so.

5. **Sweep the shared record when a named target is involved.** A feature, file, subsystem or bug carries history your own transcripts never saw. Search the tracker and the repo history for it, asking what the current state is, what was tried and did not hold, and what is still being reported. Run it in parallel with step 3. Skip only for pure activity recall with no named target.

6. **Write the brief to the contract below.**

## Output contract

Lead with where things stand, then the roll, then what is going wrong, then the one next move. When it outgrows a screen, cut detail before you cut threads.

- **Capsule.** At most five bullets. What this body of work is and where it stands.
- **Threads.** One line each, and every line carries exactly one status tag: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[owned by <session>]`, `[verified, uncommitted]`, `[reverted #N]`, `[blocked <on what>]`, `[planned, not started]`, `[completed <evidence>]`, `[unverified <why>]`. Use unverified when the source is unavailable; never invent a status to fill the format.
- **Problems.** At most five, and only the recurring ones. Include anything that shipped and was reverted, so the next attempt starts where the last one failed rather than repeating it.
- **Next move.** One concrete action. Not a menu.

Cite transcript findings by UUID and everything else by its artefact - PR number, ticket ID, branch, permalink. Write plainly and remove filler; use `deslop` for a deeper wording pass when available and useful.

## Failure modes

- **Trusting the transcript over the repo.** The transcript says it landed; `git log` says whether it did.
- **Reading transcripts in filename order.** UUIDs are not chronological, and the newest session is the one that matters.
- **Reporting a thread with no status tag.** That is the whole product. Use an explicit unverified tag when a check cannot be completed.
- **Silently working in a peer session's tree.** Say who owns what, and stay out.
- **Widening past the scope you stated.** Adjacent work stays out unless it blocks something in scope.
