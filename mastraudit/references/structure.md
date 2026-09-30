# Structure

Read this before changing ownership, registration, imports or adapters. Apply the codebase's chosen boundaries; a private execution variant and several independently deployed applications can be legitimate.

## Containment

- **Each independently deployed Mastra implementation has a clear owner.** When the codebase uses one owner package, callers use its public API. Multiple independently deployed apps can have separate owners.
- **Containment is narrower than "no `@mastra/*` anywhere else".** The core package is the real boundary; infra clients such as an MCP client are legitimately used outside the Agent-construction boundary in some codebases. Where a shipped scanner defines the default set, adopt its calibration rather than asserting a stricter rule - a blanket ban produces false positives on a pattern the codebase chose deliberately. Widen the set explicitly when a codebase wants a package treated the same way.
- **No Mastra CLI script outside the owner**, and no stray `mastra.config.*`, `src/mastra/**` or `.mastra/**` in another package.
- **Code sits in domain folders**: `agents/`, `tools/`, `workflows/`, `prompts/`, `memory/`, `storage/`, `runtime/`, `observability/`, `mcp/`, `scorers/`.
- **Public exports stay narrow** - the singleton or a documented bridge, not a deep export per agent, tool and workflow.
- **The singleton is spelled out explicitly.** No factory or barrel file hiding which surfaces are actually registered. What a reader cannot see, a reviewer cannot check.
- **Registries, docs and diagrams name surfaces that are really registered.** Phantom and deleted entries mislead every later audit.
- **Nothing heavy or optional is reachable from the singleton that request handlers import.** An eagerly registered agent carrying a browser, a renderer or any large optional dependency pulls it into every route that imports the singleton, where it fails at module load rather than at use. Attach it where it is used, and check what the built route actually traced.
- **The runtime graph imports no build-time or server-only module.** Deployers, `server-only` guards, module-load environment validation and dynamic filesystem reads inside a dependency each survive typecheck and fail at boot or first call in production.
- **Runtime dependencies are injected through the intended owner.** Directly using a standalone definition can be valid, but it doesn't receive the singleton's storage, telemetry or registry injection automatically. Check each dependency it actually uses. Don't create a second full Mastra instance merely to override one lookup, or register a private execution variant publicly to obtain storage.

## Orchestrator discipline

Mastra orchestrates; it does not implement.

- **No provider client, HTTP call, parsing, persistence, ranking, scoring, filesystem access or business rule inside a Mastra wrapper.** All of it belongs in runtime or domain code.
- **Tool `execute` bodies are thin** - ideally one line delegating to a domain function.
- **No tool calls another tool as an implementation detail.** Where one agent-facing operation composes several reads or writes, put the composition in domain code and expose one tool or workflow step around it.
- **No duplicate tool for an operation a workflow owns**, unless an agent genuinely needs it atomically and that is written down.
- **Recoverable stages are explicit.** Use a workflow when its checkpoints, progress or recovery are required. A domain operation composing several bounded reads can still be one useful tool; don't introduce a workflow solely because it has several lines.
- **Every step names the function it wraps.** A step with no callee is a claim about a system nobody built, and nothing fails to contradict it: the schemas typecheck, the graph renders, and the description reaches readers as the truth. Check this before a contract is published or a diagram is shown to anyone.
- **Field names are correct at the domain source.** Renaming in the wrapper hides the real defect and guarantees the two drift.

## Agents and models

- **Generation settings nest under `modelSettings`.** `maxOutputTokens`, `temperature`, `topP` flat at the top level are silently ignored, which is the single most repeated mistake in this area. Legacy generate and stream methods are the exception - check the installed signature before flagging.
- **Every user-facing or high-volume generation caps output explicitly.** Uncapped by omission is the same defect as uncapped by intent.
- **A test asserts the cap never appears top-level.** This one is worth automating; a shipped scanner may already do it.
- **Additional policy rides as `system`, not `instructions`.** Where `instructions` overrides the agent's own instructions rather than supplementing them, a caller adding policy that way silently destroys tool routing - no error, just worse decisions. Verify which of the two overrides in the installed version.
- **Callback behaviour matches the configured structured-output mode.** Read [contracts](contracts.md) and the installed execution path. Schema-only output and a separate structuring model can have different callback behaviour; verify rather than banning a supported combination or adding a second generation as a reflex.
- **Reasoning behaviour was measured for the models actually used**, not assumed from a documented cap.
- **Model policy is code-owned and role-based, and so is every other behaviour-bearing setting.** Environment holds secrets, not configuration. Storage mode, background-task switches and cost profiles in the environment are the same defect as a model string there. Where a codebase treats this as its own convention, report it as a judgement call rather than a correctness finding.
- **Memory is opt-in per surface.** Routers, classifiers, inspectors and one-shot structured calls do not carry it. Conversational agents that do have token limiting.
- **Every tool-holding agent sets its step limit deliberately.** The limit caps sequential model calls and defaults low, so it governs both cost and how many tool calls an agent can chain before it stops.
- **Model-facing schemas match the configured provider's strict mode.** Inspect the emitted schema, including nested objects and union arms, as described in [contracts](contracts.md). Keep provider-specific schema restrictions separate from domain and resume compatibility.
- **A model swap re-checks every tool and sub-agent schema against that provider's validator.** Providers disagree about which generated JSON Schema they accept, and the disagreement surfaces as a refused call rather than a warning.
- **Delegation uses the framework's own sub-agents or workflows-as-tools.** A hand-rolled delegate tool reimplements routing the framework already owns and hides the delegated call from everything that observes runs.

## Tools

- **Tool map keys are explicit `verb_noun` strings.** The model-visible name is the object literal key where the tool is attached to the agent, which is a different thing from the tool's own declared id. Shorthand leaks camelCase into the model's selection surface, and a codebase can pass every naming-consistency check while still doing this.
- **Descriptions are plain language**: what it does, when to pick it, jargon glossed. The reader is a model choosing between options.
- **Names carry no implementation detail and no internal system names.** A tool named for caching, connection health or the service behind it teaches the model about plumbing it cannot act on.
- **MCP wrapping follows the installed adapter contract.** Ordinary domain output and intentional MCP App protocol output take different paths; see [contracts](contracts.md). Verify the actual error mapping and envelope. Identity and tenancy come from authenticated context rather than caller-supplied identity fields.
- **Tool id, filename, prompt reference, registry row and inspector name describe the same operation.**
- **Input and output schemas are shared imports.** An opaque output type is acceptable only where the result genuinely is opaque and that is documented.
- **MCP annotations are present** wherever the tool surface requires them.
- **Every MCP client construction passes an explicit id and is memoised at module scope.** A second client built with identical config and no id throws, which is a live risk under dev-server hot reload where a factory can run twice.
- **Inputs claiming external or persisted truth validate that reference** rather than trusting the caller.
