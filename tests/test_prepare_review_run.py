"""Offline preflight regression tests; never start an agent or contact a service."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/prepare-review-run.py'
SPEC = importlib.util.spec_from_file_location('prepare_review', SCRIPT)
prepare = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prepare)


class PrepareReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.pack = self.root / 'input pack'
        self.out = self.root / 'review output'
        self.pack.mkdir()
        template = {
            'schema_version': '0.1', 'status': 'NOT_RUN', 'run_id': None,
            'runtime': {}, 'isolation': {}, 'measurements': {'wall_seconds': None},
            'gate_decision': {'status': 'PENDING'}, 'output_root': None,
        }
        contents = {
            'AGENTS.md': 'Operator must supply a completed run record and output_root before execution.\n',
            'TASK.md': 'Design a process from the supplied brief.\n',
            'input/docs/project-brief.md': 'Neutral experiment brief.\n',
            'RUN-RECORD.template.json': json.dumps(template),
        }
        self.manifest = {'kind': 'independent-design', 'process_sha': 'a' * 40,
                         'source_sha': None, 'isolation_verified': False, 'files': []}
        for name, text in contents.items():
            path = self.pack / name
            path.parent.mkdir(parents=True, exist_ok=True)
            data = text.encode()
            path.write_bytes(data)
            self.manifest['files'].append({'path': name, 'bytes': len(data),
                                           'sha256': hashlib.sha256(data).hexdigest()})
        self.write_manifest()

    def tearDown(self):
        self.temp.cleanup()

    def write_manifest(self):
        (self.pack / 'MANIFEST.json').write_text(json.dumps(self.manifest), encoding='utf-8')

    def test_existing_v01_pack_prepares_real_metadata(self):
        result = prepare.prepare_run(self.pack, self.out, 'phase0-01', True)
        self.assertEqual(result['status'], 'PREPARED')
        self.assertEqual(result['stage'], 'method-independent')
        self.assertEqual(result['role_id'], 'independent-designer')
        self.assertEqual(result['output_root'], str(self.out.resolve()))
        self.assertEqual(result['process_sha'], 'a' * 40)
        self.assertEqual(result['input_manifest_sha256'], hashlib.sha256((self.pack / 'MANIFEST.json').read_bytes()).hexdigest())
        self.assertIsNone(result['source_sha'])
        self.assertIsNone(result['started_at'])
        self.assertIsNone(result['ended_at'])
        self.assertEqual(result['gate_decision']['status'], 'PENDING')
        self.assertEqual(result['measurements']['wall_seconds'], None)
        self.assertEqual(json.loads((self.out / 'RUN-RECORD.json').read_bytes()), result)
        self.assertIn('EXPLORATORY; INDEPENDENCE UNVERIFIED', (self.out / 'START-REVIEW.txt').read_text())

    def test_no_fabricated_isolation_or_runtime(self):
        result = prepare.prepare_run(self.pack, self.out, 'phase0-02', True)
        self.assertFalse(result['isolation_verified'])
        for key, value in result['isolation'].items():
            if key != 'notes':
                self.assertIsNone(value)
        self.assertEqual(result['runtime']['actual_model'], 'unknown')
        self.assertEqual(result['runtime']['auth_mode'], 'unknown')
        self.assertEqual(result['preflight']['independence'], 'UNVERIFIED')

    def test_no_implicit_waiver(self):
        result = prepare.prepare_run(self.pack, self.out, 'phase0-03')
        self.assertFalse(result['operator_authorization']['allow_unverified_isolation'])
        self.assertEqual(result['preflight']['status'], 'BLOCKED_ENVIRONMENT')
        self.assertIn('Execution is NOT authorized', (self.out / 'START-REVIEW.txt').read_text())

    def test_pack_is_unchanged(self):
        before = {p.relative_to(self.pack): p.read_bytes() for p in self.pack.rglob('*') if p.is_file()}
        prepare.prepare_run(self.pack, self.out, 'phase0-04', True)
        after = {p.relative_to(self.pack): p.read_bytes() for p in self.pack.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_hash_mismatch_blocks_without_output(self):
        (self.pack / 'TASK.md').write_text('changed')
        with self.assertRaises(ValueError):
            prepare.prepare_run(self.pack, self.out, 'phase0-05', True)
        self.assertFalse(self.out.exists())

    def test_missing_input_blocks(self):
        (self.pack / 'TASK.md').unlink()
        with self.assertRaises(ValueError):
            prepare.prepare_run(self.pack, self.out, 'phase0-06', True)
        self.assertFalse(self.out.exists())

    def test_unlisted_file_blocks(self):
        (self.pack / 'other-design.md').write_text('excluded proposal')
        with self.assertRaises(ValueError):
            prepare.prepare_run(self.pack, self.out, 'phase0-07', True)
        self.assertFalse(self.out.exists())

    def test_output_overlap_blocks(self):
        for out in (self.pack, self.pack / 'results', self.root):
            with self.subTest(out=str(out)), self.assertRaises(ValueError):
                prepare.prepare_run(self.pack, out, 'phase0-08', True)

    def test_output_overwrite_blocks(self):
        self.out.mkdir()
        marker = self.out / 'keep.txt'
        marker.write_text('keep me')
        with self.assertRaises(FileExistsError):
            prepare.prepare_run(self.pack, self.out, 'phase0-09', True)
        self.assertEqual(marker.read_text(), 'keep me')

    def test_paths_and_ids_are_validated(self):
        for name in ('../escape', '/etc/passwd', 'C:/path', 'a\\b', 'a//b', './TASK.md', '.'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                prepare.checked_path(self.pack, name)
        for run_id in ('../run', '', 'a/b', 'a b'):
            with self.subTest(run_id=run_id), self.assertRaises(ValueError):
                prepare.prepare_run(self.pack, self.out, run_id, True)

    def test_symlink_input_blocks(self):
        target = self.root / 'outside.md'
        target.write_text('outside')
        try:
            (self.pack / 'linked.md').symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest('Symlink creation not permitted on this platform')
        with self.assertRaises(ValueError):
            prepare.prepare_run(self.pack, self.out, 'phase0-10', True)

    def test_control_directory_blocks(self):
        (self.pack / '.git').mkdir()
        with self.assertRaises(ValueError):
            prepare.prepare_run(self.pack, self.out, 'phase0-11', True)

    def test_duplicate_manifest_entry_blocks(self):
        self.manifest['files'].append(self.manifest['files'][0])
        self.write_manifest()
        with self.assertRaises(ValueError):
            prepare.prepare_run(self.pack, self.out, 'phase0-12', True)

    def test_other_stage_or_source_snapshot_blocks(self):
        self.manifest['kind'] = 'architect'
        self.write_manifest()
        with self.assertRaises(ValueError):
            prepare.prepare_run(self.pack, self.out, 'phase0-13', True)
        self.manifest['kind'] = 'independent-design'
        self.manifest['source_sha'] = 'b' * 40
        self.write_manifest()
        with self.assertRaises(ValueError):
            prepare.prepare_run(self.pack, self.out, 'phase0-13', True)

    def test_cli_prepares_without_model_execution(self):
        completed = subprocess.run([sys.executable, str(SCRIPT), '--pack', str(self.pack),
                                    '--out', str(self.out), '--run-id', 'phase0-cli',
                                    '--allow-unverified-isolation'], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn('No agent started', completed.stdout)
        self.assertEqual({p.name for p in self.out.iterdir()}, {'RUN-RECORD.json', 'START-REVIEW.txt'})


class ReviewHandoffTests(unittest.TestCase):
    setUp = PrepareReviewTests.setUp
    tearDown = PrepareReviewTests.tearDown
    write_manifest = PrepareReviewTests.write_manifest

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              capture_output=True, text=True, encoding='utf-8')

    def test_preparation_prints_exact_saved_prompt_and_access_instructions(self):
        result = self.cli('--pack', self.pack, '--out', self.out, '--run-id', 'phase0-cli',
                          '--allow-unverified-isolation')
        self.assertEqual(result.returncode, 0, result.stderr)
        shown = result.stdout.split('----- BEGIN REVIEWER PROMPT -----\n')[1].split('----- END REVIEWER PROMPT -----')[0]
        self.assertEqual(shown, (self.out / 'START-REVIEW.txt').read_text(encoding='utf-8'))
        self.assertIn('READ ONLY input pack: ' + json.dumps(str(self.pack.resolve())), result.stdout)
        self.assertIn('READ/WRITE output root: ' + json.dumps(str(self.out.resolve())), result.stdout)
        self.assertIn('INDEPENDENCE UNVERIFIED', result.stdout)
        self.assertIn('No agent started', result.stdout)
        self.assertFalse((self.out / 'independent-design.md').exists())

    def test_redisplay_does_not_change_inputs_or_outputs(self):
        prepare.prepare_run(self.pack, self.out, 'old-run', True)
        before = {p: p.read_bytes() for root in (self.pack, self.out) for p in root.rglob('*') if p.is_file()}
        result = self.cli('--show-handoff', self.out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('BEGIN REVIEWER PROMPT', result.stdout)
        after = {p: p.read_bytes() for root in (self.pack, self.out) for p in root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_no_authorization_stays_blocked_in_terminal_and_replay(self):
        result = self.cli('--pack', self.pack, '--out', self.out, '--run-id', 'blocked-run')
        for shown in (result, self.cli('--show-handoff', self.out)):
            self.assertEqual(shown.returncode, 0, shown.stderr)
            self.assertIn('BLOCKED_ENVIRONMENT', shown.stdout)
            self.assertIn('Execution is NOT authorized', shown.stdout)
            self.assertNotIn('READY_EXPLORATORY', shown.stdout)
        self.assertFalse(json.loads((self.out / 'RUN-RECORD.json').read_bytes())['operator_authorization']['allow_unverified_isolation'])

    def test_replay_refuses_changed_input_or_start_text(self):
        prepare.prepare_run(self.pack, self.out, 'original', True)
        task = self.pack / 'TASK.md'
        original = task.read_bytes()
        task.write_text('tampered')
        result = self.cli('--show-handoff', self.out)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('BEGIN REVIEWER PROMPT', result.stdout)
        task.write_bytes(original)
        with (self.out / 'START-REVIEW.txt').open('a') as stream:
            stream.write('Extra instruction')
        result = self.cli('--show-handoff', self.out)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('BEGIN REVIEWER PROMPT', result.stdout)

    def test_replay_refuses_used_run_or_mismatched_record(self):
        original = prepare.prepare_run(self.pack, self.out, 'original', True)
        for change in ({'status': 'COMPLETE'}, {'status': 'RUNNING'}, {'started_at': '2026-09-08T12:00:00Z'}, {'output_root': '/other'},
                       {'input_manifest_sha256': '0'*64}, {'role_id': 'architect'}):
            record = dict(original, **change)
            (self.out / 'RUN-RECORD.json').write_text(json.dumps(record))
            result = self.cli('--show-handoff', self.out)
            self.assertNotEqual(result.returncode, 0, change)
            self.assertNotIn('BEGIN REVIEWER PROMPT', result.stdout)

    def test_invalid_cli_options_do_not_create_files(self):
        for args in (('--pack', self.pack), ('--show-handoff', self.out, '--allow-unverified-isolation'),
                     ('--show-handoff', self.out, '--run-id', 'new'), ('--show-handoff', self.out, '--out', self.out)):
            result = self.cli(*args)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(self.out.exists())

    def test_unicode_paths_in_handoff(self):
        new_path = self.root / 'pakiet-żółć'
        self.pack.rename(new_path)
        self.pack = new_path
        prepare.prepare_run(self.pack, self.out, 'unicode', True)
        result = self.cli('--show-handoff', self.out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('pakiet-żółć', result.stdout)


if __name__ == '__main__':
    unittest.main()
