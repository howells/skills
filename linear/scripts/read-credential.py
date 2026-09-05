#!/usr/bin/env python3
"""Read one injected environment credential for an internal request pipe."""
import os
import re
import sys

if len(sys.argv) != 2 or not re.fullmatch(r"[A-Z][A-Z0-9_]*", sys.argv[1]):
    print("Usage: read-credential.py ENVIRONMENT_VARIABLE", file=sys.stderr)
    raise SystemExit(64)
value = os.environ.get(sys.argv[1], "")
if not value.strip() or any(ord(char) < 32 or ord(char) == 127 for char in value):
    print("Required credential is missing or invalid; inject a nonempty, single-line value.", file=sys.stderr)
    raise SystemExit(78)
sys.stdout.write(value)
