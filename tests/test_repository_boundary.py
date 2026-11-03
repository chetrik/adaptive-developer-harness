"""Explicit boundary between generator internals and selected customer components."""
import json
import tempfile
import unittest
from pathlib import Path
from adaptive_harness.contracts import ROOT
from adaptive_harness.core import load_catalog, make_plan, _source
from adaptive_harness.apply import approve, apply_plan
from test_selection import fixture, researched

class RepositoryBoundaryTests(unittest.TestCase):
    def test_target_library_has_no_unreferenced_assets(self):
        referenced={_source(path) for module in load_catalog()['modules'] for path in module['files']}
        actual={p.name for p in (ROOT/'library/target').iterdir() if p.is_file()}
        self.assertEqual(actual,referenced)

    def test_only_selected_target_assets_are_installed(self):
        for host in ('codex','cursor'):
            for scenario in ('calculator','crm','sensitive-saas','existing-app'):
                with self.subTest(host=host,scenario=scenario),tempfile.TemporaryDirectory() as temp:
                    base=Path(temp).resolve();target=base/'target';target.mkdir()
                    assessment=fixture(scenario)
                    if scenario in ('crm','sensitive-saas'):assessment=researched(assessment)
                    assessment['host']['name']=host
                    plan=make_plan(assessment,target)
                    chosen={d['id'] for d in plan['decisions'] if d['status']=='selected'}
                    expected={'AGENTS.md','.adaptive-harness/LICENSE','.adaptive-harness/manifest.json'}
                    for module in load_catalog()['modules']:
                        if module['id'] in chosen:expected.update(module['files'])
                    self.assertEqual({o['path'] for o in plan['operations']},expected)
                    apply_plan(plan,approve(plan,target,'Synthetic boundary test consent'),target,base/'state')
                    self.assertEqual({p.relative_to(target).as_posix() for p in target.rglob('*') if p.is_file()},expected)
                    self.assertNotEqual((target/'AGENTS.md').read_bytes(),(ROOT/'AGENTS.md').read_bytes())
                    manifest=json.loads((target/'.adaptive-harness/manifest.json').read_text())
                    for item in manifest['provenance'].values():
                        self.assertTrue(item['source_file'] in ('LICENSE','adaptive_harness/core.py') or item['source_file'].startswith('library/target/'))
