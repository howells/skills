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


if __name__ == "__main__":
    unittest.main()
