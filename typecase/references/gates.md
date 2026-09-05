# Scanners

**Reach for `@howells/lint` first.** It ships `howells/no-raw-type-utilities`, which does this generically: it carries no project token table, governs a configurable namespace, and permits exactly what you pass in `allow`. It scans `className`/`class` attributes, `cn`/`cx`/`clsx`/`cva`/`tv`/`twMerge`/`twJoin`/`classNames` arguments, and `Record<*Size, string>` size ladders through real AST scoping, so it never fires on a same-spelled word in a comment, a JSDoc `@example`, or an unrelated string prop.

```ts
import react from "@howells/lint/oxlint/react";

export default {
  extends: [react],
  rules: {
    "howells/no-raw-type-utilities": [
      "error",
      {
        allow: [
          "type-display", "type-heading", "type-body", "type-small", "type-data",
          "font-medium", "font-mono",
        ],
      },
    ],
  },
};
```

It is opt-in and enabled by no preset, so it does nothing until a project turns it on. `match` widens or narrows the governed namespace; the default is standard Tailwind typography, excluding colour, alignment and wrapping.

Write one of the three shapes below only where `@howells/lint` is not available, or where the delivery has to be a baseline or a test rather than a lint rule.

## Writing your own

Three shapes, all in production. Pick by the codebase's state, not by taste.

| Shape | Pick it when | Cost |
| --- | --- | --- |
| **oxlint plugin** | The codebase is clean, or close. Editor squiggles and a per-line message. | Needs `@howells/lint` and a JS plugin entry. |
| **Baselined script** | Existing debt is real and cannot be paid down now. Files may not grow their count; new files must be clean. | A checked-in baseline that needs deliberate refreshing. |
| **Test** | The test suite is already the CI gate and you want no new script. | Runs at test speed, reports as a test failure. |

All three read the same token list, matched against the normalised token from the section below. Only the delivery differs.

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

These patterns include custom-property shorthand, arbitrary values and negative tracking. Cover examples such as `leading-(--line-height)`, `leading-[calc(1em+2px)]`, `tracking-(--tracking)` and `-tracking-2` in scanner checks.

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

`text-(length:--my-size)` is v4 shorthand for `text-[length:var(--my-size)]`, so it is always a size and needs its own pattern - `^text-\(length:--[\w-]+\)$` - alongside the bracket form. Arbitrary weights and families (`font-[450]`, `font-[Inter]`) are shape too, and a weight pattern listing only the named steps misses them.

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
if (NAMED_TEXT_SIZE.test(base) || ARBITRARY_SIZE.test(base)) {
  return `inline font size "${base}" - use one of the roles (type-display / type-heading / type-body / type-small; type-data for numeric text)`;
}
if (FONT_WEIGHT.test(base)) {
  return `inline font weight "${base}" - weight is part of the display, heading, body or small role`;
}
if (LEADING.test(base)) {
  return `inline line-height "${base}" - the role already sets leading; delete it`;
}
```

Config, scoped so the UI package's control primitives stay out:

```ts
// oxlint.typography.config.ts
const specifier = new URL("scripts/oxlint-plugins/no-inline-typography.mjs", import.meta.url).href;

export default {
  jsPlugins: [{ name: "howells-ui", specifier }],
  rules: { "howells-ui/no-inline-typography": "error" },
};
```

## Shape 2: baselined script

`scripts/check-typography.mjs` with `scripts/typography-baseline.json`. Counts forbidden tokens per file; a file may not exceed its baseline, and a file absent from the baseline must be clean.

```js
const violations = [];
for (const [file, n] of Object.entries(current)) {
  const allowed = baseline[file] ?? 0;
  if (n > allowed) violations.push({ file, n, allowed });
}
```

`--update` rewrites the baseline. It is for recording a deliberate reduction. A baseline refreshed to make CI green records the drift as approved, and the next agent reads it as the standard.

Print the fix in the failure, and say which roles exist:

```
Typography gate: raw type utilities must be a role class (type-*).
  apps/web/features/panel.tsx: 4 (baseline 1)
Fix by using type-display/heading/title/body/small/micro/data, or run --update if intentional.
```

## Shape 3: test

`src/typography-discipline.test.ts`, walking the source tree and asserting an empty violation list. Two regexes are needed, because the attribute pattern cannot reach inside a `cn()` call:

```ts
const CLASS_ATTR = /(?:className|class)\s*[=:]\s*[{]?\s*(?<quote>["'`])(?<classes>(?:(?!\k<quote>)[\s\S])*)\k<quote>/gu;
// Anchored on the utility, not on `className=`, so a standalone `cva(…)` is read.
const CLASS_FN   = /\b(?:cn|cx|clsx|cva|tv|twMerge|twJoin|classNames)\s*\((?<args>(?:[^()]|\([^()]*\))*)/gu;
const QUOTED     = /(?<quote>["'`])(?<fragment>(?:(?!\k<quote>)[\s\S])*?)\k<quote>/gu;
```

Anchoring `CLASS_FN` on `className=` is the common mistake: it reads `className={cn("text-sm")}` and misses the `cva` variant table in the file above it. Key each quoted run by its position so a call nested inside an attribute counts once.

Exceptions go in a `Set` of paths beside a comment naming the reason and the ADR:

```ts
const EXCEPTIONS = new Set(["app/(site)/(editorial)/pulse/animated-figure.tsx"]);
```

## Scoping the roots

Every shape needs a root list, and an unreached root produces the same clean output as a covered one. Plant a violation and confirm the scanner names it:

```
apps/storybook/stories/button.stories.tsx:76  text-sm → use `type-body`
```

Then restore. Do this once per root, on install and whenever the roots change.

Where a sibling scanner already keeps a root list - an arbitrary-colour check, a drift check - read it rather than writing a second one. Two separately maintained lists that should agree is a defect waiting for one of them to be updated alone.

## Where the case is `@apply`

A stylesheet compiled as its own chunk knows no utilities, so every `@apply` in it is an unknown-class build error until it carries `@reference`. Scan `.css` files too where the house style puts typography there, and skip the rules that define the roles themselves - `.type-body { @apply text-sm … }` is the case, not a violation of it. See [`apply-rule.md`](apply-rule.md).
