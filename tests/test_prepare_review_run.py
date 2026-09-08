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


if __name__ == '__main__':
    unittest.main()
