---
name: astra-review
description: "Get an independent review from GPT-6 Astra via Codex, then verify its claims before acting. Use when the code can settle the question - does a diff hold, what changed when - or the user asks for Astra or a Codex review. Not for judgement calls (`fable-review`), criteria checks (`glm-review`) or codebase grades (`simplify`)."
---

# Astra review

Astra is the frontier lane that can run commands. Codex runs it inside the operating system's sandbox with writes blocked, so it can read the repository and also execute `git diff`, `git log`, `rg` or anything else that only reads. The Fable lane can only read files. Use Astra where the answer lives in the code: whether a diff does what it claims, where an implementation breaks, what the history says about a regression.

What comes back is a set of leads. Verify each one before acting on it.

## Choosing the lane

Three review skills send a brief to an outside model, chosen by the kind of question rather than its importance:

| The question | Lane |
| --- | --- |
| A bounded check against criteria the brief states: a contract, a spec, copy against a style guide | `glm-review` - cheap |
| An answer the repository can settle: what changed when, whether a diff does what it claims, where it breaks | `astra-review` - frontier, runs read-only commands |
| A judgement call with no checkable answer: architecture, taste, a plan, with the evidence in the brief | `fable-review` - frontier, reads files only |

A routine correctness pass over a diff is the host's own code review, not a lane.

## The route

Codex's non-interactive mode is the route, and it works the same from Claude Code, Codex and OpenCode, because all three can run a shell command. Set `REPO` to the absolute path of the repository under review and `OUT` to a file for the final message:

```bash
codex exec \
  --ignore-user-config \
  --ephemeral \
  --cd "$REPO" \
  --sandbox read-only \
  --model gpt-6-astra \
  --config 'model_reasoning_effort="high"' \
  --json \
  --output-last-message "$OUT" \
  - < brief.md > "$OUT.jsonl"
```

- `-` reads the brief from stdin. **Close stdin once the brief is written.** `codex exec` reads stdin to the end even when the prompt is a positional argument, because it appends piped input to the prompt. Left open, the pipe hangs the run silently before the model is ever called.
- `--ignore-user-config` skips the user's `config.toml`, so no MCP servers start and no personal default sandbox, model or approval policy applies. Authentication still comes from the Codex home. The global and project `AGENTS.md` and the installed skills list still load, as they do for the other lanes. Don't edit the user's configuration to make the lane work.
- `--sandbox read-only` is the boundary, enforced by the operating system rather than by the brief. Shell writes fail with `Operation not permitted`, and the file-editing tool is rejected with `writing is blocked by read-only sandbox`. Network access is off too.
- `--ephemeral` keeps the review out of the user's Codex session history.
- `--json` streams events to stdout; keep that stream in a file so a killed run still leaves what arrived. `--output-last-message` writes the final answer on its own.
- `high` effort is the default for this skill. Use a different effort only when the user explicitly asks for one.

Confirm the lane before the first invocation in a session:

```bash
printf 'Reply with exactly: lane-ok' | codex exec --ignore-user-config --ephemeral \
  --sandbox read-only --model gpt-6-astra --config 'model_reasoning_effort="high"' \
  --output-last-message "$OUT" -
```

Require exit status 0 and `$OUT` containing exactly `lane-ok`. The event stream does not echo the model name. The identity evidence is that the server rejects a slug it does not serve: exit 1, and a `turn.failed` event carrying a 400. A completed turn under `--model gpt-6-astra` is therefore Astra.

Then break the sandbox on purpose, once per session:

```bash
printf 'Sandbox check. Run the shell command: touch lane-write-probe. Then use your file-editing tool to create lane-write-probe-2. Report each result verbatim.' \
  | codex exec --ignore-user-config --ephemeral --cd "$REPO" --sandbox read-only \
    --model gpt-6-astra --config 'model_reasoning_effort="low"' --output-last-message "$OUT" - \
  && grep -q 'Operation not permitted' "$OUT" \
  && grep -q 'read-only sandbox' "$OUT" \
  && test ! -e "$REPO/lane-write-probe" && test ! -e "$REPO/lane-write-probe-2" \
  && echo sandbox-ok
```

