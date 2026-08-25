---
name: unslop
description: "Remove machine-written code tells from a diff without changing behavior: narrating comments, one-caller wrappers, impossible guards, unused options, decorative logs, and leftover scaffolding. Use before commit or review. For behavior-changing fallback cleanup use `fail-fast`; for prose use `deslop`."
---

# Unslop

The code-side counterpart to `deslop`. Same instinct, different material: `deslop` takes the tells out of writing, `unslop` takes them out of code.

Agent-written code carries a signature. Not bugs - it typechecks, the tests pass, it works. It is padded with ceremony that exists because a model was being thorough rather than because anything needs it, and the cost lands on whoever reads it next.

**The rule that decides every call: nothing here changes behaviour.** Remove a tell and the tests still pass unchanged. If a cleanup would alter what the program does, it is not this skill's - a fallback that hides a failure belongs to `fail-fast`, a file too big to hold in your head belongs to `heathen`. Say so and move on rather than smuggling a behaviour change into a tidy-up.

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

10. **Guards against states the types forbid.** A null check on a non-nullable, `?.` on a value that cannot be absent, a runtime `typeof` after the compiler already narrowed. Guards belong at the boundary where untrusted data arrives, not sprinkled inland.
11. **Redundant assertions.** `as unknown as T`, a non-null `!` where narrowing would do the job honestly. If the type is wrong, fix the type.
12. **Re-implemented standard library.** A hand-rolled `groupBy`, `chunk`, `debounce`, or date formatter beside one that already ships.
13. **Ceremonial async.** `async` on a function that never awaits, `await` on a plain value, a promise wrapper around synchronous work.

**Output and leftovers**

14. **Decorated console output.** Emoji, box-drawing, ✅/❌ status theatre, banner headers in logs and CLI output.
15. **Congratulatory strings.** "Successfully completed!", "All done!". Report the outcome or say nothing.
16. **Error messages that restate the stack.** Say what failed and what the caller should do; the stack is already there.
17. **Dead scaffolding.** `TODO` placeholders nobody owns, example blocks, and any mock, stub or fixture that leaked into a production path.
18. **Tests asserting the mock.** A test that checks a spy was called, rather than that the behaviour happened. It passes forever and proves nothing.

## Steps

Copy these steps into your todolist verbatim before you start. A step you skip stays in the list with a one-line `skip: <reason>`.

1. **Fix the scope.** Default to the diff - the branch against its merge base, or the working tree. A whole-repo sweep is a different job and needs saying out loud, because it will touch code nobody asked you to touch.
2. **Read the gate first.** Run the typecheck, lint and tests before you edit anything, so you know what green looked like. If it was not green, that is the finding; stop and say so.
3. **Pass over the diff against the catalogue.** One finding per instance, each carrying the tell number and a `file:line`. Do not rewrite as you read - a pass that edits while it scans loses the thread and starts improving things.
4. **Sort the findings into remove and refer.** Remove is anything behaviour-preserving. Refer is anything that would change what the program does, named with the skill that owns it. Never do a refer inline.
5. **Apply the removals, then run the same gate again.** Identical results, or you changed behaviour and have to back it out. Without that comparison this is an unreviewed refactor.
6. **Report.** Counts by tell number, the refer list, and the gate result before and after.

## What this is not

- Not a style pass. Formatting is `@howells/lint`.
- Not a refactor. Moving logic between modules is `heathen`; extracting a package is `aperture`.
- Not a hardening pass. Deleting a fallback so it fails loudly is `fail-fast`, and that one changes behaviour on purpose.
- Not a review. Correctness bugs are a different job; if you find one, report it and leave it.
