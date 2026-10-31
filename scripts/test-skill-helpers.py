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
    def test_test_directory_policy_is_the_same_at_root_and_nested(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for prefix in (Path(), Path('src')):
                for name in ('test', 'tests', '__tests__', 'fixture', 'fixtures', 'mock', 'mocks'):
                    path = root / prefix / name / 'fixture.ts'
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text('const key = process.env.KEY || "fallback";')
            (root / 'tests-data').mkdir()
            (root / 'tests-data/config.ts').write_text('const key = process.env.KEY || "fallback";')
            (root / 'screen.test.ts').write_text('const key = process.env.KEY || "fallback";')
            script = 'fail-fast/scripts/scan-fallbacks.py'
            default = cli(script, root, '--json')
            included = cli(script, root, '--json', '--include-tests')
            self.assertEqual(default.returncode, 0, default.stderr)
            self.assertEqual(included.returncode, 0, included.stderr)
            self.assertEqual(len({item['file'] for item in json.loads(default.stdout)}), 1)
            self.assertEqual(len({item['file'] for item in json.loads(included.stdout)}), 16)

    def test_component_json_is_complete_beyond_every_text_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for group in range(27):
                body = '\n'.join(f'const group_{group}_line_{line} = source_{group}({line});' for line in range(9))
                for copy in range(12 if group == 0 else 2):
                    (root / f'group_{group}_copy_{copy}.ts').write_text(body)
            script = 'componentize/scripts/find-god-files.py'
            result = cli(script, root, '--min-score', 0, '--max-files', 1, '--json')
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data['candidateCount'], 64)
            self.assertEqual(len(data['candidates']), 64)
            self.assertEqual(data['returnedCandidateCount'], 64)
            self.assertEqual(data['duplicateGroupCount'], 27)
            self.assertEqual(len(data['duplicateBlocks']), 27)
            self.assertEqual(data['returnedDuplicateGroupCount'], 27)
            self.assertEqual(max(len(g['matches']) for g in data['duplicateBlocks']), 12)
            self.assertFalse(data['truncated'])
            text = cli(script, root, '--min-score', 0, '--max-files', 1)
            self.assertIn('63 more candidates', text.stdout)
            self.assertIn('17 more groups', text.stdout)
            self.assertIn('8 more matches', text.stdout)

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
    def test_supported_markdown_forms_and_code_examples(self):
        cases = [
            ('[ok](exists.md)', 0),
            ('[ok](<exists.md>)', 0),
            ('[ok](<file with spaces.md>)', 0),
            ('[ok](file%20with%20spaces.md)', 0),
            ('[ok](exists.md "Title")', 0),
            ('[ok](exists.md#section)', 0),
            ('[ok](exists.md#section-1)', 0),
            ('[broken](exists.md#missing)', 1),
            ('[ok](file(with).md)', 0),
            ('[t][r]\n\n[r]: exists.md', 0),
            ('[t][]\n\n[t]: exists.md', 0),
            ('[t]\n\n[t]: exists.md', 0),
            ('[t][r]\n\n[r]: missing.md', 1),
            ('[broken](<missing file.md>)', 1),
            ('![image](exists.png)', 0),
            ('![image](missing.png)', 1),
            ('[![image](missing.png)](exists.md)', 1),
            ('[![image][picture]](exists.md)\n\n[picture]: exists.png', 0),
            ('`[code](missing.md)`', 0),
            ('``literal `[code](missing.md)` ``', 0),
            ('````md\n```\n[code](missing.md)\n````', 0),
            ('- Item\n\n    [missing](missing.md)', 2),
            ('    [code](missing.md)', 2),
            ('[undefined][reference]', 2),
            ('[t][r]\n\n[r]:\n  exists.md', 2),
            ('<a href="missing.md">HTML</a>', 2),
        ]
        for body, expected in cases:
            with self.subTest(body=body), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / 'README.md').write_text(body)
                for name in ('exists.md', 'file with spaces.md', 'file(with).md'):
                    (root / name).write_text('# Section\n# Section\n')
                (root / 'exists.png').write_bytes(b'fixture')
                result = cli('product-description/references/check-links.py', root)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_empty_coverage_and_valid_code_heading(self):
        script = "product-description/references/check-links.py"
        with tempfile.TemporaryDirectory() as directory:
            self.assertNotEqual(cli(script, directory).returncode, 0)
            self.assertNotEqual(cli(script, Path(directory, "missing")).returncode, 0)
            Path(directory, "README.md").write_text("# The `dry_run` flag\n[Flag](#the-dry_run-flag)\n")
            result = cli(script, directory)
            self.assertEqual(result.returncode, 0, result.stdout)


