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
    p=sub.add_parser('bootstrap'); p.add_argument('--prd',required=True); p.add_argument('--url',required=True); p.add_argument('--target')
    p=sub.add_parser('research'); p.add_argument('--url',required=True)
    p=sub.add_parser('plan'); p.add_argument('--assessment',required=True); p.add_argument('--target',required=True)
    p=sub.add_parser('explain'); p.add_argument('--plan',required=True)
    p=sub.add_parser('preview'); p.add_argument('--plan',required=True); p.add_argument('--target',required=True)
    p=sub.add_parser('approve'); p.add_argument('--plan',required=True); p.add_argument('--target',required=True); p.add_argument('--confirmation',required=True)
    for name in ('apply','recover'):
        p=sub.add_parser(name); p.add_argument('--plan',required=True); p.add_argument('--approval',required=True); p.add_argument('--target',required=True); p.add_argument('--state-dir',required=True)
    p=sub.add_parser('validate'); p.add_argument('--plan',required=True); p.add_argument('--target',required=True)
    args=parser.parse_args(argv)
    try:
        if args.command=='bootstrap': result=intake(args.prd,args.url,args.target)
        elif args.command=='research': result=inspect_repository(args.url)
        elif args.command=='plan': result=make_plan(read_json(args.assessment),args.target)
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
        if result.get('status') in ('blocked','fail','needs-recovery'): return 2
        return 0
    except (HarnessError,OSError,ValueError,KeyError) as exc:
        print('Помилка: '+str(exc),file=sys.stderr); return 2

if __name__=='__main__':
    raise SystemExit(main())
