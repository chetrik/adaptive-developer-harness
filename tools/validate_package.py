#!/usr/bin/env python3
"""Structural checks for the documentation starter; NOT a generator or security scanner.

Run: python tools/validate_package.py
Optional: install `jsonschema` to also validate the illustrative plan against its schema.
"""
from __future__ import annotations
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
errors = []
required = [
    'README.md','START_HERE_UA.md','CODEX_BOOTSTRAP_PROMPT.md','AGENTS.md',
    'INSPIRATIONS.md','THIRD_PARTY_NOTICES.md','docs/PRD.md','docs/ARCHITECTURE.md',
    'docs/DECISIONS.md','docs/ROADMAP.md','docs/TRACEABILITY.md','docs/ACCEPTANCE.md',
    'docs/CONVERSATION_COVERAGE.md','docs/SELECTION_POLICY.md',
    'docs/BEGINNER_EXPERIENCE.md','docs/SECURITY.md','docs/REUSE_FIRST.md',
    'docs/SKILLS_AGENTS.md','docs/STATE_HANDOFF.md',
    'schemas/harness-plan.schema.json','catalog/modules.yaml','templates/HARNESS_PLAN.md',
    'examples/harness-plan-calculator.json'
]
for path in required:
    if not (ROOT / path).is_file(): errors.append('Missing: ' + path)

prd=(ROOT/'docs/PRD.md').read_text(encoding='utf-8')
trace=(ROOT/'docs/TRACEABILITY.md').read_text(encoding='utf-8')
acc=(ROOT/'docs/ACCEPTANCE.md').read_text(encoding='utf-8')
reqs=re.findall(r'^- \*\*\[([A-Z]+-\d+)\]',prd,re.M)
rows=re.findall(r'^\| `([A-Z]+-\d+)` \|',trace,re.M)
tests=set(re.findall(r'^\| (AT-\d+) \|',acc,re.M))
if len(reqs)!=len(set(reqs)):errors.append('Duplicate requirement ID in PRD')
if len(rows)!=len(set(rows)):errors.append('Duplicate requirement row in traceability')
if set(reqs)!=set(rows):errors.append(f'Traceability mismatch: missing {set(reqs)-set(rows)}, extra {set(rows)-set(reqs)}')
for line in trace.splitlines():
    if re.match(r'^\| `[A-Z]+-\d+`',line):
        linked=set(re.findall(r'AT-\d+',line))
        if not linked:errors.append('No acceptance test in: '+line[:70])
        for tid in linked-tests:errors.append('Unknown acceptance test '+tid)

for path in ROOT.rglob('*.md'):
    content=path.read_text(encoding='utf-8')
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',content):
        if target.startswith(('http:','https:','#','mailto:')): continue
        part=target.split('#')[0]
        if part and not (path.parent / part).exists():
            errors.append('Broken local Markdown link in '+str(path.relative_to(ROOT))+': '+target)

schema=json.loads((ROOT/'schemas/harness-plan.schema.json').read_text(encoding='utf-8'))
example=json.loads((ROOT/'examples/harness-plan-calculator.json').read_text(encoding='utf-8'))
try:
    from jsonschema import Draft202012Validator
except ImportError:
    print('NOTE: jsonschema absent; skipping full example JSON Schema check')
    if example.get('schema_version')!=schema['properties']['schema_version']['const']:
        errors.append('Schema version mismatch')
else:
    v=Draft202012Validator(schema)
    for issue in v.iter_errors(example): errors.append('Example/schema: '+issue.message)

# Basic module catalog validation (YAML optional for users with pure stdlib)
try:
    import yaml
except ImportError:
    print('NOTE: PyYAML absent; skipping module catalog dependency check')
else:
    catalog=yaml.safe_load((ROOT/'catalog/modules.yaml').read_text(encoding='utf-8'))
    mods=catalog['modules']
    ids=[m['id'] for m in mods]
    if len(ids)!=len(set(ids)):errors.append('Duplicate catalog module IDs')
    for m in mods:
        for dep in m.get('dependencies',[])+m.get('conflicts',[]):
            if dep not in ids:errors.append('Unknown catalog module reference '+dep+' in '+m['id'])
        if m['id'] in m.get('dependencies',[]):errors.append('Self-dependency '+m['id'])

if errors:
    print('VALIDATION FAILED')
    for e in errors:print(' -',e)
    sys.exit(1)
print(f'OK: {len(required)} required files; {len(reqs)} requirements; {len(tests)} acceptance tests; local links and plan schema checked.')
print('This does not mean any generator or safety functionality is implemented.')
