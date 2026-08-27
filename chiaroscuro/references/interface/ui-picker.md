# Interface: Page-Direction Picker

Use this only for Chiaroscuro's page-directions mode: a complete route, page, or full-screen workflow without a settled direction. It owns generation, rendered comparison, selection, fallback, and cleanup.

## The Set

Produce six rendered states of the same page:

1. the current page, labeled `Current`; for a new route with no prior page, a conservative baseline built from the existing product system;
2. five new, genuinely different directions.

All six share content, data, state, events, validation, and downstream behavior. Do not fork API calls, data loaders, mutations, or business logic to make directions. Change presentation structure, hierarchy, typography, color, density, and interaction treatment.

Every direction must communicate the complete page hierarchy and core path. It may defer production hardening until selection, but it cannot be a fragment, mood board, or decorative hero standing in for the page.

Name directions by their visible idea, not `A`, `B`, or abstract adjectives. The labels shown in the picker must match the labels used in the selection question.

## Start Clean

Before a new round:

- use the currently selected page as the baseline;
- remove stale rejected branches, wrappers, attributes, `hidden` states, scripts, imports, and suppressions;
- confirm the baseline path still works;
- keep a single source for shared content and behavior.

## Mark Up the Directions

Keep direction code in the existing route and component structure. A local presentation switch is acceptable; a standalone fake preview app is not.

Use the picker attributes where the framework can safely render all directions in one page:

```tsx
<div data-uidotsh-pick="Page direction" className="contents">
  <div data-uidotsh-option="Current" className="contents">...</div>
  <div data-uidotsh-option="Working ledger" className="contents" hidden>...</div>
  <div data-uidotsh-option="Material index" className="contents" hidden>...</div>
</div>
```

- Apply `contents` only when it preserves valid semantics and layout. Otherwise place the attributes on existing suitable elements.
- Exactly one direction begins visible.
- Keep IDs unique even while hidden alternatives are mounted.
- Do not duplicate expensive effects merely to keep hidden directions alive. Lift behavior above the presentation choice or render the active presentation from shared state.

If mounting every direction would violate framework semantics, create a development-only presentation switch at the route boundary. Preserve the same labels and cleanup contract.

## Inject the Picker Safely

When using the `data-uidotsh-*` mechanism, load `https://ui.sh/ui-picker.js` exactly once in the shared root with the framework's supported script facility:

- Next.js: `next/script` in the root layout.
- TanStack Router: the root route's supported head/script configuration.
- Nuxt: `useHead` in `app.vue` or a shared layout.
- Vite, Laravel, or plain HTML: once in the shared document immediately before `</body>`.

Do not add a raw script to a leaf component. Make injection idempotent. If a content-security policy or offline environment blocks the script, use the route-level switch or the fallback below.

## Review Before Asking

Exercise every direction in the running app before presenting it:

- core hierarchy and path are visible;
- content and behavior match the baseline;
- desktop and mobile are legible;
- no direction creates obvious overflow, duplicate IDs, broken semantics, console errors, or failed requests;
- labels accurately describe the rendered choices.

This is exploration, so avoid polishing six production implementations. Do enough to make the choice real and comparable.

## One Selection Pause

After browser review, pause exactly once. Present all five new directions and `Current` in one structured selection. Use a native structured-question tool only when it can represent every choice; otherwise ask one concise numbered question in chat. Do not split selection across questions or ask a chain of aesthetic questions before or after it.

If the app cannot run, present screenshots when possible. If neither preview nor screenshots are possible, present concise descriptions of all six directions in the same structured selection. Keep implementing after the user chooses.

## Finalize and Remove the Picker

After selection:

1. keep the selected presentation;
2. remove the other five directions;
3. remove picker scripts before removing now-unused script imports;
4. remove all `data-uidotsh-pick`, `data-uidotsh-option`, `hidden`, temporary switch state, wrappers, comments, and suppressions;
5. remove dead styles, components, imports, and dependencies;
6. production-harden the selected path;
7. run browser verification again.

Search for `uidotsh`, direction labels, temporary switch names, and picker-script URLs. Final source must contain no rejected code or comparison scaffolding.
