# Dual Plugin Checklist

Use this when creating or reconciling Claude Code and Codex plugin metadata.

## Shared Identity

- Name is normalized and stable.
- Description says what the plugin does, not which host loads it.
- Version is synchronized across all public manifests.
- Repository, license, author, and keywords match.
- Shared content lives in one place: `skills/`, `commands/`, `agents/`, `references/`, `scripts/`, `assets/`.

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

## Release Safety

- Working tree is clean before tagging.
- Release commit is pushed before release tag is pushed.
- Existing tags for the same version do not already exist.
- npm publishing is separate from plugin publishing. A root `"private": true` is usually correct for plugin repos that are not npm packages.
- Release notes mention host-specific changes and any removed commands or skills.
