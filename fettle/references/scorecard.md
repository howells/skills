# Scorecard

Only when scores are requested. It supplements the structural verdict; it never replaces it.

Score only what was reviewed. A diff review produces a `diff score`, never repository health. An unreviewed or inapplicable axis is `--`, not zero and not a pass; a missing tool establishes no score. Compare scores across reviews only when scope and axes match.

```
Score scope: <diff against base | whole codebase at revision>
Coverage: <areas and risks actually reviewed>
Axes: Security --; Performance 2; Architecture 1; Quality 2; Tests --;
      Reliability 2; Operations --
Total: 7/12 (reviewed axes only)
```

| Axis | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Security | demonstrated exploit or exposed secret | material boundary gaps | sound boundaries, limited hardening gaps | defence in depth, evidenced |
| Performance | demonstrated unbounded or repeated work | likely material bottleneck | appropriate bounds and query/render design | measured, sustained performance |
| Architecture | severe coupling, circularity or sprawling ownership | repeated boundary or complexity debt | clear ownership, limited friction | simple, enforced dependency direction |
| Code quality | contracts broadly unreliable | recurring casts, duplication or opaque flow | readable, typed, consistent | direct, small, legible, clear invariants |
| Tests | absent or misleading for critical behaviour | fragile or happy-path only | meaningful critical-path coverage | reliable behaviour-focused coverage across levels |
| Reliability | demonstrated failure or corrupt partial state | inconsistent failure handling | expected failures degrade safely | failure and recovery designed and verified |
| Operations | broken build or operating workflow | fragile or unevidenced workflow | repeatable checks and release | verified, maintainable operation |

For user-facing UI, Accessibility may be scored on the same scale: critical barriers; material semantic, keyboard, focus or contrast gaps; principal flows accessible; deliberately verified.

A score describes the reviewed posture, not the worst finding; a critical finding still leads the findings. Report axes first; show a total only as `earned/available` over reviewed axes.
