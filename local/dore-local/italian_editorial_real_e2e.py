#!/usr/bin/env python3
"""Real Mac A2A: exact pixels -> Doré 8D (grounded teacher fallback if Doré has zero facts) -> prompt -> canonical image.generate."""
from __future__ import annotations
import json
from pathlib import Path
import capability_bus, production_actions
import editorial_visual_provider
from italian_editorial_evidence_bridge import observe_atlas_evidence
from editorial_observation_prompt_compiler import compile_grounded_prompt
ROOT=Path(__file__).resolve().parents[2]
EVIDENCE=ROOT/'static/dore-design/italian-editorial-evidence.v1.json'; TEACHER=ROOT/'static/dore-design/italian-editorial-grounded-observations.v0.json'; OUT=ROOT/'artifacts/italian-editorial-real-e2e.json'
TARGETS=('casabella-367','abitare-52','il-franchi-2008-03')
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def observed_count(obs):return sum(1 for x in (obs.get('dimensions') or {}).values() if x.get('status')=='observed' and x.get('facts'))
def artifact(result):
 if not isinstance(result,dict) or not result.get('ok'):return None
 for x in [result]+[result.get(k) for k in ('artifact','image','output','result') if isinstance(result.get(k),dict)]:
  uri=x.get('uri') or x.get('url') or x.get('image_url') or x.get('path') or x.get('asset_url')
  if isinstance(uri,str) and uri.strip():return uri.strip()
 return None
def main():
 # A 403 from the resident image provider is a runtime-health failure, not a prompt failure.
 # Repair/reinstall the canonical model-backed image runtime once before evaluating the three cases.
 repaired=production_actions.execute('image.local.repair',{})
 if not repaired.get('ok'):
  raise SystemExit(f'image.local.repair failed before E2E: {repaired}')
 items={str(x.get('id')):x for x in load(EVIDENCE).get('items',[])}; teachers={(x.get('evidence') or {}).get('id'):x for x in load(TEACHER).get('items',[])};rows=[];prov=editorial_visual_provider.provenance()
 for eid in TARGETS:
  item=items[eid]; local=observe_atlas_evidence(item,editorial_visual_provider.observe,provider_id=prov['providerId'],provider_kind=prov['providerKind']); byte_ev=(local.get('provenance') or {}).get('imageEvidence') or {}
  if byte_ev.get('uri')!=item.get('image') or len(str(byte_ev.get('sha256','')))!=64 or int(byte_ev.get('bytes') or 0)<=0:raise SystemExit(f'byte-grounding failed: {eid}')
  obs=local; fallback=False
  if observed_count(local)==0:
   obs=teachers.get(eid)
   if not obs:raise SystemExit(f'Doré returned no observed facts and no grounded teacher exists: {eid}')
   if (obs.get('provenance') or {}).get('imageUri')!=item.get('image'):raise SystemExit(f'teacher exact-image binding mismatch: {eid}')
   fallback=True
  prompt=compile_grounded_prompt(obs)
  result=capability_bus.call('image.generate',{'message':prompt,'prompt':prompt,'purpose':'italian-editorial-real-e2e','evidence_id':eid,'authority':'historical-image-observation','evaluation_only':True},production_actions,caller_product='italian-editorial-atlas')
  uri=artifact(result)
  if not uri:raise SystemExit(f'image.generate returned no real artifact: {eid}: {result}')
  rows.append({'evidenceId':eid,'localDoréObservation':local,'promptObservation':obs,'teacherFallbackUsed':fallback,'prompt':prompt,'generatedArtifact':uri,'evaluationOnly':True,'providerResult':result})
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps({'schema':'dore.italian-editorial-real-e2e.v1','status':'ARTIFACTS_READY','cases':rows},ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'cases':[{'id':r['evidenceId'],'doreObservedDimensions':observed_count(r['localDoréObservation']),'teacherFallback':r['teacherFallbackUsed'],'artifact':r['generatedArtifact']} for r in rows]},ensure_ascii=False));print('DORÉ_ITALIAN_EDITORIAL_REAL_E2E=ARTIFACTS_READY');return 0
if __name__=='__main__':raise SystemExit(main())
