# Package extraction

## React and Tailwind packages

- No app router APIs, and no `next/image` or `next/link` unless the package is explicitly Next-only.
- State the styling contract: bundled CSS, Tailwind classes, CSS variables, style props or unstyled.
- Ship CSS variables or a CSS entrypoint when classes alone aren't enough. No safelists.

## Before calling it done

- `package.json` has name, version, type, `files`, `exports`, scripts; types are emitted or referenced.
- Build output excludes tests and examples; peers aren't bundled.
- `npm pack --dry-run`, then import and build it from the intended consumer.
- No imports left from the original app (`@/lib/*`).

## Common failures

- CSS variables or global styles left behind in the app.
- An `exports` map pointing at files that aren't emitted.
- React bundled instead of peered.
- Extracting so much that the package becomes a second application.
- Two editable canonical copies left after an in-repo extraction.
