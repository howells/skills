# Interface: In-Browser Variant Picker

Covers: previewing and choosing between multiple UI variants live in the browser using a picker toolbar.

Use this when the design routes or alternatives from the SKILL workflow should be compared *in the running app* rather than in chat or ASCII. The picker lets the user toggle between annotated variants in the real rendered UI, then keeps only the chosen one.

## When To Use

- The project runs in a browser and the user wants to see real, rendered variants side by side.
- You are presenting alternatives for a hero, section, layout, or component and want a live A/B/C toggle.

Skip it for ASCII-only exploration, non-browser targets, or when the user already knows the direction.

## Reset First

If the picker was used earlier in the same project, clean up before a new round:

- Use the currently selected/visible UI as the baseline.
- Remove stale artifacts: old unselected branches, leftover `hidden` attributes, picker wrappers no longer needed.
- Keep exactly one toolbar script tag if still comparing; remove duplicates.
- Each area must be back to one clean implementation before generating new options.

## Annotate Variants

Do all variant work in the existing source files — never a standalone preview file.

1. Give each decision a human-readable label (`Hero style`, `Pricing layout`).
2. Wrap the decision: `data-uidotsh-pick="Human readable label"`.
3. Wrap each option: `data-uidotsh-option="Human readable option"`.
4. Apply the Tailwind `contents` class to wrapper and option nodes so they don't affect layout.
5. Exactly one option is visible; all others get `hidden`.
6. When the current implementation is included, it must be option 1 and carry `(current)` in its label.

```html
<div data-uidotsh-pick="Hero style" class="contents">
  <div data-uidotsh-option="Minimal (current)" class="contents">...</div>
  <div data-uidotsh-option="Bold" class="contents" hidden>...</div>
  <div data-uidotsh-option="Editorial" class="contents" hidden>...</div>
</div>
```

```tsx
<div data-uidotsh-pick="Hero style" className="contents">
  <div data-uidotsh-option="Minimal" className="contents">...</div>
  <div data-uidotsh-option="Bold" className="contents" hidden>...</div>
</div>
```

## Inject The Toolbar (once)

After variants exist, inject the script once in the shared root layout, idempotently — never in leaf components, never duplicated. Prefer framework-native script APIs.

- **Next.js**: `next/script` (a plain `<script>` in JSX can fail to execute until a full refresh in dev).

  ```tsx
  import Script from 'next/script'

  export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
      <html lang="en">
        <body>
          {children}
          <Script src="https://ui.sh/ui-picker.js" />
        </body>
      </html>
    )
  }
  ```

- **TanStack**: inject via the `scripts` array in the `head` option of `createRootRoute` in `src/routes/__root.tsx` — not a raw `<script>` in markup.
- **Nuxt**: `useHead` in `app.vue` or a layout file.
- **Vite / Laravel / plain HTML**: inject once before `</body>` in `index.html` / `resources/views/layouts/app.blade.php` / the shared root shell.

  ```html
  <script src="https://ui.sh/ui-picker.js"></script>
  ```

## Choose And Finalize

1. Let the user preview in-browser. If the toolbar can't load (CSP/offline), skip preview and ask for the selection in chat using the labels.
2. Ask for the selection with the question tool — one clear question per decision, option labels matching the picker labels, custom input left enabled. Keep the `(current)` option first when present.
3. After selection:
   - Keep only selected variants; remove unselected ones and now-unneeded picker wrapper attributes, `hidden` attributes, and empty wrappers.
   - Remove temporary comments/suppressions used only for scaffolding.
   - During cleanup, remove picker script usage *first*, then any now-unused script imports (ideally in one file edit) so intermediate saves never leave an invalid state.
   - Keep a single toolbar script tag if another comparison round is coming; otherwise remove the script and all remaining picker-only scaffolding.

## Verify

- Check desktop and mobile.
- No broken semantics, no duplicate `id`s across surviving markup.
- No stale picker artifacts remain unless intentionally staging a fresh round.
- Run lint/typecheck/tests when available.
