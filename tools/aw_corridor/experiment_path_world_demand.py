#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import cv2, numpy as np
from experiment_depth_traversal import prepare, load_pose_points, smoothstep
from experiment_predictive_local_ldi import build_local_layers, render


def shift(mask, dx, dy):
    h,w=mask.shape
    m=np.float32([[1,0,dx],[0,1,dy]])
    return cv2.warpAffine(mask,m,(w,h),flags=cv2.INTER_NEAREST,borderMode=cv2.BORDER_CONSTANT,borderValue=0)


def demand_map(dep, poses, ppu=520.0, edge_q=.90):
    gx=cv2.Sobel(dep,cv2.CV_32F,1,0,ksize=3); gy=cv2.Sobel(dep,cv2.CV_32F,0,1,ksize=3)
    grad=cv2.magnitude(gx,gy); nz=grad[grad>0]
    thr=float(np.quantile(nz,edge_q)) if nz.size else 0.0
    strong=grad>=max(.025,thr)
    p0=np.asarray(poses[0]["position"],np.float32)
    out=np.zeros(dep.shape,np.uint8); max_shift=0.0; used=0
    for pose in poses[1:]:
        p=np.asarray(pose["position"],np.float32); d=p-p0
        vx=float(d[0]*ppu); vy=float(d[1]*ppu); planar=float(np.hypot(vx,vy))
        max_shift=max(max_shift,planar)
        if planar<.5: continue
        ux,uy=vx/planar,vy/planar
        deriv=gx*ux+gy*uy
        edge=(strong & (deriv>max(.008,thr*.18))).astype(np.uint8)*255
        if not np.any(edge): continue
        band=int(np.clip(np.ceil(planar*.24)+3,4,48))
        for s in np.linspace(0.0,float(band),max(3,band//3+1)):
            out=cv2.bitwise_or(out,shift(edge,int(round(ux*s)),int(round(uy*s))))
        used+=1
    out=cv2.dilate(out,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
    n,lab,stats,_=cv2.connectedComponentsWithStats((out>0).astype(np.uint8),8)
    cleaned=np.zeros_like(out); comps=[]; min_area=max(24,int(dep.size*.00004))
    for i in range(1,n):
        area=int(stats[i,cv2.CC_STAT_AREA])
        if area<min_area: continue
        cleaned[lab==i]=255
        comps.append({"area":area,"x":int(stats[i,0]),"y":int(stats[i,1]),"w":int(stats[i,2]),"h":int(stats[i,3])})
    return cleaned,comps,thr,max_shift,used


def main():
    ap=argparse.ArgumentParser()
    for n in ("source","depth","spine","output","report"): ap.add_argument("--"+n,type=Path,required=True)
    ap.add_argument("--demand-map",type=Path); ap.add_argument("--width",type=int,default=960)
    ap.add_argument("--fps",type=int,default=24); ap.add_argument("--segment-frames",type=int,default=24)
    ap.add_argument("--local-layers",type=int,default=3); ap.add_argument("--ppu",type=float,default=520.0)
    a=ap.parse_args(); src,dep=prepare(a.source,a.depth,a.width); poses=load_pose_points(a.spine)
    demand,comps,thr,max_shift,used=demand_map(dep,poses,a.ppu)
    base,locals_,base_mask=build_local_layers(src,dep,demand,max(1,a.local_layers))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    if a.demand_map:
        a.demand_map.parent.mkdir(parents=True,exist_ok=True); cv2.imwrite(str(a.demand_map),demand)
    h,w=src.shape[:2]; wr=cv2.VideoWriter(str(a.output),cv2.VideoWriter_fourcc(*"mp4v"),a.fps,(w,h))
    unseen=[]; coverage=[]; residual=[]; contrib=np.zeros(1+len(locals_),np.int64); worst={"fraction":-1.0,"frame":-1,"pose":None}; fn=0
    for i in range(len(poses)-1):
        p0=np.asarray(poses[i]["position"],np.float32); p1=np.asarray(poses[i+1]["position"],np.float32)
        for j in range(a.segment_frames):
            s=smoothstep(j/float(a.segment_frames)); p=p0*(1-s)+p1*s
            if float(np.linalg.norm(p))<1e-6: wr.write(src); fn+=1; continue
            frame,u,c,r,cc=render(src,dep,base,locals_,p,a.ppu); wr.write(frame)
            unseen.append(u); coverage.append(c); residual.append(r); contrib+=np.asarray(cc,np.int64)
            if r>worst["fraction"]: worst={"fraction":r,"frame":fn,"pose":[float(x) for x in p]}
            fn+=1
    wr.write(src); wr.release()
    max_u=max(unseen,default=0.0); max_r=max(residual,default=0.0)
    mean_ratio=float(np.mean([c/u if u>1e-9 else 1.0 for c,u in zip(coverage,unseen)])) if unseen else 1.0
    df=float(np.count_nonzero(demand)/demand.size)
    passed=max_u>.001 and mean_ratio>=.965 and max_r<=.0026 and 0.0<df<=.30
    report={"status":"PATH_WORLD_DEMAND_ACCEPTED" if passed else "PATH_WORLD_DEMAND_INSUFFICIENT","mode":"camera_path_conditioned_world_demand","canonical_pose_is_source_authority":True,"directional_pose_masks_used":used,"world_demand_fraction":df,"world_demand_component_count":len(comps),"world_demand_components":comps[:32],"max_predicted_camera_shift_pixels":max_shift,"depth_edge_threshold":thr,"max_foreground_unseen_fraction":max_u,"mean_hidden_layer_coverage_ratio":mean_ratio,"max_residual_uncovered_fraction":max_r,"worst_residual":worst,"layer_contributed_pixels_total":[int(x) for x in contrib],"exact_final_source_relock":True,"quantitative_gate":passed,"visual_gate":"PENDING_HUMAN_REVIEW","v8_reference_world_demand_fraction":0.6867047196671047,"v8_reference_max_residual_fraction":0.002354358300481822}
    a.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0 if passed else 2

if __name__=="__main__": raise SystemExit(main())
