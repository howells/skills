#!/usr/bin/env python3
"""Preserve the GraphQL body while rejecting failed or partial responses."""
import json
import sys

body = sys.stdin.read()
sys.stdout.write(body)
try:
    response = json.loads(body)
except json.JSONDecodeError:
    print("Invalid GraphQL JSON response.", file=sys.stderr)
    raise SystemExit(1)
if not isinstance(response, dict) or response.get("errors") or not isinstance(response.get("data"), dict):
    print("GraphQL failed or returned partial/invalid data; inspect the response before continuing.", file=sys.stderr)
    raise SystemExit(1)
if any(isinstance(value, dict) and value.get("success") is False for value in response["data"].values()):
    print("GraphQL mutation reported success=false.", file=sys.stderr)
    raise SystemExit(1)
