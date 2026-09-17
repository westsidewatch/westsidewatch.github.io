#!/usr/bin/env python3
"""Design Observation A2A action.
Consumes capture jobs through the existing Doré local/A2A control plane.
It does not create a second browser runtime and does not claim capture success without a proven raster.
"""
from __future__ import annotations
import importlib, os, sys
from pathlib import Path
CAPABILITIES={"design.observe.capture"}

def _repo(): return Path(os.environ.get("DORE_REPO_ROOT") or Path(__file__).resolve().parents[2]).resolve()

def execute(capability,args=None):
 if capability not in CAPABILITIES:return {'ok':False,'status':'failed','error':{'code':'unsupported_action','message':capability}}
 args=args or {}; url=str(args.get('url') or '').strip(); source_id=str(args.get('sourceId') or '').strip(); viewport=str(args.get('viewport') or 'desktop')
 if not url.startswith('https://') or not source_id:return {'ok':False,'status':'failed','error':{'code':'invalid_args','message':'https url and sourceId required'}}
 repo=_repo(); design=repo/'dore-design'; local=repo/'local'/'dore-local'
 for p in (str(design),str(local)):
  if p not in sys.path:sys.path.insert(0,p)
 try:
  # Canonical real Design runtime already owns model-backed browser rasters.
  bridge=importlib.import_module('design_intelligence_a2a')
  snapshot={'schema':'dore.design.publish-snapshot.v1','workspace_id':f'observe:{source_id}','revision':1,'page_id':'p','page':{'id':'p','canvas':{'w':1440 if viewport=='desktop' else 390,'h':1000 if viewport=='desktop' else 844},'nodes':[{'id':'source','type':'text','text':url,'x':20,'y':20,'w':1200 if viewport=='desktop' else 350,'h':60,'size':16,'text_align':'left'}]},'tokens':{},'sha256':f'observe-{source_id}-{viewport}','created_at':0}
  payload={'surface_id':f'observe:{source_id}:{viewport}','surface_family':'design-observation','task_context':f'Observe public design source {url}; capture visual evidence only; do not imitate or promote.','primary_axis':'composition','viewport_context':viewport,'content_context':'external-design-evidence','scope':'observation-only','constraints':['preserve source provenance','real browser raster required','no canonical mutation','no production promotion'],'candidates':['observation-A','observation-B'],'base_snapshot':snapshot}
  result=bridge.explore(payload); candidates=result.get('candidates') or []; rasters=[c.get('raster') or {} for c in candidates]; proven=[r for r in rasters if r.get('real_browser_render') is True and r.get('sha256')]
  if not proven:return {'ok':False,'status':'not_ready','capability':capability,'sourceId':source_id,'reason':'canonical_design_runtime_returned_no_proven_browser_raster'}
  return {'ok':True,'status':'completed','capability':capability,'sourceId':source_id,'viewport':viewport,'url':url,'provider':result.get('provider'),'model':result.get('model'),'rasterEvidence':[{'real_browser_render':True,'sha256':r['sha256']} for r in proven],'canonical_workspace_mutated':result.get('canonical_workspace_mutated'),'production_promoted':result.get('production_promoted'),'authority':{'class':'observational-evidence','mayPromoteCanonical':False,'requiresBeautifulGate':True}}
 except Exception as exc:return {'ok':False,'status':'failed','capability':capability,'error':{'code':type(exc).__name__,'message':str(exc)}}
