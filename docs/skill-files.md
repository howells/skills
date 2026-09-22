# Where a skill's files live

The installer copies one skill at a time, so an installed skill has to stand alone. Every file a skill references sits inside its own directory.

A file two skills need is copied into both, and the duplication is deliberate. There is no shared source layer: one existed while five design references served two skills, and it was removed once `chiaroscuro` became their only consumer. See `adr/0004`. Reintroduce a source layer only when the copies are numerous enough that keeping them in step by hand is the thing going wrong.

`linear/scripts/read-credential.py` and `web-research/scripts/read-credential.py` are deliberate identical copies so each skill installs alone. Keep them in step; `scripts/test-skill-helpers.py` checks parity.

## Keeping a skill portable

- No personal names, account inventories, private repository dependencies, machine-specific home paths or secret-store identifiers. Use configured tooling and generic examples. Public tool documentation and distribution URLs may name their actual owners.
- Each `SKILL.md` must be usable by a fresh agent, with no hidden dependency on a local file the body doesn't link.
- Don't broaden a skill unless its trigger and output stay clear, and keep repo-specific product assumptions out.
- Search related skills before broadening scope. The overlap hotspots are `chiaroscuro`, `maquette`, `armature`, `reflow`, `componentize` and `typecase` (UI design, page directions, app shells, screen sizes, componentisation, the type ramp); also check `fieldtest` and `mastraudit`. `what`, `memento` and `muster` all report state: `what` decodes the last message and actions, `memento` is this session's task now, `muster` sweeps many sessions.
- Search the target skill directory before editing shared README text, and verify current installer CLI examples before changing install docs.
- Don't copy these skills into product repos; install or invoke them from the agent environment.

## Removal

Removing or renaming a skill does not update existing installs - the installer copies files and doesn't track deletions. Note the removal in `README.md`, then uninstall the stale copy from the local and global install locations by hand.
