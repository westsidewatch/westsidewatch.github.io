#!/usr/bin/env python3
"""DORÉ FILM Camera Spine Web/Blender parity gate."""
import json, math, sys
from pathlib import Path
TARGET=52.0

def distance(a,b): return math.sqrt(sum((b['p'][i]-a['p'][i])**2 for i in range(3)))
def build(nodes):
    dwell=sum(float(n.get('dwell',0)) for n in nodes)
    raw=[]
    for a,b in zip(nodes[:-1],nodes[1:]):
        speed=max(.001,(float(a.get('speed',.2))+float(b.get('speed',.2)))/2)
        raw.append(distance(a,b)/speed)
    budget=max(8.0,TARGET-dwell); total=sum(raw); travel=[v/total*budget for v in raw]
    cursor=0.; arrivals=[]; events=[]
    for i,n in enumerate(nodes):
        arrivals.append(cursor); d=float(n.get('dwell',0))
        if d: events.append(('DWELL',i,cursor,cursor+d)); cursor+=d
        if i<len(nodes)-1: events.append(('TRAVEL',i,cursor,cursor+travel[i])); cursor+=travel[i]
    return dwell,travel,arrivals,events,cursor

def main(path):
    data=json.loads(Path(path).read_text(encoding='utf-8')); nodes=data['nodes']; dwell,travel,arrivals,events,duration=build(nodes); fail=[]
    if len(nodes)!=20: fail.append(f'expected 20 nodes, got {len(nodes)}')
    if not data.get('rules',{}).get('oneCamera'): fail.append('oneCamera must be true')
    if data.get('rules',{}).get('conventionalCuts')!=0: fail.append('conventionalCuts must be 0')
    if abs(duration-TARGET)>.02: fail.append(f'duration {duration:.4f}s != {TARGET}s')
    for n in nodes:
        if len(n.get('p',[]))!=3 or len(n.get('look',[]))!=3: fail.append(f"{n.get('id')} invalid vector")
        if float(n.get('speed',0))<=0: fail.append(f"{n['id']} speed <= 0")
    print('DORÉ FILM CAMERA SPINE PARITY')
    print(f'nodes={len(nodes)} dwell={dwell:.2f}s travel={sum(travel):.2f}s total={duration:.2f}s')
    for i,n in enumerate(nodes):
        if n.get('timeBridge'): print(f"bridge {n['id']} {n['timeBridge']} arrival={arrivals[i]:.3f}s")
    print(f'events={len(events)}')
    if fail:
        print('FAIL'); [print(' -',x) for x in fail]; return 1
    print('PASS — Web + Blender shared authored timing contract is internally consistent'); return 0
if __name__=='__main__':
    default=Path(__file__).resolve().parents[1]/'camera-spine-experiment-01.json'; sys.exit(main(sys.argv[1] if len(sys.argv)>1 else default))
