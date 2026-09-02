# 4. The shared source layer is removed

Date: 2026-09-02
Status: Accepted

Supersedes [0003](0003-shared-files-ship-as-generated-copies.md).

## Context

ADR 0003 set up `shared/` as the single source for five design references, with `scripts/sync-shared.py` materialising a real copy into each consuming skill and `check-skills.py` failing when a copy drifted. Two skills consumed them: `chiaroscuro` and `foundry`.

`foundry` was removed on 2026-09-02, having never been invoked once in either Claude Code or Codex in the three and a half months since it was added. That left `chiaroscuro` as the only consumer of all five files.

A source layer with one consumer shares nothing. The five files in `shared/` and the five in `chiaroscuro/references/` were byte-identical apart from a header telling the reader not to edit the copy in front of them, and every edit meant touching the source, running the script, and committing both. The gate that made the arrangement safe was checking a copy against a source that only one skill would ever read.

## Decision

`shared/` and `scripts/sync-shared.py` are removed. The five files live in `chiaroscuro/references/`, where the only skill that reads them keeps them, and are edited in place. The generated-copy headers are gone, along with the shared-sources check in `check-skills.py` and the generated-copy exclusion in `check-vocabulary.py`.

**0003's reasoning is unchanged and still governs.** `npx skills` installs one skill at a time, an installed skill has no siblings to reach across to, and so every file a skill references sits inside its own directory. That is why a package or a symlink is still the wrong answer, and why a reference needed by two skills is copied into both rather than factored out.

What is removed is the machinery for keeping several copies in step, because there are no longer several copies.

## Consequences

Editing one of the five files is now one edit to one file, and the vocabulary gate reads it at its real path rather than through the source it was copied from.

If a second skill needs one of these files again, copy it. Note both copies in `AGENTS.md`, and keep 0003's two warnings, which outlive the machinery they were written for: a shared file must not link to a path that exists in only one skill, and content belonging to one skill must not be folded into a file another skill reads.

Reintroduce a source layer only when the copies are numerous enough that keeping them in step by hand is the thing going wrong. Two copies of one file is not that.

The cost is that a future second consumer starts from a copy rather than from a source, and nothing fails if the two then diverge. That is the trade 0003 was avoiding, and it is worth taking while the count is one.
