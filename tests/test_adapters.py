"""Synthetic integration evidence; does not assert native Cursor execution."""
import copy
import tempfile
import unittest
from pathlib import Path
from adaptive_harness.adapters import profiles
from adaptive_harness.bootstrap import intake, GENERATOR_URL
from adaptive_harness.contracts import HarnessError, digest, ROOT
from adaptive_harness.core import make_plan, check_plan
from adaptive_harness.apply import approve, apply_plan, verify
from test_selection import fixture, researched

class AdapterTests(unittest.TestCase):
    def test_cursor_four_scenarios_apply_and_idempotency(self):
        for scenario in ('calculator','crm','sensitive-saas','existing-app'):
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as tmp:
                target=Path(tmp)/'target'; target.mkdir()
                (target/'.cursor').mkdir(); config=target/'.cursor'/'user.txt'; config.write_text('User-owned configuration')
                a=fixture(scenario)
                if scenario in ('crm','sensitive-saas'): a=researched(a)
                a['host']['name']='cursor'
                p=make_plan(a,target)
                self.assertEqual(p['status'],'ready-for-approval')
                self.assertEqual(p['adapter']['status'],'contract-tested-native-unverified')
                self.assertTrue(any(o['path'].startswith('.agents/skills/') for o in p['operations']))
                self.assertFalse(any(o['path'].startswith('.codex/') for o in p['operations']))
                self.assertTrue(any(o['path']=='.cursor/rules/adh.mdc' for o in p['operations']))
                self.assertFalse((target/'AGENTS.md').exists())
                receipt=approve(p,target,'Synthetic consent')
                self.assertEqual(apply_plan(p,receipt,target,Path(tmp)/'state')['status'],'applied')
                self.assertEqual(config.read_text(),'User-owned configuration')
                self.assertEqual(verify(p,target)['status'],'not-verified')
                self.assertEqual(make_plan(a,target)['operations'],[])

    def test_single_selector_same_effective_capabilities(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=researched(fixture('crm')); a['host']['capabilities']['subagents']['value']=False
            baseline=make_plan(a,tmp)
            a['host']['name']='cursor'; cursor=make_plan(a,tmp)
            self.assertEqual(baseline['decisions'],cursor['decisions'])
            self.assertEqual([o for o in baseline['operations'] if not o['path'].endswith('/manifest.json')],
                             [o for o in cursor['operations'] if not o['path'].endswith('/manifest.json') and not o['path'].startswith('.cursor/')])

    def test_explicit_executor_target_and_unknown_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=fixture(); executor,target=profiles(a)
            a['execution_host']=executor; a['target_platform']=target
            executor['name']='local-python'; target['name']='cursor'
            self.assertEqual(make_plan(a,tmp)['adapter']['id'],'cursor')
            executor['capabilities']['write_files']={'value':'unknown','basis':'unknown','sources':[]}
            self.assertEqual(make_plan(a,tmp)['status'],'blocked')
            del a['target_platform']
            with self.assertRaisesRegex(HarnessError,'together'):make_plan(a,tmp)

    def test_adapter_tampering_invalidates_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=fixture(); a['host']['name']='cursor'; p=make_plan(a,tmp)
            p['adapter']['version']='999'
            with self.assertRaises(HarnessError):check_plan(p,tmp)

    def test_cursor_unconfirmed_discovery_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=fixture();a['host']['name']='cursor'
            a['host']['capabilities']['native_skills']['basis']='inferred'
            self.assertEqual(make_plan(a,tmp)['status'],'blocked')

    def test_bootstrap_original_formats_and_separate_profiles(self):
        with tempfile.TemporaryDirectory() as tmp:
            for suffix,raw in (('.md',b'# Synthetic PRD'),('.pdf',b'%PDF-synthetic'),('.docx',b'PK synthetic')):
                path=Path(tmp)/('prd'+suffix);path.write_bytes(raw)
                a=intake(path,GENERATOR_URL,target_platform='cursor')['assessment']
                self.assertEqual(a['prd']['sha256'],digest(raw))
                self.assertEqual(a['prd']['reading']['status'],'unread')
                self.assertEqual(a['target_platform']['name'],'cursor')
                self.assertEqual(a['execution_host']['name'],'local-python')
                self.assertEqual(a['target_platform']['capabilities']['native_skills']['value'],'unknown')

    def test_binary_reading_and_original_change_gate(self):
        # Bytes are synthetic: these tests validate provenance contracts, not PDF/DOCX readers.
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'target';target.mkdir()
            for extension in ('pdf','docx'):
                path=Path(tmp)/('prd.'+extension);path.write_bytes(b'synthetic document')
                a=fixture(); a['prd']={'source':str(path),'sha256':digest(path.read_bytes()),'format':extension}
                self.assertEqual(make_plan(a,target)['status'],'blocked')
                a['prd']['reading']={'status':'complete','reader':'synthetic fixture','locators':['page 1 / section requirements'],'notes':[]}
                p=make_plan(a,target);self.assertEqual(p['status'],'ready-for-approval')
                a['prd']['format']='markdown'
                self.assertEqual(make_plan(a,target)['status'],'blocked')
                a['prd']['format']=extension
                a['prd']['reading']['status']='partial'
                self.assertEqual(make_plan(a,target)['status'],'blocked')
                path.write_bytes(b'changed')
                with self.assertRaises(HarnessError):check_plan(p,target)

if __name__=='__main__':unittest.main()
