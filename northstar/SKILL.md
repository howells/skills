---
name: northstar
description: Create, review, or revise a concise project vision document that captures what a project is, who it is for, why it exists, success criteria, constraints, non-goals, and decision principles. Use when starting a new project, clarifying product direction, aligning a codebase for future agent work, defining a north star, or turning a vague idea into docs/vision.md.
---

# Northstar

Use this skill to turn a vague product, codebase, or initiative into a clear project vision. The output should be useful to future humans and agents: specific enough to guide decisions, short enough to be read, and honest about constraints.

## Start

When invoked:

1. State that you are using the `northstar` skill.
2. Determine whether the user wants to create, review, or revise a vision.
3. If working in a codebase, inspect existing context before asking questions:
   - `docs/vision.md`
   - `README.md`
   - `AGENTS.md`
   - `docs/brand-system.md`
   - `docs/design-context.md`
   - `package.json`
   - app, package, or domain folder names that reveal the product shape
4. If the product direction is still unclear, ask one focused question at a time.

Useful questions:

- What is the project?
- Who is it for?
- What problem does it solve?
- What should be true if it succeeds?
- What should it deliberately not become?
- What tradeoffs should future decisions respect?

Do not run a long interview if the available context is enough to draft a credible first version.

## Output

Create or update `docs/vision.md` by default unless the user specifies another path.

Use this structure unless the project already has a better local convention:

```markdown
# Vision

## What This Is

## Who It Serves

## Why It Exists

## Success

## Principles

## Non-Goals

## Open Questions
```

Keep the document direct. Prefer concrete nouns and decision language over marketing claims. A good vision document normally fits in 500-900 words.

## Writing Rules

- Describe the actual product, audience, and value, not a generic category.
- Include non-goals. A vision without boundaries is not operational.
- Include decision principles that can resolve future tradeoffs.
- Separate facts from assumptions when the codebase or user input does not fully support a claim.
- Avoid hype phrases such as "revolutionary", "seamless", "cutting-edge", or "delightful" unless the product context proves they are precise.
- Do not invent business metrics, customer segments, or compliance requirements.
- Do not add broad documentation files beyond the requested vision artifact.

## Review Mode

When reviewing an existing vision, lead with issues:

1. Missing or vague audience.
2. Unclear problem statement.
3. No measurable success criteria.
4. No non-goals or constraints.
5. Claims contradicted by the codebase.
6. Language too generic to guide implementation.

If the user asked only for a review, do not overwrite the file. Provide findings and a proposed revision excerpt instead.

## Completion Check

Before finishing, verify that the vision:

- Names the product and audience.
- Explains why the project exists.
- Gives future agents enough context to make implementation decisions.
- Includes non-goals or constraints.
- Lists open questions when the vision depends on unresolved assumptions.
