#!/usr/bin/env python3
"""Read one credential for an internal request pipe.

The environment wins. Otherwise the value comes from `.env` at the root of the
repository containing the working directory (the working directory itself when
it isn't in a repository). The value is written to stdout only, never echoed
in a diagnostic.
"""
import os
from pathlib import Path
import re
import subprocess
import sys

NAME = re.compile(r"[A-Z][A-Z0-9_]*")


def repository_root():
    try:
        result = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return Path.cwd()
    return Path(result.stdout.strip()) if result.returncode == 0 else Path.cwd()


def from_env_file(name):
    path = repository_root() / ".env"
    if not path.is_file():
        return ""
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        key, separator, value = line.partition("=")
        if not separator or key.strip() != name:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            return value[1:-1]
        return value.split(" #", 1)[0].rstrip()
    return ""


if len(sys.argv) != 2 or not NAME.fullmatch(sys.argv[1]):
    print("Usage: read-credential.py ENVIRONMENT_VARIABLE", file=sys.stderr)
    raise SystemExit(64)
name = sys.argv[1]
value = os.environ.get(name, "") or from_env_file(name)
if not value.strip() or any(ord(char) < 32 or ord(char) == 127 for char in value):
    print(f"{name} is missing or invalid in the environment and in the repository's root .env; "
          "set a nonempty, single-line value.", file=sys.stderr)
    raise SystemExit(78)
sys.stdout.write(value)
