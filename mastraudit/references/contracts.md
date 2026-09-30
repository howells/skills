# Agents, tools and structured output

Read this before introducing a model-facing contract or changing a model, provider, tool schema or result adapter. Verify examples against the installed Mastra types; provider constraints apply to the actual configured mode.

## Native output first

Use `structuredOutput: { schema }` and consume the native `response.object`, completed stream object or workflow `run.output` appropriate to that API. Validate through the canonical domain schema at the consumer boundary. Natural-language chat remains text.

Brace extraction, markdown-fence removal, `JSON.parse(response.text)`, object-to-text-to-object round trips and filling omitted fields conceal the failing boundary. Keep failure explicit: throw, or return a declared failure variant the caller handles. A provider refusal, abort, truncation or validation failure must not become an apparently successful empty result, fabricated score or default fact. If the application deliberately substitutes a fallback, preserve its failure/substitution status all the way to the consumer.

Model-facing and domain schemas can differ for a documented provider restriction, but their mapping is explicit and validated. Don't weaken the domain schema or use `unknown` to mask a missing producer-owned output contract.

## Inspect the schema that reaches the provider

The TypeScript type and the schema builder's name don't establish compatibility. Generate the JSON Schema through the installed conversion path. Inspect the root, every nested object, required properties, unions, defaults and unsupported keywords. A serializer change is a compatibility change even if the Zod code is unchanged.

For OpenAI strict Structured Outputs, verify the current [supported schema rules](https://developers.openai.com/api/docs/guides/structured-outputs): object root, required fields and `additionalProperties: false` on objects. Wrap a root array or union in an object such as `{ items: [...] }`. Represent genuinely absent values with required nullable fields when that mode requires it; don't manufacture sentinels to satisfy the schema. Nested `anyOf` can be supported while a root `anyOf` cannot.

Some schema conversions emit `oneOf` for a discriminated union and `anyOf` for a plain union. Check the installed serializer and the provider's supported subset rather than banning a builder by name. Where necessary use tagged object arms inside a supported nested union. Verify discriminator values and domain validation still distinguish the arms. Check both tool-input and final-output schemas after a provider swap.

## Tools and structured output together

Support varies by provider and model. A schema-valid object alone doesn't establish that required retrieval occurred. When the journey requires tool use, inspect actual calls and retrieved identifiers.

Mastra's documented choices are capability-aware `jsonPromptInjection: 'auto'`, a separate `structuredOutput.model`, or `prepareStep` separating acting from structuring. Choose the supported route for the installed version and configured provider. Explicit injection is a scoped compatibility choice, with a reason and a regression case, rather than a default to copy everywhere.

A separate structuring model adds another generation, cost and latency; it may also change which conversation context is available. Don't add it just to silence a type error. Check callback delivery for the chosen mode: schema-only structuring can differ from text generation and a separate structuring model. A supported `onStepFinish` combination is not automatically a defect, and a type-compatible callback is not evidence that it fires.

Set generation controls where the installed execution API reads them, usually `modelSettings`, and cap output deliberately. Additional call-level `system` context can supplement instructions; call-level `instructions` can replace them. The nested `structuredOutput.instructions` field is another contract again. Inspect the specific field before adding policy.

## Tools expose useful decisions

- Use explicit attachment keys. The agent can see the tool-map key rather than the declared tool id. Apply the project's naming convention consistently across prompts, registry and protocol output; inspect the emitted names.
- Keep descriptions discriminating and definitions compact. Measure serialised definitions separately from per-call results. Use the project's declared budgets, not numbers copied from another application.
- Return bounded identity, names, selected facts, evidence references and continuation information. Preserve distinctions such as excluded, unresolved, empty and failed. Put large source documents and full result sets behind explicit retrieval operations.
- Use `toModelOutput` when the installed API supports a separate model projection. Retain the canonical full result where consumers need it. A compact projection must preserve the facts and identifiers needed for the next decision.
- Validate output at its owning producer, then reuse that contract in Mastra, REST and SDK adapters. Adding a key, selector or strictness rule requires checking a real consumer, including nested unions and their refusal paths.
- A supervising agent that needs identifiers must receive a declared structured result or its own constituent operation. A delegated agent's progress prose or rendered page is not an identifier contract. Use native delegation where it fits, and keep each child's limits explicit.
- Registries are the definition source where the application adopts that pattern. Derive inspector and advertised capabilities from real definitions; remove deleted entries and callers together.

## Protocol mapping is an adapter contract

Mastra's `MCPServer` and an official SDK `McpServer` are different classes. A helper expecting `registerTool` isn't compatible just because both speak MCP. Verify actual methods, transport and extension support before wrapping one with another SDK's server helper.

A normal domain tool returns its domain result; the server owns MCP wrapping and error mapping. An MCP App intentionally exposing protocol `content` and `structuredContent` is a different path. Inspect how the installed server handles it so it isn't double-wrapped or validated against the wrong output schema. Preserve named errors and `isError` through the protocol. Test invalid input using a real MCP client if the Studio tool form drops error detail.

Public source: [Mastra structured output](https://mastra.ai/docs/agents/structured-output). Installed types and transport responses decide whether those features exist in the version being used.
