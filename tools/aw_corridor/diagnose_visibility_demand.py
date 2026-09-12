#!/usr/bin/env python3
"""Diagnose *why* trajectory-visibility World Demand fails.

This is not another renderer. It separates four failure sources at sampled poses:
1) front-layer raster holes,
2) holes covered by the global hidden foundation,
3) holes covered by projected local-demand support,
4) residual holes still uncovered after all world evidence.

The goal is to tell whether the next problem is demand prediction, support projection,
geometry/rasterization, or hidden-world content rather than blindly tuning thresholds.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import cv2, numpy as np
from experiment_depth_traversal import prepare, load_pose_points, smoothstep
from experiment_visibility_demand import demand
from experiment_predictive_local_ldi import build_local_layers, raster_support
from experiment_world_cache import raster_layer


def pose_samples(poses, n):
    for i in range(len(poses)-1):
        a=np.asarray(poses[i]["position"],np.float32); b=np.asarray(poses[i+1]["position"],np.float32)
        for j in range(n):
            t=smoothstep(j/float(n)); yield i,j,a*(1-t)+b*t


def frac(mask):
    return float(np.count_nonzero(mask)/mask.size)


def main():
    ap=argparse.ArgumentParser()
    for k in ("source","depth","spine","report","outdir"):
        ap.add_argument("--"+k,type=Path,required=True)
    ap.add_argument("--width",type=int,default=960); ap.add_argument("--ppu",type=float,default=520.0)
    ap.add_argument("--samples",type=int,default=12); ap.add_argument("--local-layers",type=int,default=3)
    a=ap.parse_args(); a.outdir.mkdir(parents=True,exist_ok=True)
    src,dep=prepare(a.source,a.depth,a.width); poses=load_pose_points(a.spine)
    dm,_,_=demand(dep,poses,a.ppu,a.samples)
    base,locals_,_=build_local_layers(src,dep,dm,a.local_layers)
    base_rgb,base_depth=base
    rows=[]; worst=None
    for seg,j,p in pose_samples(poses,a.samples):
        if float(np.linalg.norm(p))<1e-6: continue
        _,front_known=raster_layer(src,dep,p,a.ppu,6,0.10)
        _,base_known=raster_layer(base_rgb,base_depth,p,a.ppu,6,None)
        local_union=np.zeros(dep.shape,bool)
        for rgb,d,support in locals_:
            _,known=raster_layer(rgb,d,p,a.ppu,6,None)
            local_union |= (known>0) & raster_support(support,d,p,a.ppu,6)
        hole=front_known==0
        base_cover=hole & (base_known>0)
        local_cover=hole & local_union
        residual=hole & ~(base_known>0) & ~local_union
        h,w=dep.shape; margin=max(4,int(min(h,w)*0.02)); interior=np.ones(dep.shape,bool)
        interior[:margin,:]=False; interior[-margin:,:]=False; interior[:,:margin]=False; interior[:,-margin:]=False
        interior_residual=residual & interior
        row={
          "segment":seg,"sample":j,"pose":[float(x) for x in p],
          "front_hole_fraction":frac(hole),
          "base_cover_fraction":frac(base_cover),
          "local_cover_fraction":frac(local_cover),
          "residual_fraction":frac(residual),
          "interior_residual_fraction":frac(interior_residual),
          "demand_fraction":frac(dm>0)
        }
        rows.append(row)
        if worst is None or row["interior_residual_fraction"]>worst[0]:
            worst=(row["interior_residual_fraction"],row,residual,interior_residual,local_union,hole)
    if worst:
        _,row,residual,interior_residual,local_union,hole=worst
        cv2.imwrite(str(a.outdir/"worst-front-hole.png"),hole.astype(np.uint8)*255)
        cv2.imwrite(str(a.outdir/"worst-local-support.png"),local_union.astype(np.uint8)*255)
        cv2.imwrite(str(a.outdir/"worst-residual.png"),residual.astype(np.uint8)*255)
        cv2.imwrite(str(a.outdir/"worst-interior-residual.png"),interior_residual.astype(np.uint8)*255)
        cv2.imwrite(str(a.outdir/"world-demand-map.png"),dm)
    summary={
      "mode":"visibility_failure_provenance",
      "sample_count":len(rows),
      "world_demand_fraction":frac(dm>0),
      "max_front_hole_fraction":max((r["front_hole_fraction"] for r in rows),default=0.0),
      "max_residual_fraction":max((r["residual_fraction"] for r in rows),default=0.0),
      "max_interior_residual_fraction":max((r["interior_residual_fraction"] for r in rows),default=0.0),
      "worst_interior": worst[1] if worst else None,
      "diagnostic_rule":"If interior residual is high, demand/support/geometry is wrong; if residual is low but video is bad, hidden-world content/geometry quality is the problem.",
      "frames":rows
    }
    a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps({k:v for k,v in summary.items() if k!="frames"},indent=2))
    return 0

if __name__=="__main__": raise SystemExit(main())
