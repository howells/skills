# Sol and Astra through Codex

Check `codex exec --help`, then `codex debug models` for current IDs (for example `gpt-6.1-sol`, `gpt-6-astra`). Set `REVIEW_REPO` to the absolute repository path, `REVIEW_MODEL` to the resolved ID, and `REVIEW_OUT` to a temporary path outside the repository. Run with the brief on stdin, as described under Send in `SKILL.md`:

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

- `--ignore-user-config` skips personal model, sandbox and MCP defaults but keeps authentication. The read-only sandbox blocks writes and network, so put any external evidence in the brief.
- Close stdin after the brief. Codex reads piped input to EOF, so an open pipe hangs before the model is called.
- Require exit 0, a non-empty final message, a parsed JSONL event with `type: "turn.completed"`, and no `turn.failed`. Parse the events; quoted command output can contain those strings.
- The event stream may not echo the served model. Identity rests on the explicit model ID plus completion; say so if a proxy could remap it.
- On macOS, `xcrun`, `confstr` and `Operation not permitted` warnings on stderr often accompany successful read-only `git` commands. Check the exit status before treating them as failures.
