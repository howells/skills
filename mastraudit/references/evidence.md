# Evidence

Whether the implementation can be trusted to tell you when it is wrong. A codebase can pass every check in `structure.md` and still be unobservable and untested.

## What counts as verified

- **Every novel API usage was checked against installed types or version-matched docs**, not recalled. This is the check that gates all the others: an audit built on a remembered signature is confidently wrong.
- **The installed version is noted**, and disagreements are resolved by kind: the documentation says what a feature means, the installed code says what its defaults are and whether it exists at all in this version.
- **Where the installed packages are absent, that is a stated coverage gap.** An audit of a checkout with no installed types is an audit against convention, and saying so is the whole of its value.
- **Every Mastra package, its engine adapter and its CLI resolve to one version each.** Duplicates split types and produce two half-configured runtimes, and a CLI expecting a newer companion package than the workspace pins breaks the build on a method that is simply not there.
- **Every patched dependency is pinned by a test that fails when the patch stops applying.** A rebuilt distribution moves the lines a patch targeted, and a version bump can withdraw behaviour the code depends on - context propagated across a resume, or a claim protocol a test double still imitates from the previous version.
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

- **Domain behaviour is tested in the domain package against the real dependency at least once.** A suite that only asserts the shape of generated output can be entirely green over a broken path.
- **Wrapper tests cover ids, descriptions, schemas, annotations, registration and delegation.**
- **Boundary tests guard against product logic reappearing in wrappers** - direct fetches, filesystem access, nested tool imports, one tool invoking another's execute.
- **Round-trip tests exist for anything written durably and read back later**, including the refused-write and oversized-payload cases.
- **Negative tests neutralise every source the code reads.** Neutralising the first environment variable name found, when the code reads several, produces a test that passes by accident.
- **At least one bounded smoke test covers the critical path** against the real singleton.
- **Registration changes verify affected manifests and capability contracts.** Generated manifests, capability schemas and count pins are what a targeted run misses, so use the repository's own gate over those outputs rather than the package's tests alone.
- **Any change to what the Mastra package imports or depends on is verified by building it and starting its studio.** The bundler decides what stays external and what is bundled, and neither decision is visible to the application build, the typecheck or the tests.

## Evidence of implementation completion

Check existing logs, tests and records for these claims. Run the system only when the audit brief authorizes its effects; otherwise record missing runtime evidence as not checked.

- **A real run was driven end to end by API**, not clicked through a UI.
- **The run's own output was inspected** - the ledger, the persisted document - not just its terminal status.
- **The dev-server log was read for framework error ids even on a passing run.**
- **Any new failure mode is written down**, with the wrong turn that produced it, wherever the codebase keeps that record.
- **If the work made an environment variable required, every hand-built environment was updated**: test fixtures, the shared harness, each CI job, the task runner's passthrough list, and every deployment environment. A task runner that strips anything absent from its passthrough list will silently drop a variable set only on the CI job, and nothing warns you.
