# Interface: Interactions

## Interactive States

Design the states that apply to each interactive element; do not leave browser, async, or validation states to chance:

| State | When | Tailwind Treatment |
|-------|------|-------------------|
| **Default** | At rest | Base styling |
| **Hover** | Pointer over (not touch) | `hover:bg-gray-100` (v4 gates it to hover-capable pointers) |
| **Focus** | Keyboard/programmatic focus | `focus-visible:ring-2 focus-visible:ring-offset-2` |
| **Active** | Being pressed | `active:scale-[0.97]` |
| **Disabled** | Not interactive | `disabled:opacity-50 disabled:pointer-events-none` |
| **Loading** | Processing | Spinner, skeleton, `aria-busy="true"` |
| **Error** | Invalid state | `aria-invalid:border-red-500` |
| **Success** | Completed | Green check, confirmation |

Common miss: Designing hover without focus, or vice versa. Keyboard users never see hover states.

## Touch Targets

Canonical touch-target spec for this skill.

- MUST: On coarse pointers (touch), interactive targets are at least 44×44 CSS pixels, inclusive of invisible hit padding. A smaller visual control is fine when its full interactive area meets the minimum.
- MUST: When the visual element is smaller than 44px, keep it visually small but expand the hit area without overlapping neighboring targets:

```jsx
<button className="relative">
  <span
    className="absolute top-1/2 left-1/2 size-[max(100%,2.75rem)] -translate-1/2 pointer-fine:hidden"
    aria-hidden="true"
  />
  <Icon className="size-4" />
</button>
```

`2.75rem` = 44px. `pointer-fine:hidden` can remove the extra area for a fine pointer when neighboring controls need the space.

## Tap and Gesture Feel

- MUST: Show press feedback on pointer-*down*, commit the action on pointer-*up*. Waiting for `click` to show any feedback feels dead
- MUST: Allow cancel-by-dragging-away - moving off the target before release aborts the tap, moving back re-arms it (native `:active` + `click` behave this way; custom pointer-event handlers must reproduce it)
- SHOULD: Require ~10px of movement (hysteresis) before committing a drag to a direction; below that, treat the gesture as a tap
- SHOULD: For custom gestures, track plausible directions from the first move and cancel alternatives once intent is clear. End-state-only recognizers discard the continuous input needed for direct feedback; `zoetrope` covers gesture craft.
- SHOULD: Only pay the double-tap disambiguation delay (which delays every single tap) where double-tap genuinely exists

## Input

- MUST: `text-base` minimum on mobile inputs (prevents iOS zoom)
- MUST: `touch-manipulation` on controls (prevents double-tap zoom)
- SHOULD: `interactive-widget=resizes-content` in the viewport meta as progressive enhancement, so the on-screen keyboard resizes the layout where supported. Safari ignores it; keep fixed bottom actions usable when the keyboard overlays them
- NEVER: Disable zoom with `maximum-scale` or `user-scalable`

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content">
```

Global in CSS:
```css
@layer base {
  * { -webkit-tap-highlight-color: transparent; }
}
```

## Hover States

- MUST: Gate hover styles:

```jsx
<button className="hover:bg-gray-100">
  {/* Tailwind v4 wraps hover variants in @media (hover: hover). */}
