#!/usr/bin/env python3
"""AW-011 V13: armed corridor renderer with local structural-seam warp repair.

V12 remains the camera/geometry baseline. V13 adds the first real capability
escalation: repair.warp is admitted only for tiny structural residual components
inside the final 16:9 viewfinder. No external world and no generative synthesis.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import cv2
import numpy as np

from experiment_depth_traversal import prepare, load_pose_points, smoothstep
from experiment_depth_banded_world_cache import collect_depth_conditioned_support
from experiment_edge_aware_hidden_surface_v4 import camera_lateral_budget, nearest_edge_topology
from experiment_static_cinema_v10 import evaluate_ratio
from experiment_static_cinema_v11 import classify_components
from experiment_static_cinema_v12 import render
from hidden_surface_provider import learned_three_stage_complete


def nearest_valid_warp(frame: np.ndarray, residual: np.ndarray, max_component_pixels: int = 256):
    """Extend nearest known source/hidden pixels into tiny residual seams only."""
    mask = residual.astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    eligible = np.zeros_like(mask)
    h, w = mask.shape
    components = []
    for cid in range(1, n):
        x, y, cw, ch, area = [int(v) for v in stats[cid]]
        touches = bool(x == 0 or y == 0 or x + cw >= w or y + ch >= h)
        admit = bool(area <= max_component_pixels)
        components.append({
            'area': area,
            'bbox': [x, y, cw, ch],
            'touches_viewfinder_boundary': touches,
            'admitted_repair_warp': admit,
        })
        if admit:
            eligible[labels == cid] = 1
    if not np.any(eligible):
        return frame, residual, 0, components

    # OpenCV labels every non-zero pixel by its nearest zero pixel when using
    # DIST_LABEL_PIXEL. Here eligible seam pixels are non-zero and all known
    # pixels are zero, so labels provide a deterministic nearest-valid warp.
    _, dt_labels = cv2.distanceTransformWithLabels(
        eligible, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL
    )
    lut = {}
    ys, xs = np.where(eligible == 0)
    for yy, xx in zip(ys.tolist(), xs.tolist()):
        lab = int(dt_labels[yy, xx])
        if lab > 0 and lab not in lut:
            lut[lab] = (yy, xx)

    repaired = frame.copy()
    ry, rx = np.where(eligible > 0)
    fixed = 0
    for yy, xx in zip(ry.tolist(), rx.tolist()):
        src = lut.get(int(dt_labels[yy, xx]))
        if src is None:
            continue
        repaired[yy, xx] = frame[src[0], src[1]]
        fixed += 1
    remaining = residual.copy()
    remaining[eligible > 0] = False
    return repaired, remaining, fixed, components


def main():
    ap = argparse.ArgumentParser()
    for k in ('source','depth','spine','output','report'):
        ap.add_argument('--'+k, type=Path, required=True)
    ap.add_argument('--networks',type=Path,required=True)
    ap.add_argument('--edge-checkpoint',type=Path,required=True)
    ap.add_argument('--depth-checkpoint',type=Path,required=True)
    ap.add_argument('--color-checkpoint',type=Path,required=True)
    ap.add_argument('--device',default='cpu')
    ap.add_argument('--width',type=int,default=480)
    ap.add_argument('--output-width',type=int,default=640)
    ap.add_argument('--fps',type=int,default=12)
    ap.add_argument('--segment-frames',type=int,default=4)
    ap.add_argument('--ppu',type=float,default=520.0)
    ap.add_argument('--samples',type=int,default=4)
    ap.add_argument('--behind',type=float,default=.08)
    ap.add_argument('--edge-q',type=float,default=.90)
    ap.add_argument('--min-jump',type=float,default=.055)
    ap.add_argument('--target-residual',type=float,default=.001)
    ap.add_argument('--min-view-scale',type=float,default=.45)
    ap.add_argument('--raster-step',type=int,default=3)
    ap.add_argument('--deviation-threshold',type=float,default=1.25)
    ap.add_argument('--warp-max-component-pixels',type=int,default=256)
    a = ap.parse_args()

    src, dep = prepare(a.source, a.depth, a.width)
    poses = load_pose_points(a.spine)
    shift, radius = camera_lateral_budget(poses, a.ppu)
    support, zmap, used, mapped, inv_err = collect_depth_conditioned_support(
        dep, poses, a.ppu, a.samples, a.behind)
    topo = nearest_edge_topology(dep, support, a.edge_q, .025, a.min_jump, radius)
    internal = learned_three_stage_complete(
        src, dep, support, zmap, topo,
        a.networks, a.edge_checkpoint, a.depth_checkpoint, a.color_checkpoint, a.device)

    frames=[]; masks=[]; active=[]; maxdev=[]; sampled=[]; hidden_pixels=0
    for i in range(len(poses)-1):
        p0=np.asarray(poses[i]['position'],np.float32)
        p1=np.asarray(poses[i+1]['position'],np.float32)
        for j in range(a.segment_frames):
            t=smoothstep(j/float(a.segment_frames)); p=p0*(1-t)+p1*t
            if np.linalg.norm(p)<1e-6:
                frame=src.copy(); residual=np.zeros(dep.shape,np.bool_); af=0.0; md=0.0; hp=0
            else:
                frame,residual,af,md,hp=render(
                    src,dep,internal.rgb,internal.depth,internal.mask,p,
                    a.ppu,a.raster_step,a.deviation_threshold)
            frames.append(frame); masks.append(residual); active.append(af); maxdev.append(md)
            sampled.append([float(x) for x in p]); hidden_pixels += hp

    h,w=dep.shape
    chosen=evaluate_ratio(masks,h,w,16/9,a.target_residual,a.min_view_scale)
    x0,y0,cw,ch=chosen['rect']

    repaired_crops=[]; remaining_masks=[]; warp_pixels=[]; warp_events=[]
    raw_residuals=[]
    for fi,(fr,m) in enumerate(zip(frames,masks)):
        crop=fr[y0:y0+ch,x0:x0+cw].copy()
        cm=m[y0:y0+ch,x0:x0+cw].copy()
        raw_residuals.append(float(np.count_nonzero(cm)/cm.size))
        repaired, remaining, fixed, comps = nearest_valid_warp(
            crop, cm, a.warp_max_component_pixels)
        repaired_crops.append(repaired); remaining_masks.append(remaining); warp_pixels.append(fixed)
        if fixed:
            warp_events.append({
                'frame':fi,
                'pose':sampled[fi],
                'capability':'repair.warp',
                'pixels_repaired':fixed,
                'components':comps,
                'fallback_used':False,
            })

    residuals=[float(np.count_nonzero(m)/m.size) for m in remaining_masks]
    wi=int(np.argmax(residuals)) if residuals else -1
    wm=remaining_masks[wi] if wi>=0 else np.zeros((ch,cw),np.bool_)
    comps=classify_components(wm)
    structural=sum(c['area'] for c in comps if c['kind']=='structural_disocclusion')
    micro=sum(c['area'] for c in comps if c['kind']=='micro_raster_candidate')

    out_w=a.output_width-(a.output_width%2); out_h=int(round(out_w*9/16)); out_h-=out_h%2
    a.output.parent.mkdir(parents=True,exist_ok=True)
    wr=cv2.VideoWriter(str(a.output),cv2.VideoWriter_fourcc(*'mp4v'),a.fps,(out_w,out_h))
    if not wr.isOpened(): raise RuntimeError('video writer failed')
    for crop in repaired_crops:
        wr.write(cv2.resize(crop,(out_w,out_h),interpolation=cv2.INTER_CUBIC))
    canonical=src[y0:y0+ch,x0:x0+cw]
    wr.write(cv2.resize(canonical,(out_w,out_h),interpolation=cv2.INTER_CUBIC)); wr.release()

    rep={
        'status':'STATIC_CINEMA_V13_ARMED_CORRIDOR_READY_FOR_VISUAL_REVIEW',
        'mode':'v12_corridor_plus_event_driven_local_repair_warp',
        'canonical_world':'original_dore_artwork',
        'external_world_generation':False,
        'deviation_threshold_px':a.deviation_threshold,
        'mean_active_3d_vertex_fraction':float(np.mean(active)) if active else 0.0,
        'max_active_3d_vertex_fraction':max(active,default=0.0),
        'max_true_3d_deviation_px':max(maxdev,default=0.0),
        'raw_max_residual_fraction_before_weapon':max(raw_residuals,default=0.0),
        'max_final_viewfinder_residual_fraction':max(residuals,default=0.0),
        'mean_final_viewfinder_residual_fraction':float(np.mean(residuals)) if residuals else 0.0,
        'repair_warp_event_count':len(warp_events),
        'repair_warp_pixels_total':int(sum(warp_pixels)),
        'repair_warp_max_component_pixels':a.warp_max_component_pixels,
        'weapon_events':warp_events,
        'worst_frame_index':wi,
        'worst_frame_structural_disocclusion_pixels':structural,
        'worst_frame_micro_raster_candidate_pixels':micro,
        'persistent_hidden_pixels_rendered_total':hidden_pixels,
        'source_relock':True,
        'per_frame_synthesis':False,
        'generative_fallback_used':False,
        'capability_policy':'projection -> local 3D deviation -> persistent hidden layer -> event-driven repair.warp; stronger weapons remain holstered',
    }
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(rep,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(rep,indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
