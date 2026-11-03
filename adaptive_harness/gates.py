"""Formal task readiness inside the existing workflow. No module selection or file writes.

Statuses describe evidence, not universal control over an external coding agent.
"""
from .contracts import HarnessError,validate,digest,fingerprint
from .filesystem import root_path,snapshot
from .evidence import EvidenceStore,identity,hashes

PLACEHOLDERS={'todo','tbd','...','placeholder','<goal>','<scope>','n/a'}

def meaningful(value):return bool(value.strip()) and value.strip().lower() not in PLACEHOLDERS

def evaluate(assessment,task,target,state_dir,*,transition='implementation',receipts=None):
    if transition not in ('implementation','verification','complete'):raise HarnessError('Unknown stage transition')
    validate('project-assessment',assessment);identity(task);root=root_path(target)
    from .core import select,load_catalog
    from .workflow import session_workflow
    decisions=select(assessment,load_catalog());workflow=session_workflow(assessment,decisions)
    selected={d['id'] for d in decisions if d['status']=='selected'}
    material=assessment['feature_size'] in ('M','L','XL')
    risk='security.auth-and-data' in selected
    receipts={} if receipts is None else receipts
    validate('engineering-request',{'task':task,'receipts':receipts,'state_dir':str(state_dir),'transition':transition})
    store=EvidenceStore(state_dir,root);checks=[]
    def add(code,status,reason):checks.append({'code':code,'status':status,'reason':reason})
    def require(code,condition,reason):add(code,'pass' if condition else 'blocked',reason)
    require('task.path-separation',not (set(task['code_paths']) & (set(task['test_paths'])|set(task['config_paths'])|set(task['documentation']['paths']))), 'Код реалізації, regression tests, configs і документація мають різні ролі.')
    spec=task['spec'];acs=spec['acceptance'];acids={a['id'] for a in acs}
    require('spec.goal-scope',meaningful(spec['goal']) and meaningful(spec['scope']),'Потрібні змістовні мета і межі задачі.')
    require('spec.acceptance',bool(acs) and len(acids)==len(acs) and all(meaningful(a[k]) for a in acs for k in ('id','given','when','then')),'Потрібні унікальні перевірювані AC: умова, дія та очікуваний результат.')
    categories={a['category'] for a in acs}
    needed={c for module,c in [('security.auth-and-data','security'),('data.migration-safety','migration'),('api.contract','api')] if module in selected}
    require('spec.risk-coverage',needed<=categories,'Додайте критерії для ризиків: '+', '.join(sorted(needed)))
    if material or risk:
        require('spec.edge-cases',bool(spec['edge_cases']) and all(meaningful(v) for v in spec['edge_cases']),'Для цього обсягу/ризику потрібні крайові та помилкові сценарії.')
        require('spec.error-criteria','error' in categories,'Потрібний перевірюваний помилковий сценарій.')
    else:add('spec.edge-cases','not-applicable','Короткий цикл без додаткового документа; детальна матриця сценаріїв не обов’язкова.')
    require('spec.questions',not any(q['critical'] for q in spec['questions']),'Невирішені критичні питання блокують реалізацію.')
    nfr=spec['nfr']
    if nfr['applicability']=='unknown':add('spec.nfr','not-verified','Уточніть релевантність нефункціональних вимог.')
    elif nfr['applicability']=='required' or risk:
        require('spec.nfr',nfr['applicability']=='required' and bool(nfr['criteria']) and all(meaningful(x) for x in nfr['criteria']),'Потрібні перевірювані NFR відповідно до ризику.')
    else:add('spec.nfr','not-applicable' if meaningful(nfr['reason']) else 'blocked','NFR не релевантні лише з обґрунтуванням, погодженим у spec.')
    source=spec['source']
    if source:require('spec.source',hashes(root,[source['path']])[source['path']]==source['sha256'],'Погоджена специфікація відсутня або змінилася.')
    approval=store.get(receipts.get('spec_approval'),'spec-approval',task)
    require('spec.approval',approval is not None,'Потрібне погодження саме task/spec; install approval не замінює його.')
    require('verification.coverage',acids=={c['ac_id'] for c in task['checks']},'Кожен AC має бути пов’язаний із тестом; сторонні AC не приймаються.')
    sources=task['context'];critical={i['category'] for i in sources if i['critical']}
    required_context={'rules'}|({'code'} if any(hashes(root,task['code_paths']).values()) and transition=='implementation' else set())|({'specification'} if source else set())
    require('context.categories',required_context<=critical,'Потрібні критичні правила, пов’язаний код і специфікація, якщо вона у файлі.')
    if source:require('context.spec-binding',any(i['path']==source['path'] and i['sha256']==source['sha256'] and i['critical'] for i in sources),'Прочитаний контекст має включати ту саму специфікацію.')
    observed=[store.get(r,'context',task) for r in receipts.get('context',[]) if isinstance(r,str)]
    for index,item in enumerate(sources):
        actual=hashes(root,[item['path']])[item['path']]
        # Intended implementation changes supersede the pre-implementation code slice.
        freshness=(transition!='implementation' and item['category']=='code') or actual==item['sha256']
        delivered=any(r and r.get('source')==item for r in observed)
        status='blocked' if item['critical'] and not freshness else 'not-verified' if not freshness or not delivered else 'pass'
        add('context.source.'+str(index),status,'Джерело '+item['path']+': потрібні актуальні bytes і receipt читання; посилання/read=true недостатні.')
    if task['handoff_id']:
        from .handoff import resume,record_path
        try:
            current=resume(root,task['handoff_id'])['status']=='current'
            if transition!='implementation':current=bool(approval and approval.get('handoff') and hashes(root,[record_path(task['handoff_id'])])[record_path(task['handoff_id'])]==approval['handoff'])
        except (HarnessError,OSError):current=False
        require('context.handoff',current,'Стан handoff застарів або недоступний; спочатку звірте фактичні файли.')
    else:add('context.handoff','not-applicable','Немає попереднього checkpoint; новий документ не створюється.')
    code=hashes(root,task['code_paths'])
    if transition=='implementation' and approval:
        require('implementation.baseline',code==approval['code'],'Код змінився після погодження/підготовки; перегляньте scope та оновіть погодження контексту.')
    red=store.get(receipts.get('red'),'test-run',task)
    green=store.get(receipts.get('green'),'test-run',task)
    wanted={c['test_id'] for c in task['checks']}
    if transition in ('verification','complete'):
        require('implementation.candidate',bool(code) and all(v is not None for v in code.values()),'Потрібний наявний candidate code, а не лише твердження completed.')
    if task['kind']=='bugfix' and transition!='implementation':
        valid_red=bool(red and red['phase']=='red' and red['classification']=='assertion-failure' and red['workspace_unchanged_during_run'] and approval and red['code']==approval['code'] and set(red['result']['failures']) & wanted)
        add('bugfix.red','pass' if valid_red else 'not-verified','Потрібний observed assertion failure цільового тесту на вихідній реалізації; crash/skip/початковий GREEN не є відтворенням.')
    elif task['kind']!='bugfix':add('bugfix.red','not-applicable','Це feature, не відтворюваний дефект.')
    if transition=='complete':
        current=snapshot(root,exclude_sessions=True)
        valid_green=bool(green and green['phase']=='green' and green['classification']=='pass' and green['workspace']==current and green['code']==code and wanted<=set(green['result']['passed']))
        status='pass' if valid_green else 'blocked' if green and (green['classification']=='assertion-failure' or green['workspace']!=current) else 'not-verified'
        add('verification.observed-tests',status,'Тести повинні реально пройти для поточного коду; self-report або старий запуск не підтверджує завершення.')
        if task['kind']=='bugfix' and red and green:
            same=(red['fixed_inputs']==green['fixed_inputs'] and red['tests']==green['tests'] and red['configs']==green['configs'] and red['selection']==green['selection'] and red['runner']==green['runner'] and red['result'] and green['result'] and set(red['result']['seen'])==set(green['result']['seen']))
            require('bugfix.stable-expectations',bool(same),'Тест/fixture/config змінився: потрібен повторний RED на вихідному коді, а не підлаштування очікувань.')
            require('bugfix.order',red['observed_at_ns']<green['observed_at_ns'] and red['code']!=green['code'],'Потрібна послідовність RED → зміна реалізації → GREEN.')
        docs=task['documentation']
        if docs['applicability']=='none':add('verification.documentation','not-applicable' if meaningful(docs['reason']) else 'blocked','Нерелевантність документації є частиною погодженої специфікації.')
        elif docs['applicability']=='unknown':add('verification.documentation','not-verified','Вплив на документацію ще не перевірено.')
        else:
            actual=hashes(root,docs['paths'])
            require('verification.documentation',bool(actual) and all(v is not None for v in actual.values()) and approval is not None and actual!=approval['documentation'],'Потрібні фактичні зміни погоджених документів; зміст потребує окремого review.')
    statuses={c['status'] for c in checks}
    status='blocked' if 'blocked' in statuses else 'not-verified' if 'not-verified' in statuses else 'pass'
    return validate('gate-report',{'status':status,'allowed':status=='pass','transition':transition,'task_id':task['id'],
        'task_sha256':identity(task),'workflow_route':workflow['route'],'checks':checks,
        'scope':'Formal readiness only; no universal host enforcement, semantic guarantee or independent review claim'})
