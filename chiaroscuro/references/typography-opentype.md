# Typography & OpenType Reference

Advanced typography features for polished, professional interfaces. Companion to `interface/typography.md` for baseline rules.

---

## The Rendering Stack

"Gorgeous text rendering" is not one property — it's a stack of decisions, ordered here by how much each actually contributes. The highest-impact levers are font choice and layout discipline, not CSS tweaks.

### 1. Pixel density beats everything

On a 2x/Retina display, plain grayscale antialiasing *is* the gorgeous rendering — hinting and subpixel tricks stop mattering (Apple deleted subpixel AA entirely in macOS Mojave). Nothing in CSS matches the jump from 1x to 2x. Consequence: design and QA type on a 2x display, but verify weight/contrast on a 1x display before shipping.

### 2. Grayscale antialiasing

```html
<body class="antialiased">
```

Tailwind's `antialiased` sets `-webkit-font-smoothing: antialiased` + `-moz-osx-font-smoothing: grayscale`. Text renders thinner and crisper than the default (which dilates stems), matching Figma and Apple's own UI. The one real trade-off: at 1x DPI, light text on dark backgrounds can go too thin — fix by bumping `font-medium` → `font-semibold` on those surfaces, never by dropping `antialiased`.

Do **not** add `text-rendering: optimizeLegibility` — kerning and common ligatures are on by default in modern browsers, and it still costs layout time on long pages.

### 3. Optical sizing

The most under-used lever. Fonts drawn for text sizes have wider spacing, taller x-heights, sturdier hairlines; display cuts are tighter and more elegant. A variable font with an `opsz` axis interpolates this continuously:

```css
/* Tailwind has no utility for this — set once in base */
@layer base {
  body { font-optical-sizing: auto; }
}
```

- Requires a font with an `opsz` axis (InterVariable 4.0+, Source Serif 4, Fraunces, Roboto Flex, Newsreader). Static-weight imports (e.g. `next/font/google` `Inter({ weight: ['400','700'] })`) don't carry the axis — load the variable font.
- **If the project uses Inter, use InterVariable** — the canonical variable build from rsms.me/inter. It carries the `opsz` axis *and* the complete OpenType feature set (character variants + stylistic sets — see § Character Variants below); Google Fonts' build pipeline has historically stripped some of these. Self-host via `next/font/local` with `InterVariable.woff2` (+ `InterVariable-Italic.woff2`), or if staying on Google Fonts, request the axis explicitly: `Inter({ subsets: ['latin'], axes: ['opsz'] })`.
- A text/display *pairing* (e.g. Inter + Inter Tight) is the manual version of optical sizing. If the variable font has `opsz`, the display cut may be redundant.

### 4. Tracking tuned per size

Tracking must tighten as size grows. The reference curve is Inter's dynamic metrics formula (`tracking ≈ -0.0223 + 0.185·e^(-0.1745·px)`); in practice a stepped scale is fine — see the Manual Tracking table under Kerning below. In Tailwind, bind tracking into the type scale via `@theme` so `text-6xl` brings its tracking with it rather than relying on authors to remember `tracking-tight`:

```css
@theme {
  --text-6xl: 3.75rem;
  --text-6xl--line-height: 1.1;
  --text-6xl--letter-spacing: -0.025em;
}
```

### 5. OpenType features

Kerning and common ligatures are on by default. Opt into the extras — `tabular-nums` for anything numeric that aligns or changes, `slashed-zero` for codes, stylistic sets where the font offers them. Full detail in the sections below.

### 6. Layout-level polish

The newest tier, all cheap wins:

```html
<h1 class="text-balance">…</h1>          <!-- no orphan word on line two -->
<p class="text-pretty">…</p>             <!-- better rag, fewer orphans -->
<blockquote class="[hanging-punctuation:first]">…</blockquote>  <!-- Safari: quotes hang into margin -->
<div class="hyphens-auto" lang="en">…</div>  <!-- needs a correct lang attribute -->
```

And the part no property can do: measure ~45–75 characters per line, line-height tightening as size grows (1.5 at 16px → ~1.1 at 60px — table under Line Height Relationships below).

### The stack, condensed

```html
<body class="antialiased">  <!-- + font-optical-sizing: auto in @layer base -->
```

```
RENDERED ON        → 2x display, verified at 1x
FONT               → variable, with opsz axis where possible (Inter → InterVariable, always)
SMOOTHING          → antialiased (Tailwind), weight bump on dark 1x surfaces
OPTICAL SIZING     → font-optical-sizing: auto (base layer)
TRACKING           → bound to type scale via @theme, tighter as size grows
FEATURES           → tabular-nums etc. — see below
WRAPPING           → text-balance / text-pretty / hanging-punctuation
MEASURE & LEADING  → 45–75ch; line-height falls as size rises
```

---

## OpenType Feature Settings

OpenType features unlock professional typographic refinements. Use `font-feature-settings` for fine control or `font-variant-*` for standardized features.

