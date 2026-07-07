---
name: componentize
description: Audit a codebase for duplicated UI, repeated component patterns, and missed reuse opportunities; identify, plan, or implement scoped shared components and UI package changes. Use when asked to componentize an app, reduce duplicated components, consolidate repeated UI, adapt existing components with props/composition, create or use a Turborepo ui package, promote React/Tailwind UI reuse across apps/packages, or componentize a visually referenced part of a running app such as "the panel on the right" or "that thing in the sidebar."
---

# Componentize

Use this skill to interrogate a codebase for reuse opportunities before writing new UI. The goal is to reduce duplication, establish canonical shared components, and make app code consume those components through props, slots, composition, and clear package boundaries. Do not centralize the whole UI unless the user explicitly asks for a design-system project.

## Start

When invoked:

1. State that you are using the `componentize` skill.
2. Identify the repo shape before editing:
   - package manager and workspace config
   - apps and packages
   - whether `turbo.json` exists
   - whether a shared UI package already exists, commonly `packages/ui`, `packages/design-system`, `packages/components`, or `libs/ui`
   - UI framework, styling system, icon library, test setup, Storybook or examples
3. If the user refers to a visible target by location, appearance, or interaction, resolve that target before searching broadly.
4. Search before creating anything. Use `rg`, `rg --files`, and import relationships to find existing components, repeated markup, repeated Tailwind class strings, copied form controls, duplicated shells, and variant drift.
5. If the user asks for implementation, first state the extraction target, canonical home, public API, call sites to migrate, and validation plan. Then edit narrowly and validate. If the user asks for analysis, return an audit with prioritized extraction candidates.

## Core Principle

Prefer adaptation over addition:

1. Reuse an existing component unchanged.
2. Replace duplicate markup or one-off local components with the existing component that already owns the pattern.
3. Add a prop, variant, slot, render prop, or composition point to an existing component.
4. Extract a shared primitive from two or more local implementations.
5. Create a new shared component only when no existing component can be honestly adapted.
6. Create a new shared UI package only when reuse crosses app/package boundaries and the candidate API is domain-independent.

Do not create parallel components that differ only by copy, spacing, icon, color, or minor layout. Fold those differences into a single API unless doing so would make the component vague or overloaded.
When an existing component already matches the behavior and accessibility contract, migrate call sites to that component instead of extracting another one.

## Atomic Component Standard

Aim for the smallest useful component boundary. Extract primitives before extracting composed product UI, and make composed components depend on primitives rather than duplicating their markup or class strings.

Prefer this hierarchy:

1. token or class helper: shared spacing, typography, color, or focus-ring rules
2. primitive: Button, Input, Badge, TooltipTrigger, DialogContent
3. compound primitive: Field, Menu, Tabs, Select, DataList
4. composed surface: Toolbar, EmptyState, PageHeader, FilterBar
5. app-specific composition: route-aware shells, business workflows, copy-heavy panels

Atomic does not mean tiny files for their own sake. A component is atomic when it has one stable responsibility, one accessibility contract, no hidden domain behavior, and an API that can be reused without dragging product assumptions into other call sites.

## Variant And Composition Conventions

Follow the component conventions already present in the repo before introducing a new one:

- If the repo uses shadcn-style primitives, prefer `class-variance-authority` (`cva`) plus `VariantProps` for semantic variants and sizes, `cn`/`twMerge` for consumer `className` merging, and Radix `Slot`/`asChild` for polymorphic leaf components such as buttons, links, triggers, and menu items.
- If the repo uses Base UI from `@base-ui-components/react`, prefer its `render` prop composition model. For custom primitives that need the same polymorphism, use Base UI's `useRender` and `mergeProps` patterns rather than inventing an `asChild` clone.
- If the repo uses older MUI Base-style components, respect its `slots` and `slotProps` customization model instead of mixing in Radix `Slot` or Base UI `render` patterns.
- If the repo uses `tailwind-variants`, Stitches, Vanilla Extract, CSS modules, Panda, or another established variant system, extend that system instead of adding `cva` for one extraction.
- If there is no established pattern, use `cva` only when the component has observed semantic variants or sizes across multiple call sites. Use a plain `cn(...)` class merge for one-off primitives with no variant matrix.

For polymorphic components:

