---
name: salvage
description: "Rescue work that exists in only one place - detached HEADs, worktrees, unpushed branches, or stashes - then remove only what is proven merged and pushed. Use for repository cleanup where ambiguous work must be preserved and each surviving thread named. For status reconstruction without cleanup use `muster`."
---

# Salvage

Salvage is recovery first and disposal second. The job is to find work that exists in exactly one place, get it somewhere safe, and only then clear away what is provably redundant.

Run it in that order or not at all. A cleanup that deletes before it rescues is how a week of work disappears, and the reflog does not cover the two worst cases: uncommitted changes in a worktree you remove, and a branch whose commits were never pushed anywhere.

## What actually gets lost

Worst first. This ordering is your rescue order when time is short.

1. **Uncommitted changes in a removed worktree.** Nothing records them. No reflog, no recovery.
2. **A detached HEAD carrying commits.** Reachable from no ref, so the next `gc` takes it.
3. **Stash entries.** Reachable but invisible, and one mistyped `git stash clear` from gone.
4. **Unpushed commits.** Reflog holds them ~90 days, on one machine.
5. **A branch deleted while unmerged.** Same window, but nobody looks - the name is gone too.

## Three buckets

Every worktree, branch and stash lands in exactly one. Anything you cannot place goes in the first bucket, not the last.

**In flight.** Someone is using it right now. Report it, name who, and touch nothing.

**At risk.** Holds content that exists nowhere else. Rescue it, then re-classify.

**Safe.** Provably redundant: every commit reachable from a pushed default branch, working tree clean, nothing running. Only this bucket is eligible for removal.

## Judging "in flight" across agent hosts

This is the part that goes wrong. Worktrees on a shared machine belong to whichever agent made them, and you cannot see the others.

- **Your host's session list only shows your host's sessions.** In Claude Code, `ListAgents` says nothing about a Codex session, and vice versa. Absence from your own roll-call is not evidence of abandonment - it is no information at all.
- **Filesystem and process evidence is the only cross-host signal.** Directory and index mtime, a lock in `.git/worktrees/<name>/locked`, a process whose working directory sits inside the tree, a dev server on a port served from it.
- **Recent means live.** A tree touched inside the last day is presumed occupied.
- **Ask before assuming.** If peer agents are reachable, ask which paths they own. That beats every inference above.
- **Default to leaving it.** A stale worktree costs disk; a deleted live one costs someone their afternoon.

## Naming what you found

A rescued branch nobody can identify gets deleted next month by whoever is tidying up. Naming it is what makes the rescue stick, so do this for every at-risk item before reporting it.

- **Read the branch name for a ticket ID.** `feat/mg-1168-channel` carries `MG-1168`. Look it up in whatever tracker the session can reach and report the title and status beside the branch.
- **The ticket's state is evidence about the branch's state.** An open ticket says the work is still wanted, whatever the timestamps suggest; a closed one with the branch merged is the strongest safe-to-remove signal there is.
- **No ticket means read the commits.** Subjects and diffstat, one line: "three commits, adds the facet-filter timeout guard."
- **Say what it is not.** Work superseded by something already on the default branch is the finding, not a footnote - cite the commit that replaced it.

## Proving "safe"

Merge detection is where confident wrong answers come from.

- **Ancestry is the honest test.** `git merge-base --is-ancestor <branch> <default>`.
- **Squash and rebase merges defeat it.** The commits genuinely are not ancestors, so ancestry reports unmerged and `git cherry` and patch-ids both lie. Fall back to the forge: a PR the forge calls merged is merged.
- **A pushed branch is not a backup.** It is safe from local loss, not from someone deleting the remote branch. Pushed plus merged is the bar.
- **Record every SHA before you delete anything.** Branch tip, worktree HEAD, stash commit. Written down, a deletion is reversible; unwritten, you are relying on someone thinking to check the reflog.

## Steps

Copy these steps into your todolist verbatim before you start. A step you skip stays in the list with a one-line `skip: <reason>`.

1. **Fix the scope and say it back.** One repo by default. A sweep of every repo on the machine is a different job with a much larger blast radius, and it needs saying out loud before it starts.

2. **Do the whole census before touching anything.** Worktrees with branch, detached state, dirty count and age. Branches with upstream, ahead/behind and merge status. Stashes with age and origin branch. Commits in the reflog reachable from no ref. Read-only, no exceptions.

3. **Take the roll of live sessions and processes.** Your own host's sessions, then the cross-host evidence above. Write down which paths are spoken for before any classification.

4. **Sort into the three buckets, and name every at-risk item** per the section above. Unplaceable goes to in-flight.

5. **Rescue, additively.** A detached HEAD becomes `git branch salvage/<name> <sha>`. A dirty worktree gets a WIP commit on a `salvage/` branch - an ugly commit beats a lost file. An unpushed branch gets pushed. A stash becomes a branch with `git stash branch`. Nothing is deleted in this step, and no rescue may overwrite an existing ref.

6. **Re-verify, then remove only from the safe bucket.** Re-run the check that put each item there, because step 5 changed the repo. Then remove, worktrees before their branches, recording each SHA first.

7. **Report to the contract below.**

Do every git operation yourself. Branch, worktree and stash work is never delegated to a subagent: the state is shared and mutable, a subagent cannot see who else is in the tree, and a wrong move is unrecoverable. Reading and tracker lookups can be delegated freely.

If you are working inside a worktree, stay in it. Running git against the shared checkout from a worktree session mutates a repo another session is standing in.

## Output contract

- **Rescued.** One line each: what it was, where it now lives, and the ticket or commit summary that identifies it. This is the part worth reading.
- **Removed.** One line each with the recorded SHA, so any of it can be put back.
- **Left alone.** One line each with the reason and the owner where known. A long list here is a good outcome, not a failure.
- **Needs you.** Anything that could not be placed. One line, one question each.

Lead with the count of rescued items. If nothing was at risk, say that in one line and stop.

## Failure modes

- **Deleting before rescuing.** The entire point. Rescue is additive and reversible; deletion is neither.
- **Reading absence from your own session list as abandonment.** It only ever means the other host is invisible to you.
- **Trusting ancestry in a squash-merging repo.** Ask the forge.
- **Rescuing anonymously.** An unnamed `salvage/` branch is a deferred deletion, not a save.
- **Widening from one repo to the machine mid-run.** Finish the stated scope and propose the sweep separately.
