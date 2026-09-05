#!/usr/bin/env python3
"""Regression checks for scan coverage, typography evidence and API outcomes.

Run from any directory: python3 scripts/test-skill-helpers.py.
Fixtures are temporary; no provider, account or production repository is used.
"""
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


def cli(path, *args, body=None):
    return subprocess.run([sys.executable, str(ROOT / path), *map(str, args)],
                          input=body, capture_output=True, text=True, timeout=10)


class ScannerCoverage(unittest.TestCase):
    def test_regular_file_and_empty_directory_are_not_clean_scans(self):
        for script in ["componentize/scripts/find-god-files.py", "fail-fast/scripts/scan-fallbacks.py", "typecase/scripts/census-typography.py"]:
            with self.subTest(script=script), tempfile.TemporaryDirectory() as directory:
                self.assertNotEqual(cli(script, ROOT / "README.md", "--json").returncode, 0)
                self.assertNotEqual(cli(script, directory, "--json").returncode, 0)

    def test_real_scans_report_coverage_and_find_a_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "config.ts").write_text('export const key = process.env.KEY || "fallback";')
            fallback = cli("fail-fast/scripts/scan-fallbacks.py", directory, "--json", "--fail-on", "high")
            self.assertEqual(fallback.returncode, 1)
            self.assertTrue(any(item["rule"] == "env-default" for item in json.loads(fallback.stdout)))
            self.assertIn("Scanned 1", fallback.stderr)
            component = cli("componentize/scripts/find-god-files.py", directory, "--json")
            self.assertEqual(component.returncode, 0, component.stderr)
            self.assertEqual(json.loads(component.stdout)["scannedFileCount"], 1)

    def test_partial_scan_preserves_findings_without_a_clean_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "config.ts").write_text('const key = process.env.KEY || "fallback";')
            Path(directory, "binary.js").write_bytes(b"\0")
            result = cli("fail-fast/scripts/scan-fallbacks.py", directory, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertTrue(any(item["rule"] == "env-default" for item in json.loads(result.stdout)))
            self.assertIn("incomplete", result.stderr)

    def test_unreadable_subdirectory_never_reports_clean(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "readable.ts").write_text('const text = "text-sm";')
            Path(directory, "README.md").write_text('# Readable\n')
            locked = Path(directory, "locked")
            locked.mkdir()
            Path(locked, "hidden.ts").write_text('const key = process.env.KEY || "default";')
            Path(locked, "hidden.md").write_text('[broken](missing.md)')
            locked.chmod(0)
            try:
                if os.access(locked, os.R_OK):
                    self.skipTest("Process can read mode-000 directories")
                for script in ["componentize/scripts/find-god-files.py", "fail-fast/scripts/scan-fallbacks.py", "typecase/scripts/census-typography.py", "product-description/references/check-links.py"]:
                    with self.subTest(script=script):
                        self.assertNotEqual(cli(script, directory).returncode, 0)
            finally:
                locked.chmod(0o700)


class Typography(unittest.TestCase):
    def test_migration_inventory_retains_variants_leading_and_locations(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "screen.tsx").write_text('<p className="text-sm md:text-lg" />\n<p className="text-lg md:text-sm" />\n<p className="text-sm/6" />\n<p className="text-sm/8" />\nconst sizes: Record<Size, string> = {small: "text-xs", large: "text-xl"};\n// <p className="text-9xl" />\n<p className="leading-(--height) leading-[calc(1em+2px)] tracking-(--space) -tracking-2" />\n')
            result = cli("typecase/scripts/census-typography.py", directory, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            combinations = {tuple(item["tokens"]): item for item in data["combinations"]}
            for tokens in [("md:text-lg", "text-sm"), ("md:text-sm", "text-lg"), ("text-sm/6",), ("text-sm/8",), ("text-xs",), ("text-xl",)]:
                self.assertIn(tokens, combinations)
            self.assertNotIn("text-9xl", data["sizes"])
            self.assertEqual(combinations[("text-sm/8",)]["locations"], [{"file": "screen.tsx", "line": 4}])
            self.assertTrue(any("leading-(--height)" in tokens for tokens in combinations))

    def test_colours_stay_outside_typography(self):
        module = runpy.run_path(str(ROOT / "typecase/scripts/census-typography.py"))
        for token in ["text-[#fff]", "text-[var(--ink)]", "text-[color:var(--ink)]", "text-[oklch(0.5_0.2_20)]"]:
            self.assertFalse(module["is_shape"](token), token)

    def test_missing_requested_root_is_not_partial_success(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "screen.tsx").write_text('<p className="text-sm" />')
            result = cli("typecase/scripts/census-typography.py", directory, "--roots", ".", "missing", "--json")
            self.assertNotEqual(result.returncode, 0)


class DocumentationLinks(unittest.TestCase):
    def test_empty_coverage_and_valid_code_heading(self):
        script = "product-description/references/check-links.py"
        with tempfile.TemporaryDirectory() as directory:
            self.assertNotEqual(cli(script, directory).returncode, 0)
            self.assertNotEqual(cli(script, Path(directory, "missing")).returncode, 0)
            Path(directory, "README.md").write_text("# The `dry_run` flag\n[Flag](#the-dry_run-flag)\n")
            result = cli(script, directory)
            self.assertEqual(result.returncode, 0, result.stdout)


class GraphQLOutcomes(unittest.TestCase):
    def test_partial_errors_and_mutation_failure_are_failures(self):
        for data in [{"data": {"viewer": None}, "errors": [{"message": "denied"}]}, {"data": {"issueCreate": {"success": False}}}, {"data": None}, []]:
            with self.subTest(data=data):
                body = json.dumps(data)
                result = cli("linear/scripts/check-response.py", body=body)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, body)

    def test_success_body_is_preserved(self):
        body = json.dumps({"data": {"issues": {"nodes": []}}})
        result = cli("linear/scripts/check-response.py", body=body)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, body)

    def test_non_json_is_failure(self):
        result = cli("linear/scripts/check-response.py", body="proxy unavailable")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "proxy unavailable")

    def test_standalone_credential_helpers_agree(self):
        self.assertEqual((ROOT / "linear/scripts/read-credential.py").read_bytes(),
                         (ROOT / "web-research/scripts/read-credential.py").read_bytes())


