#!/usr/bin/env python3
"""Command-boundary fixtures for salvage's census script."""
import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parent.parent / "salvage/scripts"


def git(path, *args, check=True):
    return subprocess.run(["git", "-C", str(path), *args], capture_output=True,
                          text=True, check=check, timeout=10)


class GitFixture(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "source"
        self.remote = self.root / "remote.git"

    def repository(self, branch="main"):
        git(self.root, "init", "-q", "--initial-branch=" + branch, str(self.repo))
        git(self.repo, "config", "user.name", "Fixture")
        git(self.repo, "config", "user.email", "fixture@example.invalid")
        self.commit("base")
        git(self.root, "init", "-q", "--bare", "--initial-branch=" + branch, str(self.remote))
        git(self.repo, "remote", "add", "origin", str(self.remote))
        git(self.repo, "push", "-q", "origin", "HEAD:refs/heads/" + branch)
        return git(self.repo, "rev-parse", "HEAD").stdout.strip()

    def commit(self, text):
        (self.repo / "source.txt").write_text(text)
        git(self.repo, "add", "source.txt")
        git(self.repo, "commit", "-q", "-m", text)
        return git(self.repo, "rev-parse", "HEAD").stdout.strip()

    def command(self, script, *args, env=None):
        return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                              capture_output=True, text=True, timeout=15,
                              env={**os.environ, **(env or {})})


