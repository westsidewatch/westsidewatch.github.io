#!/usr/bin/env python3
"""Real Mac A2A acceptance: exact historical pixels -> Doré 8D -> grounded prompt -> canonical image.generate; three specimens required."""
from __future__ import annotations
import json
from pathlib import Path
import capability_bus, production_actions
import editorial_visual_provider
from italian_editorial_evidence_bridge import observe_atlas_evidence
from editorial_observation_prompt_compiler import compile_grounded_prompt
ROOT=Path(__file__).resolve().parents[2]
EVIDENCE=ROOT/'static/dore-design/italian-editorial-evidence.v1.json'
OUT=ROOT/'artifacts/italian-editorial-real-e2e.json'
TARGETS=('casabella-367','abitare-52','il-franchi-2008-03')
def load_items():
 data=json.loads(EVIDENCE.read_text(encoding='utf-8'));items=data.get('items') or data.get('evidence') or [];return {str(x.get('id')):x for x in items}
def artifact(result):
 if not isinstance(result,dict) or not result.get('ok'):return None
 candidates=[result]+[result.get(k) for k in ('artifact','image','output','result') if isinstance(result.get(k),dict)]
 for x in candidates:
  uri=x.get('uri') or x.get('url') or x.get('image_url') or x.get('path')
  if isinstance(uri,str) and uri.strip():return uri.strip()
 return None
def main():
 items=load_items();rows=[];prov=editorial_visual_provider.provenance()
 for eid in TARGETS:
  item=items.get(eid)
  if not item:raise SystemExit(f'missing canonical evidence: {eid}')
  obs=observe_atlas_evidence(item,editorial_visual_provider.observe,provider_id=prov['providerId'],provider_kind=prov['providerKind'])
  byte_ev=(obs.get('provenance') or {}).get('imageEvidence') or {}
  if byte_ev.get('uri')!=item.get('image') or len(str(byte_ev.get('sha256','')))!=64 or int(byte_ev.get('bytes') or 0)<=0:raise SystemExit(f'byte-grounding failed: {eid}')
  prompt=compile_grounded_prompt(obs)
  result=capability_bus.call('image.generate',{'message':prompt,'prompt':prompt,'purpose':'italian-editorial-real-e2e','evidence_id':eid,'authority':'historical-image-observation','evaluation_only':True},production_actions,caller_product='italian-editorial-atlas')
  uri=artifact(result)
  if not uri:raise SystemExit(f'image.generate returned no real artifact: {eid}: {result}')
  rows.append({'evidenceId':eid,'observation':obs,'prompt':prompt,'generatedArtifact':uri,'providerResult':result})
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps({'schema':'dore.italian-editorial-real-e2e.v1','status':'ARTIFACTS_READY','cases':rows},ensure_ascii=False,indent=2),encoding='utf-8');print('DORÉ_ITALIAN_EDITORIAL_REAL_E2E=ARTIFACTS_READY');print(OUT);return 0
if __name__=='__main__':raise SystemExit(main())
