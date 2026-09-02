---
name: gog
description: "Use gogcli for Daniel's Google accounts instead of Google connectors."
---

# GOG

Use the installed `/opt/homebrew/bin/gog` CLI for Daniel's Gmail, Calendar, Drive, Docs, Sheets and other Google services. Do not use the generic Gmail or Google connectors when this skill applies.

GOG already owns its OAuth credentials in `/Users/danielhowells/Library/Application Support/gogcli/`. Do not ask for an API key, copy its credentials into a project, or replace its authentication with a connector.

The authenticated accounts are:

- `daniel.howells@gmail.com`
- `daniel@danielhowells.com`
- `daniel@materialinstruments.com`
- `mail@siteinspire.com`

Honour an account the user names. Infer Material Instruments and SiteInspire from their domains or repository context. For an unspecified read, query the plausible accounts and combine the result rather than stopping for account selection. Before a mutation, ask only when the destination account remains genuinely ambiguous.

Before using an unfamiliar command, run `gog schema <command path> --json` or focused `gog <command> --help`; do not guess flags. Prefer structured, non-interactive output:

```bash
gog --account <email> --json --no-input --wrap-untrusted --readonly <command>
```

Use `--readonly` for reads and omit it only when the user requested a mutation. Sending mail, changing calendar events, sharing files and other writes require explicit user intent. Do not use `--force` unless the user explicitly asked to skip the CLI confirmation for that exact action.
