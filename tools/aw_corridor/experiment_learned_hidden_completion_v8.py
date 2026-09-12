#!/usr/bin/env python3
"""AW-011 V8: learned edge-conditioned canonical hidden RGB+depth completion.

V7 solved canvas-boundary representation. V8 changes one variable only: the
internal hidden surface content provider. Geometry, topology, extended world,
camera trajectory, rasterizer and source relock remain V7-compatible.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from experiment_depth_traversal import prepare, load_pose_points, smoothstep
from experiment_depth_banded_world_cache import collect_depth_conditioned_support
from experiment_edge_aware_hidden_surface_v4 import camera_lateral_budget, nearest_edge_topology, boundary_discontinuity
from experiment_joint_hidden_completion_v7 import build_extended_boundary_world, render
from hidden_surface_provider import classical_complete, learned_three_stage_complete


def main():
    ap=argparse.ArgumentParser()
    for k in ('source','depth','spine','output','report'): ap.add_argument('--'+k,type=Path,required=True)
    ap.add_argument('--support-map',type=Path); ap.add_argument('--edge-map',type=Path); ap.add_argument('--hidden-depth-map',type=Path)
    ap.add_argument('--provider',choices=('classical','three-stage'),default='classical')
    ap.add_argument('--networks',type=Path); ap.add_argument('--edge-checkpoint',type=Path); ap.add_argument('--depth-checkpoint',type=Path); ap.add_argument('--color-checkpoint',type=Path)
    ap.add_argument('--device',default='cpu')
    ap.add_argument('--width',type=int,default=480); ap.add_argument('--fps',type=int,default=12); ap.add_argument('--segment-frames',type=int,default=4)
    ap.add_argument('--ppu',type=float,default=520.0); ap.add_argument('--samples',type=int,default=4); ap.add_argument('--behind',type=float,default=.08)
    ap.add_argument('--edge-q',type=float,default=.90); ap.add_argument('--min-jump',type=float,default=.055)
    a=ap.parse_args()

    src,dep=prepare(a.source,a.depth,a.width); poses=load_pose_points(a.spine)
    shift,radius=camera_lateral_budget(poses,a.ppu)
    support,zmap,used,mapped,inv_err=collect_depth_conditioned_support(dep,poses,a.ppu,a.samples,a.behind)
    topo=nearest_edge_topology(dep,support,a.edge_q,.025,a.min_jump,radius)

    if a.provider == 'three-stage':
        required=(a.networks,a.edge_checkpoint,a.depth_checkpoint,a.color_checkpoint)
        if any(p is None or not p.exists() for p in required):
            raise FileNotFoundError('three-stage provider requires networks.py plus edge/depth/color checkpoints')
        hs=learned_three_stage_complete(src,dep,support,zmap,topo,a.networks,a.edge_checkpoint,a.depth_checkpoint,a.color_checkpoint,a.device)
    else:
        hs=classical_complete(src,dep,support,zmap,topo)
    irgb,idep,imask=hs.rgb,hs.depth,hs.mask

    # Keep V7 extended-world reflection unchanged so visual delta isolates the
    # learned internal completion. Border synthesis becomes a separate V9 gate.
    pad=max(24,int(np.ceil(shift+16.0)))
    ergb,edep,emask=build_extended_boundary_world(src,dep,pad)

    for path,img in ((a.support_map,support),(a.edge_map,hs.edge)):
        if path: path.parent.mkdir(parents=True,exist_ok=True); cv2.imwrite(str(path),img)
    if a.hidden_depth_map:
        a.hidden_depth_map.parent.mkdir(parents=True,exist_ok=True); cv2.imwrite(str(a.hidden_depth_map),np.uint8(np.clip(idep,0,1)*255))

    h,w=dep.shape; a.output.parent.mkdir(parents=True,exist_ok=True)
    writer=cv2.VideoWriter(str(a.output),cv2.VideoWriter_fourcc(*'mp4v'),a.fps,(w,h))
    if not writer.isOpened(): raise RuntimeError('video writer failed')
    unseen=[]; coverage=[]; residual=[]; bmean=[]; b95=[]; icount=ecount=0
    worst={'fraction':-1.0,'frame':-1,'pose':None}; fn=0
    for i in range(len(poses)-1):
        p0=np.asarray(poses[i]['position'],np.float32); p1=np.asarray(poses[i+1]['position'],np.float32)
        for j in range(a.segment_frames):
            t=smoothstep(j/float(a.segment_frames)); p=p0*(1-t)+p1*t
            if np.linalg.norm(p)<1e-6: writer.write(src); fn+=1; continue
            frame,u,c,r,fk,occ,ic,ec=render(src,dep,irgb,idep,imask,ergb,edep,emask,pad,p,a.ppu)
            bm,bp=boundary_discontinuity(frame,fk,occ)
            writer.write(frame); unseen.append(u); coverage.append(c); residual.append(r); bmean.append(bm); b95.append(bp); icount+=ic; ecount+=ec
            if r>worst['fraction']: worst={'fraction':r,'frame':fn,'pose':[float(x) for x in p]}
            fn+=1
    writer.write(src); writer.release()

    maxu=max(unseen,default=0.0); maxr=max(residual,default=0.0)
    cov=float(np.mean([c/u if u>1e-9 else 1.0 for c,u in zip(coverage,unseen)])) if unseen else 1.0
    rep={
      'status':'LEARNED_INTERNAL_HIDDEN_SURFACE_READY_FOR_VISUAL_REVIEW',
      'mode':'v7_geometry_topology_extended_world_plus_learned_internal_content',
      'hidden_surface_provider':hs.provider,
      'trajectory_samples_used':used,'mapped_support_samples':mapped,'mean_inverse_projection_error_pixels':inv_err,
      'support_fraction':float(np.count_nonzero(support)/support.size),'max_camera_lateral_shift_pixels':shift,
      'camera_conditioned_zone_radius_pixels':radius,'extended_canvas_pad_pixels':pad,
      'max_foreground_unseen_fraction':maxu,'mean_hidden_layer_coverage_ratio':cov,'max_residual_uncovered_fraction':maxr,
      'mean_hidden_boundary_discontinuity':float(np.mean(bmean)) if bmean else 0.0,'max_hidden_boundary_discontinuity_q95':max(b95,default=0.0),
      'internal_rendered_pixels_total':icount,'extended_boundary_rendered_pixels_total':ecount,'worst_residual':worst,
      'per_frame_synthesis':False,'canonical_world_completion_once':True,'visible_source_pixels_model_modified':False,'exact_final_source_relock':True,
      'coverage_gate':bool(maxu>.001 and cov>=.96 and maxr<=.005),'visual_gate':'PENDING_HUMAN_REVIEW',
      'controlled_delta':'V7 external reflection unchanged; only internal hidden RGB+depth provider changed',
      'decision_rule':'if right camel/rider gray-white fake surface becomes coherent while coverage/relock remain stable, learned content is validated; then extend the same provider to border world instead of reflection'
    }
    a.report.write_text(json.dumps(rep,indent=2)+'\n',encoding='utf-8'); print(json.dumps(rep,indent=2)); return 0

if __name__=='__main__': raise SystemExit(main())
