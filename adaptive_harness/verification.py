"""Observed, bounded test execution feeding the existing workflow's gate evaluator."""
import json
import os
import re
import selectors
import signal
import subprocess
import sys
import time
from pathlib import Path
from .contracts import ROOT,HarnessError,digest,fingerprint
from .filesystem import root_path,snapshot
from .evidence import EvidenceStore,identity,source_path,hashes,fixed_inputs


def run_tests(task,target,state_dir,execution_confirmation,*,phase='green',start='tests',pattern='test*.py',timeout=30):
    if not execution_confirmation or not execution_confirmation.strip():raise HarnessError('Explicit test execution permission required; spec/install approval is not execution permission')
    if phase not in ('red','green') or not 0<timeout<=120:raise HarnessError('Invalid verification run limits')
    if not re.fullmatch(r'[A-Za-z0-9_.*?-]+\.py',pattern):raise HarnessError('Invalid test filename pattern')
    root=root_path(target);identity(task)
    # Validate directory ancestors through a nonexistent child reference, not a broad file read.
    source_path(root,start+'/.adh-reference')
    if not (root/start).is_dir():raise HarnessError('Test directory missing')
    store=EvidenceStore(state_dir,root)
    before=snapshot(root,exclude_sessions=True);code=hashes(root,task['code_paths'])
    tests=hashes(root,task['test_paths']);configs=hashes(root,task['config_paths']);fixed=fixed_inputs(root,task)
    if not tests or any(v is None for v in tests.values()):raise HarnessError('Declared regression tests must exist')
    argv=[sys.executable,'-B',str(ROOT/'adaptive_harness/verification_runner.py'),start,pattern]
    proc=subprocess.Popen(argv,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True)
    selector=selectors.DefaultSelector();selector.register(proc.stdout,selectors.EVENT_READ)
    output=bytearray();limit=None;deadline=time.monotonic()+timeout
    def stop():
        try:os.killpg(proc.pid,signal.SIGKILL)
        except ProcessLookupError:pass
    try:
        while selector.get_map():
            if time.monotonic()>deadline:limit='timeout';stop();break
            for key,_ in selector.select(min(.1,max(0,deadline-time.monotonic()))):
                chunk=os.read(key.fileobj.fileno(),8192)
                if not chunk:selector.unregister(key.fileobj);break
                output.extend(chunk)
                if len(output)>131072:limit='output-limit';stop();break
            if limit:break
        try:proc.wait(timeout=min(2,max(.01,deadline-time.monotonic())))
        except subprocess.TimeoutExpired:limit="timeout";stop();proc.wait()
    finally:
        if proc.poll() is None:stop();proc.wait()
        selector.close();proc.stdout.close()
        # Do not leave test-spawned background processes behind.
        stop()
    after=snapshot(root,exclude_sessions=True)
    result=None
    if not limit:
        try:
            line=bytes(output).split(b'\n_ADH_TEST_RESULT_')[-1]
            result=json.loads(line)
            fields=('count','passed','seen','failures','errors','skipped','unexpected_successes','expected_failures','failure_digest')
            if not isinstance(result,dict) or set(result)!=set(fields):result=None
        except (ValueError,TypeError):result=None
    classification='not-verified'
    if result and before==after:
        if result['count']>0 and not any(result[k] for k in ('errors','skipped','unexpected_successes','expected_failures')):
            if result['failures'] and proc.returncode==1:classification='assertion-failure'
            elif not result['failures'] and proc.returncode==0 and result['passed']:classification='pass'
    data={'phase':phase,'classification':classification,'result':result,'exit_code':proc.returncode,
        'limit':limit,'output_sha256':digest(bytes(output)),'workspace':after,'workspace_unchanged_during_run':before==after,
        'fixed_inputs':fixed,'code':code,'tests':tests,'configs':configs,'runner':'python-unittest-v1',
        'selection':{'start':start,'pattern':pattern},'observed_at_ns':time.time_ns(),
        'execution_confirmation':execution_confirmation}
    rid=store.issue('test-run',task,data)
    return {'receipt':rid,'status':classification,'result':result,'limit':limit,
            'scope':'Observed unittest only; no raw logs exported; host sandbox/permissions required'}
