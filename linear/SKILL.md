---
name: linear
description: "Use configured Linear accounts via GraphQL; choose the account that owns the target. Not for transcripts (`muster`)."
---

# Linear

Linear is reached through GraphQL with the bundled helper. There is no Linear MCP in either harness; never ask for a key and never paste one.

Keys are already in the session environment: `LINEAR_API_KEY` for the default workspace, and one `LINEAR_API_KEY_<WORKSPACE>` per additional workspace. The user's own instructions say which workspace and team prefixes each variable covers; read that mapping there, never infer it from an email, project or issue prefix.

If a variable is empty, say which one and stop. Do not go looking in `.env` files, and do not copy a key anywhere.

[scripts/graphql](scripts/graphql) reads `LINEAR_API_KEY` from the environment, never from arguments, and posts a complete GraphQL JSON request from standard input to `https://api.linear.app/graphql`. For another workspace, run it with the variable re-pointed for that one subprocess:

```sh
printf '%s' '{"query":"query { viewer { name } }"}' | scripts/graphql
LINEAR_API_KEY="$LINEAR_API_KEY_OTHER" scripts/graphql < request.json
```

## Choose the account

- Honour an account the user names explicitly.
- For an issue identifier, team or project, use the documented mapping. If the prefix is not listed, make a small read-only lookup against each configured workspace and use the one that contains it.
- If more than one contains a plausible target, say so. Read-only work may inspect each; ask before a write whose destination remains ambiguous.
- For an untargeted request such as "check Linear", use the repository's documented team or issue prefix when present. Otherwise list the relevant teams from the configured workspaces before choosing.

Reads are allowed when they serve the request. Create, update, close or comment only when the user asked for that mutation.

The helpers require Python 3. [scripts/read-credential.py](scripts/read-credential.py) requires a nonempty, single-line environment credential before any request. [scripts/check-response.py](scripts/check-response.py) preserves the response and exits nonzero for GraphQL errors, invalid data or an explicit mutation failure. Inspect the returned entity before claiming success. Never automatically retry a mutation after an uncertain outcome; reconcile current state first.
