#!/usr/bin/env python3
"""AW-011 V16: three-blade engraving repair experiment.

Blade 1: geometry closure (V13/V14).
Blade 2: engraving PDE continuation (V14/V15).
Blade 3: source-only structure transfer. If blade 2 still fails the strict
engraving gate, copy the best nearby source patch into the wound. Candidate
patches are scored by the intact halo, gradient orientation and tone. This is
intentionally conservative: no generative pixels and no modification outside
wound pixels.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import cv2
import numpy as np
import experiment_static_cinema_v15 as v15
import experiment_static_cinema_v14 as base


def _best_source_patch(img: np.ndarray, wound: np.ndarray, search_radius: int = 28):
    ys,xs=np.where(wound)
    if len(xs)==0: return img.copy(), {'pixels':0,'score':0.0,'offset':[0,0]}
    y0,y1=max(0,int(ys.min())-6),min(img.shape[0],int(ys.max())+7)
    x0,x1=max(0,int(xs.min())-6),min(img.shape[1],int(xs.max())+7)
    roi=img[y0:y1,x0:x1]
    wm=wound[y0:y1,x0:x1]
    ring=(cv2.dilate(wm.astype(np.uint8),np.ones((7,7),np.uint8))>0)&(~wm)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx=cv2.Sobel(gray,cv2.CV_32F,1,0,ksize=3); gy=cv2.Sobel(gray,cv2.CV_32F,0,1,ksize=3)
    best=None
    for dy in range(-search_radius,search_radius+1):
      for dx in range(-search_radius,search_radius+1):
        if dx==0 and dy==0: continue
        sy0,sy1=y0+dy,y1+dy; sx0,sx1=x0+dx,x1+dx
        if sy0<0 or sx0<0 or sy1>img.shape[0] or sx1>img.shape[1]: continue
        donor_w=wound[sy0:sy1,sx0:sx1]
        if np.any(donor_w): continue
        cand=img[sy0:sy1,sx0:sx1]
        if not np.any(ring): continue
        tone=float(np.mean(np.abs(roi.astype(np.float32)[ring]-cand.astype(np.float32)[ring])))
        cgx=gx[sy0:sy1,sx0:sx1]; cgy=gy[sy0:sy1,sx0:sx1]
        rgx=gx[y0:y1,x0:x1]; rgy=gy[y0:y1,x0:x1]
        dot=rgx*cgx+rgy*cgy
        den=np.sqrt(rgx*rgx+rgy*rgy)*np.sqrt(cgx*cgx+cgy*cgy)+1e-4
        orient=float(np.mean(np.abs(dot[ring]/den[ring])))
        distance=(dx*dx+dy*dy)**0.5
        score=tone + 18.0*(1.0-orient) + 0.12*distance
        if best is None or score<best[0]: best=(score,dx,dy,cand.copy(),orient,tone)
    if best is None: return img.copy(), {'pixels':0,'score':999.0,'offset':[0,0]}
    score,dx,dy,cand,orient,tone=best
    out=img.copy(); block=out[y0:y1,x0:x1]; block[wm]=cand[wm]; out[y0:y1,x0:x1]=block
    return out, {'pixels':int(np.count_nonzero(wm)),'score':float(score),'offset':[int(dx),int(dy)],'orientation':float(orient),'tone_mae':float(tone)}


def third_blade(prewarp: np.ndarray, wound: np.ndarray):
    candidate,meta=_best_source_patch(prewarp,wound)
    before=v15.strict_engraving_metrics(prewarp,wound)
    after=v15.strict_engraving_metrics(candidate,wound)
    b=before['edge_density_ratio']+before['variance_ratio']+before['orientation_similarity']+before['line_crossing_score']
    a=after['edge_density_ratio']+after['variance_ratio']+after['orientation_similarity']+after['line_crossing_score']
    accepted=bool(after['fidelity_pass'] or a>b+0.10)
    meta.update({'fidelity_before':before,'fidelity_after':after,'accepted':accepted})
    return (candidate if accepted else prewarp.copy()),meta


def _report_path(argv):
    for i,a in enumerate(argv):
        if a=='--report' and i+1<len(argv): return Path(argv[i+1])
        if a.startswith('--report='): return Path(a.split('=',1)[1])
    return None


def main():
    base.engraving_metrics=v15.strict_engraving_metrics
    original=base.engraving_structure_repair
    events=[]
    # V14's callback contract is (prewarp, warp, wound). Preserve it exactly.
    def composite(prewarp, warp, wound):
        blade2=original(prewarp,warp,wound)
        b2_img=blade2[0] if isinstance(blade2,tuple) else blade2
        b2_meta=blade2[1] if isinstance(blade2,tuple) else {}
        gate=v15.strict_engraving_metrics(b2_img,wound)
        if gate['fidelity_pass']:
            events.append({'blade2':b2_meta,'blade2_gate':gate,'blade3':None})
            return b2_img
        b3_img,b3_meta=third_blade(b2_img,wound)
        events.append({'blade2':b2_meta,'blade2_gate':gate,'blade3':b3_meta})
        return b3_img
    base.engraving_structure_repair=composite
    report=_report_path(sys.argv[1:])
    rc=base.main()
    if report and report.exists():
        data=json.loads(report.read_text(encoding='utf-8'))
        data['status']='STATIC_CINEMA_V16_THREE_BLADE_READY_FOR_VISUAL_REVIEW'
        data['mode']='geometry_blade_then_engraving_blade_then_source_structure_transfer'
        data['blade_3']='repair.structure-transfer'
        data['blade_3_policy']='source-only exemplar transfer; intact-halo + gradient-orientation + tone scoring; wound-only commit; fidelity rollback; no generative fallback'
        data['blade_3_events']=events
        data['blade_3_event_count']=sum(1 for e in events if e.get('blade3') is not None)
        data['blade_3_accepted_count']=sum(1 for e in events if e.get('blade3') and e['blade3'].get('accepted'))
        report.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(data,indent=2))
    return rc

if __name__=='__main__': raise SystemExit(main())
