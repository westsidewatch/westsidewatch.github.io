#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
import cv2,numpy as np
from experiment_depth_traversal import prepare,load_pose_points,smoothstep
from experiment_geometric_support import geometric_demand
from experiment_predictive_local_ldi import build_local_layers,raster_support
from experiment_world_cache import raster_layer


def frac(m): return float(np.count_nonzero(m)/m.size)

def samples(poses,n):
    for i in range(len(poses)-1):
        a=np.asarray(poses[i]['position'],np.float32); b=np.asarray(poses[i+1]['position'],np.float32)
        for j in range(n):
            t=smoothstep(j/float(n)); yield i,j,a*(1-t)+b*t

def main():
    ap=argparse.ArgumentParser()
    for k in ('source','depth','spine','report','outdir'): ap.add_argument('--'+k,type=Path,required=True)
    ap.add_argument('--width',type=int,default=960); ap.add_argument('--ppu',type=float,default=520.0); ap.add_argument('--samples',type=int,default=12); ap.add_argument('--local-layers',type=int,default=3)
    a=ap.parse_args(); a.outdir.mkdir(parents=True,exist_ok=True)
    src,dep=prepare(a.source,a.depth,a.width); poses=load_pose_points(a.spine)
    dm,used,mapped,inv_err,_,_=geometric_demand(dep,poses,a.ppu,a.samples)
    base,locals_,_=build_local_layers(src,dep,dm,a.local_layers); base_rgb,base_depth=base
    rows=[]; worst=None
    for seg,j,p in samples(poses,a.samples):
        if np.linalg.norm(p)<1e-6: continue
        _,fk=raster_layer(src,dep,p,a.ppu,6,.10); _,bk=raster_layer(base_rgb,base_depth,p,a.ppu,6,None)
        lu=np.zeros(dep.shape,bool)
        for rgb,d,support in locals_:
            _,k=raster_layer(rgb,d,p,a.ppu,6,None); lu|=(k>0)&raster_support(support,d,p,a.ppu,6)
        hole=fk==0; residual=hole&~(bk>0)&~lu
        h,w=dep.shape; margin=max(4,int(min(h,w)*.02)); interior=np.ones(dep.shape,bool); interior[:margin,:]=0; interior[-margin:,:]=0; interior[:,:margin]=0; interior[:,-margin:]=0
        ir=residual&interior
        row={'segment':seg,'sample':j,'pose':[float(x) for x in p],'front_hole_fraction':frac(hole),'base_cover_fraction':frac(hole&(bk>0)),'local_cover_fraction':frac(hole&lu),'residual_fraction':frac(residual),'interior_residual_fraction':frac(ir),'demand_fraction':frac(dm>0)}
        rows.append(row)
        if worst is None or row['interior_residual_fraction']>worst[0]: worst=(row['interior_residual_fraction'],row,hole,lu,residual,ir)
    if worst:
        _,row,hole,lu,residual,ir=worst
        cv2.imwrite(str(a.outdir/'worst-front-hole.png'),hole.astype(np.uint8)*255); cv2.imwrite(str(a.outdir/'worst-local-support.png'),lu.astype(np.uint8)*255); cv2.imwrite(str(a.outdir/'worst-residual.png'),residual.astype(np.uint8)*255); cv2.imwrite(str(a.outdir/'worst-interior-residual.png'),ir.astype(np.uint8)*255); cv2.imwrite(str(a.outdir/'world-demand-map.png'),dm)
    summary={'mode':'geometric_support_failure_provenance','trajectory_samples_used':used,'mapped_support_samples':mapped,'mean_inverse_projection_error_pixels':inv_err,'sample_count':len(rows),'world_demand_fraction':frac(dm>0),'max_front_hole_fraction':max((r['front_hole_fraction'] for r in rows),default=0.0),'max_residual_fraction':max((r['residual_fraction'] for r in rows),default=0.0),'max_interior_residual_fraction':max((r['interior_residual_fraction'] for r in rows),default=0.0),'worst_interior':worst[1] if worst else None,'diagnostic_rule':'If inverse projection error is low but interior residual remains high, support-depth estimation or hidden-layer geometry is wrong; if residual falls but video is bad, content/local rigidity is next.','frames':rows}
    a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(json.dumps(summary,indent=2)+'\n'); print(json.dumps({k:v for k,v in summary.items() if k!='frames'},indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
