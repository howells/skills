---
name: gog
description: "Use gogcli for configured Google accounts instead of Google connectors. Not for web research (`web-research`)."
---

# GOG

Use the installed `gog` CLI for Gmail, Calendar, Drive, Docs, Sheets and other Google services. Check `command -v gog` and `gog --version` once per session; report a missing installation. After an upgrade, recheck focused help before reusing remembered flags. Treat the installed CLI's help/schema as authoritative rather than assuming these examples describe every version. Do not use generic Google connectors when this skill applies.

Discover authenticated accounts with `gog auth list`; confirm its flags with current help. GOG owns its OAuth credentials in its configured storage. Do not copy them into a project or replace its authentication with a connector. If no account is authenticated, report the missing setup; do not initiate login unless requested.

Honour an account the user names. Use repository context only when it explicitly identifies the owning account or domain. For an unspecified read, query the plausible configured accounts and label their results. Ask before a mutation whose destination remains ambiguous; never invent account aliases or assume an account inventory.

Before using an unfamiliar command, run `gog schema <command path> --json` or focused `gog <command> --help`; do not guess flags. Prefer structured, non-interactive output:

```bash
gog --account <email> --json --no-input --wrap-untrusted --readonly <command>
```

Preserve the JSON envelope, including pagination tokens. For complete searches or inventories, fetch every page and report any account or page that could not be read. Pagination is command-specific: Gmail message search supports `--all`; calendar events use `--all-pages` (`--all` means all calendars); Drive search uses `--page`. Confirm these with current help. Use `--results-only` only for a singular result or after completeness has been established. A first page is not a complete account or folder review.

## Gmail search efficiency and rate limits

Use `gog gmail messages search` for email; the root `gog search` command searches Drive. For prose-only thread reading, check support for `gmail thread get <id> --full --sanitize-content`: it avoids bulky raw MIME payloads, but removes HTTP(S) URLs. When links matter, retrieve unsanitised content and extract the needed text locally. Output filtering such as `--select` is not a guarantee of fewer API requests.

Reuse message IDs, thread IDs and content already retrieved in the task. Start with a narrow query using known correspondents, subjects and dates, without `--include-body` or `--full`; then fetch only the relevant messages or threads whose bodies are still needed. Search output may itself require metadata requests, so do not assume omitting bodies makes a search quota-free. Avoid overlapping searches, repeatedly fetching quoted thread history, or parallel Gmail searches against the same account. Keep pagination complete for the chosen scope; narrow an exploratory query rather than silently treating a partial result as complete.

For `403 rateLimitExceeded`, `userRateLimitExceeded`, or HTTP 429, inspect the reported quota and any retry delay. These are not necessarily authentication failures. Honour `Retry-After` when supplied; otherwise pause before a bounded retry, using increasing delays if needed, and reuse completed results. Allow at most two additional attempts in the current turn before reporting the incomplete search. Do not launch duplicate searches while a command is still running or already retrying. Other tasks using the same account and Google API project may share the allowance. Do not rotate accounts or credentials to evade a quota, and do not automatically retry an email send whose outcome is uncertain; check Sent first.

## Authentication and writes

On an account or authentication error, report it. Do not start an OAuth flow, add/remove credentials, or change account configuration as a repair step. This covers aliases such as `gog login`/`logout` and underlying `gog auth add`/`remove`/`manage` commands. Read-only auth status/list checks are allowed; never set a default account.

Prefer first-class commands over generic `gog api call`; use its `--allow-write` only for a write the user requested. Use `--readonly` for reads and omit it only when the user requested a mutation. Preview writes with `--dry-run` when supported. For a mutation other than sending email, add `--gmail-no-send`. Sending mail, changing calendar events, sharing files and other writes require explicit user intent. Do not use `--force` unless the user explicitly asked to skip the CLI confirmation for that exact action.