</button>
```

For stricter gating, combine it with the built-in `pointer-fine:` variant.

- NEVER: Rely on hover for functionality - hover enhances only

## State & Navigation

- SHOULD: Put shareable or navigational state such as filters, tabs, and pagination in the URL. Use the project's router or a compatible helper rather than adding a library reflexively.
- MUST: Back and Forward restore meaningful state and scroll position.

## Feedback

- SHOULD: Optimistic UI with rollback on failure
- MUST: Use the project's accessible alert-dialog pattern for an irreversible action that requires confirmation; prefer undo for safe reversible actions.
- MUST: `aria-live="polite"` for toasts/validation
- SHOULD: Delay a spinner or skeleton by about 150-300ms, and once shown keep it for about 300-500ms, so fast responses don't flicker
- SHOULD: Ellipsis for follow-up actions ("Rename…", "Loading…")

## Time-Limited Actions

- MUST: Pause timers when tab hidden:

```js
document.addEventListener('visibilitychange', () => {
  if (document.hidden) pauseTimer();
  else resumeTimer();
});
```

## Drag/Scroll

- MUST: `overscroll-contain` in modals/drawers
- NEVER: Block page scrolling or pull-to-refresh with `touchmove` and `preventDefault`
- SHOULD: Build carousels as native scrolling tracks with `scroll-snap` and leave `touch-action` alone. Only when script implements the horizontal drag, set `touch-action: pan-y pinch-zoom` so vertical scrolling and zoom still work; reserve `touch-action: none` for surfaces that own every axis
- MUST: Every drag operation, such as reordering or resizing, has a single-pointer alternative (move buttons or a menu) and a keyboard path
- MUST: During drag, disable text selection with `select-none`. Keep the dragged item and its controls operable; `inert` belongs only on a decorative drag preview or on content the drag makes unavailable
- MUST: No dead zones - if it looks clickable, it is

### `inert` Attribute

Disables all interaction on element and children:

```jsx
<div inert={!isVisible}>{/* non-interactive when inert */}</div>
```

Use for: hidden panels, content behind modals, decorative drag previews, and content a drag makes unavailable.

## Tooltips

- SHOULD: Delay the first pointer-triggered tooltip enough to avoid accidental activation, then shorten or skip delay while traversing a related toolbar. Tune the delay to density and frequency rather than treating 200ms as universal.

## Menus

- SHOULD: Trigger on `mousedown` (not `click`)
- MUST: No dead zones between menu items - use `py-*` not `space-y-*`
- SHOULD: Keep a submenu open while the pointer travels diagonally towards it (a safe triangle); use the menu primitive's own handling rather than hand-rolling it

## Focus Rings

NEVER `outline: none` without replacement. Use `:focus-visible` to show focus only for keyboard:

```jsx
<button className="outline-hidden focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-gray-900">
```

Focus ring requirements:
- High contrast (3:1 minimum against adjacent colors)
- 2-3px thick
- Offset from element (not inside it)
- Consistent across all interactive elements

When validation, disclosure, route changes, or keyboard navigation moves focus, ensure the focused element is visible. Prefer native focus scrolling; use `scrollIntoView({ block: "nearest" })` only when nested scrolling or sticky chrome obscures it, and honor reduced motion for any smooth scroll.

## Overlays

- SHOULD: Use a modal only when the task must interrupt or needs protected focus. Otherwise choose by job: a side sheet for details or filters, a bottom sheet on phones, a popover for small click-triggered content, a hover card for passive previews
- MUST: Every dialog, sheet and drawer has a title, hidden with `sr-only` when the design shows none
- MUST: Render menus and popovers in the top layer or a portal when an ancestor clips overflow; no `z-index` escapes a clipping ancestor

## Native Popover API

For tooltips, dropdowns, and non-modal overlays, prefer native popovers:

```html
<button popovertarget="menu">Open menu</button>
<div id="menu" popover class="p-4 rounded-lg shadow-lg">
  <button>Option 1</button>
  <button>Option 2</button>
</div>
```

Benefits include top-layer stacking and built-in light-dismiss behavior. Native popover does not supply every component's semantics, focus policy, keyboard model, or accessible name; add and verify those for the actual pattern.

## Roving Tabindex

For component groups (tabs, menu items, radio groups), one item is tabbable; arrow keys move within:

```html
<div role="tablist">
  <button role="tab" tabindex="0">Tab 1</button>
  <button role="tab" tabindex="-1">Tab 2</button>
  <button role="tab" tabindex="-1">Tab 3</button>
</div>
```

Arrow keys move `tabindex="0"` between items. Tab moves to the next component entirely.

## Destructive Actions: Undo > Confirm

SHOULD prefer undo over confirmation dialogs - users click through confirmations mindlessly:

1. Remove from UI immediately
2. Show undo toast
3. Actually delete after toast expires

Use confirmation only when the consequence is irreversible, such as deleting an account or a batch that cannot be undone.

## Gesture Discoverability

Swipe-to-delete and similar gestures are invisible. Hint at their existence:

- **Partially reveal**: Show delete button peeking from edge
- **Onboarding**: Coach marks on first use
- **Alternative**: Always provide a visible fallback (menu with "Delete")

NEVER rely on gestures as the only way to perform actions.

## Interactive Elements

- SHOULD: `select-none` on buttons, tabs
- MUST: `pointer-events-none` on decorative overlays
- SHOULD: Toggles take effect immediately (no confirmation)
- MUST NOT: Add `hover:*` states to non-interactive elements - reserve them for buttons, links, and other genuinely clickable elements.
- MUST NOT: Add `transition-*` for hover color or background changes on non-control elements (cards, rows, list items, static surfaces) - reserve transitions there for elements that actually move or transform, and let color swaps be instant. Interactive controls (buttons, links, form inputs) may use precise `transition-colors`/`transition-shadow` on hover/focus, per `buttons.md` and `forms.md`.
