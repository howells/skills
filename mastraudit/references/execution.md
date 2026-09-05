# Execution semantics

Where runs die. Audit this before anything structural.

Each check below exists because the failure it describes has happened. Where a codebase keeps its own failure log, match findings to it by name.

## Workflow steps

- **One discrete thing per step.** A step that processes a list is the highest-cost pattern here. Under a durable engine, everything inside a running step is lost when anything in it fails, so a step covering fourteen items loses all fourteen on the last one. List processing fans out per item.
- **A serial `await` inside a step is deliberate or it is residue.** Refactors that replace a walk often preserve its sequencing for no remaining reason.
- **No large object threaded through a chain of steps.** Read it where needed with the engine's step-result accessors, or park it durably. Threading inflates every snapshot between the two points.

## Fan-out

- **Every unit names itself in its output.** The identity must come from the unit, not from where it landed.
- **The collector preserves unit identity.** Prefer explicit identity keys. Before flagging positional collection as wrong, inspect the installed engine’s ordering guarantee through concurrency and replay; a documented, verified order-preserving operation can be valid.
- **A failing arm returns a typed failure or shortfall.** Only a failure that invalidates the whole result throws, and the throw site says why. One thrown iteration killing every sibling is a fan-out that cannot tolerate a single bad input.
- **Arms return receipts, not bulk.** Bulk data goes to durable storage and the arm returns a reference. Where a helper enforces this at the step boundary, use it; a step asserting size by hand is a step that will drift.

## Concurrency

- **Chosen from what one iteration of that step costs.** Never copied from another step in the same workflow, never left at a number nobody measured. Default to 1 and raise deliberately.
- **Bounded by the database's statement timeout, not the step's patience.** A query that comfortably passes alone can exceed a per-connection timeout when run N-way concurrent.
- **A concurrency option the engine ignores is not a knob.** Confirm the option you are setting reaches the executor before treating it as tuning.

## Retries

- **`retryConfig` belongs on the workflow.** Where an engine adapter pins retries on the function it creates, that value is unreachable from the public constructor and setting it is a silent no-op. Verify which lever actually reaches the executor in the installed version.
- **Classify before retrying.** Transient (rate limit, 5xx, socket) is worth retrying. Configuration (billing, credits, quota, auth) is not - retrying a payment-required response three times just delays the failure.
- **Side effects inside steps are idempotent by natural key.** Memoised steps re-emit on retry.

## Suspend and resume

- **`suspendSchema` and `resumeSchema` are declared** wherever a step can stop and ask, and resume is keyed by step id.
- **The payload carries human-readable names, not only ids.** An identifier rendered at a person is a defect, not a display detail.
- **New payload fields are optional and additive**, so runs suspended before the change still parse on resume.
- **The suspension is recorded immediately before the run parks**, not after.
- **The operator surface distinguishes a live suspension from a dead run.** A stale heartbeat or a claimed run with no progress is not a question awaiting an answer, and showing it as one wastes the person's time.
- **Ledger or state tokens are mapped to labels at the operator surface.**
- **What is serialised is what reaches the wire.** A payload type existing server-side is not evidence the payload is transmitted. Check the emitted event, not the type.

## State and storage

- **Any write a later step depends on throws on failure.** Only genuine telemetry is best-effort. A silently failed load-bearing write produces a run that looks fine and is not.
- **Engine working state and surface-facing events are separate types with separate size bounds.**
- **The snapshot size was measured at the end of a real run**, not assumed from the shape of the data.
- **Storage adapter choice is deliberate and its cost model understood.** Per-step write cost that scales with snapshot size makes a long workflow quadratic.
- **One store instance is shared** across memory, workflow and telemetry persistence. Separate instances give you several half-populated stores.
- **Missing storage configuration fails fast in production.** No in-memory fallback. A fallback here converts a deploy error into a data-loss incident.
- **Connection pools come from a shared helper**, with a floor above one connection and a connect timeout set. A single-connection pool can deadlock batch writes.
- **Adopting a dedicated storage adapter is a deploy-blocking change**, not a code change.

## Long agent loops

- **Completion is declared, never inferred.** A marker tool call ends the loop. Inferring completion from stream shape fails on a turn that narrates without calling a tool, and that failure is byte-identical to a clean finish.
- **Prompts mandate narration and a tool call in the same response**, so the loop gate always sees one.
- **Prompts carry a resuming clause** so continuation does not re-run earlier phases.
- **Input is locked during auto-continuation**, or concurrent submits orphan streams.
- **Rounds are bounded by both step count and elapsed time.**
