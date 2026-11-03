import copy
import json
import tempfile
import unittest
from pathlib import Path
from adaptive_harness.contracts import HarnessError,digest
from adaptive_harness.evidence import approve_spec,load_context,EvidenceStore
from adaptive_harness.gates import evaluate
from adaptive_harness.verification import run_tests
from test_selection import fixture


def task(root):
    return {'id':'calculator-fix','kind':'bugfix',
        'spec':{'goal':'Return the sum','scope':'Only addition behavior',
            'acceptance':[{'id':'AC-1','given':'two integers','when':'adding','then':'returns their sum','category':'behavior'}],
            'edge_cases':[],'nfr':{'applicability':'none','criteria':[],'reason':'No relevant throughput or service constraint for this local example'},'questions':[],'source':None},
        'context':[{'path':n,'sha256':digest((root/n).read_bytes()),'start':1,'end':1,'category':c,'critical':True} for n,c in [('AGENTS.md','rules'),('app.py','code')]],
        'code_paths':['app.py'],'test_paths':['tests/test_app.py'],'config_paths':[],
        'checks':[{'ac_id':'AC-1','test_id':'test_app.Addition.test_sum'}],
        'documentation':{'applicability':'none','paths':[],'reason':'Restores existing documented behavior; no documentation change'},'handoff_id':None}

class GatesTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name).resolve()
        self.root=self.base/'target';self.root.mkdir();self.state=self.base/'evidence'
        (self.root/'AGENTS.md').write_text('Use minimal scoped changes\n')
        (self.root/'app.py').write_text('def add(a,b): return a-b\n')
        (self.root/'tests').mkdir()
        (self.root/'tests/test_app.py').write_text('import unittest\nfrom app import add\nclass Addition(unittest.TestCase):\n def test_sum(self): self.assertEqual(add(2,3),5)\n')
        self.a=fixture();self.t=task(self.root)
    def tearDown(self):self.temp.cleanup()
    def receipts(self):
        return {'spec_approval':approve_spec(self.t,self.root,self.state,'Actual synthetic task approval'),
                'context':[x['receipt'] for x in load_context(self.t,self.root,self.state)['sources']]}
    def gate(self,r,transition='implementation'):
        return evaluate(self.a,self.t,self.root,self.state,transition=transition,receipts=r)
    def test_small_inline_spec_without_extra_files(self):
        for size in ('XS','S'):
            self.a['feature_size']=size;r=self.receipts()
            self.assertEqual(self.gate(r)['status'],'pass')
            self.assertFalse((self.root/'spec.md').exists())
    def test_complex_spec_missing_criteria_and_error_cases_blocks(self):
        self.a['feature_size']='L';self.t['spec']['acceptance']=[]
        result=self.gate(self.receipts())
        self.assertEqual(result['status'],'blocked')
        self.assertIn('spec.acceptance',[c['code'] for c in result['checks'] if c['status']=='blocked'])
    def test_critical_question_placeholder_unknown_and_risk(self):
        original=copy.deepcopy(self.t)
        for field in ('question','placeholder','unknown','risk'):
            self.t=copy.deepcopy(original);self.a=fixture()
            if field=='question':self.t['spec']['questions']=[{'text':'Which data may be public?','critical':True}]
            if field=='placeholder':self.t['spec']['goal']='TODO'
            if field=='unknown':self.t['spec']['nfr']['applicability']='unknown'
            if field=='risk':self.a['facts']['personal_data']['value']=True
            result=self.gate(self.receipts());self.assertFalse(result['allowed'])
            if field=='unknown':self.assertEqual(result['status'],'not-verified')
    def test_approval_context_missing_or_forged(self):
        self.assertEqual(self.gate({})['status'],'blocked')
        r=self.receipts();r['context']=[]
        self.assertEqual(self.gate(r)['status'],'not-verified')
        r=self.receipts();path=self.state/(r['spec_approval']+'.evidence.json')
        data=json.loads(path.read_text());data['body']['task']='f'*64;path.write_text(json.dumps(data))
        self.assertEqual(self.gate(r)['status'],'blocked')
    def test_changed_spec_and_critical_context_block(self):
        r=self.receipts();self.t['spec']['goal']='Different goal'
        self.assertEqual(self.gate(r)['status'],'blocked')
        self.t=task(self.root);r=self.receipts();(self.root/'AGENTS.md').write_text('Changed rules')
        self.assertEqual(self.gate(r)['status'],'blocked')
    def test_real_red_green_and_old_code_receipt_not_reused(self):
        r=self.receipts()
        red=run_tests(self.t,self.root,self.state,'Synthetic execution consent',phase='red')
        self.assertEqual(red['status'],'assertion-failure');r['red']=red['receipt']
        self.assertEqual(self.gate(r,'verification')['status'],'pass')
        (self.root/'app.py').write_text('def add(a,b): return a+b\n')
        green=run_tests(self.t,self.root,self.state,'Synthetic execution consent')
        self.assertEqual(green['status'],'pass');r['green']=green['receipt']
        self.assertEqual(self.gate(r,'complete')['status'],'pass')
        (self.root/'app.py').write_text('def add(a,b): return 99\n')
        self.assertEqual(self.gate(r,'complete')['status'],'blocked')
    def test_modified_test_cannot_manufacture_fix(self):
        r=self.receipts();r['red']=run_tests(self.t,self.root,self.state,'Synthetic consent',phase='red')['receipt']
        path=self.root/'tests/test_app.py';path.write_text(path.read_text().replace(',5)',',-1)'))
        (self.root/'app.py').write_text('def add(a,b): return a-b # fake fix\n')
        r['green']=run_tests(self.t,self.root,self.state,'Synthetic consent')['receipt']
        result=self.gate(r,'complete');self.assertEqual(result['status'],'blocked')
        self.assertIn('bugfix.stable-expectations',[c['code'] for c in result['checks'] if c['status']=='blocked'])
    def test_initial_green_no_red_not_verified(self):
        (self.root/'app.py').write_text('def add(a,b): return a+b\n');self.t=task(self.root)
        r=self.receipts();r['red']=run_tests(self.t,self.root,self.state,'Synthetic consent',phase='red')['receipt']
        r['green']=run_tests(self.t,self.root,self.state,'Synthetic consent')['receipt']
        self.assertFalse(self.gate(r,'complete')['allowed'])
    def test_self_report_never_satisfies_execution(self):
        r=self.receipts();r['red']='a'*64;r['green']='b'*64
        self.assertEqual(self.gate(r,'complete')['status'],'not-verified')
    def test_no_execution_without_separate_consent(self):
        self.receipts()
        with self.assertRaises(HarnessError):run_tests(self.t,self.root,self.state,'')
    def test_context_bounds_protected_paths_and_binary(self):
        for path in ('../outside','.env','.git/config','/tmp/secret'):
            bad=copy.deepcopy(self.t);bad['context'][0]['path']=path
            with self.assertRaises(HarnessError):load_context(bad,self.root,self.state)
        (self.root/'AGENTS.md').write_text('a'*33000+'\n');self.t=task(self.root)
        with self.assertRaisesRegex(HarnessError,'32 KiB'):load_context(self.t,self.root,self.state)
    def test_errors_skip_empty_timeout_and_output_limit_not_valid_red(self):
        tests=self.root/'tests/test_app.py'
        sources=[('import nonexistent_module_xyz\n',30),
                 ('import unittest\nclass T(unittest.TestCase):\n @unittest.skip("not available")\n def test_a(self): pass\n',30),
                 ('# no tests\n',30),
                 ('import time\ntime.sleep(5)\n',.1),
                 ('print("x"*150000)\n',30)]
        for source,timeout in sources:
            tests.write_text(source)
            result=run_tests(self.t,self.root,self.state,'Synthetic execution consent',phase='red',timeout=timeout)
            self.assertEqual(result['status'],'not-verified')

    def test_undeclared_fixture_change_blocks_red_green(self):
        extra=self.root/'fixture.json';extra.write_text('{"expected":5}')
        r=self.receipts();r['red']=run_tests(self.t,self.root,self.state,'Synthetic consent',phase='red')['receipt']
        extra.write_text('{"expected":-1}')
        (self.root/'app.py').write_text('def add(a,b): return a+b\n')
        r['green']=run_tests(self.t,self.root,self.state,'Synthetic consent')['receipt']
        self.assertEqual(self.gate(r,'complete')['status'],'blocked')

    def test_malformed_receipts_rejected(self):
        with self.assertRaises(HarnessError):self.gate({'context':True})

    def test_greenfield_allows_planned_code_without_fake_read(self):
        (self.root/'app.py').unlink();self.t['kind']='feature'
        self.t['context']=self.t['context'][:1]
        self.assertEqual(self.gate(self.receipts())['status'],'pass')
        self.assertEqual(self.gate(self.receipts(),'verification')['status'],'blocked')

    def test_overlapping_code_and_test_roles_block(self):
        self.t['code_paths'].append('tests/test_app.py')
        self.assertEqual(self.gate(self.receipts())['status'],'blocked')

    def test_shared_plan_handoff_and_stale_receipts_for_both_adapters(self):
        from adaptive_harness.core import make_plan,check_plan
        from adaptive_harness.apply import approve,apply_plan
        from test_handoff import record
        for host in ('codex','cursor'):
            with self.subTest(host=host):
                self.a['host']['name']=host
                p=make_plan(self.a,self.root)
                apply_plan(p,approve(p,self.root,'Synthetic install consent'),self.root,self.base/'apply-state')
                self.t=task(self.root);self.t['kind']='feature';r=self.receipts()
                engineering={'task':self.t,'receipts':r,'state_dir':str(self.state),'transition':'implementation'}
                p=make_plan(self.a,self.root,engineering=engineering)
                self.assertEqual(p['readiness']['status'],'pass');self.assertEqual(p['operations'],[])
                check_plan(p,self.root)
                h=record();h['session_id']='gates-'+host
                hp=make_plan(self.a,self.root,handoff=h,engineering=engineering)
                apply_plan(hp,approve(hp,self.root,'Synthetic checkpoint consent'),self.root,self.base/'apply-state')
                saved=json.loads((self.root/('.adaptive-harness/sessions/'+h['session_id']+'.json')).read_text())
                self.assertEqual(saved['readiness']['status'],'pass')
                receipt=self.state/(r['spec_approval']+'.evidence.json');receipt.unlink()
                with self.assertRaises(HarnessError):check_plan(p,self.root)

    def test_cli_read_approve_gate_and_run(self):
        import contextlib,io
        from adaptive_harness.__main__ import main
        taskpath=self.base/'task.json';taskpath.write_text(json.dumps(self.t))
        assessment=self.base/'assessment.json';assessment.write_text(json.dumps(self.a))
        receiptpath=self.base/'receipts.json'
        common=['--task',str(taskpath),'--target',str(self.root),'--evidence-dir',str(self.state)]
        def invoke(command,extra=[]):
            output=io.StringIO()
            with contextlib.redirect_stdout(output):code=main([command]+common+extra)
            return code,json.loads(output.getvalue())
        self.assertEqual(invoke('gate',['--assessment',str(assessment)])[0],2)
        _,approval=invoke('approve-spec',['--confirmation','Synthetic actual task instruction'])
        _,context=invoke('read-context')
        receiptpath.write_text(json.dumps({'spec_approval':approval['receipt'],'context':[s['receipt'] for s in context['sources']]}))
        self.assertEqual(invoke('gate',['--assessment',str(assessment),'--receipts',str(receiptpath)])[0],0)
        _,run=invoke('test-run',['--execution-confirmation','Synthetic host consent','--phase','red'])
        self.assertEqual(run['status'],'assertion-failure')
