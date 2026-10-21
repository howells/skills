---
name: chiaroscuro
description: "Design and build polished web UI in Tailwind v4, or rescue a screen that looks messy, generic or unfinished. Use when an interface should look gorgeous. Not for page directions (`maquette`), app shells (`armature`), screen sizes (`reflow`), Paper mockups (`paste-up`) or QA (`fieldtest`)."
---

# Chiaroscuro

Take a user-facing web interface from request to finished, working implementation. Work in the product's language, use its real content and behaviour, and give the result a specific visual point of view without adding furniture or exposing the system underneath.

Use it to build a component, region or page, or to raise an existing interface's hierarchy, finish and polish. It produces one finished design. Other jobs have their own skills:

- several page directions to choose between: `maquette`;
- a scrolling-document app turned into a fixed app shell: `armature`;
- a responsive pass across small laptops, tablets and phones: `reflow`;
- a mockup in Paper: `paste-up`.

The work is complete when the requested UI works in context, looks right on desktop and on a phone, and existing behaviour is intact.

## Hard Rules

These hold for every part of the work, including anything handed to a helper. Styling the product already has is not an exception; fix it inside the scope and mention it outside. Only an explicit instruction from the user overrides a rule.

1. **No small caps, tracked uppercase or decorative mono.** No eyebrows, kickers, section labels, chips or table headings in capitals. Mono is for literal code, identifiers and values whose characters need inspecting, never for labels or headings. Proper acronyms keep their capitals.
2. **No prose where interface belongs.** A paragraph explaining a screen means the screen has failed. Replace it with a label, a control, a value or nothing. In product UI, headings name things; they do not headline them or introduce a section. Keep only consent, constraints and error recovery.
3. **Four to six type styles, in chosen faces.** Use the product's named roles. A new size or weight needs a job no existing role does. A new face comes from `typecase`'s font recommendations and never from its never-use list; Instrument Serif is the first name on that list.
4. **Reuse before you build.** Find the existing component, shell, header or control that does the job, in this product and in any package or project the user has pointed to, and use it. A second version of an existing control is a defect.
5. **One of each.** One corner-radius scale with concentric nesting, one icon family at one stroke weight, one control height per density.
6. **Touch targets at least 44 by 44 CSS pixels.**
7. **Look at it before calling it done.** Use the path in a real browser, then look at each whole screen on desktop and on a phone as the user would. Static checks show neither that it works nor that it looks right.

## Work End to End

### 1. Inspect the Product and Task

Read project instructions, product and brand documents, the relevant route and components, existing tokens, and the runnable interface. Identify:

- the user's job and core path;
- real content, data, and states;
- the established shell, grid, components, and vocabulary;
- technical constraints and the styling system;
- what must remain unchanged.

Do not begin by inventing a visual theme in isolation. You should be able to describe the user's task, the product constraints and the interface boundary in a few concrete sentences.

For a flow, walk one concrete scenario before drawing its screens: what the person supplies, what must stay unchanged, what they choose, and what result they leave with. Keep inputs with different meanings distinct. Establish the useful end state, then work through the transitions that reach it. For a contained edit, check its place in the existing path; do not reopen the whole product.

### 2. Load Only the Relevant References

Read [`references/interface/index.md`](references/interface/index.md) and open only the branch needed for this task.

- For motion, begin with [`references/interface/animation.md`](references/interface/animation.md). If installed, use `zoetrope` for specialist motion craft, and the library's own documentation for current API facts.
- When writing or changing UI copy, use `signage` if installed, before the words shape the layout. Otherwise apply its core test here: would you say this to someone in the audience and be understood without explaining it? Keep labels concrete and remove prose that substitutes for a control.
- For charts or a collection of data visualisations, load [references/interface/charts.md](references/interface/charts.md).

The reference files are a router, not a checklist. Never load every rule file by default.

### 3. Decide the Look

Settle the product's shape before its styling. A focused, single-purpose experience puts its subject on screen and little else: no header, navigation or title by default. A persistent shell earns its place only when people move between places or work across panes.

Then decide the look in a sentence or two: hierarchy, typography, colour behaviour, density and interaction temperament. It should be specific enough to constrain implementation, not a mood-board slogan.

Compose the phone as its own design, not the desktop squeezed down: the primary action within thumb reach, sheets rather than centred modals, media full-bleed, fewer controls on screen at once and a smaller display size.

