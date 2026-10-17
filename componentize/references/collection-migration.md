# Migrating a component collection

Use when extracting a kit from many charts, cards, examples or other related consumers. Preserve the collection's meaningful differences while removing implementations that should stay the same.

## Establish the baseline

Inventory every in-scope consumer and its variants, states and source owner. Distinguish a representative sample used to shape an API from the full set that must migrate.

Capture an untouched baseline with fixed data or seed, viewport, browser, fonts, assets and settled state. Repeat the unchanged capture to reveal noise from random data, live timestamps, loading, animation or rasterisation. Stabilise that source or record its limits before treating a difference as a regression. Keep the baseline immutable through the migration; don't regenerate it from the changed code and call that parity.

## Extract by family

Choose one coherent family, derive its API from observed call sites, migrate it, then check its actual consumers before expanding to the next family. Shared primitives can own axes, labels or interaction mechanics while callers retain distinct marks, textures and semantics. Don't make every example identical to fit the first API.

Resolve exports, styles and variants in real consumers, not just in an isolated demo. When the request covers the whole collection, reconcile the final consumer count and search for old imports or inline copies. Name intentionally staged or out-of-scope consumers separately; a successful first family doesn't complete the collection.

## Verify different claims separately

| Claim | Evidence |
| --- | --- |
| Resting appearance preserved | Matched baseline and changed captures in the same settled state, inspected in context |
| Interaction preserved | Keyboard, pointer, selection, focus, tooltips and state changes exercised in affected consumers |
| Motion preserved | Played transition, interruption and intermediate frames; static parity can't show these |
| Shared implementation adopted | Consumer inventory reconciled with actual imports and removed copies |
| Performance improved | Relevant measured timing or resource use under comparable conditions |

Report the migrated denominator, actual inspected coverage and remaining gaps. Record durable evidence on the owning tracker item; don't add a local migration report unless requested.
