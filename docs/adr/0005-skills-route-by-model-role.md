# 5. Skills route by model role, never by model name

Date: 2026-09-16
Status: Accepted

## Context

Five skills carried model names in their portable payload. `next`, `rebalance` and `simplify` preferred one provider's codenames for their delegation roles, and `next` repeated them in its Codex default prompt. `foreman` hardcoded a dated table mapping its frontier, workhorse and cheap roles to one host's models, and described delegate failure modes by brand. `blender` escalated judgement calls to a named model.

Every one of those names is a snapshot. The codenames in `next` belonged to a model generation that has since been superseded; the mapping in `foreman` said "as of mid-2026" and asked the reader to re-derive it if stale, which is an admission that the sentence would be wrong soon. A skill installed globally runs under whichever model the host has that day, across Codex, Claude Code, Cursor and their peers, so a name written for one of them constrains the rest, and a brand-specific behavioural note ("this brand fails by literalism") stops being true at the next release.

The repository already forbade personal names, account inventories and machine paths in portable payloads for the same reason: an installed skill must stand alone, and what is true of one installer's environment is not true of the next.

## Decision

A portable skill names no model. It asks for a **model role**, defined in `CONTEXT.md`: frontier, workhorse or cheap. The host resolves the role to what it runs. Behavioural guidance describes the failure mode being guarded against, never the brand it was observed in.

Two skills are exempt because a specific model is their purpose: `fable-review` and `glm-review`. `check-skills.py` errors on a model name anywhere else in a `SKILL.md`, its `agents/openai.yaml` or its reference files.

## Consequences

`next`, `rebalance`, `simplify`, `foreman` and `blender` now describe roles. A maintainer who wants a skill to prefer a particular model can no longer write it into the skill; that preference belongs in the host's own configuration, where it applies to the person who set it.

The gate is a word list, and it will need a new entry when a new codename appears. Adding one is a one-line change. A false positive on an ordinary English word is fixed by narrowing the pattern, never by exempting the skill.
