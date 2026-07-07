# Spec Templates

Copy-ready skeletons for the two artifacts chiaroscuro produces. Load when writing a Change Spec or a Design Spec; the workflow rules for each live in `SKILL.md`.

## Change Spec

Translate the direction into measurable implementation changes. Use specific values, tokens, class shapes, and component names; reference the local rule or reference file that justifies each meaningful change. If the spec only changes padding, spacing, or copy, stop and deepen the design.

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

## Design Spec

For substantial work, create `docs/design/specs/design-[name].md` using this compact structure. Section-by-section guidance (what belongs in complexity guardrails, abstraction rules, and interactive states) is in `SKILL.md`.

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
