#!/usr/bin/env python3
"""Executable acceptance for newly adopted autonomous-loop components."""
from __future__ import annotations
import json,os,sys,time
from pathlib import Path
ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.cwd())).resolve();LOCAL=ROOT/'local'/'dore-local';sys.path.insert(0,str(LOCAL))

def check(name,fn,rows):
 try:detail=fn();rows.append({'check':name,'pass':bool(detail if isinstance(detail,bool) else detail.get('ok',True)),'detail':detail})
 except Exception as e:rows.append({'check':name,'pass':False,'detail':repr(e)})
def main():
 rows=[]
 def durable():
  import durable_store as d
  h=d.health();e=d.append_event('acceptance',state='EXPERIMENTING',goal_id='ecosystem-component-acceptance',payload={'source':'global-benchmark'});d.checkpoint_put('acceptance','checkpoint',{'event':e});r=d.checkpoint_get('acceptance','checkpoint');lease=d.acquire_lease('acceptance-resource',owner='acceptance',ttl=30);duplicate=d.acquire_lease('acceptance-resource',owner='other',ttl=30);d.release_lease('acceptance-resource','acceptance');idem1=d.idempotency_begin('acceptance-idempotency');d.idempotency_finish('acceptance-idempotency','PASS',{'ok':True});idem2=d.idempotency_begin('acceptance-idempotency');return {'ok':h.get('ok') and r and lease.get('acquired') and not duplicate.get('acquired') and idem1.get('acquired') and not idem2.get('acquired'),'health':h,'lease':lease,'duplicate':duplicate,'idempotency_replay':idem2}
 check('SQLite WAL checkpoint/event/lease/idempotency',durable,rows)
 def retry():
  from retry_policy import classify
  same=classify({'e':'same'},{'e':'same'},1);new=classify({'e':'old'},{'e':'new'},1);budget=classify({'e':'a'},{'e':'b'},6);return {'ok':same['action']=='BLOCK_IDENTICAL_RETRY' and new['action']=='RETRY_WITH_NEW_HYPOTHESIS' and budget['action']=='RESEARCH_OR_STOP','same':same,'new':new,'budget':budget}
 check('information-gain retry policy',retry,rows)
 def guard():
  from loop_guardrails import decide
  active=decide(state='RUNNING',turn=1,started_epoch=time.time());human=decide(state='RUNNING',turn=1,started_epoch=time.time(),reason='account_login_approval');turns=decide(state='RUNNING',turn=50,started_epoch=time.time());return {'ok':active['continue'] and human['terminal']=='HUMAN_GATE' and turns['terminal']=='RESEARCH_REQUIRED','active':active,'human':human,'turns':turns}
 check('autonomy and HUMAN_GATE guardrails',guard,rows)
 def trace():
  from trace_context import ids,child
  p=ids();c=child(p);return {'ok':len(p['trace_id'])==32 and len(p['span_id'])==16 and c['trace_id']==p['trace_id'] and c['parent_span_id']==p['span_id'],'parent':p,'child':c}
 check('trace/span correlation',trace,rows)
 def files():
  req=['dore-design/knowledge-lab/a2a/global-component-benchmark-2026-09-01.md','dore-design/knowledge-lab/resources/component-selection-2026-09-01.json','local/dore-local/durable_store.py','local/dore-local/retry_policy.py','local/dore-local/loop_guardrails.py','local/dore-local/trace_context.py'];missing=[x for x in req if not (ROOT/x).exists()];return {'ok':not missing,'missing':missing}
 check('benchmark and selected components exist',files,rows)
 ok=all(x['pass'] for x in rows);print(json.dumps({'ok':ok,'schema':'dore.ecosystem-component-acceptance.v1','passed':sum(1 for x in rows if x['pass']),'total':len(rows),'checks':rows},ensure_ascii=False));return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
