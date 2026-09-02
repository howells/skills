---
name: typecase
description: "Design, migrate and enforce a small set of named type roles across a UI codebase, with a census and a scanner. Use when raw size, weight, tracking, leading, family or case utilities have multiplied, or a type ramp needs designing or collapsing. Not for general visual direction (`chiaroscuro`), interface wording (`signage`), or one-off typography polish."
---

# Typecase

A compositor's type case is a tray of fixed compartments, and you set from what is in it. **Text shape comes from one named role, chosen from a set small enough to hold in your head.**

Shape is size, weight, family, tracking, leading and case. Colour, alignment, wrapping and truncation are not shape and stay free. `capitalize` is the one casing utility that stays a modifier rather than a role, because it cases a data value rather than styling a label; `uppercase` and `lowercase` belong to a role.

Agents write UI faster than anyone reads it, and each one sizes text by picking a plausible utility for the element in front of it. Nothing in that loop notices that the last file chose differently. One measured codebase reached **169 distinct inline typography combinations across 867 usages** before anyone counted - twelve display clamps, fifteen uppercase-marker variants, and a micro-size soup of 9/10/10.5/11/12/13px. No single commit was wrong.

**Writing the rule down does not hold it.** From a repo where the rule sat in `CLAUDE.md` for months: *"CLAUDE.md has always stated the rule. Nothing enforced it, which is why the palette grew three pairs of roles that shared a size."* A rule nothing checks is a rule the next agent will not follow.

## What the case holds

Four to six roles. Every text element in the product picks exactly one.

| Role | For |
| --- | --- |
| `type-display` | Page heroes. One responsive clamp, one role across every viewport. |
| `type-heading` | Section headings. |
| `type-body` | Names, titles and running copy. The same role does both. |
| `type-small` | Metadata, labels, captions, controls. The workhorse. |
| `type-data` | Numerics and codes. A **family variant** of the smallest role, sharing its size and weight. |

Add a role only when a real, nameable job has no home. A products-and-editorial site justified nine; an ops console justified four. Nine is the ceiling, and every role past the fifth needs a sentence saying what it does that its neighbour cannot.

**Two roles that share a size are one role wearing two coats**, and that is how a case grows past the count anyone chose. Collapse them and let weight or family carry the difference.

**Mono is never a new step.** It is the small role in a different family. A mono role that also picks its own size has started a second ladder.

### Small caps, and mono small caps especially

Letter-spaced uppercase micro-labels are the single most over-reached style in agent-written UI. It looks designed, so the model reaches for it on every heading, eyebrow, chip, table header and empty state, and the interface fills with shouting at 10px.

- **At most one small-caps role in the case**, and it earns its place by being sparse - roughly one per screen region, never one per card.
- **Uppercase mono is the sharpest version of the same fault.** Mono already reads as machine output; tracking it out and shouting it turns a label into a system log. Keep uppercase and mono apart unless the thing genuinely is a code.
- The role owns its tracking. Uppercase without positive tracking is unreadable, and inline `tracking-*` beside it means someone is tuning the role from the outside.
- Whatever `uppercase` sits in is a role, never a modifier. Where `uppercase` appears in class attributes, the codebase has a habit rather than a role.

### Arbitrary values are the last resort

`text-[11px]` stays available for a value that genuinely has no name, and it is the last thing to reach for. A one-off pixel value names nothing, so the next file writes its own, and that is how a census reaches a soup of 9/10/10.5/11/12/13px.

In order of preference:

1. **The nearest step on the standard Tailwind scale.** Pixel-level drift between screens was arbitrary rather than designed, and unifying to the nearest step is the point.
2. **A named step added to `@theme`** where the scale genuinely has no step for the job. `--text-micro: 0.6875rem` gives the value a name the next file can reuse, and it appears in the ladder rather than beside it.
3. **The arbitrary value**, where the number is measured and load-bearing. Say so in a comment beside it.

A role's own definition is the exception: `.type-small { @apply text-[0.8125rem] … }` is naming the value, which is the whole job.

### Where the case lives

Two shapes, both fine, and both defined once in the file that imports Tailwind:

- **Component classes** - `.type-body { @apply … }` in `@layer components`.
- **Theme tokens** - `--text-body` in `@theme`, used as `text-body`.

Pick one per codebase. Where the house style is `@apply` for custom classes, the case is written that way too - see [`references/apply-rule.md`](references/apply-rule.md), which carries the `@reference` requirement, the motion exclusion, and the utilities that do not mean what their name says.

`@apply` needs the theme in scope. The stylesheet that imports Tailwind has it, and so does anything `@import`ed into that one. A separately bundled stylesheet - a CSS module, a Vue, Svelte or Astro style block, a route sheet a framework compiles on its own - does not, and needs `@reference` pointing back at the entry. Define the case in the entry, or in a file imported into it, and the question does not arise.

## Steps

Copy these into your todolist verbatim before you start. A step you skip stays in the list with a one-line `skip: <reason>`.

