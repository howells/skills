---
name: mastraudit
description: Audit Mastra implementations in JavaScript/TypeScript codebases. Use when checking whether a codebase follows current Mastra guidance from the $mastra skill, keeps direct mastra/@mastra dependencies and imports contained, organizes Mastra code into agents/tools/workflows/prompts/memory/storage/runtime/observability/MCP/scorers domains, keeps application behavior in runtime/domain code instead of Mastra wrappers, and reports concrete remediation steps.
---

# Mastraudit

Audit a codebase for three things:

1. Mastra is implemented according to the current `$mastra` skill and the installed Mastra documentation.
2. Mastra is architecturally contained and organized: one approved package or module owns Mastra, and that owner uses domain folders instead of scattering agents, tools, prompts, workflows, runtime, memory, storage, observability, MCP, or scorers across the codebase.
3. Mastra implementation remains thin, typed, observable, and testable: the approved package exposes agent/workflow/tool surfaces, while runtime/domain packages own application behavior, provider adapters, parsing, persistence, ranking, scoring, and data extraction.

## Non-Negotiables

- Use `$mastra` before judging API correctness. Mastra changes quickly; do not rely on model memory for constructor signatures, model routing, storage, memory, workflow, or tool APIs.
- Exactly one package or module should own Mastra implementation. In a Turborepo, prefer one workspace package.
- Only the approved Mastra owner should declare `mastra` or `@mastra/*` dependencies, import from `mastra` or `@mastra/*`, or run direct Mastra CLI commands.
- Apps and other packages should call the approved owner's public API instead of constructing Mastra objects directly.
- Mastra wrappers must not become the application implementation. Agent-facing tools and workflow steps should delegate to runtime/domain services for provider calls, parsing, persistence, ranking, scoring, data extraction, filesystem artifacts, and business rules.
- Mastra tools should not call other Mastra tools as implementation details. If a single agent-facing operation composes multiple reads/writes, put that composition in runtime/domain code and expose one tool or workflow step around it.
- A multi-stage process should usually be a workflow, not a convenience tool that hides several internal phases. Do not keep duplicate Mastra tools for workflow-owned operations unless an agent genuinely needs that atomic capability.
- Tool contracts must be specific enough for agents and Studio. Prefer imported shared input/output schemas; avoid `outputSchema: z.unknown()` unless the result is genuinely opaque and documented.
- Tool IDs, filenames, prompt references, capability registry entries, and Studio-visible names should describe the same verb-noun operation.
- Agent and root surfaces should be deliberately small. Avoid `tools: "all"`, pseudo-agents, unused wrappers, low-level adapter utilities, and broad factories that make Studio or MCP look broader than the real orchestration graph.
- Long-running tools may opt into background tasks explicitly by tool key; short deterministic reads, checks, and routing decisions should normally stay foreground so the model receives immediate feedback.
- Application progress must be emitted through explicit domain events or workflow state, not inferred from observability exporter flush timing.
- User-facing Mastra output needs an explicit quality contract. Prompt instructions, output validation, persistence-time normalization, and render-time display transforms should agree instead of relying on prompt text alone.
- Mastra implementation code must be organized by domain under `src/`, using folders such as:
  - `agents/`
  - `tools/`
  - `workflows/`
  - `prompts/` or `agents/prompts/` when prompts are shared or substantial
  - `memory/`
  - `storage/`
  - `runtime/`
  - `observability/`
  - `mcp/`
  - `scorers/` or `evals/`

## Audit Workflow

1. Identify the repo root. Prefer the current working directory when it contains `turbo.json`, `pnpm-workspace.yaml`, or a workspace `package.json`.
2. Identify the approved Mastra owner:
   - Use the user's explicit package path/name if provided.
   - Otherwise inspect package manifests and imports. Auto-detect only when exactly one workspace declares `mastra` or `@mastra/*` dependencies.
   - If zero or multiple candidates exist, report ambiguity and ask the user to choose before remediation.
