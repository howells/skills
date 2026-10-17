"""Exercise launcher modes and desktop ownership without a model or GUI."""

import fcntl
import json
import os
from pathlib import Path
import pty
import signal
import subprocess
import sys
import tempfile
import time
import unittest


RUNNER = Path(__file__).resolve().parents[1] / 'scripts' / 'run.py'
FAKE_CODEX = '''
import fcntl
import json
import os
from pathlib import Path
import sys
import time

folder = Path(os.environ['COMPUTER_USE_TEST_FOLDER'])
args = sys.argv[1:]
record = {'args': args, 'home': os.environ['CODEX_HOME'],
          'electron': os.environ.get('ELECTRON_RUN_AS_NODE'), 'pid': os.getpid()}
if args[:2] == ['plugin', 'list']:
    print(json.dumps({'installed': [
        {'pluginId': name + '@openai-bundled', 'enabled': True}
        for name in ['computer-use', 'unified-computer-use']]}))
else:
    with (Path(record['home']) / 't3-computer-use.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            record['desktop_locked'] = False
        except BlockingIOError:
            record['desktop_locked'] = True
    if args[0] == 'exec':
        record['brief'] = sys.stdin.read()
        Path(args[args.index('--output-last-message') + 1]).write_text('Observed task outcome.')
        print(json.dumps({'type': 'turn.completed'}))
with (folder / 'calls.jsonl').open('a') as output:
    output.write(json.dumps(record) + '\\n')
if (folder / 'wait-for-signal').exists() and args[:2] != ['plugin', 'list']:
    (folder / 'started').touch()
    while True:
        time.sleep(1)
'''


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='computer-use-test-')
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name).resolve()
        self.local = self.folder / 'local-codex'
        self.local.mkdir()
        self.config = self.local / 'config.toml'
        self.original_config = 'model_provider = "configured-api-provider"\napproval_policy = "never"\n'
        self.config.write_text(self.original_config)
        binary = self.folder / 'bin'
        binary.mkdir()
        fake = binary / 'codex'
        fake.write_text('#!' + sys.executable + '\n' + FAKE_CODEX)
        fake.chmod(0o700)
        self.environment = dict(os.environ)
        self.environment.update({
            'PATH': str(binary) + os.pathsep + os.environ.get('PATH', ''),
            'COMPUTER_USE_TEST_FOLDER': str(self.folder),
            'ELECTRON_RUN_AS_NODE': '1',
        })

    def command(self, *args):
        return [sys.executable, str(RUNNER), '--codex-home', str(self.local), *args]

    def calls(self):
        path = self.folder / 'calls.jsonl'
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def interactive(self, *args):
        master, slave = pty.openpty()
        self.addCleanup(os.close, master)
        child = subprocess.Popen(self.command(*args), stdin=slave, stdout=slave,
                                 stderr=slave, env=self.environment)
        os.close(slave)
        self.addCleanup(self.stop, child)
        return child

    @staticmethod
    def stop(child):
        if child.poll() is None:
            child.terminate()
            child.wait(timeout=5)

    def assert_unlocked(self):
        with (self.local / 't3-computer-use.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def test_configuration_check_never_starts_a_controller(self):
        result = subprocess.run(self.command('--check'), capture_output=True, text=True,
                                env=self.environment, check=True)
        self.assertEqual(json.loads(result.stdout)['codex_home'], str(self.local))
        self.assertEqual(len(self.calls()), 1)
        self.assertEqual(self.calls()[0]['args'][:2], ['plugin', 'list'])

    def test_app_approval_requires_a_human_terminal_before_startup(self):
        result = subprocess.run(self.command('--approve-app', 'Google Chrome'),
                                stdin=subprocess.DEVNULL, capture_output=True,
                                text=True, env=self.environment)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.calls(), [])

    def test_interactive_probe_preserves_configuration_and_uses_normal_approvals(self):
        child = self.interactive('--approve-app', 'Google Chrome')
        self.assertEqual(child.wait(timeout=10), 0)
        call = self.calls()[-1]
        args = call['args']
        self.assertNotEqual(args[0], 'exec')
        self.assertEqual(args[args.index('--ask-for-approval') + 1], 'on-request')
        self.assertEqual(args[args.index('--sandbox') + 1], 'read-only')
        self.assertEqual(args[args.index('--enable') + 1], 'computer_use')
        self.assertNotIn('--model', args)
        self.assertNotIn('--dangerously-bypass-approvals-and-sandbox', args)
        self.assertIn('"Google Chrome"', args[-1])
        self.assertEqual(call['home'], str(self.local))
        self.assertIsNone(call['electron'])
        self.assertTrue(call['desktop_locked'])
        self.assertEqual(self.config.read_text(), self.original_config)
        self.assertFalse((self.local / 'auth.json').exists())
        self.assert_unlocked()

    def test_another_controller_prevents_interactive_probe(self):
        with (self.local / 't3-computer-use.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            child = self.interactive('--approve-app', 'com.google.Chrome')
            self.assertEqual(child.wait(timeout=10), 2)
        self.assertEqual(len(self.calls()), 1)
        self.assertEqual(self.calls()[0]['args'][:2], ['plugin', 'list'])

    def test_task_keeps_headless_evidence_and_selected_sandbox(self):
        brief = self.folder / 'brief.txt'
        brief.write_text('Inspect the requested app and verify its visible state.')
        output = self.folder / 'invocation'
        result = subprocess.run(self.command('--brief', str(brief), '--output-dir', str(output),
                                             '--sandbox', 'read-only'),
                                capture_output=True, text=True, env=self.environment)
        self.assertEqual(result.returncode, 0, result.stderr)
        call = self.calls()[-1]
        self.assertEqual(call['args'][0], 'exec')
        self.assertEqual(call['args'][call['args'].index('--sandbox') + 1], 'read-only')
        self.assertTrue(call['desktop_locked'])
        self.assertIn(brief.read_text(), call['brief'])
        self.assertEqual((output / 'result.txt').read_text(), 'Observed task outcome.')
        self.assertTrue((output / 'events.jsonl').is_file())
        self.assertTrue((output / 'stderr.log').is_file())
        self.assert_unlocked()

    def test_terminating_interactive_probe_stops_child_and_releases_desktop(self):
        (self.folder / 'wait-for-signal').touch()
        child = self.interactive('--approve-app', 'Google Chrome')
        deadline = time.monotonic() + 10
        while not (self.folder / 'started').exists():
            if child.poll() is not None or time.monotonic() >= deadline:
                self.fail('Interactive child did not start')
            time.sleep(0.02)
        call = self.calls()[-1]
        child.terminate()
        self.assertEqual(child.wait(timeout=5), 128 + signal.SIGTERM)
        with self.assertRaises(ProcessLookupError):
            os.kill(call['pid'], 0)
        self.assert_unlocked()


if __name__ == '__main__':
    unittest.main()
