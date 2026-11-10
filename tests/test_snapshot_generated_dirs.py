import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from adaptive_harness import filesystem
from adaptive_harness.apply import apply_plan, approve
from adaptive_harness.contracts import HarnessError
from adaptive_harness.core import make_plan
from adaptive_harness.handoff import resume
from test_handoff import record
from test_selection import fixture


EXPECTED_GENERATED_DIRS = frozenset({
    'node_modules', '.next', '.venv', 'venv',
    '__pycache__', 'dist', 'build',
})


class SnapshotGeneratedDirectoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / 'target'
        self.root.mkdir()
        (self.root / 'app.py').write_text('original app')
        (self.root / 'web').mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def generated_dirs(self):
        return getattr(filesystem, 'GENERATED_DIRS', EXPECTED_GENERATED_DIRS)

    def fill_generated_dirs(self, content=b'generated'):
        for name in self.generated_dirs():
            directory = self.root / name
            directory.mkdir(parents=True, exist_ok=True)
            (directory / 'artifact.bin').write_bytes(content)
        nested = self.root / 'web' / 'node_modules'
        nested.mkdir(parents=True, exist_ok=True)
        (nested / 'package.bin').write_bytes(content)

    def test_generated_directories_do_not_change_snapshot(self):
        before = filesystem.snapshot(self.root)
        self.fill_generated_dirs()
        self.assertEqual(self.generated_dirs(), EXPECTED_GENERATED_DIRS)
        self.assertEqual(filesystem.snapshot(self.root), before)

        (self.root / 'app.py').write_text('changed source')
        self.assertNotEqual(filesystem.snapshot(self.root), before)

    def test_generated_directories_do_not_consume_byte_budget(self):
        with patch('adaptive_harness.filesystem.MAX_BYTES', 1024):
            self.fill_generated_dirs(b'x' * 2048)
            filesystem.snapshot(self.root)

            (self.root / 'large-source.bin').write_bytes(b'x' * 2048)
            with self.assertRaises(HarnessError):
                filesystem.snapshot(self.root)

    def test_handoff_ignores_generated_directories_but_detects_source_change(self):
        assessment = fixture()
        state = self.base / 'state'
        install = make_plan(assessment, self.root)
        apply_plan(
            install,
            approve(install, self.root, 'Synthetic install consent'),
            self.root,
            state,
        )
        checkpoint = make_plan(assessment, self.root, handoff=record())
        apply_plan(
            checkpoint,
            approve(checkpoint, self.root, 'Synthetic handoff consent'),
            self.root,
            state,
        )

        self.fill_generated_dirs()
        self.assertEqual(resume(self.root, 'step-1')['status'], 'current')
        (self.root / 'app.py').write_text('changed source')
        self.assertEqual(resume(self.root, 'step-1')['status'], 'stale')


if __name__ == '__main__':
    unittest.main()
