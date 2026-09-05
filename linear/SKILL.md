---
name: linear
description: "Use configured Linear accounts via GraphQL; choose the account that owns the target. Not for transcripts (`muster`)."
---

# Linear

Use an existing authenticated Linear connection or the bundled GraphQL helper. Credentials and account mappings come from the user's environment; this skill ships neither.

For [scripts/graphql](scripts/graphql), inject `LINEAR_API_KEY` into the request subprocess through the configured secret manager or environment. The helper reads it without printing it in diagnostics or putting it in command arguments. It calls `https://api.linear.app/graphql` and takes a complete GraphQL JSON request on standard input:

```sh
# LINEAR_API_KEY must already be injected for the intended account.
printf '%s' '{"query":"query { viewer { name } }"}' | scripts/graphql
```

For multiple accounts, use the environment's documented credential mapping and launch a separate subprocess for each account. Do not infer credential names from an email, project or issue prefix. If no mapping or authenticated connection is available, report the missing configuration.

## Choose the account

- Honour an account the user names explicitly.
- For an issue identifier, team or project, make a small read-only lookup against the plausible configured accounts. Use the sole account that contains the target.
- If multiple accounts contain a plausible target, identify the ambiguity. Read-only work may inspect each; ask before a write whose destination remains ambiguous.
- For an untargeted request such as "check Linear", use the repository's documented team or issue prefix when present. Otherwise list the relevant teams from the configured accounts before choosing.

The attached Linear MCP is optional. Use it only when it exposes the required account. If the MCP cannot serve that account and its API key is configured, use GraphQL. Otherwise report the missing access.

Never copy a key into a project `.env`, export one globally, print it, or overwrite another account's credentials. Reads are allowed when they serve the user's request; create, update, close or comment only when the user requested that mutation.

The bundled helpers require Python 3. [scripts/read-credential.py](scripts/read-credential.py) requires a nonempty, single-line environment credential before any request. Missing credentials stop the request without interactive authentication; inject secrets before invoking the helper.

[scripts/check-response.py](scripts/check-response.py) preserves the response and exits nonzero for GraphQL errors, invalid data or an explicit mutation failure. Inspect required fields and the returned entity before claiming success. Partial data is not a complete account lookup. Never automatically retry a mutation after an uncertain outcome; reconcile current state first.
