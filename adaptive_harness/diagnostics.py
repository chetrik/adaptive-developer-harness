"""Read-only readiness diagnostics. Presence is never native execution evidence."""
import importlib.metadata
import os
import shutil
import sys
from .adapters import ADAPTERS
from .contracts import VERSION


def diagnose(platform,target=None):
    dependencies={}
    for name in ('jsonschema','PyYAML'):
        try:dependencies[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:dependencies[name]='missing'
    runtime=sys.version_info>=(3,11) and os.name=='posix' and hasattr(os,'O_NOFOLLOW') and all(v!='missing' for v in dependencies.values())
    adapter=ADAPTERS.get(platform)
    binary={'codex':'codex','claude-code':'claude','cursor':'cursor','antigravity':'antigravity'}.get(platform)
    report={'generator_version':VERSION,'platform':platform,'status':'ready-for-assessment' if runtime and adapter else 'blocked',
        'runtime':{'python':sys.version.split()[0],'posix':os.name=='posix','dependencies':dependencies},
        'adapter':adapter.status if adapter else 'not-implemented','native_executable_available':bool(binary and shutil.which(binary)),
        'native_application':'not-verified','next':('Read PRD, observe native Skills and permissions, then plan. Executable presence is not a discovery/application check.' if adapter else 'Use an implemented destination for exported code; this platform has no verified native adapter yet.')}
    if platform=='ai-studio':
        report.update(status='export-required',adapter='export-and-continue',next='Export ZIP or use Settings → GitHub, inspect exported code and select a destination adapter. No native custom Skills or Python execution assumed.')
    if target:
        from .inventory import inspect_inventory
        report['inventory']=inspect_inventory(target)
        if report['inventory']['status']=='blocked':report['status']='blocked'
    return report
