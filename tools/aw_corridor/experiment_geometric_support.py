#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
import cv2,numpy as np
from experiment_depth_traversal import prepare,load_pose_points,smoothstep
from experiment_predictive_local_ldi import build_local_layers,render
from experiment_world_cache import raster_layer


def sample_path(poses,n=8):
    out=[]
    for i in range(len(poses)-1):
        a=np.asarray(poses[i]['position'],np.float32); b=np.asarray(poses[i+1]['position'],np.float32)
        for j in range(n):
            t=smoothstep(j/float(n)); p=a*(1-t)+b*t
            if np.linalg.norm(p)>=1e-6: out.append(p)
    return out


def clean_holes(hole,shift):
    h,w=hole.shape
    m=max(3,min(18,int(np.ceil(shift*.08))))
    hole=hole.copy()
    hole[:m,:]=0; hole[-m:,:]=0; hole[:,:m]=0; hole[:,-m:]=0
    hole=cv2.morphologyEx(hole,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    return cv2.dilate(hole,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))


def inverse_project_mask(dep,pose,known,warped_depth,ppu):
    h,w=dep.shape; cx=np.float32((w-1)*.5); cy=np.float32((h-1)*.5)
    p=np.asarray(pose,np.float32); shift=float(np.hypot(p[0]*ppu,p[1]*ppu))
    hole=clean_holes((known==0).astype(np.uint8)*255,shift)
    if not np.any(hole): return np.zeros_like(hole),0,0.0

    # Infer the hidden support depth in the current view from adjacent visible
    # front geometry, then analytically invert the exact AW-011 camera model.
    zview=warped_depth.astype(np.float32)/255.0
    missing=(known==0).astype(np.uint8)*255
    zfill=cv2.inpaint(zview,missing,7.0,cv2.INPAINT_TELEA)
    yy,xx=np.nonzero(hole>0); z=zfill[yy,xx]
    gain=np.float32(1.0+max(-.35,min(.35,-float(p[2])*.9)))
    sx=np.float32(p[0]*ppu)*(.35+1.30*z)
    sy=np.float32(p[1]*ppu)*(.45+.90*z)
    ux=cx+(xx.astype(np.float32)-cx-sx)/gain
    uy=cy+(yy.astype(np.float32)-cy-sy)/gain
    ui=np.rint(ux).astype(np.int32); vi=np.rint(uy).astype(np.int32)
    valid=(ui>=0)&(ui<w)&(vi>=0)&(vi<h)
    out=np.zeros((h,w),np.uint8); out[vi[valid],ui[valid]]=255

    # Measure inversion consistency by forward-projecting the inferred support.
    zz=z[valid]; x0=ui[valid].astype(np.float32); y0=vi[valid].astype(np.float32)
    fx=cx+(x0-cx)*gain+np.float32(p[0]*ppu)*(.35+1.30*zz)
    fy=cy+(y0-cy)*gain+np.float32(p[1]*ppu)*(.45+.90*zz)
    err=float(np.mean(np.hypot(fx-xx[valid],fy-yy[valid]))) if np.any(valid) else 0.0
    return out,int(np.count_nonzero(valid)),err


def geometric_demand(dep,poses,ppu=520.0,n=8):
    probe=np.dstack([np.uint8(np.clip(dep,0,1)*255)]*3)
    demand=np.zeros(dep.shape,np.uint8); used=0; mapped=0; errs=[]; maxs=0.0
    for p in sample_path(poses,n):
        maxs=max(maxs,float(np.hypot(p[0]*ppu,p[1]*ppu)))
        warped,known=raster_layer(probe,dep,p,ppu,6,.10)
        local,count,err=inverse_project_mask(dep,p,known,warped[:,:,0],ppu)
        if count==0: continue
        demand=cv2.bitwise_or(demand,local); mapped+=count; errs.append(err); used+=1
    demand=cv2.dilate(demand,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
    nlab,labels,stats,_=cv2.connectedComponentsWithStats((demand>0).astype(np.uint8),8)
    cleaned=np.zeros_like(demand); min_area=max(24,int(dep.size*.00005)); comps=[]
    for i in range(1,nlab):
        area=int(stats[i,cv2.CC_STAT_AREA])
        if area<min_area: continue
        cleaned[labels==i]=255
        comps.append({'area':area,'x':int(stats[i,cv2.CC_STAT_LEFT]),'y':int(stats[i,cv2.CC_STAT_TOP]),'w':int(stats[i,cv2.CC_STAT_WIDTH]),'h':int(stats[i,cv2.CC_STAT_HEIGHT])})
    return cleaned,used,mapped,(float(np.mean(errs)) if errs else 0.0),maxs,comps


def main():
    ap=argparse.ArgumentParser()
    for k in ('source','depth','spine','output','report'): ap.add_argument('--'+k,type=Path,required=True)
    ap.add_argument('--demand-map',type=Path); ap.add_argument('--width',type=int,default=960); ap.add_argument('--fps',type=int,default=24); ap.add_argument('--segment-frames',type=int,default=24); ap.add_argument('--local-layers',type=int,default=3); ap.add_argument('--ppu',type=float,default=520.0); ap.add_argument('--samples',type=int,default=8)
    a=ap.parse_args(); src,dep=prepare(a.source,a.depth,a.width); poses=load_pose_points(a.spine)
    dm,used,mapped,inv_err,maxs,components=geometric_demand(dep,poses,a.ppu,a.samples)
    base,loc,_=build_local_layers(src,dep,dm,a.local_layers)
    if a.demand_map: cv2.imwrite(str(a.demand_map),dm)
    h,w=src.shape[:2]; a.output.parent.mkdir(parents=True,exist_ok=True)
    wr=cv2.VideoWriter(str(a.output),cv2.VideoWriter_fourcc(*'mp4v'),a.fps,(w,h))
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
    ok=maxu>.001 and cov>=.965 and maxr<=.0026 and 0<df<=.12
    rep={'status':'GEOMETRIC_WORLD_SUPPORT_ACCEPTED' if ok else 'GEOMETRIC_WORLD_SUPPORT_INSUFFICIENT','mode':'camera_conditioned_geometric_world_support','trajectory_samples_used':used,'mapped_support_samples':mapped,'mean_inverse_projection_error_pixels':inv_err,'world_demand_fraction':df,'world_demand_component_count':len(components),'world_demand_components':components[:32],'max_camera_shift_pixels':maxs,'max_foreground_unseen_fraction':maxu,'mean_hidden_layer_coverage_ratio':cov,'max_residual_uncovered_fraction':maxr,'worst_residual':worst,'exact_final_source_relock':True,'quantitative_gate':ok,'visual_gate':'PENDING_HUMAN_REVIEW','previous_visibility_demand_fraction':0.030357533946561543,'previous_visibility_residual_fraction':0.01551823258869908}
    a.report.write_text(json.dumps(rep,indent=2)+'\n'); print(json.dumps(rep,indent=2)); return 0 if ok else 2
if __name__=='__main__': raise SystemExit(main())
