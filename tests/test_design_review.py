"""Offline tests. Real Git/export/preflight; Codex calls are simulated explicitly."""
from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('design', ROOT / 'scripts/design-review.py')
design = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(design)


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.DEVNULL).decode().strip()


def files(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}


class DesignReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.repo = self.base / 'repo'
        self.repo.mkdir()
        git(self.repo, 'init')
        git(self.repo, 'config', 'user.name', 'Offline fixture')
        git(self.repo, 'config', 'user.email', 'fixture@example.invalid')
        self.template = {'schema_version': '0.1', 'status': 'NOT_RUN', 'runtime': {},
                         'isolation': {}, 'measurements': {}, 'gate_decision': {'status': 'PENDING'}}
        fixture = {
            'workflow/bundles.json': json.dumps({'source_sha': 'b' * 40, 'bundles': {
                'independent-design': {'task': 'prompts/07-independent-design.md', 'inputs': ['docs/project-brief.md']},
                'design-review': {'task': 'prompts/08-design-review.md', 'inputs': ['docs/project-brief.md', 'docs/experiment-plan.md']}}}),
            'templates/run-record.json': json.dumps(self.template),
            'docs/project-brief.md': 'Neutral brief\n',
            'docs/experiment-plan.md': 'Process A, not a verdict\n',
            'prompts/07-independent-design.md': 'Design independently.\n',
            'prompts/08-design-review.md': (ROOT / 'prompts/08-design-review.md').read_text(),
            'sources/secret-plan.md': 'Do not expose historical material',
            'docs/presentation-journal.md': 'Do not expose the coordinator opinion',
            '.gitignore': '__pycache__/\n*.pyc\n',
        }
        for name, text in fixture.items():
            p = self.repo / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding='utf-8')
        shutil.copytree(ROOT / 'scripts', self.repo / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-m', 'process fixture')
        self.process_sha = git(self.repo, 'rev-parse', 'HEAD')
        self.oldpack = self.base / 'old-pack'
        self.prior = self.base / design.DEFAULT_PRIOR
        exporter = design.module('build-context-pack.py')
        helper = design.module('prepare-review-run.py')
        exporter.build_pack(self.repo, 'independent-design', self.oldpack)
        record = helper.prepare_run(self.oldpack, self.prior, 'first-design', True)
        self.report = 'EXPLORATORY; INDEPENDENCE UNVERIFIED\n\nAlternative design; UTF-8: żółć.\n'.encode()
        (self.prior / 'independent-design.md').write_bytes(self.report)
        record.update({'status': 'COMPLETE', 'started_at': '2026-09-08T15:44:56Z',
                       'ended_at': '2026-09-08T16:00:31Z', 'output_artifacts': [
                           {'path': 'independent-design.md', 'sha256': design.sha(self.report)}]})
        self.save_prior(record)
        self.record = record
        self.dest = self.base / 'attempts'

    def tearDown(self):
        self.temp.cleanup()

    def save_prior(self, record):
        (self.prior / 'RUN-RECORD.json').write_bytes(design.json_bytes(record))

    def prepare(self, **kwargs):
        options = {'allow': True}
        options.update(kwargs)
        return design.prepare(self.repo, self.prior, self.dest, **options)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(self.repo / 'scripts/design-review.py'), *map(str, args)],
                              capture_output=True, text=True, encoding='utf-8')

    def test_real_exporter_freezes_both_proposals(self):
        run = self.prepare()
        record, prompt = design.verify_run(run)
        self.assertEqual((run / 'input/input/prior/independent-design.md').read_bytes(), self.report)
        self.assertEqual(record['process_sha'], self.process_sha)
        self.assertEqual(record['prior_run_id'], 'first-design')
        self.assertIn('Both proposals', prompt)
        names = set(files(run / 'input'))
        self.assertIn('input/docs/experiment-plan.md', names)
        self.assertFalse(any('sources/' in name or 'journal' in name or name.startswith('.git/') for name in names))

    def test_prior_and_old_inputs_unchanged(self):
        before = files(self.prior), files(self.oldpack)
        self.prepare()
        self.assertEqual(before, (files(self.prior), files(self.oldpack)))

    def test_preparation_not_execution_or_gate_approval(self):
        run = self.prepare()
        record, _ = design.verify_run(run)
        self.assertEqual(record['status'], 'PREPARED')
        self.assertIsNone(record['started_at'])
        self.assertIsNone(record['ended_at'])
        self.assertIsNone(record['source_sha'])
        self.assertEqual(record['gate_decision']['status'], 'PENDING')
        self.assertFalse(record['isolation_verified'])
        self.assertEqual(record['launcher']['status'], 'NOT_LAUNCHED')
        self.assertFalse((run / 'output/design-review.md').exists())

    def test_default_has_no_implicit_authorization(self):
        run = self.prepare(allow=False)
        record, prompt = design.verify_run(run)
        self.assertEqual(record['preflight']['status'], 'BLOCKED_ENVIRONMENT')
        self.assertIn('Execution is NOT authorized', prompt)
        with self.assertRaises(ValueError):
            design.launch(run, '/fake/codex')

    def test_fresh_ids_and_directories(self):
        one, two = self.prepare(), self.prepare()
        self.assertNotEqual(one, two)
        self.assertTrue(one.name.startswith('phase0-design-review-'))
        self.assertTrue(one.exists())

    def test_existing_directory_is_never_overwritten(self):
        self.dest.mkdir()
        (self.dest / 'fixed').mkdir()
        with self.assertRaises(FileExistsError):
            self.prepare(run_id='fixed')
        self.assertEqual(list((self.dest / 'fixed').iterdir()), [])

    def test_missing_prior_has_actionable_file_error(self):
        (self.prior / 'RUN-RECORD.json').unlink()
        with self.assertRaisesRegex(ValueError, 'RUN-RECORD.json'):
            self.prepare()
        self.assertFalse(self.dest.exists())

    def test_blocked_or_unclosed_prior_is_not_success(self):
        for change in ({'status': 'BLOCKED'}, {'status': 'PREPARED'}, {'ended_at': None}, {'stage': 'architect'}):
            self.save_prior(dict(self.record, **change))
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.prepare()

    def test_hash_mismatch_prevents_pack_publication(self):
        (self.prior / 'independent-design.md').write_text('Changed')
        with self.assertRaisesRegex(ValueError, 'completion hash'):
            self.prepare()
        self.assertFalse(self.dest.exists())

    def test_no_silent_hash_reconstruction(self):
        self.save_prior(dict(self.record, output_artifacts=[]))
        with self.assertRaisesRegex(ValueError, 'output_artifacts'):
            self.prepare()

    def test_record_artifact_absolute_and_mapping_forms(self):
        for entries in ([{'path': str(self.prior / 'independent-design.md'), 'sha256': design.sha(self.report)}],
                        {'independent-design.md': design.sha(self.report)},
                        {'independent-design.md': {'sha256': design.sha(self.report)}}):
            self.save_prior(dict(self.record, output_artifacts=entries))
            data, _ = design.prior_snapshot(self.prior)
            self.assertEqual(data, self.report)

    def test_duplicate_or_wrong_path_hash_is_rejected(self):
        for entries in (self.record['output_artifacts'] * 2,
                        [{'path': 'unrelated/independent-design.md', 'sha256': design.sha(self.report)}]):
            self.save_prior(dict(self.record, output_artifacts=entries))
            with self.assertRaises(ValueError):
                self.prepare()

    def test_moved_closed_prior_keeps_original_identity(self):
        moved = self.base / 'moved'
        self.prior.rename(moved)
        _, provenance = design.prior_snapshot(moved)
        self.assertEqual(provenance['run_id'], self.record['run_id'])

    def test_raw_record_and_session_data_not_copied(self):
        self.save_prior(dict(self.record, commands=['secret command'], secret='sensitive-placeholder'))
        (self.prior / 'private-session.txt').write_text('Do not include')
        run = self.prepare()
        all_bytes = b''.join(files(run / 'input').values())
        self.assertNotIn(b'sensitive-placeholder', all_bytes)
        self.assertNotIn(b'secret command', all_bytes)
        self.assertNotIn(b'Do not include', all_bytes)
        provenance = json.loads((run / 'input/input/prior/provenance.json').read_bytes())
        self.assertFalse(provenance['original_manifest_rechecked'])
        self.assertFalse(provenance['reported_isolation_verified'])

    def test_new_input_modes_have_no_write_bits(self):
        run = self.prepare()
        for p in [run / 'input', *(run / 'input').rglob('*')]:
            self.assertEqual(p.stat().st_mode & 0o222, 0)
        self.assertTrue((run / 'output/RUN-RECORD.json').stat().st_mode & 0o200)

    def test_symlink_prior_and_ancestor_rejected(self):
        linked = self.base / 'link'
        linked.symlink_to(self.prior, target_is_directory=True)
        for path in (linked, linked / 'nested'):
            with self.assertRaises(ValueError):
                design.absolute(path)

    def test_symlink_report_rejected(self):
        (self.prior / 'independent-design.md').unlink()
        (self.prior / 'independent-design.md').symlink_to(self.oldpack / 'TASK.md')
        with self.assertRaises(ValueError):
            self.prepare()

    def test_dirty_checkout_is_not_silently_exported(self):
        (self.repo / 'docs/experiment-plan.md').write_text('uncommitted')
        with self.assertRaisesRegex(ValueError, 'local changes'):
            self.prepare()
        self.assertFalse(self.dest.exists())

    def test_invalid_ids_and_inside_repo_output(self):
        for identifier in ('../escape', '', 'a b'):
            if identifier == '':  # None/empty means generate, not a path traversal.
                continue
            with self.assertRaises(ValueError):
                self.prepare(run_id=identifier)
        with self.assertRaises(ValueError):
            design.prepare(self.repo, self.prior, self.repo / 'outputs', allow=True)

    def test_tampered_frozen_input_blocks_handoff(self):
        run = self.prepare()
        p = run / 'input/input/prior/independent-design.md'
        p.chmod(0o600)
        p.write_text('Tampered')
        with self.assertRaisesRegex(ValueError, 'hash/size'):
            design.handoff(run)

    def test_unlisted_input_blocks_handoff(self):
        run = self.prepare()
        (run / 'input').chmod(0o700)
        (run / 'input/opinion.txt').write_text('Coordinator opinion')
        with self.assertRaisesRegex(ValueError, 'Unexpected input'):
            design.handoff(run)

    def test_handoff_readonly_and_exact_prompt(self):
        run = self.prepare()
        before = files(run)
        text = design.handoff(run)
        prompt = text.split('----- BEGIN REVIEWER PROMPT -----\n')[1].split('----- END REVIEWER PROMPT -----')[0]
        self.assertEqual(prompt, (run / 'output/START-REVIEW.txt').read_text())
        self.assertEqual(files(run), before)

    def test_stale_record_prompt_or_profile_blocks(self):
        for name in ('START-REVIEW.txt', 'PROFILE.toml'):
            run = self.prepare()
            with (run / 'output' / name).open('a') as stream:
                stream.write('changed')
            with self.assertRaises(ValueError):
                design.handoff(run)
        run = self.prepare()
        p = run / 'output/RUN-RECORD.json'
        rec = json.loads(p.read_bytes())
        rec['isolation_verified'] = True
        p.write_bytes(design.json_bytes(rec))
        with self.assertRaises(ValueError):
            design.handoff(run)

    def test_used_run_is_not_restarted(self):
        run = self.prepare()
        p = run / 'output/RUN-RECORD.json'
        rec = json.loads(p.read_bytes())
        rec['launcher']['status'] = 'LOGIN_FAILED'
        p.write_bytes(design.json_bytes(rec))
        with self.assertRaisesRegex(ValueError, 'used/attempted'):
            design.launch(run, '/fake/codex')

    def test_profile_preserves_controls_and_has_no_escalation(self):
        try:
            import tomllib
        except ImportError:
            self.skipTest('Optional TOML parsing check requires Python 3.11+; launcher supports 3.10')
        config = tomllib.loads(design.profile_config('model-from-client', 'high'))
        self.assertEqual(config['approval_policy'], 'never')
        self.assertEqual(config['sandbox_mode'], 'workspace-write')
        self.assertFalse(config['features']['multi_agent'])
        self.assertFalse(config['features']['memories'])
        self.assertEqual(config['forced_login_method'], 'chatgpt')
        self.assertEqual(config['model'], 'model-from-client')

    def test_cli_defaults_select_explicit_prior_not_latest(self):
        bad = self.base / 'phase0-independent-later-output'
        bad.mkdir()
        result = self.cli('--allow-unverified-isolation')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('BEGIN REVIEWER PROMPT', result.stdout)
        self.assertIn('No model has been started', result.stdout)
        created = list(self.base.glob('phase0-design-review-*'))
        self.assertEqual(len(created), 1)
        self.assertEqual(json.loads((created[0] / 'output/RUN-RECORD.json').read_bytes())['prior_run_id'], 'first-design')

    def test_cli_show_and_conflicting_options(self):
        run = self.prepare()
        result = self.cli('--show-handoff', run)
        self.assertEqual(result.returncode, 0, result.stderr)
        invalid = self.cli('--show-handoff', run, '--allow-unverified-isolation')
        self.assertNotEqual(invalid.returncode, 0)

    def test_real_local_git_update_reexec_preserves_prior(self):
        remote = self.base / 'remote.git'
        subprocess.run(['git', 'init', '--bare', str(remote)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        git(self.repo, 'remote', 'add', 'origin', str(remote))
        branch = git(self.repo, 'branch', '--show-current')
        git(self.repo, 'push', '-u', 'origin', branch)
        checkout = self.base / 'checkout'
        subprocess.run(['git', 'clone', str(remote), str(checkout)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        (self.repo / 'docs/experiment-plan.md').write_text('New committed process version\n')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-m', 'updated process fixture')
        git(self.repo, 'push')
        new_sha = git(self.repo, 'rev-parse', 'HEAD')
        before = files(self.prior), files(self.oldpack)
        result = subprocess.run([sys.executable, str(checkout / 'scripts/design-review.py'),
                                 '--update', '--allow-unverified-isolation', '--output-parent', str(self.dest)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(git(checkout, 'rev-parse', 'HEAD'), new_sha)
        created = list(self.dest.iterdir())
        self.assertEqual(len(created), 1)
        rec = json.loads((created[0] / 'output/RUN-RECORD.json').read_bytes())
        self.assertEqual(rec['process_sha'], new_sha)
        self.assertEqual(before, (files(self.prior), files(self.oldpack)))
        self.assertIn('BEGIN REVIEWER PROMPT', result.stdout)

    def test_cli_no_launch_without_tty_and_authorization(self):
        for args in (('--launch',), ('--launch', '--allow-unverified-isolation')):
            result = self.cli(*args)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(list(self.base.glob('phase0-design-review-*')))

    def simulate(self, run, *, login_failure=False, change_input=False, complete=True, sandbox_failure=False):
        calls, homes = [], []
        def call(argv, **kwargs):
            calls.append(argv)
            homes.append(Path(kwargs['env']['HOME']))
            self.assertNotIn('OPENAI_API_KEY', kwargs['env'])
            self.assertNotEqual(kwargs['env']['HOME'], os.environ.get('HOME'))
            self.assertEqual(kwargs['cwd'], run / 'output')
            if argv[1] == '--version':
                return subprocess.CompletedProcess(argv, 0, 'codex-fixture-ONLY\n', '')
            if argv[1] == 'login':
                if change_input:
                    p = run / 'input/TASK.md'
                    p.chmod(0o600)
                    p.write_text('changed during login')
                return subprocess.CompletedProcess(argv, 1 if login_failure else 0)
            self.assertEqual(argv[-1], (run / 'output/START-REVIEW.txt').read_text())
            self.assertIn('never', argv)
            self.assertNotIn('resume', argv)
            self.assertNotIn('--dangerously-bypass-approvals-and-sandbox', argv)
            if complete:
                p = run / 'output/RUN-RECORD.json'
                record = json.loads(p.read_bytes())
                record.update({'status': 'COMPLETE', 'started_at': '2026-09-08T20:00:00Z',
                               'ended_at': '2026-09-08T20:01:00Z', 'output_artifacts': []})
                for name in (design.REPORT, design.PROPOSAL):
                    data = ('Test-only ' + name).encode()
                    (run / 'output' / name).write_bytes(data)
                    record['output_artifacts'].append({'path': name, 'sha256': design.sha(data)})
                p.write_bytes(design.json_bytes(record))
            return subprocess.CompletedProcess(argv, 1 if sandbox_failure else 0)
        with patch('subprocess.run', side_effect=call), redirect_stdout(io.StringIO()):
            result = design.launch(run, '/fake/codex')
        return result, calls, homes

    def test_simulated_launch_auto_submits_and_validates_outputs(self):
        run = self.prepare()
        before = files(run / 'input')
        result, calls, homes = self.simulate(run)
        self.assertEqual(result, 0)
        self.assertEqual(len(calls), 3)
        self.assertTrue(all(not h.exists() for h in homes))
        self.assertEqual(files(run / 'input'), before)
        record = json.loads((run / 'output/RUN-RECORD.json').read_bytes())
        self.assertEqual(record['status'], 'COMPLETE')
        self.assertEqual(record['gate_decision']['status'], 'PENDING')

    def test_failed_login_never_starts_model(self):
        run = self.prepare()
        result, calls, homes = self.simulate(run, login_failure=True)
        self.assertEqual(result, 1)
        self.assertEqual(len(calls), 2)
        self.assertTrue(all(not h.exists() for h in homes))
        self.assertFalse((run / 'output/design-review.md').exists())

    def test_changed_inputs_during_login_block(self):
        run = self.prepare()
        with self.assertRaisesRegex(ValueError, 'hash/size'):
            self.simulate(run, change_input=True)
        self.assertFalse((run / 'output/design-review.md').exists())

    def test_client_exit_alone_is_not_completion(self):
        run = self.prepare()
        result, _, _ = self.simulate(run, complete=False)
        self.assertEqual(result, 3)
        record = json.loads((run / 'output/RUN-RECORD.json').read_bytes())
        self.assertEqual(record['status'], 'PREPARED')

    def test_sandbox_failure_has_no_fallback(self):
        run = self.prepare()
        result, calls, _ = self.simulate(run, complete=False, sandbox_failure=True)
        self.assertEqual(result, 1)
        self.assertEqual(len(calls), 3)
        self.assertFalse((run / 'output/design-review.md').exists())


if __name__ == '__main__':
    unittest.main()
