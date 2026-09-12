#!/usr/bin/env python3
"""AW-011 V11: clean residuals without expanding the world.

V10 established the production hypothesis: original Doré artwork is the
canonical world, 16:9 is the camera, Golden Camera Spine is XY+Z motion, and
only internal disocclusion may use learned completion. V11 does not add any new
world or generative surface. It separates tiny raster sampling cracks from
true internal disocclusion by (1) increasing reprojection mesh density and
(2) classifying connected residual components inside the fixed 16:9 viewfinder.
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
from experiment_static_cinema_v10 import evaluate_ratio


def render_internal_world(src, dep, irgb, idep, imask, pose, ppu, raster_step):
    h, w = dep.shape
    frame = np.zeros_like(src)
    occupied = np.zeros((h, w), np.uint8)

    iimg, iknown = raster_layer(irgb, idep, pose, ppu, raster_step, None)
    # Keep mask raster consistent with the same mesh density instead of V7's
    # fixed step=5 helper.
    probe = cv2.cvtColor(imask, cv2.COLOR_GRAY2BGR)
    mimg, mknown = raster_layer(probe, idep, pose, ppu, raster_step, None)
    ivis = (mknown > 0) & (mimg[:, :, 0] > 96)
    itake = (iknown > 0) & ivis
    frame[itake] = iimg[itake]
    occupied[itake] = 255

    front, fknown = raster_layer(src, dep, pose, ppu, raster_step, .10)
    frame[fknown > 0] = front[fknown > 0]
    residual = (fknown == 0) & (occupied == 0)
    return frame, residual, fknown, occupied, int(np.count_nonzero(itake))


def classify_components(mask: np.ndarray):
    """Classify residual topology; tiny components are raster-crack candidates."""
    u8 = mask.astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(u8, 8)
    comps = []
    h, w = mask.shape
    for cid in range(1, n):
        x, y, cw, ch, area = [int(v) for v in stats[cid]]
        touches = bool(x == 0 or y == 0 or x + cw >= w or y + ch >= h)
        comps.append({
            'area': area,
            'bbox': [x, y, cw, ch],
            'touches_viewfinder_boundary': touches,
            'kind': 'micro_raster_candidate' if (area <= 12 and not touches) else 'structural_disocclusion',
        })
    return comps


def main():
    ap = argparse.ArgumentParser()
    for k in ('source', 'depth', 'spine', 'output', 'report'):
        ap.add_argument('--' + k, type=Path, required=True)
    ap.add_argument('--support-map', type=Path)
    ap.add_argument('--edge-map', type=Path)
    ap.add_argument('--hidden-depth-map', type=Path)
    ap.add_argument('--residual-map', type=Path)
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
    ap.add_argument('--raster-step', type=int, default=3)
    a = ap.parse_args()

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

    frames, residual_masks, sampled_poses = [], [], []
    internal_pixels = 0
    for i in range(len(poses) - 1):
        p0 = np.asarray(poses[i]['position'], np.float32)
        p1 = np.asarray(poses[i + 1]['position'], np.float32)
        for j in range(a.segment_frames):
            t = smoothstep(j / float(a.segment_frames))
            p = p0 * (1 - t) + p1 * t
            if np.linalg.norm(p) < 1e-6:
                frame = src.copy(); residual = np.zeros(dep.shape, np.bool_); ic = 0
            else:
                frame, residual, _, _, ic = render_internal_world(
                    src, dep, internal.rgb, internal.depth, internal.mask,
                    p, a.ppu, a.raster_step)
            frames.append(frame); residual_masks.append(residual)
            sampled_poses.append([float(x) for x in p]); internal_pixels += ic

    h, w = dep.shape
    chosen = evaluate_ratio(residual_masks, h, w, 16.0/9.0, a.target_residual, a.min_view_scale)
    x0, y0, cw, ch = chosen['rect']

    cropped_masks = [m[y0:y0+ch, x0:x0+cw] for m in residual_masks]
    cropped_residuals = [float(np.count_nonzero(m) / m.size) for m in cropped_masks]
    worst_index = int(np.argmax(cropped_residuals)) if cropped_residuals else -1
    worst_mask = cropped_masks[worst_index] if worst_index >= 0 else np.zeros((ch, cw), np.bool_)
    comps = classify_components(worst_mask)
    micro_pixels = sum(c['area'] for c in comps if c['kind'] == 'micro_raster_candidate')
    structural_pixels = sum(c['area'] for c in comps if c['kind'] == 'structural_disocclusion')

    out_w = a.output_width - (a.output_width % 2)
    out_h = int(round(out_w * 9.0 / 16.0)); out_h -= out_h % 2
    a.output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(a.output), cv2.VideoWriter_fourcc(*'mp4v'), a.fps, (out_w, out_h))
    if not writer.isOpened(): raise RuntimeError('video writer failed')
    for frame in frames:
        crop = frame[y0:y0+ch, x0:x0+cw]
        writer.write(cv2.resize(crop, (out_w, out_h), interpolation=cv2.INTER_CUBIC))
    canonical_crop = src[y0:y0+ch, x0:x0+cw]
    writer.write(cv2.resize(canonical_crop, (out_w, out_h), interpolation=cv2.INTER_CUBIC))
    writer.release()

    if a.residual_map:
        vis = np.zeros((ch, cw), np.uint8); vis[worst_mask] = 255
        a.residual_map.parent.mkdir(parents=True, exist_ok=True); cv2.imwrite(str(a.residual_map), vis)
    if a.viewfinder_preview:
        preview = src.copy(); cv2.rectangle(preview, (x0,y0), (x0+cw-1,y0+ch-1), (255,255,255), 2)
        a.viewfinder_preview.parent.mkdir(parents=True, exist_ok=True); cv2.imwrite(str(a.viewfinder_preview), preview)

    full_residuals = [float(np.count_nonzero(m) / m.size) for m in residual_masks]
    z_values = [p[2] for p in sampled_poses]
    max_final = max(cropped_residuals, default=0.0)
    rep = {
        'status': 'STATIC_CINEMA_V11_CLEANUP_READY_FOR_VISUAL_REVIEW',
        'mode': 'canonical_source_world_plus_internal_completion_dense_raster',
        'camera_spine_semantics': 'golden-line XY trajectory with Z push/pull',
        'canonical_world': 'original_dore_artwork',
        'external_world_generation': False,
        'external_generated_pixels_total': 0,
        'raster_step': a.raster_step,
        'trajectory_samples_used': used,
        'mapped_support_samples': mapped,
        'mean_inverse_projection_error_pixels': inv_err,
        'max_camera_lateral_shift_pixels': shift,
        'camera_conditioned_zone_radius_pixels': radius,
        'z_range': [float(min(z_values, default=0.0)), float(max(z_values, default=0.0))],
        'selected_ratio': '16:9',
        'selected_viewfinder_rect': chosen['rect'],
        'selected_viewfinder_source_fraction': chosen['retained_source_fraction'],
        'max_full_canvas_residual_fraction': max(full_residuals, default=0.0),
        'max_final_viewfinder_residual_fraction': max_final,
        'mean_final_viewfinder_residual_fraction': float(np.mean(cropped_residuals)) if cropped_residuals else 0.0,
        'worst_frame_index': worst_index,
        'worst_frame_pose': sampled_poses[worst_index] if worst_index >= 0 else None,
        'worst_frame_component_count': len(comps),
        'worst_frame_micro_raster_candidate_pixels': micro_pixels,
        'worst_frame_structural_disocclusion_pixels': structural_pixels,
        'worst_frame_components': sorted(comps, key=lambda c: c['area'], reverse=True)[:20],
        'internal_rendered_pixels_total': internal_pixels,
        'viewfinder_gate': bool(chosen['passes']),
        'cleanup_gate': bool(max_final <= 0.0005),
        'per_frame_synthesis': False,
        'deterministic_per_frame_inpaint': False,
        'internal_completion_once': True,
        'visible_source_pixels_model_modified': False,
        'exact_final_source_relock_inside_viewfinder': True,
        'controlled_delta': 'V10 world/camera/completion fixed; only reprojection mesh density changed from step 5 to configurable dense raster plus residual topology diagnostics',
        'decision_rule': 'if dense raster materially reduces residual, classify V10 remainder as rendering debt; only structural components may justify further hidden-world completion work'
    }
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps(rep, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
