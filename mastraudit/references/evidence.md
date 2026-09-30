# Evidence

Read this before tests, evaluations and completion claims. Choose evidence for the changed behaviour, with side effects and acceptance scope made explicit.

## What counts as verified

- **Every novel API usage was checked against installed types or version-matched docs**, not recalled. This is the check that gates all the others: an audit built on a remembered signature is confidently wrong.
- **The installed version is noted**, and disagreements are resolved by kind: the documentation says what a feature means, the installed code says what its defaults are and whether it exists at all in this version.
- **Where the installed packages are absent, that is a stated coverage gap.** An audit of a checkout with no installed types is an audit against convention, and saying so is the whole of its value.
- **Resolve the relevant packages from each actual caller.** Duplicate framework or driver copies can split types, runtime identity and test guard coverage. Several applications can legitimately use different versions; investigate the coupled runtime, CLI and adapter compatibility rather than demanding one version across every project.
- **A permitted dependency patch has a regression case.** Verify the published/generated/served artefact as well as the patch source. A dependency bump can withdraw behaviour a test double still imitates. Don't add or restore a patch outside the task's scope; an explicitly removed patch remains removed.
- **A type error that appears on a version bump is investigated as a version change.** Overload resolution can collapse on a combination of options that compiled cleanly before, which looks like the code broke and is not.
- **Model ids were verified against a provider registry**, not recalled.
- **Where subagents wrote any of the code, their briefs carried the same mandate.** A delegated hallucination is still a hallucination.

## Observability and progress

- **User-visible progress comes from domain events or workflow state**, never from exporter flush timing. Telemetry timing is not a progress signal and coupling them makes progress vanish whenever export is slow.
- **Transient progress chunks have a durable record alongside them**, or they disappear on refresh and nothing replays them.
- **Progress sinks are registered from a module every bundle loads.** Registering from the app bundle alone means a separate worker bundle persists nothing, with no error anywhere.
- **Cross-process appends to one log are ordered by a database lock**, with every written value read from the locked row. A promise chain cannot order two processes.
- **Every caught error puts its cause in the log**, even where the user-facing surface deliberately shows only a class name. A terse surface is a choice; a terse log is a dead end for whoever debugs it.
- **Lifecycle and observability writes project their returned columns.** An unprojected return drags the whole row back once per step, multiplied by any fan-out.
- **Where the time went was measured from the queries the engine actually issues**, not from a query written by hand to model it.
- **Telemetry exposes correlation id, model id, model role, duration and an actionable internal stage.**
- **Sampling, payload size, cardinality and redaction are bounded per environment**, and a telemetry failure cannot fail an otherwise good run.

## Testing

- **Test the named failure risk at its real boundary.** A suite that only asserts generated shapes can be green over a broken path. Reuse applicable wrapper and containment checks; don't write a new test for every bullet or add a broad gate after each green check.
- **Durable changes have round-trip evidence**, including refused writes or oversized payloads where those are the changed risks. Drive new storage effects only within the task's authorisation.
- **An offline test blocks effects, not merely credentials.** Read the full import graph and env-loader precedence. A root env file can override refused URLs, alternate key names can survive clearing one variable, and singleton construction can discover vector indexes or initialise storage before a test body runs. See the guard procedure below.
- **At least one bounded smoke test covers the critical path** against the real singleton.
- **Registration changes verify affected manifests and capability contracts.** Generated manifests, capability schemas and count pins are what a targeted run misses, so use the repository's own gate over those outputs rather than the package's tests alone.
- **A runtime import/dependency change gets evidence from the affected bundle.** Where bundling, module-load effects or Studio discovery can fail, build and boot that owner when authorised. A product typecheck doesn't exercise Mastra's bundler. Coordinate an existing Studio process rather than starting or stopping a peer's runtime independently.

## Offline checks cannot reach a live store

Before invoking an unfamiliar test or scanner, inspect both its code and what it imports. Test filenames, mocks of one service and assertions about in-memory data do not establish isolation.

For a database-free check, install the guard before loading the real registry or adapters. Refuse the driver/network seam actually used and record attempts independently. Cover promise and callback connections, pools, startup discovery and each resolved driver copy. Fail the test in a teardown hook even when the application catches the refusal. A thrown connection error alone can be swallowed and leave a misleading green check.

