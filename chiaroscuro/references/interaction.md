# Interaction and accessibility

Contents: states · touch and pointer · overlays, menus and tooltips · focus and keyboard · names and announcements · feedback and state.

## States

Design every state an element has; keyboard users never see hover.

| State | Treatment |
| --- | --- |
| Hover | `hover:` (v4 already gates it to hover-capable pointers); add `pointer-fine:` for stricter gating |
| Focus | `focus-visible:` ring |
| Active | press feedback on pointer-down, such as `active:scale-[0.97]`; never on a disabled control (`enabled:active:`) |
| Disabled | native `disabled`, styled explicitly |
| Loading | label and width unchanged, spinner, `aria-busy="true"` |
| Error | `aria-invalid:` styles |

- Hover only enhances. Nothing works by hover alone, and nothing static gets a `hover:` state.
- Static rows, cards and surfaces swap hover colour instantly. Controls may use `transition-colors` or `transition-shadow`, never `transition-all`.
- No dead zones: anything that looks clickable is, across its whole row. Menu items use `py-*`, not `space-y-*`, so the gaps are clickable.
- `select-none` on buttons and tabs; `pointer-events-none` on decorative overlays.

## Touch and pointer

- Expand a small visual control's hit area to 44px without overlapping its neighbours:

  ```jsx
  <button className="relative">
    <span aria-hidden="true" className="absolute top-1/2 left-1/2 size-[max(100%,2.75rem)] -translate-1/2 pointer-fine:hidden" />
    <Icon className="size-4" />
  </button>
  ```

- Show press feedback on pointer-down and commit on pointer-up. Dragging off the target before release cancels; dragging back re-arms. Native `:active` plus `click` does this; custom pointer handlers must reproduce it.
- Require about 10px of movement before committing a drag to a direction. Pay the double-tap delay only where double-tap exists.
- `touch-manipulation` on controls; `-webkit-tap-highlight-color: transparent` where a control draws its own pressed state.
- Never disable zoom (`maximum-scale`, `user-scalable`). Use `interactive-widget=resizes-content` in the viewport meta as progressive enhancement; Safari ignores it, so fixed bottom actions must survive the keyboard overlaying them.
- Carousels are native scrolling tracks with `scroll-snap`. Set `touch-action: pan-y pinch-zoom` only when script implements the horizontal drag. Never block page scroll or pull-to-refresh with `preventDefault` on `touchmove`.
- Every drag (reordering, resizing) has a single-pointer alternative and a keyboard path. Swipe actions always have a visible fallback, such as a menu item. During a drag, `select-none`; `inert` only on a decorative drag preview or content the drag makes unavailable.
- `overscroll-contain` on scrolling dialogs, drawers, menus and side panels.

## Overlays, menus and tooltips

- Use a modal only when the task must interrupt or needs protected focus. Otherwise: a side sheet for details or filters, a bottom sheet on phones, a popover for small click-triggered content, a hover card for passive previews.
- Prefer `<dialog>` with `showModal()`, which makes the background inert and handles Escape. Move focus in on open and return it to the trigger on close. Every dialog, sheet and drawer has a title, `sr-only` when the design shows none.
- The native `popover` attribute gives top-layer stacking and light dismiss, not semantics, focus policy or keyboard model; add those for the actual pattern.
- Menus open on `mousedown`. Submenus stay open while the pointer travels diagonally toward them; use the primitive's own handling.
- Tooltips delay before the first one opens, then open instantly while traversing a toolbar. No interactive content inside a tooltip, and no tooltip on a natively disabled control (it can't receive focus); put the reason beside it, or use `aria-disabled` so it stays focusable. Prefer inline help to tooltips.

## Focus and keyboard

- Never remove an outline without a replacement. Rings are 2-3px, offset, consistent, and reach 3:1 against every adjacent colour. A box-shadow ring needs a transparent outline beneath it so forced-colours mode still shows focus:

  ```css
  :focus-visible {
    outline: 2px solid transparent;
    outline-offset: 2px;
    box-shadow: 0 0 0 2px var(--background), 0 0 0 4px var(--ring);
  }
  ```

- A focused element is never hidden under sticky chrome. Prefer native focus scrolling; use `scrollIntoView({ block: "nearest" })` only when nested scrolling or sticky chrome hides it.
- Native elements first: `<button>` for actions, `<a href>` for navigation (so Cmd-click and middle-click work), never `<div onClick>`. Native controls already handle keys; adding handlers can double-fire.
- Composite widgets (tabs, menus, listboxes, radio groups) use roving tabindex: one item at `tabindex="0"`, arrows move within, Tab leaves. Where focus must stay in an input, as in a combobox, use `aria-activedescendant`. Never a positive tabindex.
- Client-side route changes reset nothing. Update `document.title` and move focus to the new view's `<h1>` or `<main>`.
- A skip link first when navigation precedes `<main>`; `scroll-margin-top` on anchored headings.

## Names and announcements

- Icon-only buttons get an `aria-label`, and a visible label's text starts the accessible name. Decorative elements get `aria-hidden`, never a focusable one or an ancestor of one.
- An HTML illustration that carries meaning gets `role="img"` and a name; otherwise its raw DOM is announced.
- Alt text by purpose: `alt=""` when decorative or named by adjacent text, the meaning when informative, the action when functional.
- `aria-describedby` carries field errors. `role="status"` carries non-urgent updates such as toasts and result counts; `role="alert"` only urgent errors. Render the live region empty first and then update its text, or it may not announce.
- Announce a changing count with its context ("3 items in cart") in one atomic message.
- Anything moving or updating on its own for more than five seconds has a pause control. Toasts carrying an action or an error stay until dismissed. Pause timers when the tab is hidden (`visibilitychange`).

## Feedback and state

- Acknowledge input immediately. Delay a spinner or skeleton by 150-300ms, and once shown keep it 300-500ms, so fast responses don't flicker.
- Optimistic updates only when failure can be reversed and pending state stays visible.
- Prefer undo to confirmation: remove at once, show an undo toast, delete when it expires. Confirm only the irreversible, through the project's alert dialog, never `confirm()`. Destructive actions are set apart and never the default.
- Toggles take effect immediately.
- Shareable state (filters, tabs, pagination, open panels) lives in the URL, through the project's router. Back and Forward restore it and the scroll position.
- Persist only state that should survive; not every accordion belongs in storage.
- Keyboard shortcuts for frequent actions, shown in tooltips (`Save (⌘S)`).
