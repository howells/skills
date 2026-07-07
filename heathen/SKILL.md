---
name: heathen
description: No gods, no god files. Find and refactor god components, god scripts, oversized modules, tangled multi-responsibility files, and duplicated logic in JavaScript/TypeScript codebases. Use when asked to audit for large components or scripts, split files into meaningful pieces, simplify overgrown React components, identify duplicated code, extract shared logic, or create a safe decomposition order with tests.
---

# Heathen

No gods, no god files. Find oversized or duplicated code, then split it in a safe order. Prefer evidence over instinct: measure candidates, read the worst files, identify actual responsibilities, and refactor one behavioral boundary at a time.

## Core Rule

Do not split files just because they are long. Split when the file has multiple responsibilities, duplicated logic, unstable change reasons, hard-to-test branches, or a public interface that can be made smaller.

## Workflow

1. Run the scanner (paths below are relative to this skill's directory):

   ```bash
   python3 scripts/find-god-files.py /path/to/repo
   ```

   Use `--json` when another tool or script will consume the report. Use `--include-tests` when the user asks about duplicated test logic or test-suite cleanup.

2. Read the highest-ranked candidates before proposing changes. Confirm whether each candidate is truly overloaded or just necessarily dense.
3. Classify each confirmed candidate:
   - `god-component`: React component doing rendering, data shaping, effects, mutations, validation, and subview control in one file.
   - `god-script`: CLI/build/migration script mixing argument parsing, I/O, domain logic, formatting, and side effects.
   - `god-module`: non-UI module with multiple unrelated responsibilities.
   - `duplication`: repeated functions, schemas, UI fragments, query builders, scripts, or formatting logic.
4. Produce a split order:
   - Extract pure helpers first.
   - Extract duplicated logic before moving callers.
   - Extract hooks/state machines before child components when state is tangled.
   - Extract leaf subcomponents before layout shells when JSX is large.
   - Extract I/O adapters away from domain logic in scripts.
   - Keep public imports stable until tests pass, then clean up barrels/exports.
5. If the user asked for an audit or report, stop after the split plan unless they explicitly approve edits.
6. If the user asked for implementation, refactor one candidate at a time. After each step, run the smallest relevant test/typecheck/lint command.
7. Stop when the requested scope is handled. Do not turn a focused decomposition into a broad architecture rewrite.

## Split Patterns

For React components:

- Move data fetching/mutations into a hook only when it is reused or when it removes real branching from the component.
- Move pure formatting and derivation into local utilities.
- Move repeated JSX into named domain components, not generic `Content`, `Wrapper`, or `Container` components.
- Keep related state near the component that owns the interaction.
- Avoid creating many shallow files where every file must be opened to understand one small behavior.

For scripts:

- Separate argument parsing, configuration, domain transformation, I/O, and output formatting.
- Put deterministic transformation logic behind a function that can be unit tested without shelling out.
- Keep the executable entrypoint thin.
- Preserve exit codes and stderr/stdout behavior unless intentionally changing them.

For duplication:

- Prefer consolidating duplicated behavior after confirming the copies are meant to stay the same.
- Do not merge coincidentally similar code with different domain meaning.
- Extract shared schemas/types only when they represent the same concept.
- Replace copy-pasted tests with shared fixtures only if failures remain readable.

## Output Shape

When auditing, report:

- Candidate path.
- Evidence: line count, function/component counts, duplicated blocks, mixed responsibilities.
- Why it is or is not a real god file.
- Proposed split sequence.
- Tests or checks to run after each split.

When implementing, report files changed and the verification command results.

## Scanner

Use `scripts/find-god-files.py` (relative to this skill's directory) to find likely candidates. It is intentionally heuristic: it ranks files and duplicate blocks, but the agent must still read the code and make a judgment. By default it flags files scoring at least 35 (roughly: length past ~200-500 lines combined with multiple responsibility signals); lower `--min-score` to widen the net.

Useful options:

```bash
python3 scripts/find-god-files.py /repo
python3 scripts/find-god-files.py /repo --min-score 20 --duplicate-window 10
python3 scripts/find-god-files.py /repo --include-tests
python3 scripts/find-god-files.py /repo --json
```
