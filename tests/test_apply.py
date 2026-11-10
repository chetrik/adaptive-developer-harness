import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from adaptive_harness.contracts import HarnessError, fingerprint, digest
from adaptive_harness.core import make_plan
from adaptive_harness.apply import approve, apply_plan, verify, recover
from adaptive_harness.filesystem import snapshot
from test_selection import fixture, researched

class ApplyTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name).resolve()
        self.root=self.base/'target';self.root.mkdir();self.state=self.base/'state'
    def tearDown(self): self.tmp.cleanup()
    def prepare(self,a=None):
        p=make_plan(a or fixture(),self.root)
        return p,approve(p,self.root,'Synthetic test approval; not authorization for a real customer project')
    def test_selected_components_work_and_repeat_is_noop(self):
        p,a=self.prepare(); result=apply_plan(p,a,self.root,self.state)
        self.assertEqual(result['status'],'applied')
        self.assertTrue((self.root/'.agents/skills/adh-implement/SKILL.md').is_file())
        self.assertTrue((self.root/'.agents/skills/adh-verify/SKILL.md').is_file())
        self.assertFalse((self.root/'.agents/skills/adh-security').exists())
        result=subprocess.run([sys.executable,'.adaptive-harness/validate.py'],cwd=self.root,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('NOT VERIFIED',result.stdout)
        before=snapshot(self.root)
        result=apply_plan(p,a,self.root,self.state)
        self.assertEqual(result['status'],'already-applied');self.assertEqual(before,snapshot(self.root))
        self.assertEqual(verify(p,self.root)['status'],'not-verified')
    def test_all_four_scenarios_install_exact_selection(self):
        for name in ('calculator','crm','sensitive-saas','existing-app'):
            with self.subTest(name=name),tempfile.TemporaryDirectory() as temp:
                base=Path(temp).resolve();root=base/'target';root.mkdir();state=base/'state'
                a=fixture(name)
                if name in ('crm','sensitive-saas'): a=researched(a)
                p=make_plan(a,root);approval=approve(p,root,'Synthetic test consent')
                apply_plan(p,approval,root,state)
                actual={x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file()}
                self.assertEqual(actual,{o['path'] for o in p['operations']})
                if name=='crm': self.assertIn('.agents/skills/adh-reuse/SKILL.md',actual)
                result=subprocess.run([sys.executable,'.adaptive-harness/validate.py'],cwd=root,capture_output=True)
                self.assertEqual(result.returncode,0,result.stdout)
    def test_no_approval_no_writes(self):
        p,_=self.prepare();before=snapshot(self.root)
        with self.assertRaises(HarnessError):apply_plan(p,{},self.root,self.state)
        self.assertEqual(before,snapshot(self.root))
    def test_blocked_plan_cannot_be_approved(self):
        p=make_plan(fixture('crm'),self.root)
        with self.assertRaises(HarnessError):approve(p,self.root,'test')
        self.assertEqual(list(self.root.iterdir()),[])
    def test_modified_plan_or_target_invalidates_approval(self):
        p,a=self.prepare();p['operations'][0]['content']+='tamper'
        with self.assertRaises(HarnessError):apply_plan(p,a,self.root,self.state)
        p,a=self.prepare();(self.root/'user.txt').write_text('new work')
        with self.assertRaises(HarnessError):apply_plan(p,a,self.root,self.state)
        self.assertEqual(list(self.root.iterdir()),[self.root/'user.txt'])
    def test_wrong_target(self):
        p,a=self.prepare();other=self.base/'other';other.mkdir()
        with self.assertRaises(HarnessError):apply_plan(p,a,other,self.state)
    def test_traversal_and_absolute_paths(self):
        from adaptive_harness.filesystem import safe_path
        for path in ('../escape','/tmp/escape','a/../escape','.git/config','.env','.adaptive-harness/../../escape','C:\\escape','./AGENTS.md','.agents/skills/other/SKILL.md'):
            with self.subTest(path=path),self.assertRaises(HarnessError):safe_path(self.root,path)
    def test_symlink_ancestor_and_leaf_rejected(self):
        outside=self.base/'outside';outside.mkdir()
        (self.root/'.agents').symlink_to(outside,target_is_directory=True)
        with self.assertRaises(HarnessError):self.prepare()
        (self.root/'.agents').unlink()
        (self.root/'AGENTS.md').symlink_to(outside/'agents')
        with self.assertRaises(HarnessError):self.prepare()
        self.assertEqual(list(outside.iterdir()),[])
    def test_target_root_symlink_rejected(self):
        from adaptive_harness.filesystem import root_path
        linked=self.base/'linked-target'
        linked.symlink_to(self.root,target_is_directory=True)
        with self.assertRaisesRegex(HarnessError,'Target root contains a symlink'):
            root_path(linked)
    def test_existing_agents_and_dirty_files_preserved(self):
        old='User rules\n\n\n'; (self.root/'AGENTS.md').write_text(old)
        (self.root/'user.py').write_text('unfinished work\n')
        p,a=self.prepare();apply_plan(p,a,self.root,self.state)
        self.assertTrue((self.root/'AGENTS.md').read_text().startswith(old))
        self.assertEqual((self.root/'user.py').read_text(),'unfinished work\n')
    def test_failed_write_rolls_back(self):
        import adaptive_harness.apply as module
        p,a=self.prepare();before=snapshot(self.root);real=module._atomic;calls=0
        def fail(*args,**kwargs):
            nonlocal calls
            calls+=1
            if calls==3:raise OSError('simulated disk failure')
            return real(*args,**kwargs)
        with patch.object(module,'_atomic',fail),self.assertRaises(HarnessError):apply_plan(p,a,self.root,self.state)
        self.assertEqual(before,snapshot(self.root))
        self.assertEqual(apply_plan(p,a,self.root,self.state)['status'],'applied')
    def test_tampered_output_detected_by_generated_validator(self):
        p,a=self.prepare();apply_plan(p,a,self.root,self.state)
        (self.root/'.agents/skills/adh-verify/SKILL.md').write_text('tampered')
        result=subprocess.run([sys.executable,'.adaptive-harness/validate.py'],cwd=self.root,capture_output=True)
        self.assertEqual(result.returncode,1)
        self.assertEqual(verify(p,self.root)['status'],'fail')
        with self.assertRaises(HarnessError):apply_plan(p,a,self.root,self.state)
    def test_license_and_per_file_provenance(self):
        p,a=self.prepare();apply_plan(p,a,self.root,self.state)
        manifest=json.loads((self.root/'.adaptive-harness/manifest.json').read_text())
        self.assertIn('Copyright (c) 2026 chetrik',(self.root/'.adaptive-harness/LICENSE').read_text())
        self.assertEqual(set(manifest['files']),set(manifest['provenance']))
        self.assertTrue(all(v['license']=='MIT' for v in manifest['provenance'].values()))
    def test_state_cannot_be_in_target(self):
        p,a=self.prepare()
        with self.assertRaises(HarnessError):apply_plan(p,a,self.root,self.root/'state')
    def test_no_new_changes_after_replanning_installed_output(self):
        p,a=self.prepare();apply_plan(p,a,self.root,self.state)
        new=make_plan(fixture(),self.root)
        self.assertEqual(new['operations'],[])

if __name__=='__main__':unittest.main()

class RecoveryTests(unittest.TestCase):
    setUp=ApplyTests.setUp
    tearDown=ApplyTests.tearDown
    prepare=ApplyTests.prepare
    def test_hard_interruption_recovers(self):
        import adaptive_harness.apply as module
        p,a=self.prepare(); before=snapshot(self.root);real=module._atomic;calls=0
        def interrupt(*args,**kwargs):
            nonlocal calls
            calls+=1
            result=real(*args,**kwargs)
            if calls==1: raise KeyboardInterrupt('simulated process interruption')
            return result
        with patch.object(module,'_atomic',interrupt),self.assertRaises(KeyboardInterrupt):apply_plan(p,a,self.root,self.state)
        self.assertNotEqual(before,snapshot(self.root))
        self.assertEqual(recover(p,a,self.root,self.state)['status'],'rolled-back')
        self.assertEqual(before,snapshot(self.root))
    def test_recovery_preserves_user_edit(self):
        import adaptive_harness.apply as module
        p,a=self.prepare();real=module._atomic;calls=0
        def interrupt(*args,**kwargs):
            nonlocal calls
            calls+=1;result=real(*args,**kwargs)
            if calls==1:raise KeyboardInterrupt()
            return result
        with patch.object(module,'_atomic',interrupt),self.assertRaises(KeyboardInterrupt):apply_plan(p,a,self.root,self.state)
        path=self.root/p['operations'][0]['path'];path.write_text('new user work')
        result=recover(p,a,self.root,self.state)
        self.assertEqual(result['status'],'needs-recovery');self.assertEqual(path.read_text(),'new user work')
    def test_changed_external_prd_invalidates_approval(self):
        a=fixture();prd=self.base/'PRD.md';prd.write_text('local PRD')
        a['prd']={'source':str(prd),'sha256':digest(prd.read_bytes())}
        p,approval=self.prepare(a);prd.write_text('changed requirements')
        with self.assertRaises(HarnessError):apply_plan(p,approval,self.root,self.state)
    def test_replanned_noop_still_validates_all_files(self):
        p,a=self.prepare();apply_plan(p,a,self.root,self.state)
        new=make_plan(fixture(),self.root);self.assertEqual(new['operations'],[])
        (self.root/'.agents/skills/adh-verify/SKILL.md').unlink()
        self.assertEqual(verify(new,self.root)['status'],'fail')

class BoundaryTests(unittest.TestCase):
    setUp=ApplyTests.setUp
    tearDown=ApplyTests.tearDown
    prepare=ApplyTests.prepare
    def test_lock_shared_across_state_directories(self):
        import fcntl,os
        p,a=self.prepare()
        lock_path=Path(tempfile.gettempdir())/('adh-lock-'+digest(str(self.root)))
        with open(lock_path,'w') as handle:
            fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
            with self.assertRaises(HarnessError):apply_plan(p,a,self.root,self.state)
        self.assertEqual(list(self.root.iterdir()),[])
    def test_recovery_rejects_unapproved_directory_scope(self):
        import adaptive_harness.apply as module
        p,a=self.prepare();real=module._atomic
        def interrupt(*args,**kwargs):
            real(*args,**kwargs);raise KeyboardInterrupt()
        with patch.object(module,'_atomic',interrupt),self.assertRaises(KeyboardInterrupt):apply_plan(p,a,self.root,self.state)
        path=self.state/(p['plan_id']+'.journal.json');journal=json.loads(path.read_text());journal['directories'].append('../outside');path.write_text(json.dumps(journal))
        with self.assertRaises(HarnessError):recover(p,a,self.root,self.state)
    def test_conditional_subagent_definition_is_read_only(self):
        import tomllib
        p,a=self.prepare(researched(fixture('crm')))
        apply_plan(p,a,self.root,self.state)
        role=tomllib.loads((self.root/'.codex/agents/adh-reviewer.toml').read_text())
        self.assertEqual(role['sandbox_mode'],'read-only')
        self.assertNotIn('model',role)
