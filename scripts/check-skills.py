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
  - strict YAML: unquoted scalar values in SKILL.md frontmatter and openai.yaml must
    not contain patterns that strict parsers (GitHub, installers) reject or silently
    truncate - `: `, ` #`, a leading indicator character, or a trailing colon.
  - link integrity: every relative .md path referenced in a SKILL.md or references/
    file resolves to a real file.
  - metadata budgets: warn when one description exceeds 400 chars; error when the
    collection exceeds 7,000 chars or a Codex short description is outside 25-64.
  - routing consistency: README summaries match descriptions exactly, default prompts
    name their `$skill`, Claude/Codex invocation policy agrees, and descriptions do
    not share a long verbatim trigger clause.
  - openai schema: every field in agents/openai.yaml sits in its own section
    (interface / policy / dependencies) per the published Codex skill schema, so a
    field at the wrong depth fails instead of being silently ignored by Codex.
  - removed skills: no document points at a skill the collection no longer has, which
    the three-surface check cannot see because the surviving copies still agree.

Exit codes: 0 = clean (warnings allowed), 1 = one or more errors.
Run from the repo root: `python3 scripts/check-skills.py`.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DESCRIPTION_BUDGET = 400
COLLECTION_DESCRIPTION_BUDGET = 7000
OPENAI_SHORT_DESCRIPTION_MIN = 25
OPENAI_SHORT_DESCRIPTION_MAX = 64
OVERLAP_MIN = 50
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Basenames that name files in the *consuming* project, not inside a skill.
PROJECT_FILES = {
    "readme.md",
    "agents.md",
    "claude.md",
    "changelog.md",
    "contributing.md",
    "license.md",
    "goal.md",
    "glossary.md",
    "bug-triage.md",
}

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


# The `agents/openai.yaml` schema, from
# https://learn.chatgpt.com/docs/build-skills. A field is only valid inside its
# own section, so matching names at any indentation would accept
# `display_name` at top level or `allow_implicit_invocation` under `interface`.
OPENAI_SCHEMA: dict[str, set[str]] = {
    "interface": {
        "display_name",
        "short_description",
        "default_prompt",
        "icon_small",
        "icon_large",
        "brand_color",
    },
    "policy": {"allow_implicit_invocation"},
    "dependencies": {"tools"},
}
TOOL_FIELDS = {"type", "value", "description", "transport", "url"}
YAML_BOOLEANS = {"true", "false"}


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
        return value[1:-1]
    return value


def read_openai_yaml(path: Path, report: bool = False) -> dict[str, str]:
    """Read `agents/openai.yaml`, validating section structure when `report`.

    Returns the interface and policy fields flattened by name, which is what the
    surface checks compare against. Structural errors are reported rather than
    returned, so a malformed file still yields whatever it did define.
    """
    fields: dict[str, str] = {}
    if not path.exists():
        return fields

    rel = path.relative_to(REPO_ROOT)
    section = ""
    subkey = ""
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()

        if indent == 0:
            section = stripped.split(":", 1)[0].strip()
            subkey = ""
            if report and section not in OPENAI_SCHEMA:
                owner = next((s for s, keys in OPENAI_SCHEMA.items() if section in keys), None)
                if owner:
                    err(f"{rel}:{lineno}: `{section}` belongs under `{owner}`, not at top level")
                else:
                    err(f"{rel}:{lineno}: unknown top-level section `{section}`")
            continue

        if stripped.startswith("- ") or stripped == "-":
            if report and (section, subkey) != ("dependencies", "tools"):
                err(f"{rel}:{lineno}: list item outside `dependencies.tools`")
            stripped = stripped[2:].strip()
            if not stripped:
                continue

        kv = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", stripped)
        if not kv:
            continue
        key, value = kv.group(1), kv.group(2).strip()

        if section == "dependencies":
            if key == "tools" and not value:
                subkey = "tools"
                continue
            if subkey == "tools":
                if report and key not in TOOL_FIELDS:
                    err(f"{rel}:{lineno}: unknown field `{key}` in a `dependencies.tools` entry")
                continue

        if report:
            allowed = OPENAI_SCHEMA.get(section)
            if allowed is not None and key not in allowed:
                owner = next((s for s, keys in OPENAI_SCHEMA.items() if key in keys), None)
                if owner:
                    err(f"{rel}:{lineno}: `{key}` belongs under `{owner}`, not `{section}`")
                else:
                    err(f"{rel}:{lineno}: unknown field `{key}` under `{section}`")
            if key == "allow_implicit_invocation" and unquote(value) not in YAML_BOOLEANS:
                err(f"{rel}:{lineno}: `allow_implicit_invocation` must be true or false")

        if section in ("interface", "policy"):
            fields[key] = unquote(value)
    return fields


# Characters that cannot open a plain (unquoted) YAML scalar.
YAML_LEAD_INDICATORS = set("!&*?|>%@`\"'#,[]{}")


