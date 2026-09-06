# Review lenses

Choose lenses from the selected code and question, then use them to deepen the
strict structural review in `SKILL.md`. Lenses are investigative aids, not a
required roster. A small diff may need one; a cross-boundary change may need
several. No model count, subagent count, or command sequence is required.

Every finding needs a live source location, a concise explanation of the cost,
the simpler or safer direction, and the behavior or contract that must survive.
Use repository instructions, tests, callers, schemas, and runtime contracts to
confirm the claim. Include the exact source excerpt or an equally precise
runtime/configuration observation, so another reviewer can verify the finding
without reconstructing it from a line number. Cluster findings with one cause;
do not repeat the same problem per file. End a whole-codebase review with the
source roots and important boundaries examined, plus anything sampled or skipped.
A diff review names its comparison base and must never claim whole-codebase
health.

## Always consider: structural quality

Apply the main Simplify rubric: look for a code-judo reframing that removes
concepts, branches, modes, wrappers, or incidental orchestration. Inspect file
growth, repeated conditionals, feature leakage into shared paths, duplicated
canonical helpers, unclear type boundaries, casts and optionality that hide an
invariant, circular or wrong-way dependencies, and partial updates that should
be atomic. These standards apply at every lifecycle stage.

## Select when relevant

| Lens | Use when the selected scope includes | Confirm in source |
| --- | --- | --- |
| Security | auth, permissions, untrusted input, secrets, personal data, public writes, payments, uploads, webhooks | boundary validation, authorization path, data exposure, and the actual sink or dependency advisory |
| Reliability | async work, I/O, state transitions, network or provider calls | failure, empty, retry, timeout, rollback, and partial-state behavior |
| Performance | queries, collections, rendering, bundles, concurrency, or a reported slowdown | call paths, bounds, indexes, measurements, and workload assumptions |
| Data | schema, migrations, persistence, import/export, or transactional writes | migration effect, constraints, ownership, rollback, and all writes that must agree |
| Tests | changed behavior, regression risk, or an existing test strategy | meaningful assertions, critical-path coverage, isolation, and the test's relation to the contract |
| Operations | build, release, runtime configuration, deployment, or maintainability of the actual workflow | applicable scripts, CI coverage including root orchestration, repeatability, observability and recovery; distinguish unavailable tooling from proven failure |
| Accessibility | user-facing UI, controls, forms, navigation, motion, or visual feedback | semantic structure, keyboard flow, focus, labels, error association, contrast, and reduced-motion behavior |

Absence of a lens is not evidence of health. A focused check may establish a
finding; run it only when it answers a concrete question. Do not automatically
run builds, typechecks, lint, dependency scans, or every test suite.

## Finding format

```
[severity] path/to/file:line
Cost: <specific consequence and affected scope>.
Direction: <simpler structure or concrete corrective action>.
Evidence: <source behavior, caller, test, measurement, or configuration read>.
Excerpt: <exact relevant source, or precise observed runtime/configuration output>.
```

Use `must fix` for demonstrated dangerous or contract-breaking behavior. Use
direct structural language for clear regressions. Use conditional language for
future-stage or unproven risk. If the user requests scoring, follow the optional
[scorecard](scorecard.md); otherwise return findings and coverage only.
