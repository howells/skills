#!/usr/bin/env python3
"""Check Markdown file links, images and ATX heading anchors.

Usage: python3 check-links.py [repo-root]
Supports inline links, angle-bracket destinations and full/collapsed/shortcut
references with single-line definitions. Code spans and fenced code are ignored.
External URLs are skipped. Raw HTML destinations, indented link/code blocks and
unsupported link/definition syntax produce incomplete coverage (exit 2).
Broken supported targets exit 1. Heading slugs are approximated; renderer-specific
explicit IDs and extensions need their own renderer check.
"""
import html
import os
import re
import sys
import unicodedata
from urllib.parse import unquote

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
DEFINITION = re.compile(r"(?m)^ {0,3}\[([^\]\n]+)\]:[ \t]*(.*)$")


def blank(text):
    return re.sub(r"[^\n]", " ", text)


def mask_code(text):
    lines, fence, unsupported = [], None, []
    for lineno, line in enumerate(text.splitlines(keepends=True), 1):
        match = re.match(r"^ {0,3}(\x60{3,}|~{3,})(.*)$", line.rstrip("\n"))
        if fence:
            lines.append(blank(line))
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                fence = None
        elif match:
            fence = match[1]
            lines.append(blank(line))
        elif line.startswith(("    ", "\t")):
            if "[" in line or re.search(r"<(?:a|img)\b", line, re.I):
                unsupported.append((lineno, "indented link/code block needs a renderer-specific check"))
            lines.append(blank(line))
        else:
            lines.append(line)
    text = "".join(lines)
    cursor = 0
    while match := re.search(r"\x60+", text[cursor:]):
        start = cursor + match.start()
        run = match[0]
        closing = re.search(r"(?<!\x60)" + run + r"(?!\x60)", text[start + len(run):])
        if closing is None:
            cursor = start + len(run)
            continue
        end = start + len(run) + closing.end()
        text = text[:start] + blank(text[start:end]) + text[end:]
        cursor = end
    return text, unsupported


def unescape(text):
    return html.unescape(re.sub(r"\\(.)", r"\1", text))


def label_key(text):
    return re.sub(r"\s+", " ", unescape(text)).strip().casefold()


def closing_bracket(text, start):
    depth, pos = 1, start + 1
    while pos < len(text):
        if text[pos] == "\\":
            pos += 2
            continue
        if text[pos] == "[":
            depth += 1
        elif text[pos] == "]":
            depth -= 1
            if depth == 0:
                return pos
        pos += 1
    return None


def destination(text, start):
    pos = start
    if pos < len(text) and text[pos] == "<":
        pos += 1
        begin = pos
        while pos < len(text):
            if text[pos] == "\\":
                pos += 2
                continue
            if text[pos] == ">":
                return unescape(text[begin:pos]), pos + 1
            if text[pos] in "\n<":
                return None
            pos += 1
        return None
    begin, depth = pos, 0
    while pos < len(text):
        char = text[pos]
        if char == "\\":
            pos += 2
            continue
        if char.isspace():
            break
        if char == "(":
            depth += 1
        elif char == ")":
            if depth == 0:
                break
            depth -= 1
        if char == "<":
            return None
        pos += 1
    return (unescape(text[begin:pos]), pos) if depth == 0 else None


