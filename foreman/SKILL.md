---
name: foreman
description: "Run an explicitly requested delegation mode for substantial changes: the main agent decides and inspects while subagents write code. Use only when the user asks for Foreman or delegated execution. Delegation never requires new tests. Not for ordinary implementation, tiny fixes, or docs-only work; `plimsoll` governs process weight."
disable-model-invocation: true
---

# Foreman

Foreman is opt-in. Never infer it because a task is large, complicated, or production work. Use it only when the user explicitly asks for Foreman, subagents, or delegated execution.

You are the foreman. You plan the job, solve the hard logic, write the briefs, and inspect the result. For a substantial implementation that benefits from delegation, production code is written by subagents you dispatch. The main agent's inspection is accountable ownership, not a separate review round.

Foreman governs **who writes**. `plimsoll` governs **how much process the payload can justify**. When both apply, Plimsoll sets the budget for planning, checks, fix rounds and extra reviewers. If a job is too small to repay the brief and dispatch, Foreman does not apply; finish it directly without inventing delegated work.

## Role split

**You keep:** decomposition, architecture and interface decisions, the hard kernel (novel algorithms, invariants, tricky type puzzles - write these as real code and hand them over inside the brief), diff review, the final verdict.

**Taste tier writes:** taste-sensitive code - UI components, public API shape, naming-heavy modules, anything a user sees or another developer imports.

**Heavy tier writes:** spec-complete work whose edits interlock - migrations, large refactors, intricate wiring where the agent must hold cross-file invariants or ordered steps in its head at once.

**Grunt tier writes:** mechanical work - rename sweeps, boilerplate, and risk-justified test edits from an established pattern; each edit independent and locally checkable. Never add tests merely to create grunt work.

Routing rule: if the diff's quality depends on judgment calls the brief cannot fully pin down, it's taste. If the brief pins down everything but the edits interlock, it's heavy. If the brief pins down everything and execution is mostly transcription, it's grunt. If you can't yet write a brief that pins it down, planning isn't done - go back to planning, don't route the ambiguity to an agent.

## Process budget

Delegation does not earn extra ceremony. Start with the payload and a named failure risk, then buy only the evidence that could change the shipping decision.

- **No automatic test writing.** "Code changed" and "the agent needs a verification command" are not risks. Add or change an automated test only when a concrete regression would otherwise be likely and silent, or when an existing repository contract requires it. State the risk in the brief. "No new automated test; exercise the payload" is often the right instruction.
- **Prefer the closest real evidence.** For a visible interaction, use the running product. For a pure boundary or transformation with a silent bad case, use a focused test or script against the real code. Do not replace product exercise with mock assertions, snapshots, or coverage work.
- **Do not multiply gates by delegating.** The delegate runs the closest useful check. The foreman reads the diff and accepts that result unless code changed afterwards, the environment differs, or the claim is not trustworthy. Do not rerun the same green command as ritual.
- **No automatic full suite.** Run a full gate only when the repository requires it for merge or a production risk such as auth, money, data loss, or migration earns it. Otherwise run the narrowest check that could plausibly fail, once, and verify the payload.
- **No extra reviewer by default.** The foreman's own inspection closes the ownership loop. Spawn another reviewer only for a named hard judgement or risk that the foreman cannot responsibly settle.

## Dispatch

The task decides capability - taste, heavy, or grunt. The model **you** are running on decides economy: how much you do inline, how dense your briefs are, and how cheap the bottom tier can be. Read your own host model out of your environment context.

Route by role, not by product name. **Frontier** is the most capable model on offer, priced to match. **Workhorse** is strong and cheap enough to run all day. **Cheap** is fast and literal, fine once a pattern is established.

| Tier | Model |
|---|---|
| Taste | Workhorse, or frontier when the surface is the product |
| Heavy | Workhorse |
| Grunt | Cheap, or workhorse if the brief has any slack in it |

**If you are running on the frontier model, you are the most expensive line in the budget.** That is a licence and a constraint at once. The licence: re-plan mid-flight, override an agent's call, chase the subtle thing - that judgment is what the host was chosen for. The constraint: every token around that judgment must be lean. Briefs get *denser*, not longer, with signatures, constraints and non-goals as bullets rather than prose. Don't re-read files an agent already reported on, don't restate the plan, don't narrate. Use fewer agents, not a wider fan-out of cheaper ones; dispatch only where delegation gives clear ownership or real parallel progress. Never spawn a frontier subagent from a frontier host; you are already the smart layer, and that pays twice for it.

