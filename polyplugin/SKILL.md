---
name: polyplugin
description: Create, audit, or migrate agent plugins across Claude Code, Codex, and Cursor. Use when asked to make a plugin valid for multiple agent hosts, add .claude-plugin, .codex-plugin, or .cursor-plugin manifests, reconcile shared plugin metadata, create multi-runtime marketplace entries, validate plugin packaging, research latest host plugin requirements, or decide whether an existing skill collection should become a plugin.
---

# Polyplugin

Use this skill when a project should be packaged as a plugin for one or more agent hosts. The goal is one coherent plugin boundary with host-specific manifests, not drifting products per editor.

## References

Load `references/dual-plugin-checklist.md` when creating or changing manifests.

For Cursor work, treat the checklist as a living baseline and verify the current official Cursor docs or `cursor/plugins` repository before judging schema details. Cursor plugins are new and have already changed quickly.

## Start

When invoked:

1. State that you are using the `polyplugin` skill.
2. Identify the requested host surface:
   - Claude Code plugin
   - Codex plugin
   - Cursor plugin
   - a specific combination of hosts
   - audit only
3. Inspect the repo before editing:
   - `.claude-plugin/plugin.json`
   - `.claude-plugin/marketplace.json`
   - `.codex-plugin/plugin.json`
   - `.cursor-plugin/plugin.json`
   - `.cursor-plugin/marketplace.json`
   - Codex marketplace file if specified
   - Cursor plugin folders: `skills/`, `commands/`, `agents/`, `rules/`, `hooks/`, `mcp.json`, assets, README, CHANGELOG, and LICENSE
   - shared folders that other hosts use: `skills/`, `commands/`, `agents/`, `references/`, `scripts/`, `assets/`, `mcp`, `apps`
   - version files and release scripts
4. If the user has not specified distribution, ask only when it changes the files you would create. Otherwise choose the smallest valid addition.

## Core Decisions

### Plugin Or Skill Collection

Use a plugin when the package needs any of:

- multiple skills that should install together
- commands or slash-command routers
- bundled agents, MCP servers, apps, scripts, assets, or references
- marketplace metadata
- release tags or versioned distribution
- host-specific install/update behavior
- Cursor local, marketplace, or team-marketplace installation

Use a plain skill collection when it only contains independent `SKILL.md` folders and no shared runtime surface.

### One Boundary

Define one plugin identity before writing manifests:

- normalized plugin name
- owner or marketplace name
- description
- version
- license
- repository
- included capabilities
- host surfaces intentionally supported

Do not let Claude, Codex, and Cursor manifests diverge in name, description, version, repository, license, or included capability paths unless a host requires it.

## Workflow

### 1. Inventory

Produce a concise inventory:

- existing manifests and marketplaces
- install surfaces already working
- shared folders that both hosts should see
- host-specific folders that must stay separate
- validation commands available locally

### 2. Design The Manifest Plan

For each host, state:

- files to create or edit
- source paths for skills, commands, agents, MCP, apps, scripts, or assets
- marketplace entry, if any
- validation command
- release/tag command

Prefer additive changes. Do not delete an existing valid host manifest unless the user explicitly asks to drop that host.

### 3. Create Or Reconcile Files

Use existing conventions when present.

For Claude Code:

- keep `.claude-plugin/plugin.json` valid
- keep `.claude-plugin/marketplace.json` in sync when present
- validate with `claude plugins validate .`
- release with `claude plugins tag . --push` when publishing is requested

For Codex:

- keep `.codex-plugin/plugin.json` valid
- add a Codex marketplace entry only when the user asks for marketplace visibility or install ordering
- use the local `plugin-creator` skill or its validation scripts when available
- keep Codex-only fields out of the Claude manifest and Claude-only fields out of the Codex manifest

For Cursor:

