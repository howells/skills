---
name: mastraudit
description: "Mastra mistakes that typecheck and fail at runtime, in agents, tools, workflows, storage, Studio and MCP Apps. Use when writing, debugging or auditing Mastra code."
---

# Mastraudit

Mastra's APIs move fast and its expensive mistakes typecheck. Prevent them where the code makes them. The reference files describe recurring failure classes, not universal semantics: confirm against the installed version before flagging one.

An audit-only request permits source reading and safe local checks, not model calls, workflow runs, storage writes or deploys. Rank findings blocking, should fix or noted, each with `file:line`, consequence and fix.

## Before changing code

1. **Use the installed version, not memory.** From the package that makes the call, read `node_modules/@mastra/<pkg>/package.json` for the version and check every option you write against its `.d.ts` files and, where shipped, `dist/docs/references/*.md`. This covers the CLI and the storage and engine adapters too; a manifest range or catalog entry isn't the installed version. Fall back to published docs only when nothing is installed, and say so.
2. **Follow the working precedent.** Find the existing bridge, storage provider, model policy and domain operation. Name the execution lane (plain agent, durable workflow, Studio chat, HTTP or stdio MCP) and what constructs and registers it. Before changing ownership, registration or imports, read [references/structure.md](references/structure.md).
3. **Set the contract and the bounds.** Output shape, explicit failure and completion states, the identifiers that cross each step, and limits on output, steps, elapsed time and retries. Before writing a tool or structured output, read [references/contracts.md](references/contracts.md); before a workflow, state, storage or a long loop, read [references/execution.md](references/execution.md). Read each reference file with its own command.

## Gotchas that typecheck

- **Generation settings nest under `modelSettings`.** Flat `maxOutputTokens`, `temperature` or `topP` are silently ignored; the most repeated mistake. Cap output on every user-facing or high-volume call. Legacy generate and stream methods differ, so check the signature.
- **Call-level `instructions` replaces the agent's instructions; `system` adds to them.** Policy added through `instructions` silently breaks tool routing.
- **The tool-map key is the name the model sees,** not the tool's `id`. Use explicit `verb_noun` keys; shorthand leaks camelCase into tool selection.
- **Step limits default low** and cap how many tool calls an agent can chain. Set one on every tool-holding agent and on each delegated agent, which doesn't inherit its supervisor's. A limit hit after a tool call returns empty text, which a supervisor reads as failure and re-delegates.
- **Use native structured output:** `structuredOutput: { schema }` and the native object. Never `JSON.parse(response.text)`, strip fences or fill missing fields. Refusals, truncation and validation failures stay visible failures.
- **Inspect the JSON Schema that reaches the provider,** not the Zod type. Re-check every tool and sub-agent schema after a model or provider swap; a rejected schema arrives as a refused call, not a warning.
- **Mastra wraps; domain code implements.** Tool `execute` bodies delegate in about a line. No HTTP, parsing, persistence or business rules in wrappers, and no tool calling another tool.
- **Nothing heavy is reachable from the singleton** that request handlers import, and no build-time or `server-only` module sits in its runtime graph. Both pass typecheck and fail at boot.
- **Every MCP client gets an explicit id and is memoised at module scope.** A second identical client without an id throws, and hot reload builds one.
- **A retry re-runs the whole step body,** writes included. Make side effects idempotent by natural key, set retries per step, and never retry billing, quota or auth failures.
- **Don't fire-and-forget a workflow from a request handler** on a platform that freezes after the response; the run shows as running forever. Use the after-response primitive, await it, or hand it to a durable engine.
- **No state crosses invocations through process memory.** Module-level maps read by `onError`, finalizers or reconcilers are empty in the process that runs them.
- **No in-memory storage fallback where state must outlive the process.** Where nothing must, the in-memory warning isn't a finding; don't provision storage just to silence it.
- **Memory is opt-in per surface.** Routers, classifiers and one-shot structured calls don't carry it.
- **Enforce with the call, not the prompt.** `toolChoice` and the tool map are the contract. Never branch on a value scanned out of model narration.
- **Saving a watched file reloads Studio and kills in-flight generations.** Hold edits during a timed run, and count reloads separately from model failures.

## When something fails

Reproduce once, minimally, before blaming a provider, changing a dependency or adding a fallback: request size, effective settings, identity, source version and persisted state. Change one cause at a time. Before debugging a symptom below, read its file.

| Symptom | Look first at |
| --- | --- |
| Empty object, ignored tools, rejected schema | Native result, emitted provider schema, tools plus structured output: [contracts](references/contracts.md) |
| Slow steps, repeated searches, forgotten facts | Measured prompt, result and snapshot size; processor retention: [execution](references/execution.md) |
| Lost progress, duplicate writes, stuck resume | Checkpoints, identity, idempotency, durable state: [execution](references/execution.md) |
| Unit tests connect or write unexpectedly | Import-time initialisation, env precedence: [evidence](references/evidence.md) |
| Studio won't load, hangs bundling, loses a run | Origin, dependency graph, reload window: [Studio and MCP](references/studio-and-mcp.md) |
| Fixed over HTTP, still broken in an MCP session | Stdio process start time: [Studio and MCP](references/studio-and-mcp.md) |
| Inline HTML works, agent UI doesn't | Tool metadata, resource, result envelope, handshake: [Studio and MCP](references/studio-and-mcp.md) |
| Scores pass, answer breaks the brief | Independent expectations, hard requirements: [evidence](references/evidence.md) |

## Done

Exercise the changed journey in its real host: a visible feature through its UI or MCP host, a durable one by reading its stored output and resuming it. Read the dev-server log for framework error ids even on a pass. Before writing tests or evals, read [references/evidence.md](references/evidence.md).

Report the installed versions, what ran where, and what stayed unverified.
