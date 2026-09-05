---
name: web-research
description: "Research the open web with Exa and Tavily and synthesize one cited answer. Not for browser QA (`fieldtest`) or scraping (`firecrawl-*`)."
---

# Web research

Use Exa and Tavily as complementary research providers, then write one synthesis yourself. Firecrawl is not part of this skill.

## Authentication

Use the read-only 1Password service account token in:

`/Users/danielhowells/.codex/plugins/secrets/1password-service-account.env`

Source that file to set `OP_SERVICE_ACCOUNT_TOKEN`. This is non-interactive and must not prompt for 1Password authentication.

The provider credentials are:

- `EXA_API_KEY` from `op://keys/Exa/credential`.
- `TAVILY_API_KEY` from `op://keys/Tavily/credential`.

Use [scripts/request](scripts/request) to call either API without printing a key. Never copy the keys into a project `.env` or substitute another search provider because authentication failed.

Pass a complete JSON request body on standard input:

```sh
printf '%s' '{"query":"current timber reuse standards","type":"auto","numResults":5}' | scripts/request exa search
```

## Research

Read [references/providers.md](references/providers.md) before choosing endpoints. Use the cheapest operation that can answer the question:

1. Split the question into the factual claims or subquestions that need evidence.
2. Run Exa and Tavily discovery in parallel when independent coverage will improve confidence. Do not duplicate calls mechanically when one provider already returned the authoritative source.
3. Retrieve the underlying pages needed to support the answer. Search snippets and provider-written summaries are leads, not evidence.
4. Prefer primary sources, deduplicate URLs and repeated stories, and investigate material disagreement between providers.
5. Produce one direct synthesis with links beside the claims they support. Preserve uncertainty and source disagreement; do not paste two provider reports beside each other.

Use deep or agentic research only when ordinary search and extraction cannot answer the question. Provider-generated research reports remain inputs to the synthesis, not the final answer.

The bundled helpers require Python 3. [scripts/read-credential.py](scripts/read-credential.py) bounds each credential lookup to 30 seconds; a failure stops the request without interactive authentication.
