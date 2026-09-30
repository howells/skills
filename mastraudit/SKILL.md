---
name: mastraudit
description: "Prevent recurring Mastra failures while building agents, tools, workflows and MCP Apps. Use before changes, during debugging and for focused acceptance. Not for general UI review (`fieldtest`)."
---

# Mastraudit

Use this as a building guide throughout Mastra work. Prevent the expensive mistakes at the point the implementation makes them. The existing name also supports an explicitly requested audit.

## Before changing code

1. **Find the runtime owner and the actual version.** Resolve packages from the package that calls them, including the CLI, storage and engine adapters. A manifest range, catalog entry or directory listing isn't an installed version. Read that version's embedded docs and types, plus the matching page in a configured local vendor mirror. A recent mirror can still describe a newer release. Use published documentation when local evidence is missing; state the gap.
2. **Read the working precedent.** Follow the existing public bridge, storage provider, model policy and domain operation. Identify the execution lane: plain agent, durable workflow, Studio chat, HTTP or stdio MCP. Trace what constructs it and what registration makes public. Read [structure](references/structure.md) for ownership and import changes.
3. **Choose the contract and the bound.** Specify the useful output, explicit failure and completion states, references that cross each step, and limits on output, steps, elapsed time and retries. Give an agent the operations it needs to decide; wrapping the whole deterministic workflow can make an agent comparison circular. Read [contracts](references/contracts.md) for tools or structured output, and [execution](references/execution.md) for stateful work.
4. **Choose the acceptance path before running it.** Name the one changed journey and its observable outcome. Check test/import side effects first. Audit-only scope permits source inspection and safe local checks, not model calls, workflow admissions, storage writes or deployments. Read [evidence](references/evidence.md) before tests, evaluations or completion claims.

This is a short implementation decision, not a new planning document. Keep evidence on the owning tracker item when the project uses one.

Reuse an established pre-flight for the same source, installed versions and runtime. Revisit the relevant contract when dependencies, imports, settings or the execution lane change; don't reread settled documentation or rerun a green gate after every save.

## While building

- Keep domain behaviour and canonical schemas at their source; Mastra wires them together. Inspect the glue that typecheck cannot validate: registration keys, generated schemas, output projection, callback delivery, storage injection, resume forwarding and model settings.
- Reuse applicable installed scanners. Read their signatures and coverage before invoking them. Scanner output is a lead until checked against the actual caller and supported contract. No scanner available means a stated coverage gap, not an invented package export.
- Establish a minimal reproduction before changing a dependency, adding a fallback or blaming a provider. Start with request size, effective settings, identity, source version and persisted state. Change one cause at a time.
- For Studio, coordinate a stable runtime window with its owner before a timed run. Read [Studio and MCP](references/studio-and-mcp.md) for origins, hot reload, stale bundles, local stdio and inline apps.
- Turn a demonstrated silent failure into the smallest useful guard at its shared boundary. Make it fail on the original adverse case before trusting it. Avoid a broad suite merely because a focused check passed.

## When something fails

| Symptom | First investigation |
| --- | --- |
| Empty object, ignored tools, rejected schema | Native result, generated provider schema and tools/structured-output compatibility in [contracts](references/contracts.md). |
| Slow steps, repeated searches, missing earlier facts | Measured prompt/result/snapshot size and processor retention in [execution](references/execution.md). |
| Lost progress, duplicate writes, stuck resume | Checkpoint, identity, idempotency and durable state in [execution](references/execution.md). |
| Unit tests connect or write unexpectedly | Import-time initialisation, environment precedence and driver guard in [evidence](references/evidence.md). |
| Studio fails to load, hangs bundling or loses a run | Process, origin, dependency graph and reload window in [Studio and MCP](references/studio-and-mcp.md). |
| Fix works over HTTP but fails in an existing MCP session | Transport identity and process start time in [Studio and MCP](references/studio-and-mcp.md). |
| Inline HTML works but agent UI does not | Tool metadata, resource, result envelope and guest-host handshake in [Studio and MCP](references/studio-and-mcp.md). |
| Scores pass but the answer breaks the brief | Independent expectations, hard requirements and persisted experiment evidence in [evidence](references/evidence.md). |

## Before calling it done

Exercise the changed path with the closest permitted evidence. A visible feature needs interaction in its intended host; a durable feature needs its stored output and recovery boundary inspected. When those effects aren't authorised, state the missing acceptance evidence.

Return a short verdict, what changed, the installed versions and exact source/runtime tested, focused evidence, and remaining gaps. Keep source checks, runtime execution, persistence, host interaction, publication and deployment as separate claims. An explicit audit ranks confirmed findings by failure cost: blocking, should fix, noted; each carries `file:line`, consequence and fix. Include a coverage map for skipped checks.

Stop when the stated acceptance condition is met. A new unrelated finding goes on the tracker, not into an open-ended round of extra checks.
