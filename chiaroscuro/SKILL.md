---
name: chiaroscuro
description: Create distinctive, non-generic, user-centered UI design direction, wireframes, Tailwind v4 visual systems, Tailwind @theme tokens, design specs, and post-implementation UI polish. Use when asked to design a UI, create a layout, remove decorative UI furniture, prevent implementation/system leakage, make a page or app screen memorable, establish a visual direction, produce a design spec before implementation, clean up AI-looking interface work, componentize UI code, deduplicate repeated UI patterns, or polish Tailwind/React frontend code after implementation. This skill assumes Tailwind v4 as the mandatory styling target.
---

# Chiaroscuro

Use this skill to make UI design concrete before code, and to polish UI code after it exists. The goal is not decoration; it is specific visual direction that another agent or engineer can implement without drifting into generic AI output.

Design for the user's task, not for the implementation underneath it. Chiaroscuro must produce interfaces that feel like coherent products, not exposed schemas, prompt scaffolds, agent logs, or ornamental screenshots.

Announce at start: "I'm using the chiaroscuro skill to create a distinctive UI direction."

## First Principles

**Everything must earn its place.** The default is removal, not addition. Every visible element — every panel, badge, divider, label, shadow, wrapper, and typographic treatment — must justify itself by serving clarity, utility, hierarchy, affordance, state communication, navigation, or domain meaning. If an element can be removed without reducing comprehension, remove it. Optimise for clarity and utility above all.

**No UI furniture.** Decorative chrome, wrapper panels, floating badges, ornamental dividers, status strips, fake controls, empty accent shapes, background effects, and visual clutter are furniture — they fill space without serving the user. The instinct to make a screen "look more designed" by adding visual weight is the instinct to reach for furniture. Resist it. A screen with fewer elements and better hierarchy always beats a screen with more elements and equal hierarchy.

**No system leakage.** Hide implementation concepts, prompt/workflow mechanics, database schemas, API names, internal state machines, and agent reasoning behind user-centered nouns, verbs, progressive disclosure, and task-focused states.

## Operating Rules

- Keep design creation collaborative. Ask short questions one at a time when direction is missing.
- Prefer concrete decisions over conceptual themes.
- Make every design decision expressible as Tailwind v4 `@theme` tokens, CSS-first Tailwind utilities, custom variants, and component class shapes.
- Treat Tailwind v4 as non-negotiable. If a project is not already Tailwind v4-based, the design spec must include the Tailwind v4 token and utility model required to implement the design.
- Use the project's existing design system, components, and domain rules before inventing new primitives, but express all styling through Tailwind v4.
- Project-local visual tokens may inform values, but they do not override the Tailwind v4 requirement. Translate them into Tailwind v4 `@theme` tokens where needed.
- Do not default to marketing-page structure for apps, tools, games, dashboards, or workflows. Design the actual usable surface first.
- Apply the "earn its place" test to every element. If you cannot name what the element clarifies, cut it.
- Do not let the design spec contradict existing `docs/brand-system.md`, `docs/design-context.md`, project rules, or implemented design tokens.
- For substantial UI work, save the design spec to `docs/design/specs/design-[name].md`. For small components, an inline spec is acceptable unless the user wants a file.

## Reference Loading

Load references only as needed. All paths are relative to this skill folder.

For full design direction, read:

- `references/frontend-design.md`
- `references/brand-identity.md` if no project brand system exists
- `references/design-philosophy.md`
- `references/ux-laws.md`
- `references/typography-opentype.md`
- `references/ascii-ui-patterns.md`
- `references/tailwind-v4.md`
- `references/interface/index.md`
- `references/interface/tailwind-authoring.md`
- `references/interface/buttons.md`
- `references/interface/surfaces.md`
- `references/interface/sections.md`

Then read the relevant interface rules:

- App UI: `references/interface/app-ui.md`
- Marketing/site work: `references/interface/marketing.md`
- Visual design: `references/interface/design.md`, `references/interface/colors.md`, `references/interface/typography.md`
- Layout and responsiveness: `references/interface/layout.md`, `references/interface/spacing.md`, `references/interface/responsive.md`
- Forms: `references/interface/forms.md`
- Interactions: `references/interface/interactions.md`
- Motion: `references/interface/animation.md`
- Accessibility/content: `references/interface/content-accessibility.md`
- Performance-heavy UI: `references/interface/performance.md`

