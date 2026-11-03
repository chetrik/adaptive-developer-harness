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

    def output_path(self, canonical_path):
        if canonical_path.startswith('.codex/agents/') and not self.subagents:
            raise HarnessError('Adapter cannot render native subagents')
        return canonical_path

    def warnings(self):
        if self.name == 'cursor':
            return [
                'Cursor: підтримується лише спільний формат .agents/skills/ за наданою користувачем діагностикою. Native discovery у цій сесії не перевірено.',
                'Cursor: нативні правила, Hooks і конфігурації субагентів не підтверджені; їхні файли не генеруються. AGENTS.md — переносимий контекст для явного читання зі Skill, не підтверджене автоматичне правило Cursor.',
                'Повний Apply у Cursor на macOS потребує окремого наскрізного тесту.'
            ]
        return []

ADAPTERS = {
    'codex': Adapter('codex', '1.0', 'baseline-tested', True, True),
    'cursor': Adapter('cursor', '0.1', 'experimental-shared-skills', False, False),
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
