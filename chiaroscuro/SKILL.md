---
name: chiaroscuro
description: "Design, build, polish or critique web UI in Tailwind v4. Use when an interface should look gorgeous, looks generic or unfinished, or feels off. Not for design options (`maquette`), app shells (`armature`), screen sizes (`reflow`), Paper (`paste-up`) or QA (`fieldtest`)."
---

# Chiaroscuro

Take a web interface from request to finished, working UI with a specific point of view: the product's own language, real content and behaviour, no furniture, and nothing of the system showing through. It builds one design, whether a component, a region or a page, or rescues one that looks messy, generic or unfinished.

When someone asks only for a critique of a screenshot, page, frame, code or change, read [references/critique.md](references/critique.md) first, follow it and change nothing until they ask. Read each reference file with its own command.

Deeper passes live in `zoetrope` (motion), `signage` (wording), `typecase` (type ramp) and `componentize` (duplication); use them when installed. This skill works without them, and they never carry the hard rules for you.

## Hard rules

These hold everywhere, including work handed to a helper. Styling the product already has is not an exception: fix it inside the scope and mention it outside. Only an explicit instruction from the user overrides a rule.

1. **No small caps, tracked uppercase or decorative mono.** No eyebrows, kickers, section labels, chips or table headings in capitals. Mono is for literal code, identifiers and values whose characters need inspecting, never for labels or headings. Proper acronyms keep their capitals.
2. **No numbered items, and no dot or stripe as ornament.** Options, categories, features, cards, sections and steps go by name alone: no `01`, `1.`, `#1`, `Step 1` or numbered circle in front, beside or above. A numeral appears only as data (a rank, a count, a position such as `2 of 4`) or in an ordered list inside running text. A label, heading or list item starts with its own words, with no coloured dot or bullet before it; a dot marks real live state. A card or tile shows selection, status or category with a fill, a ring or an icon, never a stripe down one side.
3. **No prose where interface belongs.** A paragraph explaining a screen means the screen has failed. Replace it with a label, a control, a value or nothing. In product UI, headings name things; they don't headline them or introduce a section. Keep only consent, constraints and error recovery.
4. **Four to six type styles, in chosen faces.** Use the product's named roles. A new size or weight needs a job no existing role does. Never use Instrument Serif, Playfair Display, Poppins, Montserrat, Roboto or Arial for a new face. Before choosing one, read [references/font-guidance.md](references/font-guidance.md) and choose from its recommendations.
5. **Reuse before you build.** Find the existing component, shell, header or control that does the job, in this product and in any package or project the user pointed to, and use it. A second version of an existing control is a defect.
6. **One of each.** One corner-radius scale with concentric nesting, one icon family at one stroke weight, one control height per density.
7. **Touch targets at least 44 by 44 CSS pixels**, reached with invisible padding rather than bulky visuals.
8. **Look at it before calling it done**, in a real browser on desktop and phone (step 4).

## Machine-made tells

These make an interface look generated rather than designed. Leave them out unless the brief genuinely asks for one.

- Stacked rounded cards; the same padding, radius and shadow on every container; cards inside cards; white cards on a white or `gray-50` ground.
- Decorative gradients, purple or multicolour gradients, glows, blurs beyond `blur-xl`, grain or noise laid over the page.
- The editorial default: a cream or parchment ground, terracotta accent and big serif display headline. Its "technical" twin: tinted near-black with an acid-green or neon accent. Indigo as the accent by reflex.
- A headline where a name belongs ("Your week, at a glance"), one word of it picked out in colour or italic, a filler sentence under every heading.
- Word-dash labels (`Fast - built for teams`), dotted metadata strings (`Design · 4 min · Updated today`), `→` appended to links and buttons.
- Ornamental pills, version stamps, city and local-time strips, scroll prompts, hairlines and grid lines drawn for atmosphere.
- A fake product preview built from styled divs, a hero built around one oversized metric, emoji as icons, placeholder copy.
- Hero, features, testimonials, CTA by reflex; everything centred.
- Emphasis everywhere: most things bold, coloured, badged or raised, so nothing leads.
- A sheet over a modal over a scrim.

## Work end to end

### 1. Inspect the product and the task

Read the project instructions, brand documents, the route, its components and tokens, and run the interface. Know the user's job and core path, the real content and states, the established shell, components and vocabulary, and what must not change. Don't invent a visual theme in isolation.

