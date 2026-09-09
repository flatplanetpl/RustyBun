#!/usr/bin/env python3
"""Prepare a fresh independent-design run; optionally open a separate Codex CLI profile.

Default: no network, login or model. --update explicitly pulls this checkout.
--launch explicitly opens Codex and requires exploratory operator authorization.
This is profile separation, not a container or a proof of blind evaluation.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
CONFIG = '''# Fresh, per-run Codex profile. Requested controls, not verified isolation.
forced_login_method = "chatgpt"
cli_auth_credentials_store = "file"
web_search = "disabled"
project_root_markers = []
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[features]
memories = false
apps = false
multi_agent = false
shell_snapshot = false
skill_mcp_dependency_install = false

[memories]
use_memories = false
generate_memories = false

[apps._default]
enabled = false

[sandbox_workspace_write]
network_access = false
exclude_slash_tmp = true
exclude_tmpdir_env_var = true

[shell_environment_policy]
experimental_use_profile = false
'''


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def new_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    return f'phase0-independent-{stamp}-{uuid.uuid4().hex[:8]}'


def load_preparer():
    path = ROOT / 'scripts/prepare-review-run.py'
    spec = importlib.util.spec_from_file_location('rustybun_preparer', path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Cannot load preparation helper: {path}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(root: Path, *args: str) -> str:
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True,
                            text=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or 'Git failed')
    return result.stdout.strip()


def update_checkout(root: Path) -> None:
    if Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root.resolve():
        raise ValueError('--update requires the RustyBun checkout root')
    if git(root, 'status', '--porcelain', '--untracked-files=normal'):
        raise ValueError('--update refused: checkout has local changes; commit or handle them yourself')
    if not git(root, 'symbolic-ref', '--quiet', '--short', 'HEAD'):
        raise ValueError('--update requires a branch, not detached HEAD')
    print('Updating the launcher checkout with git pull --ff-only. Existing packs stay pinned.', flush=True)
    print(git(root, 'pull', '--ff-only'), flush=True)


def checked_option(value: str, name: str) -> str:
    if not value.strip() or any(ord(c) < 32 for c in value):
        raise ValueError(f'{name} must be a non-empty single-line value')
    return value


def profile_config(model: str | None, reasoning: str | None) -> str:
    lines = []
    if model is not None:
        lines.append('model = ' + json.dumps(checked_option(model, 'model')))
    if reasoning is not None:
        lines.append('model_reasoning_effort = ' + json.dumps(checked_option(reasoning, 'reasoning')))
    return '\n'.join(lines) + ('\n' if lines else '') + CONFIG


def profile_environment(home: Path, parent: dict[str, str]) -> dict[str, str]:
    # Do not pass API keys, inherited CODEX_*, XDG paths, agent/IDE metadata,
    # shell startup hooks or Python/Node injection variables to the new client.
    keep = ('TERM', 'COLORTERM', 'LANG', 'LC_ALL', 'LC_CTYPE', 'TZ', 'USER', 'LOGNAME')
    env = {key: parent[key] for key in keep if key in parent}
    paths = [p for p in parent.get('PATH', os.defpath).split(os.pathsep)
             if p and Path(p).is_absolute()]
    env['PATH'] = os.pathsep.join(paths) or os.defpath
    env.update({'HOME': str(home), 'CODEX_HOME': str(home / '.codex'),
                'XDG_CONFIG_HOME': str(home / '.config'), 'XDG_DATA_HOME': str(home / '.local/share'),
                'XDG_CACHE_HOME': str(home / '.cache'), 'XDG_STATE_HOME': str(home / '.local/state'),
                'SHELL': '/bin/bash', 'TMPDIR': '/tmp'})
    return env


def update_launcher_record(out: Path, fields: dict) -> None:
    """Update only launcher observations; preserve the agent's status and operator decisions."""
    path = out / 'RUN-RECORD.json'
    if path.is_symlink() or not path.is_file():
        raise ValueError('Run record is missing or no longer a regular file')
    record = json.loads(path.read_bytes())
    record.setdefault('launcher', {}).update(fields)
    temp = out / ('.launcher-record-' + uuid.uuid4().hex + '.tmp')
    try:
        with temp.open('x', encoding='utf-8') as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def prepare_trial(pack: Path, output_parent: Path, run_id: str | None,
                  allow: bool, model: str | None, reasoning: str | None) -> tuple[Path, str]:
    run_id = run_id or new_run_id()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,99}', run_id):
        raise ValueError('Invalid run_id')
    config = profile_config(model, reasoning)
    out = output_parent.expanduser().resolve() / f'{run_id}-output'
    pack_resolved = pack.expanduser().resolve()
    if (out == ROOT or ROOT in out.parents or out in ROOT.parents
            or pack_resolved == ROOT or ROOT in pack_resolved.parents):
        raise ValueError('Review inputs and outputs must be outside the main RustyBun checkout')
    preparer = load_preparer()
    preparer.prepare_run(pack, out, run_id, allow, model or 'unknown')
    update_launcher_record(out, {
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'helper_sha256': hashlib.sha256((ROOT / 'scripts/prepare-review-run.py').read_bytes()).hexdigest(),
        'profile_config_sha256': hashlib.sha256(config.encode()).hexdigest(),
        'profile_kind': 'fresh-home-and-codex-home', 'status': 'NOT_LAUNCHED',
        'requested_model': model or 'unknown', 'requested_reasoning_effort': reasoning or 'unknown',
        'requested_auth_mode': 'chatgpt', 'isolation_verified': False,
    })
    return out, preparer.show_handoff(out)


