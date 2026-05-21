#!/usr/bin/env python3
"""Audit Mastra implementation boundaries, package config, and domain structure."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

IGNORED_DIRS = {
    ".git",
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
}

SOURCE_EXTENSIONS = {
    ".cjs",
    ".cts",
    ".js",
    ".jsx",
    ".mjs",
    ".mts",
    ".ts",
    ".tsx",
    ".vue",
    ".svelte",
    ".mdx",
}

DEPENDENCY_FIELDS = (
    "dependencies",
    "devDependencies",
    "peerDependencies",
    "optionalDependencies",
)

MASTRA_SPECIFIER_RE = re.compile(
    r"""(?x)
    (?:from\s+|import\s*\(\s*|require\s*\(\s*|export\s+[^;]*?\s+from\s+)
    ["'](@mastra(?:/[^"']+)?|mastra)["']
    |
    ^\s*import\s+["'](@mastra(?:/[^"']+)?|mastra)["']
    """,
    re.MULTILINE,
)

MASTRA_CLI_RE = re.compile(
    r"(^|[;&|()\s])"
    r"(?:(?:npx(?:\s+-y)?|npm\s+exec|pnpm\s+(?:exec|dlx)|yarn\s+(?:exec|dlx)|bunx)\s+)?"
    r"mastra(?:\s|$)"
)

STRUCTURE_PATTERNS = (
    "mastra.config.*",
    "mastra.ts",
    "mastra.js",
    "src/mastra/**",
    ".mastra/**",
)

DOMAIN_RULES = {
    "agents": {
        "patterns": (r"\bnew\s+Agent\b",),
        "allowed_prefixes": ("src/agents/",),
    },
    "tools": {
        "patterns": (r"\bcreateTool\b",),
        "allowed_prefixes": ("src/tools/",),
    },
    "workflows": {
        "patterns": (r"\bcreateWorkflow\b", r"\bnew\s+Workflow\b"),
        "allowed_prefixes": ("src/workflows/",),
    },
    "memory": {
        "patterns": (r"\bnew\s+Memory\b",),
        "allowed_prefixes": ("src/memory/",),
    },
    "storage": {
        "patterns": (r"\bnew\s+(PostgresStore|PgVector|LibSQLStore|DuckDBStore)\b",),
        "allowed_prefixes": ("src/storage/",),
    },
    "observability": {
        "patterns": (r"\bnew\s+(LangfuseExporter|OTLPExporter)\b",),
        "allowed_prefixes": ("src/observability/",),
    },
    "mcp": {
        "patterns": (r"\bnew\s+MCPServer\b",),
        "allowed_prefixes": ("src/mcp/",),
    },
    "scorers": {
        "patterns": (r"\bcreateScorer\b", r"\bnew\s+.*Scorer\b"),
        "allowed_prefixes": ("src/scorers/", "src/evals/"),
    },
}

DOMAIN_SUPPORT_PREFIXES = (
    "src/index.",
    "src/mastra/",
    "src/runtime/",
    "src/public/",
)

DOMAIN_FOLDER_PREFIXES = (
    "src/agents/",
    "src/tools/",
    "src/workflows/",
    "src/prompts/",
    "src/memory/",
    "src/storage/",
    "src/runtime/",
    "src/observability/",
    "src/mcp/",
    "src/scorers/",
    "src/evals/",
    "src/mastra/",
    "src/public/",
    "src/editor/",
    "src/processors/",
    "src/lib/",
)


@dataclass(frozen=True)
class Package:
    path: Path
    relative_path: str
    name: str | None
    manifest: dict[str, Any]


@dataclass(frozen=True)
class Finding:
    severity: str
    category: str
    path: str
    detail: str
    package: str


def strip_jsonc(text: str) -> str:
    result: list[str] = []
    in_string = False
    string_quote = ""
    escaped = False
    index = 0
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if in_string:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == string_quote:
                in_string = False
            index += 1
            continue
        if char in {"'", '"'}:
            in_string = True
            string_quote = char
            result.append(char)
            index += 1
            continue
        if char == "/" and next_char == "/":
            while index < len(text) and text[index] not in "\r\n":
                index += 1
            continue
        if char == "/" and next_char == "*":
            index += 2
            while index + 1 < len(text) and not (text[index] == "*" and text[index + 1] == "/"):
                index += 1
            index += 2
            continue
        result.append(char)
        index += 1

    without_comments = "".join(result)
    return re.sub(r",(\s*[}\]])", r"\1", without_comments)


def load_json(path: Path, *, allow_jsonc: bool = False) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        if not allow_jsonc:
            raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
        try:
            data = json.loads(strip_jsonc(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError as jsonc_exc:
            raise SystemExit(f"Invalid JSON/JSONC in {path}: {jsonc_exc}") from jsonc_exc
    if not isinstance(data, dict):
        raise SystemExit(f"Expected JSON object in {path}")
    return data


def normalize_relative(path: Path, root: Path) -> str:
    relative = path.relative_to(root)
    value = relative.as_posix()
    return "." if value == "." else value


def is_mastra_package_name(name: str) -> bool:
    return name == "mastra" or name.startswith("@mastra/")


def package_json_workspace_patterns(root_manifest: dict[str, Any]) -> list[str]:
    workspaces = root_manifest.get("workspaces", [])
    if isinstance(workspaces, list):
        return [item for item in workspaces if isinstance(item, str)]
    if isinstance(workspaces, dict):
        packages = workspaces.get("packages", [])
        if isinstance(packages, list):
            return [item for item in packages if isinstance(item, str)]
    return []


def pnpm_workspace_patterns(root: Path) -> list[str]:
    workspace_file = root / "pnpm-workspace.yaml"
    if not workspace_file.exists():
        return []

    patterns = []
    in_packages = False
    for raw_line in workspace_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith("packages:"):
            in_packages = True
            continue
        if in_packages and line and not line.startswith((" ", "-")):
            break
        if not in_packages:
            continue
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        value = stripped[2:].strip().strip("\"'")
        if value and not value.startswith("!"):
            patterns.append(value)
    return patterns


def workspace_patterns(root: Path, root_manifest: dict[str, Any]) -> list[str]:
    patterns = []
    patterns.extend(package_json_workspace_patterns(root_manifest))
    patterns.extend(pnpm_workspace_patterns(root))
    deduped = []
    seen = set()
    for pattern in patterns:
        if pattern not in seen:
            deduped.append(pattern)
            seen.add(pattern)
    return deduped


def match_workspace_manifests(root: Path, patterns: list[str]) -> list[Path]:
    manifests: set[Path] = set()
    for pattern in patterns:
        for match in root.glob(pattern):
            if match.name in IGNORED_DIRS:
                continue
            package_json = match / "package.json"
            if package_json.exists():
                manifests.add(package_json)
    return sorted(manifests)


def discover_packages(root: Path) -> list[Package]:
    root_manifest_path = root / "package.json"
    if not root_manifest_path.exists():
        raise SystemExit(f"No package.json found at {root}")

    root_manifest = load_json(root_manifest_path)
    manifests = [root_manifest_path]
    manifests.extend(match_workspace_manifests(root, workspace_patterns(root, root_manifest)))

    packages = []
    for manifest_path in manifests:
        manifest = load_json(manifest_path)
        package_path = manifest_path.parent
        name = manifest.get("name")
        packages.append(
            Package(
                path=package_path,
                relative_path=normalize_relative(package_path, root),
                name=name if isinstance(name, str) else None,
                manifest=manifest,
            )
        )
    return packages


def mastra_dependencies(package: Package) -> list[tuple[str, str]]:
    deps: list[tuple[str, str]] = []
    for field in DEPENDENCY_FIELDS:
        section = package.manifest.get(field, {})
        if not isinstance(section, dict):
            continue
        for name in sorted(section):
            if is_mastra_package_name(name):
                deps.append((field, name))
    return deps


def resolve_allowed_package(packages: list[Package], allowed_package: str | None) -> Package | None:
    if allowed_package:
        normalized = allowed_package.rstrip("/")
        for package in packages:
            if package.relative_path == normalized or package.name == normalized:
                return package
        raise SystemExit(f"Allowed package not found by path or name: {allowed_package}")

    candidates = [package for package in packages if mastra_dependencies(package)]
    if len(candidates) == 1:
        return candidates[0]
    return None


def package_for_path(packages: list[Package], path: Path) -> Package | None:
    containing = []
    for package in packages:
        try:
            path.relative_to(package.path)
        except ValueError:
            continue
        containing.append(package)
    if not containing:
        return None
    return max(containing, key=lambda package: len(package.path.parts))


def package_label(package: Package | None) -> str:
    if package is None:
        return "(outside workspaces)"
    if package.name:
        return f"{package.name} ({package.relative_path})"
    return package.relative_path


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def iter_source_files(root: Path) -> list[Path]:
    files = []
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in IGNORED_DIRS]
        current_path = Path(current_root)
        for filename in filenames:
            path = current_path / filename
            if path.suffix in SOURCE_EXTENSIONS:
                files.append(path)
    return sorted(files)


def source_files_for_package(package: Package) -> list[Path]:
    source_root = package.path / "src"
    if not source_root.exists():
        return []
    return [path for path in iter_source_files(source_root)]


def finding(
    severity: str,
    category: str,
    path: Path,
    root: Path,
    detail: str,
    package: Package | None,
) -> Finding:
    return Finding(
        severity=severity,
        category=category,
        path=normalize_relative(path, root),
        detail=detail,
        package=package_label(package),
    )


def scan_import_boundaries(root: Path, packages: list[Package], allowed: Package | None) -> list[Finding]:
    findings = []
    for path in iter_source_files(root):
        if allowed and is_within(path, allowed.path):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        matches = sorted(
            {
                group
                for match in MASTRA_SPECIFIER_RE.finditer(content)
                for group in match.groups()
                if group
            }
        )
        if not matches:
            continue
        package = package_for_path(packages, path)
        for specifier in matches:
            findings.append(
                finding("error", "boundary-import", path, root, f"imports {specifier}", package)
            )
    return findings


def scan_dependency_boundaries(root: Path, packages: list[Package], allowed: Package | None) -> list[Finding]:
    findings = []
    for package in packages:
        if allowed and package.path == allowed.path:
            continue
        for field, name in mastra_dependencies(package):
            findings.append(
                finding(
                    "error",
                    "boundary-dependency",
                    package.path / "package.json",
                    root,
                    f"{field} declares {name}",
                    package,
                )
            )
    return findings


def scan_script_boundaries(root: Path, packages: list[Package], allowed: Package | None) -> list[Finding]:
    findings = []
    for package in packages:
        if allowed and package.path == allowed.path:
            continue
        scripts = package.manifest.get("scripts", {})
        if not isinstance(scripts, dict):
            continue
        for name, command in sorted(scripts.items()):
            if isinstance(command, str) and MASTRA_CLI_RE.search(command):
                findings.append(
                    finding(
                        "error",
                        "boundary-script",
                        package.path / "package.json",
                        root,
                        f"script {name!r} invokes Mastra CLI",
                        package,
                    )
                )
    return findings


def structure_matches(path: Path, package_root: Path) -> bool:
    relative = path.relative_to(package_root).as_posix()
    return any(fnmatch.fnmatch(relative, pattern) for pattern in STRUCTURE_PATTERNS)


def scan_structure_boundaries(root: Path, packages: list[Package], allowed: Package | None) -> list[Finding]:
    findings = []
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in IGNORED_DIRS]
        current_path = Path(current_root)
        package = package_for_path(packages, current_path)
        if package is None:
            continue
        if allowed and package.path == allowed.path:
            continue
        for filename in filenames:
            path = current_path / filename
            if structure_matches(path, package.path):
                findings.append(
                    finding(
                        "error",
                        "boundary-structure",
                        path,
                        root,
                        "Mastra-looking source or config file outside approved package",
                        package,
                    )
                )
    return findings


def scan_allowed_package_config(root: Path, allowed: Package | None) -> list[Finding]:
    if allowed is None:
        return []

    findings = []
    package_json = allowed.path / "package.json"
    if allowed.manifest.get("type") != "module":
        findings.append(
            finding(
                "warning",
                "package-config",
                package_json,
                root,
                'Mastra package should usually set "type": "module"',
                allowed,
            )
        )

    scripts = allowed.manifest.get("scripts", {})
    has_mastra_script = isinstance(scripts, dict) and any(
        isinstance(command, str) and MASTRA_CLI_RE.search(command) for command in scripts.values()
    )
    if not has_mastra_script:
        findings.append(
            finding(
                "warning",
                "package-config",
                package_json,
                root,
                "no package script invokes Mastra CLI for Studio/build/runtime inspection",
                allowed,
            )
        )

    tsconfig_path = allowed.path / "tsconfig.json"
    if not tsconfig_path.exists():
        findings.append(
            finding("error", "typescript-config", package_json, root, "missing tsconfig.json", allowed)
        )
        return findings

    tsconfig = load_json(tsconfig_path, allow_jsonc=True)
    compiler_options = tsconfig.get("compilerOptions", {})
    if not isinstance(compiler_options, dict):
        compiler_options = {}
    extends = tsconfig.get("extends")
    target = compiler_options.get("target")
    module = compiler_options.get("module")
    module_resolution = compiler_options.get("moduleResolution")

    if target and str(target).upper() not in {"ES2022", "ES2023", "ES2024", "ESNEXT"}:
        findings.append(
            finding(
                "error",
                "typescript-config",
                tsconfig_path,
                root,
                f"compilerOptions.target is {target!r}; Mastra expects ES2022 or newer",
                allowed,
            )
        )
    if module and str(module).upper() not in {"ES2022", "ES2023", "ES2024", "ESNEXT", "PRESERVE"}:
        findings.append(
            finding(
                "error",
                "typescript-config",
                tsconfig_path,
                root,
                f"compilerOptions.module is {module!r}; Mastra expects ES2022-style modules",
                allowed,
            )
        )
    if module_resolution and module_resolution != "bundler":
        findings.append(
            finding(
                "error",
                "typescript-config",
                tsconfig_path,
                root,
                f"compilerOptions.moduleResolution is {module_resolution!r}; Mastra expects bundler",
                allowed,
            )
        )
    if not target and not extends:
        findings.append(
            finding(
                "warning",
                "typescript-config",
                tsconfig_path,
                root,
                "compilerOptions.target is not set directly and no shared config is extended",
                allowed,
            )
        )
    if not module and not extends:
        findings.append(
            finding(
                "warning",
                "typescript-config",
                tsconfig_path,
                root,
                "compilerOptions.module is not set directly and no shared config is extended",
                allowed,
            )
        )
    return findings


def relative_to_package(path: Path, package: Package) -> str:
    return path.relative_to(package.path).as_posix()


def has_prefix(value: str, prefixes: tuple[str, ...]) -> bool:
    return any(value.startswith(prefix) for prefix in prefixes)


def scan_domain_structure(root: Path, allowed: Package | None) -> list[Finding]:
    if allowed is None:
        return []

    findings = []
    source_root = allowed.path / "src"
    if not source_root.exists():
        return [
            finding(
                "error",
                "domain-structure",
                allowed.path,
                root,
                "approved Mastra package has no src/ directory",
                allowed,
            )
        ]

    domain_hits: dict[str, list[Path]] = {domain: [] for domain in DOMAIN_RULES}
    files = source_files_for_package(allowed)
    for path in files:
        if path.name.endswith((".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx")):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = relative_to_package(path, allowed)
        for domain, rule in DOMAIN_RULES.items():
            if any(re.search(pattern, content) for pattern in rule["patterns"]):
                domain_hits[domain].append(path)
                if has_prefix(rel, DOMAIN_SUPPORT_PREFIXES):
                    continue
                if not has_prefix(rel, rule["allowed_prefixes"]):
                    expected = " or ".join(rule["allowed_prefixes"])
                    findings.append(
                        finding(
                            "error",
                            "domain-structure",
                            path,
                            root,
                            f"Mastra {domain} implementation should live under {expected}",
                            allowed,
                        )
                    )

    for domain, paths in domain_hits.items():
        if paths and not (source_root / domain).exists() and domain != "scorers":
            findings.append(
                finding(
                    "error",
                    "domain-structure",
                    source_root,
                    root,
                    f"detected {domain} usage but src/{domain}/ does not exist",
                    allowed,
                )
            )
    if domain_hits["scorers"] and not (source_root / "scorers").exists() and not (source_root / "evals").exists():
        findings.append(
            finding(
                "error",
                "domain-structure",
                source_root,
                root,
                "detected scorer/eval usage but neither src/scorers/ nor src/evals/ exists",
                allowed,
            )
        )

    for path in files:
        rel = relative_to_package(path, allowed)
        if "prompt" not in path.stem.lower():
            continue
        if not has_prefix(rel, ("src/prompts/", "src/agents/prompts/", "src/agents/")):
            findings.append(
                finding(
                    "warning",
                    "prompt-structure",
                    path,
                    root,
                    "prompt-like file is outside src/prompts/, src/agents/prompts/, or src/agents/",
                    allowed,
                )
            )
    return findings


def build_report(root: Path, packages: list[Package], allowed: Package | None) -> dict[str, Any]:
    findings = []
    findings.extend(scan_dependency_boundaries(root, packages, allowed))
    findings.extend(scan_import_boundaries(root, packages, allowed))
    findings.extend(scan_script_boundaries(root, packages, allowed))
    findings.extend(scan_structure_boundaries(root, packages, allowed))
    findings.extend(scan_allowed_package_config(root, allowed))
    findings.extend(scan_domain_structure(root, allowed))

    candidates = [package for package in packages if mastra_dependencies(package)]
    return {
        "root": str(root),
        "allowedPackage": None
        if allowed is None
        else {
            "path": allowed.relative_path,
            "name": allowed.name,
        },
        "candidatePackages": [
            {
                "path": package.relative_path,
                "name": package.name,
                "dependencies": [
                    {"field": field, "name": name}
                    for field, name in mastra_dependencies(package)
                ],
            }
            for package in candidates
        ],
        "findings": [item.__dict__ for item in findings],
    }


def print_text_report(report: dict[str, Any]) -> None:
    print(f"Repo: {report['root']}")
    allowed = report["allowedPackage"]
    if allowed:
        name = f" ({allowed['name']})" if allowed["name"] else ""
        print(f"Approved Mastra package: {allowed['path']}{name}")
    else:
        print("Approved Mastra package: unresolved")

    candidates = report["candidatePackages"]
    if candidates:
        print("\nPackages declaring mastra/@mastra dependencies:")
        for candidate in candidates:
            name = f" ({candidate['name']})" if candidate["name"] else ""
            deps = ", ".join(item["name"] for item in candidate["dependencies"])
            print(f"- {candidate['path']}{name}: {deps}")
    else:
        print("\nPackages declaring mastra/@mastra dependencies: none")

    findings = report["findings"]
    if not findings:
        print("\nNo deterministic Mastra audit findings.")
        print("Manual API review against $mastra docs is still required.")
        return

    print(f"\nDeterministic Mastra audit findings: {len(findings)}")
    for item in findings:
        print(
            f"- [{item['severity']}:{item['category']}] {item['path']} "
            f"({item['package']}): {item['detail']}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit Mastra boundaries, package config, and domain structure.",
    )
    parser.add_argument("repo", nargs="?", default=".", help="Repository root to audit")
    parser.add_argument(
        "--allowed-package",
        help="Approved workspace package path or package.json name",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero for warnings as well as errors",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.repo).expanduser().resolve()
    packages = discover_packages(root)
    allowed = resolve_allowed_package(packages, args.allowed_package)
    report = build_report(root, packages, allowed)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_text_report(report)

    if allowed is None:
        print(
            "\nUnable to resolve exactly one approved Mastra package. "
            "Rerun with --allowed-package <workspace-path-or-name>."
        )
        return 2

    findings = report["findings"]
    has_errors = any(item["severity"] == "error" for item in findings)
    has_warnings = any(item["severity"] == "warning" for item in findings)
    if has_errors or (args.strict and has_warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
