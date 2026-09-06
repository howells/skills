# Optional scorecard

Use this only when the user explicitly asks for scores or a numerical comparison across
reviews. It supplements a Simplify review; it never replaces the strict
structural verdict in `SKILL.md`, and it does not require extra lenses or a build
gate ladder.

## Scope and comparability

Label every score with scope, revision, comparison base (for a diff), reviewed
areas, evidence used, and axes not assessed. Score only the selected diff when
reviewing a diff; call it a `diff score` and never present it as whole-codebase
health. Compare scores only when scope, evidence, and axes are materially alike.
An unreviewed axis is `--`, never a zero or an implied pass. Missing local
prerequisites establish no score; report the unavailable evidence. A complete
source inspection may establish missing critical tests, but an incomplete search
cannot. These criteria supersede the retired scorecard: do not compare an older
score unless it is reassessed against these criteria.

```
Score scope: <diff against base | whole codebase at revision>
Coverage: <areas and lenses actually reviewed>
Axes: Security --; Performance 2; Architecture 1; Quality 2; Tests --;
       Reliability 2; Operations --
```

## Axes

Assess only applicable, reviewed axes on the same 0–3 scale:

| Axis | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Security | demonstrated exploit or exposed secret | material boundary gaps | sound boundaries with limited hardening gaps | defense in depth, supported by evidence |
| Performance | demonstrated severe unbounded or repeated work | material likely bottleneck | appropriate bounds and query/render design | measured, sustained performance |
| Architecture | severe coupling, circularity, or sprawling ownership | repeated boundary or complexity debt | clear ownership with limited friction | simple, enforced dependency direction |
| Code quality | contracts and maintenance are broadly unreliable | recurring casts, duplication, or opaque flow | readable, typed, consistent implementation | direct, small, legible code with clear invariants |
| Tests | absent or misleading coverage for applicable critical behavior | fragile or mostly happy-path coverage | meaningful critical-path coverage | reliable behavior-focused coverage across relevant levels |
| Reliability | demonstrated failure or corrupt partial state | inconsistent failure handling | expected failures degrade safely | failure and recovery behavior is designed and verified |
| Operations | confirmed broken applicable build or operating workflow | fragile or poorly evidenced workflow | repeatable checks or release operation where relevant | verified, maintainable operation for the product's needs |

Accessibility may be assessed separately for user-facing interfaces: 0 means
critical interaction barriers; 1 means material semantic, keyboard, focus, or
contrast gaps; 2 means the principal flows are accessible with limited gaps; 3
means accessible behavior is deliberately verified. Do not score a non-UI scope.

Scores describe the reviewed posture, not the single worst finding. A confirmed
critical defect still appears prominently in findings even if the surrounding
axis is otherwise strong. Apply no mechanical cap from a threshold or missing
tool alone: a cap requires source-confirmed, relevant evidence and an assessed
axis. Record the reason for any cap-like conclusion.

## Reporting

Report individual axes first. If a total is useful, show `earned/available` and
the reviewed axes rather than treating missing coverage as health. Do not assign
a maturity band unless the user asks for one; stage guides the interpretation of
the result, not the arithmetic. See [stage and evidence](stage.md) for lifecycle
calibration and [review lenses](lenses.md) for coverage selection.
