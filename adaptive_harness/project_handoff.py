"""Portable project inspection/export. Does not install Harness or execute application code."""
import json
import os
import re
import stat
import zipfile
from pathlib import Path,PurePosixPath
from .contracts import HarnessError,digest,fingerprint
from .filesystem import root_path,read_regular,MAX_BYTES,MAX_FILES
from .evidence import source_path

SKIP={'.git','node_modules','.venv','venv','__pycache__','.next','dist','build'}
SECRET=re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|AKIA[0-9A-Z]{16}|sk-(?:proj-)?[A-Za-z0-9_-]{30,}')
ENV=re.compile(r'(?:process\.env\.|import\.meta\.env\.|os\.environ\[\s*[\"\x27]|(?:os\.getenv|os\.environ\.get)\(\s*[\"\x27])([A-Z][A-Z0-9_]*)')

def protected(name):
    return any(p.startswith('.env') or p in ('.git','.ssh','.aws','.credentials','.kube','.azure','.config','.npmrc','.pypirc','.netrc','.git-credentials','id_rsa','id_ed25519') or p.endswith(('.pem','.key','.p12','.pfx')) or p in ('credentials.json','service-account.json') for p in PurePosixPath(name).parts)

def inspect_project(target):
    root=root_path(target);files={};excluded=[];env=set();services=set();scripts=[];total=0;count=0;warnings=[]
    for base,dirs,names in os.walk(root,followlinks=False):
        dirs.sort();names.sort()
        for name in list(dirs):
            p=Path(base)/name;rel=p.relative_to(root).as_posix()
            if name in SKIP or p.is_symlink() or protected(rel):excluded.append(rel);dirs.remove(name)
        for name in names:
            p=Path(base)/name;rel=p.relative_to(root).as_posix();count+=1
            if count>MAX_FILES:raise HarnessError('Project inspection file budget exceeded')
            if p.is_symlink() or protected(rel):excluded.append(rel);continue
            if not stat.S_ISREG(p.lstat().st_mode):raise HarnessError('Special file in project')
            total+=p.stat().st_size
            if total>MAX_BYTES:raise HarnessError('Project inspection byte budget exceeded')
            raw=read_regular(p)
            if SECRET.search(raw):excluded.append(rel);warnings.append('Potential credential in '+rel+'; review before export');continue
            files[rel]=digest(raw)
            if len(raw)<=1048576:
                text=raw.decode('utf-8',errors='ignore');env.update(ENV.findall(text))
                for service in ('supabase','firebase','stripe','clerk'):
                    if re.search(r'\b'+service+r'\b',text,re.I):services.add(service)
            if rel=='package.json':
                try:scripts=sorted(json.loads(raw).get('scripts',{}))
                except (ValueError,AttributeError,TypeError):warnings.append('package.json requires review')
    dependencies=[n for n in files if Path(n).name in ('package.json','package-lock.json','pnpm-lock.yaml','yarn.lock','pyproject.toml','requirements.txt','requirements.lock','uv.lock','Cargo.toml','go.mod')]
    if 'package.json' in files and not any(p in files for p in ('package-lock.json','pnpm-lock.yaml','yarn.lock')):warnings.append('No JavaScript lockfile found; reproduce dependency versions before continuing')
    if not dependencies:warnings.append('No recognized dependency manifest found; inspect project type before installing anything')
    return {'status':'review-required','files':files,'fingerprint':fingerprint(files),'excluded':sorted(excluded),
        'environment_variable_names':sorted(env),'external_services':sorted(services),'dependency_files':sorted(dependencies),
        'test_script_names':[s for s in scripts if 'test' in s or 'check' in s or 'lint' in s],
        'context_files':[n for n in files if Path(n).name in ('AGENTS.md','CLAUDE.md','PRD.md','ARCHITECTURE.md','DECISIONS.md') or n.startswith('.adaptive-harness/sessions/')],
        'warnings':warnings,'not_transferred':['Database contents and credentials','Hosted service configuration and accounts','Platform chat history unless explicitly exported'],
        'next':'Review PRD and existing code, provision missing environment/services, then bootstrap the chosen adapter. Preserve existing implementation; do not rewrite it without a concrete reason.'}

