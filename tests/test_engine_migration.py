import io
import json
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from adaptive_harness.contracts import ROOT,HarnessError
from adaptive_harness.core import make_plan,check_plan
from adaptive_harness.apply import approve,apply_plan,recover
from adaptive_harness.filesystem import snapshot
from test_selection import fixture

OLD_COMMIT='63dc1bd47e0ef9b3002ada24127c5a5ba2853f90'

class EngineMigrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name).resolve()
        self.root=self.base/'target';self.root.mkdir();self.state=self.base/'state'
        for name,content in json.loads((ROOT/'tests/fixtures/manifest-v2-030-output.json').read_text()).items():
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
        self.a=fixture();self.a['feature_size']='M'
    def tearDown(self):self.tmp.cleanup()
    def test_migration_preserves_format_and_repeat(self):
        p=make_plan(self.a,self.root)
        self.assertEqual(p['update']['migration'],'engine-0.3-to-0.4')
        apply_plan(p,approve(p,self.root,'Synthetic migration consent'),self.root,self.state)
        m=json.loads((self.root/'.adaptive-harness/manifest.json').read_text())
        self.assertEqual(m['schema_version'],'2.0');self.assertEqual(m['versions']['generator'],'0.4.0')
        self.assertEqual(make_plan(self.a,self.root)['operations'],[])
    def test_conflict_and_stale_plan(self):
        p=make_plan(self.a,self.root);a=approve(p,self.root,'Synthetic consent')
        path=self.root/'.agents/skills/adh-implement/SKILL.md';path.write_text(path.read_text()+'User edit')
        self.assertEqual(make_plan(self.a,self.root)['status'],'blocked')
        with self.assertRaises(HarnessError):apply_plan(p,a,self.root,self.state)
        self.assertTrue(path.read_text().endswith('User edit'))
    def test_interruption_recovery_and_retry(self):
        import adaptive_harness.apply as module
        p=make_plan(self.a,self.root);a=approve(p,self.root,'Synthetic migration');before=snapshot(self.root)
        real=module._atomic
        def interrupt(*args,**kwargs):real(*args,**kwargs);raise KeyboardInterrupt()
        with patch.object(module,'_atomic',interrupt),self.assertRaises(KeyboardInterrupt):apply_plan(p,a,self.root,self.state)
        self.assertEqual(recover(p,a,self.root,self.state)['status'],'rolled-back')
        self.assertEqual(snapshot(self.root),before)
        self.assertEqual(apply_plan(p,a,self.root,self.state)['status'],'applied')
        self.assertEqual(apply_plan(p,a,self.root,self.state)['status'],'already-applied')
    def test_previous_engine_recovery_is_retained_and_migration_waits(self):
        # Execute only the reviewed historical project code from the pinned local Git object.
        old=self.base/'old';old.mkdir()
        archive=subprocess.check_output(['git','archive',OLD_COMMIT,'adaptive_harness','schemas','catalog','library/target','LICENSE','examples'],cwd=ROOT)
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:tar.extractall(old,filter='data')
        script='''
import json,sys
from pathlib import Path
from unittest.mock import patch
from adaptive_harness import apply as module
from adaptive_harness.core import make_plan
root=Path(sys.argv[1]);state=Path(sys.argv[2]);base=Path(sys.argv[3])
a=json.loads(Path('examples/assessments/calculator.json').read_text())
p=make_plan(a,root);receipt=module.approve(p,root,'Synthetic old-engine consent')
(base/'old-plan.json').write_text(json.dumps(p));(base/'old-approval.json').write_text(json.dumps(receipt))
real=module._atomic
def interrupt(*args,**kwargs):
 if len(sys.argv)>4:real(*args,**kwargs)
 raise KeyboardInterrupt()
with patch.object(module,'_atomic',interrupt):
 try:module.apply_plan(p,receipt,root,state)
 except KeyboardInterrupt:pass
'''
        subprocess.run([sys.executable,'-c',script,str(self.root),str(self.state),str(self.base)],cwd=old,check=True)
        oldplan=json.loads((self.base/'old-plan.json').read_text())
        with self.assertRaises(HarnessError):check_plan(oldplan,self.root)
        p=make_plan(self.a,self.root);a=approve(p,self.root,'Synthetic migration consent')
        with self.assertRaisesRegex(HarnessError,'Unfinished prior'):apply_plan(p,a,self.root,self.state)
        command=[sys.executable,'-m','adaptive_harness','recover','--plan',str(self.base/'old-plan.json'),'--approval',str(self.base/'old-approval.json'),'--target',str(self.root),'--state-dir',str(self.state)]
        r=subprocess.run(command,cwd=old,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(json.loads(r.stdout)['status'],'rolled-back')
        self.assertEqual(apply_plan(p,a,self.root,self.state)['status'],'applied')
        # Also recover real old-engine work interrupted AFTER its first file write.
        partial=self.base/'partial';partial.mkdir();partial_state=self.base/'partial-state'
        for name,content in json.loads((ROOT/'tests/fixtures/manifest-v2-030-output.json').read_text()).items():
            path=partial/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
        baseline=snapshot(partial)
        subprocess.run([sys.executable,'-c',script,str(partial),str(partial_state),str(self.base),'after-write'],cwd=old,check=True)
        self.assertNotEqual(snapshot(partial),baseline)
        command[command.index('--target')+1]=str(partial)
        command[command.index('--state-dir')+1]=str(partial_state)
        result=subprocess.run(command,cwd=old,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(snapshot(partial),baseline)
        fresh=make_plan(self.a,partial)
        self.assertEqual(apply_plan(fresh,approve(fresh,partial,'Synthetic migration'),partial,partial_state)['status'],'applied')

    def test_old_manifest_unknown_version_and_managed_agents_edit_block(self):
        manifest=self.root/'.adaptive-harness/manifest.json'
        original=manifest.read_text();data=json.loads(original)
        data['versions']['generator']='99.0.0';manifest.write_text(json.dumps(data))
        self.assertEqual(make_plan(self.a,self.root)['status'],'blocked')
        manifest.write_text(original)
        agents=self.root/'AGENTS.md';text=agents.read_text()
        agents.write_text(text.replace('Adaptive','User customized Adaptive',1))
        self.assertEqual(make_plan(self.a,self.root)['status'],'blocked')
