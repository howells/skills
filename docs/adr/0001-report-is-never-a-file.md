# 1. Report is never a file

A report is the message a skill returns in conversation, written to its stated output contract. It is never a document left in the repo. A file exists only when someone asked for one (an artefact), and the durable record of work is a tracker item.

Audit tooling usually finishes by writing a timestamped markdown report, so a skill author reading "report your findings" could reasonably do either. An in-repo trail is diffable; a tracker item is one searchable record visible to people who never clone the repo. We chose the tracker item because scattered repo markdown is how documentation drift starts.

Consequences: no in-repo history of what an audit said, and no diffing last month's findings against this month's. Watch for skills reintroducing a default output file through an `--out` flag or a "save the summary to" step. `scripts/check-vocabulary.py` has a `report-file` rule for the wording, but it cannot catch every shape of the habit.
