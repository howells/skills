---
name: muster
description: "Rebuild working context across concurrent or older agent tasks from transcripts, git state, peer sessions, and the tracker. Use for 'catch me up', 'where did I leave off', or 'what is in flight', returning every active thread and its next move. For evidence-backed investigation use `inquest`."
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

Copy these steps into your todolist verbatim before you reason about the task. A step you skip stays in the list with a one-line `skip: <reason>`.

1. **Lock the scope and say it back.** The window - "recent" is a real range, default seven days. The topic, if one was named. The workspace, default the active one. Never read another project's transcripts unasked, and never quietly narrow "everything" to "the last few".

2. **Take the roll of live sessions first.** `ListAgents` before any reading. A busy peer session on your repo changes what you are allowed to touch and outranks anything a transcript says. Note which paths each session owns, and treat those as another agent's until it says otherwise.

3. **Fan out over the transcripts.** They live at `~/.claude/projects/<encoded-cwd>/<uuid>.jsonl`, where `<encoded-cwd>` is the workspace path with the leading slash dropped and every `/` turned into `-`. Order candidates by modification time (`ls -t`) and never by filename - the UUIDs carry no chronology. Spawn parallel subagents on a cheap model, one per slice; this is grunt work. Tell each to grep for the topic first and read only the matching regions, to skip subagent and eval transcripts, and to return one block per session: goal, decisions, open threads, corrections, and artefacts (branch, PR, ticket), each citing its UUID. Raw transcripts stay in the subagents. Only findings come back. For one or two candidates, read them directly and skip the fan-out.

4. **Verify every claim against live state.** Take each branch, PR and ticket the mining surfaced and check it: `git log`, `git status`, `gh pr view`. Merge detection is where this goes wrong - in a squash-merging repo, `git cherry` and patch-ids lie. Use ancestry or the PR's own state. A pushed branch with no PR is not a backup, and a ticket marked done proves only that someone said so.

5. **Sweep the shared record when a named target is involved.** A feature, file, subsystem or bug carries history your own transcripts never saw. Hand it to `inquest`, steering the question from "why is it like this" to "what is the current state, what was tried and did not hold, what is still being reported". Run it in parallel with step 3. Skip only for pure activity recall with no named target.

6. **Write the brief to the contract below.**

## Output contract

Lead with where things stand, then the roll, then what is going wrong, then the one next move. When it outgrows a screen, cut detail before you cut threads.

- **Capsule.** At most five bullets. What this body of work is and where it stands.
- **Threads.** One line each, and every line carries exactly one status tag: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[owned by <session>]`, `[verified, uncommitted]`, `[reverted #N]`, `[blocked <on what>]`, `[planned, not started]`. An untagged thread is an unchecked thread.
- **Problems.** At most five, and only the recurring ones. Include anything that shipped and was reverted, so the next attempt starts where the last one failed rather than repeating it.
- **Next move.** One concrete action. Not a menu.

Cite transcript findings by UUID and everything else by its artefact - PR number, ticket ID, branch, permalink. Write the brief through `deslop`.

## Failure modes

- **Trusting the transcript over the repo.** The transcript says it landed; `git log` says whether it did.
- **Reading transcripts in filename order.** UUIDs are not chronological, and the newest session is the one that matters.
- **Reporting a thread with no status tag.** That is the whole product. An untagged line means you did not check.
- **Silently working in a peer session's tree.** Say who owns what, and stay out.
- **Widening past the scope you stated.** Adjacent work stays out unless it blocks something in scope.
