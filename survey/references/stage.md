# Stage

Detecting where a project is in its life, and calibrating every severity to it. This is the reference file that keeps a survey from condemning a house for having no kitchen while the walls are going up.

## Detecting scale

Scale sets how many lenses run, not how harshly they judge.

```bash
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
  -o -name "*.py" -o -name "*.go" -o -name "*.rs" \) \
  -not -path "*/node_modules/*" -not -path "*/.git/*" \
  -not -path "*/dist/*" -not -path "*/build/*" | wc -l
```

| Source files | Scale  | Approach                                          |
| ------------ | ------ | ------------------------------------------------- |
| under 20     | small  | two or three lenses; skip architecture            |
| 20 to 100    | medium | three or four lenses; standard survey             |
| over 100     | large  | full lens set                                     |

A small project has no complex boundaries to review, and flagging its missing tests as critical is noise.

## Detecting stage

Infer from signals rather than asking cold. Most of these are a single glob or grep.

| Signal                                                                      | Indicates      |
| --------------------------------------------------------------------------- | -------------- |
| CI config (`.github/workflows/*`, `.gitlab-ci.yml`, `Jenkinsfile`)          | pre-launch or later |
| Deploy config (`vercel.json`, `Dockerfile`, `fly.toml`, `render.yaml`, `k8s/`) | pre-launch or later |
| Monitoring deps (`sentry`, `datadog`, `newrelic`)                           | production     |
| Production env references (`.env.production`, `NODE_ENV` guards)            | pre-launch or later |
| Test files exist (`**/*.test.*`, `**/*.spec.*`)                             | development or later |
| Custom domain or production URL in config                                   | production     |
| Rate limiting, cache or queue deps (`rate-limit`, `redis`, `bull`)          | production     |
| `git rev-list --count HEAD`                                                 | maturity       |

If `git rev-parse --git-dir` errors, the project is not a git repo. Treat history as **unknown**, and do not count the absence toward `prototype` - a downloaded tarball is not a weekend experiment.

| Stage         | Meaning                                     | Typical signals                                              |
| ------------- | ------------------------------------------- | ------------------------------------------------------------ |
| `prototype`   | Exploring an idea, validating a concept     | under 30 commits, no CI, no deploy config, no tests          |
| `development` | Actively building, not yet shipped          | some tests, maybe CI, no production deploy                   |
| `pre-launch`  | Feature-complete, preparing to ship         | CI, deploy config and tests, but no monitoring               |
| `production`  | Live, serving real users                    | monitoring, production env, rate limiting, 200+ commits      |

Default to `development` when signals conflict. **When in doubt, pick the earlier stage** - under-flagging costs less than burying a real finding under premature requirements.

Then confirm, because stage drives every severity in the run:

```
Detected stage: [stage], from [the two or three signals that decided it].
```

Their correction wins. With no answer available, proceed and mark the stage UNCONFIRMED everywhere it appears.

## The security readiness gate

A deep security lens on an early prototype produces a production-hardening review nobody asked for. The gate decides whether it runs. The mechanical secrets scan and dependency check run regardless, at every stage.

**Run the deep lens** when any of these hold:

- The user's focus mentions security, auth, privacy, compliance, payments, production, launch or public release.
- Stage is `pre-launch` or `production`.
- A public or launch signal exists - custom domain, production URL, deploy config alongside production env references, or launch checklist artifacts.
- A sensitive surface exists - auth, payments, webhooks, user accounts, multi-tenancy, admin areas, file uploads, email sending, public write APIs, database-backed user data, or third-party secrets.
- Mechanical checks turned up critical or high dependency vulnerabilities, likely hardcoded credentials, unsafe HTML or `eval` patterns, or server endpoints handling untrusted input.

**Skip it** only when all of these hold: stage is `prototype` or `development`, no security focus was requested, no public or launch signal is present, no sensitive surface is detected, and the mechanical secret and vulnerability scans came back clean.

When skipped, record `Security gate: lightweight` in the detection summary and score axis 1 as `--`. **A skipped lens never lowers the score** - the gate is a stage-appropriate decision about the survey, not a finding about the code. If a concrete dangerous finding turns up later in the run, add the lens back before scoring.

## Calibration blocks

Paste the block matching the detected stage verbatim into every lens prompt. Not a summary of it - the block itself.

### prototype