class ConfiguredCredentials(unittest.TestCase):
    def test_environment_credential_validation(self):
        for value in [None, "", " ", "fixture\nInjected: header", "fixture\rvalue", "fixture\tvalue", "fixture-token"]:
            env = {"PATH": os.environ["PATH"]}
            if value is not None:
                env["TEST_API_KEY"] = value
            result = subprocess.run(
                [sys.executable, str(ROOT / "linear/scripts/read-credential.py"), "TEST_API_KEY"],
                env=env, capture_output=True, text=True, timeout=10)
            if value == "fixture-token":
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, value)
            else:
                self.assertEqual(result.returncode, 78)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("fixture", result.stderr)

    def test_wrappers_stop_before_transport_without_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory, "called")
            transport = Path(directory, "curl")
            transport.write_text(f"#!{sys.executable}\nfrom pathlib import Path\nPath({str(marker)!r}).touch()\n")
            transport.chmod(0o700)
            for script, args in [("linear/scripts/graphql", []), ("web-research/scripts/request", ["exa", "search"]), ("web-research/scripts/request", ["tavily", "search"])]:
                result = subprocess.run(["/bin/sh", str(ROOT / script), *args],
                    input='{"query":"fixture"}', capture_output=True, text=True, timeout=10,
                    env={"PATH": directory + os.pathsep + os.environ["PATH"]})
                self.assertEqual(result.returncode, 78, result.stderr)
                self.assertFalse(marker.exists())
                self.assertEqual(result.stdout, "")

    def test_wrappers_preserve_body_and_select_injected_provider_key(self):
        # A local transport fixture exercises the real shell/credential pipes,
        # including fd 3, without calling a provider or using a real credential.
        with tempfile.TemporaryDirectory() as directory:
            transport = Path(directory, "curl")
            transport.write_text(f"#!{sys.executable}\n" + """import json, sys
args = sys.argv[1:]
body = open('/dev/fd/3').read() if '--data-binary' in args else None
print(json.dumps({'data': {'header': sys.stdin.read(), 'body': body, 'args': args}}))
""")
            transport.chmod(0o700)
            cases = [
                ("linear/scripts/graphql", [], "LINEAR_API_KEY", "", "https://api.linear.app/graphql"),
                ("web-research/scripts/request", ["exa", "search"], "EXA_API_KEY", "Bearer ", "https://api.exa.ai/search"),
                ("web-research/scripts/request", ["tavily", "search"], "TAVILY_API_KEY", "Bearer ", "https://api.tavily.com/search"),
                ("web-research/scripts/request", ["tavily", "research-status", "request-123"], "TAVILY_API_KEY", "Bearer ", "https://api.tavily.com/research/request-123"),
            ]
            body = '{"query":"fixture with spaces"}\n'
            for script, args, key, prefix, url in cases:
                env = {"PATH": directory + os.pathsep + os.environ["PATH"], key: "fixture-token"}
                result = subprocess.run(["/bin/sh", str(ROOT / script), *args], input=body,
                    capture_output=True, text=True, timeout=10, env=env)
                self.assertEqual(result.returncode, 0, result.stderr)
                data = json.loads(result.stdout)["data"]
                self.assertEqual(data["header"], f"Authorization: {prefix}fixture-token\n")
                self.assertEqual(data["body"], None if "research-status" in args else body)
                self.assertIn(url, data["args"])
                self.assertNotIn("fixture-token", " ".join(data["args"]))


if __name__ == "__main__":
    unittest.main()
