---
name: unslop
description: "Remove machine-written code tells from a diff without changing behavior: narrating comments, one-caller wrappers, impossible guards, unused options, decorative logs, and leftover scaffolding. Use before commit or review. For behavior-changing fallback cleanup use `fail-fast`; for prose use `deslop`."
---

# Unslop

The code-side counterpart to `deslop`. Same instinct, different material: `deslop` takes the tells out of writing, `unslop` takes them out of code.

Agent-written code carries a signature. Not bugs - it typechecks, the tests pass, it works. It is padded with ceremony that exists because a model was being thorough rather than because anything needs it, and the cost lands on whoever reads it next.

**The rule that decides every call: nothing here changes behaviour.** Remove a tell and the tests still pass unchanged. If a cleanup would alter what the program does, it is not this skill's - a fallback that hides a failure belongs to `fail-fast`, a file too big to hold in your head belongs to `componentize`. Say so and move on rather than smuggling a behaviour change into a tidy-up.

Read the surrounding code before calling something a tell. Local conventions and the purpose of an abstraction matter: a one-caller wrapper can still name a meaningful operation or preserve a useful boundary. The catalogue gives you patterns to investigate, not automatic deletions. Prefer the smallest edit that removes confirmed noise; do not rewrite neighbouring code to match your taste.

## The tells

Cite by number in findings, so a reviewer can see the pattern rather than the instance.

**Comments and names**

1. **Narrating comments.** `// loop over the users`, `// Phase 1: build the cards`. The code says it already. The assertion string or the log line is the only documentation a step needs.
2. **Doc comments that restate the signature.** "@param userId - the user id". If the doc adds nothing the type doesn't, delete it. If the symbol is exported and deserves real hover help, that is `marginalia`, not a deletion.
3. **Commented-out alternatives.** The other approach, kept "just in case". Git has it.
4. **Over-explicit names.** `userDataObject`, `handleClickEventHandler`, `configurationOptionsMap`. Say the noun.

**Ceremony**

5. **One-caller wrappers.** A function, class or module that exists to be called from exactly one place and adds nothing on the way through. Inline it.
6. **Interfaces with one implementation.** Written for a second implementation that never arrived.
7. **Options nobody passes.** Parameters whose default is the only value ever used, config objects with one live key, feature switches with one state.
8. **Symmetry for its own sake.** An empty `else`, a `default:` that cannot be reached, a `finally` that does nothing, a wrapper that only awaits.
9. **Files holding one constant.** Unless the boundary is the point, put it where it is used.

**Defensive noise**

10. **Redundant defensive handling.** A null check on a value that cannot be absent, a runtime `typeof` after the compiler already narrowed, or a `try/catch` that only rethrows the same error. Establish that the path is trusted; a type annotation alone does not validate runtime input. Keep boundary validation and catches that add meaningful context or cleanup. Catches that swallow errors or supply fallbacks belong to `fail-fast` when removing them would change behaviour.
11. **Redundant assertions.** `as any` used only to silence a type error, `as unknown as T`, a non-null `!` where narrowing would do the job honestly. Use the correct type or narrowing rather than another assertion. If fixing the mismatch requires a runtime change, report it instead.
12. **Re-implemented standard library.** A hand-rolled `groupBy`, `chunk`, `debounce`, or date formatter beside one that already ships.
13. **Redundant async plumbing.** Remove async syntax only after tracing callers and preserving Promise returns, rejection behaviour and scheduling. An `async` function without `await` still returns a Promise and converts throws to rejections; awaiting a plain value still suspends continuation. Neither is redundant merely because the syntax looks unnecessary. Refer uncertain changes instead of guessing.

**Output and leftovers**

14. **Decorated console output.** Emoji, box-drawing, ✅/❌ status theatre, banner headers in logs and CLI output.
15. **Congratulatory strings.** "Successfully completed!", "All done!". Report the outcome or say nothing.
16. **Error messages that restate the stack.** Say what failed and what the caller should do; the stack is already there.
17. **Dead scaffolding.** `TODO` placeholders nobody owns, example blocks, and any mock, stub or fixture that leaked into a production path.
18. **Tests asserting the mock.** A test that checks a spy was called, rather than that the behaviour happened. It passes forever and proves nothing.

**Control flow**

19. **Unnecessary nesting.** Newly introduced layers of `if/else` that an early return would make easier to follow. Flatten only when execution order, side effects, cleanup and return values stay the same. Leave nesting alone when it expresses the logic clearly or fits the surrounding code.

## Steps

Scale the workflow to the diff. For a small cleanup, keep the scope, reasoning and verification brief; a separate task list is optional.

1. **Fix the scope.** Default to the diff - the branch against its merge base, or the working tree. A whole-repo sweep is a different job and needs saying out loud, because it will touch code nobody asked you to touch.
2. **Choose relevant verification.** Name the behaviour that could change and use the narrowest existing check that could catch it. For comment-only changes, inspect the diff and any applicable documentation check. Record unrelated baseline failures and continue safe independent work. Preserve repository-required final checks; do not start a workspace-wide gate ladder.
3. **Pass over the diff against the catalogue.** Read nearby code to establish local conventions, then record one finding per confirmed instance, each carrying the tell number and a `file:line`. Do not rewrite as you read - a pass that edits while it scans loses the thread and starts improving things.
4. **Sort the findings into remove and refer.** Remove is anything behaviour-preserving. Refer is anything that would change what the program does, named with the skill that owns it. Never do a refer inline.
5. **Apply the removals, then verify the affected contract.** Run the selected checks and inspect return values, side effects and timing where relevant. Passing tests support equivalence; they do not prove it. Investigate changed results, distinguish flaky or pre-existing failures, and revert any removal that changes behaviour.
6. **Report.** For a small cleanup, use one to three sentences: what changed, anything referred elsewhere, and the gate result before and after. Include tell numbers and file locations when needed to explain a finding; reserve counts by tell for a requested audit or a larger diff that benefits from them.

## What this is not

- Not a style pass. Formatting is `@howells/lint`.
- Not a refactor. Moving logic between modules or extracting a package is `componentize`.
- Not a hardening pass. Deleting a fallback so it fails loudly is `fail-fast`, and that one changes behaviour on purpose.
- Not a review. Correctness bugs are a different job; if you find one, report it and leave it.
