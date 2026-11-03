import json
import tempfile
import unittest
from pathlib import Path
from adaptive_harness.contracts import HarnessError
from adaptive_harness.core import make_plan
from adaptive_harness.apply import approve, apply_plan
from test_selection import fixture

class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name)
        self.root=self.base/'target';self.root.mkdir();self.state=self.base/'state'
        self.a=fixture();self.a['feature_size']='M'
        p=make_plan(self.a,self.root)
        apply_plan(p,approve(p,self.root,'Synthetic consent'),self.root,self.state)
    def tearDown(self):self.temp.cleanup()
    def test_managed_block_edits_block_approval(self):
        path=self.root/'AGENTS.md';path.write_text(path.read_text().replace('# Adaptive Developer Harness','# User edit'))
        before=path.read_bytes();p=make_plan(self.a,self.root)
        self.assertEqual(p['status'],'blocked')
        with self.assertRaises(HarnessError):approve(p,self.root,'test')
        self.assertEqual(path.read_bytes(),before)
    def test_outside_block_edits_preserved(self):
        path=self.root/'AGENTS.md';path.write_text('User prefix\n'+path.read_text()+'User suffix\n')
        p=make_plan(self.a,self.root)
        apply_plan(p,approve(p,self.root,'Synthetic consent'),self.root,self.state)
        self.assertTrue(path.read_text().startswith('User prefix\n'))
        self.assertTrue(path.read_text().endswith('User suffix\n'))
    def test_deselected_files_stay_in_inventory(self):
        old=json.loads((self.root/'.adaptive-harness/manifest.json').read_text())
        a=fixture();p=make_plan(a,self.root)
        apply_plan(p,approve(p,self.root,'Synthetic consent'),self.root,self.state)
        current=json.loads((self.root/'.adaptive-harness/manifest.json').read_text())
        self.assertTrue(current['pending_removal'])
        self.assertTrue(set(old['files'])<=set(current['files']))
        self.assertTrue(all((self.root/n).is_file() for n in current['pending_removal']))
        self.assertEqual(make_plan(a,self.root)['operations'],[])
    def test_edited_obsolete_file_still_blocks(self):
        path=self.root/'.adaptive-harness/templates/feature.md';path.write_text('user work')
        p=make_plan(fixture(),self.root)
        self.assertEqual(p['status'],'blocked');self.assertEqual(path.read_text(),'user work')
        manifest=json.loads(next(o['content'] for o in p['operations'] if o['path'].endswith('manifest.json')))
        self.assertIn('.adaptive-harness/templates/feature.md',manifest['pending_removal'])

