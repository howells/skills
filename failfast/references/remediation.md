# Failfast remediation

Read when deciding what to do with a scanner finding. Don't strip defaults mechanically: remove hidden state and make every remaining branch explicit and justified.

## Deciding

- **Remove** when the old caller, key, flag, import path or data shape is no longer supported, or when tests pass only because a default masks missing setup (give them explicit fixtures). `legacy`, `deprecated`, `compat` and `migration` are leads, not proof: confirm no supported caller needs the path. Delete compatibility tests along with the branch and update docs and examples that mention it.
- **Require** when the code can't work without the value: fail at startup or module load with a specific message, or make it a required argument.
- **Validate** when data crosses a boundary and can be malformed: parse it with a schema, and type internal code against the parsed shape only.
- **Keep** behaviour a supported product, API or protocol needs, and say why both paths remain. A temporary migration needs an owner, a removal point and checks on both paths. Missing paperwork is not permission to remove required behaviour.

## Environment variables

Where a schema exists, required values fail validation before application code runs. Add undeclared keys to it rather than guarding in application code. In a project already using Zod:

```ts
import { z } from "zod";

export const env = z
  .object({
    DATABASE_URL: z.string().url(),
    OPENAI_API_KEY: z.string().min(1),
  })
  .parse({
    DATABASE_URL: process.env.DATABASE_URL,
    OPENAI_API_KEY: process.env.OPENAI_API_KEY,
  });
```

Use the project's validator; don't introduce Zod for this. Keep server-only secrets out of client bundles, and never log the raw environment or validation input. Run the project's own env check from its package scripts rather than guessing a validator binary.

## Refactors

Optional dependency to explicit feature flag:

```ts
// Before: analytics silently disappears when the import fails
let analytics = noopAnalytics;
try {
  analytics = await import("./analytics");
} catch {}

// After
if (features.analytics) {
  const analytics = await import("./analytics");
  analytics.track(event);
}
```

Legacy alias to canonical input:

```ts
// Before
const projectId = input.projectId ?? input.workspaceId;

// After: callers send projectId; workspaceId is rejected by the input schema
if (!input.projectId) throw new Error("projectId is required");
```
