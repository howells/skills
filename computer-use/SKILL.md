---
name: computer-use
description: "Control Mac apps, including signed-in Chrome, through native Codex Computer Use from Codex or Claude Code. Not for browser-only QA (`fieldtest`)."
---

# Computer Use

Use the current session's native Computer Use tools when available. An explicit request for Computer Use means native app control, Chrome included; don't substitute a browser extension, CDP, AppleScript or another desktop driver. File and shell work stay with their own tools.

Follow the live tool documentation, inspect the target app before acting, and verify the result on screen. Respect runtime app approvals and macOS permissions. Use one desktop controller at a time; finish or stop an existing controller before starting another.

## Hosts without native tools

When the current session has no native Computer Use tools, or its native bridge fails to initialise before app access, report that limitation and use the bundled runner. An app permission refusal still follows the approval flow below. The runner launches a headless `codex exec` with Computer Use enabled, including from Claude Code.

The runner needs macOS, the Codex CLI with a configured model, and the `computer-use@openai-bundled` and `unified-computer-use@openai-bundled` plugins enabled. `python3 scripts/run.py --check` confirms config and plugins; it does not test auth or app access.

1. Write a brief to a file: target app and account, the outcome wanted, what may change, and how to tell it's done.
2. From this skill's directory:

   ```sh
   python3 scripts/run.py --brief /abs/brief.txt --output-dir /abs/new-dir
   ```

   Use a fresh output directory each attempt. It uses `~/.codex` rather than a host proxy home (`--codex-home` for another install) and keeps its configured provider and model (`--model` only if the user asks). The shell sandbox defaults to `workspace-write`; pass `--sandbox read-only` under a read-only host policy.
3. Wait on the process; read `result.txt`, and `events.jsonl` or `stderr.log` when it fails. Cancel with SIGTERM to this runner, never `pkill codex`.
4. Check the outcome on screen. Exit code zero isn't success. After a partial run, resume from the observed state rather than repeating actions that already landed.

**One controller at a time.** The runner holds `~/.cache/computer-use/desktop.lock` across Codex and Claude Code. If it's held, another task or an idle approval session owns the desktop: wait or coordinate. Never delete the lock or start a second controller because the first is slow.

## First use of an app

Use the current session's normal app-approval flow. **"Computer Use was not approved to use …"** means the app has no saved allowance, not an auth problem.

For the headless runner, stop the controller and launch the interactive helper in a visible terminal on the Mac running Codex. Open that terminal yourself when terminal-management tools are available; otherwise give the user the command. From this skill's directory (same `--codex-home` if you overrode it):

```sh
python3 scripts/run.py --approve-app "Google Chrome"
```

The user chooses the approval scope; **Always allow** persists across headless invocations. After the access check completes, close the idle helper session to release the lock and resume the task. If the same refusal persists, report the exact error.

## Telling failures apart

- **App allowance:** ChatGPT desktop → Settings → Computer use → **Always-allowed apps**. The **Any App** toggle and Chrome's extension settings don't count.
- **macOS permissions:** Screen Recording and Accessibility for **Codex Computer Use**. Separate from app allowances.
- **`cgWindowNotFound`:** the Mac is locked, it's the wrong machine, or the app has no window. Not auth or approval. Unlocking happens on the controlling Mac, which may not be the one showing the host app.
- **Changed-app or interrupted-control errors:** someone else is moving the desktop.
- **"unsupported Codex auth method: apikey":** comes from the browser extension backend; native Computer Use works with API-key providers.

Don't edit permission databases, copy credentials or widen the sandbox to get past a refusal. Leave any legacy `mcp_servers.computer-use` entry disabled. Setup details: [Computer Use](https://developers.openai.com/codex/computer-use).
