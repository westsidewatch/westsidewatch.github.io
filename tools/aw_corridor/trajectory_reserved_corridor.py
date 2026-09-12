#!/usr/bin/env python3
"""Trajectory-reserved 3D corridor + capability envelope probe.

Diagnostic only. It does not change renderer pixels. Golden Camera Spine first
reserves a continuous family of 16:9 source-space viewfinders. Depth then
estimates where ideal same-ratio crop motion needs true 3D support, and the
probe records the minimum capability set suggested for each camera segment.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import cv2
import numpy as np

CAPABILITIES = {
    "projection.source-reprojection": {"cost": 1, "generation": 0},
    "geometry.moge": {"cost": 1, "generation": 0},
    "geometry.depth-crosscheck": {"cost": 1, "generation": 0},
    "hidden.ldi": {"cost": 2, "generation": 0},
    "hidden.layered-gaussian": {"cost": 3, "generation": 0},
    "repair.warp": {"cost": 2, "generation": 0},
    "repair.inpaint": {"cost": 4, "generation": 1},
    "nvs.generative-fallback": {"cost": 8, "generation": 5},
}

def readj(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def dumpj(p,o):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2)+"\n",encoding="utf-8")
def dumpjl(p,rows):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r)+"\n")
def sstep(t): return t*t*(3-2*t)
def clamp_rect(cx,cy,cw,ch,w,h):
    cw=max(2,min(int(round(cw)),w)); ch=max(2,min(int(round(ch)),h))
    x=max(0,min(int(round(cx-cw/2)),w-cw)); y=max(0,min(int(round(cy-ch/2)),h-ch))
    return [x,y,cw,ch]

def choose_caps(lateral,z,depth_span,deviation,residual):
    caps=["projection.source-reprojection","geometry.moge"]
    if depth_span > .20 or z > .06: caps.append("geometry.depth-crosscheck")
    if deviation > 4.0 or residual > .00025: caps.append("hidden.ldi")
    if deviation > 10.0 or residual > .0007: caps.append("repair.warp")
    # These remain trial/fallback only; never authoritative in this probe.
    trials=[]
    if deviation > 14.0: trials.append("hidden.layered-gaussian")
    if residual > .0015: trials.append("repair.inpaint")
    if residual > .005: trials.append("nvs.generative-fallback")
    return caps,trials

def main():
    ap=argparse.ArgumentParser()
    for k in ("source","depth","spine","render-report","state","report","mask","preview","capability-trials"):
        ap.add_argument("--"+k,type=Path,required=True)
    ap.add_argument("--segment-frames",type=int,default=12)
    ap.add_argument("--ppu",type=float,default=520.0)
    a=ap.parse_args()

    src=cv2.imread(str(a.source)); dep=cv2.imread(str(a.depth),cv2.IMREAD_GRAYSCALE)
    if src is None or dep is None: raise RuntimeError("source/depth missing")
    h,w=dep.shape
    if src.shape[:2]!=(h,w): src=cv2.resize(src,(w,h),interpolation=cv2.INTER_AREA)
    spine=readj(a.spine); rr=readj(a.render_report); poses=spine.get("poses",[])
    if len(poses)<2: raise RuntimeError("camera spine needs >=2 poses")
    bx,by,bcw,bch=[float(v) for v in rr["selected_viewfinder_rect"]]
    base_cx,base_cy=bx+bcw/2,by+bch/2; base_fov=float(poses[0].get("fov_degrees",50))
    residual=float(rr.get("max_final_viewfinder_residual_fraction",0.0))
    depthf=dep.astype(np.float32)/255.0
    union=np.zeros((h,w),np.uint8); armed=np.zeros((h,w),np.uint8)
    rows=[]; trials=[]; frame=0
    for si in range(len(poses)-1):
        p0,p1=poses[si],poses[si+1]
        v0=np.asarray(p0.get("position",[0,0,0]),np.float32); v1=np.asarray(p1.get("position",[0,0,0]),np.float32)
        f0=float(p0.get("fov_degrees",base_fov)); f1=float(p1.get("fov_degrees",base_fov))
        for j in range(a.segment_frames):
            t=sstep(j/float(a.segment_frames)); pos=v0*(1-t)+v1*t; fov=f0*(1-t)+f1*t
            scale=math.tan(math.radians(fov)/2)/max(1e-6,math.tan(math.radians(base_fov)/2))
            rect=clamp_rect(base_cx+float(pos[0])*a.ppu,base_cy+float(pos[1])*a.ppu,bcw*scale,bch*scale,w,h)
            x,y,rw,rh=rect; union[y:y+rh,x:x+rw]=255
            local=depthf[y:y+rh,x:x+rw]
            q10=float(np.quantile(local,.10)); q90=float(np.quantile(local,.90)); span=q90-q10
            lateral=float(math.hypot(float(pos[0]),float(pos[1]))); z=abs(float(pos[2]))
            deviation=float(a.ppu*z*span)
            halo=int(math.ceil(max(4.0,deviation*1.25)))
            ax=max(0,x-halo); ay=max(0,y-halo); ax2=min(w,x+rw+halo); ay2=min(h,y+rh+halo)
            armed[ay:ay2,ax:ax2]=255
            caps,trial=choose_caps(lateral,z,span,deviation,residual)
            cost=sum(CAPABILITIES[c]["cost"] for c in caps)
            rows.append({"frame":frame,"segment":si,"pose_xyz":[float(q) for q in pos],"fov":fov,"viewfinder_rect":rect,"scale":scale,"depth_span_q10_q90":span,"estimated_3d_deviation_px":deviation,"capability_halo_px":halo,"active_capabilities":caps,"trial_capabilities":trial,"estimated_cost_units":cost})
            for c in trial: trials.append({"frame":frame,"segment":si,"capability":c,"reason":"camera-state threshold crossed","authoritative":False})
            frame+=1
    cv2.imwrite(str(a.mask),armed)
    preview=src.copy(); preview[armed==0]=(preview[armed==0]*0.25).astype(np.uint8)
    cv2.imwrite(str(a.preview),preview)
    dumpjl(a.state,rows); dumpjl(a.capability_trials,trials)
    report={
      "status":"TRAJECTORY_RESERVED_ARMED_3D_CORRIDOR_READY_FOR_REVIEW",
      "authoritative_renderer_change":False,
      "camera_frames":len(rows),
      "source_fraction_reserved_2d":float(np.count_nonzero(union)/union.size),
      "source_fraction_armed_3d":float(np.count_nonzero(armed)/armed.size),
      "max_estimated_3d_deviation_px":max((r["estimated_3d_deviation_px"] for r in rows),default=0.0),
      "max_capability_halo_px":max((r["capability_halo_px"] for r in rows),default=0),
      "capability_trial_events":len(trials),
      "render_residual_observed":residual,
      "principle":"trajectory reserves existing source world first; 3D and extra capabilities activate only where camera-state deviation requires them"
    }
    dumpj(a.report,report); print(json.dumps(report,indent=2))
if __name__=="__main__": main()
