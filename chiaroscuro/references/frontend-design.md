# Frontend Design Reference

Create distinctive, production-grade frontend interfaces. Avoid generic AI aesthetics.

## Core Principle

Frontend work requires intentional aesthetic direction. Generic "AI slop" (purple gradients, predictable layouts) is unacceptable. Every UI decision should be deliberate and memorable.

Distinctive does not mean decorative. **Everything must earn its place.** Every visible element — every panel, badge, divider, label, shadow, wrapper, and typographic treatment — must justify itself by serving clarity, utility, hierarchy, affordance, state, navigation, content meaning, or domain character. If an element can be removed without reducing comprehension, remove it. The default is removal, not addition. UI furniture — ornamental badges, empty accent panels, fake controls, filler separators, floating chrome, background effects, and decorative typographic treatments like mono small caps sprayed across every label — exists only to make a screenshot look richer. Cut it.

Design the abstraction, not the machinery. Users should see goals, objects, actions, and outcomes from their world, not prompt scaffolds, agent steps, schema names, API mechanics, internal statuses, or implementation vocabulary. Expose diagnostics only when the target user needs them and only behind a clear affordance.

## Aesthetic Direction Template

```markdown
## Aesthetic Direction
- **Tone**: [chosen direction]
- **Memorable element**: [what makes it unforgettable]
- **Typography**: [display font] + [body font]
- **Color strategy**: [dominant + accent approach]
- **Motion philosophy**: [where/how animation is used]
```

## Tone Options

- Brutally minimal
- Maximalist chaos
- Retro-futuristic
- Organic/natural
- Luxury/refined
- Playful/toy-like
- Editorial/magazine
- Brutalist/raw
- Art deco/geometric
- Soft/pastel
- Industrial/utilitarian

## Typography

**Never use:** Roboto, Arial, Instrument Serif, Playfair Display, Poppins, Montserrat.

For the full curated font list — UI fonts, brand fonts, mono, Google Fonts picks, commercial foundries, and proven pairings — see `references/font-recommendations.md`.

**If user has a fonts folder**, check it for available licensed fonts before selecting.

## Icons

Icon rules are owned by `interface/primitives.md` (Icons section): import from the project's existing icon library, or default to Heroicons (Micro/16px in application UIs) when none is established. See that file for sizing and alignment.

**Avoid:** Mixing icon libraries or using low-quality/inconsistent icon sets.

## Color

**Never:** Purple-to-blue gradients on white (AI cliché)

**Do:**
- Commit to a cohesive palette with dominant + sharp accents
- Use CSS variables for consistency
- Consider unexpected color combinations that reinforce the tone

## Motion

See [Animation Patterns Reference](interface/animation.md) for comprehensive guidance.

**Key principles:**
- Focus on high-impact moments (page load, reveals)
- One well-orchestrated animation > scattered micro-interactions
- Every animation must answer: "Why does this exist?"
- Use `ease-out` for entering, `ease-in` for exiting, springs for interactive
- CSS-only when possible; `motion/react` when JS control required

**Quick decisions:**
- Entering screen → ease-out (200ms)
- Interactive elements → spring ({ stiffness: 400, damping: 25 })
- Staggered lists → staggerChildren: 0.03-0.05

## Spatial Composition

- Unexpected layouts, asymmetry, overlap
- Grid-breaking elements
- Generous negative space OR controlled density
- Never predictable/cookie-cutter

## Atmosphere and Character

When the aesthetic direction calls for visual texture, choose treatments that reinforce the product's meaning, interaction model, or brand character:
- Gradient meshes, noise textures, geometric patterns
- Layered transparencies, dramatic shadows
- Custom cursors, grain overlays

Every detail must earn its place. If it can be removed without changing comprehension, priority, or brand character, it's furniture — remove it.

## Implementation Matching

Match code complexity to aesthetic vision:

- **Maximalist design** → elaborate code, extensive animations, rich effects
- **Minimalist design** → restraint, precision, perfect spacing/typography

Elegance = executing the vision fully, not hedging.

## Anti-Patterns

**Generic AI aesthetics to avoid:**
- Roboto/Arial/system-ui defaults
- Purple-to-blue gradients
- White backgrounds with gray cards
- Predictable grid layouts
- Rounded corners on everything
- Mixed or inconsistent icon styles
- Cookie-cutter component patterns
- Safe, forgettable choices

