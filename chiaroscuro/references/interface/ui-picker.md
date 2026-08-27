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

## Build the Directions

Keep direction code in the existing route and component structure. Use a local presentation switch; a standalone fake preview app is not.

Render the active presentation from shared data, state, events, validation, and mutations:

```tsx
const directions = {
  current: CurrentDirection,
  ledger: WorkingLedgerDirection,
  index: MaterialIndexDirection,
}

const Direction = directions[activeDirection]
return <Direction model={sharedModel} actions={sharedActions} />
```

- Exactly one direction is mounted at a time unless side-by-side review genuinely helps.
- Keep the presentation key in local development state or a temporary URL parameter so refresh and screenshot review remain practical.
- Do not duplicate effects, API calls, loaders, or mutations. Lift behavior above the presentation choice.
- Keep direction labels and keys local to the temporary exploration code.

## Mount a Local Development Picker

Add a small, accessible picker component at the route or shared-layout boundary used by the exploration. It should:

- render only in the local development environment;
- use a native `<select>` or ordinary buttons with visible labels and keyboard support;
- update the local presentation key without resetting shared state;
- stay outside the page's layout flow so it does not alter the direction being judged;
- identify itself clearly as temporary review tooling.

Use the framework's normal local component and state mechanisms. Do not fetch, inject, or execute a remote picker script, and do not add a picker dependency for temporary exploration.

If the app cannot safely mount development tooling, use screenshots or the structured fallback rather than weakening the application's content-security policy or production boundary.

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
3. remove the local picker component, presentation map, temporary URL parameter, and development guard;
4. remove temporary switch state, wrappers, comments, and suppressions;
5. remove dead styles, components, imports, and dependencies;
6. production-harden the selected path;
7. run browser verification again.

Search for `DirectionPicker`, the temporary presentation key or URL parameter, all direction labels, and rejected component names. Final source must contain no rejected code or comparison scaffolding.
