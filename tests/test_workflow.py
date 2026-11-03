import tempfile
import unittest
from adaptive_harness.core import make_plan, explain, check_plan
from adaptive_harness.contracts import HarnessError, fingerprint
from test_selection import fixture

class WorkflowTests(unittest.TestCase):
    def test_all_routes_same_across_adapters(self):
        with tempfile.TemporaryDirectory() as root:
            for size,route in [('XS','quick'),('S','quick'),('M','standard'),('L','full'),('XL','full')]:
                results=[]
                for host in ('codex','cursor'):
                    a=fixture();a['feature_size']=size;a['host']['name']=host
                    a['host']['capabilities']['subagents']['value']=False
                    p=make_plan(a,root);w=p['workflow'];results.append(w)
                    self.assertEqual(w['route'],route)
                    self.assertEqual([x['name'] for x in w['phases']],['Specification','Implementation','Verification'])
                    self.assertFalse(w['new_chat_required']);self.assertFalse(w['automatic_session_creation'])
                    self.assertIn(w['recommendation'],explain(p))
                    if size in ('XS','S'):
                        self.assertEqual(w['specification_format'],'inline')
                        self.assertFalse(any(o['path'].endswith('/feature.md') for o in p['operations']))
                self.assertEqual(results[0],results[1])
    def test_small_risky_task_keeps_security_verification(self):
        with tempfile.TemporaryDirectory() as root:
            a=fixture();a['feature_size']='XS';a['facts']['personal_data']['value']=True
            p=make_plan(a,root)
            self.assertEqual(p['route'],'quick')
            self.assertIn('security-and-data-access',p['workflow']['phases'][2]['exit_criteria'])
    def test_workflow_cannot_be_forged_even_with_new_hash(self):
        with tempfile.TemporaryDirectory() as root:
            p=make_plan(fixture(),root);p['workflow']['phases'][2]['exit_criteria']=['skip tests']
            p['plan_id']=fingerprint({k:v for k,v in p.items() if k!='plan_id'})
            with self.assertRaises(HarnessError):check_plan(p,root)
