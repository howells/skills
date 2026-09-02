---
name: xero
description: Query Xero. Not for Starling (`starling`).
---

# Xero

Use the read-only 1Password service account token in:

`/Users/danielhowells/.codex/plugins/secrets/1password-service-account.env`

Export its assignment without prompting for 1Password authentication:

```sh
set -a
. /Users/danielhowells/.codex/plugins/secrets/1password-service-account.env
set +a
```

Load the Xero credentials at runtime with `op run` using:

- `XERO_CLIENT_ID=op://keys/Xero Custom Connection/username`
- `XERO_CLIENT_SECRET=op://keys/Xero Custom Connection/credential`

Never print a credential or token, and never write one to `.env` or any other file. The offledger CLI's stale “must be set in .env” error means environment variables; do not follow it literally.

Use the private repository `https://github.com/howells/offledger`, whose Xero CLI is `scripts/xero.mjs`. If `/Users/danielhowells/Sites/offledger` is absent, clone there with `gh repo clone howells/offledger /Users/danielhowells/Sites/offledger`, then run `pnpm install --frozen-lockfile` in that checkout. Use a clean checkout with no `.env` because the CLI loads that file over injected variables.

Run commands under `op run`; there is no `--` between `xero` and its subcommand:

```sh
cd /Users/danielhowells/Sites/offledger
XERO_CLIENT_ID='op://keys/Xero Custom Connection/username' \
XERO_CLIENT_SECRET='op://keys/Xero Custom Connection/credential' \
op run -- pnpm xero auth
```

The Xero query commands are `auth`, `revenue`, `director-loan`, `bank-balances` and `bank-transactions`. Commands beginning `sync` write to Google Sheets or local SQLite and run only when the user requested that mutation. Use the API/CLI directly; do not substitute browser scraping.