def plain_scalar_hazard(value: str) -> str | None:
    """Why a plain YAML scalar would break or change meaning under a strict parser.

    The regex readers above are lenient, but GitHub's frontmatter renderer and
    skill installers parse these files with real YAML parsers. Returns a human
    explanation, or None when the value is safe.
    """
    if ": " in value or value.endswith(":"):
        return "unquoted ': ' starts a nested mapping under strict YAML parsers"
    if " #" in value:
        return "unquoted ' #' starts a comment; the rest of the value is dropped"
    if value and value[0] in YAML_LEAD_INDICATORS:
        return f"leading {value[0]!r} is a YAML indicator and cannot open a plain scalar"
    if value.startswith(("- ", "? ")):
        return f"leading {value[:2]!r} is a YAML block indicator"
    return None


def check_yaml_strictness() -> None:
    """Line-scan frontmatter and openai.yaml for plain scalars strict parsers reject."""
    kv_re = re.compile(r"^(\s*)([A-Za-z0-9_-]+):\s+(\S.*)$")
    for skill in skill_dirs():
        targets = [(skill / "SKILL.md", True), (skill / "agents" / "openai.yaml", False)]
        for path, frontmatter_only in targets:
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            if frontmatter_only:
                match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
                if not match:
                    err(f"{skill.name}: SKILL.md has no frontmatter block")
                    continue
                text = match.group(1)
            for lineno, line in enumerate(text.split("\n"), start=1 + frontmatter_only):
                kv = kv_re.match(line)
                if not kv:
                    continue
                value = kv.group(3).strip()
                if value[0] in "\"'" or value in ("|", ">", "|-", ">-"):
                    continue  # quoted or block scalar: strict parsers handle these
                hazard = plain_scalar_hazard(value)
                if hazard:
                    err(
                        f"{path.relative_to(REPO_ROOT)}:{lineno}: "
                        f"`{kv.group(2)}` - {hazard}; quote the value or reword"
                    )


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
        if len(name) > 64 or not SKILL_NAME_RE.fullmatch(name):
            err(f"{name}: directory name must be <=64 lowercase letters, digits, and single hyphens")
        if fm.get("name") != name:
            err(f"{name}: frontmatter name={fm.get('name')!r} does not match directory")
        if not fm.get("description"):
            err(f"{name}: SKILL.md has no frontmatter description")
        if name not in readme:
            err(f"{name}: no `### `{name}`` section in README.md")
        elif not readme[name]:
            err(f"{name}: README section has no summary paragraph")
        oy = read_openai_yaml(skill / "agents" / "openai.yaml", report=True)
        if not oy.get("display_name"):
            err(f"{name}: agents/openai.yaml missing display_name")
        if not oy.get("short_description"):
            err(f"{name}: agents/openai.yaml missing short_description")
        elif not OPENAI_SHORT_DESCRIPTION_MIN <= len(oy["short_description"]) <= OPENAI_SHORT_DESCRIPTION_MAX:
            err(
                f"{name}: openai short_description is {len(oy['short_description'])} chars "
                f"(required {OPENAI_SHORT_DESCRIPTION_MIN}-{OPENAI_SHORT_DESCRIPTION_MAX})"
            )
        prompt = oy.get("default_prompt", "")
        if not prompt:
            err(f"{name}: agents/openai.yaml missing default_prompt")
        elif f"${name}" not in prompt:
            err(f"{name}: openai.yaml default_prompt does not reference ${name}")

        claude_manual = fm.get("disable-model-invocation", "false").lower() in {
            "true", "yes", "on", "1",
        }
        codex_implicit = oy.get("allow_implicit_invocation", "true").lower() in {
            "true", "yes", "on", "1",
        }
        if claude_manual == codex_implicit:
            err(
                f"{name}: Claude disable-model-invocation and Codex "
                "allow_implicit_invocation disagree"
            )

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
        if summary and summary != desc:
            err(f"{name}: README summary does not exactly match the SKILL.md description")
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
    total = sum(len(desc) for desc in descs.values())
    if total > COLLECTION_DESCRIPTION_BUDGET:
        err(
            f"skill descriptions total {total} chars "
            f"(collection budget {COLLECTION_DESCRIPTION_BUDGET})"
        )
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


# Skills removed from the collection. A deletion leaves the name behind in every
# neighbour that pointed at it, and the sync-surface check passes because the three
# copies still agree with each other. Add a name here when a skill is removed; drop
# it only if the name is ever reused.
REMOVED_SKILLS = (
    "aperture",
    "fenceline",
    "foundry",
    "heathen",
    "inquest",
    "polyplugin",
)


def check_cross_pointers() -> None:
    """Flag a backticked reference to a skill the collection no longer has."""
    pattern = re.compile(r"`(" + "|".join(REMOVED_SKILLS) + r")`")
    readme = REPO_ROOT / "README.md"
    docs = iter_reference_files() + [readme, REPO_ROOT / "CLAUDE.md", REPO_ROOT / "AGENTS.md"]
    for path in docs:
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            # The README's removal table is the one place the names belong.
            if path == readme and line.lstrip().startswith("| `"):
                continue
            m = pattern.search(line)
            if m:
                rel = path.relative_to(REPO_ROOT)
                err(f"{rel}:{i}: points at `{m.group(1)}`, removed from the collection")


def main() -> int:
    check_surfaces()
    check_yaml_strictness()
    check_drift()
    check_budget_and_overlap()
    check_links()
    check_cross_pointers()

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    total_skills = len(skill_dirs())
    print(f"\nchecked {total_skills} skills: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
