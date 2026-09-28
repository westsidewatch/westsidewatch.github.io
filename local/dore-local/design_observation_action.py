#!/usr/bin/env python3
"""Canonical A2A admission for external Design Observation."""
from __future__ import annotations
import importlib
from typing import Any
CAPABILITIES={"design.observe.capture"}

def execute(capability:str,args:dict[str,Any]|None=None)->dict[str,Any]:
 if capability not in CAPABILITIES:return {'ok':False,'status':'failed','error':{'code':'unsupported_action','message':capability}}
 args=args or {};url=str(args.get('url') or '').strip();source_id=str(args.get('sourceId') or '').strip();viewport=str(args.get('viewport') or 'desktop')
 if not url.startswith('https://') or not source_id:return {'ok':False,'status':'failed','error':{'code':'invalid_args','message':'https url and sourceId required'}}
 snap=args.get('runtimeSnapshot')
 if not isinstance(snap,dict):
  collector=importlib.import_module('design_browser_collector');capture=collector.collect(url,source_id,viewport)
  if capture.get('ok') is not True:return {'ok':False,'status':capture.get('status','not_ready'),'capability':capability,'sourceId':source_id,'reason':(capture.get('error') or {}).get('code','external_capture_unavailable'),'capture':capture}
  snap=capture
 contract=importlib.import_module('design_runtime_capture_contract');valid,reason=contract.validate(snap,url)
 if not valid:return {'ok':False,'status':'failed' if reason in ('source_identity_mismatch','canonical_mutation_forbidden','production_promotion_forbidden') else 'not_ready','capability':capability,'sourceId':source_id,'reason':reason}
 # Feed the same browser-visible evidence into the existing provider-neutral Source Probe.
 try:
  probe=importlib.import_module('source_probe_capability');probe_result=probe.execute({'url':url,'runtimeSnapshot':contract.source_probe_snapshot(snap)})
 except Exception as exc:probe_result={'ok':False,'status':'failed','error':{'code':type(exc).__name__,'message':str(exc)}}
 shot=snap['screenshot'];observer=snap['observerPayload']
 return {'ok':True,'status':'completed','capability':capability,'sourceId':source_id,'viewport':viewport,'url':url,'finalUrl':snap['finalUrl'],'renderedAt':snap.get('renderedAt'),'screenshotRef':shot.get('ref'),'rasterEvidence':[{'real_browser_render':True,'sha256':shot['sha256']}],'observerPayload':observer,'observerStatus':'captured','sourceProbe':probe_result,'canonical_workspace_mutated':False,'production_promoted':False,'authority':{'class':'observational-evidence','mayPromoteCanonical':False,'requiresBeautifulGate':True}}
