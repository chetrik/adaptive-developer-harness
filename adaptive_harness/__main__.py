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
    p=sub.add_parser('bootstrap'); p.add_argument('--prd',required=True); p.add_argument('--url',required=True); p.add_argument('--target'); p.add_argument('--platform',default='codex',choices=('codex','cursor','claude-code','antigravity','lovable'))
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
    p=sub.add_parser('interpret');p.add_argument('--prd',required=True);p.add_argument('--model',required=True);p.add_argument('--target');p.add_argument('--platform',default='codex',choices=('codex','cursor','claude-code','antigravity','lovable'));p.add_argument('--endpoint',default='http://127.0.0.1:11434');p.add_argument('--timeout',type=float,default=60)
    p=sub.add_parser('inspect-project');p.add_argument('--target',required=True)
    p=sub.add_parser('inspect-export');p.add_argument('--archive',required=True)
    p=sub.add_parser('export-project');p.add_argument('--target',required=True);p.add_argument('--files',required=True);p.add_argument('--output',required=True);p.add_argument('--confirmation',required=True)
    p=sub.add_parser('doctor');p.add_argument('--platform',default='codex');p.add_argument('--target')
    p=sub.add_parser('package-skills');p.add_argument('--target',required=True);p.add_argument('--output-dir',required=True);p.add_argument('--confirmation',required=True)
    p=sub.add_parser('check-instructions');p.add_argument('--target',required=True);p.add_argument('--project-instructions',required=True);p.add_argument('--workspace-instructions')
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
        elif args.command in ('inspect-project','inspect-export','export-project'):
            from .project_handoff import inspect_project,inspect_archive,export_project
            if args.command=='inspect-project':result=inspect_project(args.target)
            elif args.command=='inspect-export':result=inspect_archive(args.archive)
            else:result=export_project(args.target,read_json(args.files),args.output,args.confirmation)
        elif args.command in ('package-skills','check-instructions'):
            from .integrations import package_skills,check_instructions
            if args.command=='package-skills':result=package_skills(args.target,args.output_dir,args.confirmation)
            else:result=check_instructions(args.target,args.project_instructions,args.workspace_instructions)
        elif args.command=='doctor':
            from .diagnostics import diagnose
            result=diagnose(args.platform,args.target)
        elif args.command=='interpret':
            from .provider import ollama_assessment
            result=ollama_assessment(args.prd,args.model,target=args.target,platform=args.platform,endpoint=args.endpoint,timeout=args.timeout)
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
