"""Explicit approval, journalled writes and conservative recovery."""
import fcntl
import json
import os
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from .contracts import HarnessError, canonical, digest, fingerprint, validate, read_json
from .core import check_plan
from .filesystem import root_path, safe_path, read_regular, snapshot


def approve(plan, target, confirmation):
    check_plan(plan,target)
    if not confirmation or not confirmation.strip():
        raise HarnessError('Explicit human confirmation reference is required')
    return validate('approval',{'schema_version':'1.0','plan_id':plan['plan_id'],
        'target_snapshot':plan['target_snapshot'],'target':plan['target'],'decision':'approved',
        'confirmation':confirmation,'recorded_at':datetime.now(timezone.utc).isoformat()})


def check_approval(plan, approval):
    validate('approval',approval)
    if any(approval[k]!=plan[k] for k in ('plan_id','target_snapshot','target')):
        raise HarnessError('Approval does not match this plan and target state')


def _parent(root, name, created=None):
    """Anchor every ancestor to an open directory, refusing symlink traversal."""
    parts=Path(name).parts
    fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    prefix=[]
    try:
        for part in parts[:-1]:
            prefix.append(part)
            try:
                next_fd=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
            except FileNotFoundError:
                if created is None: raise
                os.mkdir(part,0o755,dir_fd=fd)
                if '/'.join(prefix) not in created: created.append('/'.join(prefix))
                next_fd=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
            os.close(fd); fd=next_fd
        return fd,parts[-1]
    except BaseException:
        os.close(fd); raise


def _atomic(root, name, content, expected, created, mode=0o644):
    safe_path(root,name)
    if mode & ~0o777: raise HarnessError('Special permission bits are not supported')
    fd,leaf=_parent(root,name,created)
    temp='.'+leaf+'.adh-'+os.urandom(8).hex()
    try:
        try:
            current=os.open(leaf,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
        except FileNotFoundError:
            actual=None
        else:
            with os.fdopen(current,'rb') as stream:
                if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode): raise HarnessError('Nonregular destination')
                actual=digest(stream.read())
        if actual!=expected: raise HarnessError('File changed immediately before write')
        out=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,mode,dir_fd=fd)
        with os.fdopen(out,'wb') as stream:
            stream.write(content); stream.flush(); os.fsync(stream.fileno())
        if expected is None:
            # Atomic no-clobber creation even if another writer creates the destination.
            os.link(temp,leaf,src_dir_fd=fd,dst_dir_fd=fd,follow_symlinks=False)
            os.unlink(temp,dir_fd=fd)
        else:
            os.replace(temp,leaf,src_dir_fd=fd,dst_dir_fd=fd)
        os.fsync(fd)
    finally:
        try: os.unlink(temp,dir_fd=fd)
        except FileNotFoundError: pass
        os.close(fd)


def _state_dir(state_dir, root):
    state=Path(os.path.abspath(state_dir))
    if state==root or root in state.parents:
        raise HarnessError('State directory must be outside target')
    for p in [state,*state.parents]:
        if p.is_symlink(): raise HarnessError('Unsafe state directory')
    state.mkdir(parents=True,exist_ok=True,mode=0o700)
    return state


def _save(path, value):
    if path.is_symlink(): raise HarnessError('Unsafe state file')
    temp=path.with_name(path.name+'.tmp-'+os.urandom(6).hex())
    try:
        with os.fdopen(os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600),'w',encoding='utf-8') as stream:
            stream.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
            stream.flush(); os.fsync(stream.fileno())
        os.replace(temp,path)
    finally:
        temp.unlink(missing_ok=True)


def _rollback(root, journal):
    errors=[]
    for item in reversed(journal['items']):
        path=safe_path(root,item['path'])
        current=digest(read_regular(path)) if path.exists() else None
        if current==item['before']: continue
        if current!=item['after']:
            errors.append(item['path']); continue
        if item['before'] is None:
            fd,leaf=_parent(root,item['path'])
            try: os.unlink(leaf,dir_fd=fd)
            finally: os.close(fd)
        else:
            _atomic(root,item['path'],bytes.fromhex(item['backup']),item['after'],[],item['mode'])
    for name in reversed(journal['directories']):
        try:
            fd,leaf=_parent(root,name)
            try: os.rmdir(leaf,dir_fd=fd)
            finally: os.close(fd)
        except OSError: pass  # Never remove nonempty directories or user additions.
    return errors


