#!/usr/bin/env python3
"""Census the inline typography in a codebase before designing a case.

Reads every class attribute in the given roots, keeps only the tokens that
define text SHAPE (size, weight, family, tracking, leading, case), and reports:

  * how many distinct combinations exist, and how often each is used
  * the size soup: every distinct font size, with its usage count
  * combinations that share a size (candidates to collapse into one role)
  * any `type-*` style classes already in use
  * sanctioned modifiers, counted apart from violations

Colour, alignment, wrapping and truncation are not shape and are ignored.

    python3 scripts/census-typography.py /path/to/repo
    python3 scripts/census-typography.py /path/to/repo --roots apps/web/app apps/web/components
    python3 scripts/census-typography.py /path/to/repo --prefix type- --top 40
    python3 scripts/census-typography.py /path/to/repo --sanctioned font-medium font-mono
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

EXTENSIONS = {".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte", ".astro", ".html", ".css"}

# Where the house style is `@apply`, the typography lives in the stylesheet
# rather than in a class attribute, and the same tokens appear there.
APPLY = re.compile(r"@apply\s+(?P<classes>[^;{}]+);")

# Every dot-directory is tooling or build output (.next, .turbo, .mastra, .vercel,
# .svelte-kit), so they are skipped wholesale rather than named one at a time.
SKIP_DIRS = {
    "node_modules",
    "dist",
    "build",
    "out",
    "coverage",
    "vendor",
    "__pycache__",
    "storybook-static",
}

# A bundle is one enormous line. Real source wraps.
MAX_LINE = 2000

# class="..." / className="..." / fooClassName={cn("...", "...")} - every quoted
# run inside a class-bearing attribute or a cn()/clsx() call.
CLASS_ATTR = re.compile(
    r"""(?:class|[A-Za-z]*[Cc]lass[Nn]ame)\s*[=:]\s*(?P<body>\{(?:[^{}]|\{[^{}]*\})*\}|"[^"]*"|'[^']*'|`[^`]*`)""",
    re.VERBOSE,
)
# A class-utility call standing on its own, outside any class attribute. A `cva`
# defining a variant table is the common shape, and a census that reads only
# attributes reports a file full of type utilities as clean.
CLASS_FN = re.compile(
    r"\b(?:cn|cx|clsx|cva|tv|twMerge|twJoin|classNames)\s*\((?P<args>(?:[^()]|\([^()]*\))*)",
)
QUOTED = re.compile(r"""(["'`])(?P<text>(?:(?!\1).)*)\1""", re.DOTALL)

SIZE_NAMED = re.compile(r"^text-(xs|sm|base|lg|xl|[2-9]xl)$")
SIZE_ARBITRARY = re.compile(
    r"^text-\[(?!#|var\(|rgb|hsl|okl(?:ch|ab)|color[-:(]|currentColor)[^\]]+\]$"
)
# v4's CSS-variable shorthand, `text-(length:--my-size)`, is always a size.
SIZE_SHORTHAND = re.compile(r"^text-\(length:--[\w-]+\)$")
WEIGHT = re.compile(r"^font-(thin|extralight|light|normal|medium|semibold|bold|extrabold|black|\[\d+\])$")
# An arbitrary family or weight is still the role's business: `font-[Inter]`.
FAMILY = re.compile(r"^font-(sans|serif|mono|display|\[[^\]]+\])$")
TRACKING = re.compile(r"^tracking-[\w.\[\]-]+$")
LEADING = re.compile(r"^leading-[\w.\[\]-]+$")
CASE = re.compile(r"^(uppercase|lowercase|capitalize)$")

# Rough px equivalents so the size soup sorts and groups sensibly.
NAMED_PX = {
    "text-xs": 12.0,
    "text-sm": 14.0,
    "text-base": 16.0,
    "text-lg": 18.0,
    "text-xl": 20.0,
    "text-2xl": 24.0,
    "text-3xl": 30.0,
    "text-4xl": 36.0,
    "text-5xl": 48.0,
    "text-6xl": 60.0,
    "text-7xl": 72.0,
    "text-8xl": 96.0,
    "text-9xl": 128.0,
}
ARBITRARY_VALUE = re.compile(r"^text-\[(-?[\d.]+)(rem|px|em|pt)\]$")


