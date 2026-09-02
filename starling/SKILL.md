---
name: starling
description: Query Starling. Not for Xero (`xero`).
---

# Starling Bank

Use the read-only 1Password service account token in:

`/Users/danielhowells/.codex/plugins/secrets/1password-service-account.env`

Export its assignment without prompting for 1Password authentication:

```sh
set -a
. /Users/danielhowells/.codex/plugins/secrets/1password-service-account.env
set +a
```

Load every Starling token at runtime with `op run` using:

- `STARLING_BUSINESS_TOKEN=op://keys/Starling Bank - Business/credential`
- `STARLING_JOINT_TOKEN=op://keys/Starling Bank - Joint/credential`
- `STARLING_PERSONAL_TOKEN=op://keys/Starling Bank - Personal/credential`
- `STARLING_RENTAL_TOKEN=op://keys/Starling Bank - Rental/credential`

Never print any credential or token value.

Use the installed `starlingcli` from `https://github.com/howells/starlingcli`. It returns structured JSON. The literal `--account` names are `business`, `joint`, `personal` and `rental`; `all` is supported for balances. Use `starlingcli schema` for the current commands, parameters and output fields.

Run commands under `op run` so credentials exist only for that process:

```sh
STARLING_BUSINESS_TOKEN='op://keys/Starling Bank - Business/credential' \
STARLING_JOINT_TOKEN='op://keys/Starling Bank - Joint/credential' \
STARLING_PERSONAL_TOKEN='op://keys/Starling Bank - Personal/credential' \
STARLING_RENTAL_TOKEN='op://keys/Starling Bank - Rental/credential' \
op run -- starlingcli balance --account all
```

Choose a named account for transactions and other account-specific data. If `op` prompts or produces no output within 30 seconds, terminate it and report a non-interactive bootstrap failure; never authenticate through the desktop app. The CLI is read-only; do not substitute browser scraping.
