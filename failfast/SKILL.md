---
name: failfast
description: "Remove fallbacks and swallowed errors that hide failures, and test-only code or mocks in production. Use when a failure is hidden, tests assert on mocks or a test needs production hooks. Not for test-first work (`tdd`), behaviour-preserving cleanup (`unslop`) or required compatibility."
---

# Failfast

A hidden fallback turns a bug into wrong output nobody sees. Leave one canonical path and one explicit failure.

## Rules

1. **No fallback without a real reason:** a product requirement or a supported external contract (permanent; no removal date). Old stored data is migrated once and the old path deleted in the same change. Everything else becomes a required input, a validation error or a deleted path. Missing docs don't make deletion safe; check for a supported caller first.
2. **Fail at the boundary, specifically.** Validate external input with a schema, check required config at startup, throw on impossible internal states.
3. **Never swallow.** No empty `catch`, no `catch` that returns fake success, no optional import that quietly degrades a required feature. Rethrow with context or handle a named, expected error.
4. **Production code doesn't know about tests.** No `isTest` or `NODE_ENV === "test"` branches, test-only methods or exports, or stub data on a production path. Test observable behaviour through the public interface. When isolation needs a double, inject it through an argument production would also use; builders, cleanup and doubles live in test utilities.
5. **Don't test the mock.** An assertion that passes because a mock exists proves nothing.
6. **Update every caller.** Removing a path moves its callers and tests in the same change. No alias or shim.

## Workflow

1. Scope: the path the user names, else the directories the diff touches; the whole repo only when asked. Scan it:

   ```bash
   python3 <this skill's directory>/scripts/scan-fallbacks.py <path>
   ```

   It prints high-severity leads, not verdicts; add `--min-severity medium` only for files you are already editing. It does not find test-only code or mocks: read `references/tests.md` before editing those.
2. Decide each lead: **remove** (no live caller or contract), **require** (config or a dependency the code can't work without), **validate** (boundary input) or **keep** (say why). `legacy`, `deprecated`, `compat` and `migration` are leads, not proof: confirm no supported caller needs the path. Tests that pass only because a default masks missing setup get explicit fixtures.
3. Remove the fallback and move callers and tests to the canonical path. Where a fallback becomes an error, test that the error fires.
4. Run the repo's checks. Report the fallbacks you kept and why.

## Environment variables

Env vars are a configuration contract. Where a validated env schema exists, declare the key there and import the typed value; no application default:

```ts
const apiKey = process.env.OPENAI_API_KEY || "dev-key"; // remove
const apiKey = env.OPENAI_API_KEY;                       // use
```

With no schema, validate at the configuration boundary using the project's conventions; don't add a package for it. Direct `process.env` reads belong only in env schema modules, generated env wiring and system keys such as `NODE_ENV` and `CI`. Never log the raw environment.
