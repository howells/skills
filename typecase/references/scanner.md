# Scanners

Contents: the token list · normalising tokens · shape 1 oxlint plugin · shape 2 test · root lists · CSS files.

A lint rule should use AST scoping so comments, documentation and unrelated string props do not become violations.

## Writing your own

Pick the shape by the codebase's state.

| Shape | Pick it when | Cost |
| --- | --- | --- |
| **oxlint plugin** | The codebase is clean, or close. Editor squiggles and a per-line message. | Needs oxlint with JS plugin support and a local rule implementation. |
| **Test** | The test suite is already the CI gate and you want no new script. | Runs at test speed, reports as a test failure. |

Both read the same token list, matched against the normalised token from the section below. Only the delivery differs.

## The token list

```js
const NAMED_TEXT_SIZE = /^text-(xs|sm|base|lg|xl|[2-9]xl)$/u;
// Arbitrary sizes, but NOT arbitrary colours, in any spelling.
const ARBITRARY_SIZE  = /^text-\[(?!#|var\(|rgb|hsl|okl(?:ch|ab)|color[-:(]|currentColor)[^\]]+\]$/u;
// v4's typed custom-property shorthand. Always a size.
const VARIABLE_SIZE   = /^text-\(length:--[\w-]+\)$/u;
const FONT_WEIGHT     = /^font-(thin|extralight|light|normal|medium|semibold|bold|extrabold|black|\[\d+\])$/u;
const FONT_FAMILY     = /^font-(sans|serif|mono|display|\[[^\]]+\])$/u;
const TRACKING        = /^-?tracking-(?:[\w.-]+|\[[^\]]+\]|\(--[\w-]+\))$/u;
const LEADING         = /^leading-(?:[\w.-]+|\[[^\]]+\]|\(--[\w-]+\))$/u;
const CASE            = /^(uppercase|lowercase)$/u;
```

Skip the sanctioned modifiers before matching, and skip the file that defines the roles.

Match against the normalised token from the next section, which is why there is no pattern here for `text-sm/6` - it arrives as `text-sm`.

The negative lookahead in `ARBITRARY_SIZE` is load-bearing. Without it the scanner flags `text-[#1c1917]` and `text-[var(--ink)]`, which are colour, and the first person to hit that false positive turns the scanner off. `color[-:(]` covers all three spellings at once: the functional `color(`, the `color-mix()` blend, and the `color:` type hint that disambiguates a bare `var()`.

## Normalise the token first

Five ways a size hides from a scanner that matches the raw class. Each is a real Tailwind form and each was found escaping a shipped rule.

| Written | Matcher sees | Fix |
| --- | --- | --- |
| `md:text-lg` | `md:text-lg` | Strip everything to the last top-level `:` |
| `!text-xl` | `!text-xl` | Strip a leading `!` |
| `hover:!text-xl` | `!text-xl` | Strip the `!` after the variant split, rather than before it |
| `text-xl!` | `text-xl!` | Strip a trailing `!` - Tailwind v4's spelling |
| `text-sm/6` | `text-sm/6` | Strip a trailing `/modifier` - the size-and-leading shorthand |

Split at depth zero, counting parentheses as well as brackets, or three forms break: `data-[state=open]:text-lg`, `text-[calc(1rem/2)]`, and v4's `text-(length:--my-size)`.

```js
function baseUtility(token) {
  const stripped = token.endsWith("!") ? token.slice(0, -1) : token;
  let depth = 0, lastColon = -1, lastSlash = -1;
  for (let i = 0; i < stripped.length; i += 1) {
    const c = stripped[i];
    if (c === "[" || c === "(") depth += 1;
    else if (c === "]" || c === ")") depth -= 1;
    else if (depth === 0 && c === ":") { lastColon = i; lastSlash = -1; }
    else if (depth === 0 && c === "/") lastSlash = i;
  }
  const base = stripped.slice(lastColon + 1, lastSlash === -1 ? undefined : lastSlash);
  return base.startsWith("!") ? base.slice(1) : base;
}
```

