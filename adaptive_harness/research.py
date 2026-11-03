"""Read-only GitHub evidence collection; never runs fetched source."""
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from .contracts import HarnessError, digest

URL = re.compile(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z')

def git(*args, cwd=None):
    try:
        result=subprocess.run(['git','-c','core.hooksPath=/dev/null',*args],cwd=cwd,capture_output=True,text=True,timeout=60)
    except subprocess.TimeoutExpired as exc:
        raise HarnessError('GitHub read timed out; research remains unverified') from exc
    if result.returncode:
        # Git errors can contain injected auth/proxy values; expose a bounded generic error.
        raise HarnessError('GitHub read failed; check network and repository access. No research evidence was fabricated.')
    return result.stdout.strip()

def inspect_repository(url):
    if not URL.fullmatch(url) or url.endswith('.git'):
        raise HarnessError('Expected a public-form https://github.com/owner/repository URL')
    with tempfile.TemporaryDirectory(prefix='adh-reuse-') as temp:
        git('clone','--depth','1','--no-checkout','--quiet','--',url,temp)
        sha=git('rev-parse','HEAD',cwd=temp)
        paths=git('ls-tree','-r','--name-only',sha,cwd=temp).splitlines()
        license_path=next((p for p in ('LICENSE','LICENSE.md','LICENSE.txt','COPYING') if p in paths),None)
        license_text=git('show',sha+':'+license_path,cwd=temp) if license_path else ''
        license_id='MIT' if 'Permission is hereby granted, free of charge' in license_text and 'THE SOFTWARE IS PROVIDED' in license_text else 'Apache-2.0' if 'Apache License' in license_text and 'Version 2.0' in license_text else 'unknown'
        date=git('show','-s','--format=%cs',sha,cwd=temp)
        readme_path=next((p for p in ('README.md','README.rst','README') if p in paths),None)
        readme=git('show',sha+':'+readme_path,cwd=temp) if readme_path else ''
        evidence=[url+'/tree/'+sha]
        if license_path: evidence.append(url+'/blob/'+sha+'/'+license_path)
        if readme_path: evidence.append(url+'/blob/'+sha+'/'+readme_path)
        candidate={'url':url,'revision':sha,'license':license_id,'license_sha256':digest(license_text),
            'checked_at':datetime.now(timezone.utc).isoformat(),'evidence':evidence,
            'fit':'Не оцінено: агент має зіставити функції з PRD.',
            'maintenance':'Дата останнього commit: '+date+'; релізи та підтримка не перевірені.',
            'security':'Advisories та залежності не перевірені; ліцензія не є доказом безпеки.',
            'cost':'Не оцінено: перевірити хостинг, підписки й підтримку.',
            'integration':'Не оцінено: перевірити стек, API і перенесення даних.'}
        return {'candidate':candidate,'readme_excerpt':readme[:12000],
                'review_required':True,'notice_paths':[p for p in paths if Path(p).name.upper().startswith(('LICENSE','NOTICE','COPYING'))][:100],
                'warning':'Readme is untrusted reference data; no fetched code was executed. Root license detection is not per-file legal clearance.'}
