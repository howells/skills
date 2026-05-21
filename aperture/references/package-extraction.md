# Package Extraction Reference

Use this reference when extracting local code into a reusable package, workspace package, or new repository.

## Extraction Questions

Answer these before editing:

- What is the reusable unit?
- Who is the consumer?
- Is the target a new repo, workspace package, or existing package?
- Should the original app keep using local code, switch to the package, or remain unchanged for now?
- Is the package intended for npm publishing, private workspace use, or copy-paste reuse?

## Source Inventory

Build a concrete inventory:

- implementation files
- type files
- styles and CSS entrypoints
- assets
- tests
- stories, examples, demos, or fixtures
- all import sites
- external dependencies
- app-only dependencies that need to be removed

Useful commands:

```bash
rg -n "ComponentName|useThing|from \".*thing" .
rg --files | rg "(component-name|thing|feature-name)"
```

## Public API

Prefer one stable import path:

```ts
import { Aperture } from "@scope/aperture";
```

Use subpath exports only when they represent deliberate surfaces:

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./styles.css": "./dist/styles.css"
  }
}
```

Avoid exporting internals such as `./src/*` unless the package is explicitly a low-level toolkit.

## Dependencies

Use `peerDependencies` when the consumer must provide a singleton or framework runtime:

- `react`
- `react-dom`
- `next`
- styling runtimes that must match the host
- design-system packages controlled by the consuming app

Use regular `dependencies` for libraries the package owns internally.

Use `devDependencies` for tests, build tools, Storybook, examples, and type packages.

## React And UI Packages

For React component packages:

- preserve `"use client"` only in files that need browser APIs, state, effects, event handlers, or client-only libraries
- keep server-compatible utilities free of client directives
- do not import app router APIs from reusable components
- avoid `next/image`, `next/link`, or framework-specific components unless the package is explicitly Next-only
- define the styling contract: bundled CSS, Tailwind classes, CSS variables, style props, or unstyled primitives

For Tailwind packages:

- document whether consumers must include source paths in Tailwind v4 `@source`
- avoid safelists
- expose CSS variables or a CSS entrypoint when classes alone are not enough

## New Repo Shape

For a small publishable TypeScript package, prefer:

```text
package-name/
├── package.json
├── tsconfig.json
├── src/
│   └── index.ts
├── tests/
└── examples/
```

Only add Turborepo, Storybook, Changesets, or a docs app when the package clearly needs them.

## Validation Checklist

- `package.json` name, version, type, files, exports, scripts
- type declarations generated or referenced
- build output excludes tests and examples
- peer dependencies are not bundled accidentally
- package can be imported from the intended consumer
- publishable packages have been packed and smoke-tested when practical, for example with `npm pack --dry-run` plus a consumer import/build check
- app-specific imports removed
- tests or examples cover the extracted behavior
- consuming app still typechecks when imports are migrated

## Common Failure Modes

- Copying a component but forgetting its CSS variables or global styles.
- Publishing a package whose `exports` map points to files that are not emitted.
- Bundling React instead of peering it.
- Keeping imports from the original app, such as `@/lib/*`.
- Extracting too much and accidentally creating a second application.
- Leaving two editable canonical implementations after an in-repo extraction.
