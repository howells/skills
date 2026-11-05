---
name: gog
description: "Work in Gmail, Calendar, Drive, Docs and Sheets through the authenticated gog CLI instead of Google connectors. Not for web research (`web-research`)."
---

# GOG

Use the installed `gog` CLI for Google services, not Google connectors. Its help and `gog schema <command path> --json` are authoritative; check them before an unfamiliar command rather than guessing flags.

```bash
gog --account <email> --json --no-input --wrap-untrusted --readonly <command>
```

## Accounts

- List them with `gog auth list`. Use the account the user names, or one the repo explicitly identifies. For an unspecified read, query each plausible account and label the results. Ask before a write whose account is ambiguous.
- On an auth error, report it. Don't log in, add or remove credentials, set a default account, or swap in a connector unless asked.

## Gotchas

- **Pagination differs per command.** Gmail message search uses `--all`; calendar events use `--all-pages` (`--all` there means all calendars); Drive search uses `--page`. A first page is not a complete review. Use `--results-only` only once completeness is settled.
- **`gog search` is Drive.** Email is `gog gmail messages search`.
- **`--sanitize-content` strips URLs.** `gmail thread get <id> --full --sanitize-content` is lean for reading prose; fetch unsanitised when links matter.
- **Gmail quota is easy to burn.** Search narrowly by correspondent, subject and date without `--include-body` or `--full`, then fetch only the bodies you need. Reuse IDs and content already fetched. No parallel or overlapping searches on one account; other tasks may share the quota.
- **Rate limits** (`rateLimitExceeded`, `userRateLimitExceeded`, 429) aren't auth failures. Honour `Retry-After`, otherwise back off; at most two retries this turn, then report the search as incomplete. Never rotate accounts to dodge a quota.

## Writes

Send mail, change events, share files or call `gog api call --allow-write` only when the user asked for that write. Drop `--readonly` only then. Preview with `--dry-run` where supported, add `--gmail-no-send` to any write that isn't sending mail, and use `--force` only when the user asked to skip confirmation for that exact action. If a send's outcome is uncertain, check Sent before retrying.
