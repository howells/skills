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
- **Cancellation is wired, not assumed.** The documented contract is that a thrown branch fails the parallel block, and that a cancel reaches only steps checking the abort signal. Nothing documents a failed sibling or an already-dispatched child workflow being stopped, so where one branch's failure should stop the rest, look for a shared abort signal threaded into the calls and confirm against the installed engine before flagging.
- **Arms return receipts, not bulk.** Bulk data goes to durable storage and the arm returns a reference. Where a helper enforces this at the step boundary, use it; a step asserting size by hand is a step that will drift.

## Concurrency

- **Chosen from what one iteration of that step costs.** Never copied from another step in the same workflow, never left at a number nobody measured. Default to 1 and raise deliberately.
- **Bounded by the database's statement timeout, not the step's patience.** A query that comfortably passes alone can exceed a per-connection timeout when run N-way concurrent.
- **A concurrency option the engine ignores is not a knob.** Confirm the option you are setting reaches the executor before treating it as tuning.

## Retries

- **`retryConfig` belongs on the workflow, and per-step `retries` overrides it.** Where an engine adapter pins retries on the function it creates, that value is unreachable from the public constructor and setting it is a silent no-op. Verify which lever actually reaches the executor in the installed version.
- **Retry posture is set per step wherever idempotency differs.** A workflow-root policy is blunt: `attempts: 0` set to protect expensive non-idempotent work also silently covers a cheap idempotent step that should have retried. Any zero carries its reason where the next reader will see it.
- **A retry re-runs the whole step body**, including writes the step already made, so a step that retries is a step whose side effects dedupe by natural key.
- **Classify before retrying.** Transient (rate limit, 5xx, socket) is worth retrying. Configuration (billing, credits, quota, auth) is not - retrying a payment-required response three times just delays the failure.
- **Side effects inside steps are idempotent by natural key.** Memoised steps re-emit on retry.

## Suspend and resume

- **`suspendSchema` and `resumeSchema` are declared** wherever a step can stop and ask, and resume is keyed by step id.
- **Resume input is validated at the boundary that receives it.** The engine claims the run before it runs anything, and validates resume data only where input validation is enabled, so confirm in the installed version whether a rejected payload leaves the run claimed. Either way a remotely callable resume refuses malformed input server-side, naming the expected shape, rather than trusting a caller-side type.
- **A guard parameterised by the caller is not in force until every call site passes it and every hop forwards it.** A stale-resume fence compared against `undefined` admits everything, and a proxy route or SDK method that forwards only the payload drops the step id in transit.
- **Nullable leaves of a suspending step's schema were round-tripped through the installed adapter**, not assumed to survive. An adapter that re-encodes the snapshot server-side can drop null-valued keys entirely, and the payload validated on the way out is a different artefact from the one validated on resume. Where the difference between null and absent carries meaning, encode it as an explicit discriminant.
- **The payload carries human-readable names, not only ids.** An identifier rendered at a person is a defect, not a display detail.
- **New payload fields are optional and additive**, so runs suspended before the change still parse on resume.
- **The suspension is recorded immediately before the run parks**, not after.
- **The operator surface distinguishes a live suspension from a dead run.** A stale heartbeat or a claimed run with no progress is not a question awaiting an answer, and showing it as one wastes the person's time.
- **Ledger or state tokens are mapped to labels at the operator surface.**
- **What is serialised is what reaches the wire.** A payload type existing server-side is not evidence the payload is transmitted. Check the emitted event, not the type.

## State and storage