3. Load `$mastra` and follow its current-docs workflow:
   - Check whether Mastra packages are installed.
   - Prefer embedded docs for the installed version.
   - Use source/types only when embedded docs are insufficient.
   - Use remote docs only when packages are unavailable.
4. Inspect deterministic boundary signals with ordinary repo search:
   - `package.json` files declaring `mastra` or `@mastra/*`.
   - Source files importing from `mastra` or `@mastra/*`.
   - Package scripts invoking the Mastra CLI.
   - Mastra-looking config/source files outside the approved owner, such as `mastra.config.*`, `mastra.ts`, `src/mastra/**`, or `.mastra/**`.
   - Broad public exports from the approved owner that expose agents, tools, workflows, storage, memory, scorers, processors, schemas, or prompt internals.
   - Tool files where the declared `id` does not match the filename's verb-noun operation.
   - `tools: "all"`, broad generated agent/tool factories, unused tool wrappers, pseudo-agent IDs, and low-level adapter wrappers that are not part of the configured Mastra surface.
   - Deleted or intentionally avoided abstractions reappearing as folders, imports, identifiers, metadata, documentation, or diagrams.
5. Manually review the approved owner against current Mastra docs:
   - TypeScript config supports ES2022/bundler semantics, directly or through an audited shared config.
   - Models use the current provider/model format required by `$mastra`.
   - Agents, tools, workflows, memory, storage, observability, and MCP usage match the installed docs.
   - Mastra runtime/registration code composes domain exports instead of hiding implementation in app code.
   - Workflow runs use the installed API shape, such as awaiting async run creation when required by local types.
   - Prompts are not buried in unrelated files when they are shared, long, or reused.
   - Tests cover agent/tool/workflow contracts and any boundary-facing public API.
   - Studio or `mastra api` can inspect the implementation when runtime verification is needed.
   - At least one bounded normal-singleton smoke exists for critical execution paths; test-mode success alone is not proof that storage, observability, background tasks, and registration work together.
