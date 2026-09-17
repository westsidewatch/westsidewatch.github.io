#!/usr/bin/env python3
from __future__ import annotations
import json, os, shutil, sys
from pathlib import Path
ROOT=Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parent.parent).resolve()
for p in (ROOT/'dore-design',ROOT/'local'/'dore-local'):
    if str(p) not in sys.path: sys.path.insert(0,str(p))
import design_intelligence_a2a as bridge
SPEC=ROOT/'dore-design'/'training'/'design-graduation.v0.json'
OUT=ROOT/'dore-design'/'training'/'evidence'/'graduation'

def base_snapshot():
    page={'id':'unseen-brief','canvas':{'w':1440,'h':900},'nodes':[
      {'id':'brand','type':'text','text':'Living Water Assembly West','x':72,'y':62,'w':620,'h':50,'size':20,'text_align':'left'},
      {'id':'verse','type':'text','text':'信我的人，就如經上所說：從他腹中要流出活水的江河來。 · John 7:38','x':72,'y':250,'w':980,'h':150,'size':34,'text_align':'left'},
      {'id':'life','type':'text','text':'Worship · Fellowship · Word · Prayer','x':72,'y':700,'w':900,'h':70,'size':22,'text_align':'left'}]}
    return {'schema':'dore.design.publish-snapshot.v1','workspace_id':'design-graduation-unseen','revision':1,'page_id':'unseen-brief','page':page,'tokens':{'paper':'#F4F0E6','ink':'#252525','gold':'#CEBD74'},'sha256':'graduation-unseen-seed','created_at':0}

def payload(phase, constraints):
    return {'surface_id':'dore-design-graduation-'+phase,'surface_family':'living-water-graduation-unseen','task_context':'Unseen graduation brief. Independently compose a new Living Water church editorial landing surface expressing arrival, living fellowship, Scripture, and quiet sacred presence. Do not reuse Round 01 geometry. Choose editorial grammar and design weapons yourself.','primary_axis':'composition','viewport_context':'desktop','content_context':'bilingual-sacred-editorial','scope':'surface-family','constraints':constraints,'candidates':['A','B'],'base_snapshot':base_snapshot()}

def copy_rasters(result,prefix):
    rdir=OUT/'rasters'; rdir.mkdir(parents=True,exist_ok=True); refs={}
    for c in result.get('candidates') or []:
        r=c.get('raster') or {}; src=Path(str(r.get('path') or ''))
        if src.is_file():
            dst=rdir/f'{prefix}-{c.get("candidate_id")}.png'; shutil.copy2(src,dst); refs[str(c.get('candidate_id'))]=str(dst.relative_to(ROOT))
    return refs

def compact(r):
    return {'decision':r.get('decision'),'provider':r.get('provider'),'model':r.get('model'),'winner':r.get('winner'),'consensus':r.get('consensus'),'memoryAdmitted':r.get('memory_admitted'),'loserFailures':r.get('loser_failures') or [],'repairLoop':r.get('repair_loop'),'candidates':[{'id':c.get('candidate_id'),'patch':c.get('patch'),'geometry':c.get('geometry'),'raster':c.get('raster')} for c in (r.get('candidates') or [])]}

def main():
    spec=json.loads(SPEC.read_text()); OUT.mkdir(parents=True,exist_ok=True)
    base=['preserve required authored content','beautiful is an admission floor','fresh geometry required','no Round 01 template reuse','no palette-only variation','no generic church template','Italian editorial references are teachers not authority','independently select weapons','do not promote to production']
    first=bridge.explore(payload('first-pass',base))
    before=copy_rasters(first,'first')
    failures=sorted({str(f.get('domain')) for f in (first.get('loser_failures') or []) if f.get('domain')})
    second_constraints=base+['self-diagnose first real-browser result and revise composition, typography, image direction and motion only where semantically justified']
    if failures: second_constraints.append('explicitly repair failure domains: '+', '.join(failures))
    second=bridge.explore(payload('self-revision',second_constraints))
    if second.get('decision')=='exploit':
        p=payload('self-revision-transfer',second_constraints+['produce fresh executable transfer variants rather than reuse stable pair']); p['surface_family']='living-water-graduation-transfer'; second=bridge.explore(p)
    after=copy_rasters(second,'second')
    second_failures=sorted({str(f.get('domain')) for f in (second.get('loser_failures') or []) if f.get('domain')})
    passed=bool(len(before)==2 and len(after)==2 and not second_failures and second.get('consensus'))
    report={'schema':'dore.design-graduation-evidence.v0','designer':'dore','mode':'unseen-brief','trainingSpec':spec['trainingId'],'beforeRaster':before,'afterRaster':after,'firstPassFailureDomains':failures,'finalFailureDomains':second_failures,'independentWeaponSelection':True,'freshGeometryRequired':True,'firstPass':compact(first),'selfRevision':compact(second),'graduated':passed,'winner':None,'productionPromoted':False,'canonicalWorkspaceMutated':False}
    (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'ok':passed,'graduated':passed,'report':str((OUT/'report.json').relative_to(ROOT))},ensure_ascii=False))
    if not passed: raise SystemExit(2)
if __name__=='__main__': main()
