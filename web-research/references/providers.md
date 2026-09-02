# Exa and Tavily routing

These APIs change. For parameters not covered here, consult the current provider indexes before calling them:

- Exa: <https://exa.ai/docs/llms.txt>
- Tavily: <https://docs.tavily.com/llms.txt>
- Tavily's official agent skills: <https://github.com/tavily-ai/skills>

## Choose the operation

| Need | Exa | Tavily |
| --- | --- | --- |
| Broad or semantic discovery | `POST /search`, normally `type: auto` with `contents.highlights: true` | `POST /search`, normally `search_depth: basic` |
| Technical docs or code examples | `/search` with a precise natural-language query, usually `type: fast`, optionally restricted to official or code domains | `/search` with official domains and `advanced` depth when precision warrants the extra credit |
| Read known URLs | `POST /contents` with `urls` and query-focused `highlights` | `POST /extract` with `urls`; add `query` and `chunks_per_source` for long pages |
| Discover pages within one site | Search plus Exa subpages when the target is known | `POST /map`, then extract only the useful URLs |
| Read a substantial bounded site | Exa contents with deliberate `subpages` | `POST /crawl` only when map plus extract would omit needed pages |
| Multi-angle research | `/search` with `deep-lite`, `deep` or `deep-reasoning` when the extra reasoning is justified | `POST /research`: `mini` for narrow work, `pro` for genuinely multi-domain work |

Do not invoke Exa Agent by default. It is a beta, long-running and potentially expensive API intended for open-ended research, list building and enrichment. A deep `/search` plus Tavily Research covers ordinary research without introducing another asynchronous workflow.

## Exa

### Search

`POST https://api.exa.ai/search` uses `Authorization: Bearer` in the current coding-agent reference.

- Keep `text`, `highlights` and `summary` inside `contents`.
- Prefer `highlights: true` for agent work; full text consumes far more context.
- `type: auto` is the normal default. Use `fast` for latency-sensitive or code searches and a deep variant only for complex synthesis.
- Use `contents.maxAgeHours: 0` only when every result must be freshly crawled. Omitting it allows cached content with live retrieval as fallback.
- Use `includeDomains`, `excludeDomains` and publication dates when the question supplies real constraints.
- Do not use deprecated `useAutoprompt`, `tokensNum`, top-level content fields or `livecrawl` parameters.

### Contents

`POST https://api.exa.ai/contents` uses `Authorization: Bearer` rather than the Search API's `x-api-key` header.

- Supply `urls`, not a search query.
- Prefer query-focused `highlights`; request `text` when the whole document matters.
- Use `subpages` and `subpageTarget` deliberately for documentation hubs.
- PDFs and JavaScript-rendered pages are supported, but validate returned content before relying on it.

### Answer

`POST /answer` can provide a cited answer for a bounded factual question. Send `stream: false` when a JSON response is required. Treat it as a cross-check or lead. The final synthesis must still inspect and cite the underlying sources.

## Tavily

All Tavily endpoints use `Authorization: Bearer`.

### Search and extract

- Keep search queries under 400 characters and split genuinely distinct questions.
- Use `basic` search for normal work; `advanced` costs more and is for precision-sensitive questions.
- Use `include_domains`, `exclude_domains`, topic and date filters when they reflect the question.
- Search with raw content is convenient for a few results. For control, filter the discovered URLs and call `/extract` with `query` and `chunks_per_source`.
- Try basic extraction first; use advanced extraction for JavaScript-heavy pages, tables or failed basic extraction.

### Map and crawl

Map discovers URLs without retrieving their content. Prefer map followed by targeted extraction when researching a documentation site. Crawl returns content from many pages and should be reserved for cases that truly need the site rather than a handful of pages.

### Research

`POST /research` returns a request ID. Retrieve it with `GET /research/{request_id}`.

- Use `mini` for focused questions and `pro` for complex multi-angle work.
- Give the request the user's real scope, constraints and known context.
- Check once after doing other source work rather than repeatedly polling and narrating an unchanged task.
- If it is still running, finish the remaining source work and check once more. If it remains incomplete, proceed with the evidence already collected rather than polling again.
- Treat its report and citation list as one research input. Verify decisive claims against the cited pages.

## Reconcile the providers

1. Canonicalize and deduplicate URLs, syndicated copies and repeated claims.
2. Rank sources by authority for the claim: the owner of a fact, specification or dataset outranks commentary about it.
3. Compare dates and distinguish publication date from the date an event occurred.
4. Open the source pages that support the decisive claims; do not cite search result pages.
5. When sources disagree, state the disagreement and explain which source is stronger rather than silently averaging them.
6. Write a single answer at the detail level the user asked for, with links adjacent to supported claims.
