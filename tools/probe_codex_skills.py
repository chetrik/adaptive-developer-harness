#!/usr/bin/env python3
"""Read-only native discovery probe. Starts no model turn and executes no Skill."""
import argparse
import json
import selectors
import subprocess
import tempfile
import time
from pathlib import Path


def probe(target):
    with tempfile.TemporaryDirectory(prefix='adh-codex-probe-') as temp:
        base=Path(temp)
        proc=subprocess.Popen(['codex','-c',f'sqlite_home="{base}/sqlite"','-c',f'log_dir="{base}/logs"','app-server','--stdio'],
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,bufsize=1,cwd=target)
        selector=selectors.DefaultSelector();selector.register(proc.stdout,selectors.EVENT_READ)
        def send(value):
            proc.stdin.write(json.dumps(value)+'\n');proc.stdin.flush()
        def receive(request_id):
            end=time.monotonic()+20
            while time.monotonic()<end:
                if proc.poll() is not None:
                    raise RuntimeError('Codex app-server exited; check host permissions for its service cache')
                for key,_ in selector.select(1):
                    line=key.fileobj.readline()
                    if line:
                        try:value=json.loads(line)
                        except ValueError:continue
                        if value.get('id')==request_id:return value
            raise RuntimeError('Codex discovery timed out; capability not verified')
        try:
            send({'id':1,'method':'initialize','params':{'clientInfo':{'name':'adh_discovery_probe','version':'0.1.0'},'capabilities':{'experimentalApi':True}}})
            if 'error' in receive(1):raise RuntimeError('Codex initialization rejected')
            send({'method':'initialized','params':{}})
            send({'id':2,'method':'skills/list','params':{'cwds':[str(target)],'forceReload':True}})
            response=receive(2)
            if 'error' in response:raise RuntimeError('Codex skills/list rejected')
            found=[]
            def walk(value):
                if isinstance(value,dict):
                    if isinstance(value.get('name'),str) and value['name'].startswith('adh-'):
                        found.append({'name':value['name'],'path':value.get('path')})
                    for nested in value.values():walk(nested)
                elif isinstance(value,list):
                    for nested in value:walk(nested)
            walk(response.get('result',{}))
            expected={p.parent.name for p in (target/'.agents/skills').glob('adh-*/SKILL.md')}
            actual={item['name'] for item in found}
            return {'status':'pass' if expected and expected<=actual else 'not-verified','expected':sorted(expected),
                    'discovered':found,'scope':'Native Skill discovery only; model invocation and subagents not tested.'}
        finally:
            selector.close();proc.terminate()
            try:proc.wait(timeout=5)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--target',required=True);args=parser.parse_args()
    try:result=probe(Path(args.target).resolve())
    except (OSError,RuntimeError) as exc:result={'status':'not-verified','reason':str(exc)}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['status']=='pass' else 2)
