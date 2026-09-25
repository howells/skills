---
name: chiaroscuro
description: "Design and build polished web UI in Tailwind v4. Not for page directions (`maquette`), app shells (`armature`), screen sizes (`reflow`) or QA (`fieldtest`)."
---

# Chiaroscuro

Take a user-facing web interface from request to finished, browser-verified implementation. Work in the product's language, use its real content and behavior, and give the result a specific visual point of view without adding furniture or exposing the system underneath.

State at the start that you are using the `chiaroscuro` skill and whether you are building new UI or refining an existing one.

Use it to build a component, region or page in a supplied or evident direction, or to raise an existing interface's hierarchy, finish and polish. It produces one finished direction. Other jobs have their own skills:

- five rendered directions to choose between: `maquette`;
- a scrolling-document app turned into a fixed app shell: `armature`;
- a responsive pass across small laptops, tablets and phones: `reflow`;
- a mockup in Paper before any code: `paste-up`.

The work is complete when the requested UI works in context, the affected user path has been exercised in a browser, and any existing behaviour is intact.

## Hard Rules

These hold wherever the work happens: in code, in a Paper file and in any brief handed to a helper. Styling the product already has is not an exception; fix it inside the scope and report it outside. Only an explicit instruction from the user overrides a rule.

1. **No small caps, tracked uppercase or decorative mono.** No eyebrows, kickers, section labels, chips or table headings in capitals. Mono is for literal code, identifiers and values whose characters need inspecting, never for labels or headings. Proper acronyms keep their capitals.
2. **No prose where interface belongs.** A paragraph explaining a screen means the screen has failed. Replace it with a label, a control, a value or nothing. Keep only consent, constraints and error recovery.
3. **Four to six type styles.** Use the product's named roles. A new size or weight needs a job no existing role does.
4. **Reuse before you build.** Find the existing component, shell, header or control that does the job, in this product and in any package or project the user has pointed to, and use it. A second version of an existing control is a defect.
5. **One of each.** One corner-radius scale with concentric nesting, one icon family at one stroke weight, one control height per density.
6. **Touch targets at least 44 by 44 CSS pixels.**
7. **Verified means used and looked at.** "Works" means you completed the path in a browser, or walked a mockup's boards in order. "Looks right" means you then viewed each whole screen as the user sees it. Report the two separately, and never claim either from static checks.

Paste this block, word for word, into any brief that hands part of the work to another agent, reviewer or art director, and check what comes back against it before accepting it.

## Work End to End

### 1. Inspect the Product and Task

Read project instructions, product and brand documents, the relevant route and components, existing tokens, and the runnable interface. Identify:

- the user's job and core path;
- real content, data, and states;
- the established shell, grid, components, and vocabulary;
- technical constraints and the styling system;
- what must remain unchanged.

Do not begin by inventing a visual theme in isolation. Inspection is complete when you can describe the user's task, the product constraints, and the interface boundary in a few concrete sentences.

For a flow, walk one concrete scenario before drawing its screens: what the person supplies, what must stay unchanged, what they choose, and what result they leave with. Keep inputs with different meanings distinct. Establish the useful end state, then work through the transitions that reach it. For a contained edit, check its place in the existing path; do not reopen the whole product.

### 2. Load Only the Relevant References

Read [`references/interface/index.md`](references/interface/index.md) and open only the branch needed for this task.

- For motion, begin with [`references/interface/animation.md`](references/interface/animation.md). If installed, use `zoetrope` for specialist motion craft, and the library's own documentation for current API facts.
- When writing or changing UI copy, use `signage` if installed, before the words shape the layout. Otherwise apply its core test here: would you say this to someone in the audience and be understood without explaining it? Keep labels concrete and remove prose that substitutes for a control.

The reference files are a router, not a checklist. Never load every rule file by default.

### 3. Set the Direction

State the chosen direction briefly: hierarchy, typography, color behavior, density, and interaction temperament. A direction should be specific enough to constrain implementation, not a mood-board slogan.

Carry the few defining decisions from the supplied design or accepted review into implementation: what leads, what stays quiet, what remains visible, and how actions relate to supporting information. Component defaults must preserve these decisions; a convenient variant is not a reason to change the composition.

### 4. Implement in Tailwind v4

Use the project's components and conventions before creating new primitives. Express visual decisions through Tailwind v4 utilities, variants, and `@theme` tokens rather than scattered arbitrary values.

Tailwind has a mechanical authorization boundary:

- Existing Tailwind v4 work is in scope.
- Converting touched UI files to an already-configured v4 system is in scope.
- If v4 adoption requires changing package manifests, build configuration, or the global CSS entry point, pause with a strong migration recommendation unless the user already authorized migration.
- Never turn a contained UI request into a repository-wide styling migration silently.

