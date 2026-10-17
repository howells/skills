# Muse Wonder through Muse

Check `muse exec --help` for the required flags. Resolve the current standard Wonder ID from available model discovery; `muse-wonder-1.0` is a current example. `muse model-profile show <id> --effort high` can confirm the configured model profile, but does not prove authentication. Honour an exact version or variant the user requested; do not substitute Spark.

Set `REVIEW_MODEL` to the resolved ID, `REVIEW_REPO` to the absolute repository path, and `REVIEW_BRIEF` to a temporary file containing the complete brief. Run this argv through [process.md](process.md), with stdin closed:

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

`--disable-write` disables non-shell workspace writes, so pair it with `--disable-shell` to close the shell route. Keep approval and sandboxing enabled; do not use `--yolo`, `--disable-sandbox` or `--disable-approval`. Do not load an integration or plugin that reopens write access. These flags do not prove that every possible external write route is isolated; report the actual tool restriction, and stop if the restriction cannot be established.

Use a bounded `Reply with exactly: lane-ok` probe through the same command before the first Wonder invocation in a session. Require exit 0, successful completion and exactly `lane-ok` in the final assistant text. Verify the selected model from returned session/provider metadata when available; label absent served-model identity unverified. A different model is a failure.

Muse emits structured JSONL records. In schema version 1, require a record whose `payload_type` is `run.terminal.completed`, whose `payload.terminal` is `completed`, and whose `payload.text` contains the non-empty final answer. `run.output.delta` is progress, not completion; a completed tool or model task is not a completed review. Reject failed, cancelled or interrupted terminal records. If the installed schema differs, use `muse schema generate-json-schema --out <temporary-directory>` to inspect it rather than guessing at success.

For the actual review, require exit 0, that completed terminal record, a non-empty final answer and no failure event for its run. A model profile, started session or partial response is not a review.
