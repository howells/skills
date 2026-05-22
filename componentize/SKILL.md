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
2. Add a prop, variant, slot, render prop, or composition point to an existing component.
3. Extract a shared primitive from two or more local implementations.
4. Create a new shared component only when no existing component can be honestly adapted.
5. Create a new shared UI package only when reuse crosses app/package boundaries and the candidate API is domain-independent.

Do not create parallel components that differ only by copy, spacing, icon, color, or minor layout. Fold those differences into a single API unless doing so would make the component vague or overloaded.

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
- whether components accept `className`, `children`, `asChild`, variant props, size props, state props, and accessible labels

Useful searches:

```sh
rg --files -g '*.{tsx,jsx,ts,js}' | rg '(^|/)(components|ui|design-system|shared|app|pages|src)/'
rg "className=['\"][^'\"]{60,}['\"]" -g '*.{tsx,jsx}'
rg 'className=\{|cn\(|clsx\(|cva\(|data-slot=' -g '*.{tsx,jsx}'
rg '(Button|Card|Modal|Dialog|Input|Select|Badge|Avatar|Tabs|Table|Toast|Tooltip)' -g '*.{tsx,jsx}'
rg '@radix-ui|class-variance-authority|cmdk|tailwind-variants|variant' -g '*.{tsx,jsx,ts,js}'
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
- expose variants for real semantic differences, not every visual one-off
- map every new prop or variant to observed call-site differences; reject speculative options until another concrete consumer needs them
- prefer `children`, slots, or composition for complex content
- preserve accessibility names, focus states, keyboard behavior, and ARIA contracts
- avoid importing app-only modules, route helpers, environment variables, or server-only code
- keep dependency weight low; app frameworks should be peer dependencies when appropriate

Do not make a component so configurable that it hides five unrelated designs. If variants conflict conceptually, split the component or extract a smaller primitive.

## Workflow

### 1. Inventory

Produce a concise inventory:

- existing shared UI locations
- duplicated patterns and where they appear
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
- props and variants
- composition/slot model
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
