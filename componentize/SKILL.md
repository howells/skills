---
name: componentize
description: "Consolidate duplicated UI into shared components, split god files or extract packages. Not for redesign (`chiaroscuro`), typography (`typecase`) or behaviour-preserving cleanup (`unslop`)."
---

# Componentize

Find what already exists, make it the one canonical version, and move every caller onto it. Don't centralise the whole UI unless asked for a design-system project.

## Rules

1. **Fix it in the shared package.** When the repo has a shared UI package, use it and fix defects at the root there rather than patching around them in the app. When several exist, use the one the user names, and don't reintroduce the one they've moved away from.
2. **Adapt before adding.** In order: reuse a component unchanged; replace duplicate markup with the component that already owns the pattern; add a prop, variant or slot to it; extract a primitive from two or more local copies; create a new shared component; create a new package only when reuse crosses app boundaries and the API is domain-free.
3. **One canonical version.** Migrate every in-scope caller in the same change and delete the superseded copy. No re-export shims or aliases for old paths. A staged migration only when asked.
4. **Every prop maps to an observed call-site difference.** No speculative options. Parallel components that differ only by copy, spacing, icon or colour become one API; if variants conflict conceptually, split or extract a smaller primitive instead of hiding five designs behind one.
5. **Domain stays in the app.** Data fetching, auth, analytics, flags, routes, permissions and business copy don't move into shared UI. Extract the presentational part.
6. **Not a redesign.** Preserve appearance and behaviour unless the user asked for visual change.

When the user points at something on screen ("the right panel", "that header"), open the running app if available, map the region to its source file through text, labels and test ids, and ask one question if several regions match. Don't guess from layout direction.

For a family of visual primitives (fills, markers, ticks, badges), Daniel likes an at-a-glance inventory page of the canonical set with its size variants, so drift is visible.

## Conventions

Extend the repo's existing system; never mix a second one in for one extraction.

- shadcn-style: `cva` + `VariantProps`, `cn`/`twMerge` for `className`, Radix `Slot`/`asChild` for polymorphic leaves.
- Base UI (`@base-ui-components/react`): `render` prop, and `useRender` + `mergeProps` for custom polymorphic primitives. No `asChild` clone.
- MUI Base: `slots`/`slotProps`.
- `tailwind-variants`, CSS modules, Vanilla Extract, Panda: extend that.
- Nothing established: `cva` only when several call sites show real variants; otherwise plain `cn(...)`.

Shared components accept `className`, leave outer margins to callers, forward refs and spread DOM props on interactive leaves, merge handlers, refs, styles and ARIA with the repo's helper, and keep their accessibility contract. Polymorphism only where props, refs and semantics can pass validly to the child; never as an escape hatch for unclear ownership.

**Server Components** (Next.js App Router): keep shared primitives environment-agnostic and free of `'use client'` unless they use client APIs. Wrap the interactive bit in the smallest client component and pass server UI through as `children`. Don't make a route, table or shell client-side for one stateful control, and don't move a component across the boundary before checking its imports and props are valid there. Serializable props only (Server Functions allowed).

## Where it lives

- Shared UI package exists and fits: put it there. Turborepo with none: `packages/ui`.
- Reuse within one app, or the API is still product-specific: an app-local shared folder.
- Consumers import through the package's public exports (deliberate subpaths like `@repo/ui/button` are fine, private source paths are not). Add the dependency where imports cross packages; don't weaken boundaries to make imports pass.
- Changing a package: check `exports` for JS and types, CSS exports and `sideEffects`, whether consumers transpile source, peer deps (React, framework, Radix, icons), and Tailwind v4 `@source` so the app scans the package's classes. A missing `@source` silently drops the package's styles.

## Splitting a god file

Length alone is never the reason. Split when a file mixes responsibilities, duplicates logic, changes for unrelated reasons or has a public interface that could be smaller. Rank candidates with the scanner, then read them:

```bash
python3 scripts/find-god-files.py /path/to/repo                  # flags score ≥ 35; ≥300 lines can list on length alone
python3 scripts/find-god-files.py /repo --min-score 20 --duplicate-window 10
python3 scripts/find-god-files.py /repo --include-tests --json
```

Split in this order, one candidate at a time, running the smallest relevant check after each: pure helpers; duplicated logic, before moving callers; hooks and state machines where state is tangled; leaf subcomponents before shells; I/O adapters away from domain logic in scripts.

- Components: name extracted pieces for their domain, never `Content` or `Wrapper`. Keep state with the component that owns the interaction. Avoid many shallow files that must all be opened to understand one behaviour.
- Scripts: thin entrypoint; parsing, config, transformation, I/O and formatting apart; preserve exit codes and stream behaviour.
- Duplication: merge only copies meant to stay the same. Similar code with different domain meaning stays apart.

## Extracting a package

Define the boundary first. In: the code, its types, styles, assets, fixtures, tests and examples. Out: routes, auth, database clients, env access, product copy, analytics, flags and old-path shims. Report hidden coupling before editing. Design a narrow public API before creating files. Read [references/package-extraction.md](references/package-extraction.md) when setting up `exports`, dependencies or a new repo.

- Within one repo: migrate the callers and delete the old implementation.
- To a separate repo: copy, and leave the source app untouched unless removal was asked for.
- Never publish, tag, push a release, or change licence, visibility, registry scope or ownership without explicit approval.

## Migrating a collection

For many charts, cards or examples moving onto one kit, read [references/collection-migration.md](references/collection-migration.md) before the first family: it covers stable baselines, family-by-family extraction and what each kind of evidence proves.

## Checking

Typecheck, lint and build what you touched and every consumer of a changed export. When shared UI moved, open the affected pages (or Storybook) and compare against before; exercise keyboard and focus on interactive primitives. Say what you didn't check.

Load `chiaroscuro` only for visual direction, `typecase` when the duplication is typographic. Scope stays here.

## Audit output

When asked for analysis rather than changes:

```markdown
## Reuse audit

### Existing shared surface
- `path`: purpose, health, import pattern

### Opportunities
| Priority | Pattern | Evidence (file:line, call-site count, current home) | Action (reuse / adapt / extract / move / none) | Why |
|---|---|---|---|---|

### Proposed API
- `ComponentName`: props, variants, slots, import path, server/client

### Home and package plan
- Existing package / `packages/ui` / app-local; exports and dependency changes

### Risks
- Coupling, accessibility, styling or boundary concerns
```
