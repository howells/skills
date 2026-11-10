---
name: nomen
description: "Generate, critique and check names for products, packages, CLIs, apps or features, with domain, registry, GitHub, App Store and web conflict checks. Use when one of these needs a name or a rename. Not for interface labels (`signage`) or legal clearance."
---

# Nomen

## Rules

- **A failed lookup is unknown, never available.** Network, auth and rate-limit errors prove nothing. Tell an authoritative not-found apart from a failed call.
- **Not published is not claimable.** A registry 404 can hide a reserved, unpublished or too-similar name; a GitHub 404 can be a private repository; an empty `dig` can be a registered, undelegated domain.
- **Check the app stores whenever it is, or might become, an app.** A name free on npm and domains can already be a shipped app, and an App Store collision blocks release.
- **Say "no obvious conflict found", never "available".** Never call a name legally clear; that needs a trademark search the user asked for.
- **Never buy, register, reserve or publish anything** without the user's say-so.

## Context

In a codebase, read the README, `package.json`, any vision or brand docs, and the existing app, package, command and env-prefix names before proposing anything. Ask only when a missing constraint changes the name space (what it is, who it is for, tone, words to avoid, which of domain, package, binary or handle it needs); otherwise state the assumption and go.

## Generate

8–12 serious candidates, no joke names unless asked. Mix strategies so the list is not one name with different suffixes: verbs, metaphors, compounds, portmanteaus, short real words, domain terms, and names chosen for sound. Avoid tired suffixes (`-ify`, `-ly`, `-base`, `-hub`, `-stack`, `-kit`) unless they carry real category signal. Insider terms suit expert products and alienate broad ones. A name should be spellable after hearing it once.

For each: why it fits, spelling or pronunciation risk, and any obvious conflict.

## Check

Search the exact name and adjacent terms on the web, then wherever the name has to live: GitHub, package registries, domains, app stores. Before checking, read [references/availability.md](references/availability.md) for the commands and how to read their results. Check the three to five strongest; replace any with a hard conflict and check the replacement.

## Output

A ranked shortlist ending in one recommendation with its tradeoffs. Per finalist: rationale, risks, the evidence found (or the gap), and the next action. Leave any unresolved domain, package or legal question explicit.

## Rename

List the public names that would change: package names, CLI commands, docs, env prefixes, API identifiers, app titles, repository names. Keep the brand decision separate from the code change, and change identifiers only when asked. When asked, rename every in-repo use with no aliases or old-name shims. Publishing under the new name, deprecating the old package or renaming the repository is outward-facing: confirm first.
