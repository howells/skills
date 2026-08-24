# Scorecard

Seven axes, each 0 to 3. Total 0 to 21. Accessibility is a bonus axis reported separately so the core number stays comparable across project types.

The point of the number is comparison over time. A survey that produces findings and no score tells you what is wrong today; one that produces a score tells you whether six months of work moved anything.

| #   | Axis             | Scored by                                     |
| --- | ---------------- | --------------------------------------------- |
| 1   | Security Posture | security lens, when the gate opens            |
| 2   | Performance      | performance lens                              |
| 3   | Architecture     | architecture lens (plus any framework lens)   |
| 4   | Code Quality     | quality lens                                  |
| 5   | Test Health      | tests lens, plus mechanical caps              |
| 6   | Resilience       | resilience lens                               |
| 7   | Operations       | mechanical checks only - no lens              |

| Bonus         | When               | Scored by           |
| ------------- | ------------------ | ------------------- |
| Accessibility | Frontend projects  | accessibility lens  |

## Criteria

### 1. Security Posture

Can an attacker exploit this?

| Score | Criteria                                                                                                                          |
| ----- | --------------------------------------------------------------------------------------------------------------------------------- |
| 0     | Exposed secrets, injection surfaces, missing auth on protected routes, no input validation at boundaries                          |
| 1     | Auth exists but has bypasses or inconsistencies; partial input validation; known high or critical CVEs in dependencies            |
| 2     | Auth covers every route, inputs validated at boundaries, clean dependency audit. Hardening missing - CSP, rate limiting, CSRF     |
| 3     | Defence in depth. Auth and authorisation, comprehensive validation, CSP, rate limiting, secrets managed properly, clean audit     |

### 2. Performance

Will it hold under real load?

| Score | Criteria                                                                                                        |
| ----- | --------------------------------------------------------------------------------------------------------------- |
| 0     | N+1 queries, unbounded fetching, no code splitting, blocking renders, no caching                                |
| 1     | Large bundles, missing indexes, client-side fetching where the server would do, render waterfalls               |
| 2     | Code splitting, lazy loading, indexed queries, reasonable bundles. Room left in caching, streaming or the edge  |
| 3     | Efficient cached queries, streaming responses, optimised bundles, and it has actually been measured             |

### 3. Architecture

Is it organised for change?

| Score | Criteria                                                                                                                                                     |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 0     | God files (authored source 1000+ lines, or any file 2000+), god page-clients, circular dependencies, barrel files, cross-workspace app imports, logic in UI  |
| 1     | Some structure, leaky boundaries. Mixed concerns, server/client boundary hacks, files in the 600 to 999 band, deep coupling between modules                  |
| 2     | Clear module boundaries and a proper server/client split. Some high coupling or unclear ownership remains                                                     |
| 3     | Clean separation, defined interfaces, dependency direction enforced. A new feature doesn't require touching unrelated code                                    |

### 4. Code Quality

Readable, correct, maintainable?

| Score | Criteria                                                                                                                                        |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0     | No type safety or `any` throughout, no linting, dead code everywhere, inconsistent patterns                                                      |
| 1     | Types with gaps - `any` and casts, lint warnings, direct `process.env` reads with no typed strategy, useless barrels, runtime `import()`, dead exports |
| 2     | Strong types, lint-clean, typed env strategy, no useless barrels, consistent patterns, little dead code. Some files in the 600 to 999 band       |
| 3     | Strict types, zero lint issues, nothing over 600 lines, no barrel or dynamic-import smells, consistent patterns, no dead code                    |

### 5. Test Health

Can you refactor with confidence?

| Score | Criteria                                                                                                     |
| ----- | ------------------------------------------------------------------------------------------------------------ |
| 0     | No tests, or tests that exist and assert nothing meaningful                                                  |
| 1     | Happy paths only. Low coverage, flaky runs, or poor isolation                                                |
| 2     | Critical paths covered. Isolated, reliable, asserting behaviour. Gaps at the edges and in integration        |
| 3     | Unit, integration and end-to-end. Meaningful assertions, fast and reliable, edge cases covered               |

### 6. Resilience

Does the unhappy path work?

