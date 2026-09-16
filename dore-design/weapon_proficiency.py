#!/usr/bin/env python3
"""Doré Design weapon proficiency executor.

Trainer supplies curriculum and references. Doré local Design Intelligence generates,
rasters, critiques, remembers failures, and self-revises in executable sandboxes.
This module does not manufacture a finished design and never promotes production.
Critic structured-output containment is provided by the resident worker; this executor
remains evidence-driven and never substitutes fixture results for model-backed training.
"""
from __future__ import annotations
import argparse, json, os, shutil, sys
from pathlib import Path

ROOT=Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parent.parent).resolve()
DESIGN=ROOT/'dore-design'; LOCAL=ROOT/'local'/'dore-local'
for p in (DESIGN,LOCAL):
    if str(p) not in sys.path: sys.path.insert(0,str(p))
import design_intelligence_a2a as bridge

IDS=['sacred-threshold','living-community','quiet-light','architectural-bloom']
ASSIGNMENTS={
 'sacred-threshold':'Campo Grafico emergence + Domus architectural hierarchy + Casabella deliberate negative space',
 'living-community':'Abitare human-scale pacing + Campo Grafico local-object persistence',
 'quiet-light':'Casabella deliberate negative space + Abitare cultured restraint',
 'architectural-bloom':'Ottagono modular grid/controlled break + Domus architectural construction',
}

def snapshot(cid:str)->dict:
    labels={
      'sacred-threshold':('LIVING WATER','LET THE CHURCH BLOOM','信我的人，就如經上所說：從他腹中要流出活水的江河來。','A threshold into worship, Scripture and community.'),
      'living-community':('LIVING WATER','CHURCH IS RELATIONSHIP','Worship · Fellowship · Word · Prayer','A living field shaped by people rather than a generic church template.'),
      'quiet-light':('LIVING WATER','BE STILL.','你們要休息，要知道我是神。','Quiet light must carry hierarchy without decorative emptiness.'),
      'architectural-bloom':('LIVING WATER','ARCHITECTURAL BLOOM','5:8 · WALL · EDITORIAL GRAVITY','Four visual units must resolve as one precise architectural whole.'),
    }
    eyebrow,title,body,note=labels[cid]
    page={'id':cid,'canvas':{'w':1440,'h':900},'nodes':[
      {'id':'eyebrow','type':'text','text':eyebrow,'x':88,'y':74,'w':520,'h':38,'size':18,'text_align':'left'},
      {'id':'hero','type':'text','text':title,'x':88,'y':158,'w':980,'h':190,'size':78,'text_align':'left'},
      {'id':'body','type':'text','text':body,'x':88,'y':430,'w':760,'h':110,'size':28,'text_align':'left'},
      {'id':'note','type':'text','text':note,'x':900,'y':650,'w':420,'h':96,'size':18,'text_align':'left'},
      {'id':'rule','type':'rule','x':88,'y':594,'w':1240,'h':1},
    ]}
    return {'schema':'dore.design.publish-snapshot.v1','workspace_id':'living-water-weapon-proficiency-01','revision':1,'page_id':cid,'page':page,'tokens':{'paper':'#F4F0E6','ink':'#252525','night':'#171813','gold':'#CEBD74','morning':'#CEBD74'},'sha256':'training-'+cid,'created_at':0}

def payload(cid:str, phase:str, constraints:list[str])->dict:
    return {
      'surface_id':f'living-water-training-{cid}-{phase}',
      'surface_family':'living-water-weapon-proficiency',
      'task_context':f'Weapon Proficiency Round 01 {phase}. Refine the existing {cid} direction; do not invent a fifth direction. Italian editorial reference: {ASSIGNMENTS[cid]}.',
      'primary_axis':'composition','viewport_context':'desktop','content_context':'bilingual-sacred-editorial',
      'scope':'surface-family','constraints':constraints,'candidates':['A','B'],'base_snapshot':snapshot(cid)
    }

def compact(result:dict)->dict:
    return {
      'taskId':result.get('task_id'),'provider':result.get('provider'),'model':result.get('model'),'winner':result.get('winner'),
      'consensus':result.get('consensus'),'memoryAdmitted':result.get('memory_admitted'),'loserFailures':result.get('loser_failures') or [],
      'repairLoop':result.get('repair_loop'),'rejectionEnforcement':result.get('rejection_enforcement'),
      'candidates':[{'id':c.get('candidate_id'),'patch':c.get('patch'),'geometry':c.get('geometry'),'raster':c.get('raster')} for c in (result.get('candidates') or [])]
    }

def copy_rasters(result:dict,target:Path,prefix:str)->dict:
    target.mkdir(parents=True,exist_ok=True); refs={}
    for c in result.get('candidates') or []:
        r=c.get('raster') or {}; src=Path(str(r.get('path') or ''))
        if src.is_file():
            dst=target/f'{prefix}-{c.get("candidate_id")}.png'; shutil.copy2(src,dst); refs[str(c.get('candidate_id'))]=str(dst.relative_to(ROOT))
    return refs

def run():
    spec=json.loads(Path(os.environ['DORE_TRAINING_SPEC']).read_text())
    evidence=ROOT/'dore-design'/'training'/'evidence'/'round-01'; rasters=evidence/'rasters'; evidence.mkdir(parents=True,exist_ok=True)
    base_constraints=['preserve authored text','preserve Living Water identity','beautiful is an admission floor','do not solve by palette swap','use grid/span/offset/negative-space/scale intentionally','reference is teacher not authority','do not imitate a publication','do not promote to production']
    rows=[]
    for cid in IDS:
        first=bridge.explore(payload(cid,'first-pass',base_constraints+[f'candidate assignment: {ASSIGNMENTS[cid]}']))
        first_refs=copy_rasters(first,rasters,cid+'-first')
        failures=sorted({str(f.get('domain')) for f in (first.get('loser_failures') or []) if f.get('domain')})
        second_constraints=base_constraints+[f'candidate assignment: {ASSIGNMENTS[cid]}','self-revise after first real-browser critique']
        if failures: second_constraints.append('explicitly avoid first-pass failure domains: '+', '.join(failures))
        second=bridge.explore(payload(cid,'self-revision',second_constraints))
        if second.get('decision')=='exploit':
            p=payload(cid,'self-revision-transfer',second_constraints+['produce fresh executable transfer variants rather than reuse a stable pair'])
            p['surface_family']='living-water-weapon-proficiency-transfer'; second=bridge.explore(p)
        second_refs=copy_rasters(second,rasters,cid+'-second')
        rows.append({
          'id':cid,'assignment':ASSIGNMENTS[cid],
          'diagnosis':{'firstPassFailureDomains':failures,'trainerQuestion':'What is carrying visual gravity, and is every empty region active composition?'},
          'weaponsUsed':['design.composition','design.typography','design.image-art-direction'],
          'beforeRaster':first_refs,'afterRaster':second_refs,'firstPass':compact(first),'selfRevision':compact(second)
        })
    report={'schema':'dore.design-weapon-proficiency-evidence.v0','designer':'dore','round':1,'surface':'living-water-bloom-armed-v2','trainingSpec':spec.get('trainingId'),'winner':None,'productionPromoted':False,'canonicalWorkspaceMutated':False,'candidates':rows}
    (evidence/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'ok':True,'round':1,'candidates':len(rows),'report':str((evidence/'report.json').relative_to(ROOT))},ensure_ascii=False))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--round');ap.add_argument('--execute',action='store_true');ap.add_argument('--raster',action='store_true');ap.add_argument('--self-revise',action='store_true');ap.parse_args();run()
