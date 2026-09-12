#!/usr/bin/env python3
"""AW-011 V7: extended-canvas boundary world + internal joint completion.

V6 proved that a same-size 'foundation' cannot solve canvas-boundary disocclusion:
the left black wedge remains because there is literally no canonical support
outside the original image rectangle. V7 adds the missing representation: a
persistent padded world only for outside-canvas exposure, while preserving V6's
internal joint RGB+depth completion unchanged.

The padded texture is diagnostic reflected Doré context, not accepted final art.
Its purpose is to remove the boundary-representation confounder so the right
camel/rider internal reveal can be judged independently.
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
from experiment_joint_hidden_completion_v5 import complete_hidden_world
from experiment_world_cache import raster_layer


def build_extended_boundary_world(src, dep, pad):
    # Reflection is diagnostic only; it provides persistent content outside the
    # canonical canvas so coverage can be separated from internal completion.
    ext_rgb = cv2.copyMakeBorder(src, pad, pad, pad, pad, cv2.BORDER_REFLECT_101)
    ext_dep = cv2.copyMakeBorder(dep, pad, pad, pad, pad, cv2.BORDER_REPLICATE).astype(np.float32)
    # Push external support slightly behind the visible canvas world.
    ext_dep = np.clip(ext_dep - .06, 0.0, 1.0)
    mask = np.full(ext_dep.shape, 255, np.uint8)
    mask[pad:pad+dep.shape[0], pad:pad+dep.shape[1]] = 0
    return ext_rgb, ext_dep, mask


def raster_mask(mask, depth, pose, ppu, step=5):
    probe=cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    warped,known=raster_layer(probe,depth,pose,ppu,step,None)
    return (known>0)&(warped[:,:,0]>96)


def crop_center(arr, pad, h, w):
    return arr[pad:pad+h, pad:pad+w]


def render(src,dep,irgb,idep,imask,ergb,edep,emask,pad,pose,ppu):
    h,w=dep.shape
    frame=np.zeros_like(src); occupied=np.zeros((h,w),np.uint8)

    # Render extended world, then crop back to canonical viewport.
    eimg,eknown=raster_layer(ergb,edep,pose,ppu,5,None)
    evis=raster_mask(emask,edep,pose,ppu,5)
    eimg=crop_center(eimg,pad,h,w); eknown=crop_center(eknown,pad,h,w); evis=crop_center(evis,pad,h,w)
    etake=(eknown>0)&evis
    frame[etake]=eimg[etake]; occupied[etake]=255

    # Internal persistent completed world.
    iimg,iknown=raster_layer(irgb,idep,pose,ppu,5,None)
    ivis=raster_mask(imask,idep,pose,ppu,5)
    itake=(iknown>0)&ivis
    frame[itake]=iimg[itake]; occupied[itake]=255

    front,fknown=raster_layer(src,dep,pose,ppu,5,.10)
    frame[fknown>0]=front[fknown>0]
    residual=(fknown==0)&(occupied==0); frame[residual]=0
    unseen=float(np.count_nonzero(fknown==0)/fknown.size); res=float(np.count_nonzero(residual)/fknown.size)
    return frame,unseen,max(0.0,unseen-res),res,fknown,occupied,int(np.count_nonzero(itake)),int(np.count_nonzero(etake))


def main():
    ap=argparse.ArgumentParser()
    for k in ('source','depth','spine','output','report'): ap.add_argument('--'+k,type=Path,required=True)
    ap.add_argument('--support-map',type=Path); ap.add_argument('--edge-map',type=Path); ap.add_argument('--hidden-depth-map',type=Path)
    ap.add_argument('--width',type=int,default=480); ap.add_argument('--fps',type=int,default=12); ap.add_argument('--segment-frames',type=int,default=4)
    ap.add_argument('--ppu',type=float,default=520.0); ap.add_argument('--samples',type=int,default=4); ap.add_argument('--behind',type=float,default=.08)
    ap.add_argument('--edge-q',type=float,default=.90); ap.add_argument('--min-jump',type=float,default=.055)
    a=ap.parse_args()

    src,dep=prepare(a.source,a.depth,a.width); poses=load_pose_points(a.spine)
    shift,radius=camera_lateral_budget(poses,a.ppu)
    support,zmap,used,mapped,inv_err=collect_depth_conditioned_support(dep,poses,a.ppu,a.samples,a.behind)
    topo=nearest_edge_topology(dep,support,a.edge_q,.025,a.min_jump,radius)
    irgb,idep,imask=complete_hidden_world(src,dep,support,zmap,topo)

    pad=max(24,int(np.ceil(shift+16.0)))
    ergb,edep,emask=build_extended_boundary_world(src,dep,pad)

    for path,img in ((a.support_map,support),(a.edge_map,topo['edge'])):
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
      'status':'EXTENDED_CANVAS_PLUS_JOINT_COMPLETION_READY_FOR_VISUAL_REVIEW',
      'mode':'persistent_extended_boundary_world_plus_internal_joint_completion',
      'trigger':'same-size foundation cannot represent outside-canvas disocclusion',
      'trajectory_samples_used':used,'mapped_support_samples':mapped,'mean_inverse_projection_error_pixels':inv_err,
      'support_fraction':float(np.count_nonzero(support)/support.size),'max_camera_lateral_shift_pixels':shift,
      'camera_conditioned_zone_radius_pixels':radius,'extended_canvas_pad_pixels':pad,
      'max_foreground_unseen_fraction':maxu,'mean_hidden_layer_coverage_ratio':cov,'max_residual_uncovered_fraction':maxr,
      'mean_hidden_boundary_discontinuity':float(np.mean(bmean)) if bmean else 0.0,'max_hidden_boundary_discontinuity_q95':max(b95,default=0.0),
      'internal_rendered_pixels_total':icount,'extended_boundary_rendered_pixels_total':ecount,'worst_residual':worst,
      'per_frame_synthesis':False,'exact_final_source_relock':True,'coverage_gate':bool(maxu>.001 and cov>=.96 and maxr<=.003),
      'visual_gate':'PENDING_HUMAN_REVIEW',
      'decision_rule':'if border black disappears while right internal gray surface persists, boundary representation is solved and learned edge-conditioned internal RGB+depth completion becomes the next isolated problem'
    }
    a.report.write_text(json.dumps(rep,indent=2)+'\n',encoding='utf-8'); print(json.dumps(rep,indent=2)); return 0

if __name__=='__main__': raise SystemExit(main())
