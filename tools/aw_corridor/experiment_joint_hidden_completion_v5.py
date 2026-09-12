#!/usr/bin/env python3
"""AW-011 V5: joint hidden color+depth completion.

Measured trigger
----------------
The nearest-edge topology probe attached 100% of demanded support to occlusion
structure, yet hidden coverage remained ~9% and residual uncovered world ~11.6%.
Therefore topology assignment alone is insufficient. This experiment keeps the
same Camera Spine, MoGe depth, geometric support, inverse projection and edge
classification, but changes the hidden-world representation from a cut surface
into one persistent jointly-completed background surface.

The test is deliberately narrow:
- topology still determines where hidden world belongs;
- hidden colour and hidden depth are completed together once in canonical space;
- the completed hidden surface is rendered persistently for every camera pose;
- no per-frame synthesis is allowed;
- the Doré front layer remains authoritative and final source relock is exact.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from experiment_depth_traversal import prepare, load_pose_points, smoothstep
from experiment_depth_banded_world_cache import collect_depth_conditioned_support
from experiment_edge_aware_hidden_surface_v4 import (
    camera_lateral_budget,
    nearest_edge_topology,
    boundary_discontinuity,
)
from experiment_world_cache import raster_layer


def complete_hidden_world(src, dep, support, zmap, topo, behind_margin=.025):
    """Create one persistent background RGB+depth surface behind occluders."""
    demanded = support > 0
    if not np.any(demanded):
        return src.copy(), dep.copy(), support.copy()

    # Give the hidden world enough support for triangle rasterization without
    # globally growing the world. The expansion remains local to demanded world.
    mask = cv2.dilate(
        support,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)),
        iterations=1,
    )
    m = mask > 0

    # Depth completion: start from geometrically recovered hidden samples.
    # Missing support receives a locally completed hidden depth. The entire
    # completed support is forced behind the local visible/background estimate.
    local_min = topo['local_min']
    target_back = np.clip(local_min - behind_margin, 0.0, 1.0).astype(np.float32)
    hidden = np.zeros_like(dep, np.float32)
    have = (zmap > 0) & m
    hidden[have] = np.minimum(zmap[have], target_back[have])

    # Seed unobserved demanded pixels with the local background hypothesis, then
    # jointly smooth only inside the hidden region. This creates a continuous
    # background manifold instead of a set of disconnected depth islands.
    hidden[m & (~have)] = target_back[m & (~have)]
    hidden_seed = hidden.copy()
    # Edge-aware smoothing on the hidden sheet: bilateral preserves large
    # structural depth changes while removing raster-scale depth spikes.
    smooth = cv2.bilateralFilter(hidden_seed, 9, 0.06, 9.0)
    hidden[m] = smooth[m]
    hidden[m] = np.minimum(hidden[m], target_back[m])
    hidden = np.clip(hidden, 0.0, 1.0)

    # Colour completion uses the same hidden mask and masks out the foreground
    # side of owning occlusion zones, preventing foreground silhouettes from
    # bleeding into revealed background. It is generated once, persistently.
    foreground = topo['foreground'] > 0
    near = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))) > 0
    completion = m | (foreground & near)
    rgb = cv2.inpaint(src, completion.astype(np.uint8) * 255, 7.0, cv2.INPAINT_TELEA)

    # Carrier depth outside hidden support stays the original Doré depth so the
    # rasterizer has valid geometry, but only the hidden mask is admitted later.
    hdep = dep.copy().astype(np.float32)
    hdep[m] = hidden[m]
    return rgb, hdep, mask


def raster_support(mask, depth, pose, ppu):
    probe = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    warped, known = raster_layer(probe, depth, pose, ppu, 5, None)
    return (known > 0) & (warped[:, :, 0] > 96)


def render(src, dep, hidden_rgb, hidden_depth, hidden_mask, pose, ppu=520.0):
    h, w = dep.shape
    frame = np.zeros_like(src)
    occupied = np.zeros((h, w), np.uint8)

    # The hidden world is now one continuous background sheet. Do not sever it
    # again at front-layer depth discontinuities; front/background separation is
    # enforced by compositing the authoritative Doré front layer last.
    himg, hknown = raster_layer(hidden_rgb, hidden_depth, pose, ppu, 5, None)
    hvis = raster_support(hidden_mask, hidden_depth, pose, ppu)
    htake = (hknown > 0) & hvis
    frame[htake] = himg[htake]
    occupied[htake] = 255

    front, front_known = raster_layer(src, dep, pose, ppu, 5, .10)
    ft = front_known > 0
    frame[ft] = front[ft]

    residual = (front_known == 0) & (occupied == 0)
    frame[residual] = 0
    unseen = float(np.count_nonzero(front_known == 0) / front_known.size)
    res = float(np.count_nonzero(residual) / front_known.size)
    cov = max(0.0, unseen - res)
    return frame, unseen, cov, res, front_known, occupied


def main():
    ap = argparse.ArgumentParser()
    for k in ('source', 'depth', 'spine', 'output', 'report'):
        ap.add_argument('--' + k, type=Path, required=True)
    ap.add_argument('--support-map', type=Path)
    ap.add_argument('--edge-map', type=Path)
    ap.add_argument('--hidden-depth-map', type=Path)
    ap.add_argument('--width', type=int, default=480)
    ap.add_argument('--fps', type=int, default=12)
    ap.add_argument('--segment-frames', type=int, default=4)
    ap.add_argument('--ppu', type=float, default=520.0)
    ap.add_argument('--samples', type=int, default=4)
    ap.add_argument('--behind', type=float, default=.08)
    ap.add_argument('--edge-q', type=float, default=.90)
    ap.add_argument('--min-jump', type=float, default=.055)
    a = ap.parse_args()

    src, dep = prepare(a.source, a.depth, a.width)
    poses = load_pose_points(a.spine)
    shift, radius = camera_lateral_budget(poses, a.ppu)
    support, zmap, used, mapped, inv_err = collect_depth_conditioned_support(
        dep, poses, a.ppu, a.samples, a.behind)
    topo = nearest_edge_topology(dep, support, a.edge_q, .025, a.min_jump, radius)
    hidden_rgb, hidden_depth, hidden_mask = complete_hidden_world(src, dep, support, zmap, topo)

    for path, image in ((a.support_map, support), (a.edge_map, topo['edge'])):
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(path), image)
    if a.hidden_depth_map:
        a.hidden_depth_map.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(a.hidden_depth_map), np.uint8(np.clip(hidden_depth, 0, 1) * 255))

    h, w = src.shape[:2]
    a.output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(a.output), cv2.VideoWriter_fourcc(*'mp4v'), a.fps, (w, h))
    if not writer.isOpened():
        raise RuntimeError('video writer failed')

    unseen = []
    coverage = []
    residual = []
    bmean = []
    b95 = []
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
            frame, u, c, r, fk, occ = render(src, dep, hidden_rgb, hidden_depth, hidden_mask, p, a.ppu)
            bm, bp = boundary_discontinuity(frame, fk, occ)
            writer.write(frame)
            unseen.append(u); coverage.append(c); residual.append(r); bmean.append(bm); b95.append(bp)
            if r > worst['fraction']:
                worst = {'fraction': r, 'frame': fn, 'pose': [float(x) for x in p]}
            fn += 1
    writer.write(src)
    writer.release()

    maxu = max(unseen, default=0.0)
    maxr = max(residual, default=0.0)
    cov = float(np.mean([c/u if u > 1e-9 else 1.0 for c, u in zip(coverage, unseen)])) if unseen else 1.0
    report = {
        'status': 'JOINT_HIDDEN_COLOR_DEPTH_READY_FOR_VISUAL_REVIEW',
        'mode': 'persistent_joint_hidden_color_depth_completion',
        'trigger': 'topology assignment reached 1.0 but coverage remained insufficient',
        'trajectory_samples_used': used,
        'mapped_support_samples': mapped,
        'mean_inverse_projection_error_pixels': inv_err,
        'support_fraction': float(np.count_nonzero(support) / support.size),
        'max_camera_lateral_shift_pixels': shift,
        'camera_conditioned_zone_radius_pixels': radius,
        'support_attached_to_occlusion_topology_ratio': float(np.count_nonzero(topo['relevant_support']) / max(1, np.count_nonzero(support))),
        'max_foreground_unseen_fraction': maxu,
        'mean_hidden_layer_coverage_ratio': cov,
        'max_residual_uncovered_fraction': maxr,
        'mean_hidden_boundary_discontinuity': float(np.mean(bmean)) if bmean else 0.0,
        'max_hidden_boundary_discontinuity_q95': max(b95, default=0.0),
        'worst_residual': worst,
        'persistent_surface_count': 1,
        'joint_color_depth_completion': True,
        'per_frame_synthesis': False,
        'exact_final_source_relock': True,
        'coverage_gate': bool(maxu > .001 and cov >= .96 and maxr <= .003),
        'visual_gate': 'PENDING_HUMAN_REVIEW',
        'decision_rule': 'if large holes collapse but seams/appearance remain, topology is retained and learned/local joint completion is next; if holes persist, hidden geometry itself is still invalid'
    }
    a.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
