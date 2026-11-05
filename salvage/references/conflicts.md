# Resolving conflicts

For a merge, rebase, cherry-pick, revert or stash apply or pop that stopped on conflicts. The goal: both sides' intent survives, nothing silently dropped.

## Rules

- **Copy before anything that rewrites the tree, index or operation:** `checkout --conflict`, `--ours`/`--theirs`, `--abort`, `reset`, `stash drop`. Copy conflicted and already-resolved paths outside the checkout; SHAs don't hold a resolution in progress. `git checkout --conflict=diff3 -- <file>` recreates the markers over your edits and unstages the file.
- **Abort only when asked,** or when you started the operation by mistake and resolved nothing. `git rebase --abort` discards every commit already replayed. A stash conflict has no abort: `git reset --merge` undoes the apply and the stash stays listed.
- **Force-push only when asked,** as `git push --force-with-lease=<branch>:<recorded-remote-sha> <remote> <branch>`, never to the default branch. If the lease fails, someone pushed: fetch and integrate; don't retry with a new SHA.

## Before resolving

1. **Find the operation and record the commits.** `git status`, then `git rev-parse --git-path <name>` for `MERGE_HEAD`, `REBASE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD` or `rebase-merge`; in a linked worktree `.git` is a file, so literal `.git/...` paths fail. In a rebase also record `rebase-merge/orig-head` and `rebase-merge/onto` for the range check. For a stash, record its full SHA from `git stash list --format='%H %gd %gs'`; the list is shared, so positions move.
2. **Get `ours` and `theirs` right.** Merge, cherry-pick, revert: `ours` is `HEAD`, the branch you are on. Rebase: inverted, `ours` is the branch being built on and `theirs` is your commit being replayed. Stash: `ours` is "Updated upstream", `theirs` is "Stashed changes".
3. **Check rerere.** It may already have rewritten files and, with `rerere.autoUpdate=true`, staged them, so they no longer show in `git ls-files -u`. Read `git diff --cached` as well as `git diff`.

## Resolve each file

1. **Find why each side changed:** the commit messages, then the PR or ticket they cite. A hunk resolved without its intent is a guess.
2. **Read the base:** `git show :1:<file>` (base), `:2:` (ours), `:3:` (theirs). A missing stage means that side added or deleted the path.
3. **Combine the intents.** If both can hold, keep both. If not, follow the operation's goal and say what the other side loses. Write no behaviour neither side asked for.

If one side's intent cannot be established, ask one question naming both commits.

## Special cases

- **Modify/delete.** Find whether the deleting side removed the content or moved it: `git diff --name-status -M <merge-base> <deleting-side>`; a heavily edited move shows only as an added file. If moved, apply the edit at the new path and `git rm` the old one.
- **Lockfiles.** Don't hand-merge. Check each side for deliberate lock-only changes (`git log <merge-base>..<side> -- <lockfile>`): a pinned transitive, a security bump. If none, resolve the manifest and regenerate. If some, start from one side's lockfile, reapply the other's change, and install with the frozen flag.
- **Long rebases.** The same hunk can conflict commit after commit. Resolve each commit on its own terms; a final-state resolution in an early commit may not compile.
- **Stash drop** takes `stash@{n}`, not a SHA: find the entry matching your recorded SHA, and drop only after the result is committed.
- **Submodule pointers.** Pick the commit containing both sides' work, not the newest.

## Finish

1. **Account for every change.** Merge: compare each side's diff from the merge base with the resolved result. Rebase, cherry-pick, revert: compare `git show <source-sha>` with `git diff --cached HEAD`. Include rerere's reuses and files git merged on its own. Every change survives or has a stated reason.
2. **Run the project's typecheck and tests,** and fix what the merge broke, then continue the operation.
3. **After a rebase,** `git range-diff <onto> <orig-head> HEAD`. Every changed commit should be a resolution you made.

## Report

```
Resolved 3 conflicts in the rebase of feat/search onto main (tip abc1234).
- src/search.ts: kept both the timeout guard and the new facet filter.
- pnpm-lock.yaml: regenerated; neither side had lock-only changes.
- src/api.ts: took main's rename; moved the feature's edit into src/http.ts.
Checks: typecheck, tests pass. Not run: e2e.
```