6. Manually review the implementation-practice lens:
   - Package boundary:
     - Public exports are narrow. The normal package API is the configured Mastra singleton or a documented runtime bridge, not deep exports for every agent/tool/workflow.
     - App/API/CLI packages do not import Mastra internals or raw `@mastra/*` packages.
     - Barrel files do not hide the configured runtime graph when explicit singleton registration would be clearer.
     - Registries, external metadata, public docs, and static diagrams reference actual configured agents, workflows, and tools, not future or deleted surfaces.
     - Every top-level registered agent has matching metadata when the codebase maintains a capability registry or similar index, and executable IDs match exactly even when user-facing groups use friendlier labels.
   - Runtime ownership:
     - Provider clients, HTTP calls, retries, normalization, parsing, filesystem artifacts, persistence, ranking/scoring algorithms, auth decisions, and domain semantics live in runtime/domain packages.
     - Mastra tools keep stable IDs/descriptions/annotations/schemas and delegate directly.
     - Workflow steps orchestrate phases, progress, branching, bounded fan-out, merges, retries, and failure states; they do not hide heavy business logic.
     - Workflows and agent-facing tools share the same runtime schemas and canonical services for equivalent operations.
     - Host-framework entry points that trigger Mastra runs create, observe, and return run state; they do not duplicate workflow or runtime write policy.
   - Tool and agent contracts:
     - Prompt prose, configured tool maps, delegated tools, capability registries, public docs, and Studio-visible config describe the same capabilities.
     - Tool inputs that claim external, persisted, or user-provided truth validate the relevant references at the contract boundary.
     - Direct tool surfaces stay lean. Routing agents do not need every delegated/internal capability loaded directly.
     - Provider or adapter choice stays behind domain/runtime services unless choosing that provider is itself the user-facing capability.
     - If a prompt, contract, or capability registry names a delegated tool or agent, that executable surface is really registered or attached.
     - Agent files should be readable as the orchestration surface: model role, instructions, memory, tools, workflows, scorers, and background-task policy should not be hidden behind broad factories.
   - Observability and background work:
     - Sampling, payload size, label cardinality, prompt/completion redaction, high-volume span filtering, and exporter batching are bounded by environment.
     - User-visible progress is explicit and independent from trace export timing.
     - Long-running work uses accepted/observable async starts, background backpressure, timeouts, concurrency limits, progress throttling, and cleanup TTLs where relevant.
     - Client, host-framework, runtime, model, storage, and transport timing are distinguishable when user-perceived latency matters.
     - Verification-visible telemetry exposes correlation id, model id, model role, request or operation duration, actionable internal stage, and bounded stage breakdowns for user-facing generation.
     - Telemetry collection is best-effort after validation and should not create user-visible failures for otherwise successful application behavior.
     - Request, auth, routing, and transport failures are distinguishable from Mastra, model, memory, and workflow failures.
   - Memory, models, and execution:
     - Memory is opt-in per surface. One-shot structured calls, routers, inspectors, checks, and classifiers usually disable memory or use read-only memory.
     - Conversational agents have prompt-growth controls such as token limiting.
     - Generation call settings (`maxOutputTokens`, `temperature`, `topP`) reach a Mastra `agent.generate`/`stream` call only under `modelSettings`. Mastra silently ignores them at the top level, so flat options drop the cap and the model runs at its full output budget. Confirm every cap is nested under `modelSettings`, not spread flat — this is the common failure when any AI-SDK-flat options object (e.g. the output of a shared options helper meant for AI-SDK `generateText`/`streamText`) is handed to a Mastra agent instead, and it is invisible because `providerOptions`/`toolChoice` do align at the top level, so it half-works and typechecks. **This is the canonical `modelSettings` footgun referenced below.**
     - Agents whose generate/stream options carry only `maxSteps`/`structuredOutput` and no `modelSettings.maxOutputTokens` run uncapped at the model's full budget; treat unbounded user-facing or high-volume generation as a cost and runaway risk, not an accepted default.
     - Reasoning controls are confirmed to actually bound the model, not assumed. Some providers ignore `reasoning.maxTokens` (e.g. OpenRouter for several models), so a low/small reasoning cap can still reason unboundedly — slow, or eating the whole `maxOutputTokens` budget and returning empty content. For latency-sensitive prose turns, disable reasoning explicitly (`providerOptions.<provider>.reasoning.enabled: false`) rather than trusting a token cap.
     - Model policy is code-owned and role-based where possible; arbitrary hidden model strings in env vars are treated as drift unless intentionally tested.
     - Model/provider names, prices, and availability are verified through `$mastra`, installed routing setup, or current provider data before making claims.
     - User-facing generation surfaces record model role and model id in testable logs or response metadata so quality and cost decisions can be traced to real runs.
   - Runtime and field verification:
     - Automated verification agents are report-only unless mutation is explicitly required.
     - Verification-only auth or environment bypasses are local-only, scoped, and tested.
     - Field checks verify the user-facing signal, relevant response metadata, error payloads, accessibility/responsive behavior where applicable, and generated output in context.
     - Field checks inspect persisted or reloaded output when the product stores generated content, not only fresh stream text.
     - Expected local-development, navigation, cancellation, cache, and session-state failures are separated from product, model, or Mastra defects.
   - Testing:
     - Runtime/domain tests cover provider adapters, parsing, ranking, persistence, algorithms, retries, and injected clients.
     - Mastra wrapper tests cover IDs, descriptions, schemas, annotations, registration, direct delegation, and startup/import configuration.
     - Boundary tests guard provider endpoints, heuristic strings, nested tool imports, `SomeTool.execute(...)`, direct `fetch`, filesystem reads/writes, and other signals that product logic leaked into Mastra wrappers.
     - Contract tests pin registered root agents, focused agent tool lists, workflow IDs, registry IDs, deleted abstractions, and background-task eligibility.
     - Retry/recovery tests cover partially completed user-initiated runs, normal singleton smoke scripts, and incomplete local-development runs when the product supports retry.
7. Report findings with severity, file paths, and concrete next steps. Clearly separate:
   - deterministic boundary findings,
   - documentation/API correctness findings from `$mastra`,
   - implementation-practice concerns.

