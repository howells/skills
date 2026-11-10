#!/usr/bin/env python3
"""Observe repositories without mutation; save complete private JSON outside source."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


READ_COMMANDS = {"rev-parse", "worktree", "status", "for-each-ref", "show-ref", "log", "rev-list", "ls-files"}


class ObservationError(Exception):
    pass


def read_git(path, *args, allowed=(0,)):
    if args[0] not in READ_COMMANDS:
        raise ObservationError("non-observation Git command refused")
    context = {"GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
               "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE", "GIT_PREFIX", "GIT_SHALLOW_FILE", "GIT_GRAFT_FILE"}
    environment = {name: value for name, value in os.environ.items() if name not in context}
    environment.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0"})
    result = subprocess.run(
        ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(path), *args],
        capture_output=True, text=True, errors="surrogateescape", timeout=30,
        env=environment)
    if result.returncode not in allowed:
        raise ObservationError("Git %s observation failed (exit %s)" % (args[0], result.returncode))
    return result


def within(path, parent):
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def outside(output, paths):
    if any(within(output, path.resolve()) for path in paths):
        raise ObservationError("output must be outside requested roots, checkouts and Git metadata")


def stamp(path):
    return path.stat().st_mtime if path.exists() else None


def process_cwds():
    result = subprocess.run(["lsof", "-a", "-d", "cwd", "-Fpcn"],
                            capture_output=True, text=True, errors="surrogateescape", timeout=15)
    if result.returncode:
        raise ObservationError("local process working-directory observation failed")
    records, current = [], {}
    for line in result.stdout.splitlines():
        if line.startswith("p"):
            current = {"pid": line[1:]}
        elif line.startswith("c"):
            current["command"] = line[1:]
        elif line.startswith("n") and line[1:].startswith("/"):
            records.append({**current, "cwd": line[1:]})
    return records


def worktree_entries(repo):
    records, current = [], {}
    for field in read_git(repo, "worktree", "list", "--porcelain", "-z").stdout.split("\0"):
        if not field:
            if current:
                records.append(current)
                current = {}
            continue
        key, _, value = field.partition(" ")
        current[key] = value if value else True
    if current:
        records.append(current)
    return records


def dirty_paths(body):
    parts, records, index = body.split("\0"), [], 0
    while index < len(parts):
        part = parts[index]
        index += 1
        if not part:
            continue
        record = {"status": part[:2], "path": part[3:]}
        if "R" in part[:2] or "C" in part[:2]:
            record["originalPath"] = parts[index]
            index += 1
        records.append(record)
    return records


def lock_paths(common, git_dirs):
    paths = set()
    for directory in set([common, *git_dirs]):
        paths.update(directory.glob("*.lock"))
        for name in ["locked", "MERGE_HEAD", "CHERRY_PICK_HEAD", "REBASE_HEAD", "rebase-merge", "rebase-apply"]:
            candidate = directory / name
            if candidate.exists():
                paths.add(candidate)
        refs = directory / "refs"
        if refs.is_dir():
            paths.update(refs.rglob("*.lock"))
    return [{"path": str(path), "mtime": stamp(path)} for path in sorted(paths)]


class Census:
    def __init__(self, output, exclusions):
        self.output = output
        self.exclusions = exclusions
        self.repositories = {}
        self.errors = []
        self.excluded = []
        self.visited = set()
        self.processes = []

    def error(self, path, operation, error):
        message = str(error) if isinstance(error, ObservationError) else "filesystem or process observation failed"
        self.errors.append({"path": str(path), "operation": operation, "message": message})

    def excluded_path(self, path):
        return any(within(path.resolve(), item) for item in self.exclusions)

    def discover(self, path, requested_root):
        if self.excluded_path(path):
            self.excluded.append({"path": str(path), "requestedRoot": str(requested_root)})
            return True
        try:
            if not path.is_dir() or not os.access(path, os.R_OK | os.X_OK):
                raise ObservationError("requested path is missing or unreadable")
            probe = read_git(path, "rev-parse", "--git-common-dir", allowed=(0, 128))
            if probe.returncode == 0:
                common = (path / probe.stdout.strip()).resolve()
                bare = read_git(path, "rev-parse", "--is-bare-repository").stdout.strip() == "true"
                checkout = None if bare else Path(read_git(path, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
                outside(self.output, [common, *([checkout] if checkout else [])])
                record = self.repositories.setdefault(str(common), {
                    "commonGitDir": str(common), "bare": bare, "entries": [],
                    "worktrees": [], "branches": [], "stashes": [], "reflogOnlyCommits": [], "locks": [],
                })
                record["entries"].append({"path": str(path), "resolvedPath": str(path.resolve()),
                                           "checkout": str(checkout) if checkout else None,
                                           "requestedRoot": str(requested_root)})
                return True
            visit = (path.resolve(), str(requested_root))
            if visit in self.visited:
                return False
            self.visited.add(visit)
            found = False
            for child in sorted(path.iterdir()):
                if child.is_dir():
                    found = self.discover(child, requested_root) or found
            return found
        except (ObservationError, OSError, subprocess.TimeoutExpired) as error:
            if isinstance(error, ObservationError) and str(error).startswith("output must"):
                raise
            self.error(path, "repository discovery", error)
            return False

    def checkout(self, registered):
        path = Path(registered["worktree"])
        record = {"path": str(path), "head": registered.get("HEAD"), "branch": registered.get("branch"),
                  "detached": bool(registered.get("detached")), "registration": registered,
                  "dirty": [], "ignoredPaths": [],
                  "excluded": self.excluded_path(path), "processes": [], "activity": {}}
        outside(self.output, [path])
        if record["excluded"]:
            if not any(item["path"] == str(path) for item in self.excluded):
                self.excluded.append({"path": str(path), "registration": "worktree"})
            return record, None
        try:
            if not path.is_dir() or not os.access(path, os.R_OK | os.X_OK):
                raise ObservationError("registered worktree is missing or unreadable")
            git_dir = Path(read_git(path, "rev-parse", "--absolute-git-dir").stdout.strip()).resolve()
            outside(self.output, [git_dir])
            record["gitDir"] = str(git_dir)
            record["dirty"] = dirty_paths(read_git(path, "status", "--porcelain=v1", "-z", "--untracked-files=all").stdout)
            record["ignoredPaths"] = [item for item in read_git(path, "ls-files", "--others", "--ignored",
                                                                  "--exclude-standard", "--directory", "-z").stdout.split("\0") if item]
            record["processes"] = [item for item in self.processes if within(Path(item["cwd"]).resolve(), path.resolve())]
            record["activity"] = {"directoryMtime": stamp(path), "indexMtime": stamp(git_dir / "index"),
                                  "headMtime": stamp(git_dir / "HEAD")}
            record["activity"]["recentWithin24Hours"] = any(
                value is not None and time.time() - value < 86400 for value in record["activity"].values())
            return record, git_dir
        except (ObservationError, OSError, subprocess.TimeoutExpired) as error:
            if isinstance(error, ObservationError) and str(error).startswith("output must"):
                raise
            self.error(path, "worktree observation", error)
            record["incomplete"] = True
            return record, None

    def observe(self, record):
        path = Path(record["entries"][0]["path"])
        common = Path(record["commonGitDir"])
        try:
            registered = [] if record["bare"] else worktree_entries(path)
            git_dirs, heads = [], []
            for entry in registered:
                checkout, git_dir = self.checkout(entry)
                record["worktrees"].append(checkout)
                if git_dir:
                    git_dirs.append(git_dir)
                head = checkout["head"]
                if head and set(head) != {"0"}:
                    heads.append(head)
            body = read_git(path, "for-each-ref", "--format=%(refname)%00%(objectname)%00%(upstream)%00%(upstream:track)%00%(committerdate:unix)",
                            "refs/heads", "refs/remotes").stdout
            for line in body.splitlines():
                ref, sha, upstream, tracking, timestamp = line.split("\0")
                record["branches"].append({"ref": ref, "sha": sha, "upstream": upstream or None,
                                            "tracking": tracking, "commitTime": int(timestamp) if timestamp else None})
            if read_git(path, "show-ref", "--verify", "--quiet", "refs/stash", allowed=(0, 1)).returncode == 0:
                for line in read_git(path, "log", "-g", "--format=%H%x00%gd%x00%ct%x00%gs", "refs/stash").stdout.splitlines():
                    sha, ref, timestamp, subject = line.split("\0", 3)
                    origin = re.match(r"(?:WIP on|On) ([^ :]+):", subject)
                    record["stashes"].append({"sha": sha, "ref": ref, "createdAt": int(timestamp),
                                               "originBranch": origin.group(1) if origin else None})
            record["reflogOnlyCommits"] = read_git(path, "rev-list", "--reflog", "--all", "--not", "--all", *heads).stdout.splitlines()
            record["locks"] = lock_paths(common, git_dirs)
        except (ObservationError, OSError, ValueError, subprocess.TimeoutExpired) as error:
            if isinstance(error, ObservationError) and str(error).startswith("output must"):
                raise
            self.error(path, "repository observation", error)
            record["incomplete"] = True


def save_private(path, data):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w") as stream:
            json.dump(data, stream, sort_keys=True, ensure_ascii=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        path.unlink()
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", help="repository paths or containers to discover recursively")
    parser.add_argument("--output", required=True, help="new private JSON file outside every requested root")
    parser.add_argument("--exclude", action="append", default=[], help="explicit protected path excluded from inspection")
    args = parser.parse_args()
    roots = [Path(item).expanduser().absolute() for item in args.roots]
    output = Path(args.output).expanduser().resolve()
    try:
        outside(output, roots)
        census = Census(output, [Path(item).expanduser().resolve() for item in args.exclude])
        process_complete = True
        try:
            census.processes = process_cwds()
        except (ObservationError, OSError, subprocess.TimeoutExpired) as error:
            process_complete = False
            census.error("local host", "process observation", error)
        observed, outcomes = [], {}
        for root in roots:
            outcome = outcomes.get(str(root))
            if outcome is None:
                outcome = census.discover(root, root)
                outcomes[str(root)] = outcome
            if outcome:
                observed.append(str(root))
            elif not any(item["path"] == str(root) for item in census.errors):
                census.error(root, "repository discovery", ObservationError("no repositories found under requested root"))
        for record in census.repositories.values():
            census.observe(record)
        data = {"format": "howells-repository-census", "version": 1,
                "generatedAt": datetime.now(timezone.utc).isoformat(),
                "coverage": {"complete": not census.errors, "requestedRoots": [str(path) for path in roots],
                             "observedRoots": observed, "errors": census.errors, "exclusions": census.excluded},
                "processEvidence": {"complete": process_complete,
                                    "scope": "local OS working directories only; remote hosts and session custody are not observed"},
                "repositories": sorted(census.repositories.values(), key=lambda record: record["commonGitDir"])}
        save_private(output, data)
        state = "complete" if data["coverage"]["complete"] else "incomplete"
        worktrees = sum(len(record["worktrees"]) for record in data["repositories"])
        print("Census %s: %s repositories, %s registered worktrees, %s exclusions." %
              (state, len(data["repositories"]), worktrees, len(census.excluded)))
        print(("Private JSON: " + str(output).replace("\n", "\\n"))[:200])
        print("Coverage: %s/%s roots observed; %s observation errors. No mutation or custody clearance." %
              (len(observed), len(roots), len(census.errors)))
        return 0 if data["coverage"]["complete"] else 2
    except (ObservationError, OSError, subprocess.TimeoutExpired):
        print("Census failed: output must be new, writable, private and outside observed source/Git directories.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
