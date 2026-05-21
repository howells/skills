---
name: fenceline
description: Add, check, explain, or repair JavaScript and TypeScript package and source architecture boundaries with the `boundaries` CLI from `@howells/boundaries`. Use when enforcing Turborepo package boundaries, preventing app-to-app imports, tagging workspace packages, running source-layer profiles such as feature-sliced, next-feature, or clean-node, or fixing boundary violations without weakening architecture rules.
---

# Fenceline

Use `@howells/boundaries` for architecture boundary enforcement in JavaScript and TypeScript codebases. The executable is `boundaries`.

This collection copy is canonical. If `@howells/boundaries` ships a bundled skill, sync its guidance from this skill rather than maintaining divergent instructions.

## Workflow

1. Confirm whether the repo is a Turborepo workspace by checking for `turbo.json` and workspace packages in `package.json`, `pnpm-workspace.yaml`, or equivalent package-manager config.
2. Install or use `@howells/boundaries` from the repo's chosen package manager.
3. For Turborepo package boundaries, run `boundaries init --dry-run --json` first.
4. Review the generated root rules, package tags, and script changes. Fix incorrect tags before applying the generated config.
5. Run `boundaries init` only after the dry run looks correct.
6. Run `boundaries check`.
7. If a violation appears, prefer fixing the import or dependency declaration. Use exceptions only when they are narrow, temporary, and documented.

To explain a package relationship, run:

```sh
boundaries explain <from-package-or-path> <to-package-or-path>
```

Use explain output before proposing policy changes. A failed relationship often means code belongs in a shared package, not that the boundary rule is wrong.

For non-Turbo source-layout checks, run a JavaScript profile directly:

```sh
boundaries check --profile feature-sliced
boundaries check --profile next-feature
boundaries check --profile clean-node
```

## Default Model

Use these package tags unless the repo already has a clearer convention:

```text
type:app
type:package
type:tooling
scope:<name>
visibility:public
visibility:internal
```

Default rules:

```text
type:app      cannot depend on type:app
type:package  cannot depend on type:app
type:tooling  cannot depend on type:app
```

This blocks app-to-app imports and keeps shared packages from reaching into deployable apps. Treat `visibility:*` as metadata until the checker can distinguish runtime dependencies from dev-only tooling dependencies.

## JavaScript Profiles

Use `--profile` when the repo is not primarily relying on Turbo package boundaries:

```text
feature-sliced: app -> pages -> widgets -> features -> entities -> shared
next-feature:   app/pages -> components -> features -> entities -> lib/shared
clean-node:     adapters/infrastructure -> application -> domain
```

Higher layers may import lower layers. Lower layers should not import higher layers.

## Good Fixes

- Move shared code from an app into a package, then import the package.
- Add a missing internal package dependency to the importing package's `package.json`.
- Use the package public entrypoint instead of importing files across package directories.
- Split package tags by purpose when a package has unclear ownership.

## Avoid

- Do not use ESLint as the primary enforcement mechanism.
- Do not add broad allowlists to make a check pass.
- Do not move task logic into root `package.json`; keep Turbo package tasks in packages and root scripts as delegators.
- Do not invent bespoke package-internal layer rules when a named profile fits. Pick a profile first, then add narrow project-specific exceptions later.

## Fallbacks

Use `turbo boundaries` as the backend when available. Consider `dependency-cruiser` or `rev-dep` only when the user asks for graph analysis that Turbo boundaries cannot answer.