### Numeric Formatting

| Feature | Property | Effect | Use When |
|---------|----------|--------|----------|
| `tnum` | `font-variant-numeric: tabular-nums` | Fixed-width digits | Data tables, prices, timers, counters |
| `lnum` | `font-variant-numeric: lining-nums` | Uniform height digits | Tables, UI elements |
| `onum` | `font-variant-numeric: oldstyle-nums` | Varying height digits | Running body text, editorial |
| `frac` | `font-variant-numeric: diagonal-fractions` | Proper fractions (½) | Recipes, measurements |
| `ordn` | `font-variant-numeric: ordinal` | Ordinal indicators (1st) | Dates, rankings |

```css
/* Data tables — digits align vertically */
.data-cell {
  font-variant-numeric: tabular-nums lining-nums;
}

/* Tailwind */
<td class="tabular-nums">1,234.56</td>

/* Body text — digits blend with lowercase */
.prose {
  font-variant-numeric: oldstyle-nums proportional-nums;
}
```

**Most important rule:** Always use `tabular-nums` for:
- Prices and currency
- Timers and countdowns
- Table columns with numbers
- Statistics and metrics
- Any numbers that animate or change

Without `tabular-nums`, changing digits cause layout shift because `1` is narrower than `0`.

### Ligatures

| Feature | Property | Effect |
|---------|----------|--------|
| `liga` | `font-variant-ligatures: common-ligatures` | Standard ligatures (fi, fl) |
| `dlig` | `font-variant-ligatures: discretionary-ligatures` | Decorative ligatures |
| `clig` | `font-variant-ligatures: contextual` | Context-dependent connections |

```css
/* Enable standard ligatures (usually on by default) */
body {
  font-variant-ligatures: common-ligatures;
}

/* Disable ligatures in code */
code, pre {
  font-variant-ligatures: none;
}
```

**Always disable ligatures in monospace/code text.** `fi` as a ligature in code is misleading.

### Small Caps

```css
/* True small caps (not fake scaled-down capitals) */
.small-caps {
  font-variant-caps: small-caps;
}

/* Appropriate: numeric content, abbreviations, short data labels */
<span class="small-caps">NASA</span>
<time class="small-caps">3:45 PM</time>
<span class="small-caps">v2.4.1</span>
```

Only use if the font has designed small cap glyphs. Faked small caps (scaled capitals) look bad.

### Character Variants & Stylistic Sets (Inter / InterVariable)

InterVariable ships a large set of `cv`/`ss` features — one of the strongest reasons to use the rsms.me build over a stripped CDN copy. The high-value ones for interfaces:

| Feature | Effect | Use When |
|---------|--------|----------|
| `cv05` | Lowercase `l` with tail | Any UI showing codes/IDs — disambiguates `I`/`l`/`1` |
| `cv11` | Single-storey `a` | Softer, more geometric personality |
| `ss01` | Open digits (alternate 0, 6, 9) | Data-dense UI, dashboards |
| `ss02` | Disambiguation set (serifed I, slashed 0, tailed l) | Codes, license keys, technical output |
| `ss03` | Round quotes & commas | Editorial/marketing surfaces |
| `zero` | Slashed zero only | Tables mixing O and 0 |
| `case` | Case-sensitive punctuation (raised hyphens/brackets in ALL CAPS) | Auto via `calt` in most cases; force for caps-only labels |

Wire features into the font token in Tailwind v4 so every use of `font-sans` gets them — don't sprinkle arbitrary properties per element:

```css
@theme {
  --font-sans: "InterVariable", ui-sans-serif, system-ui, sans-serif;
  --font-sans--font-feature-settings: "cv05", "ss03";
  --font-sans--font-variation-settings: normal;
}
```

Per-element overrides only for scoped needs:

```html
<code class="[font-feature-settings:'ss02','zero']">4f7I-l0O1</code>
```

Pick 1–3 features that suit the brand and set them globally. A different `a` or `l` across the whole product is a quiet personality decision; a per-component patchwork of glyph styles is a bug.

**Restraint is critical.** Small caps (especially mono small caps) are a high-signal typographic treatment for numeric content, abbreviations, and short data-adjacent labels. They are not a default style for every label, eyebrow, tag, or metadata field. When small caps appear on more than a few elements per screen, the treatment loses its signal and becomes decorative noise. Before applying, ask: would sentence-case in the body font at a lighter weight work just as well? If yes, use that instead.

---

## Kerning

```css
/* Enable font-level kerning */
body {
  font-kerning: normal;
}

/* Tailwind */
<h1 class="tracking-tight">Tight Headlines</h1>
```

### Manual Tracking Adjustments

