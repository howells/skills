---
name: unslop
description: "Strip machine-written tells from a diff without changing behaviour: narrating comments, one-caller wrappers, impossible guards, decorative logs, leftover scaffolding. Not for structural review (`fettle`), fallback removal (`failfast`) or prose (`deslop`)."
---

# Unslop

Agent-written code works, but it carries ceremony a model added to look thorough, and the next reader pays for it. Take the ceremony out; leave behaviour exactly as it was.

- **Nothing here changes behaviour.** If removing a tell would change what the program does, report it and name the owner: a fallback that hides a failure, a mock, stub or test hook in production code, or a test that only asserts on its mock is `failfast`; a file or module to split is `componentize`; a correctness bug is simply reported.
- **Read the neighbourhood first.** A one-caller wrapper can name a real operation or hold a deliberate boundary; local convention wins. Make the smallest edit that removes the noise, and don't restyle the code around it.
- **The scope is the diff:** the branch against its merge base, or the working tree. Sweep the whole repo only when asked.
- **Output others read is a contract.** CLI output, error text and logs consumed by scripts, users or monitoring stay as they are unless their change was asked for. This protects output that existed before the diff; output the diff itself added is fair game for tells 14–16. Never update snapshots to make a cleanup pass.

## The tells

Cite by number so a reviewer sees the pattern, not just the instance.

**Comments and names**

1. **Narrating comments.** `// loop over the users`, `// Phase 1: build the cards`.
2. **Doc comments that restate the signature.** `@param userId - the user id`. Delete; if an export needs real hover help, that's `marginalia`.
3. **Commented-out alternatives.** Git has them.
4. **Over-explicit names.** `userDataObject`, `handleClickEventHandler`, `UserShape`. Say the noun.

**Ceremony**

5. **One-caller wrappers** that add nothing on the way through. Inline them.
6. **Interfaces with one implementation,** written for a second that never came.
7. **Options nobody passes.** Parameters only ever defaulted, config objects with one live key, switches with one state.
8. **Symmetry for its own sake.** Empty `else`, unreachable `default:`, empty `finally`, a wrapper that only awaits.
9. **Files holding one constant,** unless the boundary is the point.

**Defensive noise**

10. **Impossible guards.** Null checks on values that can't be absent, `typeof` after the compiler narrowed, `try/catch` that only rethrows. A type annotation doesn't validate runtime input, so keep checks at real boundaries, and keep catches that add context or cleanup.
11. **Assertions that silence types.** `as any`, `as unknown as T`, `!` where narrowing works, widening to `unknown` and asserting back. Fix the type; if that needs a runtime change, report it.
12. **Hand-rolled standard library.** `groupBy`, `chunk`, `debounce`, date formatting. Swap only when semantics match for every caller: timing, defaults, errors, locale, edge cases. Use a language built-in or a dependency the repo already has; never add one.
13. **Async plumbing.** An `async` function with no `await` still returns a Promise and turns throws into rejections; awaiting a plain value still yields. Trace callers before removing either.

**Output and leftovers**

14. **Decorated output.** Emoji, box-drawing, ✅/❌ theatre, banners.
15. **Congratulatory strings.** "Successfully completed!", "All done!".
16. **Error messages that restate the stack.** Say what failed and what to do.
17. **Dead scaffolding.** Unowned `TODO`s, example blocks, unused fixtures.

**Control flow**

18. **New nesting an early return would flatten,** when order, side effects and return values stay the same.

## Steps

Run the narrowest existing check that could catch a behaviour change, then report in a few lines what went (by tell number) and what was referred.

In a repo on `@howells/lint`, leave lint-enforceable classes (unexplained type assertions, `unknown` in signatures, module mocking, `Reflect` access) to the preset; if it isn't loading, say so and point at the `howells-lint` skill from `howells/lint`.
