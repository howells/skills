# Brand Identity Reference

Opinionated guidance for creating distinctive visual identities. This reference owns brand-level taste: typography personality, color psychology, visual character. For UI implementation concerns (spacing, states, contrast), see `frontend-design.md`.

---

## Typography for Brand

### The Distinction

**UI fonts** disappear. They serve content without drawing attention — that's their job. Inter, Geist, DM Sans are excellent at this.

**Brand fonts** express. They carry personality in headlines, hero text, wordmarks, and anywhere the brand speaks with its own voice. A brand font should say something about who you are.

A project typically needs both: a brand font for display/identity and a UI font for body/interface. They're different jobs.

### Never Use for Brand Identity

These fonts signal "no one made a choice here":

- **Instrument Serif** — the number one AI-slop serif. Every AI-generated landing page uses it.
- **Playfair Display** — template-tier. Beautiful in isolation, generic in practice.
- **Poppins** — geometric sans that's everywhere. Indistinguishable from a thousand other sites.
- **Montserrat** — massively overexposed. Was distinctive in 2016.
- **Roboto** — Android default. Choosing it says "I didn't choose."
- **Arial** — the non-choice.

### Font Selection and Pairing

For the full curated font list covering both UI and brand fonts — including commercial foundry recommendations, Google Fonts picks, proven pairings, and pairing research guidance — see `references/font-recommendations.md`.

Before committing to any font or pairing, validate with real-world evidence at **fontsinuse.com** and **typewolf.com**.

---

## Color for Brand

### Color Psychology (Beyond the Basics)

The usual "blue = trust, red = urgency" is too shallow. Color meaning depends on context, culture, and the specific shade:

| Hue Range | Can feel | When it works | When it doesn't |
|-----------|----------|---------------|-----------------|
| Deep navy | Authority, depth | Finance, luxury, serious tools | Can feel cold or corporate |
| Warm blue | Approachable expertise | Health, education, productivity | Generic if paired with white + gray |
| Teal/cyan | Fresh, modern | Environmental, wellness, data viz | Overused in 2020-era SaaS |
| Green | Growth, natural, money | Finance, sustainability, health | Can feel clinical or cheap |
| Warm neutrals | Craft, honesty, warmth | Food, hospitality, lifestyle | Can feel boring without an accent |
| Deep amber/orange | Energy, craft, warmth | Creative tools, food, community | Can overwhelm if overused |
| Burgundy/wine | Sophistication, depth | Luxury, editorial, wine/food | Can feel dated without modern typography |
| Black + accent | Boldness, confidence | Fashion, creative, premium | Needs a confident accent to avoid being grim |

### Palettes That Signal "No One Chose"

| Pattern | Why it's generic |
|---------|-----------------|
| Blue + white + gray | Every tech startup's default |
| Purple-to-blue gradient | The AI slop gradient. Avoid entirely. |
| Teal + coral together | 2020 SaaS template era. Either alone is fine. |
| Indigo + pink | Dribbble trend, now everywhere |
| All neutrals + one blue accent | Safe, forgettable, says nothing |

### Building a Brand Palette

1. **Start with meaning.** Why this hue? What does it connect to in the brand's world?
2. **Commit to a dominant color.** Not a gradient, not a split — one confident hue that owns the brand.
3. **Add tension with an accent.** The accent should create visual interest, not just complement. Complementary hues (opposite on the color wheel) create energy.
4. **Derive, don't pick.** Tinted neutrals should carry a hint of the brand hue. Semantic colors (success, error) should harmonize, not clash.
5. **Generate full scales.** Every brand color needs a 50-900 scale in OKLCH for UI application.

### OKLCH for Brand Work

Always define brand colors in OKLCH (perceptually uniform):
- **L** (lightness): 0-1, consistent perceived brightness
- **C** (chroma): 0-0.4, saturation intensity
- **H** (hue): 0-360, position on the color wheel

OKLCH ensures shade scales look visually even. Hex/HSL scales often have perceptual jumps (e.g., blue shades that suddenly look purple at high lightness).

---

## Visual Character

### Beyond the Defaults

Most AI-generated UI uses the same visual character: medium border radius, subtle shadows, white backgrounds, gray cards. A brand's visual character should be as intentional as its color and typography.

Dimensions to decide:

| Dimension | Spectrum | Questions to ask |
|-----------|----------|-----------------|
| **Corners** | Sharp ↔ Rounded | All the same, or mixed? Sharp cards + round buttons = interesting tension. |
| **Shadows** | None ↔ Dramatic | Flat design? Subtle elevation? Dramatic layered shadows? |
| **Borders** | None ↔ Prominent | Is structure shown through borders, spacing, or background color? |
| **Density** | Airy ↔ Dense | Generous whitespace or information-rich? |
| **Texture** | Flat ↔ Rich | Pure flat color? Grain? Noise? Gradients? Patterns? |
| **Motion** | Still ↔ Expressive | Minimal transitions or choreographed animation? |

### Visual Character Prompts

Use these to push past safe defaults:

- "What if only *some* things are rounded? Sharp cards with round buttons creates tension."
- "What if no shadows at all? Or dramatic, layered shadows instead of subtle everywhere?"
- "What if the surface has color or texture instead of white + gray cards?"
- "What if borders are the character — thick, thin, dotted, or absent entirely?"
- "What would this brand look like if it were brave?"

---

## Brand Voice (Brief)

Visual identity and verbal identity should align. A few key decisions:

| Decision | Options |
|----------|---------|
| **Capitalization** | Sentence case (casual, modern) / Title Case (traditional, formal) / lowercase (tech, casual) / UPPERCASE (bold, brand marks only) |
| **Tone** | Concise + direct / Conversational + warm / Formal + precise / Playful + witty |
| **Terminology** | Does the brand have specific words it uses or avoids? |

---

## What Makes a Brand Distinctive

A brand is distinctive when:
1. **You can describe it without seeing it.** "Warm editorial with deep amber and a serif" vs "clean and modern."
2. **Swapping the logo doesn't make it generic.** The palette, type, and character carry the identity.
3. **It has a tension.** Accessible + authoritative. Playful + precise. Raw + refined.
4. **Someone would remember it.** After seeing it once, could they describe what made it different?

If the answer to any of these is "no" — push harder.
