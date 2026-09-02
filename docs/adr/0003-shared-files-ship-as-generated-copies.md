# 3. Shared files ship as generated copies

Date: 2026-08-24
Status: Superseded by [0004](0004-the-shared-source-layer-is-removed.md)

## Context

Five reference files are needed by more than one skill. The obvious problem with the arrangement is what a reader sees first: the same file sitting in both consuming skill directories, which looks like someone forgot to factor it out. It's a fair reading, and it's wrong.

The reason it's wrong is how these skills get installed. `npx skills` installs one skill at a time. An installed skill lands on its own, with no siblings alongside it and nothing to reach across to. If a skill's reference lives anywhere other than inside that skill, the install is broken the moment it happens.

That rules out the two tidy answers. A shared package needs something to resolve it, and a single-skill install has nothing. Symlinks need a target, and the target isn't there either. Both work in the repo and both fail at the only moment that matters.

This decision was taken some time ago and has held since. It's being written down now because it never was, and every reader arriving at those generated copies has had to work it out again from scratch.

## Decision

`shared/` holds the single source of each of the five files. `scripts/sync-shared.py` materialises a real copy into each consuming skill's own `references/`. Every copy opens with a comment saying not to edit it.

The duplication is deliberate and load-bearing.

### 2026-09-02 supersession

`foundry` was removed, leaving `chiaroscuro` as the only consumer of all five files, and a source layer with one consumer shares nothing. `shared/` and `scripts/sync-shared.py` are gone; the files live in `chiaroscuro/references/` and are edited in place. See [0004](0004-the-shared-source-layer-is-removed.md).

The reasoning below still governs how a reference is placed: a skill installs alone, so every file it reads sits inside it, and a file two skills need is copied into both. Only the machinery for keeping copies in step is retired.

### 2026-08-27 amendment

Brand identity became a Foundry-local reference when Chiaroscuro's identity scope moved fully to Foundry. The shared set therefore contains five sources rather than six; the installation and generated-copy decision is unchanged.

## Consequences

A skill stands alone. Install one, and everything it references is present.

The cost is that the tree contains five files in both consuming skill directories, and a copy edited in place will look like it worked. `check-skills.py` fails when a copy has drifted from its source, so that mistake is caught at the gate rather than silently kept - it's the thing making this arrangement safe rather than merely convenient, and the arrangement stops being safe if that check is ever weakened.

Watch for a shared source that links to a path existing in only one skill. It resolves in the skill you were thinking of and breaks in every other. Name the topic in the shared file and let each skill's own `SKILL.md` carry the pointer.

Watch too for content that belongs to one skill being folded into a shared file to save a copy. That's how these files drifted apart the first time.