def launch_codex(out: Path, executable: str, model: str | None,
                 reasoning: str | None) -> int:
    preparer = load_preparer()
    preparer.show_handoff(out)  # Recheck inputs/record before authentication or client startup.
    record = json.loads((out / 'RUN-RECORD.json').read_bytes())
    if not record['operator_authorization']['allow_unverified_isolation']:
        raise ValueError('Launching requires --allow-unverified-isolation; no waiver is implicit')
    config = profile_config(model, reasoning)
    if hashlib.sha256(config.encode()).hexdigest() != record['launcher']['profile_config_sha256']:
        raise ValueError('Requested profile differs from the prepared launcher record')
    # The directory is private (0700), outside the output workspace and removed on normal exit.
    # No existing credentials, instructions, skills or session databases are copied.
    with tempfile.TemporaryDirectory(prefix='rustybun-codex-', dir='/tmp') as name:
        home = Path(name)
        env = profile_environment(home, dict(os.environ))
        codex_home = home / '.codex'
        codex_home.mkdir(mode=0o700)
        (codex_home / 'config.toml').write_text(config, encoding='utf-8')
        update_launcher_record(out, {'status': 'CHECKING_CLIENT', 'attempted_at': utc_now()})
        version = subprocess.run([executable, '--version'], cwd=out, env=env,
                                 capture_output=True, text=True, check=False, timeout=20)
        if version.returncode:
            raise RuntimeError('Codex version check failed; client not launched')
        update_launcher_record(out, {'client_version_observed': version.stdout.strip(),
                                     'status': 'AWAITING_LOGIN'})
        print('\nNew Codex profile: sign in with your existing ChatGPT account using the displayed device code.\n'
              'No API-key fallback. This uses the same account limits; it is not a quota reset.', flush=True)
        login = subprocess.run([executable, 'login', '--device-auth'], cwd=out, env=env, check=False)
        if login.returncode:
            update_launcher_record(out, {'status': 'LOGIN_FAILED', 'exit_code': login.returncode})
            return login.returncode
        # Login can take time. Do not start with inputs that changed while waiting.
        handoff = preparer.show_handoff(out)
        print('\n' + handoff + '\nOpening an EMPTY, NEW session. Select the model/settings, then paste the prompt above.\n'
              'Profile separation only: other local files/system policies may still be visible.\n'
              'Do not approve access to unrelated projects or relax the sandbox.\n', flush=True)
        update_launcher_record(out, {'status': 'CLIENT_RUNNING', 'client_started_at': utc_now()})
        result = subprocess.run([executable, '--sandbox', 'workspace-write',
                                 '--ask-for-approval', 'on-request', '--no-alt-screen'],
                                cwd=out, env=env, check=False)
        # Client exit is not evidence of a completed design. The reviewer owns task status.
        update_launcher_record(out, {'status': 'CLIENT_EXITED', 'exit_code': result.returncode,
                                     'client_ended_at': utc_now()})
    update_launcher_record(out, {'temporary_profile_removed': True})
    print(f'Client closed. Outputs preserved in: {out}\nCheck the report and run record; no gate was approved.', flush=True)
    return result.returncode


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pack', type=Path, default=ROOT.parent / 'RustyBun-review-01')
    parser.add_argument('--output-parent', type=Path, default=ROOT.parent)
    parser.add_argument('--run-id', help='Optional; default is a unique UTC timestamp plus random suffix')
    parser.add_argument('--update', action='store_true', help='Clean-checkout git pull --ff-only, then re-execute the updated launcher')
    parser.add_argument('--launch', action='store_true', help='Ubuntu/Linux: device login and open a new interactive Codex CLI session')
    parser.add_argument('--allow-unverified-isolation', action='store_true', help='Explicit exploratory design-only authorization, not proof of independence')
    parser.add_argument('--model', help='Exact ID from your client; omitted means select it in the opened session')
    parser.add_argument('--reasoning', help='Effort value supported by your client/model; no automatic fallback')
    args = parser.parse_args(argv)
    if args.launch and not args.allow_unverified_isolation:
        parser.error('--launch requires explicit --allow-unverified-isolation')
    if args.launch and (not sys.platform.startswith('linux') or not sys.stdin.isatty()):
        parser.error('--launch requires a Linux interactive terminal; run as the operator, not inside a reviewer')
    out = None
    try:
        if args.update:
            update_checkout(ROOT)
            # Read the new launcher/helper after the pull, not stale Python code already in memory.
            os.execv(sys.executable, [sys.executable, str(ROOT / 'scripts/independent-review.py'),
                                     *[a for a in argv if a != '--update']])
            raise RuntimeError('Failed to re-execute updated launcher')
        executable = None
        if args.launch:
            path = profile_environment(Path('/tmp/unused'), dict(os.environ))['PATH']
            executable = shutil.which('codex', path=path)
            if executable is None:
                raise ValueError('Codex CLI is not in PATH; no installation or run was attempted')
            executable = str(Path(executable).absolute())
        os.umask(0o077)  # This process only; do not change the operator's normal shell/profile.
        out, handoff = prepare_trial(args.pack, args.output_parent, args.run_id,
                                      args.allow_unverified_isolation, args.model, args.reasoning)
        print(handoff, end='', flush=True)
        if args.launch:
            return launch_codex(out, executable, args.model, args.reasoning)
        print('Preparation only. Run this command with --launch for a NEW run in a fresh Codex profile.')
        return 0
    except (OSError, ValueError, RuntimeError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        if out is not None:
            print(f'Prepared output preserved: {out}', file=sys.stderr)
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print('\nInterrupted. Preserve any prepared output; use a new run for another attempt.', file=sys.stderr)
        return 130


if __name__ == '__main__':
    raise SystemExit(main())