- expose `asChild` only when the implementation uses a Slot-compatible library and the component can safely pass props, events, refs, accessibility attributes, and data attributes to exactly one child
- expose Base UI-style `render` only when the repo uses `@base-ui-components/react` conventions or the component genuinely needs render-prop composition
- avoid polymorphism for components with required native-only props, internal DOM structure, or accessibility semantics that would become invalid on arbitrary elements
- document or type the default element and required child/ref behavior in the component API

## Server And Client Boundaries

In React Server Component frameworks such as Next.js App Router, prefer Server Components by default and keep client boundaries as small as the interaction requires.

When componentizing in an RSC-aware app:

- identify files marked with `'use client'` and inspect their import trees before extracting or moving UI
- avoid turning a large route, layout, shell, table, form, or panel into a Client Component only because one nested control needs state, effects, browser APIs, context, or event handlers
- extract the interactive part into the smallest practical Client Component and render it inside a Server Component that owns data fetching, server-only modules, secrets, routing params, static markup, and non-interactive layout
- pass serializable data from Server Components into Client Components; do not pass functions, class instances, server-only objects, or non-serializable data across the boundary
- use `children` or explicit slots to visually nest server-rendered UI inside a small client wrapper when the interaction is only a shell such as a modal, disclosure, tabs state, or popover
- keep providers and third-party client-only wrappers as deep in the tree as possible instead of wrapping an entire app, layout, or page by default
- preserve `server-only` and `client-only` guard imports when they exist, and add them only if the repo already uses that convention or boundary mistakes are a concrete risk

If duplicate code exists because a server file cannot import a client-only component, do not solve it by making everything client-side. Split the shared presentational primitive into an environment-agnostic component when possible, then layer a small Client Component around the interactive behavior.

## Reconnaissance

Read the code, not just filenames.

### Visual Target Resolution

When the user says something like "componentize the thing on the right", "the left panel", "that header", "the card grid", or "the sidebar":

1. Inspect the running app if available. Use the browser or screenshot tool preferred by the environment.
2. Identify the visible region by screen position, nearby text, role, landmark, route, or interaction.
3. Map the region back to source by checking DOM labels/classes when possible, then searching for distinctive text, aria labels, test ids, component names, route files, and nearby icon names.
4. If several regions could match, ask one concise clarification question before editing.
5. Once mapped, name the target explicitly in the audit or implementation checkpoint:
   - visible target: "right inspector panel"
   - source owner: `path/to/file.tsx`
   - candidate extraction: `InspectorPanel`
   - consumers/call sites found

Do not guess from layout direction alone. The screen target must be tied to source evidence before extraction.

Check:

- `package.json`, workspace files, `turbo.json`, `tsconfig*`, build scripts, lint scripts, test scripts
- app routes/pages and feature directories
- `components/`, `ui/`, `design-system/`, `shared/`, `lib/`, and package entrypoints
- imports from local components, package components, shadcn/radix/headless libraries, icon libraries, and CSS utilities
- repeated class strings and repeated JSX structures
- existing components whose props and accessibility contract already cover duplicated local code
- whether components accept `className`, `children`, `asChild`, variant props, size props, state props, and accessible labels
- whether the existing stack uses `cva`, `tailwind-variants`, Radix `Slot`/`asChild`, Base UI `render`/`useRender`, MUI Base `slots`/`slotProps`, CSS modules, or another variant/composition convention
- whether the framework uses Server Components, `'use client'` directives, `server-only`/`client-only` guard imports, server actions, route handlers, or serializable Server-to-Client props

Useful searches:

```sh
rg --files -g '*.{tsx,jsx,ts,js}' | rg '(^|/)(components|ui|design-system|shared|app|pages|src)/'
rg "className=['\"][^'\"]{60,}['\"]" -g '*.{tsx,jsx}'
rg 'className=\{|cn\(|clsx\(|cva\(|tv\(|data-slot=' -g '*.{tsx,jsx}'
rg '(Button|Card|Modal|Dialog|Input|Select|Badge|Avatar|Tabs|Table|Toast|Tooltip)' -g '*.{tsx,jsx}'
rg '@radix-ui|@base-ui|@mui/base|class-variance-authority|tailwind-variants|Slot|asChild|useRender|slotProps|variant' -g '*.{tsx,jsx,ts,js}'
rg "['\"]use client['\"]|['\"]use server['\"]|server-only|client-only|useState\\(|useEffect\\(|window\\.|document\\.|localStorage" -g '*.{tsx,jsx,ts,js}'
rg --files -g '*.{tsx,jsx}' | sed 's#.*/##' | sort | uniq -d
```

