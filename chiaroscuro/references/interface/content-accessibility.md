# Interface: Content & Accessibility

## HTML Antipatterns (WCAG Quick Reference)

Common patterns that fail accessibility, mapped to WCAG success criteria.

### Critical (Must Fix)

| Pattern | WCAG | What it looks like |
|---------|------|------------------|
| Images without alt | 1.1.1 | `<img>` missing `alt` attribute |
| Icon-only buttons | 4.1.2 | `<button>` containing only SVG/icon, no `aria-label` |
| Unlabeled form inputs | 1.3.1 | `<input>`, `<select>`, `<textarea>` without `<label>` or `aria-label` |
| Non-semantic click handlers | 2.1.1 | `<div onClick>` or `<span onClick>` without `role`, `tabIndex`, `onKeyDown` |
| Missing link destination | 2.1.1 | `<a>` with only `onClick`, no `href` |
| `aria-hidden` on focusable | 4.1.2 | `aria-hidden="true"` on element with `tabIndex` or native focusability |

### Serious (Should Fix)

| Pattern | WCAG | What it looks like |
|---------|------|------------------|
| Focus outline removed | 2.4.7 | `outline-none` or `outline: none` without `focus-visible:ring` replacement |
| Missing keyboard handlers | 2.1.1 | A custom widget (not a native `<button>`, `<a href>` or form control) with `onClick` but no keyboard operation. Native controls already handle keys; adding handlers can double-fire |
| Color-only information | 1.4.1 | Status/error indicated by color alone (no icon or text) |
| Touch target too small | 2.5.5 | Clickable elements below the `interactions.md` guidance (44×44 CSS pixels on coarse pointers) |
| Heading hierarchy skipped | 1.3.1 | `h1` followed by `h3` (skipping `h2`) |

### Moderate (Consider Fixing)

| Pattern | WCAG | What it looks like |
|---------|------|------------------|
| Positive tabIndex | 2.4.3 | `tabIndex` > 0 (disrupts natural tab order) |
| Role without required attrs | 4.1.2 | `role="button"` without `tabIndex="0"` |
| Placeholder-only labels | 1.3.1 | `<input placeholder="...">` without visible `<label>` |
| Auto-playing media | 1.4.2 | `<video autoPlay>` or `<audio autoPlay>` without pause control |

## ARIA

- NEVER: Use `aria-hidden="true"` on focusable elements
- MUST: Label elements need text and an associated input
- MUST: All anchors must be valid and navigable
- MUST: Accurate names (`aria-label`), decorative elements `aria-hidden`, verify in the Accessibility Tree
- MUST: Icon-only buttons have descriptive `aria-label`
- NEVER: Add tooltips to disabled buttons (inaccessible to keyboard users)
- MUST: Tooltips shouldn't contain interactive content
- MUST: An HTML illustration that carries meaning gets `role="img"` and an accessible name; a decorative one gets `aria-hidden="true"`. Otherwise its raw DOM is announced

## Focus

- MUST: Preserve visible focus in forced-colours mode. A custom box-shadow ring needs an outline that survives when shadows are removed:

```css
:focus-visible {
  outline: 2px solid transparent;
  outline-offset: 2px;
  box-shadow: 0 0 0 2px var(--background), 0 0 0 4px var(--ring);
}
```

- MUST: Implement the keyboard model expected by the chosen semantic pattern. Composite widgets such as menus, tabs, listboxes, and radio groups commonly use arrow keys; ordinary link and button lists remain in natural Tab order.
- SHOULD: Add destructive shortcuts only when the product establishes them, exposes an alternative, and provides undo or confirmation appropriate to the consequence.

## UX Copy & Writing Voice

Interface wording, casing and voice belong to `signage`. One rule stays here because it shapes the design itself:

### No System Leakage

UI copy describes the user's objects, decisions, and next actions. System internals - database tables, API mechanics, agent steps, model names, orchestration states - stay hidden unless the target user is a technical operator whose work requires them.

- MUST: Translate implementation states into user outcomes: `sync failed` → `Updates are paused`; `indexing` → `Search is updating`; `agent step running` → `Checking the next section`
- MUST: Use domain nouns and verbs from the user's work, not database tables, API endpoints, prompt stages, model names, or workflow engine states
- MUST: Put technical diagnostics behind explicit affordances such as "View details", "Copy error", or "Open logs" when they are useful
- NEVER: Surface chain-of-thought, prompt scaffolding, hidden system instructions, raw orchestration steps, or internal scoring
- NEVER: Let navigation mirror the implementation architecture unless the target user's mental model genuinely matches it

## Content & Accessibility
- SHOULD: Inline help first; tooltips last resort
- MUST: Skeletons mirror final content to avoid layout shift
- MUST: `<title>` matches current context
- MUST: No dead ends; always offer next step/recovery
- MUST: Design empty/sparse/dense/error states
- SHOULD: Curly quotes (" "); avoid widows/orphans
- MUST: Tabular numbers for comparisons (`font-variant-numeric: tabular-nums` in the established body font).
- MUST: Redundant status cues (not color-only); icons have text labels
- MUST: Don't ship the schema - visuals may omit labels but accessible names still exist
- MUST: Use the ellipsis character `…` (not `...`)
- MUST: `scroll-margin-top` on headings for anchored links; include a "Skip to content" link; hierarchical `<h1–h6>`
- MUST: Resilient to user-generated content (short/avg/very long)
- MUST: Locale-aware dates/times/numbers/currency
- MUST: Plurals through `Intl.PluralRules`, never "1 members"
- SHOULD: Relative times ("3 hours ago") switch to absolute dates after about a week
- SHOULD: `translate="no"` on brand names, code and identifiers so page translation leaves them intact
- MUST: Announce a changing count with its context ("3 items in cart") in one atomic `role="status"` message, never as a bare number or from competing live regions
- MUST: Use non-breaking spaces to glue terms: `10\u00A0MB`, `⌘\u00A0+\u00A0K`, `Vercel\u00A0SDK`
