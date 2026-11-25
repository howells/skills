---
name: unslop
description: "Strip machine-written tells from a diff without changing behaviour: narrating comments, one-caller wrappers, impossible guards, decorative logs, leftover scaffolding. Not for structural review (`fettle`), fallback removal (`failfast`) or prose (`deslop`)."
---

# Unslop

Agent-written code works, but it carries ceremony a model added to look thorough, and the next reader pays for it. Take the ceremony out; leave behaviour exactly as it was.

- **Nothing here changes behaviour.** If removing a tell would change what the program does, report it and name the owner: a fallback that hides a failure, a mock, stub or test hook in production code, or a test that only asserts on its mock is `failfast`; a file or module to split is `componentize`; a correctness bug is simply reported.
- **Read the neighbourhood first.** A one-caller wrapper can name a real operation or hold a deliberate boundary; local convention wins. Make the smallest edit that removes the noise, keep code readable rather than compressing it into dense one-liners, and don't restyle the code around it.
- **The scope is the diff:** the branch against its merge base, or the working tree. Revert unrequested reformatting, docstrings, types or comments added to untouched lines; sweep the whole repo only when asked.
- **Fresh eyes catch more.** The turn that wrote the diff defends its own choices; when available, run the scan in a fresh context or read-only subagent, then apply the accepted edits. Asked only to review, report by tell number without editing.
- **Output others read is a contract.** CLI output, error text and logs consumed by scripts, users or monitoring stay as they are unless their change was asked for. This protects output that existed before the diff; output the diff itself added is fair game for tells 14–16. Never update snapshots to make a cleanup pass.

## The tells

Cite by number so a reviewer sees the pattern, not just the instance.

**Comments and names**

Keep comments only for: license headers, non-obvious quirks forced by an external dependency or platform you cannot reshape, public API contracts, and issue or RFC links. A surprise in our own code or a `do not remove` constraint is a refactor or encoding target (type, test, lint) — report it rather than polishing a long justification into a shorter alibi.

1. **Narrating, banner, and stale comments.** `// loop over the users`, `// Phase 1: build the cards`, `// ===== Helpers =====`, or comments describing what the code used to do.
2. **Doc comments that restate the signature.** `@param userId - the user id`. Delete; if an export needs real hover help, that's `marginalia`.
3. **Commented-out alternatives.** Git has them.
4. **Generic or over-explicit names.** `data`, `result`, `value`, `item`, `handle*`, `*Helper`/`*Manager` where a domain noun fits, and `userDataObject`, `handleClickEventHandler`, `UserShape`. Say the noun.

**Ceremony**

5. **One-caller wrappers** that add nothing on the way through. Inline them.
6. **Interfaces with one implementation and single-product factories,** written for a second variant that never came (`IThing`, `ThingFactory.create()` wrapping one constructor).
7. **Options nobody passes.** Parameters only ever defaulted, config objects with one live key, switches with one state.
8. **Symmetry for its own sake.** Empty `else`, unreachable `default:`, empty `finally`, a wrapper that only awaits.
9. **Files holding one constant,** unless the boundary is the point.

**Defensive noise**

10. **Impossible guards.** Null checks on values that can't be absent, `typeof` after the compiler narrowed, `try/catch` that only rethrows. A type annotation doesn't validate runtime input, so keep checks at real trust boundaries (request bodies, CLI args, env vars, `JSON.parse`, file/network I/O) and catches that add context or cleanup. If you cannot prove a guard is redundant, leave it.
11. **Assertions and suppressions that silence checks.** `as any`, `as unknown as T`, `!` where narrowing works, widening to `unknown` and asserting back, and unexplained `eslint-disable`, `@ts-ignore`, `@ts-expect-error`, `# type: ignore` or `# noqa`. Fix the type or keep only suppressions for genuinely style-only rules; if removing one needs a runtime change, report it.
12. **Hand-rolled standard library.** `groupBy`, `chunk`, `debounce`, date formatting. Swap only when semantics match for every caller: timing, defaults, errors, locale, edge cases. Use a language built-in or a dependency the repo already has; never add one.
13. **Async plumbing.** An `async` function with no `await` still returns a Promise and turns throws into rejections; awaiting a plain value still yields. Trace callers before removing either.

**Output and leftovers**

14. **Decorated output.** Emoji, box-drawing, ✅/❌ theatre, banners.
15. **Congratulatory strings.** "Successfully completed!", "All done!".
16. **Error messages that restate the stack.** Say what failed and what to do.
17. **Dead scaffolding and compat leftovers.** Unowned `TODO`s, example blocks, unused fixtures, debug leftovers (`console.log`, `print`, `dbg!`), unused imports or params, `_unused` renames, `// removed` tombstones, and unused re-exports.

**Control flow**

18. **Deep nesting or nested ternaries** an early return or flat `if`/`switch` would untangle, when order, side effects and return values stay the same.

## Steps

Run the narrowest existing check that could catch a behaviour change, then report in a few lines what went (by tell number) and what was referred.

In a repo on `@howells/lint`, leave lint-enforceable classes (unexplained type assertions, `unknown` in signatures, module mocking, `Reflect` access) to the preset; if it isn't loading, say so and point at the `howells-lint` skill from `howells/lint`.
