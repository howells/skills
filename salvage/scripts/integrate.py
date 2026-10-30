#!/usr/bin/env python3
"""Publish an explicit commit through a verified Git destination."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


class PublicationError(Exception):
    pass


def git(repo, *args, allow_failure=False):
    context = {"GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
               "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE", "GIT_PREFIX", "GIT_SHALLOW_FILE", "GIT_GRAFT_FILE"}
    environment = {name: value for name, value in os.environ.items() if name not in context}
    environment["GIT_TERMINAL_PROMPT"] = "0"
    result = subprocess.run(
        ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(repo), *args],
        capture_output=True, text=True, timeout=60,
        env=environment)
    if result.returncode and not allow_failure:
        # Git/provider output can contain credential-bearing URLs or hook logs.
        raise PublicationError("Git %s failed (exit %s)" % (args[0], result.returncode))
    return result


def transport(repo, remote):
    if remote not in git(repo, "remote").stdout.splitlines() or remote.startswith("-"):
        raise PublicationError("remote must name an existing configured remote")
    fetch = git(repo, "remote", "get-url", "--all", remote).stdout.splitlines()
    push = git(repo, "remote", "get-url", "--push", "--all", remote).stdout.splitlines()
    if len(fetch) != 1 or fetch != push:
        raise PublicationError("remote must have one identical fetch and push transport")
    return hashlib.sha256(fetch[0].encode()).hexdigest()


def advertised_ref(repo, remote, ref):
    lines = git(repo, "ls-remote", "--refs", remote, ref).stdout.splitlines()
    if not lines:
        return None
    pairs = [line.split("\t") for line in lines]
    if len(pairs) != 1 or len(pairs[0]) != 2 or pairs[0][1] != ref:
        raise PublicationError("ambiguous remote ref advertisement")
    sha = pairs[0][0]
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", sha):
        raise PublicationError("invalid remote tip advertisement")
    return sha


def server_default(repo, remote):
    lines = git(repo, "ls-remote", "--symref", remote, "HEAD").stdout.splitlines()
    symbols, tips = [], []
    for line in lines:
        parts = line.split("\t")
        if len(parts) != 2 or parts[1] != "HEAD":
            raise PublicationError("inconsistent server-default advertisement")
        if parts[0].startswith("ref: "):
            symbols.append(parts[0][5:])
        else:
            tips.append(parts[0])
    if not symbols:
        if not tips or (len(tips) == 1 and re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", tips[0])):
            return None
        raise PublicationError("server default is unknown or ambiguous")
    if len(symbols) != 1 or len(tips) != 1:
        raise PublicationError("server default is unknown or ambiguous")
    ref = symbols[0]
    if not ref.startswith("refs/heads/") or git(repo, "check-ref-format", ref, allow_failure=True).returncode:
        raise PublicationError("server default is not a valid branch ref")
    if advertised_ref(repo, remote, ref) != tips[0]:
        raise PublicationError("server default and branch tip are inconsistent")
    return ref, tips[0]


def publish(args):
    repo = Path(args.repo).resolve(strict=True)
    remote = args.remote
    identity = transport(repo, remote)
    head = git(repo, "rev-parse", "--verify", "HEAD").stdout.strip()
    commit = git(repo, "rev-parse", "--verify", "--end-of-options", args.commit + "^{commit}").stdout.strip()
    default = server_default(repo, remote)
    if args.intent == "integrate":
        if args.destination_ref:
            raise PublicationError("integration destination comes only from the server default")
        if default is None:
            raise PublicationError("server default is unknown; no destination was selected")
        destination, old = default
    else:
        destination = args.destination_ref or ""
        if not destination.startswith(("refs/heads/", "refs/salvage/")):
            raise PublicationError("preservation requires an explicit feature or salvage ref")
        if git(repo, "check-ref-format", destination, allow_failure=True).returncode:
            raise PublicationError("invalid preservation destination ref")
        if default and destination == default[0]:
            raise PublicationError("preservation cannot target the server default branch")
        if default is None and not destination.startswith("refs/salvage/"):
            raise PublicationError("unknown default permits only explicit refs/salvage preservation")
        old = advertised_ref(repo, remote, destination)
    expected = None if args.expected_old == "absent" else args.expected_old
    if expected is not None and not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", expected):
        raise PublicationError("expected old tip must be an exact SHA or 'absent'")
    if old != expected:
        raise PublicationError("remote tip differs from the expected old tip")
    if old:
        git(repo, "fetch", "--no-prune", "--no-prune-tags", "--no-tags",
            "--recurse-submodules=no", remote, destination)
        fetched = git(repo, "rev-parse", "--verify", "FETCH_HEAD^{commit}").stdout.strip()
        if fetched != old:
            raise PublicationError("remote tip changed during fetch")
        ancestry = git(repo, "merge-base", "--is-ancestor", old, commit, allow_failure=True)
        if ancestry.returncode:
            raise PublicationError("candidate is not a fast-forward of the verified remote tip")
    if transport(repo, remote) != identity:
        raise PublicationError("configured remote transport changed")
    if server_default(repo, remote) != default or advertised_ref(repo, remote, destination) != old:
        raise PublicationError("remote default or tip changed before push")
    pushed = git(repo, "push", "--porcelain", "--no-follow-tags", "--recurse-submodules=no", remote,
                 commit + ":" + destination, allow_failure=True)
    if pushed.returncode:
        raise PublicationError("push rejected by ordinary hooks or remote safety (exit %s)" % pushed.returncode)
    if transport(repo, remote) != identity:
        raise PublicationError("configured remote transport changed; publication is not verified")
    actual = advertised_ref(repo, remote, destination)
    current_default = server_default(repo, remote)
    default_ref_changed = (current_default[0] if current_default else None) != (default[0] if default else None)
    if actual != commit or default_ref_changed or (args.intent == "integrate" and current_default != (destination, commit)):
        raise PublicationError("remote changed around push; publication is not verified")
    return {
        "format": "howells-git-publication", "version": 1,
        "intent": args.intent, "remote": remote, "transportSha256": identity,
        "destinationRef": destination, "oldSha": old, "sha": actual,
        "pushedIsHead": commit == head,
        "sourceVerification": "not performed by this helper; installed hooks retain their own scope",
        "custodyAndReleaseApproval": "not inferred",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--remote", required=True)
    parser.add_argument("--intent", choices=["integrate", "preserve"], required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--expected-old", required=True, help="exact observed remote SHA, or absent for a new preservation ref")
    parser.add_argument("--destination-ref", help="explicit feature/salvage ref; preservation only")
    args = parser.parse_args()
    try:
        print(json.dumps(publish(args), sort_keys=True))
    except (PublicationError, OSError, subprocess.TimeoutExpired) as error:
        message = str(error) if isinstance(error, PublicationError) else "operational command could not complete"
        print("Publication failed: " + message, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