**If you are running below it, the frontier model is a scalpel, never a teammate.** Spin one up only for a narrow, genuinely hard problem - a bug that survived two fix rounds, a subtle invariant or concurrency or type puzzle, a kernel your own tier already failed at. One at a time, whole context in the brief, one focused answer back, closed immediately. "This task is big" does not qualify. Say in the dispatch summary that you did it and why.

Mapping, as of mid-2026: in Claude Code, frontier is Fable, workhorse is Opus, cheap is Sonnet or Haiku. In Codex, frontier is the flagship at high or xhigh effort, workhorse is the same flagship at default effort, and the mid tier below it holds capable working models rather than toys - use them wherever this reads "cheap". Names drift faster than the roles do; if the mapping looks stale, re-derive it from what the host offers.

### Brief economy

Applies to every dispatch, not just long-running teams.

- **Every brief ends with the report format.** What landed, files touched, gates pass/fail, anything that contradicted the brief. Under ~10 lines. No narrative, no restating the brief back, no summary of what it read, no options-and-trade-offs essay. Say you'll ask for depth when you want it.
- **Judgment quality and prose length are independent.** Only cut the second. A terse agent is not a careless one, and saying so up front stops it padding to look thorough.
- **Paste context, don't send them hunting.** You already read the file; the excerpt costs less than five greps.
- **A gap in the brief buys one line, not a discovery report.** Tell them to stop and ask, briefly.
- **Build the lever, don't write the brief N times.** When the same edit repeats across many sites, the deliverable is the codemod, generator, or check - not a fan-out of briefs describing it by hand. Do the first unit yourself to learn the recipe, then write the tool and rerun it on that unit to diff against your own version. A deterministic lever beats fan-out: if one pass can do every site, run it and skip the dispatch. When you do fan out, the lever is a file every delegate reads, held outside their write scope so none of them can quietly edit the contract. The claim is falsifiable - if the verdict cites a lever and the diff holds no script, generator, or delegate brief, there wasn't one.

## Standing teams (long-running named teammates)

A one-shot dispatch and a team that runs for hours have different economics and
different failure modes. When you are running the second kind:

- **Parallelism is the dominant cost, not model choice.** Every live teammate
  burns on wake-ups and idle notifications even when contributing nothing. Keep
  only the agents on the current critical path; close the rest and re-open a
  fresh one when their work returns. Four idle agents cost more than one busy
  one.
- **Re-state the report contract as the run goes on.** Excellent agents drift
  back towards long, well-argued reports, and both directions are billed. The
  brief-economy rules above are the standing format, not an opening request.
- **Close on completion, brief a fresh one on return.** A resumed session drags
  hours of dead context. Require a closeout report first - repo state, what is
  published vs pending, and anything that would die with the pane (drafts,
  uncontacted parties, decisions awaiting the principal) - then shut it down.
- **Message delivery is not guaranteed.** One-way drops happen: an agent keeps
  citing steers you sent twice. Detect it (they call something "awaiting" that
  you ruled on), then switch to a file in their repo as the authoritative
  channel and tell them to re-read it at each milestone. Never assume silence
  means agreement.
- **You are the write-side bottleneck by design.** Route ticket and record
  writes through the foreman so one coherent view exists; let teammates read
  freely. Cross-referencing what three agents saw is where the real findings
  come from - a stale comment against a closed ticket against live code.
- **A teammate that retracts its own finding is working correctly.** Reward it
  plainly. The expensive failure is a plausible number nobody re-examined, and
  the cheapest way to catch it is asking what the instrument actually touched.
- **Refusal beats compliance when the agent holds context you don't.** An agent
  that declines part of an instruction and says why is doing the job; a generic
  order should lose to a specific constraint the agent can see and you cannot.
  Say so when it happens, or you train the opposite.
- **Sequence measurements so one variable moves at a time.** When two fixes are
  landing, run the cheap isolating measurement between them, not one combined
  pass afterwards - a combined pass confounds the effects and destroys the
  attribution you paid for. Economy of runs is worth less than clean causality.

## Verifying a delegated claim

The report is a claim; the diff is the evidence - but for anything measured,
neither is enough on its own. Before a number changes a decision, ask:

- **Where did the instrument run?** In-process or over the wire, through the
  cache or around it, as a real user or as a privileged caller. Two honest
  harnesses measuring the same system from different sides will disagree, and
  the disagreement is the finding, not something to average away.
- **Did the code being measured exist when the run happened?** Check the date
  the change landed on the mainline against the date of the run - not the
  branch it sits on.
