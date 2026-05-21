---
name: mastra-audit
description: Audit Mastra implementations in JavaScript/TypeScript codebases. Use when checking whether a codebase follows current Mastra guidance from the $mastra skill, keeps all direct mastra/@mastra dependencies and imports inside one approved package, organizes Mastra code into domain folders such as agents, tools, workflows, prompts, memory, storage, runtime, observability, MCP, and scorers, and reports concrete remediation steps.
---

# Mastra Audit

Audit a codebase for two things:

1. Mastra is implemented according to the current `$mastra` skill and the installed Mastra documentation.
2. Mastra is architecturally contained and organized: one approved package owns Mastra, and that package uses domain folders instead of scattering agents, tools, prompts, workflows, runtime, memory, storage, observability, MCP, or scorers across the codebase.

## Non-Negotiables

- Use `$mastra` before judging API correctness. Mastra changes quickly; do not rely on model memory for constructor signatures, model routing, storage, memory, workflow, or tool APIs.
- Exactly one package or module may own Mastra tooling. In a Turborepo, this should be one workspace package.
- Only the approved Mastra package may declare `mastra` or `@mastra/*` dependencies.
- Only the approved Mastra package may import from `mastra` or `@mastra/*`, or run direct Mastra CLI commands.
- Apps and other packages must call the approved package's public API instead of constructing Mastra objects directly.
- Mastra implementation code must be organized by domain under `src/`, using folders such as:
  - `agents/`
  - `tools/`
  - `workflows/`
  - `prompts/` or `agents/prompts/` when prompts are shared or substantial
  - `memory/`
  - `storage/`
  - `runtime/`
  - `observability/`
  - `mcp/`
  - `scorers/` or `evals/`

## Audit Workflow

1. Identify the repo root. Prefer the current working directory when it contains `turbo.json`, `pnpm-workspace.yaml`, or a workspace `package.json`.
2. Identify the approved Mastra package:
   - Use the user's explicit package path/name if provided.
   - Otherwise run the scanner and auto-detect only when exactly one workspace declares `mastra` or `@mastra/*` dependencies.
   - If zero or multiple candidates exist, report ambiguity and ask the user to choose before remediation.
3. Load `$mastra` and follow its current-docs workflow:
   - Check whether Mastra packages are installed.
   - Prefer embedded docs for the installed version.
   - Use source/types only when embedded docs are insufficient.
   - Use remote docs only when packages are unavailable.
4. Run the scanner:

   ```bash
   python3 /path/to/mastra-audit/scripts/audit-mastra-implementation.py /path/to/repo --allowed-package packages/mastra
   ```

   Omit `--allowed-package` only when auto-detection is acceptable.

5. Manually review the approved package against current Mastra docs:
   - TypeScript config supports ES2022/bundler semantics, directly or through an audited shared config.
   - Models use the current provider/model format required by `$mastra`.
   - Agents, tools, workflows, memory, storage, observability, and MCP usage match the installed docs.
   - Mastra runtime/registration code composes domain exports instead of hiding implementation in app code.
   - Prompts are not buried in unrelated files when they are shared, long, or reused.
   - Tests cover agent/tool/workflow contracts and any boundary-facing public API.
   - Studio or `mastra api` can inspect the implementation when runtime verification is needed.
6. Report findings with severity, file paths, and concrete next steps. Clearly separate:
   - deterministic scanner findings,
   - documentation/API correctness findings from `$mastra`,
   - design/organization concerns.

## Remediation Guidance

When fixing issues:

- Move all Mastra setup, agents, workflows, tools, storage, memory, provider wiring, and runtime registration into the approved package.
- Move misplaced implementation files into domain folders.
- Extract shared or substantial prompts into `src/prompts/` or `src/agents/prompts/`.
- Export a narrow internal API from the approved package.
- Replace outside `mastra` or `@mastra/*` imports with imports from the approved internal package.
- Move `mastra` and `@mastra/*` dependencies from outside packages into the approved package.
- Keep app packages framework-focused.
- Keep test-only mocks separate from production paths.

After edits, rerun the scanner and relevant package-scoped tests/typechecks.

## Scanner

Use `scripts/audit-mastra-implementation.py` for deterministic checks. It reads workspace package manifests, scans source files, checks Mastra dependency/import boundaries, verifies common package/config signals, and flags Mastra implementation code outside expected domain folders.

Useful options:

```bash
python3 scripts/audit-mastra-implementation.py /repo
python3 scripts/audit-mastra-implementation.py /repo --allowed-package packages/agent-runtime
python3 scripts/audit-mastra-implementation.py /repo --allowed-package @acme/agent-runtime --json
```
