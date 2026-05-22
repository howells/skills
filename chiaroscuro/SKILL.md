---
name: chiaroscuro
description: Create distinctive, non-generic UI design direction, wireframes, Tailwind v4 visual systems, Tailwind @theme tokens, design specs, and post-implementation UI polish. Use when asked to design a UI, create a layout, make a page or app screen memorable, establish a visual direction, produce a design spec before implementation, clean up AI-looking interface work, componentize UI code, deduplicate repeated UI patterns, or polish Tailwind/React frontend code after implementation. This skill assumes Tailwind v4 as the mandatory styling target.
---

# Chiaroscuro

Use this skill to make UI design concrete before code, and to polish UI code after it exists. The goal is not decoration; it is specific visual direction that another agent or engineer can implement without drifting into generic AI output.

Announce at start: "I'm using the chiaroscuro skill to create a distinctive UI direction."

## Operating Rules

- Keep design creation collaborative. Ask short questions one at a time when direction is missing.
- Prefer concrete decisions over conceptual themes.
- Make every design decision expressible as Tailwind v4 `@theme` tokens, CSS-first Tailwind utilities, custom variants, and component class shapes.
- Treat Tailwind v4 as non-negotiable. If a project is not already Tailwind v4-based, the design spec must include the Tailwind v4 token and utility model required to implement the design.
- Use the project's existing design system, components, and domain rules before inventing new primitives, but express all styling through Tailwind v4.
- Project-local visual tokens may inform values, but they do not override the Tailwind v4 requirement. Translate them into Tailwind v4 `@theme` tokens where needed.
- Do not default to marketing-page structure for apps, tools, games, dashboards, or workflows. Design the actual usable surface first.
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

**Design mode:** The user wants visual direction, a page/screen layout, a wireframe, a design doc, or a new interface concept.

**Component fast-path:** The user wants a single component or small UI fragment. Compress discovery, skip external inspiration unless useful, and keep output implementation-ready.

**Polish mode:** The user wants to clean up, componentize, deduplicate, organize, or improve existing UI code without changing product direction.

Announce the chosen mode.

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
- memorable element: typography, layout structure, interaction model, data treatment, imagery, motion, or navigation
- frame/chrome: standard site chrome, app-like focus, or hybrid navigation
- constraints: existing brand, component library, accessibility, responsive needs, performance, implementation stack

Do not ask for aesthetic choices already implied by the product domain or existing design context.

If the work is greenfield, substantial, and direction is unclear, offer to explore multiple directions before committing. Create up to five genuinely different directions only when the user chooses that path; vary typography, palette, layout structure, density, shape language, surface treatment, and personality. Do not present five minor theme tweaks.

When exploring alternatives:

- Define each decision point with a human-readable label, such as `Hero style`, `Navigation model`, or `Pricing layout`.
- Unless the user asks for a different count, generate 3-4 options.
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

Avoid:

- purple-to-blue gradients as a default flourish
- default system fonts as the design answer
- white background plus gray cards as the whole interface
- generic centered hero plus cards layout unless the product truly needs it
- decorative cards inside cards
- uppercase wide-tracked eyebrows on sans/serif headings
- overused mono small-caps labels; use monospace uppercase labels sparingly, usually no more than one recurring label style per screen
- icon-only controls without accessible names

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
## Complexity Guardrails
## Interactive States
## Verification Checklist
```

In complexity guardrails, name concrete limits for the implementation: avoid wrapper elements with no purpose, cards inside cards, excessive nesting for simple content, too many font sizes, too many accent colors, arbitrary spacing values, and Tailwind class strings that should become reusable components.

In interactive states, specify expectations for default, hover, focus, active, disabled, loading, error, and success states when the UI includes controls or forms.

### 9. Critique Before Handoff

Review the draft like a design lead:

- Does the layout have rhythm, or is every block the same weight?
- Is priority clear from proportion, spacing, contrast, and placement?
- Does the design have one memorable element that is actually visible?
- Would a real user in this product domain find it plausible?
- Can the implementation be built cleanly with the target component system?
- Are there any cards, wrappers, arbitrary values, or decorative fragments that exist only to make the screenshot feel busier?

Revise the spec before handoff if the answer is weak.

### 10. Verify Against Red Flags

The design is not complete until these are true:

- zero default-font-as-design decisions
- zero purple-blue gradient defaults
- zero generic admin-template or AI landing-page feel
- zero repeated uppercase tracked eyebrows on sans/serif headings
- zero decorative overuse of mono small caps; use them only for functional labels, sparse section markers, or data-like metadata
- zero inaccessible icon-only controls
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
