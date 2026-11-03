"""Package selected installed Skills; never selects modules or installs target files."""
import json
import os
import re
import zipfile
from pathlib import Path
import yaml
from .contracts import HarnessError,digest
from .filesystem import root_path,read_regular
from .evidence import source_path


def package_skills(target,output_dir,confirmation):
    if not confirmation or not confirmation.strip():raise HarnessError('Actual package export approval reference required')
    from .inventory import load_inventory
    from .core import load_catalog
    root=root_path(target);out=root_path(output_dir)
    if out==root or root in out.parents:raise HarnessError('Skill packages must be outside the project')
    installed,blockers=load_inventory(root,load_catalog())
    if blockers or not installed:raise HarnessError('Install and validate the selected Harness first')
    packages=[]
    for name,expected in installed['files'].items():
        if not name.endswith('/SKILL.md') or name in installed.get('pending_removal',[]):continue
        raw=read_regular(source_path(root,name))
        if digest(raw)!=expected:raise HarnessError('Selected Skill was customized; resolve/review before packaging')
        try:
            text=raw.decode();header=yaml.safe_load(text.split('---',2)[1]);skill=header['name'];description=header['description']
        except (ValueError,KeyError,IndexError,TypeError,yaml.YAMLError) as exc:raise HarnessError('Invalid Skill frontmatter') from exc
        if not isinstance(skill,str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',skill) or len(skill)>64 or skill=='goal' or not isinstance(description,str) or not description.strip():raise HarnessError('Invalid portable Skill metadata')
        if len(raw)>1048576 or len(text)>100000:raise HarnessError('Skill exceeds Lovable import limits')
        destination=out/(skill+'.zip')
        if destination.exists() or destination.is_symlink():raise HarnessError('Package already exists; choose a new output directory')
        packages.append((destination,raw,skill))
    if not packages:raise HarnessError('No selected active Skills to package')
    if len({p[2] for p in packages})!=len(packages):raise HarnessError('Duplicate Skill names; resolve adapter transition first')
    written=[]
    for destination,raw,skill in packages:
        fd=os.open(destination,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        with os.fdopen(fd,'wb') as stream:
            with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED) as archive:archive.writestr('SKILL.md',raw)
            stream.flush();os.fsync(stream.fileno())
        written.append({'skill':skill,'path':str(destination),'source_sha256':digest(raw)})
    return {'status':'packaged','packages':written,'native_import':'not-verified','next':'Owner/admin imports each ZIP separately, verifies / Skills discovery, then invokes it on a harmless task. No automatic workspace activation.'}


def check_instructions(target,project_instructions,workspace_instructions=None):
    root=root_path(target)
    baseline=root/'.adaptive-harness/integrations/lovable/project-instructions.md'
    if not baseline.is_file():raise HarnessError('Lovable integration is not installed')
    def read(path):
        p=Path(path).absolute();safe=source_path(root_path(p.parent),p.name);raw=read_regular(safe)
        if len(raw)>40000:raise HarnessError('Instruction field exceeds review budget')
        text=raw.decode('utf-8')
        if len(text)>10000:raise HarnessError('Lovable instruction field exceeds 10,000 characters')
        return text
    expected=read(baseline);project=read(project_instructions);workspace=read(workspace_instructions) if workspace_instructions else ''
    checks=[{'name':'project-instructions-match','status':'pass' if project.strip()==expected.strip() else 'not-verified',
        'reason':'Differences require review against AGENTS.md and selected Skills; do not overwrite existing project guidance.'},
        {'name':'workspace-conflicts','status':'not-verified' if workspace.strip() else 'not-applicable',
        'reason':'Nonempty Workspace Instructions require semantic conflict review; a program cannot prove arbitrary prose is consistent.'},
        {'name':'actual-platform-application','status':'not-verified','reason':'Text comparison does not prove the platform applied it. Run a harmless task in Lovable.'}]
    return {'status':'not-verified','checks':checks,'next':'Agent reviews combined instruction sources and reports concrete conflicts before activation. Only actual host outcomes can confirm application.'}
