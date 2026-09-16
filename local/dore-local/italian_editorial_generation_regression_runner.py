#!/usr/bin/env python3
"""Run the three Italian Editorial regression specimens through canonical image.generate.

This runner does not implement an image generator. It consumes the existing DORÉ Core
image.generate capability through capability_bus, preserving one canonical generation
path. It fails closed if the local image service is unavailable and never fabricates
an artifact URI.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import capability_bus
import production_actions

ROOT=Path(__file__).resolve().parents[2]
OBS_PATH=ROOT/'static/dore-design/italian-editorial-grounded-observations.v0.json'
GRAMMAR_PATH=ROOT/'static/dore-design/italian-editorial-grammars.v1.json'
REG_PATH=ROOT/'static/dore-design/italian-editorial-generation-regression.v1.json'
DIMS=('layout','image','typography','material','density','sequence','irony','emergence')


def _load(path:Path)->dict[str,Any]:return json.loads(path.read_text(encoding='utf-8'))
def _now()->str:return datetime.now(timezone.utc).isoformat()

def _grammar_context(publication:str,era:str)->list[str]:
    data=_load(GRAMMAR_PATH)
    for family in data.get('families',[]):
        for row in family.get('eras',[]):
            if family.get('id')==publication and row.get('id')==era:
                return [f'{module}: {value}' for module,values in (row.get('grammar') or {}).items() for value in values]
    return []

def compile_prompt(observation:dict[str,Any])->str:
    evidence=observation['evidence'];publication=str(evidence['publication']);era=str(evidence['era'])
    lines=[
        'Recompose the supplied test subject as an editorial cover.',
        'The exact historical evidence relationships below are the concrete visual authority.',
        'Italian lineage terms are context only and must not invent visible content.',
        'Do not copy the historical masthead, logo, named person, or original cover text.',
        '',
        'EXACT EVIDENCE OBSERVATION:'
    ]
    for dim in DIMS:
        item=(observation.get('dimensions') or {}).get(dim) or {}
        if item.get('status')=='observed':
            lines.append(f'{dim.upper()}:')
            lines.extend(f'- {fact}' for fact in item.get('facts',[]))
        else:
            lines.append(f'{dim.upper()}: insufficient; do not invent evidence for this dimension.')
    context=_grammar_context(publication,era)
    if context:
        lines.extend(['','DESIGN DNA — CONTEXT ONLY:']+[f'- {x}' for x in context])
    lines.extend([
        '',
        'FIDELITY CONTRACT:',
        '- Preserve the observed area ratios, crop logic, hierarchy, image count, text/image relationship, negative space and material/color relationships.',
        '- Do not add architecture, concrete, furniture, grids, geometric decorations, extra photographs, overlays or materials unless the observation explicitly supports them.',
        '- A visually attractive result is not sufficient: it must remain recognizably derived from this exact evidence image relationships.',
        f"- Evidence authority: {evidence['id']}. Generated output is evaluation-only."
    ])
    return '\n'.join(lines)

def _artifact_from_result(result:dict[str,Any])->dict[str,Any]|None:
    candidates=[]
    for key in ('artifact','image','output','result'):
        value=result.get(key)
        if isinstance(value,dict):candidates.append(value)
    candidates.append(result)
    for value in candidates:
        uri=value.get('uri') or value.get('url') or value.get('image_url') or value.get('path')
        if isinstance(uri,str) and uri.strip():
            route=result.get('core_route') or {}
            return {'uri':uri.strip(),'generator':str(route.get('provider') or 'dore-image-local'),'generatedAt':_now(),'coreRoute':route}
    return None

def run_case(case:dict[str,Any],observation:dict[str,Any])->dict[str,Any]:
    prompt=compile_prompt(observation)
    args={
        'message':prompt,
        'prompt':prompt,
        'purpose':'italian-editorial-generation-regression',
        'evidence_id':case['evidenceId'],
        'authority':'grounded-observation',
        'evaluation_only':True,
    }
    result=capability_bus.call('image.generate',args,production_actions,caller_product='italian-editorial-atlas')
    artifact=_artifact_from_result(result) if isinstance(result,dict) and result.get('ok') else None
    return {'caseId':case['id'],'evidenceId':case['evidenceId'],'prompt':prompt,'providerResult':result,'generatedArtifact':artifact}

def main()->int:
    reg=_load(REG_PATH);obs=_load(OBS_PATH);by_id={(x.get('evidence') or {}).get('id'):x for x in obs.get('items',[])}
    outputs=[];unavailable=[]
    for case in reg.get('cases',[]):
        eid=case.get('evidenceId');observation=by_id.get(eid)
        if not observation:raise SystemExit(f'missing grounded observation: {eid}')
        row=run_case(case,observation);outputs.append(row)
        if not row['generatedArtifact']:unavailable.append({'evidenceId':eid,'providerResult':row['providerResult']})
    report={'schema':'dore.italian-editorial-generation-run.v1','generatedAt':_now(),'cases':outputs}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if unavailable:
        print('ITALIAN_EDITORIAL_REAL_GENERATION=NOT_AVAILABLE')
        print('No artifact was invented; canonical image.generate must return a real artifact before visual comparison.')
        return 2
    print('ITALIAN_EDITORIAL_REAL_GENERATION=ARTIFACTS_READY')
    return 0

if __name__=='__main__':raise SystemExit(main())
