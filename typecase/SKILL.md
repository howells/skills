---
name: typecase
description: "Replace a UI codebase's scattered font utilities with a few named type roles and a scanner that holds them, and choose the faces. Use when text sizes have multiplied or a type ramp needs designing. Not for visual direction (`chiaroscuro`) or wording (`signage`)."
---

# Typecase

A compositor sets from the compartments in the case. **Every piece of text takes its shape from one named role, chosen from a set small enough to hold in your head.**

Shape is size, weight, family, tracking, leading and case. Colour, alignment, wrapping and truncation are not shape and stay free.

Agents size text by picking a plausible utility for the element in front of them, and nothing notices that the last file chose differently. One codebase reached 169 distinct combinations across 867 usages, including a micro-size soup of 9/10/10.5/11/12/13px, with no single wrong commit. **A rule nobody checks does not hold**, so the job ends with a scanner in CI.

## Rules

1. **Four to six roles; nine is the ceiling.** Every role past the fifth needs a sentence saying what it does that its neighbour cannot. Add one only when a real, nameable job has no home.
2. **Hierarchy steps have distinct sizes.** Two roles sharing a size are one role. The exception is a declared family variant such as `type-data`: same size and weight as its base, different family or numeric features. It counts toward the total but adds no step.
3. **Mono is never a new step.** It is the small role in another family. A mono role with its own size has started a second ladder.
4. **No small-caps or tracked-uppercase role** unless the user asks for one or supplies a brand treatment that uses it, and then about one per screen region. An existing small-caps habit is a finding to migrate. Keep uppercase and mono apart unless the text genuinely is a code. Whatever `uppercase` sits in is a role, which owns its positive tracking.
5. **The nearest Tailwind step beats an arbitrary value.** Pixel drift between screens was never designed. Where the scale truly lacks a step, name one in `@theme` (`--text-micro: 0.6875rem`). Keep `text-[11px]` only for a measured, load-bearing value, with a comment. A role's own definition is exempt: naming the value is its job.
6. **Every weight a role uses is a face the page loads.** A `font-semibold` role over a family shipped in 400 and 700 renders a synthesised bold.

Defaults for the roles, to depart from with a reason:

| Role | For | Leading |
| --- | --- | --- |
| `type-display` | Page heroes. One responsive clamp across every viewport. | 1.0–1.1 |
| `type-heading` | Section headings. | 1.2–1.3 |
| `type-body` | Names, titles and running copy, one role for both. 16px for long-form; 14px is fine in dense tools. | 1.5 |
| `type-small` | Metadata, labels, captions, controls. The workhorse. Not below 12px. | 1.4 |
| `type-data` | Numerics and codes: `type-small` with `tabular-nums` or mono. | as base |

- Below 18px, weight 400 or heavier; light weights belong at 28px and up.
- Anything that can wrap to three lines needs leading of 1.4 or more, even in a tight row. `leading-tight` on a card description is the usual offender.
- Tracking tightens as size grows: about -0.02em from 24px up, 0 for body, about +0.05em for uppercase at 14px and below. Bind it into the role or the `@theme` size token, never inline.
- iOS Safari zooms the page when an input's text is under 16px. A role used in inputs carries the bump itself (`text-base sm:text-sm`).

## Where the case lives

Define it once, in the stylesheet that imports Tailwind or a file `@import`ed into it, as either component classes (`.type-body { @apply … }` in `@layer components`) or theme tokens (`--text-body` in `@theme`, used as `text-body`). Pick one per codebase. A separately bundled stylesheet (a CSS module, a Vue, Svelte or Astro style block, some route sheets) has no theme in scope and needs `@reference`. Where the house style writes custom classes with `@apply`, read [`references/apply-rule.md`](references/apply-rule.md) before converting any CSS: it covers `@reference`, the motion exclusion and utilities whose names lie.

Choosing or changing a face: read [`references/font-recommendations.md`](references/font-recommendations.md). OpenType features, optical sizing, rendering, wrapping and font loading: read [`references/typography-opentype.md`](references/typography-opentype.md).

## Steps

For an audit or proposal, stop after step 4 and return the census and mapping. A request to migrate or enforce authorises the rest.

1. **Census.** Run the script before forming a view on how many roles the codebase needs, and report its counts; they make the case arguable rather than a preference.

   ```bash
   python3 scripts/census-typography.py /path/to/repo --roots apps/web/app apps/web/components
   ```

   `--json` gives every location for the migration. It is lexical: it does not scan `@apply` inside Vue, Svelte or Astro style blocks, and it cannot resolve dynamic class expressions, so check those by hand. Exit 2 means coverage was incomplete, not that the census is clean.
2. **Read the jobs.** For each combination, open two or three uses and write down what the text is doing there: row title, table header, form hint, stat figure. The census sees tokens, not jobs, and a role named from its size alone is a guess.
3. **Design the case** from those jobs, using the census's proposal as a starting shape and the rules above. Name each role by its job. State the count and why.
4. **Write the mapping:** every combination the census found and the role it becomes, with the nearer role chosen where a value falls between two. Reviewers check the diff against this table.
5. **Define the case** with a comment saying a scanner enforces it.
6. **Name the sanctioned modifiers** and the one dimension each may change: `font-medium` for emphasis, `font-mono` for family, `capitalize` for casing a data value, `tabular-nums` for figures. None changes size, leading or tracking. Everything else typographic belongs to a role.
7. **Migrate** by the mapping, a whole file at a time. A file half on the case is worse than one consistently raw.
8. **Install the scanner.** Use the project's existing typography lint rule if it really covers class attributes, `cn`/`cva`-style calls and size maps. Otherwise read [`references/gates.md`](references/gates.md) for the three shapes, the token list and the normalisation that stops sizes slipping past. Wire it into CI. An unreached root reports clean, so plant one violation per root, confirm it is named with `file:line`, and restore it.
9. **Look at the migrated screens** on desktop and a phone. The small end goes wrong in place: across a 21-row table a one-step size difference lets numerals dominate rows they should annotate. Settle doubts with `getComputedStyle` on live elements.
10. **Report** combinations before and after, the roles and why that many, files migrated, the scanner, and any exceptions with owner and reason.

## What the scanner forbids

Outside the file that defines the case:

- sizes: `text-xs` … `text-9xl`, `text-[13px]`, `text-[clamp(…)]`, `text-(length:--x)`, `text-sm/6`;
- weights: `font-thin` … `font-black`, `font-[450]`, except the sanctioned emphasis weight;
- families: `font-sans`, `font-serif`, `font-display`, `font-[Inter]`, and `font-mono` except as sanctioned;
- all `tracking-*` and `leading-*`;
- `uppercase` and `lowercase`.

Arbitrary text colours (`text-[#hex]`, `text-[var(--x)]`, `text-[oklch(…)]`, `text-[color:…]`) are colour and must pass, or the first false positive gets the scanner switched off.

## Exceptions

Two hold up; a third means the case is wrong.

- **A component that owns its typography** and exposes a `size` prop, such as a stat figure or chart axis. Name it in the scanner; nothing passes it inline sizes.
- **Control primitives in a UI package.** A button's weight belongs to the control. Scope the scanner to the app rather than rewriting shadcn primitives against a document ladder.

## Where this fits

- Visual design, tokens, spacing and dark mode: `chiaroscuro`.
- The words in the labels: `signage`.
- Duplicated components behind duplicated styling: `componentize`.
