# Interface: Forms

## Labels

- MUST: Use clear, readable text for form labels — same typeface family as body text, legible size.
- MUST NOT: Apply mono small-caps, uppercase tracking, or decorative typographic treatments to form labels. Labels communicate field identity, not brand texture.
- SHOULD: Position labels above inputs. Side-aligned labels create scanning friction on narrow viewports.

## Input Types

- MUST: Correct `type` for keyboard/validation: `email`, `tel`, `url`, `number`, `search`, `password`

## Input Attributes

- MUST: `autocomplete` + meaningful `name` for login/address forms
- SHOULD: `spellcheck="false"` for emails, codes, usernames
- SHOULD: `data-1p-ignore` to suppress password manager icons where unwanted

```html
<input type="text" spellcheck="false" autocomplete="off" data-1p-ignore />
```

## Control Styling

- MUST NOT: Pair `shadow-*` with a solid gray border on any control. Use a ring instead: `ring-1 ring-black/10 shadow-*`, never `border border-gray-300 shadow-*`.
- SHOULD: Use `max-w-xs` for compact, single-purpose forms (login, sign-up, single-field) — `max-w-sm` and wider feels too spacious for focused UI.
- MUST NOT: Use `outline-offset-*` on custom focus rings for `<input>`/`<textarea>`; use `outline-offset-0` or omit it. When using a 2px focus outline, inset it with `-outline-offset-1` so it does not extend outside the element.
- MUST NOT: Use the conjoined input + button pattern where the two share a border. Add a gap between them, or nest the button visually inside the input.
- MUST: Bump small inputs to `16px` on mobile — if a text input's font size is below `16px`, add `max-sm:text-base/{lh}` to prevent iOS zoom.
- SHOULD: Scale touch controls down at `sm:` — checkboxes/radios `size-5 sm:size-4`, toggles `w-11 sm:w-9`.

## Control Markup

Build native controls; apply state styling in CSS via variants. **Never use JavaScript to toggle classes based on input state.** Replace `{brand}`/`{gray}` with project colors. Associate a `<label>` via `id`/`for`, or give the control an `aria-label`.

### Select — custom chevron

Wrap only the `<select>` and chevron (never the label) in `inline-grid grid-cols-[1fr_--spacing(8)]`; the `<select>` gets `col-span-full row-start-1 appearance-none pr-8`; the chevron SVG gets `pointer-events-none col-start-2 row-start-1 place-self-center`.

### Checkbox

```html
<span class="group inline-grid size-4 grid-cols-1">
  <input
    type="checkbox"
    class="checked:border-{brand} checked:bg-{brand} indeterminate:border-{brand} indeterminate:bg-{brand} focus-visible:outline-{brand} dark:checked:border-{brand} dark:checked:bg-{brand} dark:indeterminate:border-{brand} dark:indeterminate:bg-{brand} dark:focus-visible:outline-{brand} col-start-1 row-start-1 appearance-none rounded-sm border border-gray-300 bg-white focus-visible:outline-2 focus-visible:outline-offset-2 disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100 dark:border-white/10 dark:bg-white/5 dark:disabled:border-white/5 dark:disabled:bg-white/10 dark:disabled:checked:bg-white/10 forced-colors:appearance-auto"
  />
  <svg viewBox="0 0 14 14" fill="none" class="pointer-events-none col-start-1 row-start-1 size-7/8 self-center justify-self-center stroke-white group-has-disabled:stroke-gray-950/25 dark:group-has-disabled:stroke-white/25">
    <path d="M3 8L6 11L11 3.5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-not-has-checked:opacity-0" />
    <path d="M3 7H11" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-not-has-indeterminate:opacity-0" />
  </svg>
</span>
```

### Radio

