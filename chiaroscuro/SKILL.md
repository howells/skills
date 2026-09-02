---
name: chiaroscuro
description: "Design, build and polish user-facing web interfaces with distinctive visual direction, Tailwind v4, responsive and accessible behavior, and browser verification. Use for a component, screen, page or app that needs visual direction or structural polish. Not for QA-only browser testing (`fieldtest`), reuse audits (`componentize`), interface copy (`signage`), or the type ramp (`typecase`)."
---

# Chiaroscuro

Take a user-facing web interface from request to finished, browser-verified implementation. Work in the product's language, use its real content and behavior, and give the result a specific visual point of view without adding furniture or exposing the system underneath.

State at the start that you are using the `chiaroscuro` skill and name the operating mode.

## The Standard

**Everything earns its place.** Every panel, label, divider, shadow, control, and typographic treatment must improve clarity, utility, hierarchy, affordance, state, navigation, or domain meaning. Remove what does not.

**Design the user's task.** Build the shortest legible path through the real job. Hide schemas, prompts, agent mechanics, API names, and implementation state behind user-centered nouns, verbs, and progressive disclosure.

**Build an interface, not an explanation.** Prefer controls, comparisons, tables, diagrams, and direct manipulation to paragraphs that describe what the interface should do. Use copy for orientation and consequence, not as a substitute for design.

**Make one system.** Reuse the product's shell, grid, components, tokens, content model, and interaction conventions. The result should belong to the product while still having a deliberate direction.

**Finish the path.** Empty, loading, failure, success, overflow, persistence, keyboard, mobile, and downstream states are part of the interface. A polished screenshot with an unfinished path is unfinished work.

## Choose the Operating Mode

Choose the smallest mode that covers the request:

- **Direct implementation** - a component, contained region, or work with a supplied direction. Produce one finished direction and implementation.
- **Page directions** - a new or redesigned complete route, page, or full-screen workflow without a settled direction. Render the current page as a baseline plus five new directions, then pause once for selection.
- **Design-only** - the user asks for direction, a wireframe, or a design spec without implementation. Produce only the requested artifact.
- **Structural polish** - an existing interface needs hierarchy, responsive behavior, accessibility, dark mode, or finish without a new visual concept. Preserve and refine the existing direction as one finished implementation across the complete path.

Do not enter page-directions mode when the user supplied a direction, asked to match or extend an existing design, requested one implementation, or scoped the work to a component or contained region.

### Mode Completion

Direct implementation and structural polish each produce one finished direction. They are complete when the requested UI works in context and the affected user path has been exercised.

Page directions proceed in two phases:

1. Exploration is complete when the baseline and five new directions are rendered, reviewed, and ready for one informed selection.
2. Delivery is complete only after selection, cleanup, production hardening, and final browser verification.

Design-only work is complete when the requested artifact makes hierarchy, behavior, responsive change, states, and Tailwind v4 expression unambiguous. Do not save a design spec unless the user requested a file or the project requires one.

For structural polish, the original behavior must remain intact and the targeted hierarchy, accessibility, responsive, dark-mode, or finish problem must be resolved across the full affected path.

## Work End to End

### 1. Inspect the Product and Task

Read project instructions, product and brand documents, the relevant route and components, existing tokens, and the runnable interface. Identify:

- the user's job and core path;
- real content, data, and states;
- the established shell, grid, components, and vocabulary;
- technical constraints and the styling system;
- what must remain unchanged.

Do not begin by inventing a visual theme in isolation. Inspection is complete when you can describe the user's task, the product constraints, and the interface boundary in a few concrete sentences.

### 2. Load Only the Relevant References

Read [`references/interface/index.md`](references/interface/index.md) and open only the branch needed for this task.

- For page directions, read [`references/interface/ui-picker.md`](references/interface/ui-picker.md).
- Read [`references/tailwind-v4.md`](references/tailwind-v4.md) only for an authorized or already-configured migration.
- For design-only work, load the wireframe or design-spec references only when that artifact was requested.
- For motion, begin with [`references/interface/animation.md`](references/interface/animation.md). If installed, use `animate` for specialist implementation craft and `motion` for current library or API facts.

The reference files are a router, not a checklist. Never load every rule file by default.

### 3. Set the Direction

For direct implementation, state the chosen direction briefly: hierarchy, typography, color behavior, density, and interaction temperament. A direction should be specific enough to constrain implementation, not a mood-board slogan.

For page directions:

