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
gog --account <email> --json --results-only --no-input --wrap-untrusted --readonly <command>
```

On an account or authentication error, report it. Never run `gog login`, `gog logout` or `gog auth manage`, and never set a default account.

Use `--readonly` for reads and omit it only when the user requested a mutation. Preview writes with `--dry-run` when supported. For a mutation other than sending email, add `--gmail-no-send`. Sending mail, changing calendar events, sharing files and other writes require explicit user intent. Do not use `--force` unless the user explicitly asked to skip the CLI confirmation for that exact action.
