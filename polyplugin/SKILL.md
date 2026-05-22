---
name: polyplugin
description: Create, audit, or migrate an agent plugin so it works across both Claude Code and Codex. Use when asked to make a plugin valid for Claude and Codex, add both .claude-plugin and .codex-plugin manifests, reconcile plugin metadata, create a dual-runtime marketplace entry, validate plugin packaging, or decide whether an existing skill collection should become a plugin.
---

# Polyplugin

Use this skill when a project should be packaged as a plugin for more than one agent host. The goal is one coherent plugin boundary with host-specific manifests, not two drifting products.

## References

Load `references/dual-plugin-checklist.md` when creating or changing manifests.

## Start

When invoked:

1. State that you are using the `polyplugin` skill.
2. Identify the requested host surface:
   - Claude Code plugin
   - Codex plugin
   - both
   - audit only
3. Inspect the repo before editing:
   - `.claude-plugin/plugin.json`
   - `.claude-plugin/marketplace.json`
   - `.codex-plugin/plugin.json`
   - Codex marketplace file if specified
   - `skills/`, `commands/`, `agents/`, `mcp`, `apps`, scripts, assets, and README
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

Do not let Claude and Codex manifests diverge in name, description, version, repository, license, or included skill paths unless a host requires it.

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

### 4. Version Sync

If both hosts are supported, version should be synchronized across:

- root package/release metadata when used
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.codex-plugin/plugin.json`
- Codex marketplace entry, if it carries a version

Use an existing version bump script when present. If none exists, update the minimal set by structured JSON editing, not ad hoc text replacement.

### 5. Validate

Run the smallest complete validation set:

- Claude manifest validation when `.claude-plugin` exists
- Codex manifest validation when `.codex-plugin` exists
- package tests or plugin smoke tests
- version drift check when a script exists

If a validator is unavailable, report the exact validator that was missing and inspect the manifest shape manually.

## Guardrails

- Do not publish, tag, push, or create releases without explicit user approval.
- Do not make a private npm package public just because the plugin is public.
- Do not create a second canonical copy of skills, commands, or agents for another host. Point both hosts at shared folders when possible.
- Do not add marketplace entries with guessed ownership, install policy, authentication policy, product gating, or category if the target marketplace rules are unknown.
- Do not migrate a working Claude plugin to Codex format in-place; add Codex support alongside it.
- Do not claim a dual-host plugin is valid until both host validators, or explicit manual checks, have run.

## Output

When planning, provide:

- plugin-or-skill-collection decision
- manifest inventory
- proposed host support
- file changes
- validation/release plan

When implementing, finish with:

- manifests created or changed
- version and marketplace status
- validation results
- release/tag/push status, if requested
