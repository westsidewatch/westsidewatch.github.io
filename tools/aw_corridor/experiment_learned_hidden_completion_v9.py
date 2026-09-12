#!/usr/bin/env python3
"""AW-011 V9: learned internal hidden world + learned extended boundary world.

V7 established persistent outside-canvas representation. V8 validated learned
internal hidden RGB+depth. V9 removes the diagnostic reflected border and lets
the same isolated Edge -> Depth -> Color provider complete only the unknown
border of a larger persistent canonical world. Geometry/camera/raster/source
relock remain fixed.
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
from experiment_joint_hidden_completion_v7 import render
from hidden_surface_provider import learned_three_stage_complete, learned_three_stage_extend_canvas


def main():
    ap = argparse.ArgumentParser()
    for k in ('source', 'depth', 'spine', 'output', 'report'):
        ap.add_argument('--' + k, type=Path, required=True)
    ap.add_argument('--support-map', type=Path)
    ap.add_argument('--edge-map', type=Path)
    ap.add_argument('--extended-edge-map', type=Path)
    ap.add_argument('--hidden-depth-map', type=Path)
    ap.add_argument('--extended-world-preview', type=Path)
    ap.add_argument('--networks', type=Path, required=True)
    ap.add_argument('--edge-checkpoint', type=Path, required=True)
    ap.add_argument('--depth-checkpoint', type=Path, required=True)
    ap.add_argument('--color-checkpoint', type=Path, required=True)
    ap.add_argument('--device', default='cpu')
    ap.add_argument('--width', type=int, default=480)
    ap.add_argument('--fps', type=int, default=12)
    ap.add_argument('--segment-frames', type=int, default=4)
    ap.add_argument('--ppu', type=float, default=520.0)
    ap.add_argument('--samples', type=int, default=4)
    ap.add_argument('--behind', type=float, default=.08)
    ap.add_argument('--edge-q', type=float, default=.90)
    ap.add_argument('--min-jump', type=float, default=.055)
    ap.add_argument('--seam-pixels', type=int, default=8)
    a = ap.parse_args()

    for p in (a.networks, a.edge_checkpoint, a.depth_checkpoint, a.color_checkpoint):
        if not p.exists():
            raise FileNotFoundError(p)

    src, dep = prepare(a.source, a.depth, a.width)
    poses = load_pose_points(a.spine)
    shift, radius = camera_lateral_budget(poses, a.ppu)
    support, zmap, used, mapped, inv_err = collect_depth_conditioned_support(dep, poses, a.ppu, a.samples, a.behind)
    topo = nearest_edge_topology(dep, support, a.edge_q, .025, a.min_jump, radius)

    internal = learned_three_stage_complete(
        src, dep, support, zmap, topo,
        a.networks, a.edge_checkpoint, a.depth_checkpoint, a.color_checkpoint, a.device,
    )
    irgb, idep, imask = internal.rgb, internal.depth, internal.mask

    # World size is driven by actual camera demand, not arbitrary generative area.
    pad = max(24, int(np.ceil(shift + 16.0)))
    extended = learned_three_stage_extend_canvas(
        src, dep, pad,
        a.networks, a.edge_checkpoint, a.depth_checkpoint, a.color_checkpoint,
        a.device, seam_pixels=a.seam_pixels,
    )
    ergb, edep, emask = extended.rgb, extended.depth, extended.mask

    for path, img in ((a.support_map, support), (a.edge_map, internal.edge), (a.extended_edge_map, extended.edge)):
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(path), img)
    if a.hidden_depth_map:
        a.hidden_depth_map.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(a.hidden_depth_map), np.uint8(np.clip(idep, 0, 1) * 255))
    if a.extended_world_preview:
        a.extended_world_preview.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(a.extended_world_preview), ergb)

    h, w = dep.shape
    a.output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(a.output), cv2.VideoWriter_fourcc(*'mp4v'), a.fps, (w, h))
    if not writer.isOpened():
        raise RuntimeError('video writer failed')

    unseen = []; coverage = []; residual = []; bmean = []; b95 = []
    icount = ecount = 0
    worst = {'fraction': -1.0, 'frame': -1, 'pose': None}
    fn = 0
    for i in range(len(poses) - 1):
        p0 = np.asarray(poses[i]['position'], np.float32)
        p1 = np.asarray(poses[i + 1]['position'], np.float32)
        for j in range(a.segment_frames):
            t = smoothstep(j / float(a.segment_frames))
            p = p0 * (1 - t) + p1 * t
            if np.linalg.norm(p) < 1e-6:
                writer.write(src); fn += 1; continue
            frame, u, c, r, fk, occ, ic, ec = render(
                src, dep, irgb, idep, imask, ergb, edep, emask, pad, p, a.ppu
            )
            bm, bp = boundary_discontinuity(frame, fk, occ)
            writer.write(frame)
            unseen.append(u); coverage.append(c); residual.append(r)
            bmean.append(bm); b95.append(bp); icount += ic; ecount += ec
            if r > worst['fraction']:
                worst = {'fraction': r, 'frame': fn, 'pose': [float(x) for x in p]}
            fn += 1
    writer.write(src)
    writer.release()

    maxu = max(unseen, default=0.0)
    maxr = max(residual, default=0.0)
    cov = float(np.mean([c / u if u > 1e-9 else 1.0 for c, u in zip(coverage, unseen)])) if unseen else 1.0
    rep = {
        'status': 'LEARNED_CANONICAL_WORLD_READY_FOR_VISUAL_REVIEW',
        'mode': 'fixed_v7_geometry_plus_learned_internal_and_extended_world',
        'internal_provider': internal.provider,
        'extended_world_provider': extended.provider,
        'trajectory_samples_used': used,
        'mapped_support_samples': mapped,
        'mean_inverse_projection_error_pixels': inv_err,
        'support_fraction': float(np.count_nonzero(support) / support.size),
        'max_camera_lateral_shift_pixels': shift,
        'camera_conditioned_zone_radius_pixels': radius,
        'extended_canvas_pad_pixels': pad,
        'generated_extended_fraction_of_world': float(np.count_nonzero(emask) / emask.size),
        'max_foreground_unseen_fraction': maxu,
        'mean_hidden_layer_coverage_ratio': cov,
        'max_residual_uncovered_fraction': maxr,
        'mean_hidden_boundary_discontinuity': float(np.mean(bmean)) if bmean else 0.0,
        'max_hidden_boundary_discontinuity_q95': max(b95, default=0.0),
        'internal_rendered_pixels_total': icount,
        'extended_boundary_rendered_pixels_total': ecount,
        'worst_residual': worst,
        'per_frame_synthesis': False,
        'canonical_world_completion_once': True,
        'world_size_driven_by_camera_demand': True,
        'reflection_extended_world_removed': True,
        'visible_source_pixels_model_modified': False,
        'exact_final_source_relock': True,
        'coverage_gate': bool(maxu > .001 and cov >= .955 and maxr <= .005),
        'visual_gate': 'PENDING_HUMAN_REVIEW',
        'controlled_delta': 'V8 geometry/topology/camera/internal learned provider fixed; V7 reflected border replaced by one persistent learned border world with narrow seam admission',
        'decision_rule': 'pass when left reflected band disappears, right camel/rider hidden world remains coherent, no black holes appear, and source relock/coverage remain stable'
    }
    a.report.write_text(json.dumps(rep, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
