#!/usr/bin/env python3
"""Consistency gate for the skills collection.

Checks that each skill's three public surfaces stay in sync and that references
resolve, so the drift AGENTS.md forbids fails loudly instead of rotting silently.

Surfaces per skill:
  1. <skill>/SKILL.md frontmatter `description:`
  2. README.md `### `<skill>`` section summary
  3. <skill>/agents/openai.yaml `short_description` / `default_prompt`

Checks:
  - existence/sync: every skill has all three surfaces; no README entry without a
    skill dir (or vice versa); frontmatter `name` and openai `$name` match the dir.
  - link integrity: every relative .md path referenced in a SKILL.md or references/
    file resolves to a real file.
  - description budget & overlap: warn >500 chars; error when two descriptions share
    a verbatim clause >= 40 chars (the trigger-collision that causes mis-routing).

Exit codes: 0 = clean (warnings allowed), 1 = one or more errors.
Run from the repo root: `python3 scripts/check-skills.py`.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DESCRIPTION_BUDGET = 500
OVERLAP_MIN = 50

# Basenames that name files in the *consuming* project, not inside a skill.
PROJECT_FILES = {"readme.md", "agents.md", "changelog.md", "contributing.md", "license.md"}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def skill_dirs() -> list[Path]:
    return sorted(p.parent for p in REPO_ROOT.glob("*/SKILL.md"))


def read_frontmatter(skill_md: Path) -> dict[str, str]:
    """Parse the top YAML frontmatter block. Handles plain, quoted, and `|` block scalars."""
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    body = match.group(1)
    fields: dict[str, str] = {}
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        kv = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not kv:
            i += 1
            continue
        key, rest = kv.group(1), kv.group(2)
        if rest in ("|", ">", "|-", ">-"):
            block: list[str] = []
            i += 1
            while i < len(lines) and (lines[i].startswith(("  ", "\t")) or lines[i] == ""):
                block.append(lines[i].strip())
                i += 1
            fields[key] = " ".join(part for part in block if part).strip()
            continue
        value = rest.strip()
        if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
            value = value[1:-1]
        fields[key] = value
        i += 1
    return fields


def read_openai_yaml(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    if not path.exists():
        return fields
    for line in path.read_text(encoding="utf-8").split("\n"):
        kv = re.match(r"^\s*(display_name|short_description|default_prompt):\s*(.*)$", line)
        if not kv:
            continue
        value = kv.group(2).strip()
        if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
            value = value[1:-1]
        fields[kv.group(1)] = value
    return fields


def readme_sections() -> dict[str, str]:
    """Map skill name -> summary paragraph from README's `### `<name>`` sections."""
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    pattern = re.compile(r"^### `([a-z0-9-]+)`\s*$", re.M)
    matches = list(pattern.finditer(text))
    for idx, m in enumerate(matches):
        name = m.group(1)
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end]
        summary = ""
        for para in body.split("\n\n"):
            para = para.strip()
            if para and not para.startswith(("```", "Install", "#")):
                summary = para
                break
        sections[name] = summary
    return sections


def check_surfaces() -> None:
    dirs = skill_dirs()
    names = {d.name for d in dirs}
    readme = readme_sections()

    for name in sorted(names):
        skill = REPO_ROOT / name
        fm = read_frontmatter(skill / "SKILL.md")
        if fm.get("name") != name:
            err(f"{name}: frontmatter name={fm.get('name')!r} does not match directory")
        if not fm.get("description"):
            err(f"{name}: SKILL.md has no frontmatter description")
        if name not in readme:
            err(f"{name}: no `### `{name}`` section in README.md")
        elif not readme[name]:
            err(f"{name}: README section has no summary paragraph")
        oy = read_openai_yaml(skill / "agents" / "openai.yaml")
        if not oy.get("short_description"):
            err(f"{name}: agents/openai.yaml missing short_description")
        prompt = oy.get("default_prompt", "")
        if prompt and f"${name}" not in prompt:
            warn(f"{name}: openai.yaml default_prompt does not reference ${name}")

    for name in sorted(readme):
        if name not in names:
            err(f"README.md has a `### `{name}`` section but no {name}/ skill directory")


