#!/usr/bin/env python3
"""Command-boundary fixtures for salvage's operational helpers."""
import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parent


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


class GitIntegration(GitFixture):
    def integrate(self, old, head, **kwargs):
        return self.command("integrate.py", "--repo", self.repo, "--remote", "origin",
                            "--intent", "integrate", "--commit", head,
                            "--expected-old", old, **kwargs)

    def test_integration_uses_the_server_default_with_ordinary_hooks(self):
        old = self.repository()
        head = self.commit("candidate")
        marker = self.root / "hook-called"
        hook = self.repo / ".git/hooks/pre-push"
        hook.write_text(f"#!/bin/sh\nprintf gate > '{marker}'\n")
        hook.chmod(0o700)
        result = self.command("integrate.py", "--repo", self.repo, "--remote", "origin",
                              "--intent", "integrate", "--commit", head,
                              "--expected-old", old)
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["destinationRef"], "refs/heads/main")
        self.assertEqual(receipt["sha"], head)
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/main").stdout.strip(), head)
        self.assertTrue(marker.exists())

    def test_master_wins_over_stale_local_remote_head(self):
        old = self.repository("master")
        git(self.repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
        git(self.repo, "update-ref", "refs/remotes/origin/retained", old)
        git(self.repo, "config", "fetch.prune", "true")
        head = self.commit("candidate")
        result = self.integrate(old, head)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["destinationRef"], "refs/heads/master")
        self.assertNotEqual(git(self.remote, "show-ref", "--verify", "refs/heads/main", check=False).returncode, 0)
        self.assertEqual(git(self.repo, "rev-parse", "refs/remotes/origin/retained").stdout.strip(), old)

    def test_only_the_verified_destination_is_pushed(self):
        old = self.repository()
        head = self.commit("candidate")
        git(self.repo, "tag", "-a", "unrelated-release", "-m", "not requested")
        git(self.repo, "config", "push.followTags", "true")
        result = self.integrate(old, head)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotEqual(git(self.remote, "show-ref", "--verify", "refs/tags/unrelated-release", check=False).returncode, 0)

    def test_missing_or_detached_server_default_is_not_guessed(self):
        old = self.repository()
        head = self.commit("candidate")
        for target in ["refs/heads/missing", old]:
            if target.startswith("refs/"):
                git(self.remote, "symbolic-ref", "HEAD", target)
            else:
                git(self.remote, "update-ref", "--no-deref", "HEAD", target)
            result = self.integrate(old, head)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("default", result.stderr)
            self.assertEqual(git(self.remote, "rev-parse", "refs/heads/main").stdout.strip(), old)
            self.assertEqual(result.stdout, "")

    def test_wrong_expected_tip_and_non_fast_forward_do_not_push(self):
        old = self.repository()
        moved = self.commit("remote change")
        git(self.repo, "push", "-q", "origin", "HEAD:refs/heads/main")
        git(self.repo, "checkout", "-q", "--detach", old)
        head = self.commit("divergent candidate")
        for expected, message in [(old, "expected old"), (moved, "fast-forward")]:
            result = self.integrate(expected, head)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(message, result.stderr)
            self.assertEqual(git(self.remote, "rev-parse", "refs/heads/main").stdout.strip(), moved)

    def test_concurrent_remote_update_and_failing_hooks_reject(self):
        old = self.repository()
        head = self.commit("candidate")
        hook = self.repo / ".git/hooks/pre-push"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o700)
        result = self.integrate(old, head)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ordinary hooks", result.stderr)
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/main").stdout.strip(), old)
        tree = git(self.remote, "rev-parse", old + "^{tree}").stdout.strip()
        concurrent = git(self.remote, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                         "commit-tree", tree, "-p", old, "-m", "concurrent").stdout.strip()
        hook.write_text(f"#!/bin/sh\ngit --git-dir='{self.remote}' update-ref refs/heads/main {concurrent} {old}\n")
        result = self.integrate(old, head)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/main").stdout.strip(), concurrent)
        self.assertEqual(result.stdout, "")

    def test_non_head_preservation_is_explicit_and_does_not_claim_source_checks(self):
        old = self.repository()
        self.commit("current working tree")
        marker = self.root / "unverified"
        hook = self.repo / ".git/hooks/pre-push"
        hook.write_text(f"#!/bin/sh\nhead=$(git rev-parse HEAD)\nread local_ref local_sha remote_ref remote_sha\n[ \"$local_sha\" != \"$head\" ] || exit 1\nprintf unverified > '{marker}'\n")
        hook.chmod(0o700)
        result = self.command("integrate.py", "--repo", self.repo, "--remote", "origin",
                              "--intent", "preserve", "--commit", old, "--expected-old", "absent",
                              "--destination-ref", "refs/salvage/fixture")
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["intent"], "preserve")
        self.assertFalse(receipt["pushedIsHead"])
        self.assertIn("not performed", receipt["sourceVerification"])
        self.assertEqual(marker.read_text(), "unverified")
        self.assertEqual(git(self.remote, "rev-parse", "refs/salvage/fixture").stdout.strip(), old)
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/main").stdout.strip(), old)

    def test_detached_remote_default_still_allows_explicit_salvage(self):
        old = self.repository()
        git(self.remote, "update-ref", "--no-deref", "HEAD", old)
        result = self.command("integrate.py", "--repo", self.repo, "--remote", "origin",
                              "--intent", "preserve", "--commit", old, "--expected-old", "absent",
                              "--destination-ref", "refs/salvage/fixture")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(git(self.remote, "rev-parse", "refs/salvage/fixture").stdout.strip(), old)

    def test_explicit_repository_ignores_inherited_git_directory(self):
        old = self.repository()
        head = self.commit("candidate")
        result = self.integrate(old, head, env={"GIT_DIR": str(self.remote)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/main").stdout.strip(), head)

    def test_configured_submodule_recursion_cannot_fetch_or_publish_another_repository(self):
        self.repository()
        nested = self.repo / "nested"
        nested_remote = self.root / "nested-remote.git"
        git(self.root, "init", "-q", "--initial-branch=main", str(nested))
        git(self.root, "init", "-q", "--bare", "--initial-branch=main", str(nested_remote))
        git(nested, "config", "user.name", "Fixture")
        git(nested, "config", "user.email", "fixture@example.invalid")
        git(nested, "remote", "add", "origin", str(nested_remote))
        (nested / "source.txt").write_text("nested base")
        git(nested, "add", "source.txt")
        git(nested, "commit", "-q", "-m", "nested base")
        nested_old = git(nested, "rev-parse", "HEAD").stdout.strip()
        git(nested, "push", "-q", "-u", "origin", "HEAD:refs/heads/main")
        (self.repo / ".gitmodules").write_text('[submodule "nested"]\n\tpath = nested\n\turl = ' + str(nested_remote) + '\n')
        git(self.repo, "add", ".gitmodules", "nested")
        git(self.repo, "commit", "-q", "-m", "record nested source")
        old = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        git(self.repo, "push", "-q", "origin", "HEAD:refs/heads/main")
        (nested / "source.txt").write_text("nested unpublished work")
        git(nested, "add", "source.txt")
        git(nested, "commit", "-q", "-m", "nested unpublished work")
        git(self.repo, "add", "nested")
        git(self.repo, "commit", "-q", "-m", "candidate")
        head = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        git(self.repo, "config", "fetch.recurseSubmodules", "true")
        git(self.repo, "config", "push.recurseSubmodules", "on-demand")
        marker = self.root / "nested-push-called"
        hook = nested / ".git/hooks/pre-push"
        hook.write_text(f"#!/bin/sh\nprintf invoked > '{marker}'\n")
        hook.chmod(0o700)
        result = self.integrate(old, head)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(git(nested_remote, "rev-parse", "refs/heads/main").stdout.strip(), nested_old)
        self.assertFalse((nested / ".git/FETCH_HEAD").exists())
        self.assertFalse(marker.exists())


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
        self.assertTrue(checkout["protected"])
        self.assertEqual(checkout["ownership"], [])
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

    def test_registered_owner_exclusion_is_explicit_in_complete_evidence(self):
        old = self.repository()
        linked = self.root / "held-worktree"
        git(self.repo, "worktree", "add", "-q", "--detach", str(linked), old)
        ownership = self.root / "ownership.json"
        claim = {"path": str(linked), "owner": "Fixture owner", "scope": "all mutations",
                 "permittedActions": ["read"], "authority": "https://example.invalid/owner-handoff",
                 "releaseCondition": "owner handoff", "exclude": True}
        ownership.write_text(json.dumps({"version": 1, "claims": [claim]}))
        before = self.snapshot(self.repo, linked)
        output = self.root / "evidence.json"
        result = self.command("census.py", self.repo, "--ownership", ownership, "--output", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(output.read_text())
        held = next(item for item in data["repositories"][0]["worktrees"] if item["path"] == str(linked.resolve()))
        self.assertTrue(held["excluded"])
        self.assertEqual(held["ownership"], [claim])
        self.assertTrue(held["protected"])
        self.assertTrue(any(item["path"] == str(linked.resolve()) for item in data["coverage"]["exclusions"]))
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
        self.assertTrue(missing["protected"])
        self.assertFalse(data["coverage"]["complete"])
        self.assertEqual(self.snapshot(self.repo), before)

    def test_malformed_ownership_input_produces_incomplete_parseable_evidence(self):
        self.repository()
        ownership = self.root / "ownership.json"
        ownership.write_text("[]")
        output = self.root / "evidence.json"
        result = self.command("census.py", self.repo, "--ownership", ownership, "--output", output)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(output.read_text())["coverage"]["complete"])
        self.assertNotIn("Traceback", result.stderr)

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