1. Preserve the current page as the baseline. For a new route with no prior page, create `Current` as a conservative baseline using the product's existing shell, components, tokens, and conventions.
2. Create five genuinely different rendered directions.
3. Keep content, data, state, and behavioral code shared. Vary presentation structure, hierarchy, typography, color, density, and interaction treatment.
4. Make every direction communicate the complete page hierarchy and core path. Production hardening follows selection.
5. Review the picker in the browser, then present one structured selection to choose the direction.

If the app cannot run, still produce the coded directions and present screenshots when possible. If neither preview nor screenshots are possible, present concise descriptions in a structured selection instead of stalling.

### 4. Implement in Tailwind v4

Use the project's components and conventions before creating new primitives. Express visual decisions through Tailwind v4 utilities, variants, and `@theme` tokens rather than scattered arbitrary values.

Tailwind has a mechanical authorization boundary:

- Existing Tailwind v4 work is in scope.
- Converting touched UI files to an already-configured v4 system is in scope.
- If v4 adoption requires changing package manifests, build configuration, or the global CSS entry point, pause with a strong migration recommendation unless the user already authorized migration.
- Never turn a contained UI request into a repository-wide styling migration silently.

Build stable states, not just a stable initial frame. Dynamic geometry must not cause avoidable layout shift; keyboard actions must preserve native form semantics; focus must remain visible and move into view; clipping must not create accidental scroll containers; and interactive states must not jump because borders, labels, or controls appear late.

### 5. Exercise and Refine the Rendered Experience

Run the real app and complete the core user path. Verify, as relevant:

- desktop and mobile layouts;
- keyboard and pointer operation;
- focus order, focus visibility, semantics, and the accessibility tree;
- long, empty, loading, failure, and success states;
- console errors and failed network requests;
- persistence and the downstream effect of the user's action;
- motion interruption and reduced-motion behavior;
- contrast and real raster assets in dark mode.

Use `fieldtest` for a deeper browser-QA pass when it is installed and the risk warrants it. Tests support this pass; they do not replace it. Refine until the complete path is coherent, responsive, accessible, and visually resolved.

### 6. Clean Up and Report

After a page direction is selected, remove every rejected direction and all local picker components, presentation switches, temporary parameters, wrappers, hidden branches, suppressions, and unused imports. Re-run the relevant checks and the complete user path.

Report the direction, what changed, verification performed, and any honest limitation. Do not claim browser verification when only static checks ran.

Before reporting completion, confirm that:

- every label, heading, button, status line, and empty state has been read against `signage`, and no string carries vocabulary the audience does not use;
- the primary task is apparent without explanatory scaffolding;
- real content and adverse states do not break the hierarchy;
- keyboard, pointer, and touch behavior agree where they should;
- temporary direction or migration scaffolding is gone;
- the implementation still follows the project's architecture and vocabulary.

## Taste and Craft Guardrails

- Use authentic product content. Placeholder slogans and generic dashboard data conceal design problems.
- Keep hierarchy compact. A small, named type system is stronger than ad hoc sizes; sentence case is the default. Reserve monospace or all-caps treatment for genuinely technical or compact numeric content.
- Use one coherent icon family. Icons need accessible names or adjacent labels when their meaning is not obvious.
- Make touch targets at least 44 by 44 CSS pixels, including invisible padding, without making every visual control bulky.
- Align optical shapes by eye where mathematical centering looks wrong. Nested rounded shapes should use concentric radii, not repeated arbitrary values.
- Avoid generic AI defaults: stacked rounded cards, gratuitous gradients, glowing borders, ornamental pills, oversized hero copy, and decorative status chrome.
- In dark mode, rebuild contrast relationships rather than invert colors. Use dark-mode variants for raster assets when the light asset does not hold up.
- Motion needs a purpose, an origin, an interruption behavior, a frequency budget, and a reduced-motion treatment. Fast feedback and perceived speed matter more than spectacle.

## Specialist Boundaries

Chiaroscuro remains usable on its own. Delegate only when a specialist skill is installed and the task benefits from depth:

- `typecase` for the type ramp and its scanner;
- `componentize` for a reuse and duplication audit;
- `animate`, `motion`, `review-animations`, `improve-animations`, or `find-animation-opportunities` for focused motion work;
- `signage` for the words on the interface, whenever the copy was written by an agent;
- `fieldtest` for evidence-heavy browser QA;
- `apple-design` for Apple-platform craft;
- `dark-mode-image`, `canonicalize-tailwind`, `markup-from-image`, `prototype`, or `pick-ui-library` for their narrow utilities.

Do ordinary end-to-end interface work here. Do not force a specialist dependency, a saved design spec, a wireframe, or an approval pause unless the selected mode or the user requires it.
