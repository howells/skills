# Evidence

Whether the implementation can be trusted to tell you when it is wrong. A codebase can pass every check in `structure.md` and still be unobservable and untested.

## What counts as verified

- **Every novel API usage was checked against installed types or version-matched docs**, not recalled. This is the check that gates all the others: an audit built on a remembered signature is confidently wrong.
- **The installed version is noted**, and any disagreement between docs and installed code was resolved in favour of what is installed.
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
- **Registration changes verify affected manifests and capability contracts.** Use the required repository gate or the focused checks that cover those outputs; registration alone does not require the full suite.

## Evidence of implementation completion

Check existing logs, tests and records for these claims. Run the system only when the audit brief authorizes its effects; otherwise record missing runtime evidence as not checked.

- **A real run was driven end to end by API**, not clicked through a UI.
- **The run's own output was inspected** - the ledger, the persisted document - not just its terminal status.
- **The dev-server log was read for framework error ids even on a passing run.**
- **Any new failure mode is written down**, with the wrong turn that produced it, wherever the codebase keeps that record.
- **If the work made an environment variable required, every hand-built environment was updated**: test fixtures, the shared harness, each CI job, the task runner's passthrough list, and every deployment environment. A task runner that strips anything absent from its passthrough list will silently drop a variable set only on the CI job, and nothing warns you.
