# Execution semantics

Read this while designing steps, state, processors and model loops. Decide the failure and recovery boundaries before wiring them together.

These are recurring failure classes, not a claim that every engine has identical semantics. Match the implementation to the installed adapter and the project's adopted conventions.

## Workflow steps

- **Give each recoverable unit a checkpoint.** A durable engine can replay a failed step's body while retaining completed checkpoints. External side effects already made aren't rolled back. Keep separately recoverable list items in separate units; use the project's finer decision/IO granularity where adopted. A single batch step hides progress and repeats completed work after a late failure.
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
- **A dispatch window and an execution limit are different.** Some adapter versions parallelise an initial foreach window but refill differently. Inspect or measure that scheduler before tuning. Don't copy an item-count-sized window onto an unbounded input; preserve a bounded execution limit and use bounded chunks or supported native flow control.

## Retries

- **Follow retry settings through the actual adapter.** Workflow `retryConfig`, per-step retries and durable function retries can control different failure boundaries. Some releases default function retries to zero; others expose an override. Inspect the constructor and executor before describing a default as a hard pin or assuming one layer overrides another.
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
- **New payload fields preserve suspended-run compatibility.** Optional additive fields, explicit versioning or a validated migration can keep older snapshots resumable. This boundary isn't the same as a provider's required-field strict-output schema.
- **The suspension is recorded immediately before the run parks**, not after.
- **The operator surface distinguishes a live suspension from a dead run.** A stale heartbeat or a claimed run with no progress is not a question awaiting an answer, and showing it as one wastes the person's time.
- **Ledger or state tokens are mapped to labels at the operator surface.**
- **What is serialised is what reaches the wire.** A payload type existing server-side is not evidence the payload is transmitted. Check the emitted event, not the type.

## State and storage

- **Any write a later step depends on throws on failure.** Only genuine telemetry is best-effort. A silently failed load-bearing write produces a run that looks fine and is not.
- **Engine working state and surface-facing events are separate types with separate size bounds.**
- **The snapshot size was measured at the end of a real run**, not assumed from the shape of the data. The stored snapshot is the last write that succeeded, so where a write failed, the payload to measure is the one reconstructed rather than the one on disk.
- **Count store round-trips for the actual execution lane.** Memory, workflow snapshots and observability can issue several reads/writes per turn, especially through a durable adapter. Measure those calls and request sizes before attributing latency to the model, tools or tracer; don't assume plain generation and durable chat have the same persistence path.
- **Storage adapter choice is deliberate and its cost model understood.** Per-step write cost that scales with snapshot size makes a long workflow quadratic.
- **Storage ownership and injection are explicit.** Reuse the configured provider where memory, workflows and telemetry are intended to share persistence. Deliberately separate stores are valid; accidental duplicate instances or a standalone memory-backed agent without its provider are not.
- **Missing storage configuration fails fast in production wherever state must outlive the process.** No in-memory fallback. Establish first what has to survive: agent memory, suspended runs, traces and scores kept for analysis, schedules and background tasks, and anything two processes share. Where nothing does, the in-memory warning is not a finding, and provisioning an adapter to silence it has caused its own incident.
- **Connection pools come from the project's shared helper where one exists.** Check whether nested/batch operations can wait on a connection they already hold; a single-connection pool can deadlock that path. Use documented adapter options or a supported pre-built pool rather than assuming an option was consumed.
- **Start-up DDL was tried over the connection the deploy actually uses**, or schema initialisation is separated from the runtime and the runtime role no longer creates tables. Poolers differ: some carry initialisation fine, and a specific combination of pooler and connection option is what fails. Any schema tool sharing that database allow-lists the runtime-owned tables so a push cannot offer to drop them.
- **A storage-adapter change needs runtime acceptance.** Check startup, schema ownership and the connection the deployed runtime actually uses. Compilation cannot establish persistence or recovery. Coordinate schema and deployment effects under the task's permissions.

## Invocation boundaries

A durable run is many invocations, often in different processes, and frequently on a platform that kills the one that started it.