def export_project(target,paths,output,confirmation):
    if not confirmation or not confirmation.strip():raise HarnessError('Explicit export approval reference required')
    if not isinstance(paths,list) or not paths or len(paths)>MAX_FILES or any(not isinstance(p,str) for p in paths) or len(set(paths))!=len(paths):raise HarnessError('Provide an explicit unique file list for export')
    root=root_path(target);out=Path(output).absolute();parent=root_path(out.parent)
    if parent==root or root in parent.parents:raise HarnessError('Export must be outside the application project')
    report=inspect_project(root)
    if any(p not in report['files'] or protected(p) for p in paths):raise HarnessError('Export contains unknown, excluded or secret-like files; review the file list')
    contents={};total=0
    for name in sorted(paths):
        raw=read_regular(source_path(root,name));total+=len(raw)
        if total>MAX_BYTES or digest(raw)!=report['files'][name] or SECRET.search(raw):raise HarnessError('Export source changed or exceeds safety limits')
        contents[name]=raw
    # Only selected file metadata enters the export; unselected paths remain private.
    metadata={k:v for k,v in report.items() if k not in ('files','excluded','fingerprint','warnings','context_files','dependency_files')}
    metadata.update({'files':{n:digest(b) for n,b in contents.items()},'context_files':[p for p in report['context_files'] if p in paths],
        'dependency_files':[p for p in report['dependency_files'] if p in paths],
        'missing_dependency_files':[p for p in report['dependency_files'] if p not in paths],
        'missing_context_files':[p for p in report['context_files'] if p not in paths],
        'approval':'Export approved by host/user; reference retained by caller',
        'scope':'Code package only; secret scan is bounded and cannot certify absence of all secrets. Review selected files before sharing.'})
    if 'HARNESS_HANDOFF.json' in contents:raise HarnessError('Reserved export metadata name')
    fd=os.open(out,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try:
        with os.fdopen(fd,'wb') as stream:
            with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED) as archive:
                for name,raw in contents.items():archive.writestr(name,raw)
                archive.writestr('HARNESS_HANDOFF.json',json.dumps(metadata,ensure_ascii=False,indent=2))
            stream.flush();os.fsync(stream.fileno())
    except BaseException:
        out.unlink(missing_ok=True);raise
    return {'status':'exported','path':str(out),'files':sorted(contents),'scope':metadata['scope']}

def inspect_archive(path):
    archive_path=Path(path)
    if archive_path.is_symlink() or not archive_path.is_file() or archive_path.stat().st_size>MAX_BYTES:raise HarnessError('Invalid or oversized export archive')
    try:
        with zipfile.ZipFile(archive_path) as archive:
            items=archive.infolist();names=set();total=0;excluded=[];files=[]
            if len(items)>MAX_FILES:raise HarnessError('Archive file budget exceeded')
            for item in items:
                name=item.filename.rstrip('/');p=PurePosixPath(name)
                if not name or p.is_absolute() or p.as_posix()!=name or '..' in p.parts or '\\' in name or '\x00' in name or any(':' in part for part in p.parts) or name in names:raise HarnessError('Unsafe or duplicate archive path')
                names.add(name);total+=item.file_size
                mode=item.external_attr>>16
                if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) and not (stat.S_ISREG(mode) or stat.S_ISDIR(mode))):raise HarnessError('Archive link or special file')
                if total>MAX_BYTES or item.flag_bits&1:raise HarnessError('Oversized or encrypted archive')
                if item.is_dir():continue
                if protected(name):excluded.append(name);continue
                raw=archive.read(item)
                if SECRET.search(raw):excluded.append(name);continue
                files.append(name)
    except (zipfile.BadZipFile,RuntimeError) as exc:raise HarnessError('Cannot inspect export archive') from exc
    return {'status':'blocked' if excluded else 'review-required','files':files,'excluded':excluded,
        'next':'Do not execute archive content. Review files, extract only reviewed entries into a new workspace with host tools, run inspect-project and bootstrap. Database and chat history are separate.'}