Carry the few defining decisions from a supplied design or accepted review into implementation: what leads, what stays quiet, what remains visible, and how actions relate to supporting information. Component defaults must preserve these decisions; a convenient variant is not a reason to change the composition.

When borrowing another interface's aesthetic, name the features being borrowed, such as typography, texture, density or control treatment. Keep the target product's tasks, objects and state transitions intact; visual resemblance doesn't establish that the original app still works.

### 4. Implement in Tailwind v4

Use the project's components and conventions before creating new primitives. Express visual decisions through Tailwind v4 utilities, variants, and `@theme` tokens rather than scattered arbitrary values. Where adopting v4 would change package manifests, build configuration or the global CSS entry point, recommend the migration and ask first; a contained UI request never becomes a repository-wide styling migration.

Build stable states, not just a stable first frame. Prevent unintended layout shift: reserve room for labels and controls that arrive late, draw state-dependent edges as rings or inset shadows rather than borders, keep controls in a row at one height, and give images a fixed ratio. Keyboard actions keep native form semantics; focus stays visible and moves into view; clipping never creates an accidental scroll container.

### 5. Exercise and Refine the Rendered Experience

Run the real app at the exact route, viewport and state being changed, and complete the core user path. Check, as relevant:

- desktop and phone layouts;
- keyboard and pointer operation;
- focus order, focus visibility, semantics, and the accessibility tree;
- long, empty, loading, failure, and success states;
- console errors and failed network requests;
- persistence and the downstream effect of the user's action;
- motion interruption and reduced-motion behaviour;
- contrast and real raster assets in dark mode.

**Zoom out and reflect.** After the first complete composition and after material changes, look at the whole viewport and successive states together. What draws the eye first? Is that the user's subject or the controls around it? Is the next action apparent? Is the biggest visible problem compositional? Fix that before polishing details, and recompose when local fixes have left the whole incoherent. Passing technical checks does not answer these questions.

Use `fieldtest` for a deeper browser-QA pass and `reflow` for a full pass across screen sizes, when installed and the risk warrants it.

### 6. Clean Up and Report

Remove temporary wrappers, hidden branches, suppressions and unused imports introduced by the work. Report what changed, what you exercised and what you looked at, and any honest limitation. Never claim the browser pass when only static checks ran.

## Taste and Craft Guardrails

- Use authentic product content. Placeholder slogans and generic dashboard data conceal design problems.
- Use the product's own imagery as one coherent set, consistent in light, ratio and crop. No image is better than stock filler or the wrong object.
- Use sentence case for ordinary UI text. Aligned figures need tabular numerals in the body font, not mono.
- Icons need accessible names or adjacent labels when their meaning is not obvious.
- Reach touch targets with invisible padding rather than making every visual control bulky.
- Align optical shapes by eye where mathematical centering looks wrong.
- Avoid generic AI defaults: stacked rounded cards, gratuitous gradients, glowing borders, ornamental pills, oversized hero copy, editorial headlines in product UI, and decorative status chrome.
- In dark mode, rebuild contrast relationships rather than invert colours. Use dark-mode variants for raster assets when the light asset does not hold up.
- Motion needs a purpose, an origin, an interruption behaviour, a frequency budget, and a reduced-motion treatment. Fast feedback and perceived speed matter more than spectacle.

## Specialist Boundaries

Chiaroscuro remains usable on its own. A specialist adds depth but never carries the Hard Rules for you. Delegate only when a specialist skill is installed and the task benefits from depth:

- `typecase` for the type ramp and its scanner;
- `componentize` for a reuse and duplication audit;
- `zoetrope` for building, reviewing or finding motion, including gestures;
- `signage` when writing or changing UI copy, as directed in step 2;
- `fieldtest` for evidence-heavy browser QA;
- `reflow` for a responsive pass across every view;
- `armature` when the app needs a fixed shell with panes before it needs polish;
- `maquette` when the user wants several page directions to choose between;
- `paste-up` for any work in a Paper file;
- `dark-mode-image`, `canonicalize-tailwind`, `markup-from-image`, `prototype`, or `pick-ui-library` for their narrow utilities.

Do ordinary end-to-end interface work here. Do not force a specialist dependency, a saved design spec, a wireframe, or an approval pause unless the user asks for one.
