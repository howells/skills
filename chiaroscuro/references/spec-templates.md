# Spec Templates

Copy-ready skeletons for optional design artifacts. Load only when the user or project asks for a Change Spec or Design Spec; ordinary implementation does not produce either automatically.

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

When a saved Design Spec is required, follow the project's documentation location or use `docs/design/specs/design-[name].md` when no convention exists. Adapt this compact structure to the work rather than filling sections that do not apply.

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
