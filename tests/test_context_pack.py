"""Offline tests with tiny local Git fixtures; no models or network calls."""
import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/build-context-pack.py'
spec = importlib.util.spec_from_file_location('pack', SCRIPT)
pack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pack)


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.DEVNULL).decode().strip()


def initialize(root):
    root.mkdir()
    git(root, 'init')
    git(root, 'config', 'user.email', 'fixture@example.invalid')
    git(root, 'config', 'user.name', 'Offline fixture')


class ContextPackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base / 'repo'
        initialize(self.root)
        self.bun = self.base / 'bun'
        initialize(self.bun)
        for name, text in {'src/main.zig': 'pub fn main() void {}\n', 'AGENTS.md': 'do not leak',
                           '.claude/settings.json': '{}', 'docs/PORTING.md': 'do not leak'}.items():
            p = self.bun / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        (self.bun / 'linked.zig').write_text('src/main.zig')
        git(self.bun, 'add', '.')
        link_blob = git(self.bun, 'hash-object', '-w', 'linked.zig')
        git(self.bun, 'update-index', '--cacheinfo', '120000', link_blob, 'linked.zig')
        git(self.bun, 'commit', '-m', 'source fixture')
        self.source_sha = git(self.bun, 'rev-parse', 'HEAD')
        config = {'source_sha': self.source_sha, 'bundles': {
            kind: {'task': 'prompt.md', 'inputs': ['brief.md'], **({'requires_bun': True} if kind == 'architect' else {})}
            for kind in pack.KINDS}}
        (self.root / 'templates').mkdir()
        (self.root / 'templates/run-record.json').write_text('{"status":"NOT_RUN"}')
        (self.root / 'workflow').mkdir()
        (self.root / 'workflow/bundles.json').write_text(json.dumps(config))
        (self.root / 'brief.md').write_text('committed brief\n')
        (self.root / 'prompt.md').write_text('review the brief\n')
        (self.root / 'secret.txt').write_text('not in allowlist')
        git(self.root, 'add', '.')
        git(self.root, 'commit', '-m', 'process fixture')

    def tearDown(self):
        self.temp.cleanup()

    def test_allowlist_and_hashes(self):
        out = self.base / 'pack'
        manifest = pack.build_pack(self.root, 'independent-design', out)
        self.assertEqual({f['path'] for f in manifest['files']}, {'AGENTS.md', 'TASK.md', 'RUN-RECORD.template.json', 'input/brief.md'})
        self.assertFalse((out / 'input/secret.txt').exists())
        for record in manifest['files']:
            self.assertEqual(record['sha256'], hashlib.sha256((out / record['path']).read_bytes()).hexdigest())
        self.assertFalse(manifest['isolation_verified'])

    def test_uncommitted_content_is_not_exported(self):
        (self.root / 'brief.md').write_text('uncommitted change')
        out = self.base / 'pack'
        pack.build_pack(self.root, 'design-review', out)
        self.assertEqual((out / 'input/brief.md').read_text(), 'committed brief\n')

    def test_refuses_project_output_and_overwrite(self):
        with self.assertRaises(ValueError):
            pack.build_pack(self.root, 'design-review', self.root / 'pack')
        out = self.base / 'pack'
        out.mkdir()
        with self.assertRaises(FileExistsError):
            pack.build_pack(self.root, 'design-review', out)

    def test_architect_requires_source(self):
        with self.assertRaises(ValueError):
            pack.build_pack(self.root, 'architect', self.base / 'pack')

    def test_source_excludes_controls_history_and_symlinks(self):
        out = self.base / 'pack'
        manifest = pack.build_pack(self.root, 'architect', out, bun_repo=self.bun)
        self.assertTrue((out / 'input/bun/src/main.zig').is_file())
        for path in ['.git', 'AGENTS.md', '.claude/settings.json', 'docs/PORTING.md', 'linked.zig']:
            self.assertFalse((out / 'input/bun' / path).exists())
        excluded = {item['path'] for item in manifest['excluded_source_entries']}
        self.assertIn('linked.zig', excluded)
        self.assertIn('docs/PORTING.md', excluded)
        self.assertEqual(manifest['source_sha'], self.source_sha)

    def test_invalid_paths_and_ref(self):
        for name in ['../escape', '/absolute', 'C:/absolute', 'a\\b']:
            with self.assertRaises(ValueError):
                pack.safe_path(name)
        with self.assertRaises(ValueError):
            pack.build_pack(self.root, 'design-review', self.base / 'pack', ref='--bad')

    def test_missing_input_does_not_publish_output(self):
        git(self.root, 'rm', 'brief.md')
        git(self.root, 'commit', '-m', 'remove input')
        out = self.base / 'pack'
        with self.assertRaises(ValueError):
            pack.build_pack(self.root, 'design-review', out)
        self.assertFalse(out.exists())

    def test_manifest_is_repeatable(self):
        first = pack.build_pack(self.root, 'design-review', self.base / 'one')
        second = pack.build_pack(self.root, 'design-review', self.base / 'two')
        self.assertEqual(first, second)


if __name__ == '__main__':
    unittest.main()
