# Evidence

Versions, observability, tests and evaluations: the checks that catch Mastra failures typecheck misses.

## Versions

- **The docs say what a feature means; the installed code says whether it exists and what it defaults to.** Where installed packages are absent, the audit is against convention; say so.
- **Duplicate framework or driver copies split types, runtime identity and test guards.** Separate apps may run different versions; check the coupled runtime, CLI and adapter compatibility instead of demanding one version everywhere.
- **A type error after a version bump is a version change,** often collapsed overload resolution on an option combination that compiled before.
- **A permitted dependency patch has a regression case,** checked in the served or packed artefact, not just the patch source. A bump can withdraw behaviour a test double still imitates. Never restore an explicitly removed patch.

## Observability and progress

- **User-visible progress comes from domain events or workflow state,** never exporter flush timing, or progress vanishes when export is slow.
- **Transient progress chunks have a durable record alongside,** or a refresh loses them.
- **Register progress sinks from a module every bundle loads.** Registered from the app bundle alone, a separate worker bundle persists nothing, silently.
- **Order cross-process appends to one log with a database lock,** reading every written value from the locked row. A promise chain can't order two processes.
- **Every caught error logs its cause,** even where the user sees only a class name.
- **Lifecycle and observability writes project their returned columns;** otherwise each step drags the whole row back, multiplied by fan-out.
- **Measure time from the queries the engine actually issues,** not a hand-written model of them.
- **Telemetry carries correlation id, model id, model role, duration and an actionable stage,** with bounded sampling, payload size, cardinality and redaction. A telemetry failure never fails a good run.

## Tests

- **Test the named failure at its real boundary.** A suite asserting generated shapes can be green over a broken path.
- **Durable changes get round-trip evidence,** including refused writes or oversized payloads when those are the risk.
- **One bounded smoke test covers the critical path** against the real singleton.
- **Registration changes run the repo's gate over generated manifests, capability schemas and count pins;** a package's own tests miss them.
- **Import or dependency changes need the affected bundle built and booted.** A typecheck doesn't exercise Mastra's bundler.

### Offline tests that touch a live store

Test filenames, a mock of one service and in-memory assertions don't establish isolation. A root env file can override refused URLs, alternate key names survive clearing one variable, and singleton construction can discover vector indexes or initialise storage before the test body runs.

For a database-free test, install the guard before loading the registry or adapters. Refuse the driver or network seam actually used, covering promise and callback connections, pools, startup discovery and each resolved driver copy. Record attempts independently and fail in teardown, because the application may swallow the refusal. A global `fetch` guard doesn't cover another HTTP client, a subprocess or another driver; claim only what was blocked.

Fix the owning boundary with lazy initialisation or injected dependencies, not more refused env URLs or an excluded test. Integration tests live in a separately selected config with explicit store permissions. Never run a dangerous test to measure how dangerous it is.

## Evaluations

Scorers judge completed behaviour; processors change it during execution. A green score doesn't prove a hard requirement was enforced.

- **Define expectations independently of the current answer,** across different briefs, including the disputed adverse case: missing required use, absent fact, duplicate identity, sparse filter, later-page exhaustion, a near match failing a hard threshold.
- **Keep factual checks deterministic:** retrieved identifiers, distinct producers, counts, limits, exclusions, duplicates, cursors, stop reasons. Use model judgement only for bounded interpretation.
- **Carry required conditions from the request through to the final prose.** A count score can pass an answer that drops the requested use. Unknown evidence stays unknown.
- **Provenance isn't accuracy.** A source label records origin; a sales channel isn't necessarily the manufacturer.
- **Count unique tool calls by call id.** Cumulative snapshots repeat calls; duplicated telemetry isn't repeated execution.
- **Keep unscorable, failed, aborted and substituted results as explicit counts,** so a strong average can't hide a hard failure.
- **Durable evaluation means records readable after a reconnect,** checked in Studio or the API. In-memory wiring isn't acceptance.
- **Read existing traces and experiments before buying a new baseline.** Bound new runs by cases, calls, cost and time, and compare the same expectations before and after; don't loop on prompts until a result looks good.

Public source: [Mastra evals](https://mastra.ai/docs/evals/overview).

## Acceptance

- **Inspect the run's own output** (ledger, persisted document), not only its terminal status.
- **Secrets reach the actual runtime.** A task runner can drop an otherwise supplied secret.
- **API evidence proves the API path;** an interactive feature needs its host journey. Source tests don't prove repaired stored data, and a deployed fix is checked by reading the endpoint's version.
- **Record the measured failure and the fix on the owning tracker item.** Add reusable prevention to this skill with its version applicability, not the incident's incidental numbers.