## Remediation Guidance

When fixing issues:

- Move all Mastra setup, agents, workflows, tools, storage, memory, provider wiring, and runtime registration into the approved package.
- Move misplaced implementation files into domain folders.
- Move application behavior out of Mastra wrappers and into runtime/domain services. Keep the Mastra wrapper as the agent-facing ID, description, annotations, schemas, and delegation call.
- Replace Mastra tool-to-tool implementation calls with runtime/domain composition.
- Replace loose tool contracts with shared input/output schemas. Validate stable output fields before handing results to the model.
- Rename tool files, tool IDs, prompt references, registry rows, and tests together so one operation has one stable executable name.
- Add explicit domain progress events or workflow state for user-facing progress.
- Add environment-bounded observability policy for sampling, payload limits, cardinality, and redaction.
- Add actionable verification metadata: correlation id, model id/role, host duration, request or operation stage, internal Mastra/runtime stage, and bounded stage breakdowns.
- Extract shared or substantial prompts into `src/prompts/` or `src/agents/prompts/`.
- Export a narrow internal API from the approved package.
- Replace outside `mastra` or `@mastra/*` imports with imports from the approved internal package.
- Move `mastra` and `@mastra/*` dependencies from outside packages into the approved package.
- Keep app packages framework-focused.
- Keep test-only mocks separate from production paths.
- Delete unused adapter utility tools, unused wrappers, pseudo-agents, duplicate workflow-control tools, and misleading abstractions unless they are part of a deliberate documented Mastra design.
- Move generated-output validation and normalization into shared prompt, persistence, and display helpers rather than patching one surface at a time.
- Nest AI-SDK call settings (`maxOutputTokens`, `temperature`, …) under `modelSettings` on every Mastra `agent.generate`/`stream` call (the canonical footgun above), and funnel options through one shared options-mapping helper so flat AI-SDK options can never reach an agent unwrapped; add a test or lint asserting `maxOutputTokens` never appears at the top level of a Mastra generate/stream call. Set an explicit `modelSettings.maxOutputTokens` on agents that currently pass only `maxSteps`/`structuredOutput`.
- Add a bounded normal-singleton smoke for critical execution paths and shut down one-off background managers explicitly in diagnostic scripts.

After edits, rerun relevant package-scoped tests/typechecks and repeat the boundary searches.

Implementation drift signals are intentionally conservative. Confirm them manually before presenting them as defects:

- broad package exports from the approved Mastra package;
- direct `fetch` or filesystem implementation inside Mastra tools/workflows/storage;
- `outputSchema: z.unknown()` in tools;
- Mastra tool-to-tool `SomeTool.execute(...)` calls;
- direct `process.env` model selection in agents.
- `tools: "all"` or registered surfaces that grow whenever a file is added;
- tool IDs that diverge from filenames, prompts, registry rows, documentation, or diagrams;
- schema/capability entries for tools, workflows, or agents that are not actually registered or attached;
- pseudo-agent names in runtime plans, registries, or documentation;
- provider-specific tools exposed where a domain operation should own provider policy;
- generated agent, tool, or workflow factories that hide the Studio-visible graph;
- background-task configuration that applies to all tools instead of named long-running operations;
- user-facing generated content that depends on hidden context when the surface needs to stand alone;
- response logs that report only request duration without model id, model role, or actionable internal stage;
- generation call settings (`maxOutputTokens`, `temperature`, `topP`) passed at the top level of a Mastra `agent.generate`/`stream`/`defaultOptions` call instead of nested under `modelSettings` — the canonical footgun above (silently dropped, so the model runs at its full output budget);
- Mastra agents whose generate/stream options carry only `maxSteps`/`structuredOutput` with no `modelSettings.maxOutputTokens` (uncapped output at the model's full budget by omission — same end-state as a dropped cap);
- reasoning caps assumed to bound a model where the provider ignores them (e.g. OpenRouter `reasoning.maxTokens`), or a configured `outputLength`/`maxOutputTokens` that never reaches the agent because of an options-shape mismatch.
