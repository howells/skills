# Reading T3 history

Use the live T3 tool schemas; names and pagination fields can change. A thread list establishes membership, not that its transcripts were read.

## Coverage

1. Record the requested date window, timezone, projects and a snapshot time. Follow every project/thread listing page in scope, including archived entries when requested. Separate empty project groups from inaccessible ones.
2. Record parent/child relationships and activity timestamps. A child may contain the actual work while a root contains only orchestration. Include children when the user asks for all transcripts; distinguish them in the coverage count.
3. Read each transcript through every message page. Recover truncated items with the returned item identifier and text offset until no continuation remains. A search excerpt alone isn't a full read.
4. Use activity/tool details to verify load-bearing claims, failures and ambiguous outcomes. Reading every message doesn't imply inspecting every tool result, image, video or embedded app. Name the actual coverage.
5. Keep identifiers and positions alongside evidence so a finding is recoverable. Report the snapshot and counts of projects, top-level threads, child threads, complete reads and gaps. For a moving corpus, don't imply coverage beyond the snapshot.

For broad reviews, keep a compact coverage ledger in tool state or temporary scratch storage. Put durable findings and evidence on the owning tracker item, not in repo reports.

## Attribution and current state

- Attribute the user's direct instructions separately from agent proposals, inherited context and peer messages. A handoff quoting an earlier message isn't a new user decision.
- Deduplicate inherited transcript excerpts rather than counting repeated copies as repeated incidents. Check the original item when the distinction matters.
- Preserve corrections and the final accepted direction. An abandoned plan doesn't establish what shipped.
- Check live peers before entering a checkout. A transcript status or a list of this thread's children isn't a census of every writer.
- Verify completion at the relevant source: code integration, actual data, rendered host or delivered artefact. State when that source is unavailable.

Link a thread as `[title](t3-thread://v1/<threadId>)` using its exact ID. Include an item ID or position where useful for a long transcript.
