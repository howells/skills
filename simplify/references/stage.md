# Stage and evidence

Use stage to calibrate severity, not to excuse structural complexity. Simplify's
structural review bar applies to a diff and a whole codebase at every stage.

## Establish the context

State the selected scope first: comparison base and changed paths for a diff;
repository, revision, source roots, and excluded generated or vendored paths for
a whole-codebase review. A diff review distinguishes introduced or changed risk from relevant existing
defects. A whole-codebase finding describes the implementation as it exists; do not imply
that an existing problem was introduced by the current change.

Infer lifecycle only from corroborating evidence in the repository or from the
user. Useful signals include release notes, active deployment and operational
configuration, CI history, production incident or monitoring configuration, and
the product's documented users. A custom domain, a URL, dependency name, or a
commit count is not enough to establish production status. If the evidence is
mixed, say `stage: unconfirmed` and avoid lifecycle-dependent claims.

```
Scope: diff against <base> | whole codebase at <revision>
Stage: <prototype | development | pre-launch | production | unconfirmed>
Evidence: <specific source evidence>
```

## Calibrate risk

Report a claim only after opening the relevant source, configuration, test, or
runtime evidence. A scanner result, file-size threshold, dependency advisory, or
comment is a lead, not proof. Repository instructions and established contracts
outrank generic advice.

At any stage, treat demonstrated credential exposure, exploitable input handling,
data loss or corruption, and broken user-critical behavior as serious. At earlier
stages, describe absent production hardening, broad monitoring, caching, or
operational machinery as a conditional recommendation only when the selected
scope makes it relevant. Do not turn missing infrastructure into a finding merely
because it is common elsewhere.

Structural defects remain relevant at every stage: needless layers, duplicated
logic, boundary leaks, sprawling files, ad-hoc branches, unclear contracts, and
non-atomic state changes make the next change harder whether or not the product
has launched. Severity reflects demonstrated cost and reach, not a rubric
threshold alone.

Use these severity meanings in the report, separately from the structural verdict:

- Critical: demonstrated exploitable exposure or imminent substantial data loss.
- High: a demonstrated major failure, corruption path, or blocked critical workflow.
- Medium: a concrete bounded correctness, performance, or maintenance cost.
- Low: localized structural debt with no current behavior failure, including harmless duplicated branches.

A recommendation can block structural approval under Cursor's rubric while having
Low operational severity. Do not label it urgent or P1 solely because the rubric
asks for changes. Tracker priority is assigned separately when tracker work is
requested.

## Security and other focused checks

Select a security review when the requested scope handles authentication,
authorization, untrusted input, secrets, payments, personal data, uploads,
webhooks, public writes, or a user expressly asks for security or release
readiness. Select performance, reliability, data, test, or accessibility review
when the code or requested question raises a concrete question about that concern. See the
[lens guide](lenses.md). Do not run a universal checklist or automatic build
ladder to manufacture coverage.
