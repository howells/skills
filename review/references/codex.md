# Sol and Astra through Codex

Check `codex exec --help`, then read `codex debug models` for current supported IDs. Resolve the user's family and version there; current examples are `gpt-6.1-sol` and `gpt-6-astra`, not permanent version pins. Set `REVIEW_REPO` to the absolute repository path, `REVIEW_MODEL` to the resolved ID, and `REVIEW_OUT` to a temporary final-message path outside the repository.

Run this argv through the bounded process handling in [process.md](process.md), with the brief on stdin:

```bash
codex exec \
  --ignore-user-config \
  --ephemeral \
  --cd "$REVIEW_REPO" \
  --sandbox read-only \
  --model "$REVIEW_MODEL" \
  --config 'model_reasoning_effort="high"' \
  --json \
  --output-last-message "$REVIEW_OUT" \
  -
```

`--ignore-user-config` skips personal model, sandbox and MCP defaults while preserving authentication. Repository instructions and installed skill discovery may still load. `--ephemeral` avoids persistent session history. The operating-system sandbox blocks writes and network access; provide any external evidence in the brief. Do not edit persistent configuration or enable a bypass.

Close stdin after the brief: Codex reads piped input to EOF even with a positional prompt, so an open pipe can hang before the model is called. Capture the JSONL stdout separately from the final message.

Before the first invocation in a session, run this restricted command with `Reply with exactly: lane-ok`. Require exit 0, a completed turn and a final message of exactly `lane-ok`. Identity evidence is the explicitly selected supported model ID plus successful completion; the event stream may not echo a served model. If a proxy can remap IDs without reporting the served model, disclose that limit rather than claiming independently verified identity.

Test the sandbox once per session in a temporary scratch repository, never in the user's working tree. Ask the model to create two uniquely named probe files, one through a shell write and one through the editing tool, and quote each outcome. Require evidence that both writes were attempted and denied, successful turn completion, and neither file present. A refusal without an attempted write, or absent files alone, does not establish enforcement. If a file appears, remove only the probe and report the route as unavailable.

For an actual review, require exit 0, a non-empty final message, a parsed JSONL event with `type: "turn.completed"`, and no `turn.failed` event. Parse events; quoted command output can contain those strings. On macOS, `xcrun`, `confstr` and `Operation not permitted` stderr warnings can accompany successful read-only `git` commands; inspect their exit status and output before treating them as failure.