- **Any write a later step depends on throws on failure.** Only genuine telemetry is best-effort. A silently failed load-bearing write produces a run that looks fine and is not.
- **Engine working state and surface-facing events are separate types with separate size bounds.**
- **The snapshot size was measured at the end of a real run**, not assumed from the shape of the data. The stored snapshot is the last write that succeeded, so where a write failed, the payload to measure is the one reconstructed rather than the one on disk.
- **The store round-trips per agent turn were counted.** An agent run is a workflow run and persists its snapshot as it progresses, so one turn against a remote store can be many writes, and latency becomes a property of the link to the store rather than of the model. Measure it before blaming the model, the tools or the tracer.
- **Storage adapter choice is deliberate and its cost model understood.** Per-step write cost that scales with snapshot size makes a long workflow quadratic.
- **One store instance is shared** across memory, workflow and telemetry persistence. Separate instances give you several half-populated stores.
- **Missing storage configuration fails fast in production wherever state must outlive the process.** No in-memory fallback. Establish first what has to survive: agent memory, suspended runs, traces and scores kept for analysis, schedules and background tasks, and anything two processes share. Where nothing does, the in-memory warning is not a finding, and provisioning an adapter to silence it has caused its own incident.
- **Connection pools come from a shared helper**, with a floor above one connection. A single-connection pool can deadlock batch writes. Pass only the pool options the installed adapter documents, or hand it a pre-built pool: an undocumented option is silently absent rather than rejected.
- **Start-up DDL was tried over the connection the deploy actually uses**, or schema initialisation is separated from the runtime and the runtime role no longer creates tables. Poolers differ: some carry initialisation fine, and a specific combination of pooler and connection option is what fails. Any schema tool sharing that database allow-lists the runtime-owned tables so a push cannot offer to drop them.
- **Adopting a dedicated storage adapter is a deploy-blocking change**, not a code change.

## Invocation boundaries

A durable run is many invocations, often in different processes, and frequently on a platform that kills the one that started it.

- **No state crosses an invocation through process memory.** Module-level maps, registries and signals read by an `onError` hook, a finalizer, a reconciler or a terminal write are empty in the process that actually runs them, and empty reads as nothing to do. The worker owning the work writes its own heartbeat; a poller writing it reports liveness nobody has.
- **A terminal write merges into the durable log rather than replacing it.** The process writing the ending rarely holds what the run accumulated.
- **A workflow is not started fire-and-forget from a request handler on a platform that freezes the function after the response.** The stored run stays running with nothing driving it, which reads as a hung run rather than a dropped one. Start it under the platform's after-response primitive, await anything whose completion matters, or hand it to a durable engine. Where a boot-time restart of active runs is the recovery plan, check those steps are safe to re-drive.
- **Timeouts bound one item, not a batch.** A deadline wrapped around a whole fan-out has the reliability of its slowest call, and a route whose worst case exceeds the platform's duration ceiling is designed for resumable slicing rather than given more rope.

## Model calls inside runs

- **Tools and structured output on one call are verified against the provider actually configured.** Some models do not support both, and the failure arrives as a rejection, as tools silently never being called, as a schema-valid empty object, or as a hang to the step's timeout. The documented remedies are prompt injection for the structured part, a separate structuring model, or splitting the acting and structuring into different steps. A run with zero tool calls is a counted failure rather than a success.
- **A degenerate result throws where it is called.** Check the abort signal before reading a structured result, refuse an array or an empty string where an object was required, and size an unbounded-cardinality schema against its worst case rather than its example.
- **Behaviour the model must not exhibit is enforced by the call, not by prose.** A prompt asking an agent not to call tools is a request; `toolChoice` and an empty tool map are the contract.
- **Nothing a later step branches on is parsed out of model narration.** A classification scanned from free text against a list of candidate names resolves on whichever name appears first, which is a coin toss dressed as a field.

## Long agent loops

- **Completion is declared, never inferred.** A marker tool call ends the loop. Inferring completion from stream shape fails on a turn that narrates without calling a tool, and that failure is byte-identical to a clean finish.
- **Prompts mandate narration and a tool call in the same response**, so the loop gate always sees one.
- **Prompts carry a resuming clause** so continuation does not re-run earlier phases.
- **Input is locked during auto-continuation**, or concurrent submits orphan streams.
- **Rounds are bounded by both step count and elapsed time.**
- **Every delegation carries its own bound.** A delegated call is its own generation with its own step limit, defaulting low and not inherited from the supervisor. A bound hit on a step that called a tool returns empty text, which reads as a failed answer and invites the supervisor to delegate the same prompt again.
- **A multi-call generation flow runs server-side with durable progress.** Driven a call at a time from a client, it dies on a refresh and cannot be resumed or replayed, and every reload pays the model cost again.
