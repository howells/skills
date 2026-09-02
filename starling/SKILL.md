---
name: starling
description: Query Starling. Not for Xero (`xero`).
---

# Starling Bank

Use the read-only 1Password service account token in:

`/Users/danielhowells/.codex/plugins/secrets/1password-service-account.env`

Source that file to set `OP_SERVICE_ACCOUNT_TOKEN`. This is non-interactive and must not prompt for 1Password authentication.

Load every Starling token at runtime with `op run` using:

- `STARLING_BUSINESS_TOKEN=op://keys/Starling Bank - Business/credential`
- `STARLING_JOINT_TOKEN=op://keys/Starling Bank - Joint/credential`
- `STARLING_PERSONAL_TOKEN=op://keys/Starling Bank - Personal/credential`
- `STARLING_RENTAL_TOKEN=op://keys/Starling Bank - Rental/credential`

Never print any credential or token value.

Use the installed `starlingcli` from `https://github.com/howells/starlingcli`. It returns structured JSON and discovers account names from the four environment variables.

Run commands under `op run` so credentials exist only for that process. Use `starlingcli balance --account all` for all balances, and choose a named account for transactions or other account-specific data. The CLI is read-only; do not substitute browser scraping.