def is_shape(token: str) -> bool:
    return bool(
        SIZE_NAMED.match(token)
        or SIZE_ARBITRARY.match(token)
        or SIZE_SHORTHAND.match(token)
        or WEIGHT.match(token)
        or FAMILY.match(token)
        or TRACKING.match(token)
        or LEADING.match(token)
        or CASE.match(token)
    )


def is_size(token: str) -> bool:
    return bool(SIZE_NAMED.match(token) or SIZE_ARBITRARY.match(token) or SIZE_SHORTHAND.match(token))


def size_px(token: str) -> float | None:
    """Approximate px for sorting. Unresolvable sizes (clamp, calc, var) return None."""
    if token in NAMED_PX:
        return NAMED_PX[token]
    match = ARBITRARY_VALUE.match(token)
    if not match:
        return None
    value, unit = float(match.group(1)), match.group(2)
    return {"px": value, "rem": value * 16, "em": value * 16, "pt": value * 4 / 3}[unit]


def base_utility(token: str) -> str:
    """Normalise a Tailwind token to its bare utility.

    Depth counts brackets and parentheses alike, so neither a `:` nor a `/`
    inside them splits: `data-[state=open]:text-lg`, `text-[calc(1rem/2)]` and
    v4's CSS-variable shorthand `text-(length:--my-size)` all survive whole.

    The important marker is stripped in all three positions Tailwind allows -
    v3's `!text-xl` and `hover:!text-xl`, and v4's `text-xl!` - and so is the
    modifier a size carries for its leading (`text-sm/6`).
    """
    token = token[:-1] if token.endswith("!") else token
    depth = 0
    last_colon = last_slash = -1
    for index, character in enumerate(token):
        if character in "[(":
            depth += 1
        elif character in "])":
            depth -= 1
        elif depth == 0 and character == ":":
            last_colon, last_slash = index, -1
        elif depth == 0 and character == "/":
            last_slash = index
    base = token[last_colon + 1 : None if last_slash == -1 else last_slash]
    return base[1:] if base.startswith("!") else base


# Modifiers that may sit beside a role without becoming a role of their own.
# `font-medium` is emphasis within a role; `font-mono` is a family variant.
DEFAULT_SANCTIONED = ("font-medium", "font-mono", "tabular-nums", "capitalize")

# The case, in the order the roles are proposed. Each entry is a name, a band of
# px the role covers, and what it is for.
ROLE_BANDS = (
    ("type-display", 30.0, float("inf"), "page heroes"),
    ("type-heading", 18.0, 30.0, "section headings"),
    ("type-body", 14.0, 18.0, "names, sentences, running copy"),
    ("type-small", 0.0, 14.0, "metadata, labels, controls"),
)


def propose_case(sizes: Counter[str], mono_uses: int) -> list[tuple[str, str, list[str], int]]:
    """Fold the measured size soup into four roles.

    Returns one entry per role that the codebase actually needs: its name, its
    purpose, the sizes folding into it, and total usages. A band nothing lands
    in is dropped, so a codebase with no hero text gets no display role.
    """
    banded: defaultdict[str, list[tuple[float, str, int]]] = defaultdict(list)
    for token, count in sizes.items():
        px = size_px(token)
        if px is None:
            continue
        for name, low, high, _ in ROLE_BANDS:
            if low <= px < high:
                banded[name].append((px, token, count))
                break

    proposal = []
    for name, _, _, purpose in ROLE_BANDS:
        entries = banded.get(name)
        if not entries:
            continue
        entries.sort(key=lambda e: -e[2])
        members = [f"{token} (×{count})" for _, token, count in entries]
        proposal.append((name, purpose, members, sum(count for _, _, count in entries)))

    if mono_uses:
        proposal.append(
            (
                "type-data",
                "numerics and codes; a family variant of the smallest role, not a new step",
                [f"font-mono (×{mono_uses})"],
                mono_uses,
            )
        )
    return proposal


