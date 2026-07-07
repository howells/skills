---
name: fail-fast
description: Audit and remove unnecessary fallbacks, silent compatibility paths, legacy aliases, default environment values, swallowed errors, and backwards-compatible states that make code harder to reason about. Use when a user asks to fail fast, remove legacy behavior, eliminate hidden fallbacks, make configuration deterministic, harden env handling with Envy, or replace permissive behavior with explicit validation and clear errors.
---

# Fail Fast

Use this skill to make a codebase deterministic by finding and removing hidden fallback behavior that should be an explicit contract, validation error, migration, or test fixture.

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
   - `require`: missing config, absent dependencies, invalid user input, or an env var that belongs in the Envy schema.
   - `validate`: boundary input that must accept unknown data but should reject invalid states clearly.
   - `keep`: documented product behavior, real external API compatibility, or temporary migration with owner and removal date.
5. Edit narrowly. Remove the fallback state and update call sites/tests to use the canonical path.
6. Add or update tests that prove the code fails deterministically when the dependency, input, config, or Envy-declared env var is missing.
7. Run the scanner again, plus the repo's relevant tests, typecheck, lint, or build.
8. Report remaining fallbacks explicitly. Do not leave them invisible.

## Environment Variables

Environment variables are configuration contracts, not suggestion fields.

In TypeScript projects that use `@howells/envy`, missing required env vars are already enforced by the schema. Do not add app-level "maybe missing" branches, default values, or defensive fallbacks for those keys. Application code should import typed env values from the env module instead of reading `process.env` directly. If a required key is not in the schema, add it to the Envy schema rather than adding a runtime fallback.

Use Envy checks when available:

```bash
npx --no-install envy check local --schema ./src/env/schema.ts --from .env.production
npx --no-install envy check local --schema ./src/env/schema.ts --mode all --json
npx --no-install envy check turbo --schema ./src/env/schema.ts --task build
```

(`--no-install` ensures npx runs the project's `@howells/envy` binary rather than downloading an unrelated `envy` package if it is not a dependency.)

Accept direct `process.env` reads only in env schema modules, generated env wiring, narrow system keys such as `NODE_ENV` and `CI`, or explicitly documented migration escape hatches.

Remove patterns like:

```ts
const apiKey = process.env.OPENAI_API_KEY || "dev-key";
const databaseUrl = process.env.DATABASE_URL ?? "postgres://localhost";
```

Replace with typed Envy access:

```ts
const apiKey = env.OPENAI_API_KEY;
```

Use explicit validation only in codebases that do not use Envy and where adding Envy is outside the task scope.

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

Keep compatibility only when there is a named external caller, versioned API contract, migration deadline, owner, and tests proving both the old and new behavior. Otherwise delete aliases, legacy branches, dual option names, deprecated flags, and old data-shape adapters.

When compatibility must remain, make it visible:

```ts
// TODO(compat): remove after API clients stop sending `workspaceId` on 2026-07-01.
```

Lead the marker with `TODO`/`FIXME`/`HACK` so the scanner's `todo-compat` rule surfaces it — a bare `// Compatibility:` comment is intentionally not flagged (the keyword rule skips comment lines).

## Scanner

`scripts/scan-fallbacks.py` performs deterministic source scanning for common fallback smells:

- env var defaults (`os.getenv`/`os.environ.get`/`process.env.X ||`) and direct env reads,
- `||` / `??` fallback values,
- legacy, deprecated, backwards-compatible, and migration keywords,
- empty or swallowing `catch` blocks (JS/TS) and swallowing `except` blocks (Python),
- optional dependency fallbacks,
- aliases and dual config keys.

Detection caveats: the legacy/compatibility keyword rule fires only on code lines, not comment lines, so a bare `// Compatibility: ...` marker is intentionally not flagged. Temporary-compat comments are surfaced only when they lead with `TODO`/`FIXME`/`HACK`/`XXX` (the `todo-compat` rule) — see the Compatibility section's marker format. The keyword rule also skips declarative manifests (`package.json`, `tsconfig.json`) to avoid matching dependency names. `--fail-on` accepts only `medium` or `high` (there are no low-severity rules).

The scanner is not a substitute for judgment. Treat it as an index of places to inspect, then make the code simpler and more deterministic.