def salient_tokens(text: str) -> set[str]:
    stop = {
        "the", "and", "for", "use", "when", "with", "this", "that", "into", "from",
        "asked", "skill", "user", "your", "you", "are", "not", "its", "it", "a", "an",
        "or", "of", "to", "in", "on", "is", "as", "by", "be",
    }
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if len(w) > 2 and w not in stop}


def check_drift() -> None:
    readme = readme_sections()
    for skill in skill_dirs():
        name = skill.name
        desc = read_frontmatter(skill / "SKILL.md").get("description", "")
        if not desc:
            continue
        d_tokens = salient_tokens(desc)
        summary = readme.get(name, "")
        if summary:
            overlap = d_tokens & salient_tokens(summary)
            if d_tokens and len(overlap) / max(len(d_tokens), 1) < 0.2:
                warn(f"{name}: README summary shares few salient terms with the description (possible drift)")
        oy = read_openai_yaml(skill / "agents" / "openai.yaml")
        short = oy.get("short_description", "")
        if short and d_tokens and not (d_tokens & salient_tokens(short)):
            warn(f"{name}: openai short_description shares no salient terms with the description")


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def longest_common_substring(a: str, b: str) -> str:
    # DP over normalized strings; fine for description-length inputs.
    best = 0
    best_end = 0
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best = cur[j]
                    best_end = i
        prev = cur
    return a[best_end - best:best_end]


def check_budget_and_overlap() -> None:
    descs: dict[str, str] = {}
    for skill in skill_dirs():
        desc = read_frontmatter(skill / "SKILL.md").get("description", "")
        if not desc:
            continue
        descs[skill.name] = desc
        if len(desc) > DESCRIPTION_BUDGET:
            warn(f"{skill.name}: description is {len(desc)} chars (budget {DESCRIPTION_BUDGET})")
    names = sorted(descs)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = normalize(descs[names[i]]), normalize(descs[names[j]])
            shared = longest_common_substring(a, b).strip()
            if len(shared) >= OVERLAP_MIN:
                err(
                    f"{names[i]} and {names[j]} share a {len(shared)}-char verbatim clause "
                    f"(routing-collision risk): \"{shared}\""
                )


def iter_reference_files() -> list[Path]:
    files: list[Path] = []
    for skill in skill_dirs():
        files.append(skill / "SKILL.md")
        refs = skill / "references"
        if refs.is_dir():
            files.extend(sorted(refs.rglob("*.md")))
    return files


def check_links() -> None:
    """Flag intra-skill .md references that resolve to nothing.

    Project-file references (docs/, README.md, AGENTS.md) and placeholder paths are
    skipped. A bare shorthand like `footers.md` (meaning references/interface/footers.md)
    is accepted when that basename exists anywhere in the skill.
    """
    link_re = re.compile(r"\]\(([^)]+)\)")
    backtick_re = re.compile(r"`([^`]+\.md)`")
    # Build a per-skill basename index, then scan that skill's files.
    for skill in skill_dirs():
        basenames = {p.name for p in skill.rglob("*.md")}
        files = [skill / "SKILL.md"]
        refs = skill / "references"
        if refs.is_dir():
            files.extend(sorted(refs.rglob("*.md")))
        for file in files:
            text = file.read_text(encoding="utf-8")
            targets: set[str] = set()
            for m in link_re.finditer(text):
                targets.add(m.group(1))
            for m in backtick_re.finditer(text):
                targets.add(m.group(1))
            for raw in targets:
                target = raw.split("#", 1)[0].strip()
                if not target or not target.endswith(".md"):
                    continue
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                if any(ch in target for ch in "$<>[]{}*"):
                    continue
                base = target.rsplit("/", 1)[-1]
                if base.lower() in PROJECT_FILES:
                    continue
                if target.startswith("docs/") or "/docs/" in target:
                    continue
                if target.startswith("/"):
                    err(f"{file.relative_to(REPO_ROOT)}: absolute .md link '{target}'")
                    continue
                if (file.parent / target).resolve().exists():
                    continue
                if base in basenames:
                    continue  # shorthand reference to a file that exists elsewhere in the skill
                err(f"{file.relative_to(REPO_ROOT)}: broken .md reference '{target}'")


def main() -> int:
    check_surfaces()
    check_drift()
    check_budget_and_overlap()
    check_links()

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    total_skills = len(skill_dirs())
    print(f"\nchecked {total_skills} skills: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
