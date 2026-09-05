---
name: fail-fast
description: "Remove hidden fallbacks, swallowed errors, legacy aliases and permissive defaults. Not for behaviour-preserving cleanup (`unslop`) or required compatibility."
---

# Fail Fast

Use this skill to make a codebase deterministic by finding and removing hidden fallback behavior that should be an explicit contract, validation error, migration, or test fixture.

State at the start that you are using the `fail-fast` skill.

## Core Rule

Prefer one canonical path and one explicit failure mode.

A fallback is allowed only when it is a real product requirement, a documented migration window, or an intentional local-test fixture. Everything else should become a validation error, required input, explicit branch, deleted compatibility layer, or typed configuration contract.

## Workflow

1. Identify the target repo and its package manager.
2. Run the scanner before editing (path is relative to this skill's directory):

   ```bash
   python3 scripts/scan-fallbacks.py /path/to/repo
   ```

   Useful flags: `--json` (machine-readable output for large audits or follow-up tooling), `--include-tests` and `--include-docs` (scan files skipped by default), `--fail-on medium|high` (exit non-zero as a CI gate).

   ```bash
   python3 scripts/scan-fallbacks.py /path/to/repo --json
   ```

3. Read `references/remediation.md` when findings involve environment variables, legacy compatibility, broad catch blocks, or staged migrations.
4. Classify each finding:
   - `remove`: dead compatibility, legacy aliases, duplicate option names, fallback branches without a live caller.
   - `require`: missing config, absent dependencies, invalid user input, or an env var that belongs in the environment schema.
   - `validate`: boundary input that must accept unknown data but should reject invalid states clearly.
   - `keep`: documented product behavior, real external API compatibility, or temporary migration with owner and removal date.
5. Edit narrowly. Remove the fallback state and update call sites/tests to use the canonical path.
6. Add or update tests that prove the code fails deterministically when the dependency, input, config, or schema-declared env var is missing.
7. Run the scanner again, plus the repo's relevant tests, typecheck, lint, or build.
8. Report remaining fallbacks explicitly. Do not leave them invisible.

## Environment Variables

Environment variables are configuration contracts, not suggestion fields.

In projects with a validated environment schema, required values should fail validation before application code uses them. Import typed values from the project's environment module. If a required key is missing from the schema, declare and validate it there rather than adding an application fallback.

Use the project's existing environment validation and build checks. Inspect its scripts and validator documentation for the actual commands; do not install a new package just to follow this skill.

Accept direct `process.env` reads only in env schema modules, generated env wiring, narrow system keys such as `NODE_ENV` and `CI`, or explicitly documented migration escape hatches.

Remove patterns like:

```ts
const apiKey = process.env.OPENAI_API_KEY || "dev-key";
const databaseUrl = process.env.DATABASE_URL ?? "postgres://localhost";
```

Replace with typed environment access:

```ts
const apiKey = env.OPENAI_API_KEY;
```

When no environment schema exists, validate required values explicitly at the configuration boundary using the project's existing conventions.

## Error Handling

Fail fast does not mean crash vaguely. It means fail at the boundary with a useful, typed, or contextual error.

Prefer:

- schema validation for external input,
- explicit thrown errors for impossible internal states,
- narrow `catch` blocks that rethrow with context,
- startup preflight checks for required config and services.

Avoid:

- empty `catch` blocks,
- `catch` blocks that return fake success,
- optional dependency imports that silently degrade required features,
- fallback data that makes tests pass while production behavior is broken.

## Compatibility

Backwards compatibility must be intentional.

Distinguish permanent supported contracts from temporary migrations. Keep compatibility required by a public API, protocol or supported product behaviour; it does not need a removal date or individually named consumers. Temporary compatibility should have an owner, a migration window and checks for both paths. Missing documentation is a reason to investigate and document the contract, not proof that deletion is safe. Remove aliases, legacy branches and adapters only after establishing that no supported caller or contract still needs them.

When compatibility must remain, make it visible:

```ts
// TODO(compat): remove after API clients stop sending `workspaceId` on 2026-07-01.
```

Lead the marker with `TODO`/`FIXME`/`HACK` so the scanner's `todo-compat` rule surfaces it - a bare `// Compatibility:` comment is intentionally not flagged (the keyword rule skips comment lines).

## Scanner

`scripts/scan-fallbacks.py` performs deterministic source scanning for common fallback smells:

- env var defaults (`os.getenv`/`os.environ.get`/`process.env.X ||`) and direct env reads,
- `||` / `??` fallback values,
- legacy, deprecated, backwards-compatible, and migration keywords,
- empty or swallowing `catch` blocks (JS/TS) and swallowing `except` blocks (Python),
- optional dependency fallbacks,
- aliases and dual config keys.

Detection caveats: the legacy/compatibility keyword rule fires only on code lines, not comment lines, so a bare `// Compatibility: ...` marker is intentionally not flagged. Temporary-compat comments are surfaced only when they lead with `TODO`/`FIXME`/`HACK`/`XXX` (the `todo-compat` rule) - see the Compatibility section's marker format. The keyword rule also skips declarative manifests (`package.json`, `tsconfig.json`) to avoid matching dependency names. `--fail-on` accepts only `medium` or `high` (there are no low-severity rules) - a previously accepted `--fail-on low` now exits with an argparse error, so update any scripts that passed it.

The scanner is not a substitute for judgment. Treat it as an index of places to inspect, then make the code simpler and more deterministic.

## Completion Check

Before finishing, verify that:

- each finding was classified (remove / require / validate / keep), not just listed.
- removed fallbacks have updated call sites and tests proving deterministic failure when the dependency, input, config, or env var is missing.
- kept fallbacks have a stated reason (product requirement, external contract, or dated migration with an owner).
- the scanner and the repo's relevant tests/typecheck/lint/build were re-run after edits.
- any remaining fallbacks are reported explicitly, not left invisible.
