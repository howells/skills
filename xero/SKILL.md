---
name: xero
description: Query Xero accounting data through a configured integration. Not for Starling (`starling`).
---

# Xero

Use an existing authenticated Xero connector, API client or CLI. Discover the integration from available tools and project documentation, then inspect its current schema, help or source. This skill supplies no private repository, account inventory or credentials. If access is absent, report the missing setup instead of cloning a client or starting authentication unasked.

## Select the organisation

Honour the organisation or tenant the user names. Use the integration's supported read operation to inspect accessible organisations and select the matching identifier. Do not assume a default tenant. Read-only work may inspect plausible organisations; ask before an ambiguous selection changes the requested result.

Use credentials supplied by the configured client or secret manager. Keep secrets out of command arguments, logs, project `.env` files and examples. Allow the client's documented token refresh and private token cache; do not copy caches or create ad hoc credential files. Never initiate interactive authentication as a repair step without user intent.

## Query and report

1. Establish the organisation, requested records or report, date range, currency and accounting basis where relevant. Preserve the source's distinctions between cash and accrual, tax-inclusive and tax-exclusive, and draft and posted records.
2. Check that the chosen operation reads data. A command named “balances” or “report” may also persist rows or synchronise a database; inspect its behaviour before running it. Use a documented read-only mode when available. Local synchronisation and remote mutations require the user's request.
3. Follow the integration's pagination and filtering rules. Report partial access, missing pages and stale cached data. Do not equate a partial response with a complete ledger.
4. Bound each request or process tree, normally to 30 seconds per call. Report credential and API failures separately only when evidence distinguishes them; do not guess from silence or automatically retry an uncertain write.
5. Return the requested figures with organisation, period, currency, accounting basis and retrieval time. Reconcile totals to the returned records or report, and explain any gap instead of filling it with estimates.

Use the configured API integration directly; do not substitute browser scraping. For direct API work, consult current official Xero developer documentation for the selected authentication flow, tenant requirements and endpoints before constructing requests.
