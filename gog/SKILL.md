---
name: gog
description: "Use gogcli for configured Google accounts instead of Google connectors. Not for web research (`web-research`)."
---

# GOG

Use the installed `gog` CLI for Gmail, Calendar, Drive, Docs, Sheets and other Google services. Check `command -v gog` and report a missing installation. Do not use generic Google connectors when this skill applies.

Discover authenticated accounts with `gog auth list`; confirm its flags with current help. GOG owns its OAuth credentials in its configured storage. Do not copy them into a project or replace its authentication with a connector. If no account is authenticated, report the missing setup; do not initiate login unless requested.

Honour an account the user names. Use repository context only when it explicitly identifies the owning account or domain. For an unspecified read, query the plausible configured accounts and label their results. Ask before a mutation whose destination remains ambiguous; never invent account aliases or assume an account inventory.

Before using an unfamiliar command, run `gog schema <command path> --json` or focused `gog <command> --help`; do not guess flags. Prefer structured, non-interactive output:

```bash
gog --account <email> --json --no-input --wrap-untrusted --readonly <command>
```

Preserve the JSON envelope, including pagination tokens. For complete searches or inventories, fetch every page and report any account or page that could not be read. Pagination is command-specific: Gmail message search supports `--all`; calendar events use `--all-pages` (`--all` means all calendars); Drive search uses `--page`. Confirm these with current help. Use `--results-only` only for a singular result or after completeness has been established. A first page is not a complete account or folder review.

On an account or authentication error, report it. Do not start an OAuth flow, add/remove credentials, or change account configuration as a repair step. This covers aliases such as `gog login`/`logout` and underlying `gog auth add`/`remove`/`manage` commands. Read-only auth status/list checks are allowed; never set a default account.

Prefer first-class commands over generic `gog api call`; use its `--allow-write` only for a write the user requested. Use `--readonly` for reads and omit it only when the user requested a mutation. Preview writes with `--dry-run` when supported. For a mutation other than sending email, add `--gmail-no-send`. Sending mail, changing calendar events, sharing files and other writes require explicit user intent. Do not use `--force` unless the user explicitly asked to skip the CLI confirmation for that exact action.