For a single component or small fragment, read only `frontend-design.md` plus the 2-3 most relevant interface files.

Do not produce framework-agnostic, CSS Modules, styled-components, emotion, or plain-CSS-first design specs. Raw CSS is acceptable only inside Tailwind v4 CSS-first primitives such as `@theme`, `@utility`, `@custom-variant`, or unavoidable global base rules.

## Mode Detection

Choose a mode before loading heavy references.

**Design mode:** The user wants visual direction, a page/screen layout, a wireframe, a design doc, or a new interface concept. Load the full reference set as listed below.

**Component fast-path:** The user wants a single component or small UI fragment. Load only `references/frontend-design.md` plus 2-3 relevant interface files — do not load the full reference set.

**Polish mode:** The user wants to clean up, componentize, deduplicate, organize, or improve existing UI code without changing product direction.

Announce the chosen mode.

## Component Fast-Path Workflow

Use this for a single component, a small UI fragment, or a contained piece like a card, input, modal, or data row.

1. **Load light context.** Read `references/frontend-design.md` and 1-3 interface files relevant to the component type (e.g. `buttons.md` for a button, `forms.md` for an input, `surfaces.md` for a card). Check for `docs/brand-system.md` or `docs/design-context.md` to inherit existing tokens. Do not load the full reference set.
2. **Check what exists.** Search for existing shared components, tokens, and patterns in the project before proposing anything new. If a design system is in place, work within it.
3. **Make decisions, not specs.** Skip wireframes and multi-step direction gathering. Decide: font, size, weight, color tokens, spacing, radius, states (default, hover, focus, active, disabled, loading, error). Name each decision concretely.
4. **Build.** Implement directly with Tailwind v4 utilities and project conventions. Apply the earn-its-place test — no decorative wrappers, no furniture, no mono small-caps unless the component contains numeric or data-like content.
5. **Verify.** Run typecheck and lint. Screenshot if a browser tool is available.

## Design Mode Workflow

### 1. Load Project Context

Check for these files first:

- `docs/brand-system.md`
- `docs/design-context.md`
- relevant project rules such as `AGENTS.md`, `.ruler/`, `rules/`, or design-system docs

If `docs/brand-system.md` exists, treat it as canonical for palette, typography, tone, and visual character. Do not re-ask settled brand questions.

If only `docs/design-context.md` exists, inherit it and avoid re-asking settled visual decisions.

If neither exists and the work is substantial, ask whether to establish persistent design context. If yes, create `docs/design-context.md` with:

- brand personality and tone
- display, body, and mono font choices
- Tailwind `@theme` color tokens in OKLCH
- spacing and radius scale
- surface ladder and depth model
- button, card, input, and dense data patterns
- motion philosophy
- project-specific anti-patterns

### 2. Inspect What Exists

If redesigning existing UI:

- Open or run the app when practical.
- Capture screenshots at desktop and mobile widths when a browser tool is available.
- Inspect existing components, tokens, and layout conventions.
- Report what is working, what is generic, and what is incoherent before proposing changes.

If designing from scratch:

- Confirm the product context, target user, and whether the UI is marketing, app UI, component, game, or tool.
- Ask for reference URLs, screenshots, or brand constraints if they matter.

### 3. Gather Direction

Ask only what is missing. Prefer one question at a time.

For most work, resolve:

- UI type: app UI, marketing/site, component, tool, game, or content surface
- tone: minimal, bold, editorial, playful, luxury, brutalist, industrial, organic, retro, quiet operational, or another specified direction
- density: sparse, balanced, or dense
- memorable element: typography, layout structure, interaction model, data treatment, imagery, motion, or navigation — the memorable element must serve comprehension or utility, not just visual interest
- frame/chrome: standard site chrome, app-like focus, or hybrid navigation
- constraints: existing brand, component library, accessibility, responsive needs, performance, implementation stack

Do not ask for aesthetic choices already implied by the product domain or existing design context.

### Design Routes (5 Directions)

When the user asks for a broad-strokes redesign — a whole page, a full view, a screen, a design system overhaul, or any work that sets visual direction for an entire surface — present **5 visually distinct design routes** before committing to implementation.