class RepositoryCensus(GitFixture):
    def snapshot(self, *roots):
        return {str(path): (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mode,
                            path.stat().st_mtime_ns)
                for root in roots for path in root.rglob("*") if path.is_file() and not path.is_symlink()}

    def test_private_complete_evidence_covers_dirty_source_without_mutation(self):
        head = self.repository()
        (self.repo / "source.txt").write_text("uncommitted")
        (self.repo / "required.txt").write_text("untracked source")
        before = self.snapshot(self.repo)
        output = self.root / "evidence.json"
        result = self.command("census.py", self.repo, "--output", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(output.read_text())
        self.assertEqual(data["version"], 1)
        self.assertTrue(data["coverage"]["complete"])
        self.assertEqual(len(data["repositories"]), 1)
        checkout = data["repositories"][0]["worktrees"][0]
        self.assertEqual(checkout["head"], head)
        self.assertEqual({item["path"] for item in checkout["dirty"]}, {"source.txt", "required.txt"})
        self.assertEqual(output.stat().st_mode & 0o777, 0o600)
        self.assertLessEqual(len(result.stdout.splitlines()), 12)
        self.assertEqual(self.snapshot(self.repo), before)

    def test_aliases_detached_worktrees_stashes_hidden_history_and_locks_are_preserved(self):
        old = self.repository()
        git(self.repo, "checkout", "-q", "--detach", old)
        hidden = self.commit("historical detached work")
        git(self.repo, "checkout", "-q", "main")
        (self.repo / "source.txt").write_text("stash source")
        git(self.repo, "stash", "push", "-q", "-m", "retained stash")
        stash = git(self.repo, "rev-parse", "refs/stash").stdout.strip()
        linked = self.root / "linked"
        git(self.repo, "worktree", "add", "-q", "--detach", str(linked), old)
        (linked / "detached.txt").write_text("active detached work")
        git(linked, "add", "detached.txt")
        git(linked, "commit", "-q", "-m", "active detached work")
        detached = git(linked, "rev-parse", "HEAD").stdout.strip()
        (self.repo / ".gitignore").write_text("ignored.bin\n")
        (self.repo / "ignored.bin").write_bytes(b"retained ignored data")
        (self.repo / ".git/index.lock").write_text("retained lock")
        alias = self.root / "alias"
        alias.symlink_to(self.repo, target_is_directory=True)
        before = self.snapshot(self.repo, linked)
        output = self.root / "evidence.json"
        result = self.command("census.py", self.repo, alias, "--output", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        repositories = json.loads(output.read_text())["repositories"]
        self.assertEqual(len(repositories), 1)
        repo = repositories[0]
        self.assertEqual({item["path"] for item in repo["entries"]}, {str(self.repo), str(alias)})
        self.assertEqual(len(repo["worktrees"]), 2)
        self.assertTrue(next(item for item in repo["worktrees"] if item["head"] == detached)["detached"])
        self.assertEqual(repo["stashes"][0]["sha"], stash)
        self.assertEqual(repo["stashes"][0]["originBranch"], "main")
        self.assertIn(hidden, repo["reflogOnlyCommits"])
        self.assertNotIn(detached, repo["reflogOnlyCommits"])
        self.assertTrue(any(item["path"].endswith("index.lock") for item in repo["locks"]))
        self.assertIn("ignored.bin", next(item for item in repo["worktrees"] if item["path"] == str(self.repo.resolve()))["ignoredPaths"])
        self.assertEqual(self.snapshot(self.repo, linked), before)

    def test_missing_and_unreadable_requested_roots_are_incomplete_with_bounded_stdout(self):
        self.repository()
        unreadable = self.root / "unreadable"
        unreadable.mkdir()
        unreadable.chmod(0)
        self.addCleanup(unreadable.chmod, 0o700)
        roots = [self.repo, *[self.root / ("missing-%s" % i) for i in range(20)], unreadable]
        output = self.root / "evidence.json"
        result = self.command("census.py", *roots, "--output", output)
        self.assertEqual(result.returncode, 2, result.stderr)
        data = json.loads(output.read_text())
        self.assertFalse(data["coverage"]["complete"])
        self.assertGreaterEqual(len(data["coverage"]["errors"]), 21)
        self.assertLessEqual(len(result.stdout.splitlines()), 3)
        self.assertLessEqual(len(result.stdout), 600)
        self.assertEqual(len(data["repositories"]), 1)

    def test_failed_process_observation_is_not_full_coverage(self):
        self.repository()
        tools = self.root / "tools"
        tools.mkdir()
        lsof = tools / "lsof"
        lsof.write_text("#!/bin/sh\nexit 1\n")
        lsof.chmod(0o700)
        before = self.snapshot(self.repo)
        output = self.root / "evidence.json"
        result = self.command("census.py", self.repo, "--output", output,
                              env={"PATH": str(tools) + os.pathsep + os.environ["PATH"]})
        self.assertEqual(result.returncode, 2, result.stderr)
        data = json.loads(output.read_text())
        self.assertFalse(data["coverage"]["complete"])
        self.assertFalse(data["processEvidence"]["complete"])
        self.assertEqual(self.snapshot(self.repo), before)

    def test_output_cannot_mutate_source_or_common_git_state_or_overwrite_evidence(self):
        old = self.repository()
        linked = self.root / "linked"
        git(self.repo, "worktree", "add", "-q", "--detach", str(linked), old)
        existing = self.root / "existing.json"
        existing.write_text("private existing evidence")
        before = self.snapshot(self.repo, linked)
        for output in [self.repo / "source-evidence.json", self.repo / ".git/evidence.json", existing]:
            result = self.command("census.py", linked, "--output", output)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
        self.assertEqual(existing.read_text(), "private existing evidence")
        self.assertEqual(self.snapshot(self.repo, linked), before)

    def test_empty_repository_and_duplicate_container_roots_are_covered(self):
        git(self.root, "init", "-q", "--initial-branch=main", str(self.repo))
        container = self.root / "projects"
        container.mkdir()
        alias = container / "project"
        alias.symlink_to(self.repo, target_is_directory=True)
        output = self.root / "evidence.json"
        result = self.command("census.py", container, container, "--output", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(output.read_text())
        self.assertTrue(data["coverage"]["complete"])
        self.assertEqual(len(data["repositories"]), 1)
        self.assertEqual(len(data["repositories"][0]["worktrees"]), 1)

    def test_missing_registered_worktree_remains_visible_as_incomplete(self):
        old = self.repository()
        linked = self.root / "linked"
        git(self.repo, "worktree", "add", "-q", "--detach", str(linked), old)
        linked.rename(self.root / "moved-owner-source")
        before = self.snapshot(self.repo)
        output = self.root / "evidence.json"
        result = self.command("census.py", self.repo, "--output", output)
        self.assertEqual(result.returncode, 2, result.stderr)
        data = json.loads(output.read_text())
        missing = next(item for item in data["repositories"][0]["worktrees"] if item["path"] == str(linked.resolve()))
        self.assertTrue(missing["incomplete"])
        self.assertFalse(data["coverage"]["complete"])
        self.assertEqual(self.snapshot(self.repo), before)

    def test_explicit_roots_ignore_inherited_git_directory(self):
        self.repository()
        output = self.root / "evidence.json"
        result = self.command("census.py", self.repo, "--output", output,
                              env={"GIT_DIR": str(self.remote)})
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(output.read_text())
        self.assertEqual(data["repositories"][0]["commonGitDir"], str((self.repo / ".git").resolve()))
        self.assertEqual(len(data["repositories"][0]["worktrees"]), 1)


if __name__ == "__main__":
    unittest.main()