def plural(count: int, noun: str) -> str:
    """`3 roles`, `1 role`. Every count in the report reads as a sentence."""
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def source_files(root: Path, roots: list[str] | None) -> list[Path]:
    bases = [root / r for r in roots] if roots else [root]
    found: list[Path] = []
    for base in bases:
        if not base.exists():
            print(f"warning: {base} does not exist", file=sys.stderr)
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in EXTENSIONS:
                continue
            relative = path.relative_to(base).parts[:-1]
            if any(part in SKIP_DIRS or part.startswith(".") for part in relative):
                continue
            if path.name.endswith((".min.js", ".min.css", ".bundle.js")):
                continue
            found.append(path)
    return sorted(set(found))


def is_bundle(text: str) -> bool:
    return any(len(line) > MAX_LINE for line in text.splitlines())


def enclosing_selector(text: str, position: int) -> str:
    """The selector of the rule containing `position` - the text after the last brace."""
    opened = text.rfind("{", 0, position)
    if opened == -1:
        return ""
    start = max(text.rfind("{", 0, opened), text.rfind("}", 0, opened), text.rfind(";", 0, opened))
    return text[start + 1 : opened].strip()


def class_lists(text: str, is_stylesheet: bool, prefix: str):
    """Every class list in a file: `@apply` runs in CSS, class attributes elsewhere.

    A rule that defines a role (`.type-body { @apply … }`) is the case itself, so
    its raw utilities are the definition rather than a violation, and are skipped.

    Class-utility calls are read wherever they sit, including a `cva` variant
    table that no class attribute encloses. Each quoted run is keyed by its
    position so a `className={cn("…")}` is counted once rather than twice.
    """
    if is_stylesheet:
        for rule in APPLY.finditer(text):
            if enclosing_selector(text, rule.start()).lstrip(".").startswith(prefix):
                continue
            yield rule.group("classes")
        return

    seen: set[int] = set()
    for attr in CLASS_ATTR.finditer(text):
        body = attr.group("body")
        if body[0] in "\"'`":
            seen.add(attr.start("body") + 1)
            yield body[1:-1]
            continue
        for quoted in QUOTED.finditer(body):
            seen.add(attr.start("body") + quoted.start("text"))
            yield quoted.group("text")

    for call in CLASS_FN.finditer(text):
        for quoted in QUOTED.finditer(call.group("args")):
            position = call.start("args") + quoted.start("text")
            if position in seen:
                continue
            seen.add(position)
            yield quoted.group("text")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo", type=Path)
    parser.add_argument("--roots", nargs="*", help="paths under repo to scan (default: whole repo)")
    parser.add_argument("--prefix", default="type-", help="existing style-class prefix to detect (default: type-)")
    parser.add_argument("--top", type=int, default=25, help="how many combinations to list (default: 25)")
    parser.add_argument(
        "--sanctioned",
        nargs="*",
        default=list(DEFAULT_SANCTIONED),
        help=f"modifiers allowed beside a role (default: {' '.join(DEFAULT_SANCTIONED)})",
    )
    args = parser.parse_args()
    sanctioned = set(args.sanctioned)

    root = args.repo.resolve()
    files = source_files(root, args.roots)
    if not files:
        print("no source files found", file=sys.stderr)
        return 1

    combos: Counter[tuple[str, ...]] = Counter()
    sizes: Counter[str] = Counter()
    existing: Counter[str] = Counter()
    modifiers: Counter[str] = Counter()
    files_with_shape: set[str] = set()

    for path in files:
        try:
            text = path.read_text(encoding="utf8", errors="ignore")
        except OSError:
            continue
        if is_bundle(text):
            continue
        rel = str(path.relative_to(root))
        for class_list in class_lists(text, path.suffix == ".css", args.prefix):
            shape: list[str] = []
            for raw in class_list.split():
                token = base_utility(raw.strip())
                if not token:
                    continue
                if token.startswith(args.prefix):
                    existing[token] += 1
                    continue
                if token in sanctioned:
                    modifiers[token] += 1
                    continue
                if is_shape(token):
                    shape.append(token)
                    if is_size(token):
                        sizes[token] += 1
            if shape:
                key = tuple(sorted(set(shape)))
                combos[key] += 1
                files_with_shape.add(rel)

    usages = sum(combos.values())
    print(f"Scanned {plural(len(files), 'file')} under {root}\n")

    if existing:
        print(f"Existing `{args.prefix}*` classes in use: {len(existing)}")
        for name, count in sorted(existing.items(), key=lambda kv: -kv[1]):
            print(f"  {count:>5}  {name}")
        print()

    if modifiers:
        total = sum(modifiers.values())
        print(f"Sanctioned modifiers, allowed beside a role: {plural(total, 'usage')}")
        for name, count in sorted(modifiers.items(), key=lambda kv: -kv[1]):
            print(f"  {count:>5}  {name}")
        print()

    if not combos:
        print("No inline typography defines shape. The case already holds.")
        return 0

    print(f"Inline typography: {plural(len(combos), 'distinct combination')} "
          f"across {plural(usages, 'usage')} in {plural(len(files_with_shape), 'file')}.\n")

    print(f"Most-used combinations (top {args.top}):")
    for key, count in combos.most_common(args.top):
        print(f"  {count:>5}  {' '.join(key)}")
    if len(combos) > args.top:
        print(f"  ... and {len(combos) - args.top} more")
    print()

    print(f"The size soup: {plural(len(sizes), 'distinct font size')}")
    resolvable = [(size_px(s), s, n) for s, n in sizes.items()]
    resolvable.sort(key=lambda t: (t[0] is None, t[0] or 0))
    for px, token, count in resolvable:
        label = f"~{px:g}px" if px is not None else "unresolved"
        print(f"  {count:>5}  {token:<28} {label}")
    print()

    # Combinations sharing a size are the collapse candidates: they are the same
    # step of the ladder wearing different weights or tracking.
    by_size: defaultdict[float, list[tuple[tuple[str, ...], int]]] = defaultdict(list)
    for key, count in combos.items():
        for token in key:
            if not is_size(token):
                continue
            px = size_px(token)
            if px is not None:
                by_size[px].append((key, count))
            break

    shared = {px: entries for px, entries in by_size.items() if len(entries) > 1}
    if shared:
        print("Collapse candidates - combinations sharing one size:")
        for px in sorted(shared):
            entries = sorted(shared[px], key=lambda e: -e[1])
            total = sum(count for _, count in entries)
            print(f"  ~{px:g}px - {plural(len(entries), 'combination')}, {plural(total, 'usage')}")
            for key, count in entries[:6]:
                print(f"      {count:>5}  {' '.join(key)}")
            if len(entries) > 6:
                print(f"      ... and {len(entries) - 6} more")
        print()

    if not sizes:
        print("No inline sizes to fold. What is left above is weight, family or case,")
        print("each of which belongs to a role rather than becoming one.")
        return 0

    proposal = propose_case(sizes, modifiers.get("font-mono", 0))
    if not proposal:
        print("Every size resolved to a clamp, calc or var. Read them by hand.")
        return 0

    print(f"Proposed case - {plural(len(proposal), 'role')}:")
    for name, purpose, members, count in proposal:
        print(f"  {name:<16} {purpose}")
        print(f"  {'':16} {plural(count, 'usage')} fold in: {', '.join(members[:8])}")
        if len(members) > 8:
            print(f"  {'':16} ... and {plural(len(members) - 8, 'more size')}")
    print()
    print("Measured from this codebase, as a starting point. Read the collapse")
    print("candidates above and set each band's size by hand, dropping any role")
    print("that would carry only the usages it already has.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
