#!/usr/bin/env python3
"""AW-011 V6: separate canvas-boundary world from internal occlusion completion.

V5 materially improved the probe (hidden coverage ~9% -> ~48%, residual ~11.6%
-> ~6.6%) but visual review still showed two different failure classes:
  * black wedges entering from the canvas boundary;
  * a large pale/gray internal reveal around the right camel/rider.

Those must not be judged as one mechanism. V6 keeps V5's persistent joint
hidden RGB+depth surface for *internal* disocclusion, while routing only a thin
canonical border band to a persistent background foundation. This removes the
canvas-boundary confounder before deciding whether learned/local hidden-content
completion is required for the internal reveal.
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
from experiment_world_cache import raster_layer, build_hidden_layer


def split_support(support: np.ndarray, border_fraction: float = .10):
    h, w = support.shape
    bx = max(8, int(round(w * border_fraction)))
    by = max(8, int(round(h * border_fraction)))
    border = np.zeros_like(support, np.uint8)
    border[:, :bx] = 255
    border[:, w-bx:] = 255
    border[:by, :] = 255
    border[h-by:, :] = 255
    boundary = cv2.bitwise_and(support, border)
    internal = support.copy()
    internal[boundary > 0] = 0
    return internal, boundary, bx, by


def raster_support(mask, depth, pose, ppu):
    probe = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    warped, known = raster_layer(probe, depth, pose, ppu, 5, None)
    return (known > 0) & (warped[:, :, 0] > 96)


def render(src, dep, irgb, idep, imask, brgb, bdep, bmask, pose, ppu=520.0):
    h, w = dep.shape
    frame = np.zeros_like(src)
    occupied = np.zeros((h, w), np.uint8)

    # Canvas-boundary support is a coarse persistent foundation, not evidence
    # about internal occlusion topology.
    bimg, bknown = raster_layer(brgb, bdep, pose, ppu, 5, None)
    bvis = raster_support(bmask, bdep, pose, ppu)
    btake = (bknown > 0) & bvis
    frame[btake] = bimg[btake]
    occupied[btake] = 255

    # Internal disocclusion uses the joint RGB+depth completed hidden surface.
    iimg, iknown = raster_layer(irgb, idep, pose, ppu, 5, None)
    ivis = raster_support(imask, idep, pose, ppu)
    itake = (iknown > 0) & ivis
    frame[itake] = iimg[itake]
    occupied[itake] = 255

    front, front_known = raster_layer(src, dep, pose, ppu, 5, .10)
    frame[front_known > 0] = front[front_known > 0]
    residual = (front_known == 0) & (occupied == 0)
    frame[residual] = 0

    unseen = float(np.count_nonzero(front_known == 0) / front_known.size)
    res = float(np.count_nonzero(residual) / front_known.size)
    return frame, unseen, max(0.0, unseen-res), res, front_known, occupied, int(np.count_nonzero(itake)), int(np.count_nonzero(btake))


def main():
    ap = argparse.ArgumentParser()
    for k in ('source','depth','spine','output','report'):
        ap.add_argument('--'+k, type=Path, required=True)
    ap.add_argument('--support-map', type=Path)
    ap.add_argument('--internal-map', type=Path)
    ap.add_argument('--boundary-map', type=Path)
    ap.add_argument('--hidden-depth-map', type=Path)
    ap.add_argument('--width', type=int, default=480)
    ap.add_argument('--fps', type=int, default=12)
    ap.add_argument('--segment-frames', type=int, default=4)
    ap.add_argument('--ppu', type=float, default=520.0)
    ap.add_argument('--samples', type=int, default=4)
    ap.add_argument('--behind', type=float, default=.08)
    ap.add_argument('--edge-q', type=float, default=.90)
    ap.add_argument('--min-jump', type=float, default=.055)
    ap.add_argument('--border-fraction', type=float, default=.10)
    a = ap.parse_args()

    src, dep = prepare(a.source, a.depth, a.width)
    poses = load_pose_points(a.spine)
    shift, radius = camera_lateral_budget(poses, a.ppu)
    support, zmap, used, mapped, inv_err = collect_depth_conditioned_support(dep, poses, a.ppu, a.samples, a.behind)
    internal, boundary, bx, by = split_support(support, a.border_fraction)

    topo = nearest_edge_topology(dep, internal, a.edge_q, .025, a.min_jump, radius)
    irgb, idep, imask = complete_hidden_world(src, dep, internal, zmap, topo)

    brgb, bdep, _ = build_hidden_layer(src, dep)
    bmask = cv2.dilate(boundary, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))

    for path,img in ((a.support_map,support),(a.internal_map,internal),(a.boundary_map,boundary)):
        if path:
            path.parent.mkdir(parents=True, exist_ok=True); cv2.imwrite(str(path),img)
    if a.hidden_depth_map:
        a.hidden_depth_map.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(a.hidden_depth_map), np.uint8(np.clip(idep,0,1)*255))

    h,w = src.shape[:2]
    a.output.parent.mkdir(parents=True, exist_ok=True)
    writer=cv2.VideoWriter(str(a.output),cv2.VideoWriter_fourcc(*'mp4v'),a.fps,(w,h))
    if not writer.isOpened(): raise RuntimeError('video writer failed')

    unseen=[]; coverage=[]; residual=[]; bmean=[]; b95=[]
    internal_rendered=boundary_rendered=0
    worst={'fraction':-1.0,'frame':-1,'pose':None}; fn=0
    for i in range(len(poses)-1):
        p0=np.asarray(poses[i]['position'],np.float32); p1=np.asarray(poses[i+1]['position'],np.float32)
        for j in range(a.segment_frames):
            t=smoothstep(j/float(a.segment_frames)); p=p0*(1-t)+p1*t
            if np.linalg.norm(p)<1e-6:
                writer.write(src); fn+=1; continue
            frame,u,c,r,fk,occ,ic,bc=render(src,dep,irgb,idep,imask,brgb,bdep,bmask,p,a.ppu)
            bm,bp=boundary_discontinuity(frame,fk,occ)
            writer.write(frame); unseen.append(u); coverage.append(c); residual.append(r); bmean.append(bm); b95.append(bp)
            internal_rendered+=ic; boundary_rendered+=bc
            if r>worst['fraction']: worst={'fraction':r,'frame':fn,'pose':[float(x) for x in p]}
            fn+=1
    writer.write(src); writer.release()

    maxu=max(unseen,default=0.0); maxr=max(residual,default=0.0)
    cov=float(np.mean([c/u if u>1e-9 else 1.0 for c,u in zip(coverage,unseen)])) if unseen else 1.0
    sp=max(1,np.count_nonzero(support))
    rep={
      'status':'BOUNDARY_SEPARATED_JOINT_COMPLETION_READY_FOR_VISUAL_REVIEW',
      'mode':'internal_joint_rgb_depth_plus_boundary_foundation',
      'trigger':'V5 improved coverage but mixed canvas-boundary and internal reveal failures',
      'trajectory_samples_used':used,
      'mapped_support_samples':mapped,
      'mean_inverse_projection_error_pixels':inv_err,
      'support_fraction':float(np.count_nonzero(support)/support.size),
      'internal_support_ratio':float(np.count_nonzero(internal)/sp),
      'boundary_support_ratio':float(np.count_nonzero(boundary)/sp),
      'canonical_border_pixels_x':bx,
      'canonical_border_pixels_y':by,
      'max_camera_lateral_shift_pixels':shift,
      'camera_conditioned_zone_radius_pixels':radius,
      'max_foreground_unseen_fraction':maxu,
      'mean_hidden_layer_coverage_ratio':cov,
      'max_residual_uncovered_fraction':maxr,
      'mean_hidden_boundary_discontinuity':float(np.mean(bmean)) if bmean else 0.0,
      'max_hidden_boundary_discontinuity_q95':max(b95,default=0.0),
      'internal_rendered_pixels_total':internal_rendered,
      'boundary_rendered_pixels_total':boundary_rendered,
      'worst_residual':worst,
      'per_frame_synthesis':False,
      'exact_final_source_relock':True,
      'coverage_gate':bool(maxu>.001 and cov>=.96 and maxr<=.003),
      'visual_gate':'PENDING_HUMAN_REVIEW',
      'decision_rule':'judge internal camel/rider reveal independently of border exposure; if internal gray/false surface persists, move to learned edge-conditioned hidden RGB+depth completion'
    }
    a.report.write_text(json.dumps(rep,indent=2)+'\n',encoding='utf-8'); print(json.dumps(rep,indent=2))
    return 0

if __name__=='__main__': raise SystemExit(main())
