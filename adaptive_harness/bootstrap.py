"""Agent intake scaffold; it does not pretend to interpret the PRD."""
import platform
from urllib.parse import urlsplit
from pathlib import Path
from .contracts import ROOT, HarnessError, digest, validate
from .research import git

GENERATOR_URL='https://github.com/chetrik/adaptive-developer-harness'

def intake(prd_path, url, target=None, target_platform="codex"):
    if url.rstrip('/')!=GENERATOR_URL:
        raise HarnessError('Unexpected generator URL')
    prd=Path(prd_path)
    if not prd.is_file() or prd.is_symlink() or prd.stat().st_size>16*1024*1024:
        raise HarnessError('PRD must be an accessible regular file under 16 MiB')
    if prd.name.startswith('.env'):
        raise HarnessError('Credential files are not PRDs')
    formats={'.md':'markdown','.markdown':'markdown','.pdf':'pdf','.docx':'docx'}
    if prd.suffix.lower() not in formats:
        raise HarnessError('Supported PRD formats: Markdown, PDF, DOCX')
    from .adapters import ADAPTERS
    if target_platform not in ADAPTERS:
        raise HarnessError('Target adapter is not implemented: '+target_platform)
    raw=prd.read_bytes()
    unknown=lambda: {'value':'unknown','basis':'unknown','sources':[]}
    capabilities={k:unknown() for k in ('read_files','write_files','execute','network','native_skills','subagents')}
    capabilities['read_files']={'value':True,'basis':'observed','sources':['PRD was read from the permitted workspace']}
    capabilities['execute']={'value':True,'basis':'observed','sources':['Python '+platform.python_version()+' executed bootstrap']}
    a={'schema_version':'1.0','project_name':prd.stem,'project_type':'custom','stage':'brownfield' if target else 'unknown',
       'user_mode':'beginner','project_scale':'unknown','feature_size':'M','surfaces':[], 'prd':{'sha256':digest(raw),'source':str(prd.resolve()),'format':formats[prd.suffix.lower()], 'reading':{'status':'unread','reader':'not selected','locators':['Original document; not yet interpreted'],'notes':[]}},
       'facts':{k:unknown() for k in ('personal_data','sensitive_data','payments','authentication','public_exposure','production','schema_change','api_change','existing_harness','commodity')},
       'host':{'name':target_platform,'version':'unverified','capabilities':capabilities},
       'reuse':{'status':'pending','decision':'undecided','rationale':'Спочатку агент читає PRD і визначає доречність готових рішень.','candidates':[]},
       'unknowns':['Агент має інтерпретувати PRD, уточнити критичні факти і перевірити host capabilities.']}
    a['execution_host']={'name':'local-python','version':platform.python_version(),
        'capabilities':{k:capabilities[k].copy() for k in ('read_files','write_files','execute')}}
    a['target_platform']={'name':target_platform,'version':'unverified',
        'capabilities':{k:capabilities[k].copy() for k in ('native_skills','subagents')}}
    a['model_provider']={'kind':'agent','model':'provided by coding agent'}
    validate('project-assessment',a)
    origin=urlsplit(git('remote','get-url','origin',cwd=ROOT))
    if origin.hostname!='github.com' or origin.path.removesuffix('.git').strip('/')!='chetrik/adaptive-developer-harness':
        raise HarnessError('Local checkout origin does not match the generator URL')
    revision=git('rev-parse','HEAD',cwd=ROOT)
    dirty=bool(git('status','--porcelain',cwd=ROOT))
    return {'assessment':a,'generator':{'url':GENERATOR_URL,'local_revision':revision,'local_changes':dirty},
            'next':'Агент читає PRD, записує факти з джерелами, досліджує готові рішення і перевіряє можливості host. Це шаблон, не завершений assessment.'}