Discover source roots before running path-specific searches. Do not hard-code `packages libs src`; inspect the repo and search only directories that exist, such as `app`, `apps`, `src`, `packages`, `libs`, `frontend`, or `web`.

For import relationships, start with text search:

```sh
rg "^import .* from ['\"](\.|@|~|[A-Za-z])" -g '*.{ts,tsx,js,jsx}'
rg 'export .* from|export \{' -g 'index.{ts,tsx,js,jsx}' -g 'package.json'
```

Use graph tools such as `madge`, `dependency-cruiser`, or package-boundary checkers only when they are already installed or clearly part of the repo. Do not add new graph tooling just to complete an audit unless the user asks.

## Turborepo Decision

If the project is a Turborepo:

- Use an existing UI package when one exists and its purpose matches the work.
- Prefer `packages/ui` as the canonical home when there is no established convention.
- Keep package exports narrow and intentional.
- Make consuming apps import through the package public API. Deliberate subpath exports such as `@repo/ui/button` are fine; private source-file imports are not.
- Add missing package dependencies where imports cross package boundaries.

When creating or changing a UI package, check:

- `package.json` `exports` for JS and type entrypoints
- CSS/style exports and `sideEffects` when CSS imports must be preserved
- whether consumers need source transpilation, package build output, or direct TypeScript exports
- Tailwind v4 source scanning, including `@source` for package classes when needed
- peer dependencies for React, framework packages, Radix/headless libraries, Tailwind helpers, and icons
- package-level examples, stories, or a consumer import smoke test

If no shared package exists, recommend creating one only when the evidence supports cross-boundary reuse:

- two or more apps duplicate UI primitives or layouts
- a component is already copied across packages
- app code imports across app boundaries
- a reusable design system is emerging in more than one place
- repeated UI is blocking consistent accessibility, theming, or interaction behavior
- the candidate API is domain-independent enough to serve all known consumers

Default to an app-local shared folder when reuse is within one app, duplication is shallow, or the API is still product-specific. Avoid creating a package for a single app unless the local component tree is already large enough that a package boundary would simplify ownership.

## Extraction Targets

Prioritize components with high reuse value and low domain coupling:

- primitives: Button, IconButton, LinkButton, Input, Textarea, Select, Checkbox, Switch, RadioGroup, Badge, Avatar, Tooltip
- surfaces: Card, Panel, EmptyState, ErrorState, LoadingState, Dialog, Sheet, Popover
- data display: Table, DataList, Stat, MetricCard, Pagination, Tabs
- forms: Field, FieldLabel, FieldError, FormSection, SearchInput

Conditional targets:

- layout shells: AppShell, PageHeader, Section, Toolbar, Sidebar, Breadcrumbs

Be cautious with layout shells and any component that carries product-specific data fetching, auth, analytics, feature flags, route assumptions, navigation state, permissions, or business copy. Extract the presentational part and leave domain orchestration in the app.

## Component API Rules

Shared components should:

- accept `className` unless there is a strong reason not to
- keep layout margins with callers; components may own internal padding and gaps
- expose variants for real semantic differences, not every visual one-off; when using `cva` or an equivalent, keep variant names semantic (`intent`, `tone`, `size`) rather than tied to one caller
- map every new prop or variant to observed call-site differences; reject speculative options until another concrete consumer needs them
- prefer `children`, slots, or composition for complex content
- keep primitives leaf-like and slot-friendly when the stack supports it; avoid baking icons, labels, links, or layout wrappers into the primitive when those can be composed by the caller
- forward refs and spread valid DOM props for primitives that wrap an interactive or focusable element
- merge event handlers, refs, `className`, `style`, data attributes, and ARIA props using the repo's existing helper (`cn`, `mergeProps`, Slot, or equivalent)
- preserve accessibility names, focus states, keyboard behavior, and ARIA contracts
- keep environment-agnostic primitives free of `'use client'` unless they directly use client-only APIs; create a thin client wrapper for stateful behavior instead of marking a broad shared component client-side
- avoid importing app-only modules, route helpers, environment variables, or server-only code
- keep dependency weight low; app frameworks should be peer dependencies when appropriate

