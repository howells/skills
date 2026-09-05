# Fail Fast Remediation Reference

Use this reference file after the scanner identifies a fallback. Do not delete all defaults mechanically; remove hidden state and make every remaining branch explicit, tested, and justified.

## Classification

### Remove

Remove the fallback when:

- the old caller, config key, flag, import path, or data shape is no longer supported;
- tests only pass because a default masks missing setup;
- the fallback creates duplicate paths and investigation confirms no supported contract needs both;
- the branch says `legacy`, `deprecated`, `old`, `compat`, or `migration`, and investigation confirms no supported caller or contract still needs it.

Typical fixes:

- delete the fallback branch;
- update call sites to the canonical API;
- delete compatibility tests and replace them with canonical behavior tests;
- update docs or examples that still mention the old path.

### Require

Require the value when code cannot work correctly without it.

Typical fixes:

- fail during startup or module initialization with a specific message;
- move env vars into an environment schema and read them through the typed env module;
- replace `foo || defaultFoo` with a required function argument;
- change tests to pass explicit fixtures.

### Validate

Validate when data crosses a boundary and can be malformed.

Typical fixes:

- parse external input with a schema;
- reject impossible enum values;
- throw a domain error at the adapter boundary;
- keep internal code typed against the validated shape only.

### Keep

Keep behaviour required by a supported product, API or protocol contract. Permanent support has no required expiry; document why both paths remain and verify their contract.

For a temporary migration, record the owner, removal date or version window, and checks for both paths. Add logging or metrics when they are needed to decide whether the old path can disappear. Missing paperwork is not permission to remove required behaviour.

## Environment Variables

Environment handling should be deterministic.

Where an environment schema exists, required values should fail validation before application code uses them. Add undeclared required keys to that schema. Keep server-only secrets out of client bundles.

For example, a server environment module in a project already using Zod can validate only its required keys:

```ts
import { z } from "zod";

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  OPENAI_API_KEY: z.string().min(1),
});

export const env = envSchema.parse({
  DATABASE_URL: process.env.DATABASE_URL,
  OPENAI_API_KEY: process.env.OPENAI_API_KEY,
});
```

Use the existing validator and module conventions; this example does not require introducing Zod. Never log the raw environment or validation input containing secrets.

Application code should use typed env modules:

```ts
import { env } from "@/env/server";

export const client = createClient({ apiKey: env.OPENAI_API_KEY });
```

Remove application-level env fallbacks:

```ts
const apiKey = process.env.OPENAI_API_KEY || "test";
const url = process.env.DATABASE_URL ?? "postgres://localhost:5432/app";
```

Replace them with:

```ts
const apiKey = env.OPENAI_API_KEY;
const url = env.DATABASE_URL;
```

Run the project's documented environment validation command and the relevant build check. Inspect package scripts rather than guessing a validator binary or downloading a similarly named package.

Allowed direct `process.env` reads:

- env schema files;
- generated Next.js env mapping;
- system keys such as `NODE_ENV` and `CI`;
- documented temporary migration escape hatches.

When a schema already owns environment validation, extend it rather than duplicating guards in application code. The failure point belongs in schema parsing or the project's configuration preflight.

## Common Refactors

### From fallback config to required config

Before:

```ts
const baseUrl = config.baseUrl ?? "http://localhost:3000";
```

After:

```ts
if (!config.baseUrl) {
  throw new Error("baseUrl is required");
}
const baseUrl = config.baseUrl;
```

### From optional dependency to explicit feature flag

Before:

```ts
let analytics = noopAnalytics;
try {
  analytics = await import("./analytics");
} catch {}
```

After:

```ts
if (features.analytics) {
  const analytics = await import("./analytics");
  analytics.track(event);
}
```

### From legacy alias to canonical input

Before:

```ts
const projectId = input.projectId ?? input.workspaceId;
```

After:

```ts
if (!input.projectId) {
  throw new Error("projectId is required");
}
```

## Tests

Add tests for the failure mode, not just the happy path:

- missing schema-declared env var fails schema validation;
- missing required argument throws a specific error;
- legacy key is rejected when compatibility is removed;
- catch block rethrows with useful context;
- tests pass explicit fixtures instead of relying on global defaults.
