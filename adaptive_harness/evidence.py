"""Host-owned external evidence receipts. Never writes customer project components.

HMAC detects accidental/tampered JSON, not a malicious owner of the host/key.
The same existing journal helper writes external state. Host permissions remain authority.
"""
import hmac
import json
import os
import secrets
import stat
from pathlib import Path, PurePosixPath
from .contracts import HarnessError,canonical,digest,fingerprint,validate
from .filesystem import root_path,read_regular,snapshot

MAX_CONTEXT_BYTES=32768
MAX_SOURCE_BYTES=1024*1024

def source_path(root, name):
    if not isinstance(name,str) or '\\' in name or '\x00' in name:raise HarnessError('Unsafe source path')
    p=PurePosixPath(name)
    if not p.parts or p.is_absolute() or p.as_posix()!=name or any(x in ('..','.git','.ssh','.aws','.credentials') or x.startswith('.env') for x in p.parts):
        raise HarnessError('Protected or noncanonical source path')
    cur=root
    for part in p.parts:
        cur=cur/part
        if cur.is_symlink():raise HarnessError('Symlink source path')
    if cur.exists() and not cur.is_file():raise HarnessError('Source is not a regular file')
    return cur

def hashes(root, paths):
    result={}
    for name in paths:
        p=source_path(root,name)
        result[name]=digest(read_regular(p)) if p.exists() else None
    return result

def fixed_inputs(root, task):
    """Bind regression expectations and other inputs outside approved implementation/docs paths.

All ordinary input bytes are hashed, not delivered to the model. Existing snapshot
limits apply first; secret-like paths are represented only by metadata.
"""
    snapshot(root,exclude_sessions=True)
    allowed=set(task['code_paths'])|set(task['documentation']['paths'])
    result={}
    for base,dirs,files in os.walk(root,followlinks=False):
        dirs[:]=sorted(d for d in dirs if d!='.git')
        if Path(base)==root/'.adaptive-harness':dirs[:]=[d for d in dirs if d!='sessions']
        for name in sorted(dirs+files):
            path=Path(base)/name;rel=path.relative_to(root).as_posix()
            if rel in allowed:continue
            st=path.lstat()
            if path.is_symlink():result[rel]=['symlink',os.readlink(path)]
            elif path.is_file():
                protected=any(p.startswith('.env') or p in ('.aws','.ssh','.credentials') for p in Path(rel).parts)
                result[rel]=['protected',st.st_size,st.st_mtime_ns,st.st_ino] if protected else digest(read_regular(path))
    return fingerprint(result)

def identity(task):
    validate('engineering-task',task)
    return fingerprint(task)

class EvidenceStore:
    def __init__(self, path, target):
        from .apply import _state_dir
        self.root=root_path(target)
        self.path=_state_dir(path,self.root)
        key=self.path/'evidence.key'
        try:
            fd=os.open(key,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        except FileExistsError:pass
        else:
            with os.fdopen(fd,'wb') as out:out.write(secrets.token_bytes(32));out.flush();os.fsync(out.fileno())
        mode=key.lstat().st_mode
        if not stat.S_ISREG(mode) or mode&0o077:raise HarnessError('Evidence key must be a private regular file')
        self.key=read_regular(key)
        if len(self.key)!=32:raise HarnessError('Invalid evidence key')
    def issue(self, kind, task, data):
        from .apply import _save
        body={'kind':kind,'task':identity(task),'target':str(self.root),'nonce':secrets.token_hex(16),'data':data}
        receipt={'body':body,'mac':hmac.digest(self.key,canonical(body).encode(),'sha256').hex()}
        rid=fingerprint(receipt)
        _save(self.path/(rid+'.evidence.json'),receipt)
        return rid
    def get(self, rid, kind, task):
        if not isinstance(rid,str) or len(rid)!=64 or any(c not in '0123456789abcdef' for c in rid):return None
        p=self.path/(rid+'.evidence.json')
        if not p.exists() or p.is_symlink():return None
        try:
            receipt=json.loads(read_regular(p));body=receipt['body']
            mac=hmac.digest(self.key,canonical(body).encode(),'sha256').hex()
            if not hmac.compare_digest(mac,receipt['mac']) or fingerprint(receipt)!=rid:return None
            if body['kind']!=kind or body['task']!=identity(task) or body['target']!=str(self.root):return None
            return body['data']
        except (ValueError,KeyError,TypeError,HarnessError):return None


def approve_spec(task, target, state_dir, confirmation):
    """Record an actual host/user approval reference, independent of install/execution consent."""
    if not confirmation or not confirmation.strip():raise HarnessError('Actual specification approval reference required')
    root=root_path(target);identity(task)
    source=task['spec']['source']
    if source and hashes(root,[source['path']])[source['path']]!=source['sha256']:raise HarnessError('Specification changed or missing')
    handoff=None
    if task['handoff_id']:
        from .handoff import resume,record_path
        result=resume(root,task['handoff_id'])
        if result['status']!='current':raise HarnessError('Reconcile stale handoff before specification approval')
        handoff=digest(read_regular(source_path(root,record_path(task['handoff_id']))))
    return EvidenceStore(state_dir,root).issue('spec-approval',task,{
        'confirmation':confirmation,'handoff':handoff,'code':hashes(root,task['code_paths']),
        'documentation':hashes(root,task['documentation']['paths'])})


def load_context(task, target, state_dir):
    """Return only requested bounded slices; receipts attest delivery, never comprehension."""
    root=root_path(target);identity(task);store=EvidenceStore(state_dir,root)
    loaded=[];total=0
    # Validate all sources/bounds before returning any content or issuing receipts.
    for item in task['context']:
        path=source_path(root,item['path'])
        if not path.exists() or path.stat().st_size>MAX_SOURCE_BYTES:raise HarnessError('Context source missing or too large')
        raw=read_regular(path)
        if len(raw)>MAX_SOURCE_BYTES or digest(raw)!=item['sha256']:raise HarnessError('Context source stale or too large')
        if path.suffix.lower() in ('.pdf','.docx'):raise HarnessError('Binary document needs a verified host reader; native reader evidence not implemented')
        try:lines=raw.decode('utf-8').splitlines(keepends=True)
        except UnicodeError as exc:raise HarnessError('Context must be readable UTF-8 text') from exc
        if item['end']<item['start'] or item['end']>len(lines):raise HarnessError('Invalid context locator')
        content=''.join(lines[item['start']-1:item['end']]);total+=len(content.encode())
        if total>MAX_CONTEXT_BYTES:raise HarnessError('Context delivery exceeds 32 KiB budget; narrow sources')
        loaded.append({'source':item,'content':content})
    for item in loaded:
        item['receipt']=store.issue('context',task,{'source':item['source'],'delivered_sha256':digest(item['content'])})
    return {'sources':loaded,'bytes':total,'scope':'Bytes delivered by reader; not proof of model comprehension'}