```
This project is at PROTOTYPE stage - exploring ideas, validating a concept.

Severity calibration:
- Flag only what could lose data, leak credentials, or stop the prototype working.
- Do NOT flag: missing rate limiting, incomplete error handling, input validation
  outside auth flows, missing tests, architectural purity, performance work,
  accessibility, code organisation.
- Compress anything you would normally call High or Medium down to Low.
- The questions that matter are "does this work?" and "could this leak secrets?".
  Nothing else does yet.
- Respect the experiment. This code may be exploring an unconventional idea.
  Don't penalise it for being impractical; flag genuine danger only.
- Exception: structural defects carrying a scorecard cap (god files, god
  page-clients, circular dependencies) are still reported and still cap their
  axis at every stage. Prototype calibration lowers their severity; it does not
  suppress them. Dropping them would make the score disagree with the findings.
```

### development

```
This project is at DEVELOPMENT stage - actively building features, not yet shipped.

Severity calibration:
- Critical: actual security vulnerabilities only - injection, XSS, credential
  exposure, auth bypass.
- High: data integrity problems, bugs that would corrupt state.
- Medium: performance problems that would block usability, missing error boundaries.
- Low: everything else - architecture suggestions, missing tests, rate limiting,
  caching, monitoring.
- Do NOT rate as High or Critical: missing rate limiting, incomplete logging, no
  monitoring, missing CI checks, or production hardening. All premature here.
- For anything that isn't security or data integrity, use advisory language
  ("worth considering") rather than prescriptive ("must fix").
```

### pre-launch

```
This project is at PRE-LAUNCH stage - feature-complete, preparing to ship.

Severity calibration:
- Standard severity for most issues.
- Production hardening (rate limiting, error handling, input validation) is now
  relevant, but rate it Medium rather than Critical.
- Missing monitoring or observability is Medium - it should be set up, but it
  isn't blocking.
- Architecture and performance issues at full severity.
- Any missing error state in a user-facing flow is High.
```

### production

```
This project is at PRODUCTION stage - live, serving real users.

Severity calibration:
- Full severity throughout. Every concern is relevant.
- Missing rate limiting, monitoring or error handling are legitimate High or
  Critical concerns.
- Security issues at maximum severity.
- Performance regressions are High.
- No downgrading. If it affects real users, it matters.
```

## Severity validation table

Use during vetting to sanity-check what the lenses returned.

| Finding                             | prototype | development | pre-launch | production |
| ----------------------------------- | --------- | ----------- | ---------- | ---------- |
| Missing rate limiting               | drop      | Low         | Medium     | High       |
| Missing monitoring                  | drop      | drop        | Medium     | High       |
| Missing input validation (non-auth) | drop      | Low         | High       | Critical   |
| Missing error boundaries            | Low       | Medium      | High       | High       |
| Missing tests                       | drop      | Low         | Medium     | High       |
| Credential exposure                 | Critical  | Critical    | Critical   | Critical   |
| Injection / XSS                     | Critical  | Critical    | Critical   | Critical   |
| Architecture concerns               | drop\*    | Low         | Medium     | High       |
| Performance work                    | drop      | Low         | Medium     | High       |
| Accessibility gaps                  | drop      | Low         | Medium     | High       |

\* Except the capped structural defects named in the prototype block, which are always reported.

Where a lens rated something above what the stage warrants, downgrade it and annotate: `[adjusted for <stage> - would be <original> in production]`.

## Advisory tone

Not every project is trying to be production software, and a survey that can't tell the difference is worthless.

- **Most findings are advisory.** "You may want to consider X", not "you must do X".
- **Don't fight the user's intent.** An unconventional approach is not a defect. Flag risk, not unfamiliarity.
- **Push hard only where it's genuinely dangerous** - credential exposure, data corruption, injection.
- **YAGNI holds.** Don't recommend infrastructure the project has no use for yet.

The language ladder:

| Phrase              | Reserved for                                       |
| ------------------- | -------------------------------------------------- |
| **must fix**        | Genuine danger - security holes, data loss. Rare.  |
| **should consider** | Real problems, if the project goes further.        |
| **worth noting**    | Suggestions. No pressure.                          |

## Resolving conflicts between lenses

| Conflict                                                  | Resolution                                                             |
| --------------------------------------------------------- | ---------------------------------------------------------------------- |
| Security wants validation, simplicity wants less code      | Security wins at pre-launch and production. Earlier, it's Low - user decides. |
| Performance wants caching, architecture wants statelessness | Hot path, performance wins. Rarely called, architecture wins.          |
| Two lenses flag one area with different fixes              | Take the simpler fix; note the alternative.                            |
| A lens flags something the repo's own rules allow          | Dismiss it entirely. Project rules outrank generic best practice.      |