```html
<span class="group inline-grid size-4 grid-cols-1">
  <input
    type="radio"
    class="checked:border-{brand} checked:bg-{brand} focus-visible:outline-{brand} dark:checked:border-{brand} dark:checked:bg-{brand} dark:focus-visible:outline-{brand} col-start-1 row-start-1 appearance-none rounded-full border border-gray-300 bg-white focus-visible:outline-2 focus-visible:outline-offset-2 disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100 dark:border-white/10 dark:bg-white/5 dark:disabled:border-white/5 dark:disabled:bg-white/10 dark:disabled:checked:bg-white/10 forced-colors:appearance-auto"
  />
  <span class="pointer-events-none col-start-1 row-start-1 size-[round(down,40%,1px)] self-center justify-self-center rounded-full bg-white group-not-has-checked:opacity-0 group-has-disabled:bg-gray-400 dark:group-has-disabled:bg-white/25"></span>
</span>
```

### Toggle

Default width `w-9`. Remove all `dark:` classes if the site has no dark mode; for always-dark sites, use the `dark:` values as base and drop the prefix.

```html
<div class="group outline-{brand}-600 has-checked:bg-{brand}-600 dark:outline-{brand}-500 dark:has-checked:bg-{brand}-500 bg-{gray}-200 inset-ring-{gray}-900/5 relative inline-flex w-9 shrink-0 rounded-full p-0.5 inset-ring outline-offset-2 transition-colors duration-200 ease-in-out has-focus-visible:outline-2 dark:bg-white/5 dark:inset-ring-white/10">
  <span class="ring-{gray}-900/5 aspect-square w-1/2 rounded-full bg-white ring-1 shadow-xs transition-transform duration-200 ease-in-out group-has-checked:translate-x-full"></span>
  <input type="checkbox" class="absolute inset-0 size-full appearance-none focus:outline-hidden" />
</div>
```

To vertically center a checkbox/radio with adjacent text, wrap it in an element with `h-lh items-center` and the matching `text-{size}` — never put `h-lh` on the `inline-grid` wrapper, never use top margins.

## Input Decorations

- SHOULD: Position icons absolutely inside input with padding offset
- MUST: Clickable icons trigger input focus

```jsx
<div className="relative">
  <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400" />
  <input className="pl-10 ..." />
</div>
```

## iOS

- MUST: `text-base` minimum on mobile inputs (16px prevents zoom on focus)

## Autofocus

- SHOULD: Autofocus primary input on desktop
- NEVER: Autofocus on touch devices (opens keyboard unexpectedly)

```jsx
<input autoFocus={!('ontouchstart' in window)} />
```

## Form Behavior

- MUST: Wrap inputs in `<form>` for Enter submission
- MUST: ⌘/Ctrl+Enter submits `<textarea>`; Enter adds newline
- MUST: Keep submit enabled until request starts, then disable + show spinner + keep original label
- MUST: Use idempotency keys on submit to prevent duplicate requests
- MUST: Accept free text input; validate after, don't block typing
- MUST: Allow submitting incomplete forms to surface validation errors
- MUST: Warn on unsaved changes before navigation
- MUST: Allow pasting (never block paste)
- MUST: Trim whitespace from values
- MUST: Hydration-safe inputs — no lost focus or value after hydration
- MUST: Compatible with password managers and 2FA; allow pasting one-time codes
- SHOULD: Prefill with user data when available
- SHOULD: Placeholder ends with ellipsis: `Search…`, `sk-012345…`

## Buttons

- MUST: Disable after submission to prevent duplicates
- SHOULD: Show keyboard shortcut in tooltip: `Save (⌘S)`
- SHOULD: `active:scale-[0.97]` for press feedback

```jsx
<button className="active:scale-[0.97] transition-transform">Submit</button>
```

## Checkboxes/Radios

- MUST: No dead zones — entire row clickable

```jsx
<label className="flex items-center gap-2 cursor-pointer">
  <input type="checkbox" />
  <span>Remember me</span>
</label>
```

## Validation

- MUST: Use `aria-invalid` on invalid inputs

```jsx
<input aria-invalid={!!error} className={error ? "border-red-500" : ""} />
{error && <span className="text-sm text-red-500">{error}</span>}
```

## Destructive Actions

- MUST: Require confirmation (use `AlertDialog`, not `confirm()`)
