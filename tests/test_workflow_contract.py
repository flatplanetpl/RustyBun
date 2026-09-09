"""Check the shipped process contract and real input packs offline, without a runner."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from test_context_pack import git, initialize, pack
from test_prepare_review_run import prepare

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = 'docs/decisions/2026-09-09-pilot-v0.2.md'


def read_json(name):
    return json.loads((ROOT / name).read_bytes())


class WorkflowContractTests(unittest.TestCase):
    def setUp(self):
        self.bundles = read_json('workflow/bundles.json')['bundles']

    def test_bundles_preserve_context_boundaries_and_repository_inputs_exist(self):
        for kind, bundle in self.bundles.items():
            self.assertEqual(len(bundle['inputs']), len(set(bundle['inputs'])))
            for name in bundle['inputs']:
                self.assertTrue((ROOT / name).is_file(), name)
                self.assertNotIn('presentation-journal', name)
                if kind != 'comparative-review':
                    self.assertFalse(name.startswith('sources/'), name)
        self.assertEqual(self.bundles['independent-design']['inputs'], ['docs/project-brief.md'])
        self.assertNotIn(DECISIONS, self.bundles['architect']['inputs'])
        for kind in ('design-review', 'comparative-review'):
            self.assertIn(DECISIONS, self.bundles[kind]['inputs'])
            self.assertIn('tests/test_process_contract.py', self.bundles[kind]['inputs'])
            self.assertNotIn('tests/test_workflow_contract.py', self.bundles[kind]['inputs'])


class CurrentPackIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / 'repo'
        initialize(self.repo)
        config = read_json('workflow/bundles.json')
        names = {'workflow/bundles.json', 'templates/run-record.json'}
        for kind in ('independent-design', 'design-review', 'comparative-review'):
            names.update(config['bundles'][kind]['inputs'])
            names.add(config['bundles'][kind]['task'])
        for name in names:
            destination = self.repo / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, destination)
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-m', 'Offline copy of current process inputs')

    def run_process_contract(self, input_root):
        self.assertTrue((input_root / 'tests/test_process_contract.py').is_file())
        return subprocess.run(
            [sys.executable, '-I', '-B', '-m', 'unittest', 'discover',
             '-s', 'tests', '-p', 'test_process_contract.py', '-v'],
            cwd=input_root, capture_output=True, text=True, timeout=30)

    def test_exported_process_contract_runs_without_repository_context(self):
        for kind in ('design-review', 'comparative-review'):
            with self.subTest(kind=kind):
                out = self.base / kind
                pack.build_pack(self.repo, kind, out)
                before = {p.relative_to(out): p.read_bytes()
                          for p in out.rglob('*') if p.is_file()}
                result = self.run_process_contract(out / 'input')
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertNotIn('Ran 0 tests', result.stderr)
                after = {p.relative_to(out): p.read_bytes()
                         for p in out.rglob('*') if p.is_file()}
                self.assertEqual(before, after)

    def test_current_review_packs_export_committed_v02_with_valid_hashes(self):
        for kind in ('design-review', 'comparative-review'):
            with self.subTest(kind=kind):
                out = self.base / kind
                manifest = pack.build_pack(self.repo, kind, out)
                self.assertEqual(manifest['schema_version'], '0.1')
                self.assertFalse(manifest['isolation_verified'])
                inputs = {p.relative_to(out / 'input').as_posix()
                          for p in (out / 'input').rglob('*') if p.is_file()}
                self.assertEqual(inputs, set(read_json('workflow/bundles.json')['bundles'][kind]['inputs']))
                for item in manifest['files']:
                    self.assertEqual(hashlib.sha256((out / item['path']).read_bytes()).hexdigest(),
                                     item['sha256'])
                self.assertEqual((out / 'input/workflow/pipeline.json').read_bytes(),
                                 (ROOT / 'workflow/pipeline.json').read_bytes())
                self.assertEqual((out / 'input' / DECISIONS).read_bytes(), (ROOT / DECISIONS).read_bytes())
                self.assertEqual(json.loads((out / 'RUN-RECORD.template.json').read_bytes())['schema_version'], '0.2')

    def assert_mutation_rejected(self, name, mutate, expected_errors, expected_test):
        for kind in ('design-review', 'comparative-review'):
            with self.subTest(kind=kind, mutation=name):
                out = self.base / f'{kind}-{name}'
                pack.build_pack(self.repo, kind, out)
                mutated = self.base / f'{kind}-{name}-mutated'
                shutil.copytree(out / 'input', mutated)
                mutate(mutated)
                result = self.run_process_contract(mutated)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                for expected_error in expected_errors:
                    self.assertIn(expected_error, result.stderr)
                self.assertIn(expected_test, result.stderr)
                self.assertNotIn('Ran 0 tests', result.stderr)

    def test_exported_contract_rejects_missing_required_files(self):
        for name in ('workflow/pipeline.json', 'workflow/bundles.json',
                     'templates/migration-unit.json', 'templates/run-record.json'):
            self.assert_mutation_rejected(
                Path(name).stem, lambda root: (root / name).unlink(),
                ('FileNotFoundError: [Errno 2] No such file or directory:', f"/{name}'"),
                'ERROR: test_active_contract_versions_and_pending_gates')

    def test_exported_contract_rejects_optional_review(self):
        for name, field, test in (
                ('workflow/pipeline.json', 'review_policy',
                 'test_one_sequential_slice_without_mandatory_separate_reviewers'),
                ('templates/migration-unit.json', 'review',
                 'test_protocol_and_negative_controls_are_requirements_not_results')):
            def mutate(root):
                path = root / name
                data = json.loads(path.read_bytes())
                data[field]['required'] = False
                path.write_text(json.dumps(data))

            self.assert_mutation_rejected(Path(name).stem, mutate,
                                          ('AssertionError: False is not true',), f'FAIL: {test}')

    def test_exported_contract_rejects_two_writers(self):
        def mutate(root):
            path = root / 'workflow/pipeline.json'
            data = json.loads(path.read_bytes())
            data['limits']['max_active_writers'] = 2
            path.write_text(json.dumps(data))

        self.assert_mutation_rejected(
            'two-writers', mutate, ('AssertionError: 2 != 1',),
            'FAIL: test_one_sequential_slice_without_mandatory_separate_reviewers')

    def assert_prerequisite_required(self, prerequisite):
        for stage_id in ('planner', 'implementer', 'referee'):
            def mutate(root):
                path = root / 'workflow/pipeline.json'
                data = json.loads(path.read_bytes())
                stage = next(stage for stage in data['stages'] if stage['id'] == stage_id)
                stage['requires'].remove(prerequisite)
                path.write_text(json.dumps(data))

            self.assert_mutation_rejected(
                stage_id, mutate, (f"AssertionError: '{prerequisite}' not found",),
                'FAIL: test_baseline_and_verifier_precede_g3_and_implementation')

    def test_exported_contract_requires_baseline_before_implementation(self):
        self.assert_prerequisite_required('baseline:validated')

    def test_exported_contract_requires_verifier_before_implementation(self):
        self.assert_prerequisite_required('verifier:validated')

    def test_preflight_preserves_actual_v02_metadata_without_starting_a_run(self):
        out = self.base / 'independent-pack'
        manifest = pack.build_pack(self.repo, 'independent-design', out)
        before = {item['path']: (out / item['path']).read_bytes() for item in manifest['files']}
        record = prepare.prepare_run(out, self.base / 'output', 'offline-v02', False)
        template = read_json('templates/run-record.json')
        self.assertEqual(record['schema_version'], '0.2')
        for key in ('budget', 'review', 'interventions', 'checkpoint', 'session'):
            self.assertEqual(record[key], template[key])
        self.assertEqual(record['status'], 'PREPARED')
        self.assertEqual(record['gate_decision']['status'], 'PENDING')
        self.assertEqual(record['preflight']['status'], 'BLOCKED_ENVIRONMENT')
        self.assertIsNone(record['started_at'])
        self.assertEqual(before, {name: (out / name).read_bytes() for name in before})
        self.assertFalse((out / 'input' / DECISIONS).exists())


if __name__ == '__main__':
    unittest.main()
