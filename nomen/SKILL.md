---
name: nomen
description: Generate and validate project, product, app, package, CLI, brand, or feature names using systematic naming strategies, codebase context, domain checks, GitHub or package conflict checks, App Store / app-directory checks, and web research. Use when naming a new project, renaming an existing one, validating a name, checking availability, or generating alternatives with ranked recommendations.
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
- **App stores** — check whenever the thing being named is, or might become, a mobile
  or desktop app (see "App Store checks" below). This is easy to forget and expensive
  to miss: an App Store name collision blocks public release, and a name can be free on
  npm/domains yet already be a shipped app.
- Product directories (Product Hunt, app store category listings) for the crowded case.
- Trademark databases only when the user explicitly needs that level of signal.

### App Store checks

Apple's public iTunes Search API needs no key and answers in one request:

```
curl -s "https://itunes.apple.com/search?term=NAME&entity=software&limit=20&country=us"
```

From the JSON `results[]`, inspect each `trackName` / `sellerName` and report:

- an **exact** name match (`trackName` == the name) → the App Store name is taken;
- **prefix** matches (`trackName` starts with `NAME `, `NAME:`, `NAME -`) → close collisions;
- **category saturation** — many apps whose names merely *contain* the word (e.g. a dozen
  "clipping" apps). Even with the bare name free, a saturated category means the name is
  not distinctive and is worth flagging.

For Android, a web search for `NAME site:play.google.com` is the pragmatic equivalent.

### Verify, don't trust a single lookup

Availability APIs lie — RDAP/WHOIS services rate-limit and return false "available" for
domains that are in fact registered and serving. Before claiming a domain is free,
cross-check: a live `curl -s -o /dev/null -w "%{http_code}" https://NAME.TLD` that returns
`200`/`301`/`302` means it is taken regardless of what RDAP said; a `dig +short NAME.TLD NS`
with no nameservers is a stronger "unregistered" signal than an RDAP `404` alone. When two
signals disagree, trust the one showing the name is *taken*.

Use cautious language:

- Say "no obvious conflict found" when searches are clean.
- Say "likely unavailable" when the domain, package, or app store name appears taken.
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
- If the thing is or could become an app, the App Store (and Play Store when relevant) was checked, not just npm/domains.
- Availability claims were cross-checked (not a single RDAP/WHOIS call), especially any "available" verdict.
- The recommendation explains tradeoffs.
- Any unresolved legal, domain, or package questions are explicit.
