#!/usr/bin/env python3
from __future__ import annotations

CALENDAR_UNITS=('month','months','monthly','semester','semesters','school year','school years','个月','個月','月学习','月學習','学期','學期','学年','學年')


def _verified_pass(events, domain, stage=None):
    for x in events:
        if x.get('domain') != domain: continue
        if stage is not None and x.get('stage') != stage: continue
        if x.get('epistemic_state')=='verified' and str(x.get('status','')).lower()=='pass' and x.get('evidence_ref'):
            return True
    return False


def _unlock_count(gates, gate_id):
    return sum(1 for g in gates if gate_id in (g.get('requires') or []))


def plan(status_payload, gates):
    """Return executable gates. Calendar duration is never a readiness criterion."""
    events=(status_payload.get('learning') or {}).get('events') or []
    completed=[]; ready=[]; blocked=[]; passed=set()
    for g in gates:
        if _verified_pass(events,g['domain'],g.get('stage')):
            passed.add(g['id']); completed.append({'id':g['id'],'reason':'verified_capability'})
    for g in gates:
        if g['id'] in passed: continue
        deps=g.get('requires') or []; missing=[d for d in deps if d not in passed]
        item={'id':g['id'],'domain':g['domain'],'stage':g.get('stage'),'requires':deps,'acceptance':g.get('acceptance') or [],'next_action':g.get('next_action'),'priority':int(g.get('priority') or 0),'unlock_count':_unlock_count(gates,g['id'])}
        item['scheduler_score']=item['priority']+item['unlock_count']*10
        if missing: item['blocked_by']=missing; blocked.append(item)
        else: ready.append(item)
    ready.sort(key=lambda x:(x['scheduler_score'],x['unlock_count'],x['priority']),reverse=True)
    return {'policy':'capability-gated-v2','time_is_gate':False,'scheduler':'dependency-leverage+priority','completed':completed,'ready':ready,'blocked':blocked}


def validate_gate(gate):
    text=' '.join(str(v) for v in gate.values()).lower()
    bad=[u for u in CALENDAR_UNITS if u.lower() in text]
    if bad: raise ValueError('calendar-based learning gate forbidden: '+','.join(sorted(set(bad))))
    if not gate.get('id') or not gate.get('domain'): raise ValueError('gate requires id and domain')
    if not gate.get('acceptance'): raise ValueError('gate requires evidence-based acceptance criteria')
    return gate