The probe tests the sandbox rather than the model, so it runs at low effort. `sandbox-ok` needs all of it: the run succeeded, the reply shows the shell write denied and the edit rejected, and neither file exists. Absent files alone prove nothing, since a run that never started leaves none either.

Without `lane-ok` and `sandbox-ok`, stop and name the cause: `codex` missing from the path, not logged in (`codex login status`), the slug no longer served (`codex debug models` lists the current catalogue), or the sandbox unavailable on this machine. If either probe file exists, delete it and report the lane as unsafe. Substituting another model, another size, or another lab's model is a failed run, because the point of the lane is which model answered.

**Do not substitute Codex's own subagents.** A Codex host can spawn agents of its own, but they run under the host's configuration and are briefed from inside the session that wants the answer. The subprocess starts clean under a fixed model and sandbox, which is the whole value. If you are already running on Astra, the subprocess gives an independent context but not an independent model: say so in the report, or use `fable-review` if the question fits it.

## Build a bounded brief

Investigate first, so Astra spends its turn on the question rather than on rediscovering the repository. A brief carries:

- the question, stated as something the code can settle;
- the artifact: paths, the base commit or range, current status. For a diff, name the base and let Astra run `git diff` itself rather than pasting it;
- constraints, settled decisions, and explicit non-goals;
- validation already run, with results, and what remains uncertain. Test runs usually write caches or build output, and those writes fail in this sandbox, so run the tests yourself and put the outcome in the brief;
- anything it needs from outside the repository, since it has no network;
- a line saying that `xcrun`, `confstr` and `Operation not permitted` warnings on stderr are sandbox noise. On macOS, `git` prints them under the read-only sandbox and still returns its output;
- the boundary, verbatim: `Read-only review. Do not edit files or run state-changing commands.`

Ask for a verdict, findings with `file:line` evidence and the command that showed each one, where it disagrees with the proposed direction, and concrete changes.

A brief that names no question gets a tour of the codebase. "Review this branch" fails that bar; "this diff claims the retry is idempotent - find the input where it is not" does not.

## Run it and wait

Enforce a limit of 1800 seconds of wall-clock time on the subprocess and its children. Launch it through Python `subprocess.Popen(start_new_session=True)`, pass the brief with `communicate(input=..., timeout=1800)` so stdin closes, and kill the process group on `TimeoutExpired`. Don't assume GNU `timeout` exists on macOS. A short tool yield is fine if it returns a live session; it must not kill the review.

A multi-file brief measured at 180 seconds at high effort, in the one run timed so far. Duration tracks how much the model reads and runs, so a brief that points at a large generated file or a long history will use more of the limit; scope it to source where you can.

A run succeeded when it exits 0, `$OUT` is non-empty, and the event stream holds a `turn.completed` event and no event whose `type` is `turn.failed`. Parse the JSON lines rather than searching the text: command output quoted inside the stream can contain those strings. A started process is not a review. At the limit, kill it, say so, and stop. Output that arrives empty or cut off mid-finding is a failed run, reported as one rather than salvaged into a partial verdict.

Retry once on a transport or internal-server failure. Report an authentication, quota, billing or rate-limit rejection and stop without retrying, because those repeat.

## Verify, then report

Check every material claim against the source, the diff, the tests, or the running product. Rerun any command a load-bearing finding rests on rather than trusting the quoted output. A claim you could not confirm stays labelled unconfirmed.

Return:

- the question Astra was given;
- its verdict, and whether you agree;
- findings you verified, most serious first;
- claims that failed verification, and what you found instead;
- recommended changes, kept separate from changes already made;
- any lane failure, including a run where Astra reviewed its own model's work.

Pasting the reply verbatim is not a report. Implement nothing unless implementation was already part of the request.

## Where this fits

- A hard judgement call with no checkable answer: `fable-review`.
- A cheap check against stated criteria: `glm-review`.
- A whole-codebase grade with a comparable score: `simplify`.
- A routine correctness pass over a diff: the host's own code review.
