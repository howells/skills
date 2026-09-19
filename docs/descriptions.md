# Descriptions and the three sync surfaces

Every skill's description exists in three places and they must agree:

1. the `SKILL.md` frontmatter `description`,
2. the skill's section in `README.md`,
3. `agents/openai.yaml` installer metadata - `display_name`, `short_description` and `default_prompt`, whose `default_prompt` references `$<skill-name>`.

Change one, change all three, then run `python3 scripts/check-skills.py`.

## Budgets

Keep each frontmatter `description` within about 400 characters, and the collection total under the 7,000 the gate enforces. Codex gives the initial skill list at most 2% of the context window or 8,000 characters and shortens descriptions first when it runs out; Claude truncates crowded listings. The gate's 7,000 leaves headroom under the documented cap.

Front-load the use case. Use a terse cross-skill pointer to disambiguate overlapping scope.

## What goes where

Shared discovery stays in portable frontmatter: `name` and `description`. A description says when the skill should fire and when it should not - every one carries a `Not for ...` clause naming the skill that owns the adjacent territory.

Host-specific metadata belongs in `agents/openai.yaml`, under `interface` (UI), `policy` (invocation) or `dependencies` (required MCP servers, declared as `tools` entries with `type`, `value`, `description`, `transport` and `url`). The gate checks each field sits in its own section.

An explicit-only skill pairs `disable-model-invocation: true` with `policy.allow_implicit_invocation: false`. Otherwise omit both and leave implicit discovery enabled.

## No model names in a portable payload

Route by model role - frontier, workhorse, cheap - and let the host resolve it. A codename or product name written into a skill constrains every model that later runs it and goes stale the release after it was written. The only exceptions are skills whose whole purpose is one specific model; the gate errors on any other. The same reasoning applies to behaviour: describe the failure mode you are guarding against, never the brand you saw it in. See `adr/0005`.
