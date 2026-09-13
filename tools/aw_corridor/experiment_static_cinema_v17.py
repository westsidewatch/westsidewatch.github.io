#!/usr/bin/env python3
"""V17: strict source-only third blade experiment."""
from __future__ import annotations
import json, sys
from pathlib import Path
import cv2
import numpy as np
import experiment_static_cinema_v15 as v15
import experiment_static_cinema_v14 as base


def best_patch(img, wound, radius=36):
    ys,xs=np.where(wound)
    if len(xs)==0: return img.copy(), {'pixels':0,'offset':[0,0]}
    p=8; y0,y1=max(0,int(ys.min())-p),min(img.shape[0],int(ys.max())+p+1); x0,x1=max(0,int(xs.min())-p),min(img.shape[1],int(xs.max())+p+1)
    wm=wound[y0:y1,x0:x1]
    boundary=(cv2.dilate(wm.astype(np.uint8),np.ones((7,7),np.uint8))>0)&(~cv2.dilate(wm.astype(np.uint8),np.ones((3,3),np.uint8)).astype(bool))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx=cv2.Sobel(gray,cv2.CV_32F,1,0,ksize=3); gy=cv2.Sobel(gray,cv2.CV_32F,0,1,ksize=3); mag=np.sqrt(gx*gx+gy*gy); ang=np.arctan2(gy,gx)
    roi=img[y0:y1,x0:x1]; rm=mag[y0:y1,x0:x1]; ra=ang[y0:y1,x0:x1]; best=None
    for dy in range(-radius,radius+1):
      for dx in range(-radius,radius+1):
        if dx==0 and dy==0: continue
        a,b=y0+dy,y1+dy; c,d=x0+dx,x1+dx
        if a<0 or c<0 or b>img.shape[0] or d>img.shape[1] or np.any(wound[a:b,c:d]): continue
        cand=img[a:b,c:d]; cm=mag[a:b,c:d]; ca=ang[a:b,c:d]
        tone=float(np.mean(np.abs(roi.astype(np.float32)[boundary]-cand.astype(np.float32)[boundary])))
        orient=float(np.mean(np.abs(np.cos(ra[boundary]-ca[boundary]))))
        strength=float(np.mean(np.abs(rm[boundary]-cm[boundary])))/(float(np.mean(rm[boundary]))+1e-4)
        score=tone+28*(1-orient)+20*strength+.08*np.hypot(dx,dy)
        if best is None or score<best[0]: best=(score,dx,dy,cand.copy(),orient,tone,strength)
    if best is None: return img.copy(), {'pixels':0,'offset':[0,0]}
    score,dx,dy,cand,orient,tone,strength=best; out=img.copy(); block=out[y0:y1,x0:x1]; block[wm]=cand[wm]; out[y0:y1,x0:x1]=block
    return out, {'pixels':int(np.count_nonzero(wm)),'score':float(score),'offset':[int(dx),int(dy)],'boundary_orientation':orient,'tone_mae':tone,'gradient_strength_error':strength}


def third_blade(img,wound):
    candidate,meta=best_patch(img,wound); after=v15.strict_engraving_metrics(candidate,wound); accepted=bool(after['fidelity_pass']); meta.update({'fidelity_after':after,'accepted':accepted,'admission':'strict_fidelity_gate_only'}); return (candidate if accepted else img.copy()),meta


def report_path(argv):
    for i,a in enumerate(argv):
        if a=='--report' and i+1<len(argv): return Path(argv[i+1])
    return None


def main():
    base.engraving_metrics=v15.strict_engraving_metrics; blade2=base.engraving_structure_repair; events=[]
    def composite(prewarp,warp,wound):
        b2=blade2(prewarp,warp,wound); gate=v15.strict_engraving_metrics(b2,wound)
        if gate['fidelity_pass']: events.append({'blade2_gate':gate,'blade3':None}); return b2
        b3,m3=third_blade(b2,wound); events.append({'blade2_gate':gate,'blade3':m3}); return b3
    base.engraving_structure_repair=composite; rp=report_path(sys.argv[1:]); rc=base.main()
    if rp and rp.exists():
        d=json.loads(rp.read_text()); d['status']='STATIC_CINEMA_V17_STRICT_THREE_BLADE_READY_FOR_VISUAL_REVIEW'; d['blade_3']='repair.structure-transfer.topology-aware'; d['blade_3_events']=events; d['blade_3_event_count']=sum(e['blade3'] is not None for e in events); d['blade_3_accepted_count']=sum(bool(e['blade3'] and e['blade3']['accepted']) for e in events); rp.write_text(json.dumps(d,indent=2)+'\n')
    return rc

if __name__=='__main__': raise SystemExit(main())