This is the default behavior for page-level and system-level design work. Do not wait for the user to ask for alternatives. Do not skip this step unless:
- The user explicitly says they already know the direction they want, or
- The work is a single component, a small fragment, or a contained piece (use the component fast-path instead).

Each route must be genuinely different — not five minor theme tweaks or color swaps on the same layout. Vary across these axes:
- Typography pairing and hierarchy
- Palette mood and contrast model
- Layout structure and density
- Shape language and radius
- Surface treatment and depth
- Motion personality
- Overall character (e.g., one route could be editorial and typographic, another dense and tool-like, another bold and graphic, another quiet and spacious, another brutalist and high-contrast)

**Route format:**

For each route, provide:
1. A short evocative name (e.g., "Swiss Utility", "Dark Editorial", "Soft Spatial")
2. 2-3 sentence personality description
3. Key decisions: display font, body font, palette direction (warm/cool/neutral, light/dark), density (sparse/balanced/dense), shape language (sharp/soft/mixed), surface model (flat/layered/elevated), and memorable element
4. A rough wireframe sketch showing how layout differs from the other routes

Keep each route description concise — the goal is quick visual differentiation, not a full spec. The user picks one (or mixes elements), and only then do you develop the full design spec.

### Exploring Alternatives (General)

For smaller decision points within a chosen direction, or when iterating on an existing design:

- Define each decision point with a human-readable label, such as `Hero style`, `Navigation model`, or `Pricing layout`.
- Unless the user asks for a different count, generate 3-4 options per decision point.
- When iterating on existing UI, make option 1 the current implementation and label it `(current)`.
- Write a style definition before implementation for each option: layout, typography, color, spacing, surfaces, shape language, and personality.
- New options must be faithful executions of their style definition. Existing-design options should vary layout and component choices while still belonging to the current aesthetic.
- After the user selects an option, remove unselected variant scaffolding and any temporary comments or wrappers created only for comparison.

### 4. Optional Inspiration Research

Use inspiration research when it will sharpen concrete choices, not as procrastination.

- For websites and marketing surfaces, use curated examples such as Siteinspire when available.
- For app UI, mobile screens, onboarding, dashboards, settings, and interaction patterns, use product UI references such as Mobbin when available.
- If the user provides a reference URL, screenshot or inspect it immediately when a browser tool is available.
- Summarize observed typography, color relationships, layout patterns, spacing, and interaction details.
- Translate useful observations into Tailwind v4 tokens, class shapes, and component patterns.

Do not copy another design. Use references to identify reusable structural ideas and visual constraints.

### 5. Make Concrete Visual Decisions

Produce specific decisions, not mood-board language.

Include:

- typography: exact display/body/mono font choices and where each is used
- color: Tailwind v4 `@theme` tokens in OKLCH, including neutrals, surfaces, text, accents, hover states, and destructive states
- spacing: base unit, section gaps, component padding, layout rhythm
- surface system: canvas, surface, raised, overlay, borders, shadows, radius scale
- controls: button heights, icon sizing, input/select treatment, focus and disabled states
- layout: grid, asymmetry, density, scrolling model, mobile adaptation, state placement
- motion: where motion clarifies interaction, timing, easing, reduced-motion behavior
- content/state design: empty, loading, error, success, dense data, long text, and user-generated content behavior
- abstraction: user-facing labels, navigation, states, and workflows that describe what people are trying to do, not how the software is implemented

Never:

- purple-to-blue gradients as a default flourish
- default system fonts as the design answer
- white background plus gray cards as the whole interface
- UI furniture: chrome, decorations, separator bars, visual effects, or repeated wrappers that exist only to make the screen look more designed
- exposed internals: raw schema fields, API names, prompt/agent mechanics, "step 1/2/3" workflow scaffolds, debug statuses, or system terminology unless the target user explicitly needs them
- uppercase wide-tracked eyebrows on sans/serif headings
- icon-only controls without accessible names

Mono small-caps discipline:

- Mono small-caps (`font-variant-caps: all-small-caps` on a monospace face, or uppercase monospace at reduced size) is a refined, high-signal typographic treatment. It is not a default label style.
- Appropriate uses: numeric metadata (`v2.4.1`, `$49/mo`, `3 min read`), short data-adjacent labels in dense UI (`ID`, `STATUS`, `ETA`), and sparse section markers where a quiet structural cue is needed (typically one per screen, not one per section).
- Inappropriate uses: every section eyebrow, every card label, every sidebar heading, every tag, every piece of metadata. When mono small-caps appear on more than a few elements per screen, the treatment loses its signal and becomes wallpaper.
- Before applying mono small-caps, ask: is this label numeric or data-like? Is it short (1-3 words)? Would sentence-case in the body font at a lighter weight work just as well? If the answer to the last question is yes, use sentence-case.
- The test: if you removed all mono small-caps from the screen, would the hierarchy collapse? If not, most of them are decorative.

Avoid:

- generic centered hero plus cards layout unless the product truly needs it
- decorative cards inside cards

### 6. Wireframe

Create a low-fidelity structure before implementation.

Use ASCII wireframes from `references/ascii-ui-patterns.md`.

Include:

- desktop structure
- mobile structure for responsive work
- primary interactions
- at least one non-happy state for app UI: empty, loading, error, or permission denied

Ask whether the structure feels right before writing a final design spec when the user is actively collaborating.

### 7. Write the Change Spec

Translate the direction into measurable implementation changes.

Use this structure:

```markdown
## Change Spec

### Typography
| Element | Before | After | Reference |
| --- | --- | --- | --- |

### Colors
| Element | Before | After | Reference |
| --- | --- | --- | --- |

### Spacing
| Element | Before | After | Reference |
| --- | --- | --- | --- |

### Layout
| Element | Before | After | Reference |
| --- | --- | --- | --- |

### Motion
| Element | Before | After | Reference |
| --- | --- | --- | --- |

### Abstraction
| Exposed implementation detail | User-centered replacement | Reference |
| --- | --- | --- |
```

Rules:

- Use specific values, tokens, class shapes, and component names.
- Reference the local rule or reference file that justifies each meaningful change.
- If the spec only changes padding, spacing, or copy, stop and deepen the design.

### 8. Save the Design Spec

For substantial work, create `docs/design/specs/design-[name].md`.

Include:

- aesthetic direction and tone
- target user and surface type
- typography choices
- OKLCH Tailwind token palette
- spacing and radius scale
- surface and depth system
- canonical button, card/panel, input/select, and data-row patterns
- desktop and mobile wireframes
- state designs
- implementation notes tied to the project's component system
- anti-patterns to avoid
- abstraction rules: user-facing language, hidden implementation details, and what can be progressively disclosed
- complexity guardrails
- interactive state requirements
- contrast and accessibility requirements
- verification checklist

Use this compact structure:

```markdown
# Design Direction: [Name]

## Intent
- Surface type:
- Target user:
- Tone:
- Memorable element:

## System
- Typography:
- Color tokens:
- Spacing/radius:
- Surface ladder:
- Control patterns:

## Wireframes
### Desktop
### Mobile
### States

## Change Spec
### Typography
### Colors
### Spacing
### Layout
### Motion

## Implementation Notes
## Anti-Patterns
## Abstraction Rules
## Complexity Guardrails
## Interactive States
## Verification Checklist
```

In complexity guardrails, name concrete limits for the implementation. Every element must earn its place — cut wrapper elements with no purpose, cards inside cards, excessive nesting for simple content, decorative chrome, too many font sizes, too many accent colors, arbitrary spacing values, mono small-caps used as a general label style rather than for numeric or data-adjacent content, and Tailwind class strings that should become reusable components.

In abstraction rules, name which internal details must be hidden, translated, or deferred. Replace implementation-first copy with domain language: `API key created` can become `Connection ready`; `vector index sync failed` can become `Search is still updating`; `agent step running` can become `Checking the next section`. Keep debug details available only behind explicit affordances when the user needs diagnosis.

In interactive states, specify expectations for default, hover, focus, active, disabled, loading, error, and success states when the UI includes controls or forms.

### 9. Critique Before Handoff

Review the draft like a design lead:

- Does every visible element earn its place? For each panel, badge, divider, label, shadow, and wrapper: what does it clarify? If nothing, cut it.
- Does the layout have rhythm, or is every block the same weight?
- Is priority clear from proportion, spacing, contrast, and placement?
- Does the design have one memorable element that is actually visible — and does that element serve comprehension, not just visual interest?
- Would a real user in this product domain find it plausible?
- Can the implementation be built cleanly with the target component system?
- Are there any cards, wrappers, arbitrary values, or decorative fragments that exist only to make the screenshot feel busier?
- Are mono small-caps limited to numeric content and short data labels, or have they spread to every label on the screen?
- Does any visible text expose the database, API, prompt, model, chain, agent, workflow engine, or internal state instead of explaining the user's task?
- Would a non-engineer target user understand what to do without reading implementation vocabulary?

Revise the spec before handoff if any answer is weak.

### 10. Verify Against Red Flags

The design is not complete until these are true:

- zero default-font-as-design decisions
- zero purple-blue gradient defaults
- zero generic admin-template or AI landing-page feel
- zero repeated uppercase tracked eyebrows on sans/serif headings
- zero inaccessible icon-only controls
- zero UI furniture — every visible element passes the "earn its place" test: it serves clarity, utility, hierarchy, affordance, state, navigation, or domain meaning
- zero unnecessary system leakage in visible labels, navigation, empty states, errors, or progress states
- mono small-caps used only for numeric content and short data-adjacent labels, not sprayed across section eyebrows, card labels, sidebar headings, or general metadata
- all critical states accounted for
- contrast requirements named
- mobile and desktop structures both considered
- implementation notes are specific enough to guide code

### 11. Continue Into Implementation When Asked

If the user asked to design and implement in the same request:

- Create the smallest useful spec first.
- Implement against the project conventions immediately after the spec.
- Visually verify the rendered result when a browser or screenshot tool is available.
- Keep the final answer focused on the implemented UI and checks run, not the full design process.

## Polish Mode Workflow

Use polish mode when UI code already exists and the request is cleanup, componentization, deduplication, or visual tightening.

### 1. Scan Current State

Look for:

- large components with mixed responsibilities
- repeated section shells, heading groups, cards, controls, and empty states
- Tailwind class strings that encode reusable patterns inline
- components that bake in margins instead of accepting layout from callers
- dead wrapper elements
- duplicate component names or near-identical components
- inconsistent button, input, card, and surface treatments

Search for existing shared components before proposing new ones.

### 2. Extract and Consolidate

Keep changes behavior-preserving unless the user asked for redesign.

- Split large components by domain role, not by arbitrary JSX chunks.
- Extract reusable UI pieces only when duplication or complexity justifies it.
- Prefer existing design-system primitives.
- Ensure reusable React components accept `className` when local conventions expect it.
- Keep layout responsibility with the caller where possible.
- Never bake margins into reusable components; apply outer spacing at the call site.
- Use `clsx` or the project's existing class-merge helper when components need conditional classes.
- Extract form controls by HTML element, not by use case: one `Input` for text/email/password/etc., one `Select`, one `Textarea`. Do not create `EmailInput`/`PasswordInput` variants unless the domain behavior is genuinely different.
- When two or more elements share structure and styling but differ only by labels, placeholders, icons, or types, extract one prop-driven component.
- After extracting, scan again for repeated section containers, heading groups, card shells, button styles, and form controls.
- Avoid introducing compatibility shims or old/new comments.

### 3. Clean Tailwind Authoring

Read `references/interface/tailwind-authoring.md`.

- Prefer tokens and utilities over bespoke CSS.
- Remove conflicting utilities.
- Replace arbitrary values with scale values when the exact value is not meaningful.
- Consolidate repeated class shapes into components or small helpers only when it reduces real duplication.
- When available, use `npx @tailwindcss/cli canonicalize` to normalize class lists. Pass the project's CSS entry file with `--css path/to/input.css` when custom Tailwind v4 tokens or utilities are required for accurate output.
- Use structured output such as `--format json` or `--format jsonl` when processing many class strings.

### 4. Verify

Run scoped checks appropriate to the changed project:

- typecheck
- lint or formatter
- package/app tests
- browser screenshot review for user-facing UI

Report any checks that could not be run.

## Output Shape

For design work, end with:

- where the design spec was saved, or the inline spec
- the chosen visual direction
- the key implementation constraints
- unresolved user decisions, if any

For polish work, end with:

- changed files
- extracted components or consolidated patterns
- checks run
- remaining visual or architectural risks
