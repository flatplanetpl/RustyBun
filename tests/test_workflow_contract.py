"""Check the shipped process contract and real input packs offline, without a runner."""
import hashlib
import json
from pathlib import Path
import shutil
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
        self.pipeline = read_json('workflow/pipeline.json')
        self.bundles = read_json('workflow/bundles.json')['bundles']
        self.unit = read_json('templates/migration-unit.json')
        self.record = read_json('templates/run-record.json')
        self.stages = {stage['id']: stage for stage in self.pipeline['stages']}

    def test_active_contract_versions_and_pending_gates(self):
        for name in ('workflow/pipeline.json', 'workflow/bundles.json',
                     'templates/migration-unit.json', 'templates/run-record.json'):
            with self.subTest(path=name):
                self.assertEqual(read_json(name)['schema_version'], '0.2')
        self.assertFalse(self.pipeline['executable_runner'])
        for gate in self.pipeline['gates'].values():
            self.assertEqual(gate['status'], 'PENDING')
            self.assertIsNone(gate['approved_by'])
            self.assertEqual(gate['artifact_hashes'], [])

    def test_one_sequential_slice_without_mandatory_separate_reviewers(self):
        execution = self.pipeline['execution']
        self.assertEqual(execution['mode'], 'sequential')
        self.assertEqual(execution['main_working_sessions'], 1)
        self.assertEqual(execution['max_units'], 1)
        self.assertEqual(self.pipeline['limits']['max_active_writers'], 1)
        self.assertNotIn('reviewer_instances', self.pipeline['limits'])
        self.assertIn('review', self.stages)
        self.assertTrue(self.pipeline['review_policy']['required'])
        for old_stage in ('review-A', 'review-B', 'architecture-review'):
            self.assertNotIn(old_stage, self.stages)
        self.assertNotIn('bundle', self.stages['architect'])
        self.assertEqual(self.stages['architect']['gate_after'], 'G2')

    def test_baseline_and_verifier_precede_g3_and_implementation(self):
        self.assertIn('G2:approved', self.stages['baseline-verifier']['requires'])
        for stage in ('planner', 'implementer', 'referee'):
            with self.subTest(stage=stage):
                required = self.stages[stage]['requires']
                self.assertIn('baseline:validated', required)
                self.assertIn('verifier:validated', required)
        self.assertEqual(self.stages['planner']['gate_after'], 'G3')
        required = self.stages['implementer']['requires']
        for prerequisite in ('G3:approved', 'protocol:frozen',
                             'review-plan:approved', 'budget:approved', 'verification-reserve:available'):
            self.assertIn(prerequisite, required)
        order = list(self.stages)
        self.assertLess(order.index('baseline-verifier'), order.index('planner'))
        self.assertLess(order.index('planner'), order.index('implementer'))

    def test_review_and_retests_follow_candidate_changes(self):
        self.assertEqual(self.stages['fixer']['next'], 'review')
        self.assertIn('verification-reserve:available', self.stages['fixer']['requires'])
        self.assertIn('findings:confirmed', self.stages['fixer']['requires'])
        self.assertIn('review:frozen', self.stages['fixer']['requires'])
        self.assertIn('candidate:reviewed', self.stages['referee']['requires'])
        self.assertIn('candidate:no-confirmed-blockers', self.stages['referee']['requires'])
        self.assertEqual(self.pipeline['review_policy']['candidate_hash_must_match'], True)

    def test_comparative_review_remains_before_g1(self):
        comparative = self.stages['method-comparative']
        self.assertEqual(comparative['gate_after'], 'G1')
        self.assertIn('method-review:frozen', comparative['requires'])
        self.assertIn('G1:approved', self.stages['architect']['requires'])

    def test_budgets_have_unapproved_limits_and_reserves(self):
        budget = self.unit['budget']
        self.assertIsNone(self.pipeline['limits']['max_fix_rounds'])
        self.assertIsNone(budget['max_fix_rounds'])
        self.assertFalse(budget['approved'])
        self.assertIsNone(budget['approved_by'])
        for resource in ('wall_seconds', 'human_attention_minutes', 'model_resource'):
            self.assertIsNone(budget[resource]['limit'])
            self.assertIsNone(budget[resource]['verification_reserve'])
            self.assertIsNone(self.record['budget'][resource]['used'])
            self.assertIsNone(self.record['budget'][resource]['remaining'])
        self.assertIsNone(budget['model_resource']['unit'])
        self.assertIsNone(self.record['budget']['fix_rounds_used'])

    def test_protocol_and_negative_controls_are_requirements_not_results(self):
        verification = self.unit['verification']
        self.assertEqual(verification['owner'], 'Damian')
        self.assertEqual(verification['status'], 'NOT_RUN')
        self.assertEqual(verification['baseline_evidence'], [])
        self.assertEqual(verification['verifier_evidence'], [])
        self.assertEqual(verification['mutation_checks'], [])
        self.assertEqual(set(verification['negative_control_requirements']),
                         {'wrong_result', 'empty_test_set', 'missing_output',
                          'timeout', 'wrong_implementation'})
        for component in ('fixtures_sha256', 'tests_sha256', 'normalization_sha256',
                          'comparator_sha256', 'protocol_manifest_sha256'):
            self.assertIsNone(verification[component])
        self.assertTrue(self.unit['review']['required'])
        self.assertIsNone(self.unit['review']['kind'])
        self.assertIsNone(self.unit['review']['approved_by'])

    def test_checkpoint_has_no_fabricated_execution(self):
        checkpoint = self.record['checkpoint']
        for field in ('at', 'input_manifest_sha256', 'protocol_sha256',
                      'candidate_sha256', 'last_confirmed_state', 'next_allowed_action'):
            self.assertIsNone(checkpoint[field])
        self.assertEqual(checkpoint['evidence_artifacts'], [])
        self.assertEqual(checkpoint['open_findings'], [])
        self.assertEqual(checkpoint['budget_snapshot'], self.record['budget'])
        self.assertEqual(self.record['interventions'], [])
        self.assertIsNone(self.record['session']['previous_run_record_sha256'])
        self.assertEqual(self.record['status'], 'NOT_RUN')

    def test_pipeline_references_resolve_and_bundles_preserve_context_boundaries(self):
        tasks = self.pipeline['stages'] + self.pipeline['optional_tasks']
        self.assertEqual(len(tasks), len({task['id'] for task in tasks}))
        for task in tasks:
            self.assertTrue((ROOT / task['prompt']).is_file(), task['id'])
            if 'bundle' in task:
                self.assertEqual(self.bundles[task['bundle']]['task'], task['prompt'])
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
            self.assertIn('tests/test_workflow_contract.py', self.bundles[kind]['inputs'])


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

    def test_current_review_packs_export_committed_v02_with_valid_hashes(self):
        for kind in ('design-review', 'comparative-review'):
            with self.subTest(kind=kind):
                out = self.base / kind
                manifest = pack.build_pack(self.repo, kind, out)
                self.assertEqual(manifest['schema_version'], '0.1')
                self.assertFalse(manifest['isolation_verified'])
                for item in manifest['files']:
                    self.assertEqual(hashlib.sha256((out / item['path']).read_bytes()).hexdigest(),
                                     item['sha256'])
                self.assertEqual((out / 'input/workflow/pipeline.json').read_bytes(),
                                 (ROOT / 'workflow/pipeline.json').read_bytes())
                self.assertEqual((out / 'input' / DECISIONS).read_bytes(), (ROOT / DECISIONS).read_bytes())
                self.assertEqual(json.loads((out / 'RUN-RECORD.template.json').read_bytes())['schema_version'], '0.2')

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
