#!/usr/bin/env python3
"""Vocabulary gate: flag prose that contradicts CONTEXT.md.

CONTEXT.md fixes the words this collection uses about itself. A glossary nobody
checks is a glossary that drifts, so this reads the rules below over every
SKILL.md and reference file and reports the lines that break them.

The hard part is that several governed words are also ordinary verbs. "Surface
the conflict explicitly" is correct English and correct house style; "the
surface" as a bare noun is not. Rules therefore match the *noun* uses and
exempt the verb ones, rather than matching the word.

Precision is deliberately traded for recall: a rule that flags a correct line
is fixed by adding that line to ALLOW, not by loosening the rule. The allowlist
is the record of what was adjudicated and why.

Exit codes: 0 = clean, 1 = violations. Run from the repo root.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Determiners that mark the following word as a noun rather than a verb.
DET = r"(?:the|a|an|its|their|this|that|each|every|one|another|our|your)"

RULES: list[tuple[str, str, str]] = [
    # (name, pattern, guidance)
    (
        "bare-surface",
        rf"\b{DET}\s+surfaces?\b(?!\s+(?:area|of\b))",
        'bare "surface" — qualify it (sync/public/host/sensitive/agent surface)',
    ),
    (
        "bare-surface-plural",
        r"(?<!\w)(?<!UI )(?<!ui )(?<!sync )(?<!host )(?<!public )(?<!agent )"
        r"(?<!sensitive )(?<!attack )(?<!API )(?<!api )(?<!design )(?<!injection )"
        r"surfaces\b(?!\s+(?:a|an|the|it|them|this|that|while|when|during|later|here|mid))",
        'bare "surfaces" as a noun — qualify it, or reword if it is the verb',
    ),
    (
        # Skipped entirely when a verb of holding/returning precedes it: "the
        # arm returns a reference" is a pointer to stored data, a general
        # programming concept that CONTEXT.md deliberately does not govern.
        "bare-reference",
        rf"(?<!returns )(?<!return )(?<!validates )(?<!validate )(?<!holds )(?<!hold )"
        rf"(?<!stores )(?<!store )(?<!passes )(?<!pass )\b{DET}\s+references?\b(?!\s+(?:file|implementation|set|catalogue|documents?"
        rf"|curve|url|link|screenshot|curve|point|design|image|material|model|architecture|build))",
        'bare "reference" — say "reference file", or "cross-pointer" if it points at another skill',
    ),
    (
        # Scoped to foreman: that is where the decision bites. Elsewhere "the
        # spec" is anaphora after "design spec" is established, which is
        # ordinary English and needs no repair.
        "foreman-spec",
        r"\b(?:the|a|its)\s+spec\b",
        'bare "spec" means a tracker item that names no file paths; an agent instruction is a "brief"',
    ),
    (
        # Inverted from the obvious form on purpose. The lifecycle sense is
        # correct and common; only the migration sense is wrong, so the rule
        # requires migration context on the same line rather than flagging
        # every "the stage".
        "staged-migration",
        r"\bstage\b(?=[^.]*\b(?:migration|migrat\w+|transitional|rollout|canonical implementation)\b)"
        r"|\b(?:migration|transitional|rollout)\b[^.]*\bstage\b",
        '"stage" is lifecycle only; a transitional state is a "staged migration"',
    ),
    (
        "report-file",
        r"\breport\s+(?:file|document)\b|\bwrite\s+(?:a|the)\s+report\b",
        "a report is a message; a file someone asked for is an artefact, and the record is a tracker item",
    ),
]

# Lines adjudicated as correct despite matching a rule. Keyed by rule name;
# each entry is a substring that must appear in the offending line.
ALLOW: dict[str, list[str]] = {
    "bare-surface": [
        "the surface is the product",  # foreman: idiomatic, means the visible product
    ],
    "bare-surface-plural": [
        "surfaces deepening",  # verb
        "surfaces what",  # verb
        "surfaces the",  # verb
        "it surfaces",  # verb
        "surfaces and",  # ambiguous prose, adjudicated fine in context
    ],
    "bare-reference": [
        "the reference has",
        "the reference set",
    ],
    "foreman-spec": [
        "spec-complete",  # established adjective: fully pinned down
        "the spec source",  # code-review's own term for an upstream document
    ],
    "staged-migration": [
        "a staged migration",
        "the stage drives",
        "a stage-calibrated",
    ],
    "report-file": [
        "Writing a report file nobody asked for",  # survey: named as a failure mode
        "report file into the repo",  # survey: prohibition, not instruction
    ],
}

# Files this gate does not govern.
SKIP_NAMES = {"CONTEXT.md", "CHANGELOG.md"}

# A rule does not apply to a file whose own subject is that word. A chapter
# about UI surfaces says "the surface" the way a chapter about colour says
# "the colour"; forcing the qualifier there produces worse prose, not clearer
# prose. Scoped per rule so the exemption cannot leak.
SUBJECT_FILES: dict[str, set[str]] = {}

# Whole trees a rule does not govern, because the word's domain sense lives
# there. chiaroscuro means a UI surface — a card, a panel, a raised
# layer. product-description means the bounded user experience under study.
# Both are real domain senses, not the sync/public/host sense this rule polices.
SUBJECT_TREES: dict[str, tuple[str, ...]] = {
    "bare-surface": ("chiaroscuro/", "product-description/"),
    "bare-surface-plural": ("chiaroscuro/", "product-description/"),
}

# Rules that apply only within certain paths.
SCOPED: dict[str, str] = {
    "foreman-spec": "foreman/",
}


def governed_files() -> list[Path]:
    """Every SKILL.md and reference file, excluding generated copies.

    Generated copies are excluded because editing one is itself an error — the
    shared source is the only place a shared file is fixed. check-skills.py
    already enforces that copies match their source.
    """
    import json

    manifest_path = REPO_ROOT / "shared" / "manifest.json"
    generated: set[Path] = set()
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        generated = {REPO_ROOT / rel for copies in manifest.values() for rel in copies}

    files: list[Path] = []
    for skill_md in sorted(REPO_ROOT.glob("*/SKILL.md")):
        files.append(skill_md)
        refs = skill_md.parent / "references"
        if refs.is_dir():
            files.extend(sorted(p for p in refs.rglob("*.md") if p not in generated))
    files.extend(sorted(REPO_ROOT.glob("shared/*.md")))
    return [f for f in files if f.name not in SKIP_NAMES]


def allowed(rule: str, line: str) -> bool:
    return any(frag.lower() in line.lower() for frag in ALLOW.get(rule, ()))


def check() -> int:
    violations: list[tuple[Path, int, str, str, str]] = []
    for path in governed_files():
        in_fence = False
        for lineno, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            # Fenced blocks, shell examples and tables are not prose.
            if in_fence or line.lstrip().startswith(("$ ", "#!", "|")):
                continue
            rel = str(path.relative_to(REPO_ROOT))
            for name, pattern, guidance in RULES:
                if name in SCOPED and not rel.startswith(SCOPED[name]):
                    continue
                if rel in SUBJECT_FILES.get(name, ()):
                    continue
                if rel.startswith(SUBJECT_TREES.get(name, ())):
                    continue
                match = re.search(pattern, line, re.I)
                if match and not allowed(name, line):
                    violations.append((path, lineno, name, match.group(0).strip(), guidance))

    if not violations:
        print(f"vocabulary: clean across {len(governed_files())} files")
        return 0

    by_rule: dict[str, list] = {}
    for v in violations:
        by_rule.setdefault(v[2], []).append(v)

    for name, items in sorted(by_rule.items(), key=lambda kv: -len(kv[1])):
        print(f"\n{name} — {items[0][4]}")
        for path, lineno, _, phrase, _ in items:
            print(f"  {path.relative_to(REPO_ROOT)}:{lineno}: {phrase!r}")

    print(f"\n{len(violations)} violation(s) across {len({v[0] for v in violations})} file(s)")
    print("Fix the prose, or add the line to ALLOW with a reason if it is correct.")
    return 1


if __name__ == "__main__":
    sys.exit(check())
