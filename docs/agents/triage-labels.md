# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

| Label in mattpocock/skills | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation            |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

Edit the right-hand column to match whatever vocabulary you actually use.

## Linear specifics

These labels exist on team `SKI` (Skills):

| Label             | Id                                     |
| ----------------- | -------------------------------------- |
| `needs-triage`    | `a691c353-69ac-4bbe-8f65-ef90a7820d13` |
| `needs-info`      | `f4c1f2e3-fc22-4eb8-8655-b0f16dbbb625` |
| `ready-for-agent` | `bac2dcbd-106c-4f46-8bbf-66ded4da1d4c` |
| `ready-for-human` | `455fe468-75f3-4fc3-9835-cd4243a11ca5` |
| `wontfix`         | `271de113-005f-41f4-bca2-6a3a8a1ae4ce` |

Triage labels are orthogonal to workflow state - an issue can be `Todo` and `needs-info` at the same time. Don't collapse one into the other.

`SKI` also carries `Bug`, `Improvement` and `Feature`. Those describe what an issue *is*; the five above describe what it *needs next*. An issue usually has one of each.

**Linear replaces the label set on update rather than merging it.** Read the issue's current `labelIds`, add or remove the one you mean, and send the whole array back. Sending a single label id silently strips the rest.
