---
name: marginalia
description: "Add short JSDoc where IDE hovers or generated API docs need a contract the types don't show. Use for JS/TS exports, components, hooks and packages about to publish. Not for deleting restating comments (`unslop`) or README prose."
---

# Marginalia

JSDoc that teaches what the signature can't, short enough to read in a hover. Public declarations are the source of truth for API reference (props, defaults, constraints, callback contracts, deprecations), so hovers, `.d.ts` output and generated docs agree. Guides, quick starts, migration notes and recipes belong in the README or docs site.

## Rules

- **Teach or skip.** Document hidden behaviour: side effects, thrown errors, async, caching, lifecycle and cleanup, ordering, idempotency, units, ranges, defaults the type doesn't show, SSR or client constraints, how type parameters relate. Leave obvious exports, locals and one-line wrappers alone.
- **Hover-sized.** One summary sentence; a second short paragraph only for behaviour or constraints. If the point isn't in the first two sentences, rewrite. Long concepts go to external docs.
- **Read before writing.** Read the implementation and at least one caller or test; never document from the name. A stale guess is worse than no comment.
- **Repair what's there.** Fix or replace existing JSDoc on symbols in scope when it is wrong or restates the name.
- **TypeScript: no types in tags.** Don't repeat declared types in `@param` or `@returns`. Use `@param` only when meaning, units, defaults or callbacks aren't obvious, `@returns` only when return semantics aren't, `@typeParam` for generics whose role isn't.
- **JavaScript: tag types are the types.** IDEs and `checkJs` read JSDoc type annotations; keep them and add missing ones.
- **Examples only to prevent likely misuse,** and consistent with real usage.
- **Don't change the API.** No runtime changes or renames unless asked. Don't add or remove `@internal`, `@public`, `@alpha`, `@beta` or `@deprecated` unless asked: with `stripInternal` or API Extractor they change emitted declarations and consumer diagnostics.
- **Use the repo's tag dialect.** Where TypeDoc, API Extractor or TSDoc conventions exist, use their tags (`@remarks`, `@defaultValue`, `@example`, `@see`, release tags) and nothing nonstandard. Don't add docs tooling unasked.

```ts
/**
 * Builds a stable cache key for a request.
 *
 * Includes the normalised URL and sorted query params, so equivalent
 * requests dedupe even when callers pass params in different orders.
 */
export function createRequestKey(input: RequestInput): string;

/** Gets the user. */ // Avoid: restates the name.
export function getUser(id: string): User;
```

## Where comments go

- **On the declaration consumers see.** For overloads, shared docs go on the first overload and distinct docs on each overload that behaves differently; implementation-signature JSDoc never reaches consumers.
- **Components and hooks:** purpose, controlled versus uncontrolled, accessibility expectations, SSR or client requirements, side effects. Document props on the exported props interface; skip self-explanatory visual props.
- **Types:** document fields consumers choose between, that carry defaults or runtime effect, or that define callbacks. Leave structural fields bare.
- **Easy to miss:** exported `as const` maps, token objects, schemas, discriminated unions and inferred public types are API too.

## Scope

- **Named file or symbol:** that, plus nearby types it depends on.
- **Nothing named:** the exports added or changed in the current diff.
- **A package, or "everything":** every symbol reachable from `package.json` `exports` and `types` entrypoints and their barrels. "Everything" means every meaningful export, not exhaustive comments.
- **Internal code:** only where a maintainer would otherwise misread it: state machines, overloads, lifecycles, tricky types.

## Check comments survive

When hovers or published docs are the goal, inspect the emitted `.d.ts` or generated docs. `removeComments`, `stripInternal`, declaration rollups, and re-exports through barrels or subpath exports can drop or detach comments. Run the repo's typecheck and existing docs or API-report script for touched packages.

Report the files changed and what was checked.
