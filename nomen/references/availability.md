# Availability checks

Every result is a conflict signal at the time of the lookup. Report the source and date with it.

## GitHub

- `gh api "repos/OWNER/NAME"`: 200 is an existing repository; 404 means not visible to this credential, which includes private repositories.
- `gh search repos NAME --limit 20` gauges how crowded the name is.

## Package registries

- npm: `npm view NAME name`. Read the not-found response itself; anything else is unknown. npm also rejects names too similar to existing packages (punctuation and typo-squat rules), and spam-reserved or unpublished names 404 too.
- PyPI: `pip index versions NAME`. Crates: `cargo search NAME`. RubyGems: `gem list -r -e NAME`.

## Domains

Use an authoritative registry RDAP or registrar lookup for registration status. A live site is strong evidence the domain is in use. DNS and HTTP are evidence of use only: an empty `dig +short NAME.TLD NS` does not mean unregistered, because registered domains can lack delegation. An unregistered domain may still be reserved or premium. When signals conflict or the lookup fails, report the status as unresolved, with the evidence of use.

## App stores

Apple's iTunes Search API needs no key. Query each relevant platform with `entity=software` (iPhone), `iPadSoftware` or `macSoftware`. Use `--data-urlencode` for the term, since a raw space silently truncates the query, and widen `country` beyond `us` when the app targets other regions, since region-exclusive apps do not appear otherwise:

```
curl -s -G "https://itunes.apple.com/search" \
  --data-urlencode "term=NAME" \
  --data "entity=software&limit=20&country=us"
```

In `results[]`, read each `trackName` and `sellerName`:

- **Exact match**, compared case-insensitively ("Clipper" and "clipper" collide): the App Store name is taken.
- **Prefix match** (`NAME `, `NAME:`, `NAME -`): a close collision.
- **Saturation**: many apps that merely contain the word. The bare name may be free and still not distinctive.

If results hit the limit, refine the query rather than claim full coverage.

Android: web-search `NAME site:play.google.com`.

## Crowding

Product Hunt and app-store category listings show whether the space is crowded. Search trademark databases only when the user asks for that level of signal.
