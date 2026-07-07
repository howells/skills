#!/usr/bin/env python3
"""Rank likely god files and exact duplicate blocks in JS/TS codebases."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SOURCE_EXTENSIONS = {
    ".cjs",
    ".cts",
    ".js",
    ".jsx",
    ".mjs",
    ".mts",
    ".ts",
    ".tsx",
}

IGNORED_DIRS = {
    ".git",
    ".mastra",
    ".next",
    ".nuxt",
    ".output",
    ".turbo",
    ".vercel",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "storybook-static",
}

IGNORED_FILE_PATTERNS = (
    ".d.ts",
    ".generated.ts",
    ".generated.tsx",
    ".gen.ts",
    ".gen.tsx",
    ".spec.js",
    ".spec.jsx",
    ".spec.ts",
    ".spec.tsx",
    ".stories.js",
    ".stories.jsx",
    ".stories.ts",
    ".stories.tsx",
    ".test.js",
    ".test.jsx",
    ".test.ts",
    ".test.tsx",
)

# Test-suffix patterns re-included when --include-tests is passed.
TEST_FILE_PATTERNS = {
    ".spec.js",
    ".spec.jsx",
    ".spec.ts",
    ".spec.tsx",
    ".test.js",
    ".test.jsx",
    ".test.ts",
    ".test.tsx",
}

FUNCTION_RE = re.compile(
    r"\b(?:async\s+)?function\s+[A-Za-z0-9_$]+\s*\(|"
    r"\b(?:const|let|var)\s+[A-Za-z0-9_$]+(?:\s*:\s*[^=]+)?\s*=\s*(?:async\s*)?\([^)]*\)(?:\s*:\s*[^=]+)?\s*=>|"
    r"\b(?:const|let|var)\s+[A-Za-z0-9_$]+(?:\s*:\s*[^=]+)?\s*=\s*(?:async\s*)?[A-Za-z0-9_$]+(?:\s*:\s*[^=]+)?\s*=>"
)

COMPONENT_RE = re.compile(
    r"\b(?:export\s+)?function\s+[A-Z][A-Za-z0-9_$]*\s*\(|"
    r"\b(?:export\s+)?const\s+[A-Z][A-Za-z0-9_$]*(?:\s*:\s*[^=]+)?\s*=\s*(?:\([^)]*\)|[A-Za-z0-9_$]+)(?:\s*:\s*[^=]+)?\s*=>"
)

IMPORT_RE = re.compile(r"^\s*import\b|^\s*const\s+.*\s*=\s*require\(", re.MULTILINE)
EXPORT_RE = re.compile(r"^\s*export\b", re.MULTILINE)

RESPONSIBILITY_PATTERNS = {
    "ui": (r"<[A-Z_a-z][A-Za-z0-9_.:-]*(\s|>|/>)", r"\bclassName\s*="),
    "react-state": (r"\buse(State|Reducer|Effect|Memo|Callback|Ref)\b",),
    "forms-validation": (r"\bz\.object\b", r"\buseForm\b", r"\bvalidate\b", r"\bvalidation\b"),
    "network": (r"\bfetch\s*\(", r"\baxios\b", r"\bky\.", r"\btrpc\b", r"\bapi\.", r"/api/"),
    "database": (r"\bdrizzle\b", r"\bdb\.", r"\bselect\(", r"\binsert\(", r"\bupdate\("),
    "filesystem": (r"\bfs\.", r"node:fs", r"\breadFile", r"\bwriteFile"),
    "process-cli": (r"\bprocess\.argv\b", r"\bcommander\b", r"\byargs\b", r"\bprocess\.exit\b"),
    "routing": (r"\buseRouter\b", r"\bredirect\(", r"\bparams\b", r"\bsearchParams\b"),
    "testing": (r"\bdescribe\(", r"\bit\(", r"\btest\(", r"\bexpect\("),
}


@dataclass(frozen=True)
class FileMetrics:
    path: str
    category: str
    score: int
    lines: int
    nonblank_lines: int
    imports: int
    exports: int
    functions: int
    components: int
    responsibilities: list[str]
    reasons: list[str]


def should_ignore_file(path: Path, *, include_tests: bool = False) -> bool:
    name = path.name
    ignored_patterns = IGNORED_FILE_PATTERNS
    if include_tests:
        ignored_patterns = tuple(
            pattern
            for pattern in IGNORED_FILE_PATTERNS
            if pattern not in TEST_FILE_PATTERNS
        )
    return any(name.endswith(pattern) for pattern in ignored_patterns)


def iter_source_files(root: Path, *, include_tests: bool = False) -> list[Path]:
    files = []
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            name
            for name in dirnames
            if name not in IGNORED_DIRS and (include_tests or name != "__tests__")
        ]
        current = Path(current_root)
        for filename in filenames:
            path = current / filename
            if path.suffix in SOURCE_EXTENSIONS and not should_ignore_file(path, include_tests=include_tests):
                files.append(path)
    return sorted(files)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def detect_category(path: Path, content: str, root: Path) -> str:
    if path.name.endswith((".test.ts", ".test.tsx", ".test.js", ".test.jsx", ".spec.ts", ".spec.tsx", ".spec.js", ".spec.jsx")):
        return "test"
    rel_parts = path.relative_to(root).parts
    dir_parts = rel_parts[:-1]
    if "scripts" in dir_parts or "bin" in dir_parts or path.name.startswith(("script-", "migrate-", "seed-")):
        return "script"
    if path.suffix in {".tsx", ".jsx"} or COMPONENT_RE.search(content):
        return "component"
    return "module"


def detect_responsibilities(content: str) -> list[str]:
    detected = []
    for name, patterns in RESPONSIBILITY_PATTERNS.items():
        if any(re.search(pattern, content) for pattern in patterns):
            detected.append(name)
    return detected


def file_metrics(path: Path, root: Path) -> FileMetrics:
    content = read_text(path)
    lines = content.splitlines()
    nonblank_lines = [line for line in lines if line.strip()]
    imports = len(IMPORT_RE.findall(content))
    exports = len(EXPORT_RE.findall(content))
    functions = len(FUNCTION_RE.findall(content))
    components = len(COMPONENT_RE.findall(content))
    responsibilities = detect_responsibilities(content)
    category = detect_category(path, content, root)

    score = 0
    reasons = []
    line_count = len(lines)
    if line_count >= 500:
        score += 60
        reasons.append(f"{line_count} lines")
    elif line_count >= 300:
        score += 35
        reasons.append(f"{line_count} lines")
    elif line_count >= 200:
        score += 20
        reasons.append(f"{line_count} lines")

    if functions >= 20:
        score += 35
        reasons.append(f"{functions} functions")
    elif functions >= 12:
        score += 20
        reasons.append(f"{functions} functions")
    elif functions >= 8:
        score += 10
        reasons.append(f"{functions} functions")

    if components >= 5:
        score += 30
        reasons.append(f"{components} components")
    elif components >= 3:
        score += 15
        reasons.append(f"{components} components")

    if len(responsibilities) >= 5:
        score += 35
        reasons.append(f"{len(responsibilities)} responsibility signals")
    elif len(responsibilities) >= 3:
        score += 18
        reasons.append(f"{len(responsibilities)} responsibility signals")

    if imports >= 25:
        score += 15
        reasons.append(f"{imports} imports")
    if exports >= 12:
        score += 15
        reasons.append(f"{exports} exports")

    if category == "component" and line_count >= 180 and components >= 2:
        score += 15
        reasons.append("large component file with nested components")
    if category == "script" and line_count >= 220 and len(responsibilities) >= 3:
        score += 15
        reasons.append("script mixes multiple concerns")

    return FileMetrics(
        path=relative(path, root),
        category=category,
        score=score,
        lines=line_count,
        nonblank_lines=len(nonblank_lines),
        imports=imports,
        exports=exports,
        functions=functions,
        components=components,
        responsibilities=responsibilities,
        reasons=reasons,
    )


def normalize_line(line: str) -> str:
    stripped = line.strip()
    stripped = strip_line_comment(stripped)
    stripped = re.sub(r"\s+", " ", stripped)
    return stripped


def strip_line_comment(line: str) -> str:
    in_string = False
    quote = ""
    escaped = False
    for index, char in enumerate(line):
        next_char = line[index + 1] if index + 1 < len(line) else ""
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                in_string = False
            continue
        if char in {"'", '"', "`"}:
            in_string = True
            quote = char
            continue
        if char == "/" and next_char == "/":
            return line[:index].rstrip()
    return line


def is_meaningful_duplicate_line(line: str) -> bool:
    if not line:
        return False
    if re.match(r"^(import|export)\b", line):
        return False
    if re.match(r"^[{}()[\],.;:]+$", line):
        return False
    if line in {"},", "});", "};", "}", ");"}:
        return False
    return len(line) >= 8


def duplicate_blocks(root: Path, window: int, *, include_tests: bool = False) -> list[dict[str, Any]]:
    occurrences: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for path in iter_source_files(root, include_tests=include_tests):
        raw_lines = read_text(path).splitlines()
        normalized = [normalize_line(line) for line in raw_lines]
        indexed = [(index + 1, line) for index, line in enumerate(normalized) if line]
        if len(indexed) < window:
            continue
        for offset in range(0, len(indexed) - window + 1):
            chunk = indexed[offset : offset + window]
            text = "\n".join(line for _, line in chunk)
            if len(text) < 120:
                continue
            meaningful_lines = [line for _, line in chunk if is_meaningful_duplicate_line(line)]
            if len(meaningful_lines) < max(3, window // 2):
                continue
            digest = hashlib.sha1(text.encode("utf-8")).hexdigest()
            occurrences[digest].append(
                {
                    "path": relative(path, root),
                    "start": chunk[0][0],
                    "end": chunk[-1][0],
                    "preview": meaningful_lines[0][:100],
                }
            )

    raw_groups = []
    for matches in occurrences.values():
        locations = sorted({(match["path"], match["start"], match["end"]) for match in matches})
        if len(locations) < 2:
            continue
        preview = matches[0]["preview"]
        raw_groups.append({"locations": locations, "preview": preview})

    groups = []
    for merged in merge_overlapping_groups(raw_groups, window):
        locations = merged["locations"]
        unique_files = {loc[0] for loc in locations}
        span = max(end - start + 1 for _, start, end in locations)
        groups.append(
            {
                "files": len(unique_files),
                "occurrences": len(locations),
                "lines": span,
                "window": window,
                "matches": [
                    {"path": path, "start": start, "end": end, "preview": merged["preview"]}
                    for path, start, end in locations[:8]
                ],
            }
        )
    # Rank a single large duplicated region above many small ones: files, then span, then count.
    return sorted(groups, key=lambda item: (item["files"], item["lines"], item["occurrences"]), reverse=True)


def _parallel_overlap(locs_a: list[tuple[str, int, int]], locs_b: list[tuple[str, int, int]]) -> bool:
    """True when two window groups are the same duplicated region shifted by a few lines.

    Requires the same number of occurrences, the same files in the same order, and every
    corresponding interval to overlap or sit adjacent — so sliding windows over one region
    collapse together while genuinely distinct regions stay separate.
    """
    if len(locs_a) != len(locs_b):
        return False
    for (path_a, start_a, end_a), (path_b, start_b, end_b) in zip(locs_a, locs_b):
        if path_a != path_b:
            return False
        if start_b > end_a + 1 or start_a > end_b + 1:
            return False
    return True


def merge_overlapping_groups(raw_groups: list[dict[str, Any]], window: int) -> list[dict[str, Any]]:
    """Union window groups that describe the same maximal duplicated region."""
    # Bucket by the set of files involved; only same-signature groups can be the same region.
    buckets: dict[frozenset[str], list[int]] = defaultdict(list)
    for index, group in enumerate(raw_groups):
        signature = frozenset(loc[0] for loc in group["locations"])
        buckets[signature].append(index)

    parent = list(range(len(raw_groups)))

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(a: int, b: int) -> None:
        root_a, root_b = find(a), find(b)
        if root_a != root_b:
            parent[root_b] = root_a

    for members in buckets.values():
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                if _parallel_overlap(raw_groups[members[i]]["locations"], raw_groups[members[j]]["locations"]):
                    union(members[i], members[j])

    clusters: dict[int, list[int]] = defaultdict(list)
    for index in range(len(raw_groups)):
        clusters[find(index)].append(index)

    merged_groups = []
    for members in clusters.values():
        per_path: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for member in members:
            for path, start, end in raw_groups[member]["locations"]:
                per_path[path].append((start, end))
        locations = []
        for path, intervals in per_path.items():
            for start, end in _merge_intervals(intervals):
                locations.append((path, start, end))
        locations.sort()
        merged_groups.append(
            {"locations": locations, "preview": raw_groups[members[0]]["preview"]}
        )
    return merged_groups


def _merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Collapse overlapping/adjacent (start, end) line ranges into maximal spans."""
    ordered = sorted(intervals)
    merged: list[tuple[int, int]] = []
    for start, end in ordered:
        if merged and start <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def build_report(
    root: Path,
    min_score: int,
    duplicate_window: int,
    max_files: int,
    *,
    include_tests: bool = False,
) -> dict[str, Any]:
    metrics = [file_metrics(path, root) for path in iter_source_files(root, include_tests=include_tests)]
    candidates = [
        metric.__dict__
        for metric in sorted(metrics, key=lambda item: item.score, reverse=True)
        if metric.score >= min_score
    ][:max_files]
    duplicates = duplicate_blocks(root, duplicate_window, include_tests=include_tests)[:25]
    return {
        "root": str(root),
        "candidateCount": len(candidates),
        "duplicateGroupCount": len(duplicates),
        "includeTests": include_tests,
        "candidates": candidates,
        "duplicateBlocks": duplicates,
    }


