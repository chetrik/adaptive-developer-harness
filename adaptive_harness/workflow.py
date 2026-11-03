"""Single deterministic route policy, shared by every adapter."""

def session_workflow(assessment, decisions):
    size=assessment['feature_size']
    route={'XS':'quick','S':'quick','M':'standard','L':'full','XL':'full'}[size]
    selected={d['id'] for d in decisions if d['status']=='selected'}
    sessions={'quick':'single-cycle','standard':'specification-then-implementation','full':'milestone-sessions'}[route]
    recommendation={
        'quick':'Один короткий цикл у поточному чаті: узгодити вимоги, реалізувати, перевірити.',
        'standard':'Рекомендовано окремі сесії Specification та Implementation; перевірку можна завершити в сесії реалізації.',
        'full':'Рекомендовано окремі сесії для великих етапів; кожен етап завершується Verification і перевірюваним handoff.'}[route]
    checks=['acceptance-criteria','relevant-tests','documentation-impact','harness-integrity']
    if 'security.auth-and-data' in selected:checks.append('security-and-data-access')
    if 'security.release-gate' in selected:checks.append('release-readiness')
    review='independent-if-observed' if 'quality.independent-review' in selected else 'inline-not-independent'
    return {'route':route,'reason_id':'feature-size.'+size,'sessions':sessions,
            'new_chat_required':False,'automatic_session_creation':False,'recommendation':recommendation,
            'phases':[
                {'name':'Specification','exit_criteria':['requirements-and-acceptance-agreed','existing-code-reviewed','scope-approved']},
                {'name':'Implementation','exit_criteria':['approved-scope-implemented','changed-files-recorded']},
                {'name':'Verification','exit_criteria':checks+['results-and-next-step-recorded']}],
            'review':review,'specification_format':'inline' if route=='quick' else 'existing-or-selected-feature-spec',
            'handoff':'at-explicit-session-close-and-milestone-boundaries',
            'fallback':'Якщо нова сесія недоступна або недоречна, збережи ті самі етапи й контрольні точки в поточному чаті.'}
