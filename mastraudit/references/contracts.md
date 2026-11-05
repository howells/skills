# Agents, tools and structured output

Model-facing contracts and provider compatibility. Provider constraints apply to the configured mode; check examples against the installed types.

## Native output

Use `structuredOutput: { schema }` and consume the native `response.object`, completed stream object or workflow `run.output`. Validate through the canonical domain schema at the consumer. Chat stays text.

Brace extraction, fence stripping, `JSON.parse(response.text)`, object-to-text-to-object round trips and filling omitted fields hide the failing boundary. Throw, or return a declared failure variant the caller handles. A refusal, abort, truncation or validation failure never becomes an empty result, fabricated score or default fact. A deliberate fallback carries its substitution status to the consumer.

Model-facing and domain schemas can differ for a documented provider restriction, with an explicit, validated mapping. Don't weaken the domain schema or use `unknown` to mask a missing output contract.

## The schema the provider sees

Generate the JSON Schema through the installed conversion path and inspect it: root, nested objects, required properties, unions, defaults, unsupported keywords. A serializer change is a compatibility change even with identical Zod.

- **OpenAI strict mode** ([rules](https://developers.openai.com/api/docs/guides/structured-outputs)): object root, every field required, `additionalProperties: false`. Wrap a root array or union, as `{ items: [...] }`. Represent absence as required nullable fields, not sentinels. Nested `anyOf` can work where a root `anyOf` can't.
- **Unions:** some converters emit `oneOf` for discriminated unions and `anyOf` for plain ones. Check the converter and provider subset rather than banning a builder; tagged object arms inside a supported nested union usually work. Confirm discriminators still separate the arms.
- Check both tool-input and final-output schemas after a provider swap.

## Tools and structured output together

Support varies by provider and model. A schema-valid object doesn't prove retrieval happened; when the journey needs tools, inspect the actual calls and retrieved identifiers.

Mastra's routes: capability-aware `jsonPromptInjection: 'auto'`, a separate `structuredOutput.model`, or `prepareStep` separating acting from structuring. Pick the one the installed version and provider support. Explicit injection is a scoped compatibility choice with a reason and a regression case, not a default.

A separate structuring model adds a generation, cost and latency, and may see different context; don't add it to silence a type error. Callback delivery differs by mode: a type-compatible `onStepFinish` isn't evidence it fires, and a supported combination isn't a defect.

`structuredOutput.instructions` is a third instruction field, distinct from call-level `system` and `instructions`. Inspect which one you're setting.

## Tool results

- **Keep definitions compact and results bounded.** Measure serialised definitions separately from per-call results, against the project's own budgets.
- **Return identity, names, selected facts, evidence references and continuation info.** Keep excluded, unresolved, empty and failed distinct. Put full documents and result sets behind explicit retrieval tools.
- **`toModelOutput` projects for the model while the full result stays for consumers.** The projection keeps the facts and identifiers the next decision needs.
- **Validate output at its producer and reuse that contract** in Mastra, REST and SDK adapters. A new key, selector or strictness rule gets checked against a real consumer, including nested unions and refusal paths.
- **A supervisor that needs identifiers gets a declared structured result,** not a delegated agent's progress prose or rendered page.
- **Derive inspector and advertised capabilities from real definitions** where the app uses a registry.

## MCP adapters

Mastra's `MCPServer` and the official SDK's `McpServer` are different classes; a helper expecting `registerTool` doesn't work on both. Verify methods, transport and extension support before wrapping one with the other's helpers.

An ordinary domain tool returns its domain result and the server owns MCP wrapping and error mapping. An MCP App deliberately returning `content` and `structuredContent` takes a different path; check the installed server so it isn't double-wrapped or validated against the wrong schema. Preserve named errors and `isError` through the protocol, and test invalid input with a real MCP client where Studio's tool form drops error detail.

Public source: [Mastra structured output](https://mastra.ai/docs/agents/structured-output).
