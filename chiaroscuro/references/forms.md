# Forms

Contents: labels and inputs · choosing controls · styling · control markup · behaviour and validation.

## Labels and inputs

- Labels sit above inputs, in the body face at a legible size, sentence case. Every control has a `<label>` (wrapping or `for`) or an `aria-label`, and label and control share one hit target with no dead zone.
- A placeholder never repeats or replaces the label. Show a format or an example ending in `…` (`sk-012345…`), or leave it empty.
- The right `type` and `inputmode`; `autocomplete` and a meaningful `name` on login, address and payment fields; `autocomplete="off"` and `data-1p-ignore` on fields a password manager shouldn't touch.
- `spellcheck="false"`, `autocapitalize="none"` and `autocorrect="off"` for emails, codes and usernames. One-time codes take `autocomplete="one-time-code"` and `inputmode="numeric"`.
- `enterkeyhint` (`search`, `send`, `next`, `done`) so the phone's action key says what happens.
- Password fields get a show-and-hide toggle. Never block paste.
- Autofocus the primary input on desktop only; on touch it throws up the keyboard.
- Prefill what you know, and reuse what the person entered earlier in the flow.

## Choosing controls

- Two to seven mutually exclusive options: a segmented control. More: a radio list or select.
- A switch applies immediately; a checkbox is submitted with the form.
- One save model per settings view: everything saves on change, or there is an explicit Save. Never a mixture.
- A setting whose effect is easier to see than describe (an email, a notification, an invoice) gets a preview beside it.

## Styling

- Never a shadow with a solid grey border on a control; use a ring: `ring-1 ring-black/10 shadow-xs`.
- Custom focus outlines on `<input>` and `<textarea>` sit inside: `-outline-offset-1` with a 2px outline, never a positive offset.
- No conjoined input and button sharing a border. Leave a gap, or nest the button visually inside the input.
- Compact single-purpose forms (sign-in, one field) are `max-w-xs`.
- Touch controls scale down on larger screens: checkboxes `size-5 sm:size-4`, toggles `w-11 sm:w-9`.
- Icons inside an input sit absolutely with padding to clear them; a clickable one focuses the input.

## Control markup

Build native controls and style state with variants. Never toggle classes from input state in JavaScript. Replace `{brand}` and `{gray}` with the project's colours; drop `dark:` classes on sites without dark mode.

**Select with a custom chevron.** Wrap only the `<select>` and chevron in `inline-grid grid-cols-[1fr_--spacing(8)]`. The select takes `col-span-full row-start-1 appearance-none pr-8`; the chevron `pointer-events-none col-start-2 row-start-1 place-self-center`.

**Checkbox**

```html
<span class="group inline-grid size-4 grid-cols-1">
  <input type="checkbox" class="col-start-1 row-start-1 appearance-none rounded-sm border border-{gray}-300 bg-white checked:border-{brand} checked:bg-{brand} indeterminate:border-{brand} indeterminate:bg-{brand} focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-{brand} disabled:border-{gray}-300 disabled:bg-{gray}-100 disabled:checked:bg-{gray}-100 dark:border-white/10 dark:bg-white/5 dark:checked:border-{brand} dark:checked:bg-{brand} dark:disabled:border-white/5 dark:disabled:bg-white/10 forced-colors:appearance-auto" />
  <svg viewBox="0 0 14 14" fill="none" class="pointer-events-none col-start-1 row-start-1 size-7/8 self-center justify-self-center stroke-white group-has-disabled:stroke-{gray}-950/25 dark:group-has-disabled:stroke-white/25">
    <path d="M3 8L6 11L11 3.5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-not-has-checked:opacity-0" />
    <path d="M3 7H11" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-not-has-indeterminate:opacity-0" />
  </svg>
</span>
```

**Radio**

```html
<span class="group inline-grid size-4 grid-cols-1">
  <input type="radio" class="col-start-1 row-start-1 appearance-none rounded-full border border-{gray}-300 bg-white checked:border-{brand} checked:bg-{brand} focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-{brand} disabled:border-{gray}-300 disabled:bg-{gray}-100 dark:border-white/10 dark:bg-white/5 dark:checked:border-{brand} dark:checked:bg-{brand} forced-colors:appearance-auto" />
  <span class="pointer-events-none col-start-1 row-start-1 size-[round(down,40%,1px)] self-center justify-self-center rounded-full bg-white group-not-has-checked:opacity-0 group-has-disabled:bg-{gray}-400 dark:group-has-disabled:bg-white/25"></span>
</span>
```

**Toggle**

```html
<div class="group relative inline-flex w-9 shrink-0 rounded-full bg-{gray}-200 p-0.5 inset-ring inset-ring-{gray}-900/5 outline-offset-2 outline-{brand}-600 transition-colors duration-200 ease-in-out has-checked:bg-{brand}-600 has-focus-visible:outline-2 dark:bg-white/5 dark:inset-ring-white/10 dark:outline-{brand}-500 dark:has-checked:bg-{brand}-500">
  <span class="aspect-square w-1/2 rounded-full bg-white shadow-xs ring-1 ring-{gray}-900/5 transition-transform duration-200 ease-in-out group-has-checked:translate-x-full"></span>
  <input type="checkbox" class="absolute inset-0 size-full appearance-none focus:outline-hidden" />
</div>
```

To centre a checkbox or radio on its text's first line, wrap it in an element with `h-lh items-center` and the matching `text-*` size. Never put `h-lh` on the `inline-grid` wrapper, and never use top margins.

## Behaviour and validation

- Keep native submission: Enter submits from single-line fields and inserts a newline in a `<textarea>`. Add ⌘/Ctrl+Enter for a textarea only where it matches the product and goes through the same submit path.
- Submit stays enabled until the request starts, then disables, shows a spinner and keeps its label. Never disable it until the form is valid. A disabled button is not duplicate protection; make retryable submissions idempotent at the server.
- Accept free text and validate afterwards; never block typing. Submission reveals a complete validation summary; focus moves to it, each item links to its field, and inline errors stay too. Early field validation may supplement it.
- Each error sits below its field, joined with `aria-describedby`, the field marked `aria-invalid`. A network or permission failure gets its own recovery message.
- Normalise whitespace only where it means nothing; passwords, code and prose keep theirs.
- Inputs survive hydration without losing focus or value, and work with password managers and pasted one-time codes.
- Warn before abandoning meaningful unsaved work, not trivial or recoverable state.
