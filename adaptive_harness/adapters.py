"""Versioned rendering contracts, not platform-specific selection policies."""
from copy import deepcopy
from dataclasses import dataclass
from .contracts import HarnessError

@dataclass(frozen=True)
class Adapter:
    name: str
    version: str
    status: str
    subagents: bool
    native_rules: bool

    kind: str = 'native'

    def output_path(self, canonical_path):
        if self.name == 'claude-code':
            if canonical_path.startswith('.agents/skills/'):return canonical_path.replace('.agents/skills/', '.claude/skills/', 1)
            if canonical_path == '.codex/agents/adh-reviewer.toml':return '.claude/agents/adh-reviewer.md'
        if self.name == 'cursor' and canonical_path == '.codex/agents/adh-reviewer.toml':return '.cursor/agents/adh-reviewer.md'
        if self.name == 'antigravity' and canonical_path == '.codex/agents/adh-reviewer.toml':return '.agents/agents/adh-reviewer.md'
        if self.name == 'lovable' and canonical_path.startswith('.agents/skills/'):
            return canonical_path.replace('.agents/skills/', '.adaptive-harness/integrations/lovable/skills/',1)
        if canonical_path.startswith('.codex/agents/') and not self.subagents:
            raise HarnessError('Adapter cannot render native subagents')
        return canonical_path

    def extra_files(self):
        return {
            'claude-code':{'CLAUDE.md':'claude-entry.md'},
            'cursor':{'.cursor/rules/adh.mdc':'cursor-entry.mdc'},
            'antigravity':{'.agents/rules/adh.md':'antigravity-entry.md'},
            'lovable':{'.adaptive-harness/integrations/lovable/project-instructions.md':'lovable-instructions.md',
                '.adaptive-harness/integrations/lovable/IMPORT.md':'lovable-import.md'},
        }.get(self.name,{})

    def warnings(self):
        if self.name=='lovable':return ['Lovable: це пакет для імпорту, не активована Workspace Skill. Генератор виконується поза Lovable; потрібен owner/admin для імпорту, після нього перевірте застосування інструкцій.']
        if self.name!='codex':return [self.name+': формати підтверджено офіційними джерелами; фактичне discovery/invocation у вашому host потребує перевірки. Permissions не змінюються.']
        return []

ADAPTERS = {
    'codex': Adapter('codex', '1.0', 'baseline-tested', True, True),
    'cursor': Adapter('cursor', '1.0', 'contract-tested-native-unverified', True, True),
    'claude-code': Adapter('claude-code', '1.0', 'contract-tested-native-unverified', True, True),
    'antigravity': Adapter('antigravity', '1.0', 'contract-tested-native-unverified', True, True),
    'lovable': Adapter('lovable', '1.0', 'import-required', False, False, 'integration'),
}

def profiles(assessment):
    """Legacy host remains supported. Explicit profiles must be supplied together."""
    legacy = assessment['host']
    explicit = ('execution_host' in assessment, 'target_platform' in assessment)
    if any(explicit) and not all(explicit):
        raise HarnessError('Supply execution_host and target_platform together')
    if all(explicit):
        return assessment['execution_host'], assessment['target_platform']
    executor = {'name': legacy['name'], 'version': legacy['version'],
                'capabilities': {k: legacy['capabilities'][k] for k in ('read_files','write_files','execute')}}
    target = {'name': legacy['name'], 'version': legacy['version'],
              'capabilities': {k: legacy['capabilities'][k] for k in ('native_skills','subagents')}}
    return executor, target

def adapter_for(assessment):
    _, target = profiles(assessment)
    return ADAPTERS.get(target['name'])

def effective_assessment(assessment):
    """Normalize capabilities once for the single unchanged selector."""
    executor, target = profiles(assessment)
    result = deepcopy(assessment)
    result['host']['name'] = target['name']
    result['host']['version'] = target['version']
    result['host']['capabilities'].update(deepcopy(executor['capabilities']))
    result['host']['capabilities'].update(deepcopy(target['capabilities']))
    adapter = ADAPTERS.get(target['name'])
    if adapter is None or not adapter.subagents:
        result['host']['capabilities']['subagents'] = {
            'value': False, 'basis': 'observed',
            'sources': ['Generator adapter has no verified native subagent renderer']}
    return result

def plan_adapter(assessment):
    adapter = adapter_for(assessment)
    _, target = profiles(assessment)
    return {'id':target['name'], 'version':adapter.version if adapter else 'unavailable',
            'status':adapter.status if adapter else 'unsupported'}
