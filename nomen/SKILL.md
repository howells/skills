---
name: nomen
description: "Generate, critique, and validate names for products, projects, packages, CLIs, apps, brands, or features, with domain, package, GitHub, App Store and web conflict checks. Use for naming and renaming decisions. Not for interface labels (`signage`), body prose (`deslop`), or legal clearance."
---

# Nomen

Use this skill to generate, critique, and validate names for projects, products, apps, packages, CLIs, features, teams, or brands.

Name availability changes over time. When validating real candidates, search current sources before making claims about conflicts, package names, domains, or trademarks. Treat availability checks as evidence, not legal advice.

## References

Load `references/name-strategies.md` when generating candidates, explaining the naming approach, or validating a name (its Validation Caveats section applies to Validate Mode).

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

When validating names, check current sources appropriate to the request. For every provider or registry, network, authentication and rate-limit failures mean unknown, not available. Distinguish an authoritative not-found response from a failed lookup:

- General web search for exact name and adjacent terms.
- GitHub repository and organization conflicts when developer-facing. Concretely: `gh api "repos/OWNER/NAME"` (200 = an existing repository; 404 = not visible to this credential, which can include private repositories) for an exact owner/name, and `gh search repos NAME --limit 20` to gauge how crowded the name is.
- Package registries when relevant. Concretely: `npm view NAME name` (inspect a registry-specific not-found response; network, authentication and rate-limit failures mean unknown, not unpublished), `pip index versions NAME`, `cargo search NAME`, or a `gem list -r -e NAME`. **A registry 404 does not mean the name is registrable** - npm rejects names too similar to existing packages (punctuation/typo-squat rules), and spam-reserved or unpublished names also 404. Treat 404 as "not currently published," not "yours to claim."
- Domain and DNS signals for requested TLDs.
- **App stores** - check whenever the thing being named is, or might become, a mobile
  or desktop app (see "App Store checks" below). This is easy to forget and expensive
  to miss: an App Store name collision blocks public release, and a name can be free on
  npm/domains yet already be a shipped app.
- Product directories (Product Hunt, app store category listings) for the crowded case.
- Trademark databases only when the user explicitly needs that level of signal.

### App Store Checks

Apple's public iTunes Search API needs no key. Select the entity for the target: `software` for iPhone apps, `iPadSoftware` for iPad apps, and `macSoftware` for Mac apps; query each relevant platform. Report the platform, country and lookup date. Search results are conflict signals, not proof of registrability. If the result reaches the requested limit, broaden or refine the search rather than claiming complete coverage. URL-encode the term (a raw space silently truncates the query) and widen `country` beyond `us` if the app targets other regions - region-exclusive apps won't otherwise appear:

```
curl -s -G "https://itunes.apple.com/search" \
  --data-urlencode "term=NAME" \
  --data "entity=software&limit=20&country=us"
```

From the JSON `results[]`, inspect each `trackName` / `sellerName` and report:

- an **exact** name match (`trackName` equals the name, compared case-insensitively - the App Store treats "Clipper" and "clipper" as the same collision) → the App Store name is taken;
- **prefix** matches (`trackName` starts with `NAME `, `NAME:`, `NAME -`) → close collisions;
- **category saturation** - many apps whose names merely *contain* the word (e.g. a dozen
  "clipping" apps). Even with the bare name free, a saturated category means the name is
  not distinctive and is worth flagging.

For Android, a web search for `NAME site:play.google.com` is the pragmatic equivalent.

### Verify, Don't Trust A Single Lookup

Use an authoritative registry RDAP or registrar lookup for registration status, and inspect errors rather than treating every failed response as not found. DNS and HTTP are supporting evidence of use, not availability checks. A working site is strong evidence the domain is in use; an empty `dig +short NAME.TLD NS` result does not establish that it is unregistered. Registered domains can lack delegation ([ICANN status definitions](https://www.icann.org/resources/pages/epp-status-codes-2014-06-16-en)). When signals conflict or the registry lookup fails, report status as unresolved and preserve evidence of existing use. Even an unregistered domain may be reserved or otherwise unavailable to register.

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
4. If implementation is requested, update in-scope usage sites to the chosen name. Preserve supported external contracts until their migration is authorized; a brand rename alone does not authorize breaking published identifiers.

## Completion Check

Before finishing, verify that:

- Candidates reflect the product and audience.
- At least three naming strategies were used.
- Validation claims are current and properly caveated.
- If the thing is or could become an app, the App Store (and Play Store when relevant) was checked, not just npm/domains.
- Availability claims were cross-checked (not a single RDAP/WHOIS call), especially any "available" verdict.
- The recommendation explains tradeoffs.
- Any unresolved legal, domain, or package questions are explicit.