Build stable states, not just a stable initial frame. Dynamic geometry must not cause avoidable layout shift; keyboard actions must preserve native form semantics; focus must remain visible and move into view; clipping must not create accidental scroll containers; and interactive states must not jump because borders, labels, or controls appear late.

### 5. Exercise and Refine the Rendered Experience

Confirm the exact route, tab, viewport and state being judged. Run the real app and complete the core user path. Verify, as relevant:

- desktop and mobile layouts;
- keyboard and pointer operation;
- focus order, focus visibility, semantics, and the accessibility tree;
- long, empty, loading, failure, and success states;
- console errors and failed network requests;
- persistence and the downstream effect of the user's action;
- motion interruption and reduced-motion behavior;
- contrast and real raster assets in dark mode.

**Zoom out and reflect.** After the first complete composition and after material changes, inspect the whole viewport and successive states together. What draws the eye first? Is that the user's subject or the controls around it? Is the next action apparent? Does the result still express the agreed direction? If local fixes have left the whole incoherent, recompose before polishing more details. This is a brief part of the design work, not another report or approval round. Passing technical checks does not answer these questions.

Sweep the whole changed surface for Hard Rule 1, not only the part you were shown. In code, search the changed files and the shared components they render:

```sh
rg -n 'uppercase|small-caps|font-variant-caps|font-mono|tracking-wid|tracking-\[|letter-spacing' <changed paths>
```

Then confirm in the browser, since a shared component can reintroduce the treatment without a class in your files. In Paper, read the computed styles of the in-scope text nodes for transform, caps, letter spacing and mono families. Every hit is removed or kept as literal code, a value or an acronym. Check other consumers before editing a shared style.

Use `fieldtest` for a deeper browser-QA pass and `reflow` for a full pass across screen sizes, when installed and the risk warrants it. Tests support this pass; they do not replace it. Refine until the complete path is coherent, responsive, accessible, and visually resolved.

### 6. Clean Up and Report

Remove temporary wrappers, hidden branches, suppressions and unused imports introduced by the work. Re-run the relevant checks and the complete user path.

Report the direction, what changed, verification performed, and any honest limitation. Do not claim browser verification when only static checks ran.

Before reporting completion, confirm that:

- each Hard Rule holds across the changed surface, and the report gives the Rule 1 sweep's count of hits removed and kept;
- every component you created is listed with the existing one you checked first;
- every label, heading, button, status line, and empty state passes the audience-language test in step 2;
- the primary task is apparent without explanatory scaffolding;
- real content and adverse states do not break the hierarchy;
- keyboard, pointer, and touch behavior agree where they should;
- temporary scaffolding is gone;
- the implementation still follows the project's architecture and vocabulary.

## Taste and Craft Guardrails

- Use authentic product content. Placeholder slogans and generic dashboard data conceal design problems.
- Use sentence case for ordinary UI text. Aligned figures need tabular numerals in the body font, not mono.
- Icons need accessible names or adjacent labels when their meaning is not obvious.
- Reach touch targets with invisible padding rather than making every visual control bulky.
- Align optical shapes by eye where mathematical centering looks wrong.
- Avoid generic AI defaults: stacked rounded cards, gratuitous gradients, glowing borders, ornamental pills, oversized hero copy, and decorative status chrome.
- In dark mode, rebuild contrast relationships rather than invert colors. Use dark-mode variants for raster assets when the light asset does not hold up.
- Motion needs a purpose, an origin, an interruption behavior, a frequency budget, and a reduced-motion treatment. Fast feedback and perceived speed matter more than spectacle.

## Specialist Boundaries

Chiaroscuro remains usable on its own. A specialist adds depth but never carries the Hard Rules for you: apply them here whether or not it runs. Delegate only when a specialist skill is installed and the task benefits from depth:

- `typecase` for the type ramp and its scanner;
- `componentize` for a reuse and duplication audit;
- `zoetrope` for building, reviewing or finding motion, including gestures;
- `signage` when writing or changing UI copy, as directed in step 2;
- `fieldtest` for evidence-heavy browser QA;
- `reflow` for a responsive pass across every view;
- `armature` when the app needs a fixed shell with panes before it needs polish;
- `maquette` when the user wants several page directions to choose between;
- `dark-mode-image`, `canonicalize-tailwind`, `markup-from-image`, `prototype`, or `pick-ui-library` for their narrow utilities.

Do ordinary end-to-end interface work here. Do not force a specialist dependency, a saved design spec, a wireframe, or an approval pause unless the user asks for one.
