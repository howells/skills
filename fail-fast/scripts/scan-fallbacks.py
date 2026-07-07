#!/usr/bin/env python3
"""Scan source trees for hidden fallbacks and compatibility paths."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_EXCLUDES = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".nuxt",
    ".turbo",
    ".vercel",
    "coverage",
    "dist",
    "build",
    "out",
    "node_modules",
    "vendor",
    "__pycache__",
}

DEFAULT_EXCLUDED_FILENAMES = {
    "bun.lock",
    "bun.lockb",
    "Cargo.lock",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
}

# Declarative manifests: dependency names and fields like "deprecated" trip the
# legacy-keyword rule as noise. They are still scanned for other rules.
MANIFEST_FILENAMES = {
    "package.json",
    "tsconfig.json",
    "composer.json",
    "composer.lock",
    "Gemfile.lock",
}

TEXT_EXTENSIONS = {
    ".cjs",
    ".css",
    ".cts",
    ".go",
    ".java",
    ".js",
    ".jsx",
    ".json",
    ".md",
    ".mdx",
    ".mjs",
    ".mts",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".yaml",
    ".yml",
}


@dataclass(frozen=True)
class Finding:
    file: str
    line: int
    category: str
    severity: str
    rule: str
    match: str
    guidance: str


@dataclass(frozen=True)
class Rule:
    name: str
    category: str
    severity: str
    pattern: re.Pattern[str]
    guidance: str


RULES = [
    Rule(
        "env-default",
        "environment",
        "high",
        re.compile(r"\bprocess\.env\.[A-Z0-9_]+\s*(?:\|\||\?\?)\s*[^;\n]+"),
        "Use an Envy schema and typed env module; do not add app-level fallbacks for potentially missing env vars.",
    ),
    Rule(
        "direct-env-read",
        "environment",
        "medium",
        re.compile(r"\bprocess\.env\.[A-Z0-9_]+\b"),
        "Application code should use the typed env module; allow only env schema wiring and narrow system keys.",
    ),
    Rule(
        "getenv-default",
        "environment",
        "high",
        re.compile(r"\b(?:os\.getenv|os\.environ\.get)\([^)\n]+,\s*[^)\n]+\)"),
        "Do not hide required configuration behind getenv defaults; enforce presence through the env contract.",
    ),
    Rule(
        "nullish-fallback",
        "fallback",
        "medium",
        re.compile(r"\?\?\s*(?:['\"`][^'\"`]*['\"`]|\d+|true|false|\[\]|\{\})"),
        "Check whether the fallback should be a required value or explicit validation error.",
    ),
    Rule(
        "or-fallback",
        "fallback",
        "medium",
        re.compile(r"\|\|\s*(?:['\"`][^'\"`]*['\"`]|\d+|true|false|\[\]|\{\})"),
        "Check whether falsy values are being collapsed into hidden defaults.",
    ),
    Rule(
        "legacy-keyword",
        "compatibility",
        "medium",
        re.compile(r"\b(?:backwards?|compat(?:ibility)?|legacy|deprecated|deprecation|migration|old[-_ ]?api)\b", re.I),
        "Keep compatibility only with an owner, removal condition, and tests; otherwise remove it.",
    ),
    Rule(
        "alias-fallback",
        "compatibility",
        "high",
        re.compile(r"\b[A-Za-z_$][\w$]*\s*=\s*[^;\n]*(?:\?\?|\|\|)\s*(?:input|options|opts|config|params|props)\.[A-Za-z_$][\w$]*"),
        "Dual input keys create hidden compatibility states; prefer one canonical key.",
    ),
    Rule(
        "empty-catch",
        "error-handling",
        "high",
        re.compile(r"\bcatch\s*(?:\([^)]*\))?\s*\{\s*\}"),
        "Empty catch blocks hide failure; rethrow with context or handle a specific expected error.",
    ),
    Rule(
        "swallowing-catch",
        "error-handling",
        "high",
        re.compile(r"\bcatch\s*(?:\([^)]*\))?\s*\{[^{}]*(?:return\s+(?:null|undefined|false|true|\[\]|\{\}|['\"`][^'\"`]*['\"`])|pass\b|continue\b)[^{}]*\}", re.S),
        "Catch blocks that return fallback success should be replaced with explicit error handling.",
    ),
    Rule(
        "swallowing-except",
        "error-handling",
        "high",
        re.compile(r"\bexcept\b[^:\n]*:\s*(?:pass|return\s+None|continue)\b"),
        "Python except blocks that swallow the error (pass / return None) hide failure; handle a specific expected error or re-raise with context.",
    ),
    Rule(
        "optional-import",
        "dependency",
        "medium",
        re.compile(r"\btry\s*\{[^{}]*(?:require\(|import\()[^{}]*\}\s*catch", re.S),
        "Optional dependencies should be explicit feature boundaries, not silent degradation.",
    ),
    Rule(
        "todo-compat",
        "compatibility",
        "medium",
        re.compile(r"\b(?:TODO|FIXME|HACK|XXX)\b.*\b(?:fallback|legacy|compat|migration|temporary|remove)\b", re.I),
        "Temporary compatibility notes need an owner and removal condition or should be resolved now.",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root to scan.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.add_argument(
        "--include-tests",
        action="store_true",
        help="Include test/spec/fixture files. They are skipped by default.",
    )
    parser.add_argument(
        "--include-docs",
        action="store_true",
        help="Include Markdown documentation files. They are skipped by default.",
    )
    parser.add_argument(
        "--fail-on",
        choices=["medium", "high"],
        help="Exit non-zero when findings at or above this severity are present.",
    )
    parser.add_argument(
        "--max-file-bytes",
        type=int,
        default=1_000_000,
        help="Skip files larger than this size. Default: 1000000.",
    )
    return parser.parse_args()


def is_test_path(path: Path) -> bool:
    lowered = str(path).lower()
    return any(
        marker in lowered
        for marker in (
            ".test.",
            ".spec.",
            "__tests__",
            "/test/",
            "/tests/",
            "/fixtures/",
            "/fixture/",
            "/mocks/",
            "/mock/",
        )
    )


def iter_files(root: Path, include_tests: bool, include_docs: bool, max_file_bytes: int) -> Iterable[Path]:
    for current_root, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in DEFAULT_EXCLUDES]
        current = Path(current_root)
        for filename in files:
            path = current / filename
            if filename in DEFAULT_EXCLUDED_FILENAMES:
                continue
            if path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            if not include_docs and path.suffix.lower() in {".md", ".mdx"}:
                continue
            if not include_tests and is_test_path(path.relative_to(root)):
                continue
            try:
                if path.stat().st_size > max_file_bytes:
                    continue
            except OSError:
                continue
            yield path


def read_text(path: Path) -> str | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in raw:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace")


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def line_excerpt(text: str, offset: int) -> str:
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    if end == -1:
        end = len(text)
    return text[start:end].strip()


def is_comment_line(excerpt: str) -> bool:
    return excerpt.startswith(("//", "#", "*", "/*", "<!--"))


def scan(root: Path, include_tests: bool, include_docs: bool, max_file_bytes: int) -> list[Finding]:
    findings: list[Finding] = []
    env_default_lines: set[tuple[str, int]] = set()
    for path in iter_files(root, include_tests, include_docs, max_file_bytes):
        text = read_text(path)
        if text is None:
            continue
        rel = str(path.relative_to(root))
        is_manifest = path.name in MANIFEST_FILENAMES
        seen: set[tuple[str, int]] = set()
        for rule in RULES:
            if rule.name == "legacy-keyword" and is_manifest:
                continue
            for match in rule.pattern.finditer(text):
                line = line_number(text, match.start())
                excerpt = line_excerpt(text, match.start())
                if rule.name != "todo-compat" and is_comment_line(excerpt):
                    continue
                key = (rule.name, line)
                if key in seen:
                    continue
                seen.add(key)
                if rule.name == "env-default":
                    env_default_lines.add((rel, line))
                if rule.name == "direct-env-read" and (rel, line) in env_default_lines:
                    continue
                findings.append(
                    Finding(
                        file=rel,
                        line=line,
                        category=rule.category,
                        severity=rule.severity,
                        rule=rule.name,
                        match=excerpt,
                        guidance=rule.guidance,
                    )
                )
    return sorted(findings, key=lambda item: (item.file, item.line, item.rule))


def severity_rank(severity: str) -> int:
    return {"low": 1, "medium": 2, "high": 3}[severity]


def print_text(findings: list[Finding]) -> None:
    if not findings:
        print("No fallback smells found.")
        return

    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding.category] = counts.get(finding.category, 0) + 1

    summary = ", ".join(f"{category}={count}" for category, count in sorted(counts.items()))
    print(f"Found {len(findings)} fallback smell(s): {summary}")
    print()
    for finding in findings:
        print(f"{finding.file}:{finding.line} [{finding.severity}] {finding.category}/{finding.rule}")
        print(f"  {finding.match}")
        print(f"  -> {finding.guidance}")


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"error: root does not exist: {root}", file=sys.stderr)
        return 2

    findings = scan(root, args.include_tests, args.include_docs, args.max_file_bytes)
    if args.json:
        print(json.dumps([asdict(finding) for finding in findings], indent=2))
    else:
        print_text(findings)

    if args.fail_on:
        threshold = severity_rank(args.fail_on)
        if any(severity_rank(finding.severity) >= threshold for finding in findings):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
