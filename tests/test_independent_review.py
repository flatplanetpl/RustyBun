"""Offline launcher tests. Codex/authentication are simulated; no model or service is used."""
import contextlib
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

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/independent-review.py'
SPEC = importlib.util.spec_from_file_location('independent_review', SCRIPT)
launcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launcher)


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.pack = self.root / 'pakiet-żółć'
        self.pack.mkdir()
        contents = {
            'TASK.md': 'Design from the neutral brief only.\n',
            'AGENTS.md': 'Only read listed inputs; supply a run record.\n',
            'input/docs/project-brief.md': 'Neutral brief.\n',
            'RUN-RECORD.template.json': json.dumps({
                'status': 'NOT_RUN', 'runtime': {}, 'isolation': {},
                'measurements': {'wall_seconds': None}, 'gate_decision': {}}),
        }
        manifest = {'kind': 'independent-design', 'process_sha': 'a'*40,
                    'source_sha': None, 'files': []}
        for name, text in contents.items():
            p = self.pack / name
            p.parent.mkdir(parents=True, exist_ok=True)
            data = text.encode()
            p.write_bytes(data)
            manifest['files'].append({'path': name, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
        (self.pack / 'MANIFEST.json').write_text(json.dumps(manifest))
        self.before = {str(p.relative_to(self.pack)): p.read_bytes() for p in self.pack.rglob('*') if p.is_file()}
        self.calls = []
        self.profile = None

    def tearDown(self):
        self.temp.cleanup()

    def prepare(self, run_id='test-run', allow=True):
        return launcher.prepare_trial(self.pack, self.root / 'outputs', run_id, allow, None, None)[0]

    def record(self, out):
        return json.loads((out / 'RUN-RECORD.json').read_bytes())

    def fake_codex(self, cmd, **kw):
        self.calls.append((cmd, kw))
        self.profile = Path(kw['env']['HOME'])
        config = (self.profile / '.codex/config.toml').read_text()
        self.assertIn('forced_login_method = "chatgpt"', config)
        self.assertIn('cli_auth_credentials_store = "file"', config)
        self.assertIn('use_memories = false', config)
        self.assertIn('project_root_markers = []', config)
        self.assertEqual(self.profile.stat().st_mode & 0o777, 0o700)
        self.assertNotEqual(kw['cwd'], launcher.ROOT)
        for key in ('OPENAI_API_KEY', 'CODEX_API_KEY', 'CODEX_THREAD_ID', 'NODE_OPTIONS', 'PYTHONPATH', 'BASH_ENV'):
            self.assertNotIn(key, kw['env'])
        self.assertNotIn('resume', cmd)
        self.assertNotIn('fork', cmd)
        return subprocess.CompletedProcess(cmd, 0, 'codex-fixture 0.0\n', '')

    def test_default_preparation_is_offline_and_keeps_inputs(self):
        with patch.object(launcher.subprocess, 'run', side_effect=AssertionError('Unexpected process')):
            out, handoff = launcher.prepare_trial(self.pack, self.root, None, False, None, None)
        self.assertTrue(out.is_dir())
        self.assertIn('BEGIN REVIEWER PROMPT', handoff)
        self.assertIn('BLOCKED_ENVIRONMENT', handoff)
        self.assertEqual(self.record(out)['status'], 'PREPARED')
        self.assertEqual(self.record(out)['launcher']['status'], 'NOT_LAUNCHED')
        self.assertFalse(self.record(out)['isolation_verified'])
        self.assertIsNone(self.record(out)['started_at'])
        self.assertFalse((out / 'independent-design.md').exists())
        after = {str(p.relative_to(self.pack)): p.read_bytes() for p in self.pack.rglob('*') if p.is_file()}
        self.assertEqual(self.before, after)

    def test_auto_names_are_distinct_and_keep_pinned_process(self):
        first = self.prepare(None)
        second = self.prepare(None)
        self.assertNotEqual(first, second)
        self.assertEqual(self.record(first)['process_sha'], self.record(second)['process_sha'])
        self.assertEqual(self.record(first)['input_manifest_sha256'], self.record(second)['input_manifest_sha256'])

    def test_output_collision_does_not_overwrite(self):
        out = self.prepare()
        original = (out / 'RUN-RECORD.json').read_bytes()
        with self.assertRaises(FileExistsError):
            self.prepare()
        self.assertEqual(original, (out / 'RUN-RECORD.json').read_bytes())

    def test_bad_pack_and_invalid_id_do_not_create_output(self):
        with self.assertRaises(ValueError):
            self.prepare('../bad')
        (self.pack / 'TASK.md').write_text('changed')
        with self.assertRaises(ValueError):
            self.prepare()
        self.assertFalse((self.root / 'outputs').exists())

    def test_output_inside_main_checkout_is_rejected(self):
        with self.assertRaises(ValueError):
            launcher.prepare_trial(self.pack, launcher.ROOT, 'bad-place', True, None, None)

    def test_environment_drops_keys_state_and_relative_path_entries(self):
        parent = {'PATH': '.:/usr/bin::relative:/opt/node/bin', 'LANG': 'pl_PL.UTF-8',
                  'HOME': '/old', 'CODEX_HOME': '/old/.codex', 'OPENAI_API_KEY': 'fixture',
                  'CODEX_API_KEY': 'fixture', 'XDG_CONFIG_HOME': '/old/.config',
                  'CODEX_THREAD_ID': 'old-thread', 'NODE_OPTIONS': '--require old',
                  'PYTHONPATH': '/old/inject', 'BASH_ENV': '/old/bash', 'HTTPS_PROXY': 'fixture'}
        env = launcher.profile_environment(Path('/fresh'), parent)
        self.assertEqual(env['PATH'], '/usr/bin:/opt/node/bin')
        self.assertEqual(env['HOME'], '/fresh')
        self.assertEqual(env['CODEX_HOME'], '/fresh/.codex')
        self.assertEqual(env['XDG_CONFIG_HOME'], '/fresh/.config')
        for name in ('OPENAI_API_KEY', 'CODEX_API_KEY', 'CODEX_THREAD_ID', 'NODE_OPTIONS', 'PYTHONPATH', 'BASH_ENV', 'HTTPS_PROXY'):
            self.assertNotIn(name, env)
        self.assertEqual(parent['HOME'], '/old')

    def test_config_has_requested_not_fabricated_model(self):
        self.assertNotIn('model =', launcher.profile_config(None, None))
        self.assertIn('model = "client-model"', launcher.profile_config('client-model', 'high'))
        self.assertIn('model_reasoning_effort = "high"', launcher.profile_config('client-model', 'high'))
        for val in ('', 'name\nnew-line'):
            with self.assertRaises(ValueError):
                launcher.profile_config(val, None)

    def test_config_is_valid_toml_when_parser_is_available(self):
        try:
            import tomllib
        except ImportError:
            self.skipTest('tomllib requires Python 3.11; launcher supports 3.10')
        cfg = tomllib.loads(launcher.profile_config('model-with-"quote', 'high'))
        self.assertEqual(cfg['model'], 'model-with-"quote')
        self.assertFalse(cfg['features']['apps'])
        self.assertFalse(cfg['features']['memories'])
        self.assertFalse(cfg['memories']['generate_memories'])
        self.assertFalse(cfg['sandbox_workspace_write']['network_access'])

    def test_launch_opens_new_profile_and_preserves_task_status(self):
        out = self.prepare()
        with patch.object(launcher.subprocess, 'run', side_effect=self.fake_codex), contextlib.redirect_stdout(io.StringIO()):
            code = launcher.launch_codex(out, '/fake/codex', None, None)
        self.assertEqual(code, 0)
        self.assertEqual([x[0][1:] for x in self.calls], [
            ['--version'], ['login', '--device-auth'],
            ['--sandbox', 'workspace-write', '--ask-for-approval', 'on-request', '--no-alt-screen']])
        self.assertTrue(all(x[1]['cwd'] == out for x in self.calls))
        self.assertFalse(self.profile.exists())
        record = self.record(out)
        self.assertEqual(record['status'], 'PREPARED')
        self.assertEqual(record['gate_decision']['status'], 'PENDING')
        self.assertFalse(record['isolation_verified'])
        self.assertEqual(record['launcher']['status'], 'CLIENT_EXITED')
        self.assertEqual(record['launcher']['client_version_observed'], 'codex-fixture 0.0')
        self.assertTrue(record['launcher']['temporary_profile_removed'])
        self.assertFalse((out / 'independent-design.md').exists())

    def test_login_failure_does_not_start_model(self):
        out = self.prepare()
        def fail_login(cmd, **kw):
            result = self.fake_codex(cmd, **kw)
            if 'login' in cmd:
                result.returncode = 7
            return result
        with patch.object(launcher.subprocess, 'run', side_effect=fail_login), contextlib.redirect_stdout(io.StringIO()):
            code = launcher.launch_codex(out, '/fake/codex', None, None)
        self.assertEqual(code, 7)
        self.assertEqual(len(self.calls), 2)
        self.assertFalse(self.profile.exists())
        self.assertEqual(self.record(out)['launcher']['status'], 'LOGIN_FAILED')

    def test_launch_without_authorization_is_blocked(self):
        out = self.prepare(allow=False)
        with patch.object(launcher.subprocess, 'run') as process, self.assertRaises(ValueError):
            launcher.launch_codex(out, '/fake/codex', None, None)
        process.assert_not_called()

    def test_changed_inputs_during_login_block_client_start(self):
        out = self.prepare()
        def mutate(cmd, **kw):
            result = self.fake_codex(cmd, **kw)
            if 'login' in cmd:
                (self.pack / 'TASK.md').write_text('changed while waiting')
            return result
        with patch.object(launcher.subprocess, 'run', side_effect=mutate), contextlib.redirect_stdout(io.StringIO()), self.assertRaises(ValueError):
            launcher.launch_codex(out, '/fake/codex', None, None)
        self.assertEqual(len(self.calls), 2)
        self.assertFalse(self.profile.exists())

    def test_used_run_is_not_restarted(self):
        out = self.prepare()
        record = self.record(out)
        record['status'] = 'BLOCKED_ENVIRONMENT'
        (out / 'RUN-RECORD.json').write_text(json.dumps(record))
        with patch.object(launcher.subprocess, 'run') as process, self.assertRaises(ValueError):
            launcher.launch_codex(out, '/fake/codex', None, None)
        process.assert_not_called()

    def test_launcher_updates_do_not_erase_reviewer_results(self):
        out = self.prepare()
        record = self.record(out)
        record['status'] = 'BLOCKED_ENVIRONMENT'
        record['limitations'].append('Simulated reviewer context observation')
        (out / 'RUN-RECORD.json').write_text(json.dumps(record))
        launcher.update_launcher_record(out, {'status': 'CLIENT_EXITED'})
        self.assertEqual(self.record(out)['status'], 'BLOCKED_ENVIRONMENT')
        self.assertIn('Simulated reviewer context observation', self.record(out)['limitations'])

    def test_cli_is_one_command_for_preparation(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--pack', str(self.pack),
                                 '--output-parent', str(self.root), '--allow-unverified-isolation'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        outputs = list(self.root.glob('phase0-independent-*-output'))
        self.assertEqual(len(outputs), 1)
        self.assertIn('BEGIN REVIEWER PROMPT', result.stdout)
        self.assertIn('Preparation only', result.stdout)

    def test_cli_launch_needs_explicit_consent_and_terminal(self):
        for flags in (['--launch'], ['--launch', '--allow-unverified-isolation']):
            result = subprocess.run([sys.executable, str(SCRIPT), '--pack', str(self.pack),
                                     '--output-parent', str(self.root), *flags], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
        self.assertFalse(list(self.root.glob('phase0-independent-*-output')))

    def test_update_refuses_dirty_checkout_before_pull(self):
        with patch.object(launcher, 'git', side_effect=[str(self.root), ' M README.md']) as git_call:
            with self.assertRaises(ValueError):
                launcher.update_checkout(self.root)
        self.assertNotIn('pull', str(git_call.call_args_list))

    def test_update_uses_ff_only_and_has_no_reset_or_stash(self):
        with patch.object(launcher, 'git', side_effect=[str(self.root), '', 'main', 'Already up to date.']) as git_call, contextlib.redirect_stdout(io.StringIO()):
            launcher.update_checkout(self.root)
        self.assertEqual(git_call.call_args_list[-1].args, (self.root, 'pull', '--ff-only'))
        self.assertNotIn('reset', str(git_call.call_args_list))
        self.assertNotIn('stash', str(git_call.call_args_list))

    def test_update_reexecutes_with_original_options_without_update(self):
        class Reexec(Exception):
            pass
        with patch.object(launcher, 'update_checkout') as update, patch.object(launcher.os, 'execv', side_effect=Reexec) as execv:
            with self.assertRaises(Reexec):
                launcher.main(['--update', '--pack', str(self.pack), '--allow-unverified-isolation'])
        update.assert_called_once_with(launcher.ROOT)
        new_args = execv.call_args.args[1]
        self.assertNotIn('--update', new_args)
        self.assertIn(str(self.pack), new_args)
        self.assertIn('--allow-unverified-isolation', new_args)

    def test_update_failure_does_not_prepare_or_launch(self):
        with patch.object(launcher, 'update_checkout', side_effect=RuntimeError('FF-only refused')), patch.object(launcher, 'prepare_trial') as prepare, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(launcher.main(['--update']), 1)
        prepare.assert_not_called()


if __name__ == '__main__':
    unittest.main()
