# Issue tracker: Linear

Issues and specs for this repo live in **Linear**, team `SKI` (Skills). Linear is the record - findings, plans and specs are written up as Linear items rather than markdown in this repo, and Linear wins when the two disagree.

| | |
| --- | --- |
| Organisation | `Howells` (`howells`) |
| Organisation id | `e51748f5-c341-4ed5-904e-470fdad941aa` |
| Team | `SKI` - Skills |
| Team id | `d3a6071b-7765-4477-a72c-3047ecd2dff5` |
| Board | https://linear.app/howells/team/SKI |

## Access

Prefer the **Linear MCP server** when it is connected - authenticate with `mcp__plugin_linear_linear__authenticate` and use its tools. Always pass `org_id`, and pass labels as a JSON array.

When MCP is unavailable, use the GraphQL API at `https://api.linear.app/graphql` with a personal API key from the `LINEAR_API_KEY` environment variable:

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query":"..."}'
```

**Never commit the key.** It belongs in the environment, never in this file or any other tracked file.

## Conventions

- **Create an issue**: `issueCreate` with `teamId` set to the SKI team id above. Title in the imperative; body in markdown.
- **Read an issue**: query `issue(id: "SKI-12")` - the human identifier works wherever an id is accepted. Request `comments { nodes { body user { name } } }` to read the thread.
- **List issues**: `issues(filter: { team: { key: { eq: "SKI" } } }, orderBy: updatedAt)`, adding a `labels` filter to scope to a triage state.
- **Comment**: `commentCreate` with `issueId` and `body`.
- **Apply / remove labels**: `issueUpdate` with the full `labelIds` array. Linear replaces rather than merges, so read the current labels first and send the whole set.
- **Close**: `issueUpdate` with `stateId` set to the team's `Done` state (or `Canceled` for `wontfix`).

Search with `searchIssues(term: "...")`. The `filter` argument has no free-text `contains` operator - reaching for one returns a schema error.

## Workflow states

`Backlog`, `Todo`, `In Progress`, `In Review`, `Done`, `Canceled`, `Duplicate`.

Triage labels layer on top of these rather than replacing them - an issue can be `Todo` and `needs-info` at once. See `triage-labels.md`.

## When a skill says "publish to the issue tracker"

Create a Linear issue on team `SKI`.

## When a skill says "fetch the relevant ticket"

Query the issue by its `SKI-<n>` identifier, including comments.

## Pull requests as a request surface

**No.** This repo's PRs are not a triage queue. Work arrives as Linear issues.

## Wayfinding operations

Used by `/wayfinder`. The **map** is one Linear issue; **tickets** are its sub-issues.

- **Map**: an issue labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body.
- **Child ticket**: an issue with `parentId` set to the map's id, labelled `wayfinder:<type>` (`research` / `prototype` / `grilling` / `task`). Once claimed, assign it to the driving dev.
- **Blocking**: Linear's native issue relations - `issueRelationCreate` with `type: "blocks"`. A ticket is unblocked when every blocker reaches a completed or cancelled state.
- **Frontier query**: the map's open children, minus any with an open blocker or an assignee; first in map order wins.
- **Claim**: `issueUpdate` setting `assigneeId` to the current viewer. This is the session's first write.
- **Resolve**: comment the answer, move the issue to `Done`, then append a context pointer to the map's Decisions-so-far.

The `wayfinder:*` labels do not exist on `SKI` yet. Create them on first use.
