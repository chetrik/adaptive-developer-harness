import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from adaptive_harness.contracts import HarnessError
from adaptive_harness.core import make_plan
from adaptive_harness.apply import approve, apply_plan
from adaptive_harness.handoff import resume, record_path
from test_selection import fixture


def record():
    return {'session_id':'step-1','phase':'Verification','task':'Check calculator behavior',
            'decisions':['Use existing application'],'completed':['Reviewed requirements'],
            'unfinished':['Native UI test'],'changed_files':['app.py'],
            'tests':[{'command':None,'status':'not-verified','exit_code':None,'detail':'Application tests unavailable in synthetic fixture'}],
            'risks':['Native host not evaluated'],'next_step':'Run native application checks'}

class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name).resolve()
        self.root=self.base/'target';self.root.mkdir();self.state=self.base/'state'
        (self.root/'app.py').write_text('original app')
        self.a=fixture();p=make_plan(self.a,self.root)
        apply_plan(p,approve(p,self.root,'Synthetic install consent'),self.root,self.state)
    def tearDown(self):self.temp.cleanup()
    def checkpoint(self,data=None):
        p=make_plan(self.a,self.root,handoff=data or record())
        self.assertEqual(p['status'],'ready-for-approval',p['blockers'])
        approval=approve(p,self.root,'Synthetic handoff recording consent')
        apply_plan(p,approval,self.root,self.state)
        return p,approval
    def test_checkpoint_uses_common_apply_and_resume_detects_stale(self):
        p,a=self.checkpoint()
        self.assertEqual(len(p['operations']),1)
        self.assertEqual(p['update']['intent'],'handoff')
        self.assertEqual(resume(self.root,'step-1')['status'],'current')
        self.assertEqual(apply_plan(p,a,self.root,self.state)['status'],'already-applied')
        self.assertEqual(make_plan(self.a,self.root,handoff=record())['operations'],[])
        self.assertEqual(make_plan(self.a,self.root)['operations'],[])
        m=json.loads((self.root/'.adaptive-harness/manifest.json').read_text())
        self.assertNotIn(record_path('step-1'),m['files'])
        (self.root/'app.py').write_text('new requirements implemented')
        self.assertEqual(resume(self.root,'step-1')['status'],'stale')
    def test_no_approval_or_stale_approval_no_record(self):
        p=make_plan(self.a,self.root,handoff=record())
        with self.assertRaises(HarnessError):apply_plan(p,{},self.root,self.state)
        a=approve(p,self.root,'Synthetic consent');(self.root/'app.py').write_text('intervening work')
        with self.assertRaises(HarnessError):apply_plan(p,a,self.root,self.state)
        self.assertFalse((self.root/record_path('step-1')).exists())
    def test_new_checkpoint_does_not_make_old_one_stale(self):
        self.checkpoint();r=record();r['session_id']='step-2';r['next_step']='Continue same task'
        self.checkpoint(r)
        self.assertEqual(resume(self.root,'step-1')['status'],'current')
        self.assertEqual(resume(self.root,'step-2')['status'],'current')
    def test_existing_record_cannot_be_silently_replaced(self):
        self.checkpoint();r=record();r['next_step']='Different task'
        self.assertEqual(make_plan(self.a,self.root,handoff=r)['status'],'blocked')
        (self.root/'app.py').write_text('changed')
        self.assertEqual(make_plan(self.a,self.root,handoff=record())['status'],'blocked')
    def test_bad_records_and_references_rejected(self):
        records=[]
        for key in record():
            r=record();del r[key];records.append(r)
        for name in ('../outside','.env','.git/config','/tmp/escape','a/../b'):
            r=record();r['changed_files']=[name];records.append(r)
        for command,status,exit_code in [(None,'pass',0),('test','pass',1),('test','fail',0),('test','skipped',0)]:
            r=record();r['tests']=[{'command':command,'status':status,'exit_code':exit_code,'detail':'invalid evidence'}];records.append(r)
        r=record();r['session_id']='../escape';records.append(r)
        for r in records:
            with self.subTest(record=r),self.assertRaises(HarnessError):make_plan(self.a,self.root,handoff=r)
    def test_cannot_mix_update_with_handoff(self):
        a=fixture();a['feature_size']='M'
        self.assertEqual(make_plan(a,self.root,handoff=record())['status'],'blocked')
    def test_interrupted_checkpoint_recovers_with_same_writer(self):
        from adaptive_harness import apply as module
        p=make_plan(self.a,self.root,handoff=record());a=approve(p,self.root,'Synthetic consent')
        real=module._atomic
        def interrupt(*args,**kwargs):real(*args,**kwargs);raise KeyboardInterrupt()
        with patch.object(module,'_atomic',interrupt),self.assertRaises(KeyboardInterrupt):
            apply_plan(p,a,self.root,self.state)
        self.assertEqual(module.recover(p,a,self.root,self.state)['status'],'rolled-back')
        self.assertFalse((self.root/record_path('step-1')).exists())
        self.assertEqual(apply_plan(p,a,self.root,self.state)['status'],'applied')
    def test_symlink_record_directory_refused(self):
        outside=self.base/'outside';outside.mkdir()
        (self.root/'.adaptive-harness/sessions').symlink_to(outside,target_is_directory=True)
        with self.assertRaises(HarnessError):make_plan(self.a,self.root,handoff=record())
        self.assertEqual(list(outside.iterdir()),[])

    def test_agent_cli_checkpoint_and_resume(self):
        import subprocess,sys
        from adaptive_harness.contracts import ROOT
        assessment=self.base/'assessment.json';assessment.write_text(json.dumps(self.a))
        data=self.base/'handoff.json';data.write_text(json.dumps(record()))
        def run(*args,code=0):
            result=subprocess.run([sys.executable,'-m','adaptive_harness',*args],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(result.returncode,code,result.stderr)
            return result.stdout
        self.assertEqual(json.loads(run('inventory','--target',str(self.root)))['status'],'installed')
        plan=self.base/'plan.json';plan.write_text(run('handoff-plan','--assessment',str(assessment),'--record',str(data),'--target',str(self.root)))
        self.assertIn('step-1.json',run('preview','--plan',str(plan),'--target',str(self.root)))
        approval=self.base/'approval.json';approval.write_text(run('approve','--plan',str(plan),'--target',str(self.root),'--confirmation','Synthetic CLI consent'))
        run('apply','--plan',str(plan),'--approval',str(approval),'--target',str(self.root),'--state-dir',str(self.state))
        self.assertEqual(json.loads(run('resume','--target',str(self.root),'--session-id','step-1'))['status'],'current')
        (self.root/'app.py').write_text('changed')
        self.assertEqual(json.loads(run('resume','--target',str(self.root),'--session-id','step-1',code=2))['status'],'stale')
