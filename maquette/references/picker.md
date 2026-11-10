# The picker

`DirectionPicker` is review tooling, not a contestant. It looks the same in every project: a dark floating pill that works over any page, light or dark.

Contents: Behaviour · Framework gotchas · Markup and styles · Compare mode

## Behaviour

- **Guard:** `process.env.NODE_ENV === 'development'` in Next.js, `import.meta.env.DEV` in Vite.
- **URL key `maquette`:** `?maquette=ledger`, so refreshes, screenshots and links land on the same direction. Absent selects `current`; `all` is compare mode (component or region only). Any other value renders a tooling error naming the valid keys, never an undefined component.
- Switch with `history.replaceState`, without a reload and without resetting shared state.
- One `<button type="button">` per direction with `aria-pressed`. Without `type="button"` a picker inside a form submits it.
- `[` and `]` step through the set; `H` hides the picker for screenshots. Ignore keys typed into fields (see the handler).
- Fixed at bottom centre, outside the layout flow. When the piece itself lives there (a toast stack, a bottom sheet, a dock), add the `top` class.
- Past four directions, use the `<select>` form below.

## Framework gotchas

- **Next.js App Router:** keep the selection in a small Client Component; pass server-rendered parts in as props or slots. `useSearchParams` observes `replaceState`. On a prerendered route, wrap the component that calls `useSearchParams` in `Suspense` or the build fails.
- **Vite and plain React:** `replaceState` does not re-render; update state and URL together.
- **SSR reading `location` directly:** render `Current` on the server and first client pass, then apply the URL selection after hydration.

```ts
function onKeyDown(event: KeyboardEvent) {
  if (event.defaultPrevented || event.isComposing) return
  if (event.metaKey || event.ctrlKey || event.altKey) return
  const target = event.target
  if (target instanceof HTMLElement && (target.isContentEditable || target.closest('input, textarea, select'))) return
  if (event.key === ']') select(keys[(keys.indexOf(active) + 1) % keys.length])
  else if (event.key === '[') select(keys[(keys.indexOf(active) - 1 + keys.length) % keys.length])
  else if (event.key === 'h' || event.key === 'H') setHidden((hidden) => !hidden)
}
```

`keys` is the direction keys in picker order, plus `all` where compare applies. `select` writes the URL and the selection together.

## Markup and styles

```tsx
<nav className="maquette-picker" aria-label="Design directions (temporary)" hidden={hidden}>
  {keys.map((key) => (
    <button key={key} type="button" aria-pressed={key === active} onClick={() => select(key)}>
      {labels[key]}
    </button>
  ))}
</nav>
```

Past four directions:

```tsx
<nav className="maquette-picker" aria-label="Design directions (temporary)" hidden={hidden}>
  <select aria-label="Direction" value={active} onChange={(event) => select(event.target.value)}>
    {keys.map((key) => (
      <option key={key} value={key}>{labels[key]}</option>
    ))}
  </select>
</nav>
```

`labels` maps each key to its direction name, with `all` labelled `Compare`.

```css
.maquette-picker {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2147483647;
  display: flex;
  gap: 2px;
  max-width: calc(100vw - 32px);
  padding: 4px;
  overflow-x: auto;
  border-radius: 999px;
  background: rgb(10 10 10 / 0.88);
  box-shadow: inset 0 0 0 1px rgb(255 255 255 / 0.1), 0 8px 24px rgb(0 0 0 / 0.24);
  font: 500 13px/1 system-ui, sans-serif;
}

.maquette-picker[hidden] { display: none; }
.maquette-picker.top { bottom: auto; top: 24px; }

.maquette-picker button,
.maquette-picker select {
  all: unset;
  flex: none;
  min-height: 44px;
  box-sizing: border-box;
  padding: 0 14px;
  display: flex;
  align-items: center;
  border-radius: 999px;
  color: rgb(255 255 255 / 0.6);
  cursor: pointer;
}

.maquette-picker select { color: #fff; }
.maquette-picker option { color: initial; }
.maquette-picker button:hover { color: rgb(255 255 255 / 0.9); }
.maquette-picker button[aria-pressed='true'] { background: rgb(255 255 255 / 0.14); color: #fff; }
.maquette-picker :focus-visible { outline: 2px solid rgb(255 255 255 / 0.7); outline-offset: 2px; }
```

`all: unset` keeps the project's global button and select styles out. In plain HTML or another framework, keep the class names and structure.

## Compare mode

`?maquette=all` renders every direction, `Current` first, in a grid of labelled cells:

- each cell is the width the piece really renders, so spacing and scale stay honest;
- cells share one model and one set of actions;
- every cell renders the same tree, so hard-coded `id`s collide; generate them per instance (`useId` in React);
- below 640px the grid is one column.

Compare is for spotting differences; judge the finalists by switching at full size.
