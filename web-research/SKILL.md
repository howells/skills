---
name: web-research
description: "Research the open web with Exa and Tavily and synthesize one cited answer. Not for browser QA (`fieldtest`) or scraping (`firecrawl-*`)."
---

# Web research

Use Exa and Tavily as complementary research providers, then write one synthesis yourself. Firecrawl is not part of this skill.

## Authentication

Inject `EXA_API_KEY` and `TAVILY_API_KEY` from the user's configured secret manager or environment into the request subprocess. Only the selected provider's key is required for a call. This skill contains no account inventory, vault names or credential-file paths.

Use [scripts/request](scripts/request) to call either API without exposing a key in diagnostics or command arguments. Never copy keys into a project `.env` or substitute another search provider because authentication failed. Report which provider is unavailable and any resulting coverage gap. Credential loading must be non-interactive and bounded by the host's timeout; do not initiate login as a repair step.

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

The bundled helpers require Python 3. [scripts/read-credential.py](scripts/read-credential.py) requires a nonempty, single-line environment credential before any request. Inject secrets before invoking the helper; it never reads a credential file or initiates authentication.
