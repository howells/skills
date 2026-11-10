# Structure

Ownership, registration, imports and adapters. Apply the codebase's chosen boundaries; a private execution variant and several independently deployed apps can be legitimate.

## Containment

- **Each independently deployed Mastra implementation has one owner package.** Callers use its public API: the singleton or a documented bridge, not a deep export per agent, tool and workflow.
- **The boundary is the core package, not every `@mastra/*` import.** Infra clients such as an MCP client can legitimately live elsewhere. A blanket ban flags deliberate patterns.
- **No Mastra CLI script, `mastra.config.*`, `src/mastra/**` or `.mastra/**` outside the owner.**
- **The singleton is spelled out.** No factory or barrel hiding which surfaces are registered; what a reader can't see, a reviewer can't check.
- **Registries, docs and diagrams name only what is really registered.** Remove deleted entries with their callers.
- **Heavy or optional dependencies attach where they are used,** not to an eagerly registered agent. Otherwise every route importing the singleton pulls them in and fails at module load. Check what the built route actually traced.
- **The runtime graph imports nothing build-time or server-only.** Deployers, `server-only` guards, module-load env validation and dynamic filesystem reads inside a dependency survive typecheck and fail at boot or first call.
- **Runtime dependencies come through the owner.** A standalone definition doesn't get the singleton's storage, telemetry or registry injection; check each dependency it uses. Don't create a second full Mastra instance to override one lookup, or register a private variant publicly to get storage.
- **Trace singleton import cycles before blaming the bundler.** Workflow → runtime adapter → singleton → workflow fails at module initialisation.

## Orchestration

- **Composition lives in domain code.** Where one agent-facing operation composes several reads or writes, expose one tool or step around a domain function.
- **No duplicate tool for an operation a workflow owns,** unless an agent genuinely needs it atomically and that is written down.
- **Use a workflow when checkpoints, progress or recovery are required,** not because an operation has several lines.
- **Every step names the function it wraps.** A step with no callee describes a system nobody built, and nothing contradicts it: schemas typecheck, the graph renders.
- **Fix field names at the domain source.** Renaming in the wrapper hides the defect and guarantees drift.

## Agents and models

- **Model policy is code-owned and role-based,** and so is every behaviour-bearing setting. The environment holds secrets, not storage mode, background switches or cost profiles. Where a codebase chose otherwise, report it as a judgement call.
- **Measure reasoning behaviour for the models actually used,** not from a documented cap.
- **Conversational agents with memory have token limiting.**
- **Delegate with the framework's sub-agents or workflows-as-tools.** A hand-rolled delegate tool reimplements routing and hides the call from run observers.

## Tools

- **Tool id, filename, prompt reference, registry row and inspector name describe the same operation.** Apply the naming convention across prompts, registry and protocol output, and inspect the emitted names.
- **Input and output schemas are shared imports.** An opaque output type only where the result genuinely is opaque, and documented.
- **Identity and tenancy come from authenticated context,** never caller-supplied fields. Inputs that claim external or persisted truth validate that reference.
