# Lenses

The review lenses a survey dispatches, what each one looks for, and what it must return. These replace named reviewer personas - a lens is defined here and pasted into a subagent prompt, so the skill stands alone in any repo.

## Selecting lenses

Start from scale, then add for type and circumstance.

| Scale  | Base lenses                            |
| ------ | -------------------------------------- |
| small  | quality, resilience                    |
| medium | quality, resilience, performance, architecture |
| large  | quality, resilience, performance, architecture, tests |

Then:

- **Security** only when the readiness gate in `stage.md` opens. Never by default.
- **Tests** when test files exist and scale is medium or large.
- **Accessibility** when the project is frontend-heavy and scale is medium or large. Scores a bonus axis, outside the /21.
- **Data** when the scope includes a database, migrations or an ORM schema.
- **Domain** when a framework with its own audit skill is detected. For Mastra, hand off to `mastraudit` rather than running a lens - it knows things this skill does not.

A user focus prioritises the matching lens; it does not remove the others unless scope is explicitly narrowed.

Typical counts: two or three lenses on a small project, three or four on a medium one, more as a large scope needs. These are not caps. A medium frontend project with a database and an open security gate legitimately reaches seven.

## What every lens receives

Compose each prompt from these parts. All of them, every time.

1. **The stage calibration block**, pasted verbatim from `stage.md`. Not paraphrased.
2. **The mechanical summary** - what built, what typechecked, what linted, what the tests did, what the secrets scan found, and which workspaces lack a lint or typecheck pipeline.
3. **Its slice of the signal manifests**, labelled as leads. The lens opens the file before reporting anything.
4. **The repo's own conventions** where they exist - `CLAUDE.md`, `AGENTS.md`, contributing docs, architecture notes, any failure log. State plainly that **project rules outrank generic best practice**, and that flagging something the repo explicitly allows is an error.
5. **The criteria table for the one axis it scores**, from `scorecard.md`, with an instruction to score it at the end.
6. **The output format** below.

## What every lens returns

Findings, worst first, each one:

```
[Severity] path/to/file.ts:142
What it costs, in one sentence.
Fix: what to do instead.
Excerpt: <the exact source line or lines the lens read>
```

The excerpt is mandatory and is not decoration. The vetting phase compares it against the live file to answer "is what the lens saw still there, and does it mean what the lens said". Without it, vetting degrades into re-deriving intent from a line number, which is how mis-attributed findings survive.

Then, last:

```
Axis score: [0-3] - [one sentence of justification]
```

Score the **overall posture of the axis** against its criteria table, not the worst single finding. One medium issue in an otherwise strong area does not force a low score.

## The lenses

### quality

Is the code readable, correct and maintainable? Type safety and the honesty of it - `any`, casts, suppressions. Lint state. Dead code and dead exports. Consistency of pattern and naming. Direct `process.env` reads with no typed strategy. Useless barrel files. Runtime `import()` used where a static import would do. File length against the 600-line band.

Scores axis 4, Code Quality.

### resilience

Does the unhappy path work? Every async operation should have loading, error and empty states. Look for unhandled rejections, blank screens on failure, hangs, crashes on empty data, missing error boundaries, and network failures that don't degrade. Retry logic where it's warranted, and its absence where it is.

Also the determinism smells: env vars with silent defaults, `catch` blocks that swallow, legacy aliases and compatibility shims. Report these as findings and route them to `fail-fast`; do not remove them here.

Scores axis 6, Resilience.

### performance

Will this hold under real load? N+1 queries, unbounded fetching, missing indexes. Bundle size and code splitting. Render waterfalls, blocking renders, client-side fetching where the server would do. Caching that isn't there and caching that's wrong. Repeated scans over the same data.

Prefer the measured claim. "This is O(n²) over a list that reaches ten thousand" beats "this could be optimised".

Scores axis 2, Performance.

### architecture

Is the codebase organised for change? God files - authored source over 1000 lines, or anything over 2000. God page-clients: a thin `page.tsx` or `layout.tsx` passing straight through to one enormous `"use client"` component. Circular dependencies. Barrel files. Cross-workspace app imports. Business logic tangled into UI. Server and client boundary hacks - `*-wrapper`, `*-client`, boundaries hoisted higher than they need to be.

Report the structural defects; route the decomposition to `componentize`.

Scores axis 3, Architecture.

### tests

Can you refactor with confidence? Coverage of critical paths, not coverage as a number. Whether assertions test behaviour or restate the implementation. Isolation, flakiness, speed. Edge cases and integration gaps. A test suite that passes while asserting nothing is worse than none, because it buys false confidence.

Scores axis 5, Test Health.

### security

**Only when the gate in `stage.md` opens.**

Auth coverage across every protected route, and consistency of it. Authorisation as distinct from authentication. Input validation at boundaries. Injection surfaces - SQL, XSS, command, template. Secrets handling and anything hardcoded. Dependency CVEs. CSRF, CSP, rate limiting. Unsafe HTML and `eval`.

Scores axis 1, Security Posture.

### data

Schema and migration safety. Destructive migrations without a path back. Missing indexes on queried columns. Cascade behaviour. Transactions around writes that must land together. Load-bearing writes that fail silently. N+1 access patterns at the ORM layer.

Contributes to axes 2 and 6; does not own an axis alone.

### accessibility

Semantic HTML. Keyboard navigation, including focus order and traps in modals. ARIA that helps rather than decorates. Contrast, measured rather than eyeballed. `prefers-reduced-motion`. Skip links, focus management, form labelling and error association.

Scores the bonus accessibility axis, reported as `+n/3` outside the /21.

## A second opinion on an axis

Where two lenses score the same axis - architecture and a framework lens both scoring axis 3, say - **take the lower score.** Conservative by design: a survey that flatters is worse than useless, because the next one has nothing to compare against.
