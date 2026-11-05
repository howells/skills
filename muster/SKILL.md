---
name: muster
description: "Catch up on work across concurrent or older sessions: what's in flight, who owns it, what was decided, and a handoff when asked. Not for this task's status (`memento`), the last reply (`what`) or git conflicts and cleanup (`salvage`)."
---

# Muster

A roll-call of what is in flight right now, the state each thread is actually in, and the next move. Not a summary of what you did. For a forgotten project, recover its purpose, audience and intended outcome before the activity.

This earns a skill because of concurrency. The expensive mistake is two agents on one branch, or resuming a thread another session already merged, reverted or abandoned. **Say who owns what, and stay out of a peer's tree.**

## The record

No source is authoritative alone. Transcripts hold what was decided and why, and go stale the moment another session pushes. Live git and PRs hold what is true of the code. Peer sessions hold work that exists nowhere else yet. The tracker holds what people believe. A transcript is history and a ticket is a claim; only git and running sessions are current.

## Steps

1. **Scope.** "Recent" defaults to seven days; the workspace defaults to the active one. Don't read another project's transcripts unasked, and don't quietly narrow "everything" to "the last few".
2. **Live sessions first.** Use the harness's session, task and agent tools. In Codex, the task list and this task's agent list are separate; neither is a census of the other. An unavailable API is not evidence that nobody is working; record it as a gap.
3. **History.** Prefer the harness's task-history tools, archived tasks included when in scope. Claude transcripts live under `~/.claude/projects/`, where `/Users/me/app` usually maps to `-Users-me-app`; check the directory exists. Codex keeps `sessions/` and `archived_sessions/` under its home; match the recorded workspace before reading. **Order by timestamp, never filename**: UUIDs aren't chronological. Search the topic first. Skip subagent history unless asked; "all transcripts" includes children. In T3 Code, read [references/t3-history.md](references/t3-history.md) first.
4. **Verify against live state.** Check every branch, PR and ticket the history surfaced with `git log`, `git status`, `gh pr view`. Ancestry proves an ordinary merge, but a negative ancestry or patch-id result can't disprove a squash merge: compare the merged PR's recorded head with the branch tip and inspect later commits separately. A pushed branch is a backup, not proof of integration; a done ticket proves only that someone said so.
5. **Named target.** For a feature, file or bug, search the tracker and repo history in parallel with step 3: current state, what was tried and didn't hold, what's still reported.

## Output

Lead with where things stand; when it outgrows a screen, cut detail before threads.

- **Capsule.** Up to five bullets: what this work is and where it stands.
- **Threads.** One line each, with exactly one tag: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[owned by <session>]`, `[verified, uncommitted]`, `[reverted #N]`, `[blocked <on what>]`, `[planned, not started]`, `[completed <evidence>]`, `[unverified <why>]`. Never invent a status to fill the format.
- **Problems.** Up to five recurring ones, including anything shipped then reverted, so the next attempt starts where the last one failed.
- **Next move.** One action, not a menu.

Cite transcript findings by session ID and everything else by artefact: PR number, ticket ID, branch, permalink.

### Handoff

When asked for one, write it in chat: purpose and outcome, settled decisions and rejected approaches, live code and tracker state, the current writer and checkout owner, authorized side effects and limits, coverage gaps, then the next action. Separate proposals from decisions and done from intended. Link the owning tracker item; don't write a local handoff file.

Anything the next task depends on that lives only in temporary storage (briefs, datasets, evidence) needs a durable home and exact location before you hand off: a pinned commit, an authorized tracker attachment, or private task storage. Carry each unanswered question's exact text and status; a restart, timeout or unrelated message is not an answer.
