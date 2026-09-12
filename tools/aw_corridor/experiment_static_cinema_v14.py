#!/usr/bin/env python3
"""AW-011 V14: dual-blade engraving-aware armed corridor.

Blade 1: geometry seam closure with V13 repair.warp.
Blade 2: engraving-aware local structural repair, admitted only when a local
fidelity gate says the warp-covered wound is too flat / discontinuous relative
to the surrounding Dore engraving. No external world and no generative NVS.
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
from experiment_static_cinema_v13 import nearest_valid_warp
from hidden_surface_provider import learned_three_stage_complete


def _gray(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def engraving_metrics(img: np.ndarray, wound: np.ndarray, ring_px: int = 5):
    """Compare repaired wound structure to a known-source annulus around it."""
    m = wound.astype(np.uint8)
    if not np.any(m):
        return {
            'wound_pixels': 0,
            'edge_density_wound': 0.0,
            'edge_density_ring': 0.0,
            'variance_wound': 0.0,
            'variance_ring': 0.0,
            'edge_density_ratio': 1.0,
            'variance_ratio': 1.0,
            'fidelity_pass': True,
        }
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ring_px*2+1, ring_px*2+1))
    ring = (cv2.dilate(m, kernel) > 0) & (m == 0)
    g = _gray(img)
    edges = cv2.Canny(g, 45, 110) > 0
    wound_b = m > 0
    ew = float(edges[wound_b].mean()) if np.any(wound_b) else 0.0
    er = float(edges[ring].mean()) if np.any(ring) else 0.0
    vw = float(np.var(g[wound_b].astype(np.float32))) if np.any(wound_b) else 0.0
    vr = float(np.var(g[ring].astype(np.float32))) if np.any(ring) else 0.0
    edge_ratio = ew / max(er, 1e-6)
    var_ratio = vw / max(vr, 1e-6)
    # A repaired engraving wound should not collapse into a smooth gray slab.
    passed = bool(edge_ratio >= 0.45 and var_ratio >= 0.35)
    return {
        'wound_pixels': int(np.count_nonzero(wound_b)),
        'edge_density_wound': ew,
        'edge_density_ring': er,
        'variance_wound': vw,
        'variance_ring': vr,
        'edge_density_ratio': edge_ratio,
        'variance_ratio': var_ratio,
        'fidelity_pass': passed,
    }


def engraving_structure_repair(prewarp: np.ndarray, warp: np.ndarray, wound: np.ndarray):
    """Second blade: PDE/isophote continuation restricted to the tiny wound.

    The source image outside the wound remains immutable. OpenCV Navier-Stokes
    inpainting continues local intensity contours across the wound, which is a
    better fit for engraved line continuity than nearest-pixel copying.
    """
    mask = (wound.astype(np.uint8) * 255)
    if not np.any(mask):
        return warp.copy()
    # Give the structure solver one-pixel context but only commit wound pixels.
    context_mask = cv2.dilate(mask, np.ones((3,3), np.uint8), iterations=1)
    candidate = cv2.inpaint(prewarp, context_mask, 3.0, cv2.INPAINT_NS)
    out = warp.copy()
    w = mask > 0
    out[w] = candidate[w]
    return out


def main():
    ap=argparse.ArgumentParser()
    for k in ('source','depth','spine','output','report'):
        ap.add_argument('--'+k,type=Path,required=True)
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
    ap.add_argument('--diagnostic-dir',type=Path)
    a=ap.parse_args()

    src,dep=prepare(a.source,a.depth,a.width); poses=load_pose_points(a.spine)
    shift,radius=camera_lateral_budget(poses,a.ppu)
    support,zmap,used,mapped,inv_err=collect_depth_conditioned_support(dep,poses,a.ppu,a.samples,a.behind)
    topo=nearest_edge_topology(dep,support,a.edge_q,.025,a.min_jump,radius)
    internal=learned_three_stage_complete(src,dep,support,zmap,topo,a.networks,a.edge_checkpoint,a.depth_checkpoint,a.color_checkpoint,a.device)

    frames=[]; masks=[]; active=[]; maxdev=[]; sampled=[]; hidden_pixels=0
    for i in range(len(poses)-1):
        p0=np.asarray(poses[i]['position'],np.float32); p1=np.asarray(poses[i+1]['position'],np.float32)
        for j in range(a.segment_frames):
            t=smoothstep(j/float(a.segment_frames)); p=p0*(1-t)+p1*t
            if np.linalg.norm(p)<1e-6:
                frame=src.copy(); residual=np.zeros(dep.shape,np.bool_); af=0.0; md=0.0; hp=0
            else:
                frame,residual,af,md,hp=render(src,dep,internal.rgb,internal.depth,internal.mask,p,a.ppu,a.raster_step,a.deviation_threshold)
            frames.append(frame); masks.append(residual); active.append(af); maxdev.append(md); sampled.append([float(x) for x in p]); hidden_pixels+=hp

    h,w=dep.shape
    chosen=evaluate_ratio(masks,h,w,16/9,a.target_residual,a.min_view_scale)
    x0,y0,cw,ch=chosen['rect']

    final_crops=[]; remaining_masks=[]; events=[]; raw_res=[]
    sword1_pixels=0; sword2_pixels=0; sword2_events=0
    if a.diagnostic_dir: a.diagnostic_dir.mkdir(parents=True,exist_ok=True)

    for fi,(fr,m) in enumerate(zip(frames,masks)):
        crop=fr[y0:y0+ch,x0:x0+cw].copy(); cm=m[y0:y0+ch,x0:x0+cw].copy()
        raw_res.append(float(np.count_nonzero(cm)/cm.size))
        warp, remaining, fixed, comps=nearest_valid_warp(crop,cm,a.warp_max_component_pixels)
        wound=cm & (~remaining)
        sword1_pixels += fixed
        before=engraving_metrics(warp,wound)
        final=warp
        second=False
        after=before
        if fixed and not before['fidelity_pass']:
            second=True; sword2_events += 1; sword2_pixels += int(np.count_nonzero(wound))
            final=engraving_structure_repair(crop,warp,wound)
            after=engraving_metrics(final,wound)
        final_crops.append(final); remaining_masks.append(remaining)
        if fixed:
            events.append({
                'frame':fi,'pose':sampled[fi],
                'blade_1':'repair.warp','blade_1_pixels':fixed,
                'fidelity_after_blade_1':before,
                'blade_2':'repair.engraving-structure' if second else None,
                'blade_2_pixels':int(np.count_nonzero(wound)) if second else 0,
                'fidelity_after_blade_2':after,
                'generative_fallback_used':False,
            })
            if a.diagnostic_dir:
                cv2.imwrite(str(a.diagnostic_dir/f'frame-{fi:02d}-blade1.png'),warp)
                cv2.imwrite(str(a.diagnostic_dir/f'frame-{fi:02d}-blade2.png'),final)
                cv2.imwrite(str(a.diagnostic_dir/f'frame-{fi:02d}-wound.png'),wound.astype(np.uint8)*255)

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
    for crop in final_crops: wr.write(cv2.resize(crop,(out_w,out_h),interpolation=cv2.INTER_CUBIC))
    canonical=src[y0:y0+ch,x0:x0+cw]
    wr.write(cv2.resize(canonical,(out_w,out_h),interpolation=cv2.INTER_CUBIC)); wr.release()

    final_fidelity_fail=sum(1 for e in events if not e['fidelity_after_blade_2']['fidelity_pass'])
    rep={
      'status':'STATIC_CINEMA_V14_DUAL_BLADE_READY_FOR_VISUAL_REVIEW',
      'mode':'geometry_blade_then_engraving_blade_under_fidelity_gate',
      'canonical_world':'original_dore_artwork','external_world_generation':False,
      'deviation_threshold_px':a.deviation_threshold,
      'mean_active_3d_vertex_fraction':float(np.mean(active)) if active else 0.0,
      'max_active_3d_vertex_fraction':max(active,default=0.0),
      'max_true_3d_deviation_px':max(maxdev,default=0.0),
      'raw_max_residual_fraction_before_weapon':max(raw_res,default=0.0),
      'max_final_viewfinder_residual_fraction':max(residuals,default=0.0),
      'blade_1_warp_pixels_total':int(sword1_pixels),
      'blade_2_engraving_event_count':int(sword2_events),
      'blade_2_engraving_pixels_total':int(sword2_pixels),
      'final_fidelity_fail_event_count':int(final_fidelity_fail),
      'weapon_events':events,
      'worst_frame_index':wi,
      'worst_frame_structural_disocclusion_pixels':structural,
      'worst_frame_micro_raster_candidate_pixels':micro,
      'persistent_hidden_pixels_rendered_total':hidden_pixels,
      'source_relock':True,'per_frame_synthesis':False,'generative_fallback_used':False,
      'capability_policy':'blade1 geometry closure -> engraving fidelity gate -> blade2 local structure continuation only on fidelity failure; stronger generative weapons remain holstered'
    }
    a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(json.dumps(rep,indent=2)+'\n',encoding='utf-8'); print(json.dumps(rep,indent=2))
    return 0

if __name__=='__main__': raise SystemExit(main())
