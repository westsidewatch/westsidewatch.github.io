#!/usr/bin/env python3
"""AW-011 V10: original artwork is the world; 16:9 is the camera.

V9 proved that a larger persistent world removes coverage holes, but also showed
that generating an entire outside-canvas world creates unnecessary visual debt.
V10 keeps the useful depth/topology/occlusion work and removes border-world
generation entirely. The Doré source is the canonical world, the Golden Camera
Spine drives XY+Z motion, and learned completion is admitted only for internal
disocclusion. A ratio bakeoff finds the largest safe centred viewfinder that can
travel through the whole spine without exposing outside-canvas residuals.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from experiment_depth_traversal import prepare, load_pose_points, smoothstep
from experiment_depth_banded_world_cache import collect_depth_conditioned_support
from experiment_edge_aware_hidden_surface_v4 import camera_lateral_budget, nearest_edge_topology
from experiment_joint_hidden_completion_v7 import raster_mask
from experiment_world_cache import raster_layer
from hidden_surface_provider import learned_three_stage_complete


def render_internal_world(src, dep, irgb, idep, imask, pose, ppu):
    """Render canonical source + persistent internal hidden layer; no border world."""
    h, w = dep.shape
    frame = np.zeros_like(src)
    occupied = np.zeros((h, w), np.uint8)

    iimg, iknown = raster_layer(irgb, idep, pose, ppu, 5, None)
    ivis = raster_mask(imask, idep, pose, ppu, 5)
    itake = (iknown > 0) & ivis
    frame[itake] = iimg[itake]
    occupied[itake] = 255

    front, fknown = raster_layer(src, dep, pose, ppu, 5, .10)
    frame[fknown > 0] = front[fknown > 0]
    residual = (fknown == 0) & (occupied == 0)
    frame[residual] = 0
    return frame, residual, fknown, occupied, int(np.count_nonzero(itake))


def centred_rect(h: int, w: int, aspect: float, scale: float):
    max_w = min(w, int(np.floor(h * aspect)))
    cw = max(2, int(np.floor(max_w * scale)))
    ch = max(2, int(np.floor(cw / aspect)))
    cw -= cw % 2
    ch -= ch % 2
    x0 = (w - cw) // 2
    y0 = (h - ch) // 2
    return x0, y0, cw, ch


def evaluate_ratio(residual_masks, h, w, aspect, target_residual, min_scale):
    best = None
    # Largest-first search. The crop is global and fixed for the whole shot.
    for scale in np.linspace(1.0, min_scale, 111):
        x0, y0, cw, ch = centred_rect(h, w, aspect, float(scale))
        vals = [float(np.count_nonzero(m[y0:y0+ch, x0:x0+cw]) / (cw * ch)) for m in residual_masks]
        candidate = {
            'aspect': aspect,
            'scale_of_max_inscribed_view': float(scale),
            'rect': [x0, y0, cw, ch],
            'max_residual_fraction': max(vals, default=0.0),
            'mean_residual_fraction': float(np.mean(vals)) if vals else 0.0,
            'passes': bool(max(vals, default=0.0) <= target_residual),
        }
        if candidate['passes']:
            best = candidate
            break
    if best is None:
        x0, y0, cw, ch = centred_rect(h, w, aspect, min_scale)
        vals = [float(np.count_nonzero(m[y0:y0+ch, x0:x0+cw]) / (cw * ch)) for m in residual_masks]
        best = {
            'aspect': aspect,
            'scale_of_max_inscribed_view': min_scale,
            'rect': [x0, y0, cw, ch],
            'max_residual_fraction': max(vals, default=0.0),
            'mean_residual_fraction': float(np.mean(vals)) if vals else 0.0,
            'passes': False,
        }
    best['retained_source_fraction'] = float((best['rect'][2] * best['rect'][3]) / (w * h))
    return best


def main():
    ap = argparse.ArgumentParser()
    for k in ('source', 'depth', 'spine', 'output', 'report'):
        ap.add_argument('--' + k, type=Path, required=True)
    ap.add_argument('--support-map', type=Path)
    ap.add_argument('--edge-map', type=Path)
    ap.add_argument('--hidden-depth-map', type=Path)
    ap.add_argument('--viewfinder-preview', type=Path)
    ap.add_argument('--networks', type=Path, required=True)
    ap.add_argument('--edge-checkpoint', type=Path, required=True)
    ap.add_argument('--depth-checkpoint', type=Path, required=True)
    ap.add_argument('--color-checkpoint', type=Path, required=True)
    ap.add_argument('--device', default='cpu')
    ap.add_argument('--width', type=int, default=480)
    ap.add_argument('--output-width', type=int, default=640)
    ap.add_argument('--fps', type=int, default=12)
    ap.add_argument('--segment-frames', type=int, default=4)
    ap.add_argument('--ppu', type=float, default=520.0)
    ap.add_argument('--samples', type=int, default=4)
    ap.add_argument('--behind', type=float, default=.08)
    ap.add_argument('--edge-q', type=float, default=.90)
    ap.add_argument('--min-jump', type=float, default=.055)
    ap.add_argument('--target-residual', type=float, default=.001)
    ap.add_argument('--min-view-scale', type=float, default=.45)
    a = ap.parse_args()

    for p in (a.networks, a.edge_checkpoint, a.depth_checkpoint, a.color_checkpoint):
        if not p.exists():
            raise FileNotFoundError(p)

    src, dep = prepare(a.source, a.depth, a.width)
    poses = load_pose_points(a.spine)
    shift, radius = camera_lateral_budget(poses, a.ppu)
    support, zmap, used, mapped, inv_err = collect_depth_conditioned_support(
        dep, poses, a.ppu, a.samples, a.behind)
    topo = nearest_edge_topology(dep, support, a.edge_q, .025, a.min_jump, radius)
    internal = learned_three_stage_complete(
        src, dep, support, zmap, topo,
        a.networks, a.edge_checkpoint, a.depth_checkpoint, a.color_checkpoint, a.device,
    )

    for path, img in ((a.support_map, support), (a.edge_map, internal.edge)):
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(path), img)
    if a.hidden_depth_map:
        a.hidden_depth_map.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(a.hidden_depth_map), np.uint8(np.clip(internal.depth, 0, 1) * 255))

    frames = []
    residual_masks = []
    internal_pixels = 0
    sampled_poses = []
    for i in range(len(poses) - 1):
        p0 = np.asarray(poses[i]['position'], np.float32)
        p1 = np.asarray(poses[i + 1]['position'], np.float32)
        for j in range(a.segment_frames):
            t = smoothstep(j / float(a.segment_frames))
            p = p0 * (1 - t) + p1 * t
            if np.linalg.norm(p) < 1e-6:
                frame = src.copy()
                residual = np.zeros(dep.shape, np.bool_)
                ic = 0
            else:
                frame, residual, _, _, ic = render_internal_world(
                    src, dep, internal.rgb, internal.depth, internal.mask, p, a.ppu)
            frames.append(frame)
            residual_masks.append(residual)
            internal_pixels += ic
            sampled_poses.append([float(x) for x in p])

    h, w = dep.shape
    ratios = {
        '16:9': 16.0 / 9.0,
        '8:5': 8.0 / 5.0,
        '4:3': 4.0 / 3.0,
    }
    bakeoff = {
        name: evaluate_ratio(residual_masks, h, w, aspect, a.target_residual, a.min_view_scale)
        for name, aspect in ratios.items()
    }
    chosen = bakeoff['16:9']
    x0, y0, cw, ch = chosen['rect']

    out_w = a.output_width - (a.output_width % 2)
    out_h = int(round(out_w * 9.0 / 16.0))
    out_h -= out_h % 2
    a.output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(a.output), cv2.VideoWriter_fourcc(*'mp4v'), a.fps, (out_w, out_h))
    if not writer.isOpened():
        raise RuntimeError('video writer failed')
    for frame in frames:
        crop = frame[y0:y0+ch, x0:x0+cw]
        writer.write(cv2.resize(crop, (out_w, out_h), interpolation=cv2.INTER_CUBIC))
    canonical_crop = src[y0:y0+ch, x0:x0+cw]
    writer.write(cv2.resize(canonical_crop, (out_w, out_h), interpolation=cv2.INTER_CUBIC))
    writer.release()

    if a.viewfinder_preview:
        preview = src.copy()
        cv2.rectangle(preview, (x0, y0), (x0 + cw - 1, y0 + ch - 1), (255, 255, 255), 2)
        a.viewfinder_preview.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(a.viewfinder_preview), preview)

    cropped_residuals = [
        float(np.count_nonzero(m[y0:y0+ch, x0:x0+cw]) / (cw * ch)) for m in residual_masks
    ]
    full_residuals = [float(np.count_nonzero(m) / m.size) for m in residual_masks]
    z_values = [p[2] for p in sampled_poses]
    rep = {
        'status': 'STATIC_CINEMA_16_9_READY_FOR_VISUAL_REVIEW',
        'mode': 'canonical_source_world_plus_internal_completion_plus_safe_viewfinder',
        'camera_spine_semantics': 'golden-line XY trajectory with Z push/pull',
        'canonical_world': 'original_dore_artwork',
        'external_world_generation': False,
        'external_generated_pixels_total': 0,
        'internal_provider': internal.provider,
        'trajectory_samples_used': used,
        'mapped_support_samples': mapped,
        'mean_inverse_projection_error_pixels': inv_err,
        'support_fraction': float(np.count_nonzero(support) / support.size),
        'max_camera_lateral_shift_pixels': shift,
        'camera_conditioned_zone_radius_pixels': radius,
        'z_range': [float(min(z_values, default=0.0)), float(max(z_values, default=0.0))],
        'internal_rendered_pixels_total': internal_pixels,
        'ratio_bakeoff': bakeoff,
        'selected_ratio': '16:9',
        'selected_viewfinder_rect': chosen['rect'],
        'selected_viewfinder_source_fraction': chosen['retained_source_fraction'],
        'max_full_canvas_residual_fraction': max(full_residuals, default=0.0),
        'max_final_viewfinder_residual_fraction': max(cropped_residuals, default=0.0),
        'mean_final_viewfinder_residual_fraction': float(np.mean(cropped_residuals)) if cropped_residuals else 0.0,
        'viewfinder_gate': bool(chosen['passes']),
        'per_frame_synthesis': False,
        'internal_completion_once': True,
        'visible_source_pixels_model_modified': False,
        'exact_final_source_relock_inside_viewfinder': True,
        'controlled_delta': 'V9 learned outside-canvas world removed; source artwork is canonical world; fixed 16:9 safe viewfinder crops the whole Golden Camera Spine; only internal disocclusion remains learned',
        'decision_rule': 'pass if 16:9 keeps the full spine inside the source world with negligible residual while preserving useful XY and Z motion; outside-canvas generation should then leave the main AW path'
    }
    a.report.write_text(json.dumps(rep, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
