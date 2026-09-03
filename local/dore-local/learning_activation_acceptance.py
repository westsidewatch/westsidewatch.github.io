#!/usr/bin/env python3
"""Isolated acceptance for semantic binding and durable learning activation."""
from __future__ import annotations
import importlib, json, os, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];LOCAL=ROOT/'local'/'dore-local';sys.path.insert(0,str(LOCAL))
def main():
 checks=[]
 def check(name,value,detail=None):checks.append({'check':name,'pass':bool(value),'detail':detail})
 with tempfile.TemporaryDirectory(prefix='dore-learning-activation-') as td:
  os.environ['DORE_LOCAL_HOME']=td
  import goal_queue
  importlib.reload(goal_queue)
  goal_queue.enqueue('product','product-loop',priority='high')
  goal_queue.current()
  message={'message_id':'fixture-peer-followup','kind':'peer_review_followup','requires_reply':True}
  goal_queue.enqueue('fixture-peer-followup','newsroom',priority='high',source='coordination_worker',metadata={'execution_kind':'coordination_message','requires_reply':True,'message':message})
  learning=Path(td)/'coordination'/'learning'/'fixture-peer-followup.json';learning.parent.mkdir(parents=True);learning.write_text(json.dumps({'state':'RESEARCH_REQUIRED','observed_at':'2026-09-03T13:39:59Z'}))
  selected=goal_queue.current();rows={x['goal_id']:x for x in goal_queue.load()['goals']}
  check('durable learning request preempts active product loop',selected.get('goal_id')=='fixture-peer-followup',selected)
  check('preempted loop is checkpointed',rows['product']['status']=='PAUSED',rows['product'])
  check('activation reason is durable and explicit',(selected.get('metadata') or {}).get('activation_reason')=='DURABLE_RESEARCH_REQUIRED',selected)
  goal_queue.enqueue('older-learning','other',priority='critical',source='coordination_worker',metadata={'execution_kind':'coordination_message','requires_reply':True,'message':{'message_id':'older-learning'}})
  older=Path(td)/'coordination'/'learning'/'older-learning.json';older.write_text(json.dumps({'state':'RESEARCH_REQUIRED','observed_at':'2026-09-02T00:00:00Z'}))
  selected_again=goal_queue.current();check('active learning claim is idempotent within nested driver reads',selected_again.get('goal_id')=='fixture-peer-followup' and goal_queue.get('fixture-peer-followup').get('status')=='ACTIVE',selected_again)
  import coordination_completion
  importlib.reload(coordination_completion);sent=[];coordination_completion.send_to_chatgpt=lambda *a,**k: sent.append((a,k)) or {'message_id':k.get('message_id')}
  ctx={'goal_id':'fixture-peer-followup','goal':'newsroom','metadata':{'message':message}}
  job={'research_id':'research-fixture','history':[{'state':x} for x in ['RESEARCH_QUEUED','RESEARCHING','KNOWLEDGE_RETURNED','EXPERIMENTING','VERIFIED','PROMOTED','RESUME_PARENT']]}
  driver={'result':{'coordination_goal':{'result':{'ok':True,'reviewed_message_id':'fixture-peer-followup','response_type':'SUBSTANTIVE_PEER_REVIEW_FOLLOWUP'}}}}
  receipt=coordination_completion.complete(ctx,job,driver);check('terminal receipt requires and preserves full learning chain',receipt.get('ok') is True and len(sent)==1 and sent[0][1].get('message_id')=='result-fixture-peer-followup',receipt)
  bad={'result':{'coordination_goal':{'result':{'ok':True,'reviewed_message_id':'stale-message'}}}}
  rejected=coordination_completion.complete(ctx,job,bad);check('stale semantic result cannot become terminal receipt',rejected.get('error')=='semantic_completion_binding_failed',rejected)
 from peer_collaboration import respond
 diagnostic={'message_id':'diag-new','kind':'peer_diagnostic','subject':'semantic mismatch','body':{'classification':'SEMANTIC_RESPONSE_MISMATCH / FALSE_TERMINAL_PASS','required':'RESEARCH_QUEUED -> RESEARCH_STARTED'}}
 dr=respond(diagnostic,ROOT);check('diagnostic cannot terminal-pass without repair evidence',dr.get('ok') is False and dr.get('terminal_eligible') is False,dr);check('diagnostic semantic scope is current request',dr.get('requested_transition')=='RESEARCH_QUEUED -> RESEARCH_STARTED' and dr.get('reviewed_message_id')=='diag-new',dr)
 follow={'message_id':'fixture-peer-followup','kind':'peer_review_followup','subject':'Newsroom followup','body':{'peer_question':'smallest real signal?'}}
 fr=respond(follow,ROOT);check('followup response is source-bound',fr.get('ok') is True and fr.get('reviewed_message_id')=='fixture-peer-followup' and (fr.get('semantic_binding') or {}).get('source_message_id')=='fixture-peer-followup',fr)
 source=(LOCAL/'dore_agent_core.py').read_text();driver=(LOCAL/'autonomous_driver.py').read_text();check('agent imports control-plane modules from control root','CONTROL_ROOT' in source and "LOCAL=CONTROL_ROOT/'local'/'dore-local'" in source);check('driver imports control-plane modules from control root','CONTROL_ROOT' in driver and "LOCAL=CONTROL_ROOT/'local'/'dore-local'" in driver)
 ok=all(x['pass'] for x in checks);print(json.dumps({'ok':ok,'schema':'dore.learning-activation-acceptance.v1','checks':checks},ensure_ascii=False));return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
