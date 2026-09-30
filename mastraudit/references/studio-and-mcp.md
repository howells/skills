# Studio and MCP

Read this before starting Studio, interpreting a Studio failure, changing cross-package imports or accepting an inline app. Work with the runtime owner; preserve peers' processes and in-flight runs.

## Establish what is running

Record the checkout and source state, command, owning process, actual listening port, browser origin and API target. Use the project's script and emitted URL rather than assuming a default port. A background task's time limit can stop an otherwise healthy server.

Distinguish HTTP MCP on a deployed endpoint from stdio MCP started from local source. An existing stdio session may load its code only once. A deployed fix doesn't update that process. Inspect its start time and source; reconnect or launch a fresh owned client before reopening a fixed defect. Keep local, deployed and long-lived-client evidence separate.

Check environment precedence without printing secrets. An exported shell credential can override an env-file value, while a project env helper can deliberately override the shell. Diagnose the effective source, not merely the presence of a value in a file. Resolve a stale exported value for the owned process using the intended secret loader. Never copy a credential into logs, briefs, plugin files or command arguments.

For `Failed to load Studio`, inspect the failed browser request first. `localhost` and `127.0.0.1` are different origins. Credentialed requests cannot use a wildcard allowed origin. Match the configured UI/API origins and credential policy; don't universalise one project's loopback hostname or loosen CORS to hide the mismatch.

## Hot reload and stale builds

A source save in the Mastra package or a watched domain dependency can reload Studio and kill an in-flight generation. Agree a quiet write window for a timed acceptance run. Record reloads separately from model failures; don't spend another run until the runtime is stable.

File deletion and new cross-package exports can invalidate the watcher's dependency graph. A watcher stuck at `Bundling...`, an old tool list, or a missing export after a successful rebundle can require a clean restart, rather than repeated cache deletion. Confirm the actual registered capability list and emitted module. Coordinate the restart with its owner and stop only the owned process or agreed port.

Installed dependency source, generated `.mastra` output and served browser assets are separate artefacts. Removing a patch or changing a version is not enough if the host still serves a cached bundle. Inspect the browser's actual asset URLs and compare the complete relevant bundle to the intended installed distribution, not only its loader. Rebuild/restart when needed and authorised. Honour an explicitly removed patch; record upstream host limitations rather than silently restoring it.

Reproduce a suspected vendor regression on the actual installed build with one controlled case. A bundle diff or a remembered version comparison is a lead. Before pinning or upgrading, verify the relevant upstream change and the application/client compatibility affected by it.

## Execution lanes and processors

Plain generation, thread chat/send-message and a durable adapter can follow different execution paths. An adapter may mutate the agent it wraps; if it changes thread runtime routing, give it a dedicated Agent definition rather than also using that instance for in-process chat. Verify the intended lane through both generation and the actual chat endpoint, with process logs and trace correlation.

Trace singleton import cycles before blaming bundling: workflow to runtime adapter to singleton to workflow can fail at module initialisation. Definitions depend on domain or engine code; an adapter that reads the singleton is not a safe dependency for constructing that singleton. A private execution variant may need explicit storage injection; creating another full Mastra instance can duplicate storage, observability and public registration.

Studio's registry, detail endpoint and rendered list can disagree about processors. Inspect the actual hook methods and source responsible for detecting phases before treating a missing row as a missing runtime guard. Confirm invocation at the provider boundary. Don't add a dummy hook or change runtime behaviour merely to make a UI count agree.

## Inline app contract

MCP Apps serve HTML resources over MCP for a host to render. Browser WebMCP exposes tools from a page to a browser agent. They are different capabilities; one doesn't establish support for the other.

For an MCP App, check the installed server and target host's extension support. Follow [Mastra MCP Apps](https://mastra.ai/docs/connections/mcp) and the [MCP Apps SDK](https://github.com/modelcontextprotocol/ext-apps), then verify the actual wire:

1. `tools/list` preserves the tool's UI resource URI, visibility and any host-specific entrypoint metadata.
2. The resource registry/read serves that exact `ui://` URI with the supported HTML profile, metadata and CSP. Bundle guest dependencies where the intended host requires it.
3. The tool result separates concise model-facing `content` from UI data in `structuredContent` or another explicitly supported channel. Inspect initial tool delivery and later guest tool calls: host-specific result envelopes can differ. Unwrap only measured/documented shapes; don't accumulate speculative fallbacks.
4. The guest registers handlers before connecting, receives tool arguments/results, renders them and uses the SDK's supported host methods. An iframe, successful resource read or static standalone page doesn't establish the handshake.
5. A real host interaction changes a selection or query, sends the revised arguments, receives the correct result and updates the agent context where the feature requires it. Distinguish a read-only tool call from a guest method that sends chat and starts another paid model turn.

An ordinary Studio JSON tool form may have no custom field or async picker hook. Verify the installed host's support before trying to inject controls; an MCP App can own the picker when that path is supported. Don't copy a historical route restriction into a permanent rule about where Studio renders apps.

## Acceptance in the intended host

Use real records with identities that expose disputed assumptions, such as a brand id different from its URL slug. Check images, record links, selected identities, empty/error states, pagination exhaustion, a revised choice, dimensions and horizontal overflow. Run the project's browser QA and accessibility tooling when appropriate. Attribute a missing parent-iframe title or other host-owned violation to the host; changing guest HTML cannot repair the parent wrapper.

A saved Studio result establishes saved rendering. A fresh agent call establishes current tool invocation. A local web preview establishes that web host. Installation and metadata establish neither native-host interaction nor comparison in the current chat. Report each separately and leave unavailable host acceptance open.