Two orderings carry the bugs. Stripping a leading `!` before the colon split misses `hover:!text-xl`, which is how v3 spells an important utility under a variant. Resetting `lastSlash` at each top-level colon matters too: without it, `group-hover:text-sm/6` keeps a slash index from before the variant boundary.

## Shape 1: oxlint plugin

`scripts/oxlint-plugins/no-inline-typography.mjs`, reporting on the JSX attribute node so the message lands on the line.

Cover four call sites, or the rule reads as enforced while most violations walk past:

- `className="…"` and `class="…"`
- Pass-through props: match `/(?:^class$)|class[Nn]ame$/u`, catching `triggerClassName`, `avatarClassName`
- String arguments to class utilities: `cn`, `clsx`, `cx`, `cva`, `tv`, `twMerge`, `twJoin`, `classNames` - **wherever the call sits**, including a `cva` defined above the component with no attribute around it
- Size ladders: a `Record<*Size, string>` whose values are class strings

The last two are where a component library keeps most of its type utilities. A scanner that reaches only into class attributes reports `button-variants.ts` as clean.

Name the fix in the message, so the reader does not have to look the case up:

```js
const SHAPE = {
  "font size": [NAMED_TEXT_SIZE, ARBITRARY_SIZE, VARIABLE_SIZE],
  "font weight": [FONT_WEIGHT],
  "font family": [FONT_FAMILY],
  "tracking": [TRACKING],
  "line-height": [LEADING],
  "case": [CASE],
};
for (const [kind, patterns] of Object.entries(SHAPE)) {
  if (patterns.some((pattern) => pattern.test(base))) {
    return `inline ${kind} "${base}" - the role sets it; use type-display / type-heading / type-body / type-small (type-data for numeric text)`;
  }
}
```

Example configuration; add the project's intended file scope and permitted primitive exceptions:

```ts
// oxlint.typography.config.ts
const specifier = new URL("scripts/oxlint-plugins/no-inline-typography.mjs", import.meta.url).href;

export default {
  jsPlugins: [{ name: "typography", specifier }],
  rules: { "typography/no-inline-typography": "error" },
};
```

## Shape 2: test

`src/typography-discipline.test.ts`, walking the source tree and asserting an empty violation list. Two regexes are needed, because the attribute pattern cannot reach inside a `cn()` call:

```ts
const CLASS_ATTR = /(?:className|class)\s*[=:]\s*[{]?\s*(?<quote>["'`])(?<classes>(?:(?!\k<quote>)[\s\S])*)\k<quote>/gu;
// Anchored on the utility, not on `className=`, so a standalone `cva(…)` is read.
const CLASS_FN   = /\b(?:cn|cx|clsx|cva|tv|twMerge|twJoin|classNames)\s*\((?<args>(?:[^()]|\([^()]*\))*)/gu;
const QUOTED     = /(?<quote>["'`])(?<fragment>(?:(?!\k<quote>)[\s\S])*?)\k<quote>/gu;
```

Anchoring `CLASS_FN` on `className=` is the common mistake: it reads `className={cn("text-sm")}` and misses the `cva` variant table in the file above it. Key each quoted run by its position so a call nested inside an attribute counts once.

Exceptions go in a `Set` of paths beside a comment naming the reason:

```ts
const EXCEPTIONS = new Set(["app/charts/axis-label.tsx"]);
```

## Root lists

Where a sibling scanner already keeps a root list - an arbitrary-colour check, a drift check - read it rather than writing a second one. Two separately maintained lists that should agree is a defect waiting for one of them to be updated alone.

## CSS files

Where the house style puts typography in `.css` through `@apply`, scan stylesheets too, and skip the rules that define the roles: `.type-body { @apply text-sm … }` is the case, not a violation of it.
