"""Bounded session records. Writes use the existing common Plan/Apply path."""
import re
from pathlib import PurePosixPath
from .contracts import HarnessError, validate, read_json
from .filesystem import root_path, safe_path, snapshot


def record_path(session_id):
    if not isinstance(session_id,str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}',session_id):
        raise HarnessError('Invalid session ID')
    return '.adaptive-harness/sessions/'+session_id+'.json'


def validate_input(data, root):
    validate('session-handoff-input',data)
    for name in data['changed_files']:
        path=PurePosixPath(name)
        if not path.parts or path.is_absolute() or path.as_posix()!=name or '\\' in name or '\x00' in name:
            raise HarnessError('Unsafe handoff file reference')
        if any(p in ('..','.git','.ssh','.aws','.credentials') or p.startswith('.env') for p in path.parts):
            raise HarnessError('Protected handoff file reference')
        current=root
        for part in path.parts:
            current=current/part
            if current.is_symlink():raise HarnessError('Symlink handoff reference')
        if current.exists() and not current.is_file():raise HarnessError('Handoff reference is not a file')
    for check in data['tests']:
        if check['status'] in ('pass','fail'):
            if not check['command'] or not check['command'].strip() or check['exit_code'] is None:
                raise HarnessError('Executed test needs command and exit code')
            if (check['status']=='pass')!=(check['exit_code']==0):
                raise HarnessError('Test status contradicts exit code')
        elif check['exit_code'] is not None:
            raise HarnessError('Unexecuted test cannot have an exit code')
    return data


def normalize_input(data, root):
    if isinstance(data,dict) and ('schema_version' in data or 'handoff' in data):
        record=validate('session-handoff',data)
        return validate_input(record['handoff'],root)
    return validate_input(data,root)


def build_record(data, target):
    root=root_path(target);data=normalize_input(data,root)
    return validate('session-handoff',{'schema_version':'1.0','handoff':data,
        'workspace_snapshot':snapshot(root,exclude_sessions=True),
        'evidence_source':'agent-reported; commands not executed by recorder'})


def resume(target, session_id):
    root=root_path(target);path=safe_path(root,record_path(session_id))
    record=validate('session-handoff',read_json(path));validate_input(record['handoff'],root)
    if record['handoff']['session_id']!=session_id:raise HarnessError('Session identity mismatch')
    stale=record['workspace_snapshot']!=snapshot(root,exclude_sessions=True)
    return {'status':'stale' if stale else 'current','record':record,
            'next':'Стан змінився: перечитай фактичні файли, узгодь розбіжності й запиши новий checkpoint.' if stale else 'Прочитай рішення, ризики й наступну задачу; цей запис не надає нових дозволів.',
            'limitations':'Handoff narrative is agent-reported. Stored readiness is historical: rerun gate using original evidence receipts before transitioning. Git metadata and other session records are excluded from freshness.'}