- keep `.cursor-plugin/plugin.json` at the plugin root
- use the official Cursor schema as the source of truth; as of 2026-06-04, `name` is required and the manifest allows only the documented fields
- use default component folders when possible: `skills/`, `commands/`, `agents/`, `rules/`, `hooks/`, and `mcp.json`
- declare component paths only when custom discovery is needed; paths must be relative to the plugin root and must not use absolute paths or `..`
- use `mcpServers` in the manifest only for a path, inline config object, or array of either; do not invent `mcp`, `apps`, or host-specific fields not accepted by the schema
- use `hooks` as either a path such as `./hooks/hooks.json` or an inline hooks object
- keep Cursor rules in `rules/*.mdc` with frontmatter (`description`, `alwaysApply`, optional `globs`)
- keep skills in `skills/<skill-name>/SKILL.md` with `name` and `description` frontmatter
- keep agents and commands in markdown/text files with `name` and `description` frontmatter
- for a multi-plugin Cursor marketplace repo, keep the root `.cursor-plugin/marketplace.json` minimal: `name`, optional `owner`, optional `metadata.description`, and `plugins[]` entries with `name`, `source`, and optional `description`
- do not put version, category, tags, keywords, or author in Cursor marketplace entries; those belong in each plugin's `.cursor-plugin/plugin.json`
- for local testing, place or symlink the plugin at `~/.cursor/plugins/local/<plugin-name>/`, with `.cursor-plugin/plugin.json` at that root, then restart Cursor or run `Developer: Reload Window`
- for marketplace publishing, use Cursor's current submission flow; do not assume marketplace acceptance, private team-marketplace eligibility, required-vs-optional rollout, or security review status without checking current Cursor docs

Cursor plugins are not VS Code extensions. Cursor also supports VS Code/Open VSX extensions, but that is a different packaging surface and should not be mixed with `.cursor-plugin` manifests.

### 4. Version Sync

If multiple hosts are supported, version should be synchronized across:

- root package/release metadata when used
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.codex-plugin/plugin.json`
- Codex marketplace entry, if it carries a version
- `.cursor-plugin/plugin.json`

Use an existing version bump script when present. If none exists, update the minimal set by structured JSON editing, not ad hoc text replacement.

Do not add a version to `.cursor-plugin/marketplace.json`; the current Cursor marketplace schema does not allow it.

### 5. Validate

Run the smallest complete validation set:

- Claude manifest validation when `.claude-plugin` exists
- Codex manifest validation when `.codex-plugin` exists
- Cursor manifest validation when `.cursor-plugin` exists
- package tests or plugin smoke tests
- version drift check when a script exists

For Cursor validation:

- prefer an official local validator from the Cursor plugin template, `cursor/plugins` repository, or current Cursor CLI/docs when available
- validate `.cursor-plugin/plugin.json` against the current Cursor plugin schema and `.cursor-plugin/marketplace.json` against the current marketplace schema when a marketplace file exists
- verify declared component paths exist and resolve within the plugin root
- verify local loading by symlinking to `~/.cursor/plugins/local/<plugin-name>/` and reloading Cursor when the user asks for local install validation

If a validator is unavailable, report the exact validator that was missing and inspect the manifest shape manually against official sources.

## Guardrails

- Do not publish, tag, push, or create releases without explicit user approval.
- Do not make a private npm package public just because the plugin is public.
- Do not create a second canonical copy of skills, commands, or agents for another host. Point both hosts at shared folders when possible.
- Do not add marketplace entries with guessed ownership, install policy, authentication policy, product gating, or category if the target marketplace rules are unknown.
- Do not migrate a working Claude plugin to Codex format in-place; add Codex support alongside it.
- Do not flatten Cursor rules, hooks, MCP server configs, or agents into generic skill text just to make them fit Claude or Codex. Keep host-specific primitives in host-specific manifests while preserving one shared plugin identity.
- Do not claim a multi-host plugin is valid until each supported host validator, or explicit manual checks against current official sources, has run.

## Output

When planning, provide:

- plugin-or-skill-collection decision
- manifest inventory
- proposed host support
- file changes
- validation/release plan
- for Cursor, whether the target is local install, public marketplace, team marketplace, or audit only

When implementing, finish with:

- manifests created or changed
- version and marketplace status
- validation results
- release/tag/push status, if requested
- current-source note for Cursor work: which official Cursor docs/repo/schema were checked and when
