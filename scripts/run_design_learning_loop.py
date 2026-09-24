#!/usr/bin/env python3
"""Doré Design Intelligence continuous observation subloop.
Planning/orchestration layer: produces bounded work packets for the upgraded Doré autonomous loop.
It never fetches arbitrary sources itself and never promotes canonical design.
"""
import json, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'static'/'dore-design'
CONFIG=D/'design-learning-loop.v1.json'
STATE=D/'design-learning-loop-state.v1.json'

STAGES=('discover','admit-source','capture','observe','normalize-evidence','compare','distill','generate-candidate','render','beautiful-gate','learn','update-search-priorities')

def load(path, default):
    return json.loads(path.read_text()) if path.exists() else default

def validate(cfg):
    errors=[]
    if cfg.get('role')!='subloop-of-dore-autonomous-loop': errors.append('must remain a Doré big-loop subloop')
    if tuple(cfg.get('cycle',()))!=STAGES: errors.append('cycle order changed or incomplete')
    gates=cfg.get('hardGates') or {}
    if gates.get('observationMayPromoteCanonical') is not False: errors.append('observation authority escalation')
    if gates.get('generatedArtifactMayBecomeHistoricalAuthority') is not False: errors.append('generated artifact authority escalation')
    if gates.get('beautifulGateRequired') is not True: errors.append('Beautiful Gate missing')
    if gates.get('humanAuthorityForCanonicalPromotion') is not True: errors.append('human canonical authority missing')
    share=sum(float(x.get('minimumShare',0)) for x in cfg.get('sourceLanes',[]))
    if abs(share-1)>1e-9: errors.append('source lane minimum shares must sum to 1')
    return errors

def plan(cfg, state, budget=20):
    lanes=cfg['sourceLanes']; packets=[]
    assigned=0
    for lane in lanes:
        n=int(budget*lane['minimumShare']); assigned+=n
        packets.append({'lane':lane['id'],'quota':n,'mode':lane['mode'],'next':'discover','authority':'observation-only'})
    if assigned < budget:
        packets[0]['quota'] += budget-assigned
    return {
      'schema':'dore.design-learning-loop-plan.v1',
      'generatedAt':datetime.now(timezone.utc).isoformat(),
      'cycle':STAGES,
      'workPackets':packets,
      'feedbackFromPreviousCycle':state.get('feedback',[]),
      'promotion':'blocked-until-beautiful-gate-and-human-authority'
    }

def main(argv):
    cfg=load(CONFIG,{})
    errors=validate(cfg)
    if errors:
        for e in errors: print('FAIL:',e)
        return 1
    state=load(STATE,{'feedback':[]})
    budget=int(argv[1]) if len(argv)>1 else 20
    if budget<4: print('FAIL: budget must allow all four source lanes'); return 1
    print(json.dumps(plan(cfg,state,budget),ensure_ascii=False,indent=2))
    return 0
if __name__=='__main__': sys.exit(main(sys.argv))