Demonstrate that the guard catches a direct attempt and a deliberately swallowed attempt, without opening a socket. Report the guard's scope and observed attempt count. A global-fetch guard doesn't cover another HTTP client, a subprocess or another driver instance; don't claim isolation beyond what was blocked.

Use lazy initialisation or injected test dependencies where imports perform unnecessary storage work. Fix the common owning boundary rather than setting more refused env URLs or excluding the one test that exposed it. Keep integration checks in a separately selected configuration with explicit store and effect permissions; a suffix does not authorise them. Never run a dangerous test just to measure how dangerous it is.

## Evaluations that can change a decision

Scorers judge completed behaviour; processors can affect it during execution. A scorer file, registered scorer or green score doesn't establish that a hard requirement was enforced. Follow the actual hook, input, output and stored result.

- Define expectations independently of the current answer. Include different briefs and at least the disputed adverse case: a missing required use, absent fact, duplicate identity, sparse filter, later-page exhaustion or a near match that fails a hard threshold.
- Keep factual checks deterministic where possible: retrieved identifiers, distinct producers, category/use, counts, numeric limits, exclusions, duplicates, page cursors and stopping reasons. Use model/classifier judgement only for bounded interpretation; don't replace checkable facts with another model's approval.
- Preserve required conditions from the original request through extraction, retrieval, selection and final prose. A count/performance score can pass an answer that omits the requested use. Unknown evidence remains unknown, not verified suitability.
- Distinguish aesthetic judgement, provenance and factual accuracy. A source label records origin; it isn't an accuracy score. A sampling/sales channel isn't necessarily the manufacturer.
- Count unique tool calls using trace/call identity. Cumulative snapshots can repeat the same call; duplicated telemetry isn't repeated execution. Inspect genuine repeated requests, empty pages, failed-call guards, final-step behaviour and answers cut off by step limits.
- Represent unscorable, failed, aborted and substituted results explicitly. Keep those counts alongside valid scores rather than converting them into normal success or allowing a strong average to hide a hard failure.
- Persist datasets, experiments and scorer records to the intended store when durability is required. Inspect their identifiers, case outputs and associations in Studio or the API, then establish that the same records are readable after a controlled reconnect/restart. In-memory wiring isn't durable evaluation acceptance.
- Read existing traces and experiment records before buying a new baseline. If new model/evaluation runs are authorised, bound cases, calls, cost and elapsed time, use a stable source/runtime, and compare the same independent expectations before and after the change. Don't loop on new prompts until a result looks good.

Public source: [Mastra evaluation guide](https://mastra.ai/docs/evals/overview). Check the installed storage and evaluation APIs before creating a dataset or experiment.

## Evidence of implementation completion

Check existing logs, tests and records for these claims. Run the system only when the audit brief authorizes its effects; otherwise record missing runtime evidence as not checked.

- **Exercise the actual consumer journey.** API evidence establishes the API path; an interactive feature also needs the intended browser/host journey. Inspect fresh execution separately from saved rendering. See [Studio and MCP](studio-and-mcp.md).
- **The run's own output was inspected** - the ledger, the persisted document - not just its terminal status.
- **The dev-server log was read for framework error ids even on a passing run.**
- **Record the measured failure and the effective fix** on the owning tracker item or the codebase's designated record. Add the reusable prevention to the guide, with its version/adapter applicability; don't turn an incident's incidental numbers or old workaround into a universal rule.
- **Required secrets reach the actual runtime.** Check test fixtures, task-runner passthrough and deployment environment under the project's policies. A task runner can drop an otherwise supplied secret. Don't add hosted checks or deployments merely to verify a guide.

## Keep delivery claims separate

State the exact source revision and installed packages checked. Then state independently whether the change was committed, pushed, built, served, executed, persisted and interacted with. A commit, command exit, installation, terminal run status or screenshot is evidence for its own claim only.

For an upgrade or release, check the built/packed artefact and a real selected consumer. For a deployed fix, read the endpoint's version and exercise the relevant route. Source-level tests don't establish repaired stored data. Missing runtime, model, native-host or recovery evidence stays open without inflating a bounded pass into whole-system acceptance.
