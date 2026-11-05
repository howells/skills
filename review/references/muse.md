# Muse Wonder through Muse

Check `muse exec --help` for current flags. Resolve the standard Wonder ID from model discovery (for example `muse-wonder-1.0`); honour an exact version or variant the user asked for, and don't substitute Spark. Set `REVIEW_MODEL`, `REVIEW_REPO` (absolute) and `REVIEW_BRIEF` (a temporary file holding the brief), then run with stdin closed, as described under Send in `SKILL.md`:

```bash
muse exec \
  --model "$REVIEW_MODEL" \
  --reasoning-effort high \
  --workspace "$REVIEW_REPO" \
  --disable-write \
  --disable-shell \
  --disable-web-tools \
  --disable-reminders \
  --no-foreign-personal-context \
  --no-session-log \
  --json \
  --prompt-file "$REVIEW_BRIEF"
```

- `--disable-write` covers only non-shell writes, so it needs `--disable-shell` too. Keep approval and sandboxing on: no `--yolo`, `--disable-sandbox` or `--disable-approval`, and no plugin that reopens writes.
- Output is JSONL. In schema version 1, success is a record with `payload_type: "run.terminal.completed"`, `payload.terminal: "completed"` and the answer in `payload.text`. `run.output.delta` is progress, not completion. Reject failed, cancelled or interrupted terminal records. If the schema differs, inspect it with `muse schema generate-json-schema --out <temporary-directory>` rather than guessing.
- Check the served model in the session or provider metadata when present; otherwise say identity is unverified.
