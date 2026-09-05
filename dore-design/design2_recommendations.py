"""DORÉ DESIGN 2.0 Phase 5 recommendation and learning-event store."""
import copy,json,os,tempfile,time,uuid
from pathlib import Path
import design2_commands

SCHEMA='dore.design.recommendation-log.v1'
DECISIONS={'accept','reject','modify'}


def _load(path):
    p=Path(path)
    if not p.exists(): return {'schema':SCHEMA,'events':[]}
    data=json.loads(p.read_text(encoding='utf-8'))
    if data.get('schema')!=SCHEMA: raise ValueError('invalid_recommendation_log')
    return data


def _save(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=path.name+'.',dir=str(path.parent))
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=2,sort_keys=True)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


def propose(base,path,page_id,commands,reason='',context=None,signals=None):
    w=base.workspace();rev=int(w.get('revision',0))
    if not isinstance(commands,list) or not commands: raise ValueError('commands_required')
    # Validate commands against a copy without mutating the workspace.
    probe=copy.deepcopy(w)
    for command in commands: probe=design2_commands.apply(probe,command)
    event={
        'id':'rec-'+uuid.uuid4().hex[:16],
        'status':'proposed',
        'workspace_id':w.get('id'),
        'page_id':page_id,
        'base_revision':rev,
        'commands':copy.deepcopy(commands),
        'reason':str(reason or ''),
        'context':copy.deepcopy(context or {}),
        'signals':copy.deepcopy(signals or []),
        'proposed_at':int(time.time()),
    }
    log=_load(path);log['events'].append(event);_save(path,log)
    return event


def decide(base,path,recommendation_id,decision,expected_revision,commands=None,note=''):
    if decision not in DECISIONS: raise ValueError('invalid_decision')
    log=_load(path);event=next((e for e in log['events'] if e.get('id')==recommendation_id),None)
    if not event: raise ValueError('recommendation_not_found')
    if event.get('status')!='proposed': raise ValueError('recommendation_already_decided')
    current=base.workspace();rev=int(current.get('revision',0))
    if int(expected_revision)!=rev: raise ValueError('stale_revision')
    applied=[];result_revision=rev
    if decision in {'accept','modify'}:
        applied=copy.deepcopy(event['commands'] if decision=='accept' else commands)
        if not isinstance(applied,list) or not applied: raise ValueError('commands_required')
        updated=copy.deepcopy(current)
        for command in applied: updated=design2_commands.apply(updated,command)
        saved=base.save(updated);result_revision=int(saved.get('revision',rev))
    event.update({
        'status':'decided',
        'decision':decision,
        'applied_commands':applied,
        'result_revision':result_revision,
        'note':str(note or ''),
        'decided_at':int(time.time()),
    })
    _save(path,log)
    return copy.deepcopy(event)


def state(path):
    return _load(path)
