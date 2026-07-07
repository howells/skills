# Fail Fast Remediation Reference

Use this reference after the scanner identifies a fallback. The goal is not to delete all defaults mechanically; the goal is to remove hidden state and make every remaining branch explicit, tested, and justified.

## Classification

### Remove

Remove the fallback when:

- the old caller, config key, flag, import path, or data shape is no longer supported;
- tests only pass because a default masks missing setup;
- the fallback creates two valid ways to do the same thing;
- the branch says `legacy`, `deprecated`, `old`, `compat`, or `migration` without an owner and removal condition.

Typical fixes:

- delete the fallback branch;
- update call sites to the canonical API;
- delete compatibility tests and replace them with canonical behavior tests;
- update docs or examples that still mention the old path.

### Require

Require the value when code cannot work correctly without it.

Typical fixes:

- fail during startup or module initialization with a specific message;
- move env vars into an Envy schema and read them through the typed env module;
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

Keep a fallback only when it has:

- a named external user or protocol requirement;
- a documented owner;
- a removal date or version window;
- tests that describe why both paths exist;
- logging or metrics if the old path should disappear.

## Environment Variables

Environment handling should be deterministic.

In TypeScript repos that use `@howells/envy`, required env var presence is already enforced by the schema. "The env var might be missing" is not a reason to add an application fallback, because the Envy schema should make that state unreachable. If a required key is not declared, add it to the schema.

Use Envy schemas for env contracts:

```ts
import { defineEnv } from "@howells/envy";
import { z } from "zod";

export const envSchema = defineEnv({
  server: {
    DATABASE_URL: z.string().url(),
    OPENAI_API_KEY: z.string().min(1),
  },
  public: {
    NEXT_PUBLIC_APP_URL: z.string().url(),
  },
  system: {
    NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
    CI: z.coerce.boolean().default(false),
  },
});
```

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

Use Envy commands when present:

```bash
npx --no-install envy check local --schema ./src/env/schema.ts --from .env.production
npx --no-install envy check local --schema ./src/env/schema.ts --mode all --json
npx --no-install envy check turbo --schema ./src/env/schema.ts --task build
```

Allowed direct `process.env` reads:

- env schema files;
- generated Next.js env mapping;
- system keys such as `NODE_ENV` and `CI`;
- documented temporary migration escape hatches.

Do not replace an env fallback with another hand-rolled guard in an Envy project. The proper failure point is schema parsing or an Envy preflight command.

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

- missing Envy-declared env var fails schema validation;
- missing required argument throws a specific error;
- legacy key is rejected when compatibility is removed;
- catch block rethrows with useful context;
- tests pass explicit fixtures instead of relying on global defaults.
