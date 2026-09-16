---
name: howells-lint
description: "Put a repo on @howells/lint so the preset actually loads, and add a ratchet when a backlog appears. Use for lint setup or a config named .mjs/.json. Not for prose (`deslop`), diff tells (`unslop`) or codebase review (`simplify`)."
---

# Howells lint

Put a repo on `@howells/lint` so the preset actually loads, and keep it that way. The package is the policy; this skill is the setup and the checks the package cannot make for you.

State at the start that you are using the `howells-lint` skill.

## The trap this exists for

Oxlint discovers only `oxlint.config.ts` and `oxlint.config.mts`. A config named `oxlint.config.mjs`, `.js`, `.cjs` or `oxlint.config.json` is never read, the run is quiet, and it exits 0. MaterialGraph linted on Oxlint's defaults for months with 27 such files; five sibling repos had the same. A repo that depends on `@howells/lint` with no config at all is in the same state and looks identical from outside.

`@howells/lint` 3.3.x passes an ignored spelling with `--config` and prints a warning, which loads the preset but pins one config for the whole run and defeats nested per-package discovery. The rename is still the fix.

## Setup, in order

Before renaming or deleting any lint or format config, search the repo for its filename. Package scripts, `knip.json` and custom runners name config files by path and break silently on a rename. A `biome.json` or `.oxlintrc.<name>.json` may also be a published package export or a file a script reads as data, and must stay.

1. Node 24.15.0 or later, pinned in `.node-version`; pnpm named in `packageManager`.
2. `@howells/lint` is the only direct lint dependency, at the latest published version. Never add `oxlint`, `oxfmt`, `ultracite`, `oxlint-tsgolint` or `oxlint-plugin-react-doctor` directly. Never alias an old version under another name (`"@x/lint-policy": "npm:@howells/lint@0.5.0"`); that is a rule disposal by another route.
3. One `oxlint.config.ts` per package that lints, extending the closest preset:
   - `@howells/lint/oxlint/core` for Node or non-React TypeScript
   - `@howells/lint/oxlint/react` when `react` is a dependency
   - `@howells/lint/oxlint/next` when `next` is a dependency
   - `@howells/lint/oxlint/playwright` as an overlay for E2E specs
   In a monorepo the root gets `core` for its scripts and each app or package gets its own. A root `next` config with `disabledReactDoctorRules` for `packages/**` is the alternative when packages have no config of their own.
4. `oxfmt.config.ts` that re-exports or spreads `@howells/lint/oxfmt`. Oxfmt has no `extends` key; an object it does not recognise formats to its defaults in silence.
5. Scripts: `"lint": "howells-check ."` and `"lint:fix": "howells-fix ."`. No `--config` in a monorepo package script: it defeats nested discovery.
6. Verify by running `pnpm lint` and reading the rule names in the output. A run that shows only `typescript(...)` and `eslint(...)` and never `anti-slop(...)` or `unicorn(...)` has not loaded the preset.

Minimal config:

```ts
import next from "@howells/lint/oxlint/next";

export default {
  extends: [next],
};
```

## What a consumer may not do

- Switch rules off at config level to shrink a backlog. The preset ships as ultracite ships it; a rule that is wrong for every repo is changed in `@howells/lint` itself, once, so all repos agree. `func-style` is `expression`: arrow functions, so the fix for a declaration backlog is a codemod to arrows, never the reverse.
- Keep a `compat` or `policy` shim that "preserves the previous rule set". That is the same disposal with a longer comment.
- Add a rule entry for a plugin not in scope. `"vitest/foo": "off"` outside an override that names `plugins: ["vitest"]` is discarded without a message.
- Run `howells-oxfmt --write .` from a monorepo root. It formats every file under the root config and ignores the package configs.

## A backlog that appears on first load

Expect tens of thousands of findings in a repo that has never had the preset. Do not fix in place before the gate is green.

1. Add a ratchet: a script that runs `oxlint --format json` per package, counts findings per package per rule, compares to a committed baseline, and fails only when a count rises. Commit the baseline at today's numbers. Pre-push is green from here and the backlog can only fall.
2. Fix by rule, with a codemod (ts-morph) per rule, one commit and one typecheck-plus-test run per rule, rebaselining after each. Order by count. Rules whose autofix changes behaviour and must be checked against the test suite: `sort-keys`, `unicorn/no-useless-undefined`, `typescript/consistent-type-definitions`, `unicorn/catch-error-name`, `typescript/no-unnecessary-type-assertion`, `typescript/promise-function-async`, `new-cap`, `vitest/prefer-strict-equal`, `vitest/prefer-called-with`, `vitest/prefer-describe-function-title`, `vitest/prefer-import-in-mock`.
3. Rules that need a human sentence per site stay in the baseline and burn down as files are touched: `anti-slop/require-safety-comment-for-type-assertion`, `typescript/strict-boolean-expressions`.

## Scripts

- `scripts/sweep.mjs` walks every package under a directory (default `~/Sites`) and reports configs that never load, packages that depend on `@howells/lint` with no config, missing preset imports, and `--config` in lint scripts. Read-only. Run it before trusting any repo's lint status.
- `scripts/fix.mjs <repo>` applies the setup to one repo: bumps the dependency, replaces policy aliases, renames or creates configs by dependency, pins `.node-version`. It runs no install and no git. Review its output, run `pnpm install`, verify with `pnpm lint`, commit explicit paths.

Both are plain Node with no dependencies.