def print_report(report: dict[str, Any]) -> None:
    print(f"Repo: {report['root']}")
    print(f"Likely god-file candidates: {report['candidateCount']}")
    for item in report["candidates"]:
        reasons = ", ".join(item["reasons"]) if item["reasons"] else "heuristic match"
        responsibilities = ", ".join(item["responsibilities"]) or "none"
        print(
            f"- score {item['score']:>3} [{item['category']}] {item['path']}: "
            f"{reasons}; responsibilities: {responsibilities}"
        )

    print(f"\nDuplicate block groups: {report['duplicateGroupCount']}")
    for group in report["duplicateBlocks"][:10]:
        print(
            f"- {group['occurrences']} occurrences across {group['files']} files "
            f"({group['window']}-line window)"
        )
        for match in group["matches"][:4]:
            print(f"  - {match['path']}:{match['start']} preview: {match['preview']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rank likely god components, god scripts, and duplicate JS/TS blocks.",
    )
    parser.add_argument("repo", nargs="?", default=".", help="Repository root to scan")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--min-score", type=int, default=35, help="Minimum candidate score")
    parser.add_argument("--max-files", type=int, default=40, help="Maximum candidates to print")
    parser.add_argument(
        "--include-tests",
        action="store_true",
        help="Include test/spec files in candidate and duplicate scanning",
    )
    parser.add_argument(
        "--duplicate-window",
        type=int,
        default=9,
        help="Normalized line window for exact duplicate block detection",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.repo).expanduser().resolve()
    if not root.exists():
        print(f"Path does not exist: {root}", file=sys.stderr)
        return 2
    report = build_report(
        root,
        args.min_score,
        args.duplicate_window,
        args.max_files,
        include_tests=args.include_tests,
    )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