| Score | Criteria                                                                                                                      |
| ----- | ------------------------------------------------------------------------------------------------------------------------------- |
| 0     | No error handling. Unhandled rejections, blank screens on failure, no loading states, crashes on empty data                    |
| 1     | Inconsistent. Some spinners, some `try`/`catch`, but many paths show raw errors, hang, or ignore empty states                  |
| 2     | Error boundaries in place, loading and error states on most async flows, network failure degrades. Empty states still patchy    |
| 3     | Every async operation has loading, error and empty states. Boundaries at the right levels. Retries where warranted             |

### 7. Operations

Ready to run and maintain? Derived from the mechanical pass, never from a lens.

| Score | Criteria                                                                                                                                |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 0     | Build broken or fragile, type errors, no automated checks, no deployment config                                                          |
| 1     | Build passes with warnings. Basic CI. Deployment minimal or manual                                                                       |
| 2     | Clean build, types and lint. CI runs tests. Deployment repeatable. Monitoring or structured logging missing                              |
| 3     | Clean build; lint and typecheck configured and CI-enforced in every app and package; monitoring, structured logging, rollback capability |

### Bonus: Accessibility

| Score | Criteria                                                                                                     |
| ----- | ------------------------------------------------------------------------------------------------------------ |
| 0     | No semantic HTML, keyboard navigation broken, no alt text, no ARIA                                           |
| 1     | Some semantic elements and alt text, but broken keyboard nav, poor contrast, no focus management             |
| 2     | Semantic HTML, keyboard navigable, sound ARIA, good contrast. Missing reduced-motion or modal focus trapping |
| 3     | WCAG 2.1 AA. Screen-reader tested, reduced motion, skip links, focus management, accessible forms            |

## Mechanical caps

These override a lens score. A cap is a ceiling, not a value - a lens scoring below the cap keeps its lower score.

| Condition                                                                        | Cap                |
| -------------------------------------------------------------------------------- | ------------------ |
| Build broken                                                                     | Operations → 0     |
| Type errors without build failure                                                | Operations → 1     |
| Any app or package with no configured lint **and** typecheck                     | Operations → 2     |
| No test files found                                                              | Test Health → 0    |
| Test failures in the mechanical pass                                             | Test Health → 1    |
| Any authored source file at 2000+ lines                                          | Architecture → 1   |
| A god page-client - thin page or layout passing through to one 1000+ line client | Architecture → 1   |
| Pervasive code-policy violations (useless barrels, untyped env reads, heavy runtime `import()`) | Code Quality → 2 |

The 2000-line cap is a presumptive blocker, not a proof. A genuine reason can be argued in the writeup; the default verdict is "split it". Isolated code-policy cases are findings without a cap - the cap is for the pervasive pattern.

## Deriving the total

1. **Score the posture, not the worst finding.** Each lens scores its axis against the criteria table as a whole.
2. **Two lenses on one axis: take the lower.** Conservative by design.
3. **Apply the mechanical caps** after the lens scores are in.
4. **An axis nobody reviewed is `--`.** Adjust the denominator - `X/18` where one axis was skipped - and say why in one line. Never infer health from absence of review, and never let a gated-out security lens pull the number down.
5. **Bonus axes report separately** as `+n/3`, outside the /21.

## Bands

| Range | Band                 | Meaning                                                                          |
| ----- | -------------------- | -------------------------------------------------------------------------------- |
| 0-7   | **Fragile**          | Critical gaps across several areas. Real risk of incidents or cascading failure  |
| 8-12  | **Developing**       | Foundation there, notable weaknesses. Fine for building, risky in production     |
| 13-17 | **Solid**            | Well built, specific things to improve. Shippable with known tradeoffs           |
| 18-21 | **Production-grade** | Maintainable, resilient, secure                                                  |

## Stage is interpretation, not scoring

**The score is absolute.** A prototype at 10/21 is healthy and expected. A production system at 10/21 needs attention. Same number, different verdict, and the difference belongs in the written interpretation rather than in the arithmetic.

Bending the number to flatter the stage destroys the only thing the number is for. Next quarter's survey has to be comparable to this one.

## Recording a score

Write the score into the tracker item with the survey, in a form the next run can find: the total, the seven axis values, the stage it was taken at, and the commit it was taken from. A score without its stage and its commit is not comparable to anything.