class SkillGateContracts(unittest.TestCase):
    def setUp(self):
        self.module = runpy.run_path(str(ROOT / 'scripts/check-skills.py'))
        self.globals = self.module['read_openai_yaml'].__globals__
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.globals['REPO_ROOT'] = self.root
        self.skill = self.root / 'fixture'
        self.skill.mkdir()
        (self.skill / 'SKILL.md').write_text('# Fixture\n')

    def test_model_names_are_checked_in_nested_references(self):
        path = self.skill / 'references/interface/guide.md'
        path.parent.mkdir(parents=True)
        path.write_text('Use a frontier model.\n')
        self.module['check_model_names']()
        self.assertEqual(self.module['errors'], [])
        path.write_text('Use Opus.\n')
        self.module['check_model_names']()
        self.assertTrue(any('references/interface/guide.md:1' in e for e in self.module['errors']))

    def test_markdown_link_cannot_resolve_by_basename_elsewhere(self):
        path = self.skill / 'references/interface/guide.md'
        path.parent.mkdir(parents=True)
        path.write_text('# Guide\n')
        entry = self.skill / 'SKILL.md'
        entry.write_text('[Guide](references/guide.md)\n')
        self.module['check_links']()
        self.assertTrue(any('broken .md reference' in e for e in self.module['errors']))
        self.module['errors'].clear()
        entry.write_text('[Guide](references/interface/guide.md) and prose shorthand `guide.md`\n')
        self.module['check_links']()
        self.assertEqual(self.module['errors'], [])

    def test_openai_schema_checks_boolean_types_and_scalar_depth(self):
        path = self.skill / 'agents/openai.yaml'
        path.parent.mkdir()
        valid = 'interface:\n  display_name: "Fixture"\n  short_description: "A useful fixture description"\npolicy:\n  allow_implicit_invocation: false\n'
        cases = [
            (valid, None),
            (valid.replace(': false', ': "false"'), 'Boolean'),
            (valid.replace('  short_description:', '    short_description:'), 'indentation'),
            (valid + 'dependencies:\n  tools:\n    - type: "mcp"\n      value: "fixture"\n      description: "Fixture tool"\n', None),
            (valid + 'dependencies:\n  tools:\n    - type: "mcp"\n        value: "fixture"\n', 'indentation'),
        ]
        for body, error in cases:
            with self.subTest(body=body):
                self.module['errors'].clear()
                path.write_text(body)
                self.module['read_openai_yaml'](path, report=True)
                if error:
                    self.assertTrue(any(error in e for e in self.module['errors']), self.module['errors'])
                else:
                    self.assertEqual(self.module['errors'], [])


class ConfiguredCredentials(unittest.TestCase):
    def test_environment_credential_validation(self):
        for value in [None, "", " ", "fixture\nInjected: header", "fixture\rvalue", "fixture\tvalue", "fixture-token"]:
            env = {"PATH": os.environ["PATH"]}
            if value is not None:
                env["TEST_API_KEY"] = value
            with tempfile.TemporaryDirectory() as directory:
                result = subprocess.run(
                    [sys.executable, str(ROOT / "web-research/scripts/read-credential.py"), "TEST_API_KEY"],
                    env=env, cwd=directory, capture_output=True, text=True, timeout=10)
            if value == "fixture-token":
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, value)
            else:
                self.assertEqual(result.returncode, 78)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("fixture", result.stderr)

    def test_repository_root_env_file_is_the_fallback(self):
        script = str(ROOT / "web-research/scripts/read-credential.py")
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(["git", "init", "-q", directory], check=True)
            Path(directory, ".env").write_text('# keys\nOTHER=1\nexport TEST_API_KEY="from-file" \nPLAIN_KEY=plain # note\n')
            nested = Path(directory, "apps", "web")
            nested.mkdir(parents=True)
            env = {"PATH": os.environ["PATH"]}
            for name, expected in [("TEST_API_KEY", "from-file"), ("PLAIN_KEY", "plain")]:
                result = subprocess.run([sys.executable, script, name], env=env, cwd=nested,
                    capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, expected)
            result = subprocess.run([sys.executable, script, "TEST_API_KEY"], env={**env, "TEST_API_KEY": "from-env"},
                cwd=nested, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.stdout, "from-env")
            result = subprocess.run([sys.executable, script, "ABSENT_KEY"], env=env, cwd=nested,
                capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 78)
            self.assertEqual(result.stdout, "")

    def test_wrappers_stop_before_transport_without_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory, "called")
            transport = Path(directory, "curl")
            transport.write_text(f"#!{sys.executable}\nfrom pathlib import Path\nPath({str(marker)!r}).touch()\n")
            transport.chmod(0o700)
            for script, args in [("web-research/scripts/request", ["exa", "search"]), ("web-research/scripts/request", ["tavily", "search"])]:
                result = subprocess.run(["/bin/sh", str(ROOT / script), *args],
                    input='{"query":"fixture"}', capture_output=True, text=True, timeout=10, cwd=directory,
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


def load_tests(loader, tests, pattern):
    sys.dont_write_bytecode = True
    tests.addTests(loader.discover(str(ROOT / "salvage/scripts"), pattern="test_*.py"))
    return tests


if __name__ == "__main__":
    unittest.main()
