---
name: marginalia
description: Add useful, concise JSDoc to JavaScript and TypeScript code, especially public package APIs, exported functions, classes, React components, hooks, complex types, and behavior where IDE hover help matters. Use when asked to add or improve JSDoc/code comments for public APIs, exported symbols, generated API docs, IDE hover help, or package publishing documentation without changing behavior.
---

# Marginalia

Use this skill to add high-signal JSDoc that helps readers, IDEs, declaration files, and generated API docs. The goal is not comments everywhere; the goal is concise documentation at the right boundaries. Overly long JSDoc makes IDE hovers harder to use, so prefer the shortest comment that explains the missing context.

For TypeScript package APIs, treat JSDoc as the source of truth for API reference material, not as a replacement for authored docs. Props, exported types, defaults, constraints, callback contracts, and deprecations belong close to the public declarations so IDE hovers, `.d.ts` output, and generated docs agree. Usage guides, examples, conceptual explanations, migration notes, and recipes usually belong in README or site documentation.

## Start

When invoked:

1. State that you are using the `marginalia` skill.
2. Determine the documentation target:
   - public package API
   - all exports in a package or module
   - complex internal code only
   - React components, hooks, utilities, classes, or types
   - generated docs or IDE hover quality
3. If the user does not name a file, symbol, package, or scope, ask one concise clarification question before editing. Infer a public API pass only when the request clearly mentions package docs, publishing documentation, generated API docs, or IDE hover quality for a package.
4. Read the right amount before editing:
   - targeted pass: requested file/symbol, nearby types, and one relevant usage or test when available
   - public API pass: `package.json` exports/types, public entrypoints, barrels, `tsconfig*`, docs tooling, README/examples, and representative call sites
   - complex internal pass: implementation, tests, and callers that reveal behavior

Do not infer behavior from names alone. Read the implementation and at least one usage path when available.

## Documentation Density

Choose the smallest density that satisfies the request.

- **Public API pass:** Consider every exported symbol reachable from package entrypoints. Add JSDoc only where it teaches behavior, constraints, usage, or API intent; record obvious exports as `leave`.
- **Meaningful pass:** Document exported symbols plus complex internal functions, tricky types, overloads, state machines, lifecycle behavior, side effects, and non-obvious constraints.
- **Targeted pass:** Document only the named file, component, or symbol.

Meaningful and targeted passes reuse steps 2-4 of the Package API Workflow (decide, write, validate) without the full surface inventory from step 1.

Avoid blanket comments on obvious local variables, simple one-line wrappers, and code whose type signature already explains everything.

## What To Document

Prioritize:

- exported functions, classes, constants with non-obvious semantics, React components, hooks, and types
- overloads, generics, conditional types, mapped types, branded types, and callback contracts
- options objects and config fields when IDE completion should guide consumers
- side effects, thrown errors, async behavior, caching, lifecycle, cleanup, ordering, and idempotency
- units, ranges, defaults, stability guarantees, runtime environment, and SSR/client constraints
- deprecations, experimental APIs, and internal-only exports when the repo uses those conventions

For published packages, focus on symbols included in `exports` and generated `.d.ts` files. Internal helpers only need JSDoc when they are complex enough that maintainers benefit.

For generated API docs, make defaults and behavioral constraints explicit in comments when they are not visible from the type alone. Prefer standard TSDoc-compatible tags such as `@remarks`, `@defaultValue`, `@example`, `@deprecated`, `@see`, and release tags when the repo's tooling recognizes them.

## Comment Rules

Write comments that add information the type system cannot express. Keep them short enough to be useful in an IDE hover.

Brevity rules:

- Prefer one sentence for simple public APIs.
- Use one short summary plus one short paragraph for behavior or constraints.
- Use examples sparingly; include them only when they prevent likely misuse.
- Split long conceptual material into external docs instead of putting it in JSDoc.
- If a hover would feel like an article, cut it down.

Good JSDoc:

```ts
/**
 * Builds a stable cache key for a request.
 *
 * The key includes the normalized URL and sorted query params so equivalent
 * requests dedupe even when callers pass params in different orders.
 */
export function createRequestKey(input: RequestInput): string {
  // ...
}
```

Avoid:

```ts
/** Gets the user. */
export function getUser(id: string): User;
```

Rules:

- Start with a concise summary sentence.
- Add a second paragraph only for behavior, constraints, or examples that matter.
- Prefer prose over noisy `@param` tags when TypeScript names and types are clear.
- Use `@param` for public APIs when parameter meaning is not fully obvious from the name, or when a function has multiple positional parameters, callbacks, options, units, defaults, side effects, or overloaded semantics.
- Use `@returns` only when return semantics are not obvious from the type.
- Use `@typeParam` for exported generics when the role, constraints, inference behavior, defaults, or relationship between type parameters is not obvious.
- Use `@throws`, `@deprecated`, `@example`, `@remarks`, `@defaultValue`, `@see`, `@internal`, `@public`, `@alpha`, or `@beta` when the repo's tooling or docs use them.
- Do not duplicate TypeScript types in prose, including type annotations inside `@param` or `@returns` tags.
- Do not add comments that simply restate the function name.
- Do not change runtime behavior while documenting.

