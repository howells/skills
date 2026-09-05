---
name: xero
description: Query Xero accounting data through Daniel's offledger CLI. Not for Starling (`starling`).
---

# Xero

Use the read-only 1Password service account token in:

`/Users/danielhowells/.codex/plugins/secrets/1password-service-account.env`

Run the bootstrap and requested command in the same non-interactive subprocess. Require the service-account file and assignment before invoking `op`:

```sh
set -eu
credential_file=/Users/danielhowells/.codex/plugins/secrets/1password-service-account.env
test -r "$credential_file" || { echo 'Service-account file missing' >&2; exit 1; }
set -a
. "$credential_file"
set +a
test -n "${OP_SERVICE_ACCOUNT_TOKEN:-}" || { echo 'Service-account token missing' >&2; exit 1; }
```

Load the Xero credentials at runtime with `op run` using:

- `XERO_CLIENT_ID=op://keys/Xero Custom Connection/username`
- `XERO_CLIENT_SECRET=op://keys/Xero Custom Connection/credential`

Never print a credential or token or create ad hoc credential files. The CLI-managed access-token cache at `~/.offledger/xero-tokens.json` is the sole file exception; verify the directory and file remain private (0700/0600). Never copy that cache or write credentials to `.env`. The offledger CLI's stale “must be set in .env” error means environment variables; do not follow it literally.

Use the private repository `https://github.com/howells/offledger`, whose Xero CLI is `scripts/xero.mjs`. If `/Users/danielhowells/Sites/offledger` is absent, clone there with `gh repo clone howells/offledger /Users/danielhowells/Sites/offledger`, then run `pnpm install --frozen-lockfile` in that checkout. Use a clean checkout with no `.env` because the CLI loads that file over injected variables. If an existing checkout has one, preserve it and use a separate owned clean checkout following the host’s worktree policy. If that is unavailable, report the blocker; never delete or bypass the file silently.

Run commands under `op run`; there is no `--` between `xero` and its subcommand:

```sh
cd /Users/danielhowells/Sites/offledger
XERO_CLIENT_ID='op://keys/Xero Custom Connection/username' \
XERO_CLIENT_SECRET='op://keys/Xero Custom Connection/credential' \
op run -- pnpm xero bank-balances --dry-run </dev/null
```

For reads, use `revenue`, `director-loan`, `bank-transactions`, or `bank-balances --dry-run`. Plain `bank-balances` initializes SQLite and writes balance rows; it is a mutation, as are commands beginning `sync`. Run these only when the user requested that mutation. Reads refresh authentication as needed; do not run a separate `auth` command routinely. Use it for an explicitly requested authentication check or a diagnosed token problem. It may update the approved token cache. Inspect current command help/source if its behaviour is unclear. Enforce a 30-second process-tree timeout through the host runner or a Python subprocess runner. Stdin redirection alone does not prevent desktop authentication. On timeout, distinguish credential lookup from the API request only when evidence identifies the stage, and never fall back to desktop authentication. Use the API/CLI directly; do not substitute browser scraping.