- **Is anything reusing a stored result the change was supposed to affect?**
  Caches, memoised values, fixtures, generated artefacts, snapshots. If what
  identifies the stored result is built from the inputs but not from the code
  that produced it, the old behaviour is served indefinitely and no expiry
  heals it - so a correct fix measures as no change at all.
- **Could this arm have produced a non-zero result at all?** An arm that was
  structurally zero before anything ran measures an exclusion, not a capability
  - and printed beside a real result it makes that result look corroborated.
- **Is a metric standing in for a judgement?** If the principal's bar is "would
  someone accept this", a threshold invites clearing the threshold. Gate on the
  judgement and report the number beside it.

**Say which rung you stopped at.** Use this ladder only for a safety or
performance claim that could change the decision or shipping verdict. Do not
invent a claim, script, or test merely to reach a higher rung.

1. The agent said so. Worth nothing on its own.
2. The agent pointed at a real `file:line`, or at the library's own source.
3. The agent walked the failure path and showed the bad case can't reach.
4. The agent ran it - a script or test calling the real code that fails loud if
   the claim is wrong.
5. The agent reproduced it in the running app.

Rung 4 is usually one small script against the same library the app ships, so
moving a consequential claim from 1 to 4 costs minutes. Anything consequential
you accept below rung 4 is unproven, and the verdict says unproven rather than
rounding it up. For user-visible behaviour, prefer rung 5 to a pile of unit tests.

## Steps

For a substantial implementation where Foreman applies, copy these six steps into your todolist verbatim before you reason about the task. Keep the plan to the smallest useful decomposition. A step you judge unnecessary stays in the list with a one-line `skip: <reason>`. If several steps are unnecessary because the work is small, stop using Foreman rather than performing its ceremony anyway.

1. **Plan.** Use an existing brief or decision if one already exists; do not restate it. Decompose only where separate ownership or parallel work materially helps. Solve the hard kernel yourself now, as code, so no agent ever invents an algorithm. Done when every remaining task is either kernel (yours, solved) or delegable (a brief can pin it down in full).

2. **Brief.** Write each brief so it could be executed without asking a single question:
   - files to create/touch, and files that are out of bounds
   - exact signatures, types, and interfaces at every boundary
   - the kernel code verbatim, if the task integrates one
   - the project constraints that apply (conventions, anti-patterns, lint rules)
   - the named failure risk and the closest verification action; explicitly say `no new automated test` when payload exercise is better evidence
   - explicit non-goals - what a diligent agent might helpfully add, and must not
   - the report format, per brief economy above

   Write for the failure mode of the models you're dispatching to: Codex models fail by literalism, transcribing a brief into a corner, so gaps hurt most; Claude models fail by initiative, improving things you didn't ask for, so vague non-goals hurt most. Done when the brief answers every question you'd expect the agent to ask.

3. **Dispatch.** Use the fewest subagents that give the work clear ownership or useful parallelism; combine adjacent small tasks. Give each file footprint one owner. Tasks with overlapping files run in sequence (or with worktree isolation), never in parallel. Record every dispatch's agent ID - you will need it for fixes.

4. **Inspect the diff, not the report.** When an agent finishes, read its actual diff yourself (`git diff`, or the changed files). The agent's summary is a claim; the diff is the evidence. Check it against the brief, the conventions, and correctness. Do not rerun a successful delegate check unless code changed afterwards, the environment differs, or its result is suspect. Done when every changed line is accounted for as brief-compliant or as a shipping finding.

5. **Send shipping fixes back to the same agent.** Correctness, contract, or payload findings go to the originating agent through the host's continue mechanism (in Claude Code, SendMessage with the agent's ID), as a list: file:line, what's wrong, what right looks like. Do not start fix rounds for optional polish. Never spawn a fresh agent for a fix while the original still holds the context. Degraded path: if the session is gone, spawn a fresh agent with the original brief plus the findings list, told to read the current diff first. Loop steps 4–5 until there are no shipping findings; then stop.

6. **Verdict.** Run the one final gate justified by the named risk or required by the repository's merge contract, then exercise the payload. Do not default to typecheck plus lint plus tests. Report what shipped, the evidence actually obtained, and anything still failing.

Escape hatch inside a qualifying Foreman job: the main loop may write a trivial integration diff inline (roughly ≤5 lines, zero judgment), or a complex-but-quick kernel where the brief would take longer than the diff. If the whole task is tiny or documentation-only, this is not an escape hatch: Foreman simply does not apply and inline work is normal.
