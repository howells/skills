# 5. Skills route by model role, never by model name

A portable skill names no model. It asks for a role (the most capable model, the default working model, a cheaper one) and the host resolves it. Behavioural guidance describes the failure mode being guarded against, never the brand it was observed in.

A skill installed globally runs under whichever model the host has that day, across Codex, Claude Code, Cursor and their peers. A model name is a snapshot that constrains the other hosts and goes stale at the next release, and so does a note like "this brand fails by literalism". A preference for a particular model belongs in the host's own configuration.

`scripts/check-skills.py` (`check_model_names`) errors on a model name in any `SKILL.md`, `agents/openai.yaml` or reference file. `review` is exempt because routing to a named model is its purpose, and `deslop` is exempt because it names models only as the provenance of a writing tell. The check is a word list: add the new codename when one appears, and fix a false positive by narrowing the pattern, never by exempting a skill.