class UpdateTests(IntegrityTests):
    # Inherited integrity cases also exercise this update fixture.
    def update_plan(self):return make_plan(fixture(),self.root,remove_obsolete=True)
    def test_approved_removal_and_repeat(self):
        from adaptive_harness.apply import verify
        p=self.update_plan();removed=p['expected_absent'];self.assertTrue(removed)
        self.assertTrue(all((self.root/n).exists() for n in removed))
        with self.assertRaises(HarnessError):apply_plan(p,{},self.root,self.state)
        a=approve(p,self.root,'Synthetic explicit delete consent')
        apply_plan(p,a,self.root,self.state)
        self.assertTrue(all(not (self.root/n).exists() for n in removed))
        self.assertEqual(apply_plan(p,a,self.root,self.state)['status'],'already-applied')
        self.assertEqual(make_plan(fixture(),self.root,remove_obsolete=True)['operations'],[])
        self.assertEqual(verify(p,self.root)['status'],'not-verified')
        path=self.root/removed[0];path.write_text('restored by user')
        self.assertEqual(verify(p,self.root)['status'],'fail')
    def test_pending_then_explicit_removal(self):
        p=make_plan(fixture(),self.root)
        apply_plan(p,approve(p,self.root,'Keep pending files'),self.root,self.state)
        pending=json.loads((self.root/'.adaptive-harness/manifest.json').read_text())['pending_removal']
        q=self.update_plan();self.assertEqual(q['expected_absent'],pending)
        apply_plan(q,approve(q,self.root,'Remove pending files'),self.root,self.state)
        self.assertFalse(json.loads((self.root/'.adaptive-harness/manifest.json').read_text())['pending_removal'])
    def test_changed_obsolete_file_cannot_be_deleted(self):
        p=self.update_plan();path=self.root/p['expected_absent'][0];path.write_text('user customization')
        q=self.update_plan();self.assertEqual(q['status'],'blocked')
        with self.assertRaises(HarnessError):approve(q,self.root,'test')
        self.assertEqual(path.read_text(),'user customization')
    def test_removed_managed_block_blocks(self):
        (self.root/'AGENTS.md').write_text('User replaced the file')
        self.assertEqual(self.update_plan()['status'],'blocked')
    def test_unknown_versions_and_forged_ownership_block(self):
        path=self.root/'.adaptive-harness/manifest.json';original=path.read_text()
        for defect in ('version','path','hash'):
            m=json.loads(original)
            if defect=='version':m['versions']['generator']='999.0'
            elif defect=='path':
                m['files']['.adaptive-harness/user-notes.md']='a'*64
                m['provenance']['.adaptive-harness/user-notes.md']=m['provenance']['AGENTS.md']
            else:m['files']['.adaptive-harness/templates/feature.md']='b'*64
            path.write_text(json.dumps(m))
            self.assertEqual(self.update_plan()['status'],'blocked',defect)
        path.write_text(original)
    def test_delete_interrupt_recovers_and_preserves_new_user_files(self):
        from unittest.mock import patch
        from adaptive_harness import apply as module
        from adaptive_harness.filesystem import snapshot
        p=self.update_plan();a=approve(p,self.root,'Synthetic delete consent');before=snapshot(self.root)
        real=module._delete
        def interrupt(*args):real(*args);raise KeyboardInterrupt()
        with patch.object(module,'_delete',interrupt),self.assertRaises(KeyboardInterrupt):
            apply_plan(p,a,self.root,self.state)
        self.assertEqual(module.recover(p,a,self.root,self.state)['status'],'rolled-back')
        self.assertEqual(snapshot(self.root),before)
        with patch.object(module,'_delete',interrupt),self.assertRaises(KeyboardInterrupt):
            apply_plan(p,a,self.root,self.state)
        edited=self.root/p['expected_absent'][0];edited.write_text('New user work')
        self.assertEqual(module.recover(p,a,self.root,self.state)['status'],'needs-recovery')
        self.assertEqual(edited.read_text(),'New user work')
    def test_failure_after_deletes_rolls_back(self):
        from unittest.mock import patch
        from adaptive_harness import apply as module
        from adaptive_harness.filesystem import snapshot
        p=self.update_plan();a=approve(p,self.root,'Synthetic delete consent');before=snapshot(self.root)
        real=module._atomic;calls=0
        def fail(*args,**kwargs):
            nonlocal calls
            calls+=1
            if calls==1:raise OSError('Synthetic write failure after deletes')
            return real(*args,**kwargs)
        with patch.object(module,'_atomic',fail),self.assertRaises(HarnessError):apply_plan(p,a,self.root,self.state)
        self.assertEqual(snapshot(self.root),before)
    def test_kept_shared_files_are_not_removed(self):
        p=self.update_plan()
        self.assertNotIn('.agents/skills/adh-verify/SKILL.md',p['expected_absent'])
        self.assertNotIn('.adaptive-harness/templates/handoff.md',p['expected_absent'])
    def test_inventory_versions(self):
        from adaptive_harness.inventory import inspect_inventory
        r=inspect_inventory(self.root)
        self.assertEqual(r['status'],'installed');self.assertEqual(r['versions']['generator'],'0.5.1')
        self.assertTrue(r['components']);self.assertTrue(all(c['revision'] for c in r['components'].values()))

    def test_every_delete_boundary_recovers(self):
        from unittest.mock import patch
        from adaptive_harness import apply as module
        from adaptive_harness.filesystem import snapshot
        p=self.update_plan();a=approve(p,self.root,'Synthetic removal consent');before=snapshot(self.root)
        real=module._delete
        for boundary in range(1,len(p['expected_absent'])+1):
            calls=0
            def interrupt(*args):
                nonlocal calls
                real(*args);calls+=1
                if calls==boundary:raise KeyboardInterrupt()
            with patch.object(module,'_delete',interrupt),self.assertRaises(KeyboardInterrupt):
                apply_plan(p,a,self.root,self.state)
            self.assertEqual(module.recover(p,a,self.root,self.state)['status'],'rolled-back')
            self.assertEqual(snapshot(self.root),before)
    def test_cursor_update_removes_only_managed_native_reviewer(self):
        a=fixture();a['host']['name']='cursor'
        (self.root/'.cursor').mkdir();(self.root/'.cursor/user.txt').write_text('user instructions')
        p=make_plan(a,self.root,remove_obsolete=True)
        self.assertIn('.codex/agents/adh-reviewer.toml',p['expected_absent'])
        apply_plan(p,approve(p,self.root,'Synthetic Cursor transition consent'),self.root,self.state)
        self.assertEqual((self.root/'.cursor/user.txt').read_text(),'user instructions')
        self.assertEqual(make_plan(a,self.root,remove_obsolete=True)['operations'],[])
    def test_shared_module_file_is_retained(self):
        from unittest.mock import patch
        from adaptive_harness.core import load_catalog
        catalog=load_catalog()
        for module in catalog['modules']:
            if module['id']=='quality.independent-review':module['files'].append('.agents/skills/adh-verify/SKILL.md')
        with patch('adaptive_harness.core.load_catalog',return_value=catalog):
            p=make_plan(self.a,self.root)
            apply_plan(p,approve(p,self.root,'Synthetic shared ownership consent'),self.root,self.state)
            q=self.update_plan()
            self.assertNotIn('.agents/skills/adh-verify/SKILL.md',q['expected_absent'])
            apply_plan(q,approve(q,self.root,'Synthetic removal consent'),self.root,self.state)
            m=json.loads((self.root/'.adaptive-harness/manifest.json').read_text())
            self.assertEqual(m['owners']['.agents/skills/adh-verify/SKILL.md'],['core.test-baseline'])

