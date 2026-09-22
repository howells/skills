---
name: maquette
description: "Render five page directions beside the current page, then build the chosen one. Not for a single direction (`chiaroscuro`)."
disable-model-invocation: true
---

# Maquette

A maquette is the small model a sculptor makes to choose a form before committing to the full piece. This skill does that for a page: the current page plus five genuinely different directions, rendered in the running app behind a temporary picker, one selection, then the chosen direction built properly and every rejected one removed.

State at the start that you are using the `maquette` skill.

Use it for a complete route, page or full-screen workflow whose direction is not settled. When the user supplied a direction, asked to match or extend an existing design, or scoped the work to a component or region, build one direction with `chiaroscuro` instead.

## 1. Inspect before drawing

Read the project instructions, the route and its components, the shell, the tokens and the real content. Write down in a few sentences who uses this page, what they are there to do, and what must stay unchanged. Every direction answers the same task with the same content; only presentation varies.

## 2. The set

Six rendered states of the same page:

1. the current page, labelled `Current`. For a new route with no prior page, build a conservative baseline from the product's existing shell, components and tokens;
2. five new directions that differ on purpose.

All six share content, data, state, events, validation and downstream behaviour. Never fork API calls, loaders, mutations or business logic to make a direction. Vary presentation structure, hierarchy, typography, colour, density and interaction treatment.

Every direction shows the complete page hierarchy and core path. It may leave production hardening until after selection, but it cannot be a fragment, a mood board or a decorative hero standing in for the page.

Name each direction by its visible idea, never `A`, `B` or an abstract adjective. The labels in the picker match the labels in the selection question.

## 3. Start clean

Before each round:

- use the currently selected page as the baseline;
- remove stale rejected branches, wrappers, hidden states, scripts, imports and suppressions from any earlier round;
- confirm the baseline path still works;
- keep one source for shared content and behaviour.

## 4. Build the directions

Keep direction code inside the existing route and component structure behind a local presentation switch. A standalone fake preview app is not acceptable.

```tsx
const directions = {
  current: CurrentDirection,
  ledger: WorkingLedgerDirection,
  index: MaterialIndexDirection,
}

const Direction = directions[activeDirection]
return <Direction model={sharedModel} actions={sharedActions} />
```

- Mount one direction at a time unless side-by-side review genuinely helps.
- Keep the presentation key in local development state or a temporary URL parameter so refresh and screenshots stay practical.
- Lift effects, API calls, loaders and mutations above the presentation choice.
- Keep direction labels and keys local to the temporary code.

## 5. Mount a local picker

Add a small accessible component named `DirectionPicker` at the route or layout boundary used by the exploration. It:

- renders only in local development;
- uses a native `<select>` or ordinary labelled buttons with keyboard support;
- changes the presentation key without resetting shared state;
- sits outside the page's layout flow, so it does not alter the direction being judged;
- identifies itself as temporary review tooling.

Never fetch or inject a remote picker script, and never add a dependency for it. If the app cannot safely mount development tooling, use screenshots or described options rather than loosening its security policy or production boundary.

## 6. Review before asking

Exercise every direction in the running app:

- the core hierarchy and path are visible;
- content and behaviour match the baseline;
- desktop and mobile are legible;
- no direction introduces overflow, duplicate IDs, broken semantics, console errors or failed requests;
- each label describes what is actually rendered.

This is exploration. Do enough to make the choice real and comparable, and no more.

## 7. One selection

Pause exactly once. Present `Current` and all five directions in one structured selection, using the host's structured-question tool when it can hold every option, otherwise one numbered question in chat. Never split the choice across questions or add aesthetic questions before or after it.

If the app cannot run, present screenshots. If neither preview nor screenshots are possible, present short descriptions of all six in the same selection.

## 8. Build the chosen direction and remove the rest

1. Keep the selected presentation.
2. Remove the other five directions.
3. Remove `DirectionPicker`, the presentation map, the temporary URL parameter and the development guard.
4. Remove temporary switch state, wrappers, comments and suppressions.
5. Remove dead styles, components, imports and dependencies.
6. Harden the selected path to production quality, including empty, loading, failure, keyboard, mobile and dark-mode states. Apply `chiaroscuro` for this when installed.
7. Verify the complete path again in the browser.

Search for `DirectionPicker`, the presentation key or URL parameter, every direction label and every rejected component name. The final source contains no rejected code and no comparison scaffolding.

## Report

Name the chosen direction, what changed, the verification performed, and any honest limitation. Do not claim browser verification when only static checks ran.