def targets_of(text, inherited_references=None):
    text, unsupported = mask_code(text)
    references, targets = dict(inherited_references or {}), []
    if re.search(r"<(?:a|img)\b[^>]*\b(?:href|src)\s*=", text, re.I):
        unsupported.append((1, "raw HTML destinations need a renderer-specific check"))
    definitions = list(DEFINITION.finditer(text))
    for match in definitions:
        parsed = destination(match[2], 0)
        if parsed is None or not parsed[0] or not re.fullmatch(
                r"\s*(?:\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|\([^()\n]*\))?\s*",
                match[2][parsed[1]:] if parsed else ""):
            unsupported.append((text.count("\n", 0, match.start()) + 1,
                                "unsupported reference definition; use a single-line destination"))
        else:
            references.setdefault(label_key(match[1]), parsed[0])
    for match in reversed(definitions):
        text = text[:match.start()] + blank(match[0]) + text[match.end():]
    pos = 0
    while pos < len(text):
        if text[pos] == "\\":
            pos += 2
            continue
        if text[pos] != "[":
            pos += 1
            continue
        end = closing_bracket(text, pos)
        if end is None:
            pos += 1
            continue
        lineno = text.count("\n", 0, pos) + 1
        label, following = text[pos + 1:end], end + 1
        if "[" in label:
            nested, gaps = targets_of(label, references)
            targets.extend((lineno + line - 1, target) for line, target in nested)
            unsupported.extend((lineno + line - 1, reason) for line, reason in gaps)
        if following < len(text) and text[following] == "(":
            start = following + 1
            while start < len(text) and text[start].isspace():
                start += 1
            parsed = destination(text, start)
            tail = re.match(r"\s*(?:\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|\([^()\n]*\))?\s*\)",
                            text[parsed[1]:]) if parsed else None
            if parsed is None or tail is None:
                unsupported.append((lineno, "unsupported inline link syntax"))
                pos = following + 1
                continue
            targets.append((lineno, parsed[0]))
            pos = parsed[1] + tail.end()
        elif following < len(text) and text[following] == "[":
            ref_end = closing_bracket(text, following)
            if ref_end is None:
                unsupported.append((lineno, "unterminated link reference"))
                pos = following + 1
                continue
            key = label_key(text[following + 1:ref_end] or label)
            if key in references:
                targets.append((lineno, references[key]))
            else:
                unsupported.append((lineno, "undefined link reference"))
            pos = ref_end + 1
        else:
            key = label_key(label)
            if key in references:
                targets.append((lineno, references[key]))
            pos = end + 1
    return targets, unsupported


def slugify(text):
    text = re.sub(r"\x60([^\x60]*)\x60", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"\1", text)
    text = text.replace("*", "")
    text = unicodedata.normalize("NFC", text).lower()
    return "".join(ch for ch in text if ch.isalnum() or ch in " _-").replace(" ", "-")


def headings_of(path):
    with open(path, encoding="utf-8") as source:
        # Keep inline heading code: its text contributes to the renderer's slug.
        lines = source.read().splitlines()
    seen, slugs, fence = {}, set(), None
    for line in lines:
        marker = re.match(r"^ {0,3}(\x60{3,}|~{3,})(.*)$", line)
        if marker:
            if fence is None:
                fence = marker[1]
            elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            continue
        match = HEADING.match(line) if fence is None else None
        if match:
            base = slugify(match[2])
            count = seen.get(base, 0)
            seen[base] = count + 1
            slugs.add(base if count == 0 else f"{base}-{count}")
    return slugs


def md_files():
    def traversal_error(error):
        raise error
    for dirpath, dirnames, filenames in os.walk(ROOT, onerror=traversal_error):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        for name in filenames:
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)


def main():
    if not os.path.isdir(ROOT):
        print("Root must be a directory.", file=sys.stderr)
        return 2
    try:
        files = sorted(md_files())
    except OSError as error:
        print(f"Incomplete directory coverage: {error}", file=sys.stderr)
        return 2
    if not files:
        print("No Markdown files checked; no clean verdict.", file=sys.stderr)
        return 2
    anchors, problems, incomplete, checked = {}, [], [], 0
    for path in files:
        rel = os.path.relpath(path, ROOT)
        try:
            with open(path, encoding="utf-8") as source:
                targets, unsupported = targets_of(source.read())
            incomplete.extend(f"{rel}:{line}: {reason}" for line, reason in unsupported)
            for lineno, target in targets:
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("//"):
                    continue
                checked += 1
                file_part, _, anchor = target.partition("#")
                file_part = unquote(file_part.split("?", 1)[0])
                dest = os.path.normpath(os.path.join(os.path.dirname(path), file_part)) if file_part else path
                if not os.path.isfile(dest):
                    problems.append(f"{rel}:{lineno}: missing file: {target}")
                elif anchor and dest.endswith(".md"):
                    if dest not in anchors:
                        anchors[dest] = headings_of(dest)
                    if unquote(anchor).lower() not in anchors[dest]:
                        problems.append(f"{rel}:{lineno}: missing anchor: {target}")
        except (OSError, UnicodeError) as error:
            incomplete.append(f"{rel}: incomplete file coverage: {error}")
    for problem in problems + incomplete:
        print(problem)
    print(f"{len(files)} files, {checked} relative links, {len(problems)} broken, {len(incomplete)} incomplete")
    return 1 if problems else 2 if incomplete else 0


if __name__ == "__main__":
    sys.exit(main())
