---
name: aperture
description: Extract a component, hook, utility, feature, or subsystem from an existing codebase into a reusable package, workspace package, or new publishable repository. Use when asked to make code reusable, move code into its own repo, create an npm package, extract a shared package, package a component library, define package exports, preserve examples/tests, or replace app-local imports with a canonical package boundary. For a tangled god file that needs decomposition first, use heathen.
---

# Aperture

Use this skill to extract useful local code into a clean reusable package. The goal is not just moving files; the goal is a stable public surface, minimal dependencies, working examples, and a package that can be reused without dragging the original app with it.

## References

Load `references/package-extraction.md` when planning or executing an extraction.

## Start

When invoked:

1. State that you are using the `aperture` skill.
2. Determine the requested target:
   - new repo (ask where the user keeps projects, or use the parent directory of the current repo)
   - new workspace package inside the current monorepo
   - existing package or library
   - publishable npm package
3. If the target, package name, consumer, publishing intent, or migration scope is not specified and the choice materially affects the work, ask concise questions until those decisions are clear.
4. Read before moving anything:
   - the source files being extracted
   - all import sites and usage examples
   - package manager and workspace config
   - build, test, lint, and typecheck scripts
   - existing package conventions, export maps, tsconfig, CSS strategy, and examples

Do not infer the public API from filenames alone. Read actual usage.

## Extraction Workflow

### 1. Define The Boundary

Identify what belongs in the package and what must stay in the host app.

Include:

- reusable component, hook, utility, types, styles, assets, fixtures, and tests
- small support modules that are intrinsic to the extracted behavior
- examples that demonstrate the intended package API

Exclude:

- app routes, auth/session code, database clients, environment access, project-specific copy, analytics, feature flags, and unrelated design-system wrappers
- compatibility shims for old import paths unless the user explicitly asks for a migration period

If the extraction exposes hidden coupling, report it before editing and choose the smallest coherent boundary.

### 2. Design The Public Surface

Define the package API before creating files:

- package name
- entrypoints
- exported components/functions/types
- peer dependencies versus bundled dependencies
- styling contract
- asset handling
- server/client/runtime constraints

Prefer a narrow API. Do not export every internal file because it happens to exist.

### 3. Create Or Adapt The Target

Use the target's existing conventions when present. For a new TypeScript package, include only the files needed for a working package:

- `package.json`
- `src/`
- `tsconfig.json`
- build config only if the repo does not already provide one
- tests or examples appropriate to the package

For publishable npm packages:

- use an explicit `exports` map
- emit or reference types
- set `files`
- mark React, Next, framework, and styling libraries as peers when consumers must provide them
- avoid app-only environment assumptions

### 4. Move Code Carefully

Copy or move the extracted code according to the user request.

When creating a new repo from an existing app, copy first and leave the original source intact unless the user explicitly asks to remove or rewrite it. When extracting inside the same repo, update usage sites only when the requested migration scope says the original app should switch to the package now.

Rewrite imports to the new package boundary. Preserve user edits and avoid unrelated cleanup.

### 5. Validate

Run the smallest meaningful checks:

- build and typecheck the package, plus relevant tests
- check any consumer whose imports changed
- for publishable packages, smoke-test the packed artifact when practical

See the full **Validation Checklist** in `references/package-extraction.md` for the complete list. If a full validation command is too broad or expensive, run package-scoped checks and say what was not run.

## Output

When planning, provide:

- source inventory
- proposed package boundary
- public API
- dependency plan
- file move plan
- validation plan

When implementing, finish with:

- created or changed package path
- public exports
- consumer import changes
- validation results
- any follow-up decisions such as package name, registry, or release process

## Guardrails

- Do not turn extraction into a broad refactor.
- Do not create a package that depends on the original app to function.
- Do not silently change licensing, publishing visibility, registry scope, or package ownership.
- Do not delete original code when extracting to a separate repo unless explicitly requested.
- Do not leave duplicate canonical implementations inside one repo unless the user wants a staged migration.
- Do not auto-publish, tag, push, or create a release without explicit approval.

## Completion Check

Before finishing, verify that:

- the package has a clear purpose and public API
- dependency boundaries are explicit
- package exports and types work
- examples or tests prove the extracted behavior
- the original app either still works or has been intentionally migrated
