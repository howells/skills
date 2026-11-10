# Execution semantics

Steps, fan-out, retries, resume, storage, invocation boundaries and model loops. Engines differ: match the installed adapter and the project's conventions.

## Workflow steps

- **Give each recoverable unit a checkpoint.** A durable engine replays a failed step's body but keeps completed checkpoints; external side effects aren't rolled back. One batch step hides progress and repeats finished work after a late failure.
- **A serial `await` inside a step is deliberate or residue.** Refactors often keep a sequence nothing needs any more.
- **Don't thread a large object through a chain of steps.** Read it with the engine's step-result accessors or park it durably; threading inflates every snapshot in between.

## Fan-out

- **Every unit names itself in its output,** and the collector keys by that identity rather than position, unless the installed engine documents order preservation through concurrency and replay.
- **A failing arm returns a typed failure or shortfall.** Throw only when the whole result is invalid, saying why; otherwise one bad input kills every sibling.
- **Cancellation is wired, not assumed.** A thrown branch fails the parallel block, and cancel reaches only steps that check the abort signal. Nothing stops an already-dispatched child workflow; where one failure should stop the rest, thread a shared abort signal.
- **Arms return receipts, not bulk.** Bulk goes to durable storage; the arm returns a reference.

## Concurrency

- **Set it from what one iteration costs.** Default to 1 and raise deliberately; never copy another step's number.
- **The database's statement timeout bounds it.** A query that passes alone can time out run N-way.
- **Confirm the option reaches the executor.** An ignored concurrency option isn't a knob.
- **A dispatch window isn't an execution limit.** Some adapters parallelise an initial `foreach` window and refill differently; measure before tuning, and never size a window to an unbounded input.

## Retries

- **Follow retry settings through the actual adapter.** Workflow `retryConfig`, per-step retries and durable-function retries govern different boundaries, and defaults differ by release.
- **Set retries per step where idempotency differs.** A root `attempts: 0` protecting expensive work also stops a cheap idempotent step from retrying.

## Suspend and resume

- **Declare `suspendSchema` and `resumeSchema`** wherever a step can stop and ask; resume is keyed by step id.
- **Validate resume input server-side** at the boundary that receives it, naming the expected shape. The engine claims the run before validating, and only validates where input validation is enabled; check whether a rejected payload leaves the run claimed.
- **A caller-parameterised guard isn't in force until every call site passes it and every hop forwards it.** A stale-resume fence compared against `undefined` admits everything; a proxy forwarding only the payload drops the step id.
- **Round-trip nullable leaves through the installed adapter.** Server-side re-encoding can drop null-valued keys. Where null and absent mean different things, use an explicit discriminant.
- **New payload fields keep suspended runs resumable:** optional additive fields, versioning or a validated migration. This is separate from a provider's strict-output schema.
- **Record the suspension immediately before the run parks.**
- **Distinguish a live suspension from a dead run.** A stale heartbeat or a claimed run with no progress isn't a question awaiting an answer.
- **Check the emitted event, not the type.** A server-side payload type doesn't prove the payload is sent.

## State and storage

- **A write a later step depends on throws on failure.** Only telemetry is best-effort.
- **Engine working state and surface-facing events are separate types with separate size bounds.**
- **Measure snapshot size at the end of a real run.** Where a write failed, measure the reconstructed payload, not the last one stored.
- **Count store round-trips for the actual lane.** Memory, snapshots and observability can each read and write per turn, especially through a durable adapter. Measure before blaming the model or tracer.
- **Know the adapter's cost model.** Per-step write cost that scales with snapshot size makes a long workflow quadratic.
- **Share the configured provider where persistence is meant to be shared.** Deliberately separate stores are fine; an accidental duplicate instance, or a standalone memory-backed agent without its provider, is not.
- **Missing storage config fails fast in production** where agent memory, suspended runs, kept traces and scores, schedules or cross-process state must survive.
- **Try start-up DDL over the connection the deploy actually uses,** or move schema initialisation out of the runtime. Specific pooler and option combinations fail.
- **A storage-adapter change needs runtime acceptance:** startup, schema ownership, the deployed connection. Compilation proves no persistence.

## Invocation boundaries

A durable run is many invocations, often in different processes, on a platform that may kill the one that started it.

- **The worker that owns the work writes its own heartbeat.** A poller writing it reports liveness nobody has.
- **A terminal write merges into the durable log,** never replaces it; the process writing the end rarely holds what the run accumulated.
- **A boot-time restart of active runs re-drives their steps;** check they are safe to repeat.
- **Timeouts bound one item, not a batch.** A deadline around a whole fan-out has the reliability of its slowest call; a route whose worst case exceeds the platform ceiling needs resumable slicing.

## Long agent loops

- **Completion is declared,** by terminal workflow state or an explicit completion operation, never inferred from narration or stream closure. Some loop APIs evaluate `stopWhen` only on non-terminal finishes.
- **Handle no-progress turns.** Enforce the required action at the call or controller and bound continuations; don't invent no-op tool calls to keep a loop alive.
- **Prompts carry a resuming clause** so continuation doesn't re-run earlier phases.
- **Lock input during auto-continuation,** or concurrent submits orphan streams.
- **Bound rounds by step count and elapsed time.**
- **Run multi-call generation server-side with durable progress.** Driven from a client, it dies on refresh and every reload pays the model cost again.

## Context and processor budgets

- **Measure before diagnosing a timeout:** serialised tool definitions, result bytes, final prompt tokens, stored history, snapshot size. An output cap bounds none of them, and request bodies can dominate an apparent model timeout.
- **Project model results and workflow state separately.** A compact `toModelOutput` can cut prompt cost while the full result still bloats snapshots.
- **Keep required evidence across the decision.** A fixed last-N-tool-steps window can drop identifiers and search results well below any token limit, causing repeated retrieval. Prefer a measured token budget that retains the request, hard constraints and held identities.
- **Trim tool calls and results in pairs.** Rewriting a dropped result as assistant prose makes the model echo it as an assertion; inspect the provider prompt before enabling compact-history modes.
- **Processor order is behaviour.** Trace the final `toolChoice`, tools and instructions after every hook; a repeat-failure guard can block a later completion action.
- **Mutable guards and processors are per request.** A shared singleton guard carries one user's failures into another's run; test a second independent request.
