#!/usr/bin/env python3
"""Persist bounded Design Learning feedback; never mutate canonical design."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('feedback');p.add_argument('--state',default='static/dore-design/design-learning-loop-state.v1.json');a=p.parse_args();fp=Path(a.feedback);sp=Path(a.state);r=json.loads(fp.read_text(encoding='utf-8'));s=json.loads(sp.read_text(encoding='utf-8'))
 if r.get('ok') is not True or r.get('status')!='completed':raise SystemExit('completed Beautiful Gate feedback required')
 if (r.get('beautifulGate') or {}).get('authority')!='human':raise SystemExit('human Beautiful Gate authority required')
 if (r.get('learning') or {}).get('canonicalWrite') is not False:raise SystemExit('canonical write forbidden')
 entry={'candidateId':r.get('candidateId'),'decision':(r.get('beautifulGate') or {}).get('decision'),'learning':r.get('learning'),'nextCycleFeedback':r.get('nextCycleFeedback')};s.setdefault('feedback',[]).append(entry);s['cycle']=max(int(s.get('cycle',0)),1);s['canonicalWrites']=0
 # Feedback adjusts exploration priors only; diversity floor prevents convergence onto one source/lane.
 s['nextCyclePolicy']={'useFeedback':True,'preserveDiversityFloor':True,'allowSourceMonoculture':False,'canonicalDesignMutation':False}
 sp.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(sp)
if __name__=='__main__':main()