class MigrationTests(unittest.TestCase):
    def test_actual_v1_output_migrates_and_repeats(self):
        from adaptive_harness.contracts import ROOT
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'target';root.mkdir()
            files=json.loads((ROOT/'tests/fixtures/manifest-v1-output.json').read_text())
            for name,content in files.items():
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
            a=fixture();a['feature_size']='M';p=make_plan(a,root)
            self.assertEqual(p['status'],'ready-for-approval',p['blockers'])
            self.assertEqual(p['update']['migration'],'manifest-1-to-2')
            self.assertEqual(p['update']['installed_versions']['generator'],'unknown')
            apply_plan(p,approve(p,root,'Synthetic migration consent'),root,Path(temp)/'state')
            self.assertEqual(json.loads((root/'.adaptive-harness/manifest.json').read_text())['schema_version'],'2.0')
            self.assertEqual(make_plan(a,root)['operations'],[])
    def test_legacy_customization_not_overwritten(self):
        from adaptive_harness.contracts import ROOT
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            files=json.loads((ROOT/'tests/fixtures/manifest-v1-output.json').read_text())
            for name,content in files.items():
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
            path=root/'AGENTS.md';path.write_text(path.read_text()+'User legacy addition')
            p=make_plan(fixture(),root,remove_obsolete=True)
            self.assertEqual(p['status'],'blocked')
            self.assertTrue(path.read_text().endswith('User legacy addition'))

    def test_interrupted_legacy_migration_recovers_after_prd_change(self):
        from unittest.mock import patch
        from adaptive_harness import apply as module
        from adaptive_harness.contracts import ROOT,digest
        from adaptive_harness.filesystem import snapshot
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp);root=base/'target';root.mkdir();state=base/'state'
            files=json.loads((ROOT/'tests/fixtures/manifest-v1-output.json').read_text())
            for name,content in files.items():
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
            prd=base/'PRD.md';prd.write_text('Synthetic changed requirements')
            a=fixture();a['prd']={'source':str(prd),'sha256':digest(prd.read_bytes())}
            p=make_plan(a,root,remove_obsolete=True);approval=approve(p,root,'Synthetic migration consent')
            before=snapshot(root);real=module._delete
            def interrupt(*args):real(*args);raise KeyboardInterrupt()
            with patch.object(module,'_delete',interrupt),self.assertRaises(KeyboardInterrupt):
                apply_plan(p,approval,root,state)
            prd.write_text('New user requirements after interruption')
            self.assertEqual(module.recover(p,approval,root,state)['status'],'rolled-back')
            self.assertEqual(snapshot(root),before)
            with self.assertRaises(HarnessError):apply_plan(p,approval,root,state)