When TypeDoc, API Extractor, or TSDoc conventions are present, follow the repo's established tag style, preserve release tags, avoid nonstandard tags unless configured, and run the existing docs or API report check when practical.

## Generated API Reference

When the documentation target is generated API docs or single-source package documentation:

- Treat public source declarations as the canonical input for API reference.
- Inspect existing docs tooling first, such as TypeDoc, API Extractor, React docgen, declaration rollups, or custom site generators.
- Prefer structured tooling over parsing comments with ad hoc string matching.
- Keep generated API tables/reference data separate from authored examples, guides, and conceptual copy.
- Verify comments survive the package's declaration or docs pipeline before calling the pass complete.
- If no docs tooling exists, recommend a generated-docs plan but do not add new tooling unless the user asked for implementation.

Common split:

- **JSDoc/TSDoc:** API tables, prop descriptions, exported type docs, callback contracts, defaults, constraints, IDE hover text.
- **Authored docs:** installation, quick starts, composition examples, design rationale, migration guidance, recipes, and screenshots.

## Package API Workflow

### 1. Build The Public Surface

List symbols exposed through:

- `package.json` `exports`
- `types`, `typings`, or declaration entrypoints
- root barrel files
- intentional subpath exports

Useful searches:

```sh
rg '^\s*export\b' -g '*.{ts,tsx,js,jsx,mts,cts,d.ts}'
rg '"(exports|types|typings|main|module|browser)"' -g 'package.json'
rg '^\s*(module\.exports|exports\.)' -g '*.{js,cjs,cts}'
rg '@public|@internal|@deprecated|@alpha|@beta|@remarks|@example' -g '*.{ts,tsx,js,jsx}'
```

For each public symbol, record whether it already has useful JSDoc and whether the declaration output would preserve it.

Use a lightweight inventory before package-wide edits:

```markdown
| Symbol | Source file | Export path | Existing JSDoc | Decision | Reason |
| --- | --- | --- | --- | --- | --- |
```

### 2. Decide What Needs JSDoc

Classify each candidate:

- add: missing useful public API documentation
- improve: existing comment is stale, vague, or type-duplicative
- leave: signature and naming are already sufficient
- skip: private/simple helper with no meaningful hidden behavior

If the user asked for "everything", interpret that as every meaningful exported/public symbol unless they explicitly ask for exhaustive comments.

### 3. Write The Comments

Keep comments close to the exported declaration that consumers see. For overloads, place shared docs on the first overload or exported declaration, place distinct docs on each overload whose behavior differs, and do not rely on implementation-signature JSDoc for consumer docs.

For React components and hooks:

- document the component/hook purpose and key behavior
- document important props through exported prop interfaces when present
- mention controlled/uncontrolled behavior, accessibility expectations, SSR/client requirements, and side effects
- avoid documenting every visual prop when the prop name and type are enough

For types and interfaces:

- document the interface purpose
- document fields when users choose between them, when defaults matter, when they affect runtime behavior, or when they define callback contracts
- leave obvious structural fields undocumented
- prefer examples for complex config objects

Also inspect exported const assertions, token maps, schemas, namespace-like objects, discriminated unions, and inferred public types when they are part of the package API.

### 4. Validate

Choose commands from `package.json` scripts, workspace package scripts, or existing CI/docs config. Do not invent new tooling just to validate comments.

Run the narrowest meaningful checks:

- typecheck for touched packages
- lint/format if comments are linted
- package build when declaration output matters
- API docs generation if the repo uses TypeDoc, API Extractor, or similar
- inspect generated `.d.ts` or docs output when publishing/IDE hover quality is the goal

For declaration preservation, check relevant compiler/doc settings such as `removeComments`, declaration emit, generated `.d.ts` entrypoints, re-exported symbols, `stripInternal`, API Extractor rollups, and whether docs remain attached after barrel or subpath export generation.

Report the exact commands run. If checks are unavailable or too broad, report exactly what was and was not verified.

## Output

When planning, provide:

- public surface inspected
- symbols to add, improve, leave, and skip
- validation plan

For package-wide or multi-module passes, present the candidate surface and intended documentation density before editing unless the user already requested implementation.

When implementing, finish with:

- files changed
- kinds of APIs documented
- public symbols considered, JSDoc added, JSDoc improved, and symbols left undocumented with reasons
- validation results

## Guardrails

- Do not create documentation theater. A comment must teach something.
- Do not add stale guesses. If behavior is unclear, read usage or tests before documenting.
- Do not write long comments that bury the useful detail. If the important point is not visible in the first sentence or two, rewrite.
- Do not document private helpers exhaustively unless complexity justifies it.
- Do not use JSDoc to hide poor names. Rename only when the user asked for refactoring or the rename is necessary and safe.
- Do not add examples that are not typechecked or at least consistent with real usage.
- Do not introduce generated docs tooling unless the user asks or the repo already uses it.
- Do not alter public API while adding JSDoc unless explicitly requested.

## Completion Check

Before finishing, verify:

- public exported symbols requested by the user were considered
- comments explain behavior, constraints, examples, or IDE-helpful usage
- comments are concise enough to improve hover clarity
- no comments merely restate obvious names or TypeScript types
- generated declarations/docs preserve comments when that matters
- validation ran or the gap is reported
