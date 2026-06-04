# Multi-Host Plugin Checklist

Use this when creating or reconciling Claude Code, Codex, and Cursor plugin metadata.

Cursor plugin details change quickly. Before creating or auditing Cursor manifests, verify the current official sources:

- Cursor docs: `https://cursor.com/docs/plugins`
- Cursor plugin reference: `https://cursor.com/docs/reference/plugins`
- Official plugin repo and schemas: `https://github.com/cursor/plugins`
- Cursor plugin template, when relevant: `https://github.com/cursor/plugin-template`

The Cursor notes below reflect official docs and `cursor/plugins` commit `c8402bc8e3673b973719fe3acc2c4837fef34f86` as checked on 2026-06-04.

## Shared Identity

- Name is normalized and stable.
- Description says what the plugin does, not which host loads it.
- Version is synchronized across all public manifests.
- Repository, license, author, and keywords match.
- Shared content lives in one place: `skills/`, `commands/`, `agents/`, `references/`, `scripts/`, `assets/`.
- Host-specific primitives stay host-specific: Cursor `rules/`, `hooks/`, and `mcp.json`; Claude command routers; Codex interface metadata; host-specific marketplace files.
- Do not duplicate canonical skill, command, or agent text per host unless the host format requires a wrapper.

## Claude Code Surface

Expected files:

- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json` when the repo is a marketplace source

Common checks:

- `plugin.json` points to existing `skills` and `commands` directories when used.
- Marketplace plugin entry version matches `plugin.json`.
- `claude plugins validate .` passes.
- Release tags use `claude plugins tag .` so the tag name matches plugin metadata.

## Codex Surface

Expected files:

- `.codex-plugin/plugin.json`
- optional marketplace entry, commonly in a repo or personal marketplace file

Common checks:

- The manifest uses only fields accepted by Codex validation.
- Optional folders such as MCP, apps, scripts, or assets are declared only when they exist.
- Marketplace entries include required policy/category fields when that marketplace format requires them.
- If the local `plugin-creator` skill is available, use its validator or scaffold scripts instead of guessing the exact schema.

## Cursor Surface

Expected files for a single plugin:

- `.cursor-plugin/plugin.json` at the plugin root
- `README.md`
- `LICENSE`
- optional `CHANGELOG.md`
- optional `assets/` for logos and images
- component folders as needed: `skills/`, `commands/`, `agents/`, `rules/`, `hooks/`
- optional `mcp.json` for MCP server definitions

Expected files for a multi-plugin marketplace repository:

- root `.cursor-plugin/marketplace.json`
- one directory per plugin
- each plugin directory has its own `.cursor-plugin/plugin.json`

Current manifest schema checks:

- `.cursor-plugin/plugin.json` requires `name`.
- `name` must match `^[a-z0-9]([a-z0-9.-]*[a-z0-9])?$`.
- Recommended plugin fields: `displayName`, `description`, `version`, `author`, `publisher`, `homepage`, `repository`, `license`, `logo`, `keywords`, `category`, `tags`.
- Component fields are `commands`, `agents`, `skills`, `rules`, `hooks`, and `mcpServers`.
- `commands`, `agents`, `skills`, and `rules` accept a string path/glob or an array of string paths/globs.
- `hooks` accepts a path string or inline hooks object.
- `mcpServers` accepts a path string, inline config object, or array of either.
- The schema disallows unknown top-level fields, so do not add Claude/Codex fields or invented aliases.
- Paths should be relative to the plugin root and should not use absolute paths or `..`.

Current Cursor marketplace schema checks:

- `.cursor-plugin/marketplace.json` requires `name` and `plugins`.
- Optional top-level fields are `owner` and `metadata`.
- `owner` requires `name` and may include `email`.
- `metadata` may include `description`.
- Each plugin entry requires `name` and `source`, and may include `description`.
- Do not put version, category, tags, keywords, author, license, or repository in marketplace plugin entries; the current schema rejects unknown fields.
- Marketplace entry `name` must match the plugin's `.cursor-plugin/plugin.json` `name`.
- `source` is a plugin directory path relative to the marketplace root or a remote URL. For local repository validation, relative sources must resolve to plugin directories.

Current component checks:

- Skills: `skills/<skill-name>/SKILL.md` with `name` and `description` frontmatter.
- Rules: `rules/*.mdc` with frontmatter. `description` is required for Agent Requested rules; `alwaysApply` and optional `globs` control application mode.
- Agents: markdown files under `agents/` with `name` and `description` frontmatter.
- Commands: markdown or text files under `commands/` with `name` and `description` frontmatter.
- Hooks: commonly `hooks/hooks.json`, with scripts under `hooks/`; verify event names and input/output contract against current Cursor hook docs.
- MCP: use `mcp.json` or `mcpServers`; verify Cursor's current MCP transport and install-link guidance before publishing.

Current local testing checks:

- Copy or symlink the plugin to `~/.cursor/plugins/local/<plugin-name>/`.
- `.cursor-plugin/plugin.json` must sit at that plugin root.
- Restart Cursor or run `Developer: Reload Window`.
- Verify loaded components in Cursor: skills/rules in settings, MCP servers in MCP settings, hooks/agents/commands where applicable.

Distribution checks:

- Public marketplace plugins are distributed as Git repositories and submitted through Cursor's publishing flow.
- Cursor docs state marketplace plugins are manually reviewed before listing; do not claim acceptance or listing until review completes.
- Team marketplaces are separate from public marketplace listings and may depend on Teams or Enterprise plan features.
- Required-vs-optional team distribution is an admin policy decision, not a manifest field to guess.
- Cursor also supports VS Code/Open VSX extensions, but that is a separate extension surface and not a `.cursor-plugin` package.

## Release Safety

- Working tree is clean before tagging.
- Release commit is pushed before release tag is pushed.
- Existing tags for the same version do not already exist.
- npm publishing is separate from plugin publishing. A root `"private": true` is usually correct for plugin repos that are not npm packages.
- Release notes mention host-specific changes and any removed commands or skills.
- For Cursor releases, verify whether the target is local install, public marketplace submission, team marketplace import, or GitHub release. Do not substitute one distribution path for another.