Do not make a component so configurable that it hides five unrelated designs. If variants conflict conceptually, split the component or extract a smaller primitive.
Do not use `asChild`, `render`, or slot props as an escape hatch for unclear ownership. They are for preserving valid semantics and composition, not for hiding unrelated components behind one API.
Do not move a component across a server/client boundary until you know whether its imports, props, and children are valid in the target environment.

## Workflow

### 1. Inventory

Produce a concise inventory:

- existing shared UI locations
- duplicated patterns and where they appear
- existing components that can replace duplicate code without API changes
- components that should be adapted with props
- components that should be extracted
- components that should remain app-local

### 2. Choose Canonical Homes

For each candidate, choose one:

- existing component: adapt API and migrate call sites
- existing UI package: move or add component there
- new UI package: create the smallest viable package only when the package threshold is met
- app-local shared folder: use only when reuse is intra-app
- no action: duplication is superficial or domain-specific

### 3. Design The API

Define the public component API before moving files:

- component name and import path
- props and variants, including whether variants are implemented with `cva`, `tailwind-variants`, CSS modules, or an existing local helper
- composition/slot model, including whether polymorphism uses Radix/shadcn `asChild`, Base UI `render`/`useRender`, MUI Base `slots`/`slotProps`, or no polymorphism
- server/client boundary, including whether the component stays server-rendered, remains environment-agnostic, or needs a small `'use client'` wrapper
- styling/theming contract
- accessibility contract
- examples or tests that prove expected usage

### 4. Implement In Small Slices

Extract one coherent group at a time. Update imports and call sites immediately so the repo does not keep two canonical versions.

Only load related skills when the user request requires that concern, the repo already uses that workflow, or the current extraction is blocked without it. Use `chiaroscuro` for UI visual polish or Tailwind/React component deduplication decisions, `aperture` for package extraction details, and `fenceline` for package boundary enforcement. Keep this skill's componentization workflow as the controlling scope.

### 5. Validate

Run the narrowest meaningful checks:

- typecheck for touched packages/apps
- lint for touched packages/apps
- relevant tests
- Storybook/examples build when shared UI examples exist
- consuming app build when package exports or imports changed
- consumer import smoke test proving exported JS, types, and styles resolve when a shared package changed
- rendered UI smoke check for affected pages/components when a runnable app or Storybook exists
- keyboard/focus checks for interactive primitives such as dialogs, selects, tabs, and buttons
- bundle or build smoke check when a change moves `'use client'` boundaries, imports client-only libraries from server code, or changes package entrypoints used by Server Components

If checks are unavailable or too broad, say exactly what was and was not verified.

## Audit Output

When returning an analysis, use this shape:

```markdown
## Reuse Audit

### Existing Shared Surface
- `path`: purpose, health, import pattern

### Highest-Value Opportunities
| Priority | Pattern | Evidence | Recommendation | Why |
|---|---|---|---|---|

Evidence should include representative `file:line` references, occurrence or call-site count, current owner/home, and whether the action is reuse unchanged, adapt, extract, move, or no action.

### Proposed Shared API
- `ComponentName`: props, variants, slots, import path

### Package Plan
- Use existing package / create `packages/ui` / keep app-local
- Export strategy
- Dependency changes
- Server/client boundary notes for RSC-aware apps

### Migration Plan
1. Extract/adapt component
2. Migrate call sites
3. Delete duplicate implementations
4. Validate

### Risks
- Coupling, accessibility, styling, or package-boundary concerns
```

## Guardrails

- Do not start by creating new components; search for reuse first.
- Do not leave duplicated canonical implementations after migration unless the user asks for a staged rollout.
- Do not move domain behavior into a shared UI package.
- Do not weaken package boundaries to make imports pass.
- Do not perform broad redesign while componentizing unless the user asked for visual redesign.
- Do not introduce a component library dependency without checking the existing stack and tradeoffs.

## Completion Check

Before finishing, verify:

- every new or changed shared component has a clear consumer
- duplicate implementations were removed or explicitly left for a stated reason
- imports use the canonical public path
- props/composition cover known variants without overfitting
- validation ran or the gap is reported
