---
name: review
description: "Get an independent review with fable, sol, muse (wonder), opus or astra, then verify its claims. Use for a named-model second opinion on code, a decision or stated criteria. Not for a codebase health grade (`simplify`) or browser QA (`fieldtest`)."
---

# Review

One workflow, with a model argument selecting the review lane. The outside model returns leads; verify them before treating them as findings or acting on them.

## Invocation

Use `review <model> <question or scope>` in the host's skill syntax:

```text
$review fable challenge this architecture decision
$review sol check this change against the acceptance criteria
$review muse review this plan's assumptions
$review wonder review this plan's assumptions
$review opus argue against this proposed design
$review astra find where this diff breaks the retry contract
```

In Claude Code, use `/review` with the same arguments. Model arguments are case-insensitive. `wonder` is an alias for `muse`; both select Muse Wonder. Accept only `fable`, `sol`, `muse`, `wonder`, `opus` and `astra`. An unsupported argument stops selection; do not silently reinterpret it as another model.

Honour a model the user already named. If no model is named, choose Fable for a judgement call, Astra for a question the repository can settle, or Sol for a bounded check against stated criteria, and announce the choice. Opus and Muse Wonder are available when requested; the model argument does not restrict the kind of question they can review.

| Argument | Model family | CLI route |
| --- | --- | --- |
| `fable` | Claude Fable | Claude, file reads |
| `sol` | GPT Sol | Codex, read-only commands |
| `muse`, `wonder` | Muse Wonder | Muse, file reads |
| `opus` | Claude Opus | Claude, file reads |
| `astra` | GPT Astra | Codex, read-only commands |

Resolve the current model from the host's live catalogue or the CLI's supported aliases. A family argument selects the newest standard version available, unless the user specified a version. Do not silently replace a family, provider, or explicitly requested version. Use high reasoning effort unless the user requests another supported effort.

## Build an independent brief

Investigate first. Give the outside model a brief someone without this conversation could act on:

- The exact question or decision, with the relevant review lenses.
- The artefact: paths, relevant excerpts, base commit or range, and current working-tree status. Include untracked files when they are part of the change.
- The options and proposed direction, the constraints, settled decisions and explicit non-goals.
- Validation already run, its outcome and remaining uncertainty. Run tests yourself if they write caches or build output.
- Evidence from outside the repository that the model cannot retrieve.
- The boundary, verbatim: `Read-only review. Do not edit files or run state-changing commands.`

For a file-only route, include the diff and history excerpts it needs; it cannot run `git`. For a route with read-only commands, name the base and let it inspect the diff itself. Ask for a verdict, evidence with `file:line` citations, disagreements, concrete changes, and what would change its mind. Separate checkable claims from judgement calls.

Start a fresh context with only this brief. Repository instructions may still load; independence means it has not inherited this conversation or the author's conclusions. Do not resume the author's session. If the selected model is also the authoring model, disclose that the context is independent but the model is the same.

## Send the brief

When the harness can start its own thread or task for a chosen model with a fresh context, run the review there, as T3 Code does with `delegate_task`. The user can watch and open that thread, and the harness reports its completion. Follow [references/delegation.md](references/delegation.md), and check that route before reaching for a CLI. Only when the harness has no such route, or cannot run the selected model, use the provider's CLI:

- Fable or Opus: [references/claude.md](references/claude.md).
- Sol or Astra: [references/codex.md](references/codex.md).
- Muse or Wonder: [references/muse.md](references/muse.md).

For CLI process handling, read [references/process.md](references/process.md). Keep transient briefs and captured replies outside the repository. They support the invocation; the report is a message, and durable decisions belong on the owning tracker item.

A started process or accepted task is not a completed review. Require successful completion and a non-empty final answer, with the selected model's identity established by the route's metadata. If identity cannot be established, label it unverified. Report authentication, quota, billing, rate-limit, unavailable-model or permission failures and stop. Retry once only for a transport or internal-server failure, after establishing that the original invocation has stopped.

## Verify and report

Check every material claim against the source, diff, tests or running product. Rerun commands supporting a load-bearing claim. Label leads you cannot confirm as unconfirmed, and do not convert opinions into factual findings.

Return:

- The question and selected model, including any identity or isolation limitation.
- Its verdict and whether you agree, with the reason for any disagreement.
- Verified findings, most severe first, with evidence.
- Claims that failed verification and what you found instead.
- Recommended changes, distinct from changes already made, and unresolved objections.
- Any failed or incomplete invocation.

Do not paste the outside reply as the report. Implement changes only when implementation is already authorised. A requested further review starts a fresh context carrying the original brief, prior claims, your verification and responses, and remaining objections.
