#!/usr/bin/env python3
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'static'/'dore-design'
C=D/'design-learning-loop.v1.json'

def main():
    cfg=json.loads(C.read_text()); errors=[]
    lanes={x['id']:x for x in cfg.get('sourceLanes',[])}
    for lane in ('italian-editorial','independent-editorial','digital-web','outside-mutation'):
        if lane not in lanes: errors.append(f'missing discovery lane {lane}')
    cycle=cfg.get('cycle',[])
    for stage in ('discover','observe','compare','distill','generate-candidate','render','beautiful-gate','learn','update-search-priorities'):
        if stage not in cycle: errors.append(f'missing loop stage {stage}')
    if cycle.index('beautiful-gate') > cycle.index('learn'): errors.append('learning occurs before Beautiful Gate')
    gates=cfg.get('hardGates',{})
    checks={
      'observationMayPromoteCanonical':False,
      'generatedArtifactMayBecomeHistoricalAuthority':False,
      'beautifulGateRequired':True,
      'humanAuthorityForCanonicalPromotion':True
    }
    for k,v in checks.items():
        if gates.get(k) is not v: errors.append(f'gate violation {k}')
    if errors:
        for e in errors: print('FAIL:',e)
        return 1
    print('PASS: continuous design scanning is a bounded Doré big-loop subloop; learning cannot bypass Beautiful Gate or human canonical authority.')
    return 0
if __name__=='__main__': sys.exit(main())
