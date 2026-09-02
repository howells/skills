---
name: xero
description: Query Xero. Not for Starling (`starling`).
---

# Xero

Use the read-only 1Password service account token in:

`/Users/danielhowells/.codex/plugins/secrets/1password-service-account.env`

Source that file to set `OP_SERVICE_ACCOUNT_TOKEN`. This is non-interactive and must not prompt for 1Password authentication.

Load the Xero credentials at runtime with `op run` using:

- `XERO_CLIENT_ID=op://keys/Xero Custom Connection/username`
- `XERO_CLIENT_SECRET=op://keys/Xero Custom Connection/credential`

Never print any credential or token value.

Use the private repository `https://github.com/howells/offledger`, whose Xero CLI is `scripts/xero.mjs` and whose package command is `pnpm xero -- <command>`.

If no local checkout exists, clone the repository first. Run its Xero command under `op run` so the two variables are injected only for that process. Use the API/CLI directly; do not substitute browser scraping.
