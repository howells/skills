# Interface Rules

UI/UX guidelines for building polished, accessible interfaces.

## Rules

| File | Description |
|------|-------------|
| [design.md](design.md) | Visual design principles |
| [colors.md](colors.md) | Color palettes, shade scales, accessibility |
| [spacing.md](spacing.md) | Spacing system, layout methodology |
| [typography.md](typography.md) | Type hierarchy and readability |
| [layout.md](layout.md) | Layout patterns |
| [tailwind-authoring.md](tailwind-authoring.md) | Tailwind class-level authoring discipline |
| [buttons.md](buttons.md) | Button sizing, hierarchy, focus, touch targets |
| [surfaces.md](surfaces.md) | Surface hierarchy, cards, dividers |
| [sections.md](sections.md) | Section composition and cross-section consistency |
| [forms.md](forms.md) | Form design and validation |
| [interactions.md](interactions.md) | User interaction patterns |
| [animation.md](animation.md) | Motion and transitions |
| [performance.md](performance.md) | UI performance optimization |
| [marketing.md](marketing.md) | Marketing page guidelines |
| [app-ui.md](app-ui.md) | App UI guidelines (dashboards, SaaS, data tools) |
| [responsive.md](responsive.md) | Responsive design, input detection, safe areas, tactical breakpoint rules |
| [dark-mode.md](dark-mode.md) | Dark-mode color, surfaces, shadows, images, SVGs |
| [content-accessibility.md](content-accessibility.md) | Accessible content |
| [ui-picker.md](ui-picker.md) | In-browser variant picker for live A/B comparison |

## Component References

Load only the ones present in the work. Small components are grouped into four files; open the file and jump to the `##` anchor named after the component.

| File | Covers (anchors) |
|------|-------------|
| [marketing-components.md](marketing-components.md) | Landing Pages, Headers, Footers, Heading Groups, Feature Lists, Testimonials, Team Sections, Logo Clouds, Login Pages |
| [data-components.md](data-components.md) | Tables, Dashboards, Navigation, Pagination, Description Lists |
| [primitives.md](primitives.md) | Badges, Avatars, Icons, Images, SVG, Border Radius |
| [type-content.md](type-content.md) | Copywriting, Prose Content, Custom Fonts |
| [pricing-cards.md](pricing-cards.md) | Pricing tiers, emphasized plans |

## Related References

| Reference | Description |
|-----------|-------------|
| [design-philosophy.md](../../references/design-philosophy.md) | Timeless design principles |
| [frontend-design.md](../../references/frontend-design.md) | Fonts, component checklist, anti-patterns |
| [ascii-ui-patterns.md](../../references/ascii-ui-patterns.md) | ASCII wireframe patterns |
| [tailwind-v4.md](../../references/tailwind-v4.md) | Tailwind v4 migration guide |
| [brand-identity.md](../../references/brand-identity.md) | Brand and identity typography |
| [typography-opentype.md](../../references/typography-opentype.md) | OpenType features and fine typography |
| [ux-laws.md](../../references/ux-laws.md) | UX heuristics and laws |

## Quick Reference

### When Building UI

1. Check `design.md` for visual principles
2. Check `colors.md` for palette rules
3. Check `spacing.md` for spacing methodology
4. Check `typography.md` for text styling
5. Check `tailwind-authoring.md` before composing class strings
6. Check `buttons.md` / `surfaces.md` / `sections.md` when those patterns appear
7. Check `animation.md` before adding motion

### Accessibility Minimums

- 4.5:1 contrast for normal text
- 3:1 contrast for large text
- Never rely on color alone
- Honor `prefers-reduced-motion`
