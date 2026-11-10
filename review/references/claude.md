# Fable and Opus through Claude

Check `claude --help` for current flags. Set `REVIEW_MODEL` to the user's exact version if named, otherwise the alias `fable` or `opus`. Run from the repository under review with the brief on stdin, as described under Send in `SKILL.md`:

```bash
claude -p \
  --model "$REVIEW_MODEL" \
  --effort high \
  --permission-mode plan \
  --tools "Read,Glob,Grep" \
  --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
  --no-session-persistence \
  --output-format json
```

- `--tools` removes the shell and other built-ins; `--allowedTools` would only preapprove them. The empty strict MCP config keeps unrelated integrations out. Add `--add-dir` for inputs outside the repository.
- Don't pass the brief as a positional argument after `--tools`: the variadic flag swallows it as tool names.
- Don't use `--continue`, `--resume` or a fallback model.
- The JSON is a result object or an array of messages; for an array, take the final `type: "result"` message. Require exit 0, `is_error: false`, a non-empty `result`, and a `modelUsage` key in the selected family (`claude-fable-*` or `claude-opus-*`, or the exact version requested).
