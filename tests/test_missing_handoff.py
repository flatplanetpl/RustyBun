"""Regression checks for redisplay before preparation; no network or model calls."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/prepare-review-run.py'


class MissingHandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.out = self.root / 'review-output'

    def tearDown(self):
        self.temp.cleanup()

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              capture_output=True, text=True, encoding='utf-8')

    def make_pack(self):
        pack = self.root / 'input pack'
        pack.mkdir()
        template = {'status': 'NOT_RUN', 'runtime': {}, 'isolation': {},
                    'measurements': {}, 'gate_decision': {}}
        files = {'TASK.md': 'Design only.\n', 'AGENTS.md': 'Read TASK.md.\n',
                 'input/brief.md': 'A neutral brief.\n',
                 'RUN-RECORD.template.json': json.dumps(template)}
        manifest = {'kind': 'independent-design', 'process_sha': 'a' * 40,
                    'source_sha': None, 'files': []}
        for name, text in files.items():
            p = pack / name
            p.parent.mkdir(parents=True, exist_ok=True)
            data = text.encode('utf-8')
            p.write_bytes(data)
            manifest['files'].append({'path': name, 'bytes': len(data),
                                      'sha256': hashlib.sha256(data).hexdigest()})
        (pack / 'MANIFEST.json').write_text(json.dumps(manifest), encoding='utf-8')
        return pack

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob('*') if p.is_file() and not p.is_symlink()}

    def test_missing_directory_explains_prepare_and_does_not_create(self):
        result = self.cli('--show-handoff', self.out)
        self.assertEqual(result.returncode, 1)
        self.assertIn(str(self.out / 'RUN-RECORD.json'), result.stderr)
        self.assertIn('--show-handoff only redisplays', result.stderr)
        self.assertIn('--pack INPUT_PACK --out NEW_OUTPUT_DIR --run-id RUN_ID', result.stderr)
        self.assertIn('Preparation prints the reviewer prompt automatically', result.stderr)
        self.assertFalse(self.out.exists())
        self.assertNotIn('BEGIN REVIEWER PROMPT', result.stdout)

    def test_empty_directory_remains_empty(self):
        self.out.mkdir()
        result = self.cli('--show-handoff', self.out)
        self.assertEqual(result.returncode, 1)
        self.assertIn('No files were changed', result.stderr)
        self.assertEqual(list(self.out.iterdir()), [])

    def test_partial_output_is_preserved(self):
        self.out.mkdir()
        (self.out / 'independent-design.md').write_text('Keep existing work.', encoding='utf-8')
        before = self.snapshot()
        result = self.cli('--show-handoff', self.out)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Existing outputs must not be overwritten', result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_input_pack_passed_as_output_is_not_modified(self):
        pack = self.make_pack()
        before = self.snapshot()
        result = self.cli('--show-handoff', pack)
        self.assertEqual(result.returncode, 1)
        self.assertIn('OUTPUT directory, not the input pack', result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_broken_record_symlink_is_not_treated_as_missing_preparation(self):
        self.out.mkdir()
        try:
            (self.out / 'RUN-RECORD.json').symlink_to(self.root / 'absent-record')
        except (OSError, NotImplementedError):
            self.skipTest('Symlink creation unavailable')
        result = self.cli('--show-handoff', self.out)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Symlink is not an authorized input', result.stderr)
        self.assertNotIn('No prepared run record found', result.stderr)
        self.assertTrue((self.out / 'RUN-RECORD.json').is_symlink())

    def test_record_directory_stays_invalid(self):
        (self.out / 'RUN-RECORD.json').mkdir(parents=True)
        result = self.cli('--show-handoff', self.out)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Missing or non-regular input', result.stderr)
        self.assertTrue((self.out / 'RUN-RECORD.json').is_dir())

    def test_create_then_redisplay_still_prints_exact_prompt(self):
        pack = self.make_pack()
        created = self.cli('--pack', pack, '--out', self.out, '--run-id', 'diagnostic-test',
                           '--allow-unverified-isolation')
        self.assertEqual(created.returncode, 0, created.stderr)
        record = json.loads((self.out / 'RUN-RECORD.json').read_bytes())
        self.assertEqual(record['status'], 'PREPARED')
        self.assertFalse(record['isolation_verified'])
        self.assertIsNone(record['started_at'])
        before = self.snapshot()
        shown = self.cli('--show-handoff', self.out)
        self.assertEqual(shown.returncode, 0, shown.stderr)
        self.assertEqual(shown.stdout, created.stdout)
        prompt = shown.stdout.split('----- BEGIN REVIEWER PROMPT -----\n')[1].split('----- END REVIEWER PROMPT -----')[0]
        self.assertEqual(prompt, (self.out / 'START-REVIEW.txt').read_text(encoding='utf-8'))
        self.assertEqual(before, self.snapshot())

    def test_no_implicit_authorization(self):
        pack = self.make_pack()
        created = self.cli('--pack', pack, '--out', self.out, '--run-id', 'blocked-test')
        self.assertEqual(created.returncode, 0, created.stderr)
        shown = self.cli('--show-handoff', self.out)
        self.assertEqual(shown.returncode, 0, shown.stderr)
        self.assertIn('BLOCKED_ENVIRONMENT', shown.stdout)
        self.assertIn('Execution is NOT authorized', shown.stdout)
        self.assertNotIn('READY_EXPLORATORY', shown.stdout)


if __name__ == '__main__':
    unittest.main()