1. **Census before designing.** Run the script and read its output before forming any opinion about how many roles the codebase needs.

   ```bash
   python3 scripts/census-typography.py /path/to/repo --roots apps/web/app apps/web/components
   ```

   It counts distinct shape combinations, the size soup, combinations sharing a size, any roles already in use, and proposes a case measured from what it found. Its proposal is a starting point. Report the counts before proposing anything - the numbers are what make the case arguable rather than a preference.

2. **Read representative occurrences before naming anything.** For each distinct combination the census found, open two or three of the places it is used and write down the job the text is doing there - a row title, a table header, a form hint, a stat figure. A combination doing two jobs gets both recorded. The census counts tokens and cannot see jobs, and a role named from size alone is a guess wearing a number.

   ```bash
   grep -rn 'text-\[11px\]' apps/web --include='*.tsx' | head -5
   ```

3. **Design the case from the jobs, checked against the size ladder.** Take the census's proposal as the starting shape, then decide each band's actual size by hand. Name every role by the job you recorded in step 2. Reject any role that would carry only its own current usages, and any pair sharing a size. State the count and why that count.

4. **Write the migration mapping.** A table: every combination the census found, and the role it becomes. Where an old value falls between two roles, pick the nearer and say so. This table is the deliverable a reviewer checks the diff against.

5. **Define the case once**, in the file that imports Tailwind, with a comment saying what the case is and that a scanner enforces it. Set leading and tracking inside each role.

6. **Name the sanctioned modifiers.** The short list that may sit beside a role: typically `font-medium` for emphasis, `font-mono` for data, `tabular-nums`, and truncation, wrapping, alignment and colour. Everything typographic outside that list belongs to a role.

7. **Migrate**, following the mapping. Convert whole files rather than leaving a file half on the case - a stylesheet with some rules converted and some raw is worse than one consistently raw.

8. **Install the scanner.** `@howells/lint` already ships one - turn on `howells/no-raw-type-utilities` and pass the roles in `allow`. Where that is not available, [`references/gates.md`](references/gates.md) has the three shapes to write instead, the token list, and the five ways a size hides from a naive matcher. Wire it into CI.

9. **Prove the scanner bites.** Plant a violation in a file it should cover, confirm it is named with a `file:line` and a suggested role, then restore. Do this once per configured root, checking each against where the UI actually lives.

10. **Record the exceptions**, if any. Each needs a named file, a stated reason, and an owner. One is normal; three means the case is wrong.

11. **Render it and look.** Screenshot the migrated screens at desktop and mobile widths and compare against before. Roles that were right in a table can still be wrong on a page - especially the small end, where a 21-row table compounds a size difference until the numerals dominate rows they are meant to annotate. Fix by reading `getComputedStyle` on live elements, rather than by reading the diff.

12. **Report.** Combinations before and after, roles and why that many, files migrated, the scanner and its planted-violation proof, exceptions and their owners.

## What the scanner forbids

Anywhere outside the file defining the case:

- Font sizes: `text-xs` … `text-9xl`, `text-[13px]`, `text-[clamp(…)]`, `text-(length:--my-size)`, and the `text-sm/6` shorthand
- Weights: `font-thin` … `font-black` and `font-[450]`, other than a single sanctioned emphasis weight
- Families: `font-sans`, `font-serif`, `font-display`, `font-[Inter]`, and `font-mono` other than as a sanctioned modifier
- `tracking-*` and `leading-*`, entirely
- `uppercase`, `lowercase`

Normalise each token before matching, or five real Tailwind forms walk past: the variant prefix (`md:text-lg`), the important marker in all three positions Tailwind allows (`!text-xl`, `hover:!text-xl`, `text-xl!`), the leading modifier (`text-sm/6`), and v4's CSS-variable shorthand (`text-(length:--my-size)`, which is a size). Class-utility calls (`cn`, `clsx`, `cva`, `tv`, `twMerge`) are scanned as class lists, and so are pass-through props such as `triggerClassName`. Arbitrary text colours are colour and must not be flagged, in every spelling: `text-[#hex]`, `text-[var(--x)]`, `text-[oklch(…)]`, `text-[color:var(--x)]`, `text-[color-mix(…)]`.

## Exceptions

Two hold up. A third is a sign the case itself is wrong.

- **A component that owns its own typography internally** and exposes a `size` prop - a stat figure, a chart axis. One component, named in the scanner, and nothing else passes it inline sizes.
- **Control primitives in a UI package.** A button's weight is part of the control, and rewriting shadcn primitives against a document ladder is the wrong fix for a real distinction. Scope the scanner to the app and leave the primitives out.

## Where this fits

- Visual direction, tokens, spacing, dark mode and browser verification: `chiaroscuro`.
- The words in the labels rather than their size, and over-reached small caps as a copy problem: `signage`.
- Optical sizing, `opsz`, per-size tracking and the rendering stack: chiaroscuro's typography references.
- Duplicated components behind the duplicated styling: `componentize`.
- Removing the raw utilities as machine-written code tells: `unslop`.
