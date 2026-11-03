import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from adaptive_harness.contracts import ROOT, HarnessError, fingerprint, validate, read_json
from adaptive_harness.core import make_plan, explain, load_catalog, check_plan


def fixture(name='calculator'):
    return read_json(ROOT/'examples/assessments'/f'{name}.json')


def researched(a):
    """Synthetic evidence for deterministic tests; never claimed as live research."""
    a=copy.deepcopy(a)
    a['reuse']={'status':'complete','decision':'build','rationale':'Контрольний приклад: порівняли готове рішення; для вузького scope обрано власну реалізацію.',
        'candidates':[{'url':'https://github.com/example/synthetic-fixture','revision':'1'*40,'license':'MIT','license_sha256':'2'*64,
        'checked_at':'2026-11-03T00:00:00Z','evidence':['Synthetic test evidence only'],'fit':'Fixture fit assessment','maintenance':'Not verified in synthetic fixture',
        'security':'Not verified in synthetic fixture','cost':'Fixture cost comparison','integration':'Fixture integration comparison'}]}
    return a

class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()
    def test_four_scenarios_and_minimality(self):
        for name in ('calculator','crm','sensitive-saas','existing-app'):
            with self.subTest(name=name):
                a=fixture(name)
                if name in ('crm','sensitive-saas'): a=researched(a)
                p=make_plan(a,self.root)
                self.assertEqual(p['status'],'ready-for-approval')
                selected={d['id'] for d in p['decisions'] if d['status']=='selected'}
                self.assertIn('core.safety-baseline',selected)
                if name in ('calculator','existing-app'):
                    self.assertNotIn('docs.adr',selected); self.assertNotIn('data.migration-safety',selected)
                if name=='existing-app': self.assertNotIn('process.sdd-workflow',selected)
                if name in ('crm','sensitive-saas'): self.assertIn('security.auth-and-data',selected)
                if name=='sensitive-saas': self.assertIn('security.release-gate',selected)
    def test_deterministic_input_key_order(self):
        a=fixture(); b=json.loads(json.dumps(a,sort_keys=True))
        self.assertEqual(make_plan(a,self.root),make_plan(b,self.root))
        self.assertEqual(list(self.root.iterdir()),[])
    def test_unknown_does_not_mean_false(self):
        a=fixture(); a['facts']['personal_data']={'value':'unknown','basis':'unknown','sources':[]}
        p=make_plan(a,self.root)
        self.assertEqual(p['status'],'blocked')
        self.assertTrue(any(d['id']=='security.auth-and-data' and d['status']=='selected' for d in p['decisions']))
    def test_inferred_absence_blocks(self):
        a=fixture(); a['facts']['personal_data']['basis']='inferred'
        self.assertEqual(make_plan(a,self.root)['status'],'blocked')
    def test_reuse_required_for_crm_and_cms(self):
        for kind in ('crm','cms','auth','billing'):
            a=fixture(); a['project_type']=kind
            self.assertEqual(make_plan(a,self.root)['status'],'blocked')
    def test_offline_explained(self):
        a=fixture('crm'); a['reuse']['status']='offline'
        p=make_plan(a,self.root)
        self.assertIn('GitHub недоступний',explain(p))
        self.assertEqual(p['status'],'blocked')
    def test_no_review_capability_uses_honest_fallback(self):
        a=researched(fixture('crm')); a['host']['capabilities']['subagents']['value']=False
        p=make_plan(a,self.root)
        self.assertTrue(any(d['id']=='quality.inline-review' and d['status']=='selected' for d in p['decisions']))
        self.assertFalse(any(o['path'].endswith('.toml') for o in p['operations']))
        self.assertIn('не незалежним',explain(p))
    def test_unsupported_host_and_unverified_skill_capability(self):
        a=fixture(); a['host']['name']='lovable'
        self.assertEqual(make_plan(a,self.root)['status'],'blocked')
        a=fixture(); a['host']['capabilities']['native_skills']['basis']='inferred'
        self.assertEqual(make_plan(a,self.root)['status'],'blocked')
    def test_contract_rejects_untyped_risk_and_extra_fields(self):
        a=fixture(); a['facts']['personal_data']['value']='no'
        with self.assertRaises(HarnessError): make_plan(a,self.root)
        a=fixture(); a['disable_security']=True
        with self.assertRaises(HarnessError): make_plan(a,self.root)
    def test_catalog_invalid_graphs(self):
        import yaml
        original=load_catalog()
        for defect in ('missing','cycle','duplicate','conflict'):
            c=copy.deepcopy(original)
            if defect=='missing': c['modules'][0]['dependencies']=['missing']
            if defect=='cycle': c['modules'][0]['dependencies']=[c['modules'][0]['id']]
            if defect=='duplicate': c['modules'].append(c['modules'][0])
            if defect=='conflict': c['modules'][0]['conflicts']=['missing']
            original_read=Path.read_text
            def read(path,*args,**kwargs):
                return yaml.safe_dump(c) if path==ROOT/'catalog/modules.yaml' else original_read(path,*args,**kwargs)
            with patch.object(Path,'read_text',read),self.assertRaises(HarnessError): load_catalog()
    def test_plan_cannot_disable_policy_even_with_rehashed_id(self):
        p=make_plan(fixture(),self.root)
        p['operations']=[]
        p['plan_id']=fingerprint({k:v for k,v in p.items() if k!='plan_id'})
        with self.assertRaises(HarnessError): check_plan(p,self.root)
    def test_beginner_explanation(self):
        text=explain(make_plan(fixture(),self.root))
        for heading in ('Готові рішення','Що додамо','Що пропустимо','Ризики','Наступна дія','вручну запускати CLI не потрібно'):
            self.assertIn(heading,text)
    def test_migration_not_skipped_for_small_change(self):
        a=fixture(); a['facts']['schema_change']['value']=True
        p=make_plan(a,self.root)
        self.assertTrue(any(o['path']=='.agents/skills/adh-migration/SKILL.md' for o in p['operations']))
    def test_no_ui_artifact_for_worker(self):
        a=fixture(); a['surfaces']=['worker']
        p=make_plan(a,self.root)
        self.assertFalse(any('ui-check' in o['path'] for o in p['operations']))
    def test_existing_user_file_conflict(self):
        target=self.root/'.agents/skills/adh-verify/SKILL.md'; target.parent.mkdir(parents=True);target.write_text('user-owned')
        self.assertEqual(make_plan(fixture(),self.root)['status'],'blocked')
        self.assertEqual(target.read_text(),'user-owned')
    def test_duplicate_json_key_rejected(self):
        p=self.root/'input.json';p.write_text('{"a":1,"a":2}')
        with self.assertRaises(HarnessError):read_json(p)