**If you catch yourself making any of these choices, stop and reconsider.**

### Concrete AI Slop Checks

When reviewing or building, scan for these specific code-level tells. See `interface/design.md` → "AI Slop Detection" for the full table.

- `transition-all` → specify exact properties
- `bg-gradient-to-*` used decoratively → justify or remove
- `shadow-[0_0_*]` glow effects → real UIs use shadows for depth, not glow
- Same `rounded-*` / padding / shadow on every card → vary visual weight
- Placeholder text still present (`"Lorem ipsum"`, `"Your text here"`)
- Emoji used as section icons → use actual iconography
- `blur-*` > `blur-xl` on decorative elements → performance cost, no purpose
- Hero → Features → Testimonials → CTA landing page formula → break the mold
- Visible implementation terminology (`schema`, `pipeline`, `agent step`, `vector store`, raw API names) → translate into user goals and domain language unless this is a developer tool where those terms are the user's objects
- Extra wrappers, floating labels, decorative status chips, and nonfunctional panels → remove unless they clarify state, hierarchy, navigation, or affordance

### Content Authenticity

Fabricated content has its own AI fingerprint, independent of visual styling. Scan demo data and copy for these tells:

- Suspiciously round numbers (`99.99%`, `50%`, `$100.00`) → organic values (`47.2%`, `$89`, `18 of 43`)
- Placeholder people ("John Doe", "Jane Smith") and slop brands ("Acme", "Nexus", "SmartFlow") → contextually believable names for the product's domain
- One avatar image reused for every person, identical timestamps on every row → unique avatars, varied dates
- AI copy clichés ("Elevate", "Seamless", "Unleash", "Next-Gen", "Supercharge") → plain, specific language about what the product does
- Micro-copy tells: exclamation marks in success states, "Oops!" in errors, passive voice → confident direct voice ("Connection failed. Try again.")
- Title Case On Every Header → sentence case by default, unless the brand system chose otherwise

## Design Review Checklist

Use this checklist when reviewing UI implementations.

### Red Flags (Fail)

These indicate generic "AI slop" design:

- [ ] Uses Roboto/Arial/system-ui as primary font
- [ ] Purple-to-blue gradient present (the AI cliché)
- [ ] White background + gray cards pattern throughout
- [ ] Uniform rounded corners on everything (no variation)
- [ ] Mixed or inconsistent icon styles across the UI
- [ ] Could be mistaken for any AI-generated landing page
- [ ] No discernible aesthetic direction
- [ ] Cookie-cutter hero → features → testimonials → CTA layout
- [ ] UI furniture present: decorative chrome, filler panels, fake controls, or visual effects with no user-facing purpose
- [ ] Mono small-caps used as a general label style — appearing on section eyebrows, card labels, sidebar headings, tags, or most metadata rather than limited to numeric content and short data-adjacent labels
- [ ] System internals leak into navigation, labels, empty states, errors, or progress copy

### Yellow Flags (Question)

These warrant discussion:

- [ ] No memorable element identified — what makes this stick?
- [ ] Typography pairing unclear or default-feeling
- [ ] Color palette lacks cohesion or intention
- [ ] Motion is scattered micro-interactions, not orchestrated (see [animation.md](interface/animation.md))
- [ ] Spacing feels arbitrary rather than systematic
- [ ] Layout is "safe" — no unexpected decisions
- [ ] Illustrations feel stock rather than curated
- [ ] The design explains how the software works internally instead of what the user can accomplish

### Green Flags (Pass)

These indicate intentional design:

- [ ] Clear aesthetic direction that could be articulated
- [ ] Typography choices are deliberate and create hierarchy
- [ ] Color palette reinforces the intended tone
- [ ] At least one memorable/distinctive element
- [ ] Layout has at least one unexpected decision
- [ ] Spacing is consistent and generous where needed
- [ ] Motion (if present) is purposeful and orchestrated
- [ ] Would not be mistaken for a generic template
- [ ] Every visible element has a purpose tied to comprehension, hierarchy, affordance, state, navigation, or domain meaning
- [ ] Implementation details are translated into user-centered language or intentionally hidden