- **No state crosses an invocation through process memory.** Module-level maps, registries and signals read by an `onError` hook, a finalizer, a reconciler or a terminal write are empty in the process that actually runs them, and empty reads as nothing to do. The worker owning the work writes its own heartbeat; a poller writing it reports liveness nobody has.
- **A terminal write merges into the durable log rather than replacing it.** The process writing the ending rarely holds what the run accumulated.
- **A workflow is not started fire-and-forget from a request handler on a platform that freezes the function after the response.** The stored run stays running with nothing driving it, which reads as a hung run rather than a dropped one. Start it under the platform's after-response primitive, await anything whose completion matters, or hand it to a durable engine. Where a boot-time restart of active runs is the recovery plan, check those steps are safe to re-drive.
- **Timeouts bound one item, not a batch.** A deadline wrapped around a whole fan-out has the reliability of its slowest call, and a route whose worst case exceeds the platform's duration ceiling is designed for resumable slicing rather than given more rope.

## Model calls inside runs

- **Verify tools and structured output against the configured provider.** See [contracts](contracts.md) for native results, schema conversion and supported remedies. If the acceptance journey requires retrieval, a schema-valid answer with no retrieval calls doesn't pass it.
- **A degenerate result fails at its consumer boundary.** Check the abort signal and expected native shape; preserve an explicit failure variant when the contract has one. Size cardinality against the bound, rather than only the example.
- **Behaviour the model must not exhibit is enforced by the call, not by prose.** A prompt asking an agent not to call tools is a request; `toolChoice` and an empty tool map are the contract.
- **Nothing a later step branches on is parsed out of model narration.** A classification scanned from free text against a list of candidate names resolves on whichever name appears first, which is a coin toss dressed as a field.

## Long agent loops

- **Completion is declared, never inferred from narration or stream closure.** Use the workflow's terminal state or an explicit completion operation for an auto-continuing agent. Some loop APIs only evaluate `stopWhen` on non-terminal finishes; inspect that path. A narration-only turn can close naturally without fulfilling the goal.
- **Handle no-progress turns explicitly.** A prompt alone doesn't guarantee a tool call or completion. Enforce the required action at the call/controller boundary where appropriate, and bound continuations without inventing no-op tool calls to keep the loop alive.
- **Prompts carry a resuming clause** so continuation does not re-run earlier phases.
- **Input is locked during auto-continuation**, or concurrent submits orphan streams.
- **Rounds are bounded by both step count and elapsed time.**
- **Every delegation carries its own bound.** A delegated call is its own generation with its own step limit, defaulting low and not inherited from the supervisor. A bound hit on a step that called a tool returns empty text, which reads as a failed answer and invites the supervisor to delegate the same prompt again.
- **A multi-call generation flow runs server-side with durable progress.** Driven a call at a time from a client, it dies on a refresh and cannot be resumed or replayed, and every reload pays the model cost again.

## Context and processor budgets

- **Measure before diagnosing a timeout.** Separate serialised tool definitions, result bytes, final provider prompt tokens, stored history and workflow snapshot size. A token cap on generated output doesn't bound any of the others. Request and response bodies can dominate an apparent gateway or model timeout.
- **Project model results and workflow state separately.** A compact `toModelOutput` can reduce prompt cost while a full tool/step result still bloats durable snapshots. Park bulk durably and pass references at the checkpoint boundary too.
- **Preserve required evidence across the decision.** A fixed last-N-tool-step window can discard identifiers and search results well below a real token limit, causing repeated retrieval and unsupported answers. Prefer a measured token budget and semantic retention of the current request, hard constraints and held identities. Check the actual installed limiter's guarantees.
- **Keep tool calls and results paired.** Trim or retain them together so the provider sees a valid conversation. Rewriting a dropped result as the assistant's own prose can make the model echo it as an assertion; inspect the provider prompt before enabling compact-history modes.
- **Processor order is behaviour.** Trace the final effective fields after all hooks, including `toolChoice`, tools and instructions. A repeat-failure guard can silently prevent a later presentation/completion action unless the final-step contract is applied in the correct order.
- **State belongs to the request that owns it.** Instantiate mutable guards/processors per request where needed, and test a second independent request. A shared singleton guard must not carry a previous run's failures or held results into another user.
- **Scorers inspect; processors intervene.** A registered scorer doesn't enforce a hard requirement during execution. Verify the hook that actually changes the request when claiming a runtime guard.