if __name__=='__main__': unittest.main()

class AdditionalPolicyTests(unittest.TestCase):
    def test_modes_keep_identical_safety(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=researched(fixture('crm'));b=copy.deepcopy(a);b['user_mode']='developer'
            p=make_plan(a,tmp);q=make_plan(b,tmp)
            safety=lambda plan: [d for d in plan['decisions'] if d['id'].startswith('security.')]
            self.assertEqual(safety(p),safety(q));self.assertIn('Технічні деталі',explain(q))
    def test_route_does_not_disable_risk(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=researched(fixture('sensitive-saas'));a['feature_size']='XS'
            p=make_plan(a,tmp);self.assertEqual(p['route'],'quick')
            self.assertTrue(any(d['id']=='security.release-gate' and d['status']=='selected' for d in p['decisions']))
    def test_incomplete_collector_evidence_blocks_final_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=researched(fixture('crm'));a['reuse']['candidates'][0]['fit']='Не оцінено: потрібно прочитати PRD'
            self.assertEqual(make_plan(a,tmp)['status'],'blocked')
    def test_secrets_not_copied_from_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'.env').write_text('SYNTHETIC_PRIVATE_VALUE=not-a-real-secret')
            p=make_plan(fixture(),root)
            self.assertNotIn('SYNTHETIC_PRIVATE_VALUE',json.dumps(p))
    def test_malformed_manifest_blocks_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'.adaptive-harness').mkdir();(root/'.adaptive-harness/manifest.json').write_text('{}')
            self.assertEqual(make_plan(fixture(),root)['status'],'blocked')
