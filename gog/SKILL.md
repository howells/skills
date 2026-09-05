---
name: gog
description: "Use gogcli for Daniel's Google accounts instead of Google connectors. Not for public web research (`web-research`)."
---

# GOG

Use the installed `/opt/homebrew/bin/gog` CLI for Daniel's Gmail, Calendar, Drive, Docs, Sheets and other Google services. Do not use the generic Gmail or Google connectors when this skill applies.

GOG already owns its OAuth credentials in `/Users/danielhowells/Library/Application Support/gogcli/`. Do not ask for an API key, copy its credentials into a project, or replace its authentication with a connector.

The authenticated accounts are:

- `daniel.howells@gmail.com` — personal Gmail
- `daniel@danielhowells.com` — personal domain
- `daniel@materialinstruments.com` — Material Instruments
- `mail@siteinspire.com` — SiteInspire

Honour an account the user names. Infer Material Instruments and SiteInspire from their domains or repository context. For an unspecified read, query the plausible accounts and combine the result rather than stopping for account selection. Do not default between the two personal accounts for a mutation; ask when the destination remains genuinely ambiguous.

Before using an unfamiliar command, run `gog schema <command path> --json` or focused `gog <command> --help`; do not guess flags. Prefer structured, non-interactive output:

```bash
gog --account <email> --json --no-input --wrap-untrusted --readonly <command>
```

Preserve the JSON envelope, including pagination tokens. For complete searches or inventories, fetch every page and report any account or page that could not be read. Pagination is command-specific: Gmail message search supports `--all`; calendar events use `--all-pages` (`--all` means all calendars); Drive search uses `--page`. Confirm these with current help. Use `--results-only` only for a singular result or after completeness has been established. A first page is not a complete account or folder review.

On an account or authentication error, report it. Do not start an OAuth flow, add/remove credentials, or change account configuration as a repair step. This covers aliases such as `gog login`/`logout` and underlying `gog auth add`/`remove`/`manage` commands. Read-only auth status/list checks are allowed; never set a default account.

Prefer first-class commands over generic `gog api call`; use its `--allow-write` only for a write the user requested. Use `--readonly` for reads and omit it only when the user requested a mutation. Preview writes with `--dry-run` when supported. For a mutation other than sending email, add `--gmail-no-send`. Sending mail, changing calendar events, sharing files and other writes require explicit user intent. Do not use `--force` unless the user explicitly asked to skip the CLI confirmation for that exact action.
