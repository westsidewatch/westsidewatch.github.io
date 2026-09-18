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
MAX_ATTEMPTS=int(os.environ.get('DORE_GRADUATION_MAX_ATTEMPTS','6'))

def base_snapshot():
    page={'id':'unseen-brief','canvas':{'w':1440,'h':900},'nodes':[
      {'id':'brand','type':'text','text':'Living Water Assembly West','x':72,'y':62,'w':620,'h':50,'size':20,'text_align':'left'},
      {'id':'verse','type':'text','text':'信我的人，就如經上所說：從他腹中要流出活水的江河來。 · John 7:38','x':72,'y':250,'w':980,'h':150,'size':34,'text_align':'left'},
      {'id':'life','type':'text','text':'Worship · Fellowship · Word · Prayer','x':72,'y':700,'w':900,'h':70,'size':22,'text_align':'left'}]}
    return {'schema':'dore.design.publish-snapshot.v1','workspace_id':'design-graduation-unseen','revision':1,'page_id':'unseen-brief','page':page,'tokens':{'paper':'#F4F0E6','ink':'#252525','gold':'#CEBD74'},'sha256':'graduation-unseen-seed','created_at':0}

def payload(phase,constraints):
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

def domains(r):
    return sorted({str(f.get('domain')) for f in (r.get('loser_failures') or []) if f.get('domain')})

def main():
    spec=json.loads(SPEC.read_text()); OUT.mkdir(parents=True,exist_ok=True)
    base=['preserve required authored content','beautiful is an admission floor','fresh geometry required','no Round 01 template reuse','no palette-only variation','no generic church template','Italian editorial references are teachers not authority','independently select weapons','do not promote to production']
    attempts=[]; previous_failures=[]; graduated=False; admitted_winner=None
    for attempt in range(1,MAX_ATTEMPTS+1):
        constraints=list(base)
        if previous_failures:
            constraints += ['This is autonomous remedial training after a failed real-browser Beauty Gate. Diagnose and materially repair the prior failure domains before attempting graduation again.','prior failure domains: '+', '.join(previous_failures),'Do not merely vary palette or reuse rejected geometry. Recompose where necessary, control typography and image direction, and use motion only when semantically justified.']
        result=bridge.explore(payload(f'attempt-{attempt}',constraints))
        if result.get('decision')=='exploit':
            p=payload(f'attempt-{attempt}-transfer',constraints+['produce fresh executable transfer variants rather than reuse a stable pair']); p['surface_family']=f'living-water-graduation-transfer-{attempt}'; result=bridge.explore(p)
        refs=copy_rasters(result,f'attempt-{attempt}')
        loser_failure_domains=domains(result)
        winner=result.get('winner')
        consensus=bool(result.get('consensus'))
        # loser_failures describe the rejected alternate, not the admitted winner.
        # Graduation is established when the real-browser critic reaches consensus on
        # a concrete winner with complete raster evidence. Rejected-alternate failures
        # remain evidence but must not veto the winner.
        passed=bool(len(refs)==2 and consensus and winner in refs)
        attempts.append({'attempt':attempt,'rasters':refs,'rejectedAlternateFailureDomains':loser_failure_domains,'result':compact(result),'passed':passed})
        final_failures=[] if passed else (loser_failure_domains or ['beauty-gate-no-consensus'])
        report={'schema':'dore.design-graduation-evidence.v2','designer':'dore','mode':'unseen-brief','trainingSpec':spec['trainingId'],'attempts':attempts,'finalFailureDomains':final_failures,'independentWeaponSelection':True,'freshGeometryRequired':True,'graduated':passed,'admittedWinner':winner if passed else None,'winner':None,'productionPromoted':False,'canonicalWorkspaceMutated':False}
        (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'attempt':attempt,'graduated':passed,'consensus':consensus,'admittedWinner':winner if passed else None,'rejectedAlternateFailureDomains':loser_failure_domains,'rasters':len(refs)},ensure_ascii=False),flush=True)
        if passed:
            graduated=True; admitted_winner=winner; break
        previous_failures=final_failures
    print(json.dumps({'ok':graduated,'graduated':graduated,'attempts':len(attempts),'admittedWinner':admitted_winner,'report':str((OUT/'report.json').relative_to(ROOT))},ensure_ascii=False))
    return 0 if graduated else 2
if __name__=='__main__': raise SystemExit(main())