For a flow, walk one concrete scenario before drawing screens: what the person supplies, what stays unchanged, what they choose, what they leave with. Keep inputs with different meanings distinct. For a contained edit, check its place in the existing path rather than reopening the whole product.

### 2. Decide the look

Settle the shape before the styling. A focused, single-purpose experience, such as a picker, a checkout or a viewer, puts its subject on screen with no header, navigation or title by default. A persistent shell earns its place only when people move between places or work across panes.

Then state the look in a sentence or two: hierarchy, typography, colour behaviour, density and interaction temperament, specific enough to constrain the code. Test each choice by swapping it: if the alternative wouldn't change the meaning (the same font, sidebar and grey-with-blue as every SaaS dashboard), it is a default, not a choice. With the product name removed, the design should still say what it's for.

Compose the phone as its own design, not the desktop squeezed down: the primary action within thumb reach, sheets rather than centred modals, media full-bleed, fewer controls at once and a smaller display size.

Carry the defining decisions of a supplied design or accepted review into the code: what leads, what stays quiet, what remains visible, how actions relate to supporting information. A convenient component variant is not a reason to change the composition. When borrowing another interface's aesthetic, name the features borrowed (type, texture, density, control treatment) and keep the target product's tasks and state transitions intact.

Hide the machinery. Labels, navigation, statuses, empty states and errors describe the user's work: `sync failed` becomes `Updates are paused`, `agent step running` becomes `Checking the next section`. Prompt scaffolds, agent steps, model names, schema, queue states and raw diagnostics stay out of the primary UI unless they are the product's own objects; put diagnostics behind "View details" or "Copy error".

Emphasise by quietening the rest: there is a ceiling on how loud something can get and no floor on how quiet the rest can go. Use the product's own imagery as one coherent set, consistent in light, ratio and crop; no image is better than stock filler or the wrong object.

Before building, read the reference file for each part the work touches:

- Layout, spacing, alignment, surfaces, depth, app states and navigation: [layout](references/layout.md).
- Palettes, tokens, contrast and dark mode: [color](references/color.md).
- Text in use, rich text, custom fonts, numbers and dates: [type](references/type.md).
- Interactive states, overlays, menus, focus, keyboard, touch and accessibility: [interaction](references/interaction.md).
- Forms, settings and native control markup: [forms](references/forms.md).
- Buttons, tables, dashboards, navigation, badges, avatars, icons, images, SVG and charts: [components](references/components.md).
- A marketing or landing page: [marketing](references/marketing.md).
- Any motion: [motion](references/motion.md).
- Tailwind class authoring: [tailwind](references/tailwind.md).

### 3. Build in Tailwind v4

Use the project's components and conventions before new primitives, and express decisions as utilities, variants and `@theme` tokens rather than scattered arbitrary values. In a project on another styling system or Tailwind version, build in what it has; the rules hold and the class names translate. A UI request never becomes a styling migration.

When the project has nothing for the job, default to these rather than hand-rolling: Base UI for accessible primitives (dialogs, popovers, menus, selects), cmdk for command menus, Sonner for toasts, input-otp for code inputs, Motion for springs, layout and exit animation, NumberFlow for animated numbers, Recharts for charts, dnd kit for drag and drop, Virtuoso for long lists, clsx for conditional classes and cva for typed variants, next-themes for flash-free theming. Never mix component libraries.

Build stable states, not just a stable first frame. Reserve room for labels and controls that arrive late, draw state-dependent edges as rings or inset shadows rather than borders, keep controls in a row at one height, and give images a fixed ratio. Keep native form semantics; focus stays visible and moves into view; clipping never creates an accidental scroll container.

### 4. Look, then refine

Run the real app at the exact route and exercise the changed path on desktop and phone, including the states, content and input methods the change affects. Search the changed files for `uppercase`, `tracking-`, `font-mono`, `border-l-`, `border-s-`, `rounded-full`, `list-decimal`, `padStart` and `index + 1`, and clear every hit against rules 1 and 2.

Then zoom out, after the first full composition and after any material change. Look at the whole viewport and successive states together. What draws the eye first: the user's subject, or the controls around it? Is the next action apparent? Fix the biggest compositional problem before polishing details, and recompose when local fixes have left the whole incoherent. Before refining, read [references/critique.md](references/critique.md) and run its lenses against your own screen.

### 5. Clean up and report

Remove temporary wrappers, hidden branches, suppressions and unused imports the work introduced. Report what changed, what you exercised and what you looked at, and any limitation. Never claim the browser pass when only static checks ran.
