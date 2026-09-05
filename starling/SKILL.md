---
name: starling
description: Query Daniel's Starling Bank balances and transactions. Not for Xero (`xero`).
---

# Starling Bank

Use the read-only 1Password service account token in:

`/Users/danielhowells/.codex/plugins/secrets/1password-service-account.env`

Run this bootstrap and the requested command in the same non-interactive subprocess. Stop before `op run` if the file or service-account assignment is missing:

```sh
set -eu
credential_file=/Users/danielhowells/.codex/plugins/secrets/1password-service-account.env
test -r "$credential_file" || { echo 'Service-account file missing' >&2; exit 1; }
set -a
. "$credential_file"
set +a
test -n "${OP_SERVICE_ACCOUNT_TOKEN:-}" || { echo 'Service-account token missing' >&2; exit 1; }
```

Load every Starling token at runtime with `op run` using:

- `STARLING_BUSINESS_TOKEN=op://keys/Starling Bank - Business/credential`
- `STARLING_JOINT_TOKEN=op://keys/Starling Bank - Joint/credential`
- `STARLING_PERSONAL_TOKEN=op://keys/Starling Bank - Personal/credential`
- `STARLING_RENTAL_TOKEN=op://keys/Starling Bank - Rental/credential`

Never print any credential or token value.

Check `command -v starlingcli` first; if missing, report the dependency rather than guessing an installation or rebuilding it unasked. Use the installed `starlingcli` from `https://github.com/howells/starlingcli`. It returns structured JSON. The literal `--account` names are `business`, `joint`, `personal` and `rental`; `all` is supported for balances. Use `starlingcli schema` for the current commands, parameters and output fields.

Run commands under `op run` so credentials exist only for that process:

```sh
STARLING_BUSINESS_TOKEN='op://keys/Starling Bank - Business/credential' \
STARLING_JOINT_TOKEN='op://keys/Starling Bank - Joint/credential' \
STARLING_PERSONAL_TOKEN='op://keys/Starling Bank - Personal/credential' \
STARLING_RENTAL_TOKEN='op://keys/Starling Bank - Rental/credential' \
op run -- starlingcli balance --account all </dev/null
```

Choose a named account for transactions and other account-specific data. Enforce a 30-second process-tree timeout using the host runner or a Python subprocess timeout; stdin redirection alone cannot prevent desktop authentication. Never authenticate through the desktop app. If the command times out, report whether the failure is known to be credential lookup or the bank request; silence alone cannot distinguish them. Use only commands the installed schema describes as reads. Do not substitute browser scraping.
