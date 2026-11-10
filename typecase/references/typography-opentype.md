# Typography and OpenType

How text renders inside the roles: rendering, features, tracking and loading.

Contents: rendering · OpenType features · tracking · loading.

## Rendering

The biggest levers are the font and the layout, not CSS tweaks.

- **Pixel density beats everything.** On a 2x display plain grayscale antialiasing is the good rendering. Design on 2x; check weight and contrast on a 1x screen before shipping.
- **`antialiased` once, on the root** (Tailwind sets both `-webkit-font-smoothing` and `-moz-osx-font-smoothing`), never per component. At 1x, light text on dark can go too thin: bump that role's weight a step rather than dropping `antialiased`.
- **Never set `text-rendering: optimizeLegibility`.** Kerning and common ligatures are already on, and it costs layout time on long pages.
- **Optical sizing is on by default** (`font-optical-sizing: auto` is the initial value). It only works when the loaded font has an `opsz` axis: InterVariable, Source Serif 4, Fraunces, Newsreader, Roboto Flex. Static-weight imports such as `Inter({ weight: ['400','700'] })` drop the axis. Do not hard-code `"opsz"` in `font-variation-settings` unless the design deliberately decouples optical size from font size. If the variable font has `opsz`, a separate display cut (Inter Tight) may be redundant.
- **Inter means InterVariable**, self-hosted from rsms.me with `next/font/local` (`InterVariable.woff2` plus the italic). Google's build has stripped some cv/ss features; if staying on Google Fonts, request the axis: `Inter({ subsets: ['latin'], axes: ['opsz'] })`.
- **Text and Display cuts.** "Display" in a family name means a cut drawn for large sizes (SF Pro Display, Heldane Display). Use the cut that matches the role's size.

## OpenType features

Use the property where one exists: `font-weight: 650`, not `font-variation-settings: "wght" 650`; `font-variant-numeric: tabular-nums`, not `font-feature-settings: "tnum"`. Properties keep working when a non-variable fallback renders. Keep `font-feature-settings` for features with no property, such as `cv05` or `ss01`.

### Figures

| Property value | Effect | Use for |
| --- | --- | --- |
| `tabular-nums` | Fixed-width digits | Prices, timers, counters, metrics, numeric columns, anything that changes |
| `lining-nums` | Cap-height digits | Tables, UI |
| `oldstyle-nums` | Digits with ascenders and descenders | Running editorial text, if the font has them |
| `diagonal-fractions` | ½ | Recipes, measurements |
| `slashed-zero` | 0 with a slash | Codes, keys, tables mixing O and 0 |

Without `tabular-nums`, a changing number shifts layout because `1` is narrower than `0`. Leave figures in prose proportional.

### Ligatures

Common ligatures are on by default. Turn them off in code: `code, pre { font-variant-ligatures: none; }`, since `fi` as one glyph misleads in code.

### Small caps

Not a UI treatment (see the SKILL.md rules). Where a brand treatment or the user calls for them, use `font-variant-caps: small-caps` only on a font with drawn small-cap glyphs; scaled capitals look wrong. A small-caps wordmark does not license small-caps navigation, captions or buttons.

### Character variants and stylistic sets (InterVariable)

| Feature | Effect | Use when |
| --- | --- | --- |
| `cv05` | `l` with a tail | Codes and IDs: separates `I`, `l` and `1` |
| `cv11` | Single-storey `a` | Softer, more geometric voice |
| `ss01` | Open digits | Dense dashboards |
| `ss02` | Disambiguation set: serifed I, slashed 0, tailed l | Licence keys, technical output |
| `ss03` | Round quotes and commas | Editorial and marketing |
| `case` | Case-sensitive punctuation | Caps-only text; usually automatic via `calt` |

Set one to three globally on the font token so every use carries them; a per-component patchwork of glyph shapes is a bug.

```css
@theme {
  --font-sans: "InterVariable", ui-sans-serif, system-ui, sans-serif;
  --font-sans--font-feature-settings: "cv05", "ss03";
}
```

Per-element overrides only for a scoped need: `<code class="[font-feature-settings:'ss02','zero']">`.

## Tracking

Kerning is built into the font and on by default; `font-kerning: none` is never a fix. Tracking tightens as size grows. Inter's own curve is `tracking ≈ -0.0223 + 0.185·e^(-0.1745·px)`; a stepped scale is fine.

Use `em`, never `px`, so tracking scales with size. Bind it to the size token so the step brings its tracking with it:

```css
@theme {
  --text-6xl: 3.75rem;
  --text-6xl--line-height: 1.1;
  --text-6xl--letter-spacing: -0.025em;
}
```

## Loading

| `font-display` | Behaviour | Use for |
| --- | --- | --- |
| `swap` | Fallback at once, swap when ready | Body text |
| `optional` | Fallback unless cached, no swap | Performance-critical pages |
| `block` | Brief invisible period, then swap | Short display or brand text |

Preload only the one or two faces the first screen needs (`<link rel="preload" as="font" type="font/woff2" crossorigin>`). Match the fallback's metrics with `size-adjust`, `ascent-override`, `descent-override` and `line-gap-override` on a local fallback `@font-face` so the swap does not reflow; Fontaine and `next/font` calculate them. Serve `woff2`. Subset with `unicode-range` (`next/font` does it automatically). Load every weight and style the roles use: a missing face is synthesised, and `font-synthesis: none` on body text hides the symptom by breaking the fallback.
