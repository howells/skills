# Studio and MCP

Running Studio, reading its failures, cross-package imports and inline MCP Apps. Work with the runtime's owner; don't stop a peer's process or in-flight run.

## What is running

- **Record the process, command, actual port, browser origin and API target.** Use the project's script and printed URL, not a default port. A background task's time limit can stop a healthy server.
- **HTTP MCP on a deployed endpoint and stdio MCP from local source are different.** A stdio session may load its code once; a deployed fix doesn't reach it. Check its start time and reconnect or launch a fresh client before reopening a fixed defect.
- **Diagnose the effective env source.** An exported shell credential can override an env file, or a project helper the shell. Never print or copy credentials into logs, briefs or arguments.
- **`Failed to load Studio`: read the failed browser request first.** `localhost` and `127.0.0.1` are different origins, and credentialed requests can't use a wildcard origin. Match the configured origins; don't loosen CORS to hide a mismatch.

## Reloads and stale builds

- **File deletions and new cross-package exports can break the watcher's dependency graph.** Stuck at `Bundling...`, an old tool list, or a missing export after a successful rebundle means a clean restart, not repeated cache deletion. Coordinate it with the owner.
- **Installed source, generated `.mastra` output and served browser assets are separate artefacts.** A changed version or removed patch means nothing while the host serves a cached bundle; compare the browser's actual asset URLs and full bundle to the installed distribution.
- **Reproduce a suspected vendor regression on the installed build with one controlled case** before pinning or upgrading. A bundle diff or remembered changelog is a lead.

## Execution lanes and processors

- **Plain generation, thread chat and a durable adapter can take different paths.** An adapter may mutate the agent it wraps; if it reroutes thread runtime, give it a dedicated Agent definition. Verify the lane through both generation and the real chat endpoint, with logs and trace correlation.
- **Studio's registry, detail endpoint and rendered list can disagree about processors.** Check the hook methods and confirm invocation at the provider boundary; don't add a dummy hook to make a UI count agree.

## Inline app contract

MCP Apps serve HTML resources over MCP for a host to render. Browser WebMCP exposes a page's tools to a browser agent. One doesn't imply the other.

For an MCP App, check the installed server's and target host's extension support against [Mastra MCP](https://mastra.ai/docs/connections/mcp) and the [MCP Apps SDK](https://github.com/modelcontextprotocol/ext-apps), then verify the wire:

1. `tools/list` keeps the tool's UI resource URI, visibility and any host-specific entrypoint metadata.
2. The resource read serves that exact `ui://` URI with the supported HTML profile, metadata and CSP; bundle guest dependencies where the host requires it.
3. The result separates concise model-facing `content` from UI data in `structuredContent` or another supported channel. Initial delivery and later guest calls can use different host envelopes; unwrap only measured or documented shapes.
4. The guest registers handlers before connecting, receives arguments and results, renders them, and uses the SDK's host methods. An iframe or successful resource read doesn't prove the handshake.
5. A real host interaction changes a selection, sends revised arguments, gets the right result and updates agent context where needed. A guest method that sends chat starts another paid model turn; a read-only tool call doesn't.

A plain Studio JSON tool form may have no custom field or async picker hook; an MCP App can own the picker where the host supports it.

## Acceptance in the host

Use real records whose identities expose assumptions. Check images, record links, selected identities, empty and error states, pagination exhaustion, a revised choice, dimensions and horizontal overflow. A host-owned accessibility violation such as a missing parent-iframe title belongs to the host; guest HTML can't fix it.

A saved Studio result proves saved rendering, a fresh agent call proves current invocation, a local preview proves that web host, and installation proves none of them. Report each separately.
