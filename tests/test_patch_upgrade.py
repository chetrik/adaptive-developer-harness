"""0.5.0 installed assets must remain upgradable without losing user changes."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from adaptive_harness.contracts import ROOT, HarnessError
from adaptive_harness.core import make_plan
from adaptive_harness.apply import approve, apply_plan, recover
from adaptive_harness.filesystem import snapshot
from test_selection import fixture


class PatchUpgradeTests(unittest.TestCase):
    def old_install(self, root, host):
        data = json.loads((ROOT / f'tests/fixtures/manifest-v2-050-{host}-output.json').read_text())
        for name, content in data.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        a = fixture()
        a['feature_size'] = 'M'
        a['host']['name'] = host
        return a

    def test_upgrade_all_three_hosts_preserves_files_and_is_noop_on_repeat(self):
        for host in ('codex', 'cursor', 'claude-code'):
            with self.subTest(host=host), tempfile.TemporaryDirectory() as temp:
                base = Path(temp).resolve(); root = base / 'app'; root.mkdir()
                a = self.old_install(root, host)
                (root / 'user.txt').write_text('Keep this')
                agents = root / 'AGENTS.md'
                agents.write_text('User-owned preface\n' + agents.read_text())
                p = make_plan(a, root)
                self.assertEqual(p['status'], 'ready-for-approval', p['blockers'])
                self.assertEqual(p['update']['migration'], 'engine-0.5.0-to-0.5.2')
                self.assertFalse(any(o['action'] == 'delete' for o in p['operations']))
                apply_plan(p, approve(p, root, 'Synthetic upgrade consent'), root, base / 'state')
                self.assertEqual((root / 'user.txt').read_text(), 'Keep this')
                self.assertTrue(agents.read_text().startswith('User-owned preface'))
                self.assertEqual(make_plan(a, root)['operations'], [])
                manifest = json.loads((root / '.adaptive-harness/manifest.json').read_text())
                self.assertEqual(manifest['versions']['generator'], '0.5.2')
                self.assertEqual(manifest['schema_version'], '2.0')

    def test_customized_component_blocks_upgrade_and_approved_stale_plan(self):
        for host in ('codex', 'cursor', 'claude-code'):
            with self.subTest(host=host), tempfile.TemporaryDirectory() as temp:
                base = Path(temp).resolve(); root = base / 'app'; root.mkdir()
                a = self.old_install(root, host)
                p = make_plan(a, root); consent = approve(p, root, 'Synthetic consent')
                path = root / '.adaptive-harness/templates/feature.md'
                path.write_text(path.read_text() + '\nUser requirement\n')
                before = snapshot(root)
                self.assertEqual(make_plan(a, root)['status'], 'blocked')
                with self.assertRaises(HarnessError):
                    apply_plan(p, consent, root, base / 'state')
                self.assertEqual(snapshot(root), before)

    def test_upgrade_interruption_recovery_and_retry(self):
        from adaptive_harness import apply as module
        for host in ('codex', 'cursor', 'claude-code'):
            with self.subTest(host=host), tempfile.TemporaryDirectory() as temp:
                base = Path(temp).resolve(); root = base / 'app'; root.mkdir(); state = base / 'state'
                a = self.old_install(root, host)
                p = make_plan(a, root); consent = approve(p, root, 'Synthetic consent')
                before = snapshot(root); atomic = module._atomic
                def interrupt(*args, **kwargs):
                    atomic(*args, **kwargs)
                    raise KeyboardInterrupt()
                with patch.object(module, '_atomic', interrupt), self.assertRaises(KeyboardInterrupt):
                    apply_plan(p, consent, root, state)
                self.assertEqual(recover(p, consent, root, state)['status'], 'rolled-back')
                self.assertEqual(snapshot(root), before)
                self.assertEqual(apply_plan(p, consent, root, state)['status'], 'applied')
                self.assertEqual(apply_plan(p, consent, root, state)['status'], 'already-applied')
                self.assertEqual(make_plan(a, root)['operations'], [])

    def test_original_050_checkout_recovers_its_interrupted_operation(self):
        import test_engine_migration as historical
        case = historical.EngineMigrationTests('test_previous_engine_recovery_is_retained_and_migration_waits')
        case.setUp()
        try:
            with patch.object(historical, 'OLD_COMMIT', '2ab369790fda5be2db57097d0f6fe90813aee9e1'):
                case.test_previous_engine_recovery_is_retained_and_migration_waits()
        finally:
            case.tearDown()

    def test_051_manifest_updates_to_052_without_rewriting_components(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp).resolve(); root = base / 'app'; root.mkdir()
            assessment = fixture()
            install = make_plan(assessment, root)
            apply_plan(install, approve(install, root, 'Synthetic install consent'), root, base / 'state')
            manifest_path = root / '.adaptive-harness/manifest.json'
            manifest = json.loads(manifest_path.read_text())
            manifest['versions']['generator'] = '0.5.1'
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + '\n')

            plan = make_plan(assessment, root)
            self.assertEqual(plan['update']['migration'], 'engine-0.5.1-to-0.5.2')
            self.assertEqual([op['path'] for op in plan['operations']], ['.adaptive-harness/manifest.json'])
            apply_plan(plan, approve(plan, root, 'Synthetic patch update consent'), root, base / 'state')
            updated = json.loads(manifest_path.read_text())
            self.assertEqual(updated['versions']['generator'], '0.5.2')
