# The `@apply` rule

Where the house style is *"align to using the `@apply` syntax for any custom Tailwind classes"*, custom CSS is written as `@apply` runs rather than raw declarations, and the type case is defined the same way.

Read the best-converted file in the codebase before writing a line. Copy its shape.

## Convert these

Any declaration with an exact Tailwind v4 utility or theme-token equivalent:

- `display`, `position`, `inset` / `top` / `right` / `bottom` / `left`
- `flex`, `flex-direction`, `flex-grow`, `flex-shrink`, `basis`, `align-items`, `justify-content`, `align-self`, `align-content`, `order`
- `gap`, `padding*`, `margin*`, `width`, `height`, `min-*`, `max-*`
- `font-size`, `font-weight`, `text-align`, `line-height`, `letter-spacing`, `text-decoration`, `white-space`, `overflow-wrap`
- `border-radius`, `border-width`, `overflow`, `opacity`, `z-index`, `cursor`, `pointer-events`, `object-fit`, `isolation`, `list-style`, `appearance`, `touch-action`, `user-select`

**Arbitrary values are house style rather than a fallback.** `gap-[0.55rem]`, `tracking-[-0.012em]`, `h-[8.25rem]` are correct. Rounding a measured value to the nearest scale step changes the design - several such values are load-bearing.

## Never convert these

Leave as raw CSS, in the same rule, below the `@apply` line:

- **`transition`, `transform`, `animation`, everything inside `@keyframes`**, and `scale`, `translate`, `rotate`, `perspective`
- Custom properties (`--anything`), and any value resolved at runtime from `var(--…)`
- `color` / `background` whose value comes from a CSS variable
- `box-shadow` with a computed or `color-mix` colour
- `clip-path`, `container-type`, `container-name`, `grid-template-areas`, `grid-template-columns` using `minmax()` beyond what a utility expresses
- Anything inside `@supports`, `@container`, or a `prefers-reduced-motion` block naming a property above

**The motion exclusion is measured.** Tailwind's `transition-*` utilities set `transition-property`, so one rule replacing another rule's transition list silently kills the animation - in one codebase that took out the peel corner on 56 tiles and a `hover:scale-125` that had never once transitioned. Tailwind v4 also compiles `.scale-*` to `scale:` and `.-translate-x-*` to `translate:`, rather than to `transform:`. Neither lint, axe nor the build says a word.

## Utilities that do not mean what the CSS said

A utility whose name matches a value is a different declaration. Check the emitted CSS.

- **`align-items: start` is not `items-start`.** `items-start` compiles to `align-items: flex-start`, a different computed value. `items-[start]` is not a utility and fails the build with `Cannot apply unknown utility class`, which has taken every route in an app to a 500. Leave it raw. The same holds for `justify-content: start`, `end`, and any box-alignment keyword with a `flex-`-prefixed twin.
- Anywhere else a conversion changes the computed value, it is wrong however right it reads.

## `@reference` in a separately bundled stylesheet

A stylesheet the bundler compiles on its own knows no utilities, so every `@apply` in it is an unknown-class build error until it points back at the entry. CSS modules and Vue, Svelte and Astro style blocks are always in this position; a route sheet imported from a `.tsx` often is, depending on the framework. Add at the top, at the correct relative depth:

```css
@reference "../../globals.css";
```

The entry stylesheet does not need it, nor does anything `@import`ed into the entry - both compile with the theme present. Which side of the line a given file sits on is a property of the build, so convert one rule and check the emitted CSS before converting the file.

A missing `@reference` usually fails the build loudly with an unknown-utility error, which is the good failure mode. It is not guaranteed: `@apply` inside a consuming package's own `@layer` block has been observed emitting nothing at all, leaving classes that exist and do nothing. Check the computed style of one converted rule before converting the file, rather than trusting the build to tell you.

## Do not change specificity or source order

`@apply` emits declarations at the specificity of the selector you write, so a one-for-one conversion preserves the cascade. That is the only reason it is safe.

- Do not merge two rules, split one rule, or move a declaration between rules.
- Do not reorder rules. A trailing `@media` block can override component rules through source order alone, and reordering leaves rules silently dead.
- An unlayered rule beats every `@layer utilities` rule at any specificity. Converting a rule into or out of a layer changes what wins.

## Keep every comment

The comments record defects that cost hours. Keep them attached to the rule they describe, and leave the wording alone - a comment naming a property still describes what the CSS does.

## Verify by computed style

For each file touched, compare `getComputedStyle` on a live element before and after, at desktop and mobile widths. A diff that looks right is what ships these bugs.

Convert whole files. A stylesheet half on `@apply` is worse than one consistently raw, so revert a file you cannot finish rather than leaving it split.
