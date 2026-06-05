---
name: mastraudit
description: Audit Mastra implementations in JavaScript/TypeScript codebases. Use when checking whether a codebase follows current Mastra guidance from the $mastra skill, keeps direct mastra/@mastra dependencies and imports contained, organizes Mastra code into agents/tools/workflows/prompts/memory/storage/runtime/observability/MCP/scorers domains, keeps product behavior in runtime/domain code instead of Mastra wrappers, and reports concrete remediation steps.
---

# Mastraudit

Audit a codebase for three things:

1. Mastra is implemented according to the current `$mastra` skill and the installed Mastra documentation.
2. Mastra is architecturally contained and organized: one approved package or module owns Mastra, and that owner uses domain folders instead of scattering agents, tools, prompts, workflows, runtime, memory, storage, observability, MCP, or scorers across the codebase.
3. Mastra implementation remains thin, typed, observable, and testable: the approved package exposes agent/workflow/tool surfaces, while runtime/domain packages own product behavior, provider adapters, parsing, persistence, ranking, scoring, and source extraction.

## Non-Negotiables

- Use `$mastra` before judging API correctness. Mastra changes quickly; do not rely on model memory for constructor signatures, model routing, storage, memory, workflow, or tool APIs.
- Exactly one package or module should own Mastra implementation. In a Turborepo, prefer one workspace package.
- Only the approved Mastra owner should declare `mastra` or `@mastra/*` dependencies, import from `mastra` or `@mastra/*`, or run direct Mastra CLI commands.
- Apps and other packages should call the approved owner's public API instead of constructing Mastra objects directly.
- Mastra wrappers must not become the product implementation. Agent-facing tools and workflow steps should delegate to runtime/domain services for provider calls, parsing, persistence, ranking, scoring, source extraction, filesystem artifacts, and business rules.
- Mastra tools should not call other Mastra tools as implementation details. If a single agent-facing operation composes multiple reads/writes, put that composition in runtime/domain code and expose one tool or workflow step around it.
- Tool contracts must be specific enough for agents and Studio. Prefer imported shared input/output schemas; avoid `outputSchema: z.unknown()` unless the result is genuinely opaque and documented.
- Product progress must be emitted through explicit domain events or workflow state, not inferred from observability exporter flush timing.
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
5. Manually review the approved owner against current Mastra docs:
   - TypeScript config supports ES2022/bundler semantics, directly or through an audited shared config.
   - Models use the current provider/model format required by `$mastra`.
   - Agents, tools, workflows, memory, storage, observability, and MCP usage match the installed docs.
   - Mastra runtime/registration code composes domain exports instead of hiding implementation in app code.
   - Prompts are not buried in unrelated files when they are shared, long, or reused.
   - Tests cover agent/tool/workflow contracts and any boundary-facing public API.
   - Studio or `mastra api` can inspect the implementation when runtime verification is needed.
6. Manually review the implementation-practice lens:
   - Package boundary:
     - Public exports are narrow. The normal package API is the configured Mastra singleton or a documented runtime bridge, not deep exports for every agent/tool/workflow.
     - App/API/CLI packages do not import Mastra internals or raw `@mastra/*` packages.
     - Barrel files do not hide the configured runtime graph when explicit singleton registration would be clearer.
   - Runtime ownership:
     - Provider clients, HTTP calls, retries, normalization, parsing, filesystem artifacts, persistence, ranking/scoring algorithms, auth decisions, and domain semantics live in runtime/domain packages.
     - Mastra tools keep stable IDs/descriptions/annotations/schemas and delegate directly.
     - Workflow steps orchestrate phases, progress, branching, bounded fan-out, merges, retries, and failure states; they do not hide heavy business logic.
   - Tool and agent contracts:
     - Prompt prose, configured tool maps, delegated tools, capability registries, public docs, and Studio-visible config describe the same capabilities.
     - Tool inputs that claim source-backed truth validate real source joins or locators at the contract boundary.
     - Direct tool surfaces stay lean. Routing agents do not need every delegated/internal capability loaded directly.
   - Observability and background work:
     - Sampling, payload size, label cardinality, prompt/completion redaction, high-volume span filtering, and exporter batching are bounded by environment.
     - User-visible progress is explicit and independent from trace export timing.
     - Long-running work uses accepted/observable async starts, background backpressure, timeouts, concurrency limits, progress throttling, and cleanup TTLs where relevant.
     - Client/server timing is split when browser-visible diagnostics matter.
   - Memory, models, and execution:
     - Memory is opt-in per surface. One-shot structured calls, routers, source inspections, browser checks, and classifiers usually disable memory or use read-only memory.
     - Conversational agents have prompt-growth controls such as token limiting.
     - Model policy is code-owned and role-based where possible; arbitrary hidden model strings in env vars are treated as drift unless intentionally tested.
     - Model/provider names, prices, and availability are verified through `$mastra`, installed routing setup, or current provider data before making claims.
   - Browser and field verification:
     - Browser agents are report-only unless mutation is explicitly required.
     - Local QA/auth bypasses are local-only, scoped, and tested when automated checks need operator routes.
     - Browser checks verify the user-facing signal: client console fields, response-header interpretation, mobile overflow, sticky footer overlap, sheet scrollability, generated copy in context, and route error payloads.
   - Testing:
     - Runtime/domain tests cover provider adapters, parsing, ranking, persistence, algorithms, retries, and injected clients.
     - Mastra wrapper tests cover IDs, descriptions, schemas, annotations, registration, direct delegation, and startup/import configuration.
     - Boundary tests guard provider endpoints, heuristic strings, nested tool imports, `SomeTool.execute(...)`, direct `fetch`, filesystem reads/writes, and other signals that product logic leaked into Mastra wrappers.
7. Report findings with severity, file paths, and concrete next steps. Clearly separate:
   - deterministic boundary findings,
   - documentation/API correctness findings from `$mastra`,
   - implementation-practice concerns.

## Remediation Guidance

When fixing issues:

- Move all Mastra setup, agents, workflows, tools, storage, memory, provider wiring, and runtime registration into the approved package.
- Move misplaced implementation files into domain folders.
- Move product behavior out of Mastra wrappers and into runtime/domain services. Keep the Mastra wrapper as the agent-facing ID, description, annotations, schemas, and delegation call.
- Replace Mastra tool-to-tool implementation calls with runtime/domain composition.
- Replace loose tool contracts with shared input/output schemas. Validate stable output fields before handing results to the model.
- Add explicit domain progress events or workflow state for user-facing progress.
- Add environment-bounded observability policy for sampling, payload limits, cardinality, and redaction.
- Extract shared or substantial prompts into `src/prompts/` or `src/agents/prompts/`.
- Export a narrow internal API from the approved package.
- Replace outside `mastra` or `@mastra/*` imports with imports from the approved internal package.
- Move `mastra` and `@mastra/*` dependencies from outside packages into the approved package.
- Keep app packages framework-focused.
- Keep test-only mocks separate from production paths.

After edits, rerun relevant package-scoped tests/typechecks and repeat the boundary searches.

Implementation drift signals are intentionally conservative. Confirm them manually before presenting them as defects:

- broad package exports from the approved Mastra package;
- direct `fetch` or filesystem implementation inside Mastra tools/workflows/storage;
- `outputSchema: z.unknown()` in tools;
- Mastra tool-to-tool `SomeTool.execute(...)` calls;
- direct `process.env` model selection in agents.
