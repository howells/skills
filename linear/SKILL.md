---
name: linear
description: "Use either Linear account when MCP has the wrong one. Not for transcripts (`muster`)."
---

# Linear

Use the read-only 1Password service account token in:

`/Users/danielhowells/.codex/plugins/secrets/1password-service-account.env`

Source that file to set `OP_SERVICE_ACCOUNT_TOKEN`. This is non-interactive and must not prompt for 1Password authentication.

There are two accounts:

- `howells` uses `op://keys/linear/credential`.
- `material-instruments` uses `op://keys/linear material-instruments/credential`.

Use [scripts/graphql](scripts/graphql) to call `https://api.linear.app/graphql` without exposing either key. Pass the account name as its first argument and a complete GraphQL JSON request on standard input.

## Choose the account

- Honour an account the user names explicitly.
- For an issue identifier, team or project, make a small read-only lookup against both accounts. Use the sole account that contains the target.
- If both accounts contain a plausible target, identify the ambiguity. Read-only work may inspect both; ask before a write whose destination remains ambiguous.
- For an untargeted request such as "check Linear", use the repository's documented team or issue prefix when present. Otherwise list the relevant teams from both accounts before choosing.

The attached Linear MCP is optional. Use it only when it exposes the required account. An absent, expired or wrong-account MCP is not a blocker: use GraphQL immediately.

Never copy either key into a project `.env`, export one globally, print it, or replace one account's key with the other. Reads are allowed when they serve the user's request; create, update, close or comment only when the user requested that mutation.
