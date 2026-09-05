#!/usr/bin/env python3
"""Read one 1Password credential with a bounded, non-interactive bootstrap."""
import subprocess
import sys

try:
    result = subprocess.run(["op", "read", sys.argv[1]], stdin=subprocess.DEVNULL, capture_output=True, timeout=30)
except subprocess.TimeoutExpired:
    print("Credential bootstrap exceeded 30 seconds; no interactive authentication attempted.", file=sys.stderr)
    raise SystemExit(124)
except FileNotFoundError:
    print("Credential bootstrap requires the op CLI.", file=sys.stderr)
    raise SystemExit(127)
if result.returncode or not result.stdout.strip():
    print("Credential bootstrap failed or returned an empty value; check configured non-interactive access.", file=sys.stderr)
    raise SystemExit(result.returncode or 1)
sys.stdout.buffer.write(result.stdout)