| Context | Tracking | Why |
|---------|----------|-----|
| Large display text (>48px) | Tighter (`-0.02em` to `-0.04em`) | Large text has too much visual space |
| Body text (14-18px) | Default (0) | Designed for this range |
| Small text (<12px) | Looser (`0.01em` to `0.02em`) | Improves legibility at small sizes |
| All caps (when justified) | Looser (`0.05em` to `0.1em`) | Caps need more breathing room |
| Short caps UI text (rare) | Looser (`0.02em` to `0.05em`) | Improves readability when caps are used |

```css
/* Headline */
h1 { letter-spacing: -0.02em; }

/* When uppercase is justified (not a default — see typography.md rules) */
.mono-eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

---

## Text Wrapping

### `text-wrap` Values

| Value | Use For | Effect |
|-------|---------|--------|
| `balance` | Headings, short text | Evenly distributes text across lines |
| `pretty` | Body paragraphs | Avoids orphaned words on last line |
| `stable` | Editable content | Doesn't reflow as user types |

```css
/* Headings: balanced wrapping */
h1, h2, h3 {
  text-wrap: balance;
}

/* Body: avoid orphans */
p {
  text-wrap: pretty;
}
```

```html
<!-- Tailwind -->
<h1 class="text-balance">A heading that wraps nicely across lines</h1>
<p class="text-pretty">Body text that avoids leaving a single word on the last line</p>
```

**Performance note:** `text-wrap: balance` has a performance cost on very long text (it tries multiple layouts). Only use on headings and short text blocks, not on entire pages of prose.

### Hyphenation

```css
/* Enable hyphenation for narrow columns */
.narrow-column {
  hyphens: auto;
  -webkit-hyphens: auto;
  overflow-wrap: break-word;
}
```

Use hyphenation for:
- Narrow sidebar text
- Mobile layouts where words exceed container width
- Multi-column layouts

Avoid for:
- Headlines (use `text-balance` instead)
- Code or technical terms
- Short labels

---

## Line Height Relationships

Line height should relate to the type scale:

| Text Size | Line Height | Ratio |
|-----------|-------------|-------|
| 12px (xs) | 16px | 1.33 |
| 14px (sm) | 20px | 1.43 |
| 16px (base) | 24px | 1.5 |
| 18px (lg) | 28px | 1.56 |
| 20px (xl) | 28px | 1.4 |
| 24px (2xl) | 32px | 1.33 |
| 30px (3xl) | 36px | 1.2 |
| 36px (4xl) | 40px | 1.11 |
| 48px (5xl) | 48px | 1.0 |
| 60px+ | 1.0–1.1 | Nearly solid |

**Pattern:** As text gets larger, line height ratio decreases. Large display text at 1.5 line height looks excessively spaced.

---

## Viewport-Based Sizing

Use `clamp()` for responsive typography without breakpoints:

```css
/* Fluid heading: 24px at 320px viewport, 48px at 1440px */
h1 {
  font-size: clamp(1.5rem, 1rem + 2vw, 3rem);
}

/* Fluid body: 14px minimum, 18px maximum */
body {
  font-size: clamp(0.875rem, 0.8rem + 0.25vw, 1.125rem);
}
```

**Rules:**
- Always set a minimum (`clamp` first value) — viewport units alone can make text unreadable on small screens
- Always set a maximum — text shouldn't grow forever on large screens
- Body text range: 14px–18px
- Heading text range: 24px–64px depending on hierarchy level

---

## Performance

### Font Loading Strategy

```css
/* Prevent FOIT (Flash of Invisible Text) */
@font-face {
  font-family: "Custom Font";
  src: url("/fonts/custom.woff2") format("woff2");
  font-display: swap; /* Show fallback immediately, swap when loaded */
}
```

| `font-display` | Behavior | Use When |
|----------------|----------|----------|
| `swap` | Fallback immediately, swap when ready | Body text (readability > style) |
| `optional` | Fallback if not cached, no swap | Performance-critical pages |
| `block` | Brief invisible period, then swap | Display/brand fonts (short text) |

### Subsetting

Only load the characters you need:

```css
/* Latin-only subset */
@font-face {
  unicode-range: U+0000-00FF, U+0131, U+0152-0153;
}
```

Next.js `next/font` handles subsetting automatically.

---

## Quick Reference

```
FONT SMOOTHING        → antialiased on body (always; weight bump on dark 1x)
OPTICAL SIZING        → font-optical-sizing: auto + opsz variable font
text-rendering        → never set optimizeLegibility (redundant + slow)
NUMBERS IN TABLES     → tabular-nums (always)
NUMBERS IN PROSE      → oldstyle-nums (if font supports)
LIGATURES IN CODE     → disabled (always)
LARGE HEADINGS        → tighter tracking (-0.02em)
ALL CAPS              → wider tracking (+0.05em)
HEADINGS WRAPPING     → text-balance
BODY WRAPPING         → text-pretty
LINE HEIGHT           → decreases as text size increases
FLUID SIZING          → clamp(min, preferred, max)
FONT DISPLAY          → swap for body, optional for perf-critical
```
