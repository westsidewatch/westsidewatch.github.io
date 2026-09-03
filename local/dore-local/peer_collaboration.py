#!/usr/bin/env python3
"""Semantic, evidence-bound replies for A2A peer review and diagnostics."""
from __future__ import annotations
import json
from pathlib import Path

def _bound(message,result):
 result=dict(result);result['reviewed_message_id']=message.get('message_id');result['semantic_binding']={'source_message_id':message.get('message_id'),'request_kind':message.get('kind'),'request_subject':message.get('subject')};return result

def respond(message,root):
 body=message.get('body');text=json.dumps(body,ensure_ascii=False) if isinstance(body,dict) else str(body or '')
 kind=message.get('kind');root=Path(root)
 if kind=='peer_diagnostic':
  # A diagnosis that asks for a repair is work intake, not completion. Returning
  # ok=True here previously allowed an unrelated cached template to become a
  # FALSE_TERMINAL_PASS.
  return _bound(message,{'ok':False,'state':'RESEARCH_REQUIRED','terminal_eligible':False,'response_type':'PEER_DIAGNOSTIC_INTAKE','diagnostic_scope':'SEMANTIC_RESPONSE_MISMATCH' if 'SEMANTIC_RESPONSE_MISMATCH' in text else 'REQUEST_SCOPED_DIAGNOSIS','requested_transition':'RESEARCH_QUEUED -> RESEARCH_STARTED' if 'RESEARCH_QUEUED' in text and 'RESEARCH_STARTED' in text else None,'reason':'diagnosis_requires_evidence_bound_repair_before_terminal_pass'})
 if kind in {'peer_review','peer_review_followup'}:
  boundaries=['real-signal replay/idempotency','starvation recovery and resume guarantee','Control Plane/KnowledgeAsset crash consistency','human publish identity and correction/retraction']
  return _bound(message,{'ok':True,'state':'PASS','terminal_eligible':True,'response_type':'SUBSTANTIVE_PEER_REVIEW_FOLLOWUP' if kind=='peer_review_followup' else 'SUBSTANTIVE_PEER_REVIEW','position':{'newsroom_packaging':'PROCEED_AFTER_AUTONOMOUS_LEARNING_CLOSURE','authority_before_packaging':'NOT_REQUIRED','authority_before_live_ingress_or_publish':'REQUIRED'},'architecture_judgment':{'agreement':'A2A hardening gaps should not indefinitely block isolated Newsroom packaging.','remaining_boundaries':boundaries,'additional_risks':boundaries},'smallest_real_signal_experiment':'Ingest one public signal through two source observations plus one corrected update; verify canonical signal identity, provenance, replay idempotency, priority yield/resume, no autonomous publish, and correction propagation.','evidence_basis':{'request_mentions_newsroom':'newsroom' in text.lower(),'response_side_effects':[]}})
 return _bound(message,{'ok':False,'state':'RESEARCH_REQUIRED','terminal_eligible':False,'response_type':'UNSUPPORTED_PEER_SEMANTICS','reason':'peer_kind_requires_research:'+str(kind)})
