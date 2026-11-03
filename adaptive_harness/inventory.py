"""Installed inventory validation and pure reconciliation metadata; no writes or selection."""
from .contracts import ROOT, VERSION, POLICY, HarnessError, digest, fingerprint, read_json, validate
from .filesystem import safe_path, read_regular, root_path

MANIFEST='.adaptive-harness/manifest.json'

def path_owners(catalog):
    owners={'AGENTS.md':['core.agent-entry'],'.adaptive-harness/LICENSE':['core.safety-baseline']}
    for module in catalog['modules']:
        for name in module['files']:
            owners.setdefault(name,[]).append(module['id'])
    from .adapters import ADAPTERS
    for adapter in ADAPTERS.values():
        for name in adapter.extra_files():owners[name]=["core.agent-entry"]
        for module in catalog["modules"]:
            for name in module["files"]:
                if name.startswith(".codex/agents/") and not adapter.subagents:continue
                mapped=adapter.output_path(name)
                owners.setdefault(mapped,[])
                if module["id"] not in owners[mapped]:owners[mapped].append(module["id"])
    return owners

def load_inventory(root, catalog):
    path=safe_path(root,MANIFEST)
    if not path.exists():return {},[]
    try:
        old=read_json(path)
        if not isinstance(old,dict) or old.get('schema_version') not in ('1.0','2.0'):
            raise HarnessError('Unknown manifest version')
        validate('manifest-v'+old['schema_version'][0],old)
        allowed=path_owners(catalog)
        if set(old['files'])!=set(old['provenance']) or not set(old['files'])<=set(allowed):
            raise HarnessError('Unknown component path or incomplete provenance')
        if not set(old.get('pending_removal',[]))<=set(old['files']):
            raise HarnessError('Invalid pending removal inventory')
        ids={m['id'] for m in catalog['modules']}
        if not set(old['modules'])<=ids:raise HarnessError('Unknown installed module')
        for name in old['files']:safe_path(root,name)
        registry=read_json(ROOT/'catalog/legacy-component-hashes.json')
        legacy=registry['files']
        if old['schema_version']=='1.0':
            # Legacy manifests have no trustworthy component version. Recognize exact original assets.
            for name,sha in old['files'].items():
                if name!='AGENTS.md' and sha not in legacy.get(name,[]):
                    raise HarnessError('Unrecognized legacy component: '+name)
        else:
            v=old['versions']
            if v['generator'] not in ('0.3.0','0.4.0',VERSION) or v['policy']!=POLICY or v['catalog']!=catalog['catalog_version']:
                raise HarnessError('Unsupported installed versions; migration required')
            from .adapters import ADAPTERS
            adapter=ADAPTERS.get(v['adapter'])
            if not adapter or (v['adapter_version']!=adapter.version and not (v['adapter']=='cursor' and v['adapter_version']=='0.1' and v['generator'] in ('0.3.0','0.4.0'))):raise HarnessError('Unknown installed adapter version')
            if set(old['owners'])!=set(old['files']) or not set(old['components'])<=ids:
                raise HarnessError('Incomplete ownership inventory')
            from .core import _source
            for name,sha in old['files'].items():
                if name=='AGENTS.md':continue
                source=ROOT/'LICENSE' if name=='.adaptive-harness/LICENSE' else ROOT/'library/target'/_source(name)
                supported=[digest(source.read_bytes()),*legacy.get(name,[]),*[r['files'].get(name) for r in registry['releases'].values()]]
                if v['generator'] in registry['releases']:supported=[registry['releases'][v['generator']]['files'].get(name),*legacy.get(name,[])]
                if sha not in supported:
                    raise HarnessError('Unrecognized installed component revision: '+name)
            for name,owners in old['owners'].items():
                if not owners or not set(owners)<=set(allowed[name]):raise HarnessError('Invalid component ownership')
            tracked=set(old['modules'])|{mid for owners in old['owners'].values() for mid in owners}
            if set(old['components'])!=tracked:
                raise HarnessError('Untracked component ownership')
            if components(tracked,old['owners'],old['files'],set(old['modules']))!=old['components']:
                raise HarnessError('Component inventory revision mismatch')
        return old,[]
    except (HarnessError,ValueError,KeyError,TypeError) as exc:
        return {},['Інвентар заблоковано: '+str(exc)]

def versions(catalog,adapter):
    return {'generator':VERSION,'policy':POLICY,'catalog':catalog['catalog_version'],
            'adapter':adapter['id'],'adapter_version':adapter['version']}

def components(modules, owners, hashes, selected):
    return {mid:{'revision':fingerprint({n:hashes[n] for n in sorted(hashes) if mid in owners.get(n,[])}),
                 'status':'active' if mid in selected else 'pending_removal',
                 'files':sorted(n for n in hashes if mid in owners.get(n,[]))} for mid in sorted(modules)}

def inspect_inventory(target):
    from .core import load_catalog
    root=root_path(target);old,blockers=load_inventory(root,load_catalog())
    files={}
    for name,sha in old.get('files',{}).items():
        path=safe_path(root,name)
        files[name]={'expected':sha,'actual':digest(read_regular(path)) if path.exists() else None,
                     'status':'pending_removal' if name in old.get('pending_removal',[]) else 'active'}
    return {'status':'blocked' if blockers else 'installed' if old else 'not-installed',
            'versions':old.get('versions',{'generator':'unknown','manifest':old.get('schema_version','none')}),
            'components':old.get('components',{}),'files':files,'blockers':blockers}
