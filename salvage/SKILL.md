---
name: salvage
description: "Resolve git conflicts when a merge, rebase, cherry-pick, revert or stash apply or pop reports CONFLICT or leaves conflict markers, including mid-task. Rescue stranded work in detached HEADs, worktrees, unpushed branches and stashes; remove only copies proven merged and pushed. Not for status recovery (`muster`)."
---

# Salvage

No one's work is lost in git. Two jobs:

- **A merge, rebase, cherry-pick, revert or stash apply stopped on conflicts**, or the tree has conflict markers: read [references/conflicts.md](references/conflicts.md) and follow it.
- **Work may be stranded, or branches, worktrees or stashes need cleaning up:** follow the rest of this file.

## Rules

- **Never destroy the only copy.** Rescue first, delete last. Record every SHA before changing anything, and copy uncommitted work somewhere private; a SHA preserves only commits.
- **Don't abort, reset or force-push your way out of trouble.** `--abort`, `reset --hard`, `checkout .` and `checkout --conflict` discard work recorded nowhere; a force push can overwrite someone else's. Do them only when asked, or abort an operation you started by mistake before resolving anything.
- **Do git writes yourself, from where you stand.** Don't hand branch, worktree or stash changes to a helper; it cannot see who else is in the tree. Inside a worktree, don't run git against the shared checkout.
- **Push recovered work only when asked** or when standing policy covers it.

## What gets lost

Rescue in this order:

1. Uncommitted changes in a removed worktree. No reflog, no recovery.
2. A detached HEAD carrying commits. On no ref, so the next `gc` takes it.
3. Stash entries. One `git stash clear` from gone.
4. Unpushed commits. The reflog holds them about 90 days, on one machine.
5. A branch deleted while unmerged. Same window, and the name is gone.

## Three buckets

Every worktree, branch and stash lands in one. Anything you cannot place is in flight.

- **In flight.** Someone may be using it. Report it with the owner and touch nothing.
- **At risk.** Holds content that exists nowhere else. Rescue it, then re-sort.
- **Safe.** Every commit reachable from the pushed default branch, ignored content accounted for, nothing running in it. Only this bucket is removed.

## Steps

1. **Census, read-only.** One repo unless the user asked for more; propose a machine-wide sweep rather than widening mid-run. Run `python3 scripts/census.py <repo> --output <new-private-file>.json` (see Scripts). It covers worktrees, branches (upstream, ahead/behind, merged), stashes and unreachable reflog commits.
2. **Work out who owns what** (below), then sort into buckets and name every at-risk item.
3. **Rescue, additively.** No deletion and no overwriting an existing ref.
   - **Detached HEAD:** `git branch salvage/<name> <sha>`.
   - **Dirty worktree you own:** commit the selected files as WIP on a recovery branch. Leave credentials out.
   - **Stash:** don't use `git stash branch`; it can drop the stash and leave changes uncommitted. Instead: `git worktree add -b <recovery-branch> <path> <stash-sha>^1`, then `git stash apply --index <stash-sha>` there, commit, and check the staged and untracked files all came across. Leave the stash in the list.
4. **Remove only the safe bucket,** worktrees before their branches, recording each SHA as you go.
5. **Report** (below).

## Who owns a worktree

Your host's session list shows only your host. Absence from it says nothing about a Codex or Claude session elsewhere. The cross-host evidence is the filesystem: directory and index mtimes, `.git/worktrees/<name>/locked`, a process or dev server running inside the tree. Touched in the last day means occupied. If peers are reachable, ask them which paths they own; that beats inference. When unsure, leave it: a stale worktree costs disk, a deleted live one costs someone their afternoon.

## Ignored files

`git worktree remove` deletes ignored files even when `git status` is clean. Run `git ls-files --others --ignored --exclude-standard` in each checkout before calling it safe.

- **Regenerable** (`node_modules`, `.next`, `dist`) only when the inputs are preserved and nothing in them was edited by hand.
- **Unique:** `.env.local`, local databases, certificates, scratch work. Copy them privately and check the copy before removing the source.
- **Unclear:** keep the checkout and say what is unresolved.

## Naming what you found

An unnamed `salvage/` branch gets deleted next month by whoever tidies up. For each at-risk item, look up any ticket ID in the branch name and report its title and status; an open ticket means the work is still wanted. With no ticket, summarise the commits in one line ("three commits, adds the facet-filter timeout guard"). If the default branch has superseded it, cite the replacing commit.

## Proving "safe"

- **Test against the fresh remote, not local `main`.** Fetch without pruning, then `git merge-base --is-ancestor <tip> <remote>/<default>`. If the remote cannot be reached, nothing is removed.
- **Squash and rebase merges defeat ancestry,** and `git cherry` and patch-ids mislead too. Ask the forge for the merged PR's head and match it to the current branch tip; commits after that head are unmerged. If equivalence cannot be shown, keep the branch.
- **A pushed branch is a copy, not integration.** It can be deleted remotely. The bar is the pushed default branch.

## Scripts

Both take `--help`.

- [scripts/census.py](scripts/census.py) is read-only. `--output` must be a new file outside every scanned repo. `--ownership` takes `{"version": 1, "claims": [{"path": "/abs/path", ...}]}`; claims are evidence, not permission. `--exclude PATH` skips a protected path. A non-zero exit means the census is incomplete. Its output is coverage, not a safe-to-delete verdict.
- [scripts/integrate.py](scripts/integrate.py) publishes one exact commit, only when the push is authorised. `--intent integrate` fast-forwards the server's default branch; `--intent preserve --destination-ref <ref>` pushes a named feature or `refs/salvage/` ref, never the default (`--expected-old absent` for a new one). `--expected-old` is the remote SHA you observed. If the remote moved, inspect it; don't retry.

## Report

Lead with the number of items rescued, or say nothing was at risk.

- **Rescued:** what it was, where it lives now, the ticket or commit summary.
- **Removed:** the recorded SHA, so it can be put back.
- **Left alone:** the reason and owner. A long list is a good outcome.
- **Needs you:** one line and one question per unplaced item.
