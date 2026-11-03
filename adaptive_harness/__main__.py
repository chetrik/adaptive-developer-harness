"""Small agent interface. End users may work entirely through their coding agent."""
import argparse
import difflib
import json
import sys
from pathlib import Path
from .contracts import HarnessError, read_json
from .core import make_plan, explain
from .apply import approve, apply_plan, verify, recover
from .bootstrap import intake
from .research import inspect_repository


def main(argv=None):
    parser=argparse.ArgumentParser(description='Adaptive Harness: agent-operated plan/approve/apply/validate')
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('bootstrap'); p.add_argument('--prd',required=True); p.add_argument('--url',required=True); p.add_argument('--target'); p.add_argument('--platform',default='codex',choices=('codex','cursor'))
    p=sub.add_parser('research'); p.add_argument('--url',required=True)
    p=sub.add_parser('plan'); p.add_argument('--assessment',required=True); p.add_argument('--target',required=True); p.add_argument('--remove-obsolete',action='store_true'); p.add_argument('--engineering')
    p=sub.add_parser('inventory'); p.add_argument('--target',required=True)
    p=sub.add_parser('handoff-plan'); p.add_argument('--assessment',required=True); p.add_argument('--record',required=True); p.add_argument('--target',required=True); p.add_argument('--engineering')
    p=sub.add_parser('resume'); p.add_argument('--target',required=True); p.add_argument('--session-id',required=True)
    p=sub.add_parser('explain'); p.add_argument('--plan',required=True)
    p=sub.add_parser('preview'); p.add_argument('--plan',required=True); p.add_argument('--target',required=True)
    p=sub.add_parser('approve'); p.add_argument('--plan',required=True); p.add_argument('--target',required=True); p.add_argument('--confirmation',required=True)
    for name in ('apply','recover'):
        p=sub.add_parser(name); p.add_argument('--plan',required=True); p.add_argument('--approval',required=True); p.add_argument('--target',required=True); p.add_argument('--state-dir',required=True)
    p=sub.add_parser('validate'); p.add_argument('--plan',required=True); p.add_argument('--target',required=True)
    for command in ('gate','approve-spec','read-context','test-run'):
        p=sub.add_parser(command); p.add_argument('--task',required=True); p.add_argument('--target',required=True); p.add_argument('--evidence-dir',required=True)
        if command=='gate':
            p.add_argument('--assessment',required=True); p.add_argument('--transition',choices=('implementation','verification','complete'),default='implementation'); p.add_argument('--receipts')
        if command=='approve-spec':p.add_argument('--confirmation',required=True)
        if command=='test-run':
            p.add_argument('--execution-confirmation',required=True); p.add_argument('--phase',choices=('red','green'),default='green'); p.add_argument('--start',default='tests'); p.add_argument('--pattern',default='test*.py'); p.add_argument('--timeout',type=float,default=30)
    args=parser.parse_args(argv)
    try:
        if args.command in ('gate','approve-spec','read-context','test-run'):
            from .evidence import approve_spec,load_context
            task=read_json(args.task)
            if args.command=='approve-spec':result={'receipt':approve_spec(task,args.target,args.evidence_dir,args.confirmation),'scope':'Specification only; not install or test execution permission'}
            elif args.command=='read-context':result=load_context(task,args.target,args.evidence_dir)
            elif args.command=='test-run':
                from .verification import run_tests
                result=run_tests(task,args.target,args.evidence_dir,args.execution_confirmation,phase=args.phase,start=args.start,pattern=args.pattern,timeout=args.timeout)
            else:
                from .gates import evaluate
                result=evaluate(read_json(args.assessment),task,args.target,args.evidence_dir,transition=args.transition,receipts=read_json(args.receipts) if args.receipts else {})
        elif args.command=='bootstrap': result=intake(args.prd,args.url,args.target,args.platform)
        elif args.command=='research': result=inspect_repository(args.url)
        elif args.command=='plan': result=make_plan(read_json(args.assessment),args.target,remove_obsolete=args.remove_obsolete,engineering=read_json(args.engineering) if args.engineering else None)
        elif args.command=='handoff-plan': result=make_plan(read_json(args.assessment),args.target,handoff=read_json(args.record),engineering=read_json(args.engineering) if args.engineering else None)
        elif args.command=='resume':
            from .handoff import resume
            result=resume(args.target,args.session_id)
        elif args.command=='inventory':
            from .inventory import inspect_inventory
            result=inspect_inventory(args.target)
        else:
            plan=read_json(args.plan)
            if args.command=='explain':
                print(explain(plan),end=''); return 0
            if args.command=='preview':
                from .core import check_plan
                from .filesystem import root_path, safe_path, read_regular
                # Blocked plans are shown via explain; exact approvable diff requires valid inputs.
                check_plan(plan,args.target)
                for op in plan['operations']:
                    path=safe_path(root_path(args.target),op['path'])
                    old=read_regular(path).decode() if path.exists() else ''
                    print(''.join(difflib.unified_diff(old.splitlines(True),op['content'].splitlines(True),fromfile=op['path']+' (before)',tofile=op['path']+' (after)')),end='')
                return 0
            if args.command=='approve': result=approve(plan,args.target,args.confirmation)
            elif args.command=='apply': result=apply_plan(plan,read_json(args.approval),args.target,args.state_dir)
            elif args.command=='recover': result=recover(plan,read_json(args.approval),args.target,args.state_dir)
            else: result=verify(plan,args.target)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        if args.command=='gate' and not result['allowed']:return 2
        if args.command=='test-run' and result['status']=='not-verified':return 2
        if result.get('status') in ('blocked','fail','needs-recovery','stale'): return 2
        return 0
    except (HarnessError,OSError,ValueError,KeyError) as exc:
        print('Помилка: '+str(exc),file=sys.stderr); return 2

if __name__=='__main__':
    raise SystemExit(main())