def apply_plan(plan, approval, target, state_dir):
    root=root_path(target)
    check_approval(plan,approval)
    check_plan(plan,root,fresh=False)
    state=_state_dir(state_dir,root)
    lock=os.open(Path(tempfile.gettempdir())/('adh-lock-'+digest(str(root))),os.O_WRONLY|os.O_CREAT|os.O_NOFOLLOW|os.O_NONBLOCK,0o600)
    if not stat.S_ISREG(os.fstat(lock).st_mode):
        os.close(lock);raise HarnessError('Unsafe lock file')
    try:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        receipt_path=state/(plan['plan_id']+'.receipt.json')
        journal_path=state/(plan['plan_id']+'.journal.json')
        if receipt_path.exists():
            receipt=read_json(receipt_path)
            if receipt.get('plan_id')!=plan['plan_id'] or receipt.get('plan_digest')!=fingerprint(plan) or receipt.get('post_snapshot')!=snapshot(root):
                raise HarnessError('Applied target changed; a new plan is required')
            return validate('apply-result',{'schema_version':'1.0','plan_id':plan['plan_id'],'status':'already-applied','changed':[],'evidence':['Receipt and complete target snapshot match; no writes.']})
        if journal_path.exists() and read_json(journal_path).get('status') in ('writing','needs-recovery'):
            raise HarnessError('Interrupted operation; recover journal before applying')
        check_plan(plan,root)
        journal={'schema_version':'1.0','plan_id':plan['plan_id'],'target':str(root),'status':'writing','items':[],'directories':[]}
        # Prepare all backups before any target mutation.
        for op in plan['operations']:
            path=safe_path(root,op['path'])
            backup=read_regular(path) if path.exists() else b''
            journal['items'].append({'path':op['path'],'before':op['before'],'after':op['after'],
                'backup':backup.hex(),'mode':stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644})
        journal['directories']=sorted({str(parent) for op in plan['operations'] for parent in Path(op['path']).parents if str(parent)!='.' and not (root/parent).exists()},key=lambda x:(len(Path(x).parts),x))
        _save(journal_path,journal)
        try:
            for op,item in zip(plan['operations'],journal['items']):
                _atomic(root,op['path'],op['content'].encode(),op['before'],journal['directories'],item['mode'])
                _save(journal_path,journal)
            # Confirm every expected output before committing receipt.
            for op in plan['operations']:
                if digest(read_regular(safe_path(root,op['path'])))!=op['after']:
                    raise HarnessError('Output changed during Apply')
            receipt={'plan_id':plan['plan_id'],'plan_digest':fingerprint(plan),'post_snapshot':snapshot(root)}
            _save(receipt_path,receipt)
            journal['status']='applied'; _save(journal_path,journal)
        except Exception as exc:
            errors=_rollback(root,journal)
            journal['status']='needs-recovery' if errors else 'rolled-back'
            journal['conflicts']=errors
            _save(journal_path,journal)
            raise HarnessError('Apply failed; '+journal['status']) from exc
        return validate('apply-result',{'schema_version':'1.0','plan_id':plan['plan_id'],'status':'applied',
            'changed':[o['path'] for o in plan['operations']], 'evidence':['Exact approved contents written; recovery journal and receipt saved.','Application tests and native discovery are not verified by Apply.']})
    except BlockingIOError as exc:
        raise HarnessError('Another Apply holds the target lock') from exc
    finally:
        os.close(lock)


def _recover_locked(plan, approval, target, state_dir):
    root=root_path(target); check_approval(plan,approval); check_plan(plan,root,fresh=False)
    state=_state_dir(state_dir,root)
    path=state/(plan['plan_id']+'.journal.json')
    journal=read_json(path)
    if journal.get('target')!=str(root) or journal.get('plan_id')!=plan['plan_id'] or journal.get('status') not in ('writing','needs-recovery'):
        raise HarnessError('No matching interrupted journal')
    expected={o['path']:o for o in plan['operations']}
    if len(journal.get('items',[]))!=len(expected) or {i['path'] for i in journal['items']}!=set(expected):
        raise HarnessError('Incomplete or duplicate recovery journal')
    allowed_dirs={str(parent) for op in plan['operations'] for parent in Path(op['path']).parents if str(parent)!='.'}
    if not set(journal.get('directories',[]))<=allowed_dirs:
        raise HarnessError('Journal directory scope mismatch')
    for item in journal['items']:
        op=expected.get(item['path'])
        if not op or item['before']!=op['before'] or item['after']!=op['after']:
            raise HarnessError('Journal scope mismatch')
        if item['before'] is not None and digest(bytes.fromhex(item['backup']))!=item['before']:
            raise HarnessError('Journal backup mismatch')
    errors=_rollback(root,journal)
    journal['status']='needs-recovery' if errors else 'rolled-back'; journal['conflicts']=errors
    _save(path,journal)
    return {'status':journal['status'],'conflicts':errors}


def recover(plan, approval, target, state_dir):
    root=root_path(target)
    lock=os.open(Path(tempfile.gettempdir())/('adh-lock-'+digest(str(root))),os.O_WRONLY|os.O_CREAT|os.O_NOFOLLOW|os.O_NONBLOCK,0o600)
    try:
        if not stat.S_ISREG(os.fstat(lock).st_mode): raise HarnessError('Unsafe lock file')
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        return _recover_locked(plan,approval,target,state_dir)
    except BlockingIOError as exc:
        raise HarnessError('Another operation holds the target lock') from exc
    finally:
        os.close(lock)


def verify(plan, target):
    validate('plan-v1',plan)
    root=root_path(target)
    checks=[]
    if fingerprint({k:v for k,v in plan.items() if k!='plan_id'})!=plan['plan_id'] or str(root)!=plan['target']:
        raise HarnessError('Invalid plan identity')
    for name,expected in plan['expected_files'].items():
        path=safe_path(root,name)
        good=path.exists() and digest(read_regular(path))==expected
        checks.append({'name':name,'status':'pass' if good else 'fail','detail':'Expected content hash matches' if good else 'Missing or changed output'})
    checks += [{'name':name,'status':'not-verified','detail':'Requires separate observed execution evidence'} for name in ('application-tests','native-skill-discovery','independent-review')]
    return validate('validation-report',{'schema_version':'1.0','status':'fail' if any(c['status']=='fail' for c in checks) else 'not-verified','checks':checks})
