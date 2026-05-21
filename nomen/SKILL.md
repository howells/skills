---
name: nomen
description: Generate and validate project, product, app, package, CLI, brand, or feature names using systematic naming strategies, codebase context, domain checks, GitHub or package conflict checks, and web research. Use when naming a new project, renaming an existing one, validating a name, checking availability, or generating alternatives with ranked recommendations.
---

# Nomen

Use this skill to generate, critique, and validate names for projects, products, apps, packages, CLIs, features, teams, or brands.

Name availability changes over time. When validating real candidates, search current sources before making claims about conflicts, package names, domains, or trademarks. Treat availability checks as evidence, not legal advice.

## References

Load `references/name-strategies.md` when generating candidates or explaining the naming approach.

## Start

When invoked:

1. State that you are using the `nomen` skill.
2. Determine whether the user wants generation, validation, renaming, or critique.
3. If working in a codebase, inspect relevant context first:
   - `README.md`
   - `package.json`
   - `docs/vision.md`
   - `docs/brand-system.md`
   - app, package, command, and domain folder names
   - existing public names, product copy, and environment prefixes
4. Ask only for missing constraints that materially change the name space.

Useful questions:

- What is being named?
- Who is it for?
- Should it feel technical, editorial, premium, playful, utilitarian, or institutional?
- Are there words, sounds, languages, or categories to avoid?
- Does it need a domain, package name, CLI binary, social handle, or legal clearance?

Ask one question at a time when blocked. If not blocked, proceed with stated assumptions.

## Generate Mode

Generate 8-12 serious candidates unless the user requests a smaller set. Use multiple strategies rather than one pattern:

- Verb names.
- Metaphor names.
- Compound names.
- Short-word names.
- Portmanteau names.
- Prefix or suffix variants.
- Domain-specific references.
- Names with strong sound or rhythm.

For each candidate, include:

- The strategy used.
- Why it fits the product.
- Pronunciation or spelling risk.
- Tone and category fit.
- Obvious conflict risk before deeper validation.

Avoid filler. Do not include joke names unless the user asks for them.

## Validate Mode

When validating names, check current sources appropriate to the request:

- General web search for exact name and adjacent terms.
- GitHub repository and organization conflicts when developer-facing.
- Package registries when relevant, such as npm, PyPI, crates.io, or RubyGems.
- Domain and DNS signals for requested TLDs.
- App stores or product directories when relevant.
- Trademark databases only when the user explicitly needs that level of signal.

Use cautious language:

- Say "no obvious conflict found" when searches are clean.
- Say "likely unavailable" when the domain or package appears taken.
- Do not say a name is legally available unless a qualified trademark check has been done.
- Do not buy, register, reserve, or claim anything without explicit user approval.

## Output

Present results as a ranked shortlist. For each finalist, include:

- Name.
- Rationale.
- Fit.
- Risks.
- Validation evidence.
- Suggested next action.

End with a clear recommendation, not an undifferentiated list.

## Rename Mode

When renaming an existing project:

1. Identify public surfaces that would need to change, such as package names, CLI commands, docs, env prefixes, API identifiers, app titles, and repository names.
2. Separate brand rename work from technical migration work.
3. Do not change identifiers unless the user explicitly asks for implementation.
4. If implementation is requested, update all usage sites canonically rather than adding aliases or compatibility shims.

## Completion Check

Before finishing, verify that:

- Candidates reflect the product and audience.
- At least three naming strategies were used.
- Validation claims are current and properly caveated.
- The recommendation explains tradeoffs.
- Any unresolved legal, domain, or package questions are explicit.
