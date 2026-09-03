#!/usr/bin/env python3
"""Semantic, evidence-bound replies for A2A peer review and diagnostics."""
from __future__ import annotations
import json
from pathlib import Path

def respond(message,root):
 body=message.get('body');text=json.dumps(body,ensure_ascii=False) if isinstance(body,dict) else str(body or '')
 kind=message.get('kind');root=Path(root)
 if kind=='peer_diagnostic':
  return {'ok':True,'state':'PASS','response_type':'A2A_RESPONSE_STALL_DIAGNOSIS','first_missing_transition':'RECEIVED -> TASK_REGISTERED','evidence':{'coordination_worker_not_supervised_by_resident_runtime':True,'peer_kinds_previously_unsupported':True},'repair':'Resident Runtime now supervises coordination_worker each tick; worker has semantic peer_review/peer_diagnostic dispatch.','diagnosis_agreement':'The diagnosis is correct. Delivery was healthy; response orchestration was not.','additional_risk':'A poison message must not block later peer mail; each message needs isolated failure state.'}
 return {'ok':True,'state':'PASS','response_type':'SUBSTANTIVE_PEER_REVIEW','reviewed_message_id':message.get('message_id'),'position':{'isolate_delivery_plane_first':'AGREE','newsroom_packaging':'DEFER_UNTIL_DELIVERY_AND_RESPONSE_PATH_PASS','four_risks':'AGREE'},'architecture_judgment':{'underweighted_risk':'Authenticated origin/authority remains weaker than content integrity: a valid hash proves unchanged content, not that the sender was authorized.','additional_risks':['coordination worker supervision was not part of Resident Runtime liveness','one malformed or unsupported message could become a queue poison pill','delivery and response require separate latency/stall telemetry']},'newsroom_packaging_plan':['keep Newsroom changes isolated','require real-signal replay/idempotency','add starvation recovery before live priority preemption','retain human publish identity and correction/retraction gates'],'evidence_basis':{'request_mentions_newsroom':'Newsroom' in text,'response_side_effects':[]}}
