#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
import cv2,numpy as np
from experiment_depth_traversal import prepare,load_pose_points,smoothstep
from experiment_predictive_local_ldi import build_local_layers,render
from experiment_world_cache import raster_layer

def sh(mask,dx,dy):
    h,w=mask.shape
    M=np.float32([[1,0,dx],[0,1,dy]])
    return cv2.warpAffine(mask,M,(w,h),flags=cv2.INTER_NEAREST,borderValue=0)

def samples(poses,n=8):
    out=[]
    for i in range(len(poses)-1):
        a=np.asarray(poses[i]['position'],np.float32); b=np.asarray(poses[i+1]['position'],np.float32)
        for j in range(n):
            t=smoothstep(j/float(n)); p=a*(1-t)+b*t
            if np.linalg.norm(p)>=1e-6: out.append(p)
    return out

def demand(dep,poses,ppu=520.0,n=8):
    probe=np.dstack([np.uint8(np.clip(dep,0,1)*255)]*3)
    out=np.zeros(dep.shape,np.uint8); p0=np.asarray(poses[0]['position'],np.float32); used=0; maxs=0.0
    for p in samples(poses,n):
        d=p-p0; vx=float(d[0]*ppu); vy=float(d[1]*ppu); maxs=max(maxs,float(np.hypot(vx,vy)))
        _,known=raster_layer(probe,dep,p,ppu,6,0.10)
        hole=(known==0).astype(np.uint8)*255
        m=max(3,min(18,int(np.ceil(maxs*.08))))
        hole[:m,:]=0; hole[-m:,:]=0; hole[:,:m]=0; hole[:,-m:]=0
        hole=cv2.morphologyEx(hole,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
        if not np.any(hole): continue
        hole=cv2.dilate(hole,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
        out=cv2.bitwise_or(out,sh(hole,int(round(-vx)),int(round(-vy))))
        used+=1
    out=cv2.dilate(out,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
    return out,used,maxs

def main():
    ap=argparse.ArgumentParser()
    for k in ('source','depth','spine','output','report'): ap.add_argument('--'+k,type=Path,required=True)
    ap.add_argument('--demand-map',type=Path); ap.add_argument('--width',type=int,default=960); ap.add_argument('--fps',type=int,default=24); ap.add_argument('--segment-frames',type=int,default=24); ap.add_argument('--local-layers',type=int,default=3); ap.add_argument('--ppu',type=float,default=520.0); ap.add_argument('--samples',type=int,default=8)
    a=ap.parse_args(); src,dep=prepare(a.source,a.depth,a.width); poses=load_pose_points(a.spine)
    dm,used,maxs=demand(dep,poses,a.ppu,a.samples); base,loc,_=build_local_layers(src,dep,dm,a.local_layers)
    if a.demand_map: cv2.imwrite(str(a.demand_map),dm)
    h,w=src.shape[:2]; wr=cv2.VideoWriter(str(a.output),cv2.VideoWriter_fourcc(*'mp4v'),a.fps,(w,h))
    U=[];C=[];R=[]; worst={'fraction':-1.0,'frame':-1,'pose':None}; fn=0
    for i in range(len(poses)-1):
        p0=np.asarray(poses[i]['position'],np.float32); p1=np.asarray(poses[i+1]['position'],np.float32)
        for j in range(a.segment_frames):
            t=smoothstep(j/float(a.segment_frames)); p=p0*(1-t)+p1*t
            if np.linalg.norm(p)<1e-6: wr.write(src); fn+=1; continue
            frame,u,c,r,_=render(src,dep,base,loc,p,a.ppu); wr.write(frame); U.append(u); C.append(c); R.append(r)
            if r>worst['fraction']: worst={'fraction':r,'frame':fn,'pose':[float(x) for x in p]}
            fn+=1
    wr.write(src); wr.release()
    maxu=max(U,default=0); maxr=max(R,default=0); cov=float(np.mean([c/u if u>1e-9 else 1.0 for c,u in zip(C,U)])) if U else 1.0; df=float(np.count_nonzero(dm)/dm.size)
    ok=maxu>.001 and cov>=.965 and maxr<=.0026 and 0<df<=.30
    rep={'status':'TRAJECTORY_VISIBILITY_DEMAND_ACCEPTED' if ok else 'TRAJECTORY_VISIBILITY_DEMAND_INSUFFICIENT','mode':'camera_trajectory_visibility_world_demand','trajectory_samples_used':used,'world_demand_fraction':df,'max_camera_shift_pixels':maxs,'max_foreground_unseen_fraction':maxu,'mean_hidden_layer_coverage_ratio':cov,'max_residual_uncovered_fraction':maxr,'worst_residual':worst,'exact_final_source_relock':True,'quantitative_gate':ok,'visual_gate':'PENDING_HUMAN_REVIEW','previous_path_demand_fraction':0.3007610600087604}
    a.report.write_text(json.dumps(rep,indent=2)+'\n'); print(json.dumps(rep,indent=2)); return 0 if ok else 2
if __name__=='__main__': raise SystemExit(main())
