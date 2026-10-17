# Fable and Opus through Claude

Check `claude --help` for the required flags. Set `REVIEW_MODEL` to the user's exact version if named, otherwise the supported alias `fable` or `opus`. Run from the repository under review. The command below defines the argv to run through the bounded process handling in [process.md](process.md); pass the brief on stdin and close it.

```bash
claude -p \
  --model "$REVIEW_MODEL" \
  --effort high \
  --permission-mode plan \
  --tools "Read,Glob,Grep" \
  --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
  --disallowedTools "Edit,Write,NotebookEdit" \
  --no-session-persistence \
  --output-format json
```

`--tools` removes the shell and other built-in tools; `--allowedTools` would only preapprove them. The empty strict MCP configuration excludes unrelated integrations. These controls restrict tools, not every operating-system write route; retain the read-only brief boundary. Add `--add-dir` for any input outside the repository.

Do not pass a positional brief after variadic `--disallowedTools`: it can be swallowed as tool names. Do not use `--continue`, `--resume` or a fallback model.

Before the first invocation with this family in a session, run the same restricted command with `Reply with exactly: lane-ok` as stdin. The JSON can be a result object or an array of messages; for an array, use the final message with `type: "result"`. Require exit 0, `is_error: false`, exactly `lane-ok`, and a `modelUsage` key in the selected family (`claude-fable-*` or `claude-opus-*`). An explicitly requested version must match exactly. If metadata is absent, report identity as unverified; a different family or version is a failure.

For the actual review, require exit 0, `is_error: false`, and a non-empty `result`. Verify model identity again on the actual reply, not only the probe. Reject empty or failed replies; do not salvage them into a verdict.
